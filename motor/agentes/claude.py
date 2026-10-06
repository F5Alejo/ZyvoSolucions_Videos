"""Claude (API de Anthropic) como `LLMProvider`: la otra IA de los agentes, además de Ollama.

Se elige en Configuración (`agentes.proveedor = "claude"`) y necesita `ANTHROPIC_API_KEY` en
`.env`. A diferencia de Ollama, **el texto del curso sale del equipo**: por eso no es el de por
defecto. Cada respuesta es JSON que cumple el esquema del agente (salida estructurada), y si
Claude se niega a responder, la API reintenta sola con otro modelo (`fallbacks: "default"`).
"""

import base64
import copy
import json
import os

from motor.agentes.ollama import OllamaNoDisponible

MODELO_DEFECTO = "claude-opus-5"

# Lo que la salida estructurada no admite en el esquema: lo revisa después `depurar()`.
_SIN_SOPORTE = ("minItems", "maxItems", "minLength", "maxLength", "minimum", "maximum", "pattern")


def _esquema(esquema: dict) -> dict:
    """El esquema del agente, con `additionalProperties: false` en cada objeto y sin límites numéricos."""
    e = copy.deepcopy(esquema)

    def limpiar(nodo):
        if isinstance(nodo, dict):
            for k in _SIN_SOPORTE:
                nodo.pop(k, None)
            if nodo.get("type") == "object":
                nodo["additionalProperties"] = False
                nodo.setdefault("required", list(nodo.get("properties", {})))
            for v in nodo.values():
                limpiar(v)
        elif isinstance(nodo, list):
            for v in nodo:
                limpiar(v)
    limpiar(e)
    return e


def _cliente(tiempo: float):
    import anthropic
    return anthropic.Anthropic(timeout=tiempo, max_retries=2)


class Claude:
    """El `LLMProvider` (motor/proveedores.py) de Claude."""
    nombre = "claude"

    def estado(self) -> dict:
        from app import configuracion
        modelo = configuracion.leer()["agentes"]["modelo_claude"]
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return {"encendido": False, "modelos": [], "faltan": [modelo]}
        return {"encendido": True, "modelos": [modelo], "faltan": []}

    def chat(self, modelo: str, sistema: str, usuario: str, esquema: dict, imagenes: list[str] | None = None,
             tiempo: float = 300) -> dict:
        import anthropic
        contenido = [{"type": "image", "source": {"type": "base64", "media_type": _tipo_imagen(img), "data": img}}
                     for img in imagenes or []]
        contenido.append({"type": "text", "text": usuario})
        try:
            r = _cliente(tiempo).beta.messages.create(
                model=modelo,
                max_tokens=16000,
                system=sistema,
                messages=[{"role": "user", "content": contenido}],
                output_config={"format": {"type": "json_schema", "schema": _esquema(esquema)}},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
        except anthropic.AuthenticationError as e:
            raise OllamaNoDisponible("Claude rechazó la clave: revisa ANTHROPIC_API_KEY en .env") from e
        except anthropic.NotFoundError as e:
            raise OllamaNoDisponible(f"Claude no tiene el modelo «{modelo}»") from e
        except anthropic.RateLimitError as e:
            raise OllamaNoDisponible("Claude está limitando las peticiones: se usan las reglas") from e
        except anthropic.APIStatusError as e:
            raise OllamaNoDisponible(f"Claude respondió con un error ({e.status_code})") from e
        except anthropic.APIConnectionError as e:
            raise OllamaNoDisponible("No hay conexión con Claude") from e
        if r.stop_reason in ("refusal", "max_tokens"):
            raise OllamaNoDisponible(f"Claude no terminó la respuesta ({r.stop_reason})")
        texto = next((b.text for b in r.content if b.type == "text"), "")
        try:
            return json.loads(texto)
        except ValueError as e:
            raise OllamaNoDisponible("Claude no devolvió JSON") from e

    def liberar(self, modelo: str) -> None:
        """Nada que liberar: el modelo no corre en este equipo."""


def _tipo_imagen(datos_b64: str) -> str:
    cabeza = base64.b64decode(datos_b64[:16] + "==")[:4]
    return "image/jpeg" if cabeza[:2] == b"\xff\xd8" else "image/webp" if cabeza == b"RIFF" else "image/png"
