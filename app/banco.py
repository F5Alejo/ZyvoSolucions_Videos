"""Banco de medios de cada marca: los clips y fotos propios que el Director pone de fondo.

Como en el video de ejemplo (la impresora, el modelado, la pieza en la mano), el material real
lo pone la empresa: sube sus tomas una vez y el Director (motor/direccion.py) elige, frase por
frase, la que mejor va con lo que dice la voz. Por eso cada toma lleva una **descripción** y unas
**etiquetas**: es lo único que el Director lee de ella. Una toma con la etiqueta «general» puede
salir con cualquier frase (sirve de relleno cuando nada coincide).

Vive en `datos/bancos/<marca>/` (fuera de git: es material de clientes), con su índice en
`banco.json`. Cada archivo se revisa al subirlo: un clip tiene que tener imagen y una foto tiene
que abrir; si no, no entra.
"""

import json
import re
import secrets
import shutil
import subprocess
import threading
from datetime import datetime
from pathlib import Path

from app import datos

EXT_CLIP = {".mp4", ".mov", ".m4v", ".webm"}
EXT_FOTO = {".jpg", ".jpeg", ".png", ".webp"}
MAX_BYTES = 500 * 1024 * 1024
_candado = threading.Lock()


class BancoInvalido(ValueError):
    pass


def carpeta(marca: str) -> Path:
    if not re.fullmatch(r"[a-z0-9-]+", marca or ""):
        raise BancoInvalido("Esa marca no existe")
    return datos.RAIZ_DATOS / "bancos" / marca


def _indice(marca: str) -> Path:
    return carpeta(marca) / "banco.json"


def listar(marca: str) -> list[dict]:
    ruta = _indice(marca)
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else []


def _guardar(marca: str, items: list[dict]) -> None:
    ruta = _indice(marca)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(ruta)


def ruta(marca: str, archivo: str) -> Path | None:
    """El archivo de una toma, solo si está dentro de la carpeta del banco."""
    raiz = carpeta(marca).resolve()
    p = (raiz / archivo).resolve()
    return p if p.parent == raiz and p.exists() else None


def _etiquetas(valor) -> list[str]:
    if isinstance(valor, str):
        valor = valor.split(",")
    limpias = [re.sub(r"\s+", " ", str(x)).strip().lower()[:40] for x in valor or []]
    return list(dict.fromkeys(x for x in limpias if x))[:20]


def _probar_clip(archivo: Path) -> dict:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "json", str(archivo)],
                           capture_output=True, text=True, timeout=60)
        info = json.loads(r.stdout or "{}")
        v = (info.get("streams") or [{}])[0]
        duracion = float(info.get("format", {}).get("duration") or 0)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        raise BancoInvalido("No se pudo leer el video")
    if not v.get("width") or duracion < 0.5:
        raise BancoInvalido("El archivo no trae imagen de video (o dura menos de medio segundo)")
    return {"ancho": v["width"], "alto": v["height"], "duracion": round(duracion, 3)}


def _probar_foto(archivo: Path) -> dict:
    from PIL import Image, UnidentifiedImageError
    try:
        with Image.open(archivo) as im:
            im.verify()
        with Image.open(archivo) as im:
            return {"ancho": im.width, "alto": im.height, "duracion": None}
    except (UnidentifiedImageError, OSError):
        raise BancoInvalido("La imagen no se pudo abrir")


def _miniatura(archivo: Path, destino: Path) -> None:
    """Un cuadro del clip (a 1 s) para la pantalla del banco y para que la IA vea de qué trata."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(archivo), "-frames:v", "1",
                    "-vf", "scale=480:-2", str(destino)], capture_output=True, timeout=60)


def agregar(marca: str, nombre: str, origen: Path, descripcion: str = "", etiquetas=None) -> dict:
    """Mete en el banco el archivo `origen` (ya en disco). Lo mueve; si no sirve, lo borra y avisa."""
    ext = Path(nombre).suffix.lower()
    tipo = "clip" if ext in EXT_CLIP else "foto" if ext in EXT_FOTO else None
    if tipo is None:
        origen.unlink(missing_ok=True)
        raise BancoInvalido("Sube un video (MP4, MOV, WEBM) o una foto (JPG, PNG, WEBP)")
    if origen.stat().st_size > MAX_BYTES:
        origen.unlink(missing_ok=True)
        raise BancoInvalido(f"El archivo pasa de {MAX_BYTES // 1024 // 1024} MB")
    id_ = secrets.token_hex(5)
    destino = carpeta(marca) / f"{id_}{ext}"
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(origen), destino)
    try:
        medidas = _probar_clip(destino) if tipo == "clip" else _probar_foto(destino)
    except BancoInvalido:
        destino.unlink(missing_ok=True)
        raise
    miniatura = None
    if tipo == "clip":
        _miniatura(destino, carpeta(marca) / f"{id_}.jpg")
        miniatura = f"{id_}.jpg" if (carpeta(marca) / f"{id_}.jpg").exists() else None
    item = {"id": id_, "tipo": tipo, "archivo": destino.name, "miniatura": miniatura or (destino.name if tipo == "foto" else None),
            "nombre": Path(nombre).name[:120], "descripcion": str(descripcion or "").strip()[:400],
            "etiquetas": _etiquetas(etiquetas), "subido": datetime.now().isoformat(timespec="seconds"), **medidas}
    with _candado:
        _guardar(marca, listar(marca) + [item])
    return item


def actualizar(marca: str, id_: str, descripcion: str | None = None, etiquetas=None) -> dict:
    with _candado:
        items = listar(marca)
        item = next((x for x in items if x["id"] == id_), None)
        if item is None:
            raise BancoInvalido("Esa toma no está en el banco")
        if descripcion is not None:
            item["descripcion"] = str(descripcion).strip()[:400]
        if etiquetas is not None:
            item["etiquetas"] = _etiquetas(etiquetas)
        _guardar(marca, items)
    return item


def eliminar(marca: str, id_: str) -> None:
    with _candado:
        items = listar(marca)
        item = next((x for x in items if x["id"] == id_), None)
        if item is None:
            raise BancoInvalido("Esa toma no está en el banco")
        for f in {item["archivo"], item.get("miniatura")} - {None}:
            (carpeta(marca) / f).unlink(missing_ok=True)
        _guardar(marca, [x for x in items if x["id"] != id_])
