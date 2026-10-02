"""Los archivos de un curso y de su marca que necesitan las escenas: imágenes del PPTX y logo."""

from pathlib import Path

from app import datos, extractor, taller


def media(t: dict) -> Path | None:
    """La carpeta con las imágenes extraídas del PPTX (la crea si el curso es de antes de este paso)."""
    base = taller.ruta_trabajo(t["id"]).parent
    carpeta, entrada = base / "media", base / "entrada.pptx"
    if not carpeta.exists() and entrada.exists():
        extractor.guardar_imagenes(entrada, carpeta)
    return carpeta if carpeta.exists() else None


def logo(marca: dict) -> Path | None:
    """El logo apto para fondo oscuro; None si no hay (la escena escribe el nombre de la marca)."""
    local = (marca.get("video") or {}).get("logo_local")
    if local and (datos.RAIZ / local).exists():
        return datos.RAIZ / local
    archivo = (marca.get("logo") or {}).get("archivo")
    if archivo and (marca.get("logo") or {}).get("fondo") == "oscuro":
        return datos.ruta_segura("repo_videos", archivo)
    return None
