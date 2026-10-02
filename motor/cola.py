"""Producir en segundo plano, un video a la vez.

Producir tarda minutos y usa toda la CPU: un solo hilo trabajador atiende una cola. El estado
de cada video vive en `salida/<clave>/estado.json` (no en trabajo.json, para no pisar lo que
la persona guarda mientras tanto) y la página lo consulta con `GET /taller/<id>/render`.

Estados: `en_cola` → `produciendo` → `listo` | `error`.
"""

import json
import queue
import threading
import traceback
from datetime import datetime

from app import taller
from motor import empaquetar, produccion
from motor.agentes.base import ErrorAgente
from motor.voz import VozNoDisponible

PREFIJO_AGENTE = "agente-"  # la clave en la cola de un agente: «agente-redactor»

_cola: queue.Queue = queue.Queue()
_activos: set[tuple[str, str]] = set()
_candado = threading.Lock()
_hilo: threading.Thread | None = None


def _ruta(id_: str, clave: str):
    return taller.ruta_trabajo(id_).parent / "salida" / clave / "estado.json"


def _escribir(id_: str, clave: str, **campos) -> None:
    ruta = _ruta(id_, clave)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    estado = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    estado.update(campos)
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
    tmp.replace(ruta)


def estado(id_: str, clave: str) -> dict | None:
    ruta = _ruta(id_, clave)
    if not ruta.exists():
        return None
    e = json.loads(ruta.read_text(encoding="utf-8"))
    if e.get("estado") in ("en_cola", "produciendo") and (id_, clave) not in _activos:
        # El servidor se reinició a mitad de camino: no hay nadie produciéndolo.
        e = {**e, "estado": "error", "mensaje": "Se interrumpió (se reinició el servidor). Vuelve a producirlo."}
    if e.get("estado") == "listo":
        qa = ruta.parent / "qa.json"
        e["informe"] = json.loads(qa.read_text(encoding="utf-8")) if qa.exists() else None
    return e


def estados(t: dict) -> dict[str, dict | None]:
    return {v["clave"]: estado(t["id"], v["clave"]) for v in t["videos"]}


def en_cola(id_: str, clave: str) -> bool:
    return (id_, clave) in _activos


def encolar(id_: str, clave: str) -> bool:
    """Pone el video en la cola. False si ya estaba en la cola o produciéndose."""
    global _hilo
    with _candado:
        if (id_, clave) in _activos:
            return False
        _activos.add((id_, clave))
        _escribir(id_, clave, estado="en_cola", paso="En la cola", progreso=0, mensaje=None,
                  pedido=datetime.now().isoformat(timespec="seconds"))
        _cola.put((id_, clave))
        if _hilo is None or not _hilo.is_alive():
            _hilo = threading.Thread(target=_trabajar, name="motor-cola", daemon=True)
            _hilo.start()
    return True


def _trabajar() -> None:
    while True:
        id_, clave = _cola.get()
        try:
            t = taller.cargar(id_)  # lo último que guardó la persona
            if t is None:
                continue
            _escribir(id_, clave, estado="produciendo", paso="Empezando", progreso=0.01,
                      inicio=datetime.now().isoformat(timespec="seconds"))
            avance = lambda paso, x: _escribir(id_, clave, paso=paso, progreso=round(x, 3))  # noqa: E731
            if clave == empaquetar.CLAVE:
                empaquetar.armar_completo(t, avisar=avance)
            elif clave.startswith(PREFIJO_AGENTE):
                from motor.agentes import registro
                r = registro.ejecutar(id_, clave[len(PREFIJO_AGENTE):], avisar=avance)
                _escribir(id_, clave, propuestas=r["propuestas"], con_ia=r["con_ia"])
            else:
                produccion.producir(t, clave, avisar=avance)
            _escribir(id_, clave, estado="listo", paso="Listo", progreso=1,
                      fin=datetime.now().isoformat(timespec="seconds"))
        except (VozNoDisponible, produccion.ErrorProduccion, empaquetar.NoSePuedeArmar, ErrorAgente) as e:
            _escribir(id_, clave, estado="error", mensaje=str(e))
        except Exception:
            _escribir(id_, clave, estado="error", mensaje="La producción falló. El detalle quedó en estado.json.",
                      detalle=traceback.format_exc()[-3000:])
        finally:
            with _candado:
                _activos.discard((id_, clave))
            _cola.task_done()


def esperar() -> None:
    """Bloquea hasta que la cola quede vacía (para las pruebas)."""
    _cola.join()
