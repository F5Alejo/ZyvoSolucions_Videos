"""Frase → archivo de audio, con la voz elegida en el taller.

Cada frase se genera por separado: así se sabe exactamente cuándo empieza y termina cada una
(para los subtítulos y para cambiar de lámina) sin tener que transcribir nada.

Lo generado se guarda en caché por (voz + texto): volver a producir un video solo genera las
frases que cambiaron, y con ElevenLabs no se paga dos veces la misma frase.
"""

import hashlib
import json
import os
import subprocess
import threading
import wave
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = Path(os.environ.get("INTERFAZ_MODELOS", RAIZ / "modelos"))

# Todo el audio intermedio se lleva a este formato antes de unirlo.
FRECUENCIA = 48000


class VozNoDisponible(RuntimeError):
    """La voz elegida no se puede usar en este equipo (falta el modelo, la clave, etc.)."""


# ── Proveedores ──────────────────────────────────────────────────────────────

class _Kokoro:
    """Kokoro-82M (Apache 2.0) por ONNX, en CPU. La voz gratuita para entregar."""
    extension = ".wav"
    _modelo = None
    _candado = threading.Lock()

    def __init__(self, voz: dict):
        self.voice_id = voz["voice_id"]
        self.velocidad = (voz.get("ajustes") or {}).get("velocidad", 1.0)

    def _cargar(self):
        with _Kokoro._candado:
            if _Kokoro._modelo is None:
                onnx, voces = MODELOS / "kokoro" / "kokoro-v1.0.int8.onnx", MODELOS / "kokoro" / "voices-v1.0.bin"
                if not (onnx.exists() and voces.exists()):
                    raise VozNoDisponible("Falta el modelo Kokoro: corre «python scripts/descargar_modelos.py»")
                from kokoro_onnx import Kokoro
                _Kokoro._modelo = Kokoro(str(onnx), str(voces))
        return _Kokoro._modelo

    def generar(self, texto: str, destino: Path) -> None:
        import soundfile as sf
        audio, frecuencia = self._cargar().create(texto, voice=self.voice_id, speed=self.velocidad, lang="es")
        sf.write(str(destino), audio, frecuencia)


class _Piper:
    """Piper (MIT). ⚠ La voz davefx es solo para borradores internos: ver docs/bitacora.md."""
    extension = ".wav"
    _cargadas: dict = {}

    def __init__(self, voz: dict):
        self.ruta = MODELOS / "voces" / f"{voz['voice_id']}.onnx"

    def generar(self, texto: str, destino: Path) -> None:
        if not self.ruta.exists():
            raise VozNoDisponible(f"Falta la voz de Piper {self.ruta.name}: corre «python scripts/descargar_modelos.py»")
        from piper import PiperVoice
        if self.ruta not in _Piper._cargadas:
            _Piper._cargadas[self.ruta] = PiperVoice.load(str(self.ruta))
        voz = _Piper._cargadas[self.ruta]
        with wave.open(str(destino), "wb") as w:
            voz.synthesize_wav(texto, w)


class _ElevenLabs:
    """ElevenLabs (de pago). Necesita la variable de entorno ELEVENLABS_API_KEY."""
    extension = ".mp3"

    def __init__(self, voz: dict):
        if not voz.get("voice_id"):
            raise VozNoDisponible(f"La voz {voz['nombre']} no tiene voice_id de ElevenLabs en datos/voces.json")
        self.voz = voz

    def generar(self, texto: str, destino: Path) -> None:
        clave = os.environ.get("ELEVENLABS_API_KEY")
        if not clave:
            raise VozNoDisponible("Falta la clave de ElevenLabs (variable ELEVENLABS_API_KEY)")
        import httpx
        r = httpx.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voz['voice_id']}",
            params={"output_format": "mp3_44100_128"},
            headers={"xi-api-key": clave},
            json={"text": texto, "model_id": self.voz.get("modelo"), "voice_settings": self.voz.get("ajustes")},
            timeout=120,
        )
        if r.status_code in (401, 403):
            raise VozNoDisponible("ElevenLabs rechazó la clave: ¿caducó?")
        r.raise_for_status()
        destino.write_bytes(r.content)


PROVEEDORES = {"Kokoro": _Kokoro, "Piper": _Piper, "ElevenLabs": _ElevenLabs}


def proveedor(voz: dict):
    clase = PROVEEDORES.get(voz.get("proveedor"))
    if clase is None:
        raise VozNoDisponible(f"El motor no sabe usar voces de {voz.get('proveedor')}")
    return clase(voz)


# ── Frases ───────────────────────────────────────────────────────────────────

def _clave(voz: dict, texto: str) -> str:
    firma = json.dumps([voz.get("proveedor"), voz.get("voice_id"), voz.get("modelo"), voz.get("ajustes"), texto],
                       ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(firma.encode("utf-8")).hexdigest()[:24]


def a_wav(origen: Path, destino: Path) -> None:
    """Cualquier audio → WAV mono de 48 kHz (el formato con el que se arma la pista)."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(origen), "-ac", "1", "-ar", str(FRECUENCIA),
                    "-c:a", "pcm_s16le", str(destino)], check=True)


def frase(voz: dict, texto: str, cache: Path) -> Path:
    """Genera (o toma de la caché) el audio de una frase ya normalizada. Devuelve el WAV de 48 kHz."""
    cache.mkdir(parents=True, exist_ok=True)
    final = cache / f"{_clave(voz, texto)}.wav"
    if final.exists():
        return final
    p = proveedor(voz)
    crudo = cache / f"{final.stem}.crudo{p.extension}"
    p.generar(texto, crudo)
    a_wav(crudo, final)
    crudo.unlink()
    return final
