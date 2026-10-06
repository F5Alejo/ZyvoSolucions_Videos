"""Versiones de cada video y regeneración selectiva.

Cada vez que un video sale bien, se guarda una versión en `salida/<clave>/versiones/v001/` con su
MP4, su informe de calidad y su VideoSpec: así se puede comparar «Versión 1» con «Versión 2» y
saber exactamente cómo se hizo cada una. Se guardan las últimas `MAXIMO`; el MP4 se enlaza (sin
copiarlo) cuando el disco lo permite.

Regenerar por partes no necesita nada especial: el motor ya reutiliza lo que no cambió (la voz
por frase y cada escena por su huella). Para forzar que algo se rehaga aunque no haya cambiado,
basta con borrar su caché: `olvidar_escena()` o `olvidar_voz()`.
"""

import json
import os
import re
import shutil
from pathlib import Path

from app import taller
from motor import renderers, videospec

MAXIMO = 5


def carpeta(t: dict, clave: str) -> Path:
    return taller.ruta_trabajo(t["id"]).parent / "salida" / clave / "versiones"


def _enlazar(origen: Path, destino: Path) -> None:
    try:
        os.link(origen, destino)
    except OSError:
        shutil.copy2(origen, destino)


def guardar(t: dict, clave: str) -> dict:
    """Guarda lo recién producido como una versión nueva y borra las más viejas."""
    salida = taller.ruta_trabajo(t["id"]).parent / "salida" / clave
    base = carpeta(t, clave)
    base.mkdir(parents=True, exist_ok=True)
    numeros = [int(m.group(1)) for d in base.iterdir() if (m := re.fullmatch(r"v(\d{3})", d.name))]
    n = max(numeros, default=0) + 1
    destino = base / f"v{n:03d}"
    destino.mkdir()
    # Enlace duro: no ocupa más disco. Es seguro porque cada producción escribe un MP4 nuevo y lo
    # pone en su lugar con `replace` (produccion.producir): nunca se reescribe el archivo enlazado.
    _enlazar(salida / f"{clave}.mp4", destino / "video.mp4")
    for nombre in ("qa.json", "videospec.json", f"{clave}.vtt", f"{clave}.srt"):
        if (salida / nombre).exists():
            shutil.copy2(salida / nombre, destino / nombre)
    for viejo in sorted(d for d in base.iterdir() if re.fullmatch(r"v\d{3}", d.name))[:-MAXIMO]:
        shutil.rmtree(viejo)
    return resumen(destino)


def resumen(d: Path) -> dict:
    qa = json.loads((d / "qa.json").read_text(encoding="utf-8")) if (d / "qa.json").exists() else {}
    return {"version": d.name, "numero": int(d.name[1:]), "creado": qa.get("creado"), "voz": qa.get("voz"),
            "duracion": qa.get("duracion"), "formato": qa.get("formato"), "firma": qa.get("firma"),
            "fallas": sum(1 for c in qa.get("chequeos", []) if c.get("ok") is False),
            "bugs": len(qa.get("bugs", [])), "avisos": qa.get("avisos", [])}


def lista(t: dict, clave: str) -> list[dict]:
    base = carpeta(t, clave)
    if not base.exists():
        return []
    return [resumen(d) for d in sorted(base.iterdir(), reverse=True) if re.fullmatch(r"v\d{3}", d.name)]


def archivo(t: dict, clave: str, version: str, nombre: str) -> Path | None:
    """Solo el video, el informe y los subtítulos de una versión: nada más de la carpeta."""
    if not re.fullmatch(r"v\d{3}", version) or nombre not in {"video.mp4", "qa.json", f"{clave}.vtt", f"{clave}.srt"}:
        return None
    ruta = carpeta(t, clave) / version / nombre
    return ruta if ruta.is_file() else None


# ── Regenerar por partes ─────────────────────────────────────────────────────

def _spec(t: dict, clave: str) -> videospec.VideoSpec | None:
    ruta = taller.ruta_trabajo(t["id"]).parent / "salida" / clave / "videospec.json"
    return videospec.leer(ruta) if ruta.exists() else None


def olvidar_escena(t: dict, clave: str, lamina: int) -> int:
    """Borra de la caché la escena de esa lámina: el próximo render la vuelve a dibujar. Devuelve cuántas borró."""
    spec = _spec(t, clave)
    if spec is None:
        return 0
    cache = taller.ruta_trabajo(t["id"]).parent / "salida" / clave / "escenas"
    borradas = 0
    for e, x in zip(spec.escenas, renderers.escenas_html(spec)):
        if e.lamina == lamina:
            for f in cache.glob(f"{x[4]}.*"):
                f.unlink()
                borradas += 1
    return borradas


def olvidar_voz(t: dict, clave: str) -> int:
    """Borra de la caché el audio de las frases de ese video: el próximo render las vuelve a generar."""
    spec = _spec(t, clave)
    if spec is None:
        return 0
    borradas = 0
    for e in spec.escenas:
        for f in e.narracion:
            if f.audio and Path(f.audio).exists():
                Path(f.audio).unlink()
                borradas += 1
    return borradas
