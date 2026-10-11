"""Los archivos de un curso y de su marca que necesitan las escenas: imágenes del PPTX y logo."""

import json
from pathlib import Path

from app import datos, extractor, taller


def media(t: dict) -> Path | None:
    """La carpeta con las imágenes extraídas del PPTX (la crea si el curso es de antes de este paso)."""
    base = taller.ruta_trabajo(t["id"]).parent
    carpeta, entrada = base / "media", base / "entrada.pptx"
    if not carpeta.exists() and entrada.exists():
        extractor.guardar_imagenes(entrada, carpeta)
    return carpeta if carpeta.exists() else None


def disposicion(t: dict) -> dict | None:
    """La geometría de las láminas del PPTX, para el modo fiel (`app/disposicion.py`).

    Leer un PPTX de 88 láminas forma por forma tarda, así que se guarda en
    `disposicion.json` la primera vez. Los cursos de antes de este paso lo generan al pedirlo.
    """
    base = taller.ruta_trabajo(t["id"]).parent
    cache, entrada = base / "disposicion.json", base / "entrada.pptx"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    if not entrada.exists():
        return None
    from app import disposicion as leer_disposicion
    d = leer_disposicion.leer(entrada)
    cache.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def formas(t: dict, n: int) -> list[dict]:
    """Las formas de la lámina `n` (1..N), o vacío si no se pudo leer el PPTX."""
    d = disposicion(t)
    if not d:
        return []
    return next((l["formas"] for l in d["laminas"] if l["n"] == n), [])


def logo(marca: dict) -> Path | None:
    """El logo apto para fondo oscuro; None si no hay (la escena escribe el nombre de la marca)."""
    local = (marca.get("video") or {}).get("logo_local")
    if local and (datos.RAIZ / local).exists():
        return datos.RAIZ / local
    archivo = (marca.get("logo") or {}).get("archivo")
    if archivo and (marca.get("logo") or {}).get("fondo") == "oscuro":
        return datos.ruta_segura("repo_videos", archivo)
    return None
