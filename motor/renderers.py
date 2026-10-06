"""Los renderers: VideoSpec resuelto → video mudo.

Hoy hay uno, `PlaywrightRenderer` (Chromium dibuja la entrada y la salida de cada escena, ffmpeg
sostiene lo del medio y luego le aplica la cámara y los fundidos). Remotion no se incluye: pide
licencia de pago a empresas (ver `ARCHITECTURE.md`, sección 5.1). Un renderer nuevo solo tiene
que cumplir `VideoRenderer` (`motor/proveedores.py`) y registrarse en `RENDERERS`.
"""

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


RENDERERS = {PlaywrightRenderer.nombre: PlaywrightRenderer}
RENDERER_DEFECTO = PlaywrightRenderer.nombre


def renderer(nombre: str | None = None):
    return RENDERERS.get(nombre or RENDERER_DEFECTO, RENDERERS[RENDERER_DEFECTO])()
