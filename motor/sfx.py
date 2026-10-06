"""Efectos de sonido: un catálogo cerrado, generado con código, y el director que decide dónde van.

Los sonidos no son archivos bajados de internet: se sintetizan aquí (ondas y ruido filtrado). Son
originales, salen idénticos en cada render y no tienen problemas de licencia.

El director es sobrio a propósito: los efectos refuerzan la experiencia, no la tapan.
- Como mucho un efecto por escena, y nunca en la primera.
- Suena al empezar la escena, antes de que entre la voz (la voz entra `tiempos.entrada` después).
- Bajo: -26 dB por defecto, nunca más de -12 dB.
"""

import threading
from pathlib import Path

import numpy as np
import soundfile as sf

from motor.voz import FRECUENCIA

VOLUMEN_DEFECTO = -26.0
VOLUMEN_MAXIMO = -12.0

CATALOGO = {
    "whoosh": "Barrido de aire",
    "transicion": "Barrido suave",
    "pop": "Pop",
    "click": "Clic",
    "exito": "Éxito",
    "notificacion": "Notificación",
    "impacto": "Impacto grave",
    "tecleo": "Tecleo",
}


def _t(segundos: float) -> np.ndarray:
    return np.arange(int(segundos * FRECUENCIA)) / FRECUENCIA


def _envolvente(n: int, ataque: float, caida: float) -> np.ndarray:
    a, c = max(1, int(ataque * FRECUENCIA)), max(1, int(caida * FRECUENCIA))
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, min(a, n))
    env[-c:] *= np.linspace(1, 0, min(c, n)) ** 2
    return env


def _ruido_filtrado(segundos: float, desde: float, hasta: float, semilla: int) -> np.ndarray:
    """Ruido blanco con un pasabanda que se mueve de `desde` a `hasta` Hz (un barrido)."""
    rng = np.random.default_rng(semilla)
    n = int(segundos * FRECUENCIA)
    ruido = rng.standard_normal(n)
    espectro = np.fft.rfft(ruido)
    f = np.fft.rfftfreq(n, 1 / FRECUENCIA)
    centro = np.sqrt(desde * hasta)
    banda = np.exp(-0.5 * (np.log(np.maximum(f, 1) / centro) / 0.9) ** 2)
    base = np.fft.irfft(espectro * banda, n)
    # El barrido: se mezcla una versión aguda que crece con el tiempo.
    agudo = np.fft.irfft(espectro * np.exp(-0.5 * (np.log(np.maximum(f, 1) / hasta) / 0.6) ** 2), n)
    p = np.linspace(0, 1, n)
    return base * (1 - p) + agudo * p


def _tono(segundos: float, hz: float, caida: float = 8.0) -> np.ndarray:
    t = _t(segundos)
    return np.sin(2 * np.pi * hz * t) * np.exp(-caida * t)


def sintetizar(id_: str) -> np.ndarray:
    """Las muestras (mono, 48 kHz, pico 1.0) de un efecto del catálogo."""
    if id_ not in CATALOGO:
        raise ValueError(f"El efecto «{id_}» no está en el catálogo")
    if id_ in ("whoosh", "transicion"):
        largo = 0.45 if id_ == "whoosh" else 0.6
        x = _ruido_filtrado(largo, 300, 2400 if id_ == "whoosh" else 1200, 7 if id_ == "whoosh" else 11)
        x *= _envolvente(len(x), largo * 0.55, largo * 0.45)
    elif id_ == "pop":
        t = _t(0.09)
        x = np.sin(2 * np.pi * (900 - 4000 * t) * t) * np.exp(-45 * t)
    elif id_ == "click":
        x = _ruido_filtrado(0.03, 2000, 6000, 3) * _envolvente(int(0.03 * FRECUENCIA), 0.001, 0.025)
    elif id_ == "exito":
        a, b = _tono(0.35, 880, 7), _tono(0.5, 1318.5, 6)
        x = np.zeros(int(0.65 * FRECUENCIA))
        x[:len(a)] += a
        x[int(0.12 * FRECUENCIA):int(0.12 * FRECUENCIA) + len(b)] += b
    elif id_ == "notificacion":
        x = _tono(0.35, 1046.5, 10) + 0.5 * _tono(0.35, 2093, 14)
    elif id_ == "impacto":
        t = _t(0.45)
        x = np.sin(2 * np.pi * (110 - 60 * t) * t) * np.exp(-9 * t)
        x += 0.25 * _ruido_filtrado(0.45, 80, 400, 5) * np.exp(-14 * t)
    else:  # tecleo
        x = np.zeros(int(0.6 * FRECUENCIA))
        rng = np.random.default_rng(13)
        clic = _ruido_filtrado(0.025, 1800, 5000, 17) * _envolvente(int(0.025 * FRECUENCIA), 0.001, 0.02)
        for inicio in np.cumsum(rng.uniform(0.06, 0.11, 6)):
            a = int(inicio * FRECUENCIA)
            x[a:a + len(clic)] += clic[: len(x) - a]
    pico = np.max(np.abs(x)) or 1.0
    return (x / pico).astype(np.float32)


def archivo(id_: str, cache: Path) -> Path:
    """El WAV del efecto (se sintetiza una vez y queda en `cache`)."""
    cache.mkdir(parents=True, exist_ok=True)
    ruta = cache / f"{id_}.wav"
    if not ruta.exists():
        propio = cache / f"{id_}.{threading.get_ident()}.wav"  # otro render puede estar escribiendo el mismo
        sf.write(str(propio), sintetizar(id_), FRECUENCIA, subtype="PCM_16")
        propio.replace(ruta)
    return ruta


# ── El director ──────────────────────────────────────────────────────────────

def dirigir(escenas: list[dict], modo: str | None) -> list[list[dict]]:
    """Los efectos de cada escena según el modo del estilo: None (ninguno) o "sutil".

    Devuelve, por escena, una lista de {"id", "desfase", "volumen"} con `desfase` en segundos desde
    el inicio de la escena.
    """
    salida: list[list[dict]] = [[] for _ in escenas]
    if modo != "sutil":
        return salida
    for i, e in enumerate(escenas):
        if i == 0:
            continue
        efecto = "transicion" if e.get("transicion_previa") == "fundido" else "whoosh"
        salida[i].append({"id": efecto, "desfase": 0.05, "volumen": VOLUMEN_DEFECTO})
    return salida
