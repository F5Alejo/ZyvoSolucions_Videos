"""Cliente mínimo de Ollama (API local en http://localhost:11434).

Mientras un agente trabaja, el modelo queda cargado (`keep_alive` de 2 minutos: volver a
cargarlo en cada pregunta costaba ~30 s). Al terminar el agente se descarga con `descargar()`:
el equipo tiene 8 GB y el render también necesita memoria.
"""

import json
import time

import httpx

from app import configuracion


class OllamaNoDisponible(RuntimeError):
    """Ollama no está encendido o no tiene el modelo: se usan las reglas sin IA."""


def _url() -> str:
    return configuracion.leer()["agentes"]["url"].rstrip("/")


# Con Ollama apagado, cada consulta tarda ~4 s en Windows (localhost prueba ::1 y luego 127.0.0.1)
# y la interfaz la pide al aceptar cada propuesta: se guarda unos segundos.
SEGUNDOS_ESTADO = 10
_estado: dict = {"hora": 0.0, "clave": None, "datos": None}


def estado() -> dict:
    """Si Ollama responde, qué modelos tiene y si están los que pide la configuración."""
    conf = configuracion.leer()["agentes"]
    clave = (conf["url"], conf["modelo_texto"], conf["modelo_vision"])
    if _estado["clave"] == clave and time.monotonic() - _estado["hora"] < SEGUNDOS_ESTADO:
        return _estado["datos"]
    try:
        r = httpx.get(f"{_url()}/api/tags", timeout=2)
        r.raise_for_status()
        modelos = sorted(m["name"] for m in r.json().get("models", []))
        faltan = [m for m in (conf["modelo_texto"], conf["modelo_vision"])
                  if m not in modelos and f"{m}:latest" not in modelos]
        datos = {"encendido": True, "modelos": modelos, "faltan": faltan}
    except (httpx.HTTPError, ValueError):
        datos = {"encendido": False, "modelos": [], "faltan": [conf["modelo_texto"], conf["modelo_vision"]]}
    _estado.update(hora=time.monotonic(), clave=clave, datos=datos)
    return datos


def chat(modelo: str, sistema: str, usuario: str, esquema: dict, imagenes: list[str] | None = None,
         tiempo: float = 300) -> dict:
    """Un pedido con respuesta JSON que cumple `esquema`. Lanza OllamaNoDisponible si no se puede."""
    mensaje = {"role": "user", "content": usuario}
    if imagenes:
        mensaje["images"] = imagenes
    cuerpo = {
        "model": modelo, "stream": False, "format": esquema, "keep_alive": "2m", "think": False,
        "options": {"temperature": 0.2},
        "messages": [{"role": "system", "content": sistema}, mensaje],
    }
    try:
        r = httpx.post(f"{_url()}/api/chat", json=cuerpo, timeout=tiempo)
    except httpx.HTTPError as e:
        raise OllamaNoDisponible(f"Ollama no responde en {_url()}") from e
    if r.status_code == 404:
        raise OllamaNoDisponible(f"Ollama no tiene el modelo {modelo}: «ollama pull {modelo}»")
    r.raise_for_status()
    try:
        return json.loads(r.json()["message"]["content"])
    except (KeyError, ValueError) as e:
        raise OllamaNoDisponible("El modelo no devolvió JSON válido") from e


def descargar(modelo: str) -> None:
    """Saca el modelo de la memoria ya (si Ollama no responde, no pasa nada)."""
    try:
        httpx.post(f"{_url()}/api/generate", json={"model": modelo, "keep_alive": 0}, timeout=10)
    except httpx.HTTPError:
        pass


class Ollama:
    """El `LLMProvider` (motor/proveedores.py) de Ollama. Llama a las funciones del módulo en cada uso."""
    nombre = "ollama"

    def estado(self) -> dict:
        return estado()

    def chat(self, modelo, sistema, usuario, esquema, imagenes=None, tiempo=300) -> dict:
        return chat(modelo, sistema, usuario, esquema, imagenes, tiempo)

    def liberar(self, modelo: str) -> None:
        descargar(modelo)
