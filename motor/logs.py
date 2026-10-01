"""Registro técnico de cada curso: una línea JSON por evento en `datos/trabajos/<id>/logs/<clave>.jsonl`.

Aquí sí van los detalles (*traceback*, código de error, intento): la interfaz solo muestra el
mensaje para la persona, y el modo diagnóstico lee este archivo.
"""

import json
import traceback
from datetime import datetime

from app import taller

MAX_LINEAS = 2000  # el registro de un video no crece sin límite


def _ruta(id_trabajo: str, clave: str):
    ruta = taller.ruta_trabajo(id_trabajo)
    return ruta.parent / "logs" / f"{clave}.jsonl" if ruta else None


def escribir(id_trabajo: str, clave: str, etapa: str, estado: str, mensaje: str = "", error=None,
             intento: int | None = None, **extra) -> None:
    ruta = _ruta(id_trabajo, clave)
    if ruta is None:
        return
    evento = {"timestamp": datetime.now().isoformat(timespec="milliseconds"), "project_id": id_trabajo,
              "video": clave, "stage": etapa, "status": estado, "message": mensaje}
    if intento is not None:
        evento["retry"] = intento
    if error is not None:
        codigo = getattr(error, "codigo", None)
        evento.update(error_code=codigo, severity=getattr(error, "severidad", None),
                      recovery=getattr(error, "recuperacion", None))
        causa = error.__cause__ or error
        evento["stacktrace"] = "".join(traceback.format_exception(type(causa), causa, causa.__traceback__))[-4000:]
    evento.update(extra)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    if len(lineas) > MAX_LINEAS:
        ruta.write_text("\n".join(lineas[-MAX_LINEAS:]) + "\n", encoding="utf-8")


def leer(id_trabajo: str, clave: str, ultimos: int = 200) -> list[dict]:
    ruta = _ruta(id_trabajo, clave)
    if ruta is None or not ruta.exists():
        return []
    return [json.loads(x) for x in ruta.read_text(encoding="utf-8").splitlines()[-ultimos:] if x.strip()]
