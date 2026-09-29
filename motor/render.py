"""Escenas HTML → video mudo H.264, con Playwright (Chromium) y ffmpeg.

Por cada escena se dibujan cuadro a cuadro solo los primeros `DURACION_ENTRADA` segundos (la
animación de entrada), llevando cada animación CSS a su instante exacto: el resultado es el
mismo en cada render. El resto de la escena es el último cuadro sostenido por ffmpeg, así que
una lámina de 40 s cuesta lo mismo que una de 5 s.
"""

import math
import shutil
import subprocess
from pathlib import Path

from motor.escenas import DURACION_ENTRADA

FPS = 30
CODIFICAR = ["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "18",
             "-preset", "medium", "-r", str(FPS), "-g", str(FPS * 2)]

_IR_A = """(ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }"""
_LISTO = """async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
}"""


def cuadros(segundos: float) -> int:
    return max(1, round(segundos * FPS))


def video(escenas: list[tuple[str, int]], ancho: int, alto: int, destino: Path, trabajo: Path,
          avisar=lambda hechas, total: None) -> None:
    """`escenas`: (html, cuadros) por escena. Escribe `destino` (mp4 sin audio)."""
    from playwright.sync_api import sync_playwright

    trabajo.mkdir(parents=True, exist_ok=True)
    entrada = math.ceil(DURACION_ENTRADA * FPS)
    partes = []
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={"width": ancho, "height": alto}, device_scale_factor=1)
        for i, (html, total) in enumerate(escenas):
            carpeta = trabajo / f"escena-{i:03d}"
            carpeta.mkdir(exist_ok=True)
            pagina_html = carpeta / "escena.html"
            pagina_html.write_text(html, encoding="utf-8")
            pagina.goto(pagina_html.resolve().as_uri())
            pagina.evaluate(_LISTO)
            dibujar = min(entrada, total)
            for f in range(dibujar):
                pagina.evaluate(_IR_A, f * 1000 / FPS)
                pagina.screenshot(path=str(carpeta / f"{f:04d}.png"))
            parte = trabajo / f"parte-{i:03d}.mp4"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(carpeta / "%04d.png"),
                 "-vf", f"tpad=stop_mode=clone:stop={total - dibujar}", "-frames:v", str(total),
                 *CODIFICAR, "-an", str(parte)], check=True)
            shutil.rmtree(carpeta)
            partes.append(parte)
            avisar(i + 1, len(escenas))
        navegador.close()

    lista = trabajo / "partes.txt"
    lista.write_text("".join(f"file '{x.name}'\n" for x in partes), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(destino)], check=True)


def unir(video_mudo: Path, audio: Path, destino: Path) -> None:
    """Video + narración → MP4 final: AAC 48 kHz 192 kbps y `faststart` para la web."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video_mudo), "-i", str(audio),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", "-shortest", str(destino)], check=True)
