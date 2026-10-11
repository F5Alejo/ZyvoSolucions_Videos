"""Los renderers: VideoSpec resuelto → video mudo.

Hay dos, y la diferencia no es de qué herramienta usan sino de **qué sale en el video**:

| | `playwright` | `hyperframes` |
|---|---|---|
| La lámina | se **rearma** con la plantilla de la marca | se **redibuja** como está en el PPTX |
| Los cuadros | la entrada y la salida; el medio va congelado | todos, buscando cada instante |
| Los elementos | entran al principio de la lámina | van entrando mientras habla la voz |
| Cuesta | segundos por lámina | minutos por video |

El de siempre (`playwright`) sirve cuando la presentación es pobre y conviene rehacerla con la
identidad de la marca. El fiel (`hyperframes`) sirve cuando la presentación ya está diseñada y
lo que se quiere es animarla, que es el caso de los cursos de RiskMann.

Remotion no se incluye: pide licencia de pago a empresas (ver `docs/plan-migracion.md`, 5.1).
Un renderer nuevo solo tiene que cumplir `VideoRenderer` (`motor/proveedores.py`) y registrarse
en `RENDERERS`.
"""

from pathlib import Path

from motor import camara, escenas, hyperframes, render, videospec
from motor.escenas import lamina as mod_lamina


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


class HyperFramesRenderer:
    """La diapositiva, animada: redibuja cada lámina del PPTX y revela sus formas con la voz."""

    nombre = "hyperframes"
    descripcion = "Animar la diapositiva (HyperFrames)"

    def render(self, spec: videospec.VideoSpec, cache: Path, tmp: Path,
               avisar=lambda hechas, total: None) -> tuple[Path, list[dict]]:
        v = spec.video
        proyecto = hyperframes.preparar(tmp / "hf", spec.clave)
        hyperframes.copiar_recursos(proyecto, mod_lamina.FUENTE, self._media(spec))

        laminas, archivos, t = [], {}, 0.0
        for e in spec.escenas:
            dur = e.cuadros / v.fps
            cid = f"lamina{e.lamina}"
            archivo = f"compositions/{e.id}.html"
            archivos[archivo] = mod_lamina.composicion(
                e.formas, e.narracion, dur, cid, v.ancho, v.alto, spec.escala_pt,
                media="assets/media/", plan=e.animacion,
                fuente=f"assets/fuentes/{mod_lamina.FUENTE.name}",
                fondo=e.fondo_lamina or spec.estilo.get("fondo"),
                inicio_escena=e.inicio or 0.0,
                acento=spec.estilo.get("acento"))
            laminas.append({"n": e.lamina, "cid": cid, "archivo": archivo,
                            "inicio": round(t, 3), "duracion": round(dur, 3)})
            t += dur
            avisar(len(laminas), len(spec.escenas) + 1)

        hyperframes.escribir(proyecto, mod_lamina.indice(laminas, v.ancho, v.alto, t,
                                                         spec.estilo.get("fondo", "#000000")), archivos)
        # `check` revisa la composición antes de gastar minutos dibujándola: encuentra
        # desbordes, solapes y contrastes bajos que a simple vista se escapan. No aborta el
        # render —un aviso no es motivo para quedarse sin video—, pero queda en el informe.
        problemas = [{"escena": -1, "detalle": x} for x in hyperframes.revisar(proyecto)]
        mudo = hyperframes.render(proyecto, tmp / "mudo.mp4", fps=v.fps,
                                  calidad="draft" if v.crf == "23" else "looks")
        avisar(len(spec.escenas) + 1, len(spec.escenas) + 1)
        return mudo, problemas

    @staticmethod
    def _media(spec: videospec.VideoSpec) -> Path | None:
        from app import taller
        carpeta = taller.ruta_trabajo(spec.trabajo).parent / "media"
        return carpeta if carpeta.exists() else None


RENDERERS = {PlaywrightRenderer.nombre: PlaywrightRenderer,
             HyperFramesRenderer.nombre: HyperFramesRenderer}
RENDERER_DEFECTO = PlaywrightRenderer.nombre


def renderer(nombre: str | None = None):
    return RENDERERS.get(nombre or RENDERER_DEFECTO, RENDERERS[RENDERER_DEFECTO])()
