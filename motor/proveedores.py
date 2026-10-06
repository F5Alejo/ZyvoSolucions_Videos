"""Las interfaces de los proveedores: lo que tiene que cumplir una voz, una IA o un renderer nuevo.

| Interfaz | Implementaciones | Dónde se registran |
|---|---|---|
| `TTSProvider` | Kokoro, Piper, ElevenLabs | `motor/voz.py` → `PROVEEDORES` |
| `LLMProvider` | Ollama (las reglas sin IA son su respaldo) | `motor/agentes/ollama.py` → `Ollama` |
| `VideoRenderer` | Playwright + ffmpeg | `motor/renderers.py` → `RENDERERS` |

La música y los efectos de sonido son catálogos de archivos con su licencia (`datos/musica/`,
`motor/sfx.py`), no proveedores: no hace falta una clase hasta que haya un segundo origen.
"""

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class TTSProvider(Protocol):
    extension: str  # el formato que escribe (".wav", ".mp3"); luego se pasa a WAV de 48 kHz

    def __init__(self, voz: dict): ...

    def generar(self, texto: str, destino: Path) -> None:
        """Escribe en `destino` el audio de `texto`. Lanza VozNoDisponible si no se puede."""


@runtime_checkable
class LLMProvider(Protocol):
    nombre: str

    def estado(self) -> dict:
        """{"encendido": bool, "modelos": [...], "faltan": [...]}"""

    def chat(self, modelo: str, sistema: str, usuario: str, esquema: dict, imagenes: list[str] | None = None,
             tiempo: float = 300) -> dict:
        """Una respuesta JSON que cumple `esquema`. Lanza un error si no puede (el agente usa reglas)."""

    def liberar(self, modelo: str) -> None:
        """Saca el modelo de la memoria (el render también la necesita)."""


@runtime_checkable
class VideoRenderer(Protocol):
    nombre: str
    descripcion: str

    def render(self, spec, cache: Path, tmp: Path, avisar=None) -> tuple[Path, list[dict]]:
        """VideoSpec resuelto → video mudo en `tmp`, y los problemas de encuadre por escena."""
