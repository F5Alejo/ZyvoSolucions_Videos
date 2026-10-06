"""Producir en segundo plano, varias cosas a la vez.

Hay dos carriles con su propio límite (`configuracion["cola"]`): **render** (videos y paquetes, que
tardan minutos y usan mucha CPU) y **agentes** (proponen guiones, textos…, casi siempre en segundos).
Así un guion no espera a que termine un render. Dentro de cada carril el turno es justo: se atiende
primero el curso con menos trabajos corriendo, para que quien manda 8 videos no deje esperando a
los demás. Cada trabajo corre en su propio hilo. El estado
de cada video vive en `salida/<clave>/estado.json` (no en trabajo.json, para no pisar lo que
la persona guarda mientras tanto) y la página lo consulta con `GET /taller/<id>/render`.

Estados: `en_cola` → `produciendo` → `listo` | `error`. Mientras produce un video, `fase` dice la etapa
(QUEUED, SCRIPTING, GENERATING_AUDIO, … QA_PASSED, COMPLETED o FAILED; ver `produccion.FASES`).
"""

import json
import os
import threading
import time
import traceback
from datetime import datetime

from app import taller
from motor import empaquetar, errores, logs, produccion
from motor.agentes.base import ErrorAgente
from motor.errores import ErrorZyvo
from motor.voz import VozNoDisponible

PREFIJO_AGENTE = "agente-"  # la clave en la cola de un agente: «agente-redactor»

CARRILES = ("render", "agentes")
_pendientes: dict[str, list[tuple[str, str]]] = {c: [] for c in CARRILES}
_corriendo: dict[str, list[tuple[str, str]]] = {c: [] for c in CARRILES}
_activos: set[tuple[str, str]] = set()  # en la cola o corriendo, en cualquier carril
_candado = threading.Condition()


def carril(clave: str) -> str:
    return "agentes" if clave.startswith(PREFIJO_AGENTE) else "render"


def limite(carril_: str) -> int:
    """Cuántos trabajos de ese carril corren a la vez. Renders «automático»: uno por cada 6 núcleos (1 a 4)."""
    from app import configuracion
    n = configuracion.leer()["cola"][carril_]
    return n if n else max(1, min(4, (os.cpu_count() or 4) // 6))


def _ruta(id_: str, clave: str):
    trabajo = taller.ruta_trabajo(id_)
    return trabajo.parent / "salida" / clave / "estado.json" if trabajo else None


def _leer(ruta) -> dict:
    """En Windows, leer mientras otro hilo reemplaza el archivo puede fallar un instante: se reintenta."""
    for intento in range(20):
        try:
            return json.loads(ruta.read_text(encoding="utf-8"))
        except (PermissionError, json.JSONDecodeError):
            if intento == 19:
                raise
            time.sleep(0.025)
    return {}


_estados = threading.Lock()  # un estado.json lo escriben la cola, el trabajador y la API: de a uno


def _escribir(id_: str, clave: str, **campos) -> None:
    ruta = _ruta(id_, clave)
    if ruta is None:  # se borró el curso mientras se producía
        return
    with _estados:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        estado = _leer(ruta) if ruta.exists() else {}
        estado.update(campos)
        tmp = ruta.with_suffix(f".{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")
        for intento in range(20):  # Windows no deja reemplazar un archivo que alguien está leyendo
            try:
                tmp.replace(ruta)
                return
            except PermissionError:
                if intento == 19:
                    raise
                time.sleep(0.025)


def estado(id_: str, clave: str) -> dict | None:
    ruta = _ruta(id_, clave)
    if ruta is None or not ruta.exists():
        return None
    e = _leer(ruta)
    if e.get("estado") in ("en_cola", "produciendo") and (id_, clave) not in _activos:
        # El servidor se reinició a mitad de camino: no hay nadie produciéndolo.
        e = {**e, "estado": "error", "fase": "FAILED", "mensaje": "Se interrumpió (se reinició el servidor). Vuelve a producirlo."}
    if e.get("estado") == "listo":
        qa = ruta.parent / "qa.json"
        e["informe"] = _leer(qa) if qa.exists() else None
    return e


def estados(t: dict) -> dict[str, dict | None]:
    return {v["clave"]: estado(t["id"], v["clave"]) for v in t["videos"]}


def en_cola(id_: str, clave: str) -> bool:
    return (id_, clave) in _activos


def encolar(id_: str, clave: str) -> bool:
    """Pone el video (o el agente) en su carril. False si ya estaba en la cola o produciéndose."""
    with _candado:
        if (id_, clave) in _activos:
            return False
        _activos.add((id_, clave))
        _escribir(id_, clave, estado="en_cola", fase="QUEUED", paso="En la cola", progreso=0, mensaje=None,
                  codigo=None, severidad=None, recuperacion=None, etapa=None, detalle=None,
                  pedido=datetime.now().isoformat(timespec="seconds"))
        _pendientes[carril(clave)].append((id_, clave))
        _despachar(carril(clave))
    return True


def _despachar(carril_: str) -> None:
    """Arranca lo que quepa en el carril. Se llama con `_candado` tomado."""
    pendientes, corriendo = _pendientes[carril_], _corriendo[carril_]
    while len(corriendo) < limite(carril_):
        listos = [x for i, x in enumerate(pendientes) if _puede_empezar(x, pendientes[:i], corriendo)]
        if not listos:
            return
        # El turno justo: el primero en la fila entre los cursos con menos trabajos corriendo.
        siguiente = min(listos, key=lambda x: sum(1 for c in corriendo if c[0] == x[0]))
        pendientes.remove(siguiente)
        corriendo.append(siguiente)
        threading.Thread(target=_trabajar, args=(*siguiente, carril_), daemon=True,
                         name=f"motor-{carril_}-{siguiente[1]}").start()


def _puede_empezar(x: tuple[str, str], antes: list, corriendo: list) -> bool:
    """El paquete une los videos del curso: corre solo, después de los que se pidieron antes que él."""
    del_curso = [c for c in corriendo if c[0] == x[0]]
    if x[1] == empaquetar.CLAVE:
        return not del_curso and not any(a[0] == x[0] for a in antes)
    return not any(c[1] == empaquetar.CLAVE for c in del_curso)


def _trabajar(id_: str, clave: str, carril_: str) -> None:
    try:
        t = taller.cargar(id_)  # lo último que guardó la persona
        if t is None:
            return
        _escribir(id_, clave, estado="produciendo", paso="Empezando", progreso=0.01,
                  inicio=datetime.now().isoformat(timespec="seconds"))
        def avance(paso, x):
            try:
                _escribir(id_, clave, paso=paso, progreso=round(x, 3))
            except OSError:
                pass  # el avance es solo para mostrar: si un instante no se puede escribir, se sigue produciendo
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
            _corriendo[carril_].remove((id_, clave))
            _despachar(carril_)
            _candado.notify_all()


def esperar() -> None:
    """Bloquea hasta que no quede nada en la cola ni corriendo (para las pruebas)."""
    with _candado:
        _candado.wait_for(lambda: not _activos)
