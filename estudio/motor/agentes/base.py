"""Lo común a todos los agentes: registro, ejecución en la cola y propuestas.

Un agente **propone**; una persona acepta o descarta. Las propuestas viven en
`trabajo["propuestas"]` con su estado (pendiente, aceptada, descartada), la fecha y con qué se
hicieron (el modelo de Ollama o «reglas» si no había IA). Volver a correr un agente reemplaza
sus propuestas pendientes; las aceptadas y descartadas quedan como historial.

Los agentes corren en la misma cola que los renders (motor/cola.py): uno a la vez, y nunca al
mismo tiempo que un render (el equipo tiene 8 GB).
"""

import secrets
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from app import configuracion, taller
from motor.agentes import ollama


class ErrorAgente(RuntimeError):
    """Algo que la persona puede resolver (agente desactivado, falta Ollama o un modelo…)."""


@dataclass
class Contexto:
    """Lo que un agente recibe para trabajar: si hay IA, con qué modelo, y cómo avisar su avance."""
    con_ia: bool
    modelo: str | None
    avisar: Callable[[str, float], None]
    usadas: list = field(default_factory=list)  # cuántas respuestas vinieron de la IA

    def chat(self, sistema: str, usuario: str, esquema: dict, imagenes: list[str] | None = None) -> dict | None:
        """Pregunta al modelo; None si no hay IA o si falló (el agente usa sus reglas)."""
        if not self.con_ia:
            return None
        try:
            r = ollama.chat(self.modelo, sistema, usuario, esquema, imagenes)
        except ollama.OllamaNoDisponible:
            self.con_ia = False  # si se cae a mitad de camino, el resto va con reglas
            return None
        self.usadas.append(1)
        return r


@dataclass
class Agente:
    id: str
    nombre: str
    que: str
    donde: str                 # en qué paso del curso aparece
    modelo: str | None         # "texto", "vision" o None (no usa Ollama)
    proponer: Callable[[dict, Contexto], list[dict]]
    aplicar: Callable[[dict, dict], None] | None = None  # None: la propuesta es informativa
    necesita_ia: bool = False  # sin IA no puede hacer nada útil


REGISTRO: dict[str, Agente] = {}


def registrar(a: Agente) -> Agente:
    REGISTRO[a.id] = a
    return a


def _hay_whisper() -> bool:
    import importlib.util
    return importlib.util.find_spec("faster_whisper") is not None


def estado_agentes() -> list[dict]:
    conf = configuracion.leer()["agentes"]
    o = ollama.estado()
    salida = []
    for a in REGISTRO.values():
        modelo = conf["modelo_texto"] if a.modelo == "texto" else conf["modelo_vision"] if a.modelo == "vision" else None
        tiene = bool(modelo) and o["encendido"] and (modelo in o["modelos"] or f"{modelo}:latest" in o["modelos"])
        if a.id == "revisor_voz":
            modelo, tiene = "whisper small", _hay_whisper()
        salida.append({"id": a.id, "nombre": a.nombre, "que": a.que, "donde": a.donde, "modelo": modelo,
                       "activo": conf["activos"].get(a.id, True), "con_ia": tiene, "necesita_ia": a.necesita_ia,
                       "acepta": a.aplicar is not None})
    return salida


def ejecutar(id_trabajo: str, id_agente: str, avisar=lambda paso, x: None) -> dict:
    a = REGISTRO.get(id_agente)
    if a is None:
        raise ErrorAgente(f"No existe el agente «{id_agente}»")
    conf = configuracion.leer()["agentes"]
    if not conf["activos"].get(a.id, True):
        raise ErrorAgente(f"{a.nombre} está desactivado en Configuración")
    t = taller.cargar(id_trabajo)
    if t is None:
        raise ErrorAgente("El curso ya no existe")

    modelo = conf["modelo_texto"] if a.modelo == "texto" else conf["modelo_vision"] if a.modelo == "vision" else None
    o = ollama.estado() if modelo else {"encendido": False, "modelos": []}
    con_ia = bool(modelo) and o["encendido"] and (modelo in o["modelos"] or f"{modelo}:latest" in o["modelos"])
    if a.necesita_ia and not con_ia:
        raise ErrorAgente(f"{a.nombre} necesita Ollama con el modelo {modelo}: «ollama pull {modelo}»")
    ctx = Contexto(con_ia=con_ia, modelo=modelo, avisar=avisar)

    try:
        propuestas = a.proponer(t, ctx)
    finally:
        if ctx.usadas:
            ollama.descargar(modelo)  # libera la RAM para el render
    ahora = datetime.now().isoformat(timespec="seconds")
    for p in propuestas:
        propio = p.pop("hecha_con", None)  # p. ej. «whisper small»: IA local que no es Ollama
        p.update(id=secrets.token_hex(4), agente=a.id, creada=ahora, estado="pendiente",
                 hecha_con=propio or (modelo if p.pop("con_ia", False) else "reglas"))

    # Se relee el curso: mientras el agente pensaba, la persona pudo guardar otras cosas.
    fresco = taller.cargar(id_trabajo)
    viejas = [p for p in fresco.get("propuestas", []) if not (p["agente"] == a.id and p["estado"] == "pendiente")]
    fresco["propuestas"] = viejas + propuestas
    taller.guardar(fresco)
    return {"propuestas": len(propuestas), "con_ia": bool(ctx.usadas)}


def _buscar(t: dict, id_propuesta: str) -> dict:
    p = next((p for p in t.get("propuestas", []) if p["id"] == id_propuesta), None)
    if p is None:
        raise ErrorAgente("Esa propuesta ya no existe")
    if p["estado"] != "pendiente":
        raise ErrorAgente("Esa propuesta ya se aceptó o se descartó")
    return p


def aceptar(t: dict, id_propuesta: str) -> dict:
    p = _buscar(t, id_propuesta)
    a = REGISTRO[p["agente"]]
    if a.aplicar is not None:
        a.aplicar(t, p)
    p.update(estado="aceptada", resuelta=datetime.now().isoformat(timespec="seconds"))
    taller.guardar(t)
    return t


def descartar(t: dict, id_propuesta: str) -> dict:
    _buscar(t, id_propuesta).update(estado="descartada", resuelta=datetime.now().isoformat(timespec="seconds"))
    taller.guardar(t)
    return t


def en_videos(t: dict) -> list[tuple[dict, dict, int]]:
    """(video, lámina efectiva, índice en el video) de las láminas que van a algún video."""
    por_n = {l["n"]: l for l in taller.laminas_efectivas(t)}
    return [(v, por_n[n], i) for v in t["videos"] for i, n in enumerate(v["laminas"]) if n in por_n]


def texto_de(l: dict) -> str:
    """Todo el texto de una lámina (lo que se ve y lo que se narra): el origen contra el que se revisa."""
    partes = [p for ps in l.get("formas", {}).values() for p in ps]
    pantalla = l.get("pantalla") or {}
    partes += [pantalla.get("titulo") or ""] + list(pantalla.get("vinetas") or [])
    return "\n".join(partes + [l.get("notas_original", ""), l.get("notas", "")])
