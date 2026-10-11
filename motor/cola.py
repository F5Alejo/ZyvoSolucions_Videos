"""Producir en segundo plano, por carriles.

Producir un video tarda minutos y usa toda la CPU, así que los renders siguen yendo de a uno.
Pero un agente no compite con un render: es una llamada a Ollama (o a sus reglas) que apenas
usa memoria. Antes todo compartía una sola cola y un solo hilo, así que pedir un render dejaba
la interfaz sin poder hacer nada más hasta que terminara.

Ahora hay un **carril** por tipo de trabajo, cada uno con su cola y sus hilos:

| Carril | Qué lleva | A la vez |
|---|---|---|
| `render` | producir un video y armar el curso completo (`empaquetar`) | 1: satura CPU y disco |
| `agentes` | los agentes (`agente-*`) | 2: son llamadas a Ollama, no compiten con el render |

Dos trabajos del mismo carril siguen esperándose; dos de carriles distintos corren a la vez.
`CARRILES` se puede bajar a 1 y 1 en un equipo chico (la decisión original era de un equipo de
8 GB; ver `motor/agentes/base.py`).

El estado de cada video vive en `salida/<clave>/estado.json` (no en trabajo.json, para no pisar
lo que la persona guarda mientras tanto) y la página lo consulta con `GET /taller/<id>/render`.

Estados: `en_cola` → `produciendo` → `listo` | `error`. Mientras produce un video, `fase` dice la etapa
(QUEUED, SCRIPTING, GENERATING_AUDIO, … QA_PASSED, COMPLETED o FAILED; ver `produccion.FASES`).
"""

import json
import queue
import threading
import traceback
from datetime import datetime

from app import taller
from motor import empaquetar, errores, logs, produccion
from motor.agentes.base import ErrorAgente
from motor.errores import ErrorZyvo
from motor.voz import VozNoDisponible

PREFIJO_AGENTE = "agente-"  # la clave en la cola de un agente: «agente-redactor»

# Cuántos trabajos a la vez admite cada carril. Un render satura el equipo: va de a uno.
CARRILES = {"render": 1, "agentes": 2}
CARRIL_DEFECTO = "render"

_colas: dict[str, queue.Queue] = {c: queue.Queue() for c in CARRILES}
_activos: set[tuple[str, str]] = set()
_candado = threading.Lock()
_hilos: dict[str, list[threading.Thread]] = {c: [] for c in CARRILES}


def carril(clave: str) -> str:
    """En qué carril va un trabajo. Los agentes tienen el suyo; todo lo demás es render."""
    return "agentes" if clave.startswith(PREFIJO_AGENTE) else CARRIL_DEFECTO


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
        e = {**e, "estado": "error", "fase": "FAILED", "mensaje": "Se interrumpió (se reinició el servidor). Vuelve a producirlo."}
    if e.get("estado") == "listo":
        qa = ruta.parent / "qa.json"
        e["informe"] = json.loads(qa.read_text(encoding="utf-8")) if qa.exists() else None
    return e


def estados(t: dict) -> dict[str, dict | None]:
    return {v["clave"]: estado(t["id"], v["clave"]) for v in t["videos"]}


def en_cola(id_: str, clave: str) -> bool:
    return (id_, clave) in _activos


def encolar(id_: str, clave: str) -> bool:
    """Pone el trabajo en la cola de su carril. False si ya estaba en la cola o produciéndose."""
    c = carril(clave)
    with _candado:
        if (id_, clave) in _activos:
            return False
        _activos.add((id_, clave))
        _escribir(id_, clave, estado="en_cola", fase="QUEUED", paso="En la cola", progreso=0, mensaje=None,
                  codigo=None, severidad=None, recuperacion=None, etapa=None, detalle=None,
                  carril=c, pedido=datetime.now().isoformat(timespec="seconds"))
        _colas[c].put((id_, clave))
        _arrancar(c)
    return True


def _arrancar(c: str) -> None:
    """Levanta los hilos que le falten al carril. Se llama con `_candado` tomado."""
    _hilos[c] = [h for h in _hilos[c] if h.is_alive()]
    if len(_hilos[c]) < CARRILES[c]:
        h = threading.Thread(target=_trabajar, args=(c,), name=f"motor-cola-{c}", daemon=True)
        _hilos[c].append(h)
        h.start()


def _trabajar(c: str) -> None:
    while True:
        id_, clave = _colas[c].get()
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
                _escribir(id_, clave, propuestas=r["propuestas"], con_ia=r["con_ia"], invalidas=r.get("invalidas", 0))
            else:
                produccion.producir(t, clave, avisar=avance, fase=lambda f: _escribir(id_, clave, fase=f))
            _escribir(id_, clave, estado="listo", fase="COMPLETED", paso="Listo", progreso=1,
                      fin=datetime.now().isoformat(timespec="seconds"))
        except ErrorZyvo as e:
            # Ya clasificado por el motor: el detalle técnico quedó en logs/<clave>.jsonl.
            clasificado = {k: v for k, v in e.como_dict().items() if k != "mensaje"}
            _escribir(id_, clave, estado="error", fase="FAILED", mensaje=str(e), **clasificado)
        except (VozNoDisponible, produccion.ErrorProduccion, empaquetar.NoSePuedeArmar, ErrorAgente) as e:
            _escribir(id_, clave, estado="error", fase="FAILED", mensaje=str(e))
        except Exception as e:
            error = errores.ErrorZyvo("MOTOR_001", etapa="cola")
            error.__cause__ = e
            logs.escribir(id_, clave, "cola", "error", f"{type(e).__name__}: {e}"[:500], error)
            _escribir(id_, clave, estado="error", fase="FAILED", mensaje=f"{error} El detalle quedó en el registro del curso.",
                      detalle=traceback.format_exc()[-3000:], **{k: v for k, v in error.como_dict().items() if k != "mensaje"})
        finally:
            with _candado:
                _activos.discard((id_, clave))
            _colas[c].task_done()


def esperar() -> None:
    """Bloquea hasta que todos los carriles queden vacíos (para las pruebas)."""
    for cola in _colas.values():
        cola.join()
