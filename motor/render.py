"""Escenas HTML → video mudo H.264, con Playwright (Chromium) y ffmpeg.

Por cada escena se dibujan cuadro a cuadro solo la **entrada** (sus primeros segundos) y la
**salida** (sus últimos), llevando cada animación CSS a su instante exacto: el resultado es el
mismo en cada render. Entre una y otra no se mueve nada, así que ffmpeg sostiene el último
cuadro de la entrada: una lámina de 40 s cuesta lo mismo que una de 5 s.

Al terminar la entrada se revisa el encuadre: si algún texto se sale de la pantalla o de su
caja, se informa (el control de calidad lo muestra como «Todo el texto cabe»).
"""

import json
import math
import shutil
import subprocess
from pathlib import Path

FPS = 30  # por defecto; la configuración puede pedir 25 o 60


def codificar(fps: int = FPS, crf: str = "18", preset: str = "medium") -> list[str]:
    return ["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", crf,
            "-preset", preset, "-r", str(fps), "-g", str(fps * 2)]


_IR_A = """(ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }"""
_LISTO = """async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
}"""
# Qué texto se sale de la pantalla o de su caja (con todo ya en su sitio).
_ENCUADRE = """() => {
  const W = innerWidth, H = innerHeight, fuera = [];
  const nombre = (el) => (el.textContent || el.className).trim().slice(0, 50);
  for (const el of document.querySelectorAll("h1, li, .kicker, .serie, .foto")) {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.bottom > H - 14 || r.left < -1 || r.top < -1)) fuera.push("se sale de la pantalla: " + nombre(el));
  }
  const cuerpo = document.querySelector(".cuerpo");
  const sobra = cuerpo ? cuerpo.scrollHeight - cuerpo.clientHeight : 0;
  if (sobra > 2) fuera.push("el texto no cabe en la lámina (sobran " + sobra + " px)");
  return fuera;
}"""


def cuadros(segundos: float, fps: int = FPS) -> int:
    return max(1, round(segundos * fps))


def video(escenas: list[tuple], ancho: int, alto: int, destino: Path, trabajo: Path,
          avisar=lambda hechas, total: None, fps: int = FPS, escala: float = 1.0,
          crf: str = "18", preset: str = "medium", cache: Path | None = None,
          posproceso=None) -> list[dict]:
    """Escribe `destino` (mp4 sin audio) y devuelve los problemas de encuadre encontrados.

    `escenas`: (html, cuadros) o (html, cuadros, segundos_de_entrada, segundos_de_salida[, huella]).
    El HTML siempre se diseña en el lienzo `ancho`×`alto`; `escala` lo dibuja más pequeño
    (p. ej. 2/3 para 720p) sin cambiar la composición.

    Con `cache` y una `huella` por escena, cada escena dibujada se guarda como `<huella>.mp4` (y sus
    problemas de encuadre en `<huella>.json`): si la escena no cambió, no se vuelve a dibujar.
    `posproceso(i, parte, trabajo)` puede transformar la parte de la escena `i` (cámara, transición)
    antes de guardarla.
    """
    trabajo.mkdir(parents=True, exist_ok=True)
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
    partes: list[Path | None] = [None] * len(escenas)
    problemas: list[dict] = []
    faltan = []
    for i, escena in enumerate(escenas):
        huella = escena[4] if len(escena) > 4 else None
        if cache is not None and huella and (cache / f"{huella}.mp4").exists() and (cache / f"{huella}.json").exists():
            partes[i] = cache / f"{huella}.mp4"
            problemas += [{"escena": i, "detalle": x} for x in json.loads((cache / f"{huella}.json").read_text(encoding="utf-8"))]
            avisar(i + 1, len(escenas))
        else:
            faltan.append(i)

    if faltan:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": ancho, "height": alto}, device_scale_factor=escala)
            for i in faltan:
                escena = escenas[i]
                parte, encuadre = _dibujar(pagina, i, escena, trabajo, fps, crf, preset)
                if posproceso is not None:
                    parte = posproceso(i, parte, trabajo) or parte
                huella = escena[4] if len(escena) > 4 else None
                if cache is not None and huella:
                    guardada = cache / f"{huella}.mp4"
                    if guardada.exists():  # otro render en paralelo dibujó la misma escena
                        Path(parte).unlink(missing_ok=True)
                    else:
                        shutil.move(str(parte), guardada)
                    (cache / f"{huella}.json").write_text(json.dumps(encuadre, ensure_ascii=False), encoding="utf-8")
                    parte = guardada
                partes[i] = parte
                problemas += [{"escena": i, "detalle": x} for x in encuadre]
                avisar(len([x for x in partes if x]), len(escenas))
            navegador.close()

    lista = trabajo / "partes.txt"
    lista.write_text("".join(f"file '{x.resolve().as_posix()}'\n" for x in partes), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(destino)], check=True)
    return sorted(problemas, key=lambda x: x["escena"])


def _dibujar(pagina, i: int, escena: tuple, trabajo: Path, fps: int, crf: str, preset: str) -> tuple[Path, list[str]]:
    """Dibuja una escena: la entrada y la salida cuadro a cuadro; ffmpeg sostiene lo del medio."""
    html, total = escena[0], escena[1]
    ent_s = escena[2] if len(escena) > 2 else 1.2
    sal_s = escena[3] if len(escena) > 3 else 0.0
    carpeta = trabajo / f"escena-{i:03d}"
    shutil.rmtree(carpeta, ignore_errors=True)
    (carpeta / "e").mkdir(parents=True, exist_ok=True)
    (carpeta / "x").mkdir(exist_ok=True)
    pagina_html = carpeta / "escena.html"
    pagina_html.write_text(html, encoding="utf-8")
    pagina.goto(pagina_html.resolve().as_uri())
    pagina.evaluate(_LISTO)

    a = min(total, math.ceil(ent_s * fps) + 1)
    b = min(total - a, math.ceil(sal_s * fps) + 1) if sal_s > 0 else 0
    if total - a - b < 2:  # escena corta: se dibuja entera
        a, b = total, 0
    for f in range(a):
        pagina.evaluate(_IR_A, f * 1000 / fps)
        pagina.screenshot(path=str(carpeta / "e" / f"{f:04d}.png"))
    pagina.evaluate(_IR_A, ent_s * 1000)
    encuadre = list(pagina.evaluate(_ENCUADRE))
    for j, f in enumerate(range(total - b, total)):
        pagina.evaluate(_IR_A, f * 1000 / fps)
        pagina.screenshot(path=str(carpeta / "x" / f"{j:04d}.png"))

    parte = trabajo / f"parte-{i:03d}.mp4"
    entradas = ["-framerate", str(fps), "-i", str(carpeta / "e" / "%04d.png")]
    if b:
        entradas += ["-framerate", str(fps), "-i", str(carpeta / "x" / "%04d.png")]
        filtro = f"[0:v]tpad=stop_mode=clone:stop={total - a - b}[m];[m][1:v]concat=n=2:v=1:a=0[v]"
    else:
        filtro = f"[0:v]tpad=stop_mode=clone:stop={total - a}[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", filtro, "-map", "[v]",
                    "-frames:v", str(total), *codificar(fps, crf, preset), "-an", str(parte)], check=True)
    shutil.rmtree(carpeta)
    return parte, encuadre


def unir(video_mudo: Path, audio: Path, destino: Path) -> None:
    """Video + narración → MP4 final: AAC 48 kHz 192 kbps y `faststart` para la web."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video_mudo), "-i", str(audio),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", "-shortest", str(destino)], check=True)


def quemar_subtitulos(mp4: Path, srt: Path, trabajo: Path, fps: int = FPS, crf: str = "18",
                      preset: str = "medium") -> None:
    """Dibuja los subtítulos dentro de la imagen (para redes, donde se ve sin sonido). Reemplaza `mp4`.

    El filtro `subtitles` de ffmpeg no acepta bien rutas de Windows («C:»): se trabaja con
    rutas relativas dentro de `trabajo`, con la fuente Montserrat al lado.
    """
    from motor.escenas import FUENTE

    trabajo.mkdir(parents=True, exist_ok=True)
    shutil.copy(srt, trabajo / "subs.srt")
    (trabajo / "fuentes").mkdir(exist_ok=True)
    shutil.copy(FUENTE, trabajo / "fuentes" / FUENTE.name)
    estilo = ("FontName=Montserrat,FontSize=20,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,"
              "BorderStyle=3,Outline=6,Shadow=0,MarginV=36,Alignment=2")
    salida = trabajo / "con-subtitulos.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4.resolve()),
                    "-vf", f"subtitles=subs.srt:fontsdir=fuentes:force_style='{estilo}'",
                    *codificar(fps, crf, preset), "-c:a", "copy", "-movflags", "+faststart", salida.name],
                   check=True, cwd=trabajo)
    salida.replace(mp4)
