"""Detector de bugs: convierte cada chequeo fallido del control de calidad en un bug clasificado.

No arregla nada solo: dice qué pasó, en qué escena, qué tan grave es y qué conviene hacer. Así se
pueden contar patrones entre videos (los mismos códigos de `motor/errores.py`).
"""

import re
import unicodedata

from motor import videospec

# id del chequeo → (bug, severidad, recuperación)
CATALOGO = {
    "resolucion": ("VIDEO_002", "HIGH", "REGENERAR_VIDEO"),
    "formato": ("VIDEO_003", "HIGH", "REGENERAR_VIDEO"),
    "encuadre": ("TEXT_001", "MEDIUM", "ACORTAR_TEXTO"),
    "sincronia": ("SYNC_001", "HIGH", "REGENERAR_AUDIO"),
    "volumen": ("AUDIO_002", "MEDIUM", "REGENERAR_AUDIO"),
    "saturacion": ("AUDIO_004", "MEDIUM", "REGENERAR_AUDIO"),
    "negros": ("VIDEO_004", "HIGH", "REGENERAR_ESCENA"),
    "silencios": ("AUDIO_003", "MEDIUM", "REVISAR_GUION"),
    "caracteres": ("TEXT_002", "LOW", "REVISAR_TEXTO"),
    "contenido": ("CONTENT_001", "HIGH", "REVISAR_CURSO"),
}

_RARO = re.compile("[�\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]")


def _raros(texto: str) -> bool:
    return bool(_RARO.search(texto)) or any(unicodedata.category(c) == "Co" for c in texto)


def chequeos_de_contenido(spec: videospec.VideoSpec, laminas: list[dict]) -> list[dict]:
    """Lo que se revisa sobre el VideoSpec: caracteres extraños y que estén todas las láminas e imágenes."""
    raros = []
    for e in spec.escenas:
        textos = [e.vista.get("titulo", ""), *e.vista.get("vinetas", []), *(f.texto for f in e.narracion)]
        if any(_raros(x) for x in textos):
            raros.append(e.id)
    en_video = {e.lamina for e in spec.escenas}
    faltan = [l["n"] for l in laminas if l["n"] not in en_video]
    sin_imagen = [e.id for e, l in zip(spec.escenas, laminas)
                  if l.get("foto") and not (l.get("imagen_info") or {}).get("decorativa") and not e.vista.get("imagen")]
    problemas = [f"faltan las láminas {', '.join(map(str, faltan))}"] if faltan else []
    problemas += [f"{x}: su imagen no está" for x in sin_imagen]
    return [
        {"id": "caracteres", "ok": not raros, "titulo": "Textos sin caracteres extraños",
         "detalle": ("Revisar: " + ", ".join(raros)) if raros else "Títulos, viñetas y subtítulos se leen bien",
         "escenas": raros},
        {"id": "contenido", "ok": not problemas, "titulo": "Todas las láminas e imágenes están en el video",
         "detalle": "; ".join(problemas) or f"{len(spec.escenas)} escenas, con sus imágenes",
         "escenas": sin_imagen},
    ]


def detectar(chequeos: list[dict], spec: videospec.VideoSpec) -> list[dict]:
    """Un bug por cada chequeo que falló (`ok` es False). Los informativos (`None`) no son bugs."""
    salida = []
    for c in chequeos:
        if c.get("ok") is not False or c.get("id") not in CATALOGO:
            continue
        codigo, severidad, recuperacion = CATALOGO[c["id"]]
        escenas = c.get("escenas") or [None]
        for escena in escenas:
            salida.append({"bug": codigo, "severity": severidad, "scene": escena, "check": c["id"],
                           "description": f"{c['titulo']}: {c['detalle']}", "recovery": recuperacion})
    orden = {s: i for i, s in enumerate(("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"))}
    return sorted(salida, key=lambda b: orden[b["severity"]])
