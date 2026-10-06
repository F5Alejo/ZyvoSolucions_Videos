"""Estilos: cómo se ve y cómo suena un video, en una sola elección («Educativo», «Social»…).

Cada estilo vive en `datos/estilos/<id>.json` (con versión) y solo combina cosas que ya están en
los catálogos: una plantilla de animación, una cámara, una transición, si los subtítulos van
dentro de la imagen, si hay efectos de sonido, la energía de la música y un formato sugerido.

Aplicar un estilo escribe esas elecciones en el curso; después la persona puede cambiar cualquier
cosa por lámina. El estilo no inventa nada: si un archivo de estilo pide algo que no existe, no se carga.
"""

import json

from app import configuracion, datos
from motor import catalogo
from motor.escenas import animacion

ENERGIAS = {"calmada": "Calmada", "media": "Media", "energica": "Enérgica"}
MODOS_SFX = (None, "sutil")


class EstiloInvalido(ValueError):
    pass


def _carpeta():
    return datos.RAIZ_DATOS / "estilos"


def validar(e: dict) -> dict:
    if not e.get("id") or not e.get("nombre"):
        raise EstiloInvalido("El estilo necesita id y nombre")
    reglas = [("animacion", animacion.plantillas()), ("camara", catalogo.CAMARA), ("transicion", catalogo.TRANSICION),
              ("formato", {"16:9", "9:16", "1:1", "4:5"})]
    for campo, permitidos in reglas:
        if e.get(campo) not in permitidos:
            raise EstiloInvalido(f"Estilo «{e['id']}»: {campo} «{e.get(campo)}» no está en el catálogo")
    if e.get("sfx") not in MODOS_SFX:
        raise EstiloInvalido(f"Estilo «{e['id']}»: efectos «{e.get('sfx')}» no existe")
    if e.get("musica") is not None and e["musica"] not in ENERGIAS:
        raise EstiloInvalido(f"Estilo «{e['id']}»: música «{e['musica']}» no existe")
    if not isinstance(e.get("subtitulos_quemados"), bool):
        raise EstiloInvalido(f"Estilo «{e['id']}»: subtitulos_quemados tiene que ser sí o no")
    return e


def estilos() -> dict[str, dict]:
    salida = {}
    carpeta = _carpeta()
    if carpeta.exists():
        for f in sorted(carpeta.glob("*.json")):
            e = validar(json.loads(f.read_text(encoding="utf-8")))
            salida[e["id"]] = e
    return salida


def del_curso(t: dict) -> dict | None:
    return estilos().get(t.get("estilo") or "")


def aplicar(t: dict, id_: str, con_formato: bool = True) -> dict:
    """Escribe en el curso lo que pide el estilo. Las elecciones por lámina se conservan."""
    e = estilos().get(id_)
    if e is None:
        raise EstiloInvalido(f"El estilo «{id_}» no existe")
    t["estilo"] = id_
    t["animacion"] = animacion.validar_curso({**(t.get("animacion") or {}), "plantilla": e["animacion"]})
    escena = {k: v for k, v in (t.get("escena") or {}).items() if k == "laminas"}
    t["escena"] = catalogo.validar_escena({**escena, "camara": e["camara"], "transicion": e["transicion"]})
    propios = t.get("ajustes_video") or {}
    video = {**propios.get("video", {}), "subtitulos_quemados": e["subtitulos_quemados"]}
    configuracion.ajustar_trabajo(t, {**propios, "video": video})
    if con_formato:
        t["formatos"] = [e["formato"]]
    return t


# ── Director de música ───────────────────────────────────────────────────────

def elegir_musica(energia: str | None, pistas: list[dict]) -> str | None:
    """La pista para un estilo: la primera con esa energía; si ninguna la declara, la primera que haya.

    Solo elige entre las pistas que la persona subió con su licencia (`datos/musica/`): nunca baja
    música de internet. Sin energía pedida, no hay música.
    """
    if not energia or not pistas:
        return None
    con_energia = [p for p in pistas if p.get("energia") == energia]
    sin_declarar = [p for p in pistas if not p.get("energia")]
    elegida = (con_energia or sin_declarar or [None])[0]
    return elegida["archivo"] if elegida else None


def modo_sfx(t: dict) -> str | None:
    e = del_curso(t)
    modo = (e or {}).get("sfx")
    return modo if modo in MODOS_SFX else None
