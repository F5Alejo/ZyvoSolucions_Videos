"""La pista de narración: cada frase en su instante, y el volumen a la norma de publicación.

-14 LUFS integrados con picos por debajo de -1,5 dBTP: lo que YouTube y las redes esperan. En
un LMS suena igual de bien. Se normaliza en dos pasadas (medir y luego ajustar de forma
lineal) para no comprimir la voz.
"""

import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from motor.voz import FRECUENCIA

LUFS = -14.0
PICO = -1.5


def armar_pista(segmentos: list[tuple[float, Path]], duracion: float, destino: Path) -> None:
    """Coloca cada WAV (48 kHz, mono) en su segundo de inicio sobre una pista de silencio."""
    pista = np.zeros(int(round(duracion * FRECUENCIA)), dtype=np.float32)
    for inicio, wav in segmentos:
        datos, frecuencia = sf.read(str(wav), dtype="float32")
        if frecuencia != FRECUENCIA:
            raise ValueError(f"{wav.name} está a {frecuencia} Hz; se esperaba {FRECUENCIA}")
        a = int(round(inicio * FRECUENCIA))
        b = min(a + len(datos), len(pista))
        pista[a:b] += datos[: b - a]
    sf.write(str(destino), pista, FRECUENCIA, subtype="PCM_16")


def medir(archivo: Path) -> dict:
    """Mide la sonoridad con el filtro loudnorm de ffmpeg (primera pasada)."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(archivo),
         "-af", f"loudnorm=I={LUFS}:TP={PICO}:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])


def normalizar(origen: Path, destino: Path) -> float:
    """Lleva la pista a `LUFS` en estéreo (como sale en el MP4) y devuelve los LUFS logrados.

    No se usa loudnorm para corregir: cuando la ganancia choca con el límite de picos pasa a modo
    dinámico y se queda corto (medido: -15,2 en vez de -14). Aquí se sube con ganancia lineal, un
    limitador contiene los picos y se repite hasta quedar a ±0,3 LUFS. Se mide en estéreo porque
    duplicar un canal mono sube ~3 dB la sonoridad.
    """
    estereo = destino.with_name(destino.stem + "-estereo.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(origen), "-ac", "2", "-ar", str(FRECUENCIA),
                    "-c:a", "pcm_s16le", str(estereo)], check=True)
    techo = 10 ** ((PICO - 0.5) / 20)  # medio dB de margen: el limitador mira muestras, no picos reales
    ganancia = LUFS - float(medir(estereo)["input_i"])
    logrado = None
    for _ in range(4):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(estereo),
                        "-af", f"volume={ganancia:.2f}dB,alimiter=limit={techo:.4f}:level=false",
                        "-ar", str(FRECUENCIA), "-c:a", "pcm_s16le", str(destino)], check=True)
        logrado = float(medir(destino)["input_i"])
        if abs(logrado - LUFS) <= 0.3:
            break
        ganancia += LUFS - logrado
    estereo.unlink()
    return logrado
