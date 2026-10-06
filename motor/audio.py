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


def armar_pista(segmentos: list[tuple], duracion: float, destino: Path) -> None:
    """Coloca cada WAV (48 kHz, mono) en su segundo de inicio sobre una pista de silencio.

    Cada segmento es (inicio, wav) o (inicio, wav, ganancia_db): los efectos de sonido entran bajos.
    """
    pista = np.zeros(int(round(duracion * FRECUENCIA)), dtype=np.float32)
    for inicio, wav, *resto in segmentos:
        datos, frecuencia = sf.read(str(wav), dtype="float32")
        if resto:
            datos = datos * np.float32(10 ** (resto[0] / 20))
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


def normalizar(origen: Path, destino: Path, lufs: float = LUFS) -> float:
    """Lleva la pista a `lufs` en estéreo (como sale en el MP4) y devuelve los LUFS logrados.

    No se usa loudnorm para corregir: cuando la ganancia choca con el límite de picos pasa a modo
    dinámico y se queda corto (medido: -15,2 en vez de -14). Aquí se sube con ganancia lineal, un
    limitador contiene los picos y se repite hasta quedar a ±0,3 LUFS. Se mide en estéreo porque
    duplicar un canal mono sube ~3 dB la sonoridad.
    """
    estereo = destino.with_name(destino.stem + "-estereo.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(origen), "-ac", "2", "-ar", str(FRECUENCIA),
                    "-c:a", "pcm_s16le", str(estereo)], check=True)
    techo = 10 ** ((PICO - 0.5) / 20)  # medio dB de margen: el limitador mira muestras, no picos reales
    ganancia = lufs - float(medir(estereo)["input_i"])
    logrado = None
    for _ in range(4):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(estereo),
                        "-af", f"volume={ganancia:.2f}dB,alimiter=limit={techo:.4f}:level=false",
                        "-ar", str(FRECUENCIA), "-c:a", "pcm_s16le", str(destino)], check=True)
        logrado = float(medir(destino)["input_i"])
        if abs(logrado - lufs) <= 0.3:
            break
        ganancia += lufs - logrado
    estereo.unlink()
    return logrado


def mezclar_musica(narracion: Path, musica: Path, destino: Path, duracion: float, volumen_db: float) -> None:
    """Música de fondo en bucle bajo la voz: baja sola cuando alguien habla y se apaga al final.

    `volumen_db` es el nivel de la música respecto a su original (p. ej. -22). La compresión con
    la voz como llave (sidechain) la baja ~10 dB más mientras hay narración.
    """
    salida_fundido = max(0.0, duracion - 2.0)
    filtro = (
        f"[1:a]aresample={FRECUENCIA},aformat=channel_layouts=stereo,volume={volumen_db:.1f}dB,"
        f"atrim=0:{duracion:.3f},afade=t=in:d=1.0,afade=t=out:st={salida_fundido:.3f}:d=2.0[m];"
        f"[0:a]aformat=channel_layouts=stereo,asplit=2[voz][llave];"
        f"[m][llave]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=500[fondo];"
        f"[voz][fondo]amix=inputs=2:duration=first:normalize=0[mezcla]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(narracion), "-stream_loop", "-1", "-i", str(musica),
                    "-filter_complex", filtro, "-map", "[mezcla]", "-ar", str(FRECUENCIA),
                    "-c:a", "pcm_s16le", str(destino)], check=True)
