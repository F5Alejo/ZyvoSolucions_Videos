"""Lo común a todos los agentes: registro, ejecución en la cola y propuestas.

Un agente **propone**; una persona acepta o descarta. Las propuestas viven en
`trabajo["propuestas"]` con su estado (pendiente, aceptada, descartada), la fecha y con qué se
hicieron (el modelo de Ollama o «reglas» si no había IA). Volver a correr un agente reemplaza
sus propuestas pendientes; las aceptadas y descartadas quedan como historial.

Los agentes corren en la misma cola que los renders (motor/cola.py): uno a la vez, y nunca al
mismo tiempo que un render (el equipo tiene 8 GB).

Cada agente tiene permisos (`PERMISOS`): qué partes del curso lee y cuáles puede cambiar al aceptar
su propuesta. Si al aplicar toca otra cosa, el cambio se deshace y la propuesta se rechaza. Toda
respuesta de la IA se valida contra su esquema antes de usarse; si no lo cumple, el agente usa sus
reglas.
"""

import copy
import secrets
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from app import configuracion, taller
from motor.agentes import ollama


class ErrorAgente(RuntimeError):
    """Algo que la persona puede resolver (agente desactivado, falta Ollama o un modelo…)."""


LLM = ollama.Ollama()  # el LLMProvider de todos los agentes

# Varios agentes corren a la vez (motor/cola.py): el modelo se descarga cuando termina el último.
_usando_modelo: dict[str, int] = {}
_candado_modelo = threading.Lock()


_INVALIDO = object()


def depurar(valor, esquema: dict, descartes: list | None = None):
    """`valor` si cumple el esquema JSON (tipos, enum, required, min/maxItems); si no, `_INVALIDO`.

    En una lista de objetos, el elemento que no cumple se quita (y se cuenta en `descartes`) en vez
    de tirar toda la respuesta: si la IA se equivoca en una lámina, las demás siguen sirviendo.
    """
    tipo = esquema.get("type")
    tipos = {"object": dict, "array": list, "string": str, "boolean": bool, "number": (int, float), "integer": int}
    if tipo in tipos and not isinstance(valor, tipos[tipo]):
        return _INVALIDO
    if tipo in ("number", "integer") and isinstance(valor, bool):
        return _INVALIDO
    if "enum" in esquema and valor not in esquema["enum"]:
        return _INVALIDO
    if tipo == "object":
        if any(k not in valor for k in esquema.get("required", [])):
            return _INVALIDO
        limpio = dict(valor)
        for k, sub in esquema.get("properties", {}).items():
            if k in valor:
                limpio[k] = depurar(valor[k], sub, descartes)
                if limpio[k] is _INVALIDO:
                    return _INVALIDO
        return limpio
    if tipo == "array":
        items = esquema.get("items", {})
        limpios = [depurar(x, items, descartes) for x in valor]
        if items.get("type") == "object":
            if descartes is not None:
                descartes.extend(1 for x in limpios if x is _INVALIDO)
            limpios = [x for x in limpios if x is not _INVALIDO]
        elif any(x is _INVALIDO for x in limpios):
            return _INVALIDO
        if len(limpios) < esquema.get("minItems", 0) or len(limpios) > esquema.get("maxItems", len(limpios)):
            return _INVALIDO
        return limpios
    return valor


def cumple(valor, esquema: dict) -> bool:
    return depurar(valor, esquema) is not _INVALIDO


@dataclass
class Contexto:
    """Lo que un agente recibe para trabajar: si hay IA, con qué modelo, y cómo avisar su avance."""
    con_ia: bool
    modelo: str | None
    avisar: Callable[[str, float], None]
    usadas: list = field(default_factory=list)  # cuántas respuestas vinieron de la IA
    tiempo: float = 300                         # segundos máximos por pregunta
    invalidas: int = 0                          # respuestas que no cumplían el esquema (se usaron reglas)

    def chat(self, sistema: str, usuario: str, esquema: dict, imagenes: list[str] | None = None) -> dict | None:
        """Pregunta al modelo; None si no hay IA o si falló (el agente usa sus reglas)."""
        if not self.con_ia:
            return None
        try:
            r = LLM.chat(self.modelo, sistema, usuario, esquema, imagenes, self.tiempo)
        except ollama.OllamaNoDisponible:
            self.con_ia = False  # si se cae a mitad de camino, el resto va con reglas
            return None
        self.usadas.append(1)
        # JSON → esquema → valores permitidos → recién ahí se usa. Nunca se ejecuta nada.
        descartes: list = []
        limpio = depurar(r, esquema, descartes)
        self.invalidas += len(descartes) + (limpio is _INVALIDO)
        return None if limpio is _INVALIDO else limpio


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
    version: str = "1"
    lee: tuple[str, ...] = ()       # partes del curso que usa (se completan desde PERMISOS)
    escribe: tuple[str, ...] = ()   # las únicas que puede cambiar al aceptar su propuesta
    tiempo: float = 300             # segundos máximos por pregunta a la IA


# Qué lee y qué puede cambiar cada agente. Ninguno tiene acceso a todo el curso.
PERMISOS = {
    "redactor": (("laminas", "ediciones"), ("ediciones",)),
    "guionista": (("laminas", "ediciones", "videos"), ("ediciones",)),
    "verificador": (("laminas", "ediciones", "verificadas"), ("verificadas",)),
    "director": (("laminas", "ediciones", "videos", "animacion"), ("animacion",)),
    "descriptor": (("laminas", "imagenes"), ("imagenes",)),
    "evaluador": (("laminas", "ediciones", "videos", "banco"), ("banco",)),
    "publicador": (("laminas", "ediciones", "videos", "publicacion"), ("publicacion",)),
    "revisor_voz": (("laminas", "ediciones", "videos", "salida"), ()),
}
TIEMPOS = {"descriptor": 180}  # segundos por pregunta; el resto usa el de por defecto


REGISTRO: dict[str, Agente] = {}


def registrar(a: Agente) -> Agente:
    if a.id not in PERMISOS:
        raise ErrorAgente(f"El agente «{a.id}» no tiene permisos definidos")
    a.lee, a.escribe = PERMISOS[a.id]
    a.tiempo = TIEMPOS.get(a.id, a.tiempo)
    REGISTRO[a.id] = a
    return a


def _hay_whisper() -> bool:
    import importlib.util
    return importlib.util.find_spec("faster_whisper") is not None


def estado_agentes() -> list[dict]:
    conf = configuracion.leer()["agentes"]
    o = LLM.estado()
    salida = []
    for a in REGISTRO.values():
        modelo = conf["modelo_texto"] if a.modelo == "texto" else conf["modelo_vision"] if a.modelo == "vision" else None
        tiene = bool(modelo) and o["encendido"] and (modelo in o["modelos"] or f"{modelo}:latest" in o["modelos"])
        if a.id == "revisor_voz":
            modelo, tiene = "whisper small", _hay_whisper()
        salida.append({"id": a.id, "nombre": a.nombre, "que": a.que, "donde": a.donde, "modelo": modelo,
                       "activo": conf["activos"].get(a.id, True), "con_ia": tiene, "necesita_ia": a.necesita_ia,
                       "acepta": a.aplicar is not None, "version": a.version, "lee": list(a.lee),
                       "escribe": list(a.escribe)})
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
    o = LLM.estado() if modelo else {"encendido": False, "modelos": []}
    con_ia = bool(modelo) and o["encendido"] and (modelo in o["modelos"] or f"{modelo}:latest" in o["modelos"])
    if a.necesita_ia and not con_ia:
        raise ErrorAgente(f"{a.nombre} necesita Ollama con el modelo {modelo}: «ollama pull {modelo}»")
    ctx = Contexto(con_ia=con_ia, modelo=modelo, avisar=avisar, tiempo=a.tiempo)

    with _candado_modelo:
        _usando_modelo[modelo] = _usando_modelo.get(modelo, 0) + 1
    try:
        propuestas = a.proponer(t, ctx)
    finally:
        with _candado_modelo:
            _usando_modelo[modelo] -= 1
            ultimo = not _usando_modelo[modelo]
        if ctx.usadas and ultimo:
            LLM.liberar(modelo)  # libera la RAM para el render
    ahora = datetime.now().isoformat(timespec="seconds")
    for p in propuestas:
        propio = p.pop("hecha_con", None)  # p. ej. «whisper small»: IA local que no es Ollama
        p.update(id=secrets.token_hex(4), agente=a.id, creada=ahora, estado="pendiente",
                 hecha_con=propio or (modelo if p.pop("con_ia", False) else "reglas"))

    # Se relee el curso: mientras el agente pensaba, la persona (u otro agente) pudo guardar otras cosas.
    with taller.candado(id_trabajo):
        fresco = taller.cargar(id_trabajo)
        viejas = [p for p in fresco.get("propuestas", []) if not (p["agente"] == a.id and p["estado"] == "pendiente")]
        fresco["propuestas"] = viejas + propuestas
        taller.guardar(fresco)
    return {"propuestas": len(propuestas), "con_ia": bool(ctx.usadas), "invalidas": ctx.invalidas}


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
        antes = copy.deepcopy(t)
        a.aplicar(t, p)
        tocadas = sorted(k for k in set(antes) | set(t) if antes.get(k) != t.get(k) and k not in a.escribe)
        if tocadas:
            t.clear()
            t.update(antes)
            raise ErrorAgente(f"{a.nombre} intentó cambiar {', '.join(tocadas)}, que no le corresponde")
    p.update(estado="aceptada", resuelta=datetime.now().isoformat(timespec="seconds"))
    taller.guardar(t)
    return t


def aceptar_todas(t: dict, id_agente: str) -> tuple[dict, list[str]]:
    """Acepta las pendientes de un agente de una vez. Devuelve el curso y los errores de las que no se pudo."""
    errores = []
    for p in [p for p in t.get("propuestas", []) if p["agente"] == id_agente and p["estado"] == "pendiente"]:
        try:
            aceptar(t, p["id"])
        except (ErrorAgente, ValueError) as e:
            errores.append(f"{p['titulo']}: {e}")
    return t, errores


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
