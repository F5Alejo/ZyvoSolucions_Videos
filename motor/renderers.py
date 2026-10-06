"""Los renderers: VideoSpec resuelto → video mudo.

- `HyperFramesRenderer` (el de por defecto): el video entero como una composición HyperFrames,
  con un momento visual por frase de la voz (motor/direccion.py, motor/hyperframes/).
- `PlaywrightRenderer` (el de respaldo): Chromium dibuja la entrada y la salida de cada escena, ffmpeg
  sostiene lo del medio y luego le aplica la cámara y los fundidos.

Remotion no se incluye: pide licencia de pago a empresas (ver `docs/plan-migracion.md`, sección 5.1).
Un renderer nuevo solo tiene que cumplir `VideoRenderer` (`motor/proveedores.py`) y registrarse en `RENDERERS`.
"""

import shutil
import subprocess
from pathlib import Path

from motor import camara, escenas, render, videospec


def _fundidos(spec: videospec.VideoSpec) -> list[tuple[bool, bool]]:
    """(entra con fundido, sale con fundido) de cada escena. La transición de una escena es hacia la siguiente."""
    es = spec.escenas
    return [(i > 0 and es[i - 1].transicion == "fundido", i < len(es) - 1 and e.transicion == "fundido")
            for i, e in enumerate(es)]


def escenas_html(spec: videospec.VideoSpec) -> list[tuple]:
    """(html, cuadros, entrada, salida, huella) de cada escena."""
    v, fps = spec.video, spec.video.fps
    salida = []
    for e, (entra, sale) in zip(spec.escenas, _fundidos(spec)):
        html = escenas.html(e.vista, spec.estilo, v.formato, spec.voz.solo_borrador, e.animacion, e.cuadros / fps)
        huella = videospec.huella(html, e.cuadros, e.entrada, e.salida, fps, v.escala, v.crf, v.preset,
                                  e.camara, entra, sale, camara.ZOOM, camara.PANEO, camara.FUNDIDO)
        salida.append((html, e.cuadros, e.entrada, e.salida, huella))
    return salida


class PlaywrightRenderer:
    nombre = "playwright"
    descripcion = "Navegador (Chromium) y ffmpeg"

    def render(self, spec: videospec.VideoSpec, cache: Path, tmp: Path, avisar=lambda hechas, total: None) -> tuple[Path, list[dict]]:
        """Dibuja (o toma de `cache`) cada escena y las une en `tmp/mudo.mp4`. Devuelve el video y el encuadre."""
        v = spec.video
        lista = escenas_html(spec)
        fundidos = _fundidos(spec)

        def posproceso(i: int, parte: Path, trabajo: Path) -> Path:
            e = spec.escenas[i]
            entra, sale = fundidos[i]
            return camara.aplicar(parte, trabajo / f"camara-{i:03d}.mp4", e.camara, entra, sale, e.cuadros,
                                  v.ancho_real, v.alto_real, v.fps, spec.estilo["fondo"], v.crf, v.preset)

        mudo = tmp / "mudo.mp4"
        encuadre = render.video(lista, v.ancho, v.alto, mudo, tmp / "escenas", avisar=avisar, fps=v.fps,
                                escala=v.escala, crf=v.crf, preset=v.preset, cache=cache, posproceso=posproceso)
        # Las escenas que ya no usa el video (se editó la lámina) no se guardan para siempre.
        vigentes = {x[4] for x in lista}
        for viejo in cache.glob("*.*"):
            if viejo.stem not in vigentes:
                viejo.unlink()
        return mudo, encuadre


def _cuadros(video: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(video)], capture_output=True, text=True)
    return int((r.stdout or "0").strip() or 0)


class HyperFramesRenderer:
    """El video entero como una composición HyperFrames: texto cinético al ritmo de la voz y tomas de fondo.

    Necesita los momentos de cada escena (`Escena.beats`, de motor/direccion.py). El video se
    guarda en `cache` con la huella de su composición: si nada cambió, no se vuelve a renderizar.
    """
    nombre = "hyperframes"
    descripcion = "HyperFrames: texto cinético al ritmo de la voz, con tomas del banco de la empresa"

    def render(self, spec: videospec.VideoSpec, cache: Path, tmp: Path, avisar=lambda hechas, total: None) -> tuple[Path, list[dict]]:
        from motor import hyperframes
        if any(e.narracion and not e.beats for e in spec.escenas):
            raise ValueError("El video no tiene dirección (momentos por escena): falta la etapa del Director")
        v = spec.video
        proyecto = tmp / "hyperframes"
        shutil.rmtree(proyecto, ignore_errors=True)
        indice, usados = hyperframes.componer(spec, proyecto)
        cache.mkdir(parents=True, exist_ok=True)
        guardado = cache / f"hf-{hyperframes.huella(indice, usados, spec)}.mp4"
        cuadros = sum(e.cuadros for e in spec.escenas)
        if not guardado.exists():
            crudo = proyecto / "render.mp4"
            avisar(0, 1)
            hyperframes.renderizar(proyecto, crudo, v.fps, v.crf, cuadros / v.fps, avisar=avisar)
            nuevo = cache / f"{guardado.stem}.tmp.mp4"
            if v.escala == 1 and _cuadros(crudo) == cuadros:
                shutil.move(str(crudo), nuevo)
            else:  # la voz manda: exactamente los cuadros del VideoSpec, y al tamaño pedido
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-an",
                                "-vf", f"scale={v.ancho_real}:{v.alto_real}:flags=lanczos,tpad=stop_mode=clone:stop=-1",
                                "-frames:v", str(cuadros), "-c:v", "libx264", "-crf", v.crf, "-preset", v.preset,
                                "-pix_fmt", "yuv420p", str(nuevo)], check=True)
            nuevo.replace(guardado)
            for viejo in cache.glob("hf-*.mp4"):
                if viejo != guardado:
                    viejo.unlink(missing_ok=True)
        mudo = tmp / "mudo.mp4"
        shutil.copy2(guardado, mudo)
        return mudo, []


RENDERERS = {PlaywrightRenderer.nombre: PlaywrightRenderer, HyperFramesRenderer.nombre: HyperFramesRenderer}
RENDERER_DEFECTO = HyperFramesRenderer.nombre
RENDERER_RESPALDO = PlaywrightRenderer.nombre  # si a este equipo le falta Node o HyperFrames


def renderer(nombre: str | None = None):
    """El renderer pedido; si es HyperFrames y este equipo no lo tiene, el de respaldo."""
    nombre = nombre if nombre in RENDERERS else RENDERER_DEFECTO
    if nombre == HyperFramesRenderer.nombre:
        from motor import hyperframes
        if hyperframes.disponible():
            nombre = RENDERER_RESPALDO
    return RENDERERS[nombre]()
