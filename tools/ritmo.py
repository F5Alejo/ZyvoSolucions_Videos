"""Pista rítmica sintetizada para videos sin voz: bombo, platillos, palmas, bajo y acordes.

Uso (desde la carpeta del proyecto):
    python ../../tools/ritmo.py tools/ritmo.json

ritmo.json:
    {
      "bpm": 120, "duracion": 16, "salida": "assets/ritmo.wav",
      "secciones": [
        { "desde": 0, "hasta": 4,  "bombo": true, "platillo": true },
        { "desde": 4, "hasta": 16, "bombo": true, "platillo": true, "palmas": true, "bajo": true, "acordes": true }
      ],
      "subidas": [7.0]          (segundos donde TERMINA una subida de ruido de 1 compás)
    }

Todo es síntesis propia y determinista (semilla fija): mismo JSON, mismo archivo, sin
derechos de terceros. El bajo trae armónicos altos a propósito: en un portátil o un
teléfono una fundamental de 55-110 Hz sola suena a silencio.
"""

import json, sys, wave
import numpy as np

SR = 44100
RNG = np.random.default_rng(7)
PROGRESION = [  # un acorde por compás: (fundamental del bajo, notas del acorde)
    (110.00, (220.00, 261.63, 329.63)),   # La menor
    (87.31, (174.61, 220.00, 261.63)),    # Fa
    (130.81, (261.63, 329.63, 392.00)),   # Do
    (98.00, (196.00, 246.94, 293.66)),    # Sol
]


def env_exp(n, k):
    return np.exp(-np.arange(n) / SR * k)


def bombo():
    n = int(0.38 * SR); t = np.arange(n) / SR
    f = 48 + 120 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 8)
    x = np.tanh(2.4 * x)                       # saturación: armónicos que sí se oyen
    click = RNG.standard_normal(int(0.003 * SR)) * 0.5
    x[:click.size] += click
    return x * 0.5


def platillo():
    n = int(0.07 * SR)
    x = np.diff(np.diff(RNG.standard_normal(n + 2)))
    return x / np.abs(x).max() * env_exp(n, 55) * 0.55


def palmas():
    n = int(0.2 * SR); x = np.zeros(n)
    for d in (0.0, 0.011, 0.023):
        i = int(d * SR); m = n - i
        r = np.diff(RNG.standard_normal(m + 1))
        x[i:] += r / np.abs(r).max() * env_exp(m, 22 if d else 16)
    return x * 0.62


def nota_bajo(f0, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f0 * h * t) / h ** 0.9 for h in range(1, 10))
    e = np.minimum(1, t / 0.005) * (0.55 + 0.45 * np.exp(-t * 10))
    e *= np.clip((dur - t) / 0.02, 0, 1)
    return x * e * 0.16


def acorde(notas, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) for f in notas)
    e = np.minimum(1, t / 0.35) * np.clip((dur - t) / 0.4, 0, 1)
    return x * e * 0.05


def subida(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.diff(RNG.standard_normal(n + 1))
    return x / np.abs(x).max() * (t / dur) ** 2.2 * 0.28


def pegar(buf, x, t0):
    i = int(round(t0 * SR))
    if i >= buf.size: return
    m = min(x.size, buf.size - i)
    buf[i:i + m] += x[:m]


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    pulso = 60.0 / cfg["bpm"]; compas = 4 * pulso
    total = cfg["duracion"]
    buf = np.zeros(int(total * SR) + SR)
    K, H, C = bombo(), platillo(), palmas()
    for s in cfg["secciones"]:
        t = s["desde"]
        while t < s["hasta"] - 1e-6:
            n_pulso = int(round(t / pulso))
            barra = int(t // compas)
            if s.get("bombo"): pegar(buf, K, t)
            if s.get("platillo"): pegar(buf, H, t + pulso / 2)
            if s.get("palmas") and n_pulso % 2 == 1: pegar(buf, C, t)
            if s.get("bajo"):
                f0 = PROGRESION[barra % 4][0] * 2      # una octava arriba: audible en parlantes pequeños
                pegar(buf, nota_bajo(f0, pulso / 2 * 0.9), t)
                pegar(buf, nota_bajo(f0 * (2 if n_pulso % 4 == 3 else 1), pulso / 2 * 0.9), t + pulso / 2)
            if s.get("acordes") and abs(t - barra * compas) < 1e-6:
                pegar(buf, acorde(PROGRESION[barra % 4][1], compas), t)
            t += pulso
    for fin in cfg.get("subidas", []):
        pegar(buf, subida(compas / 2), fin - compas / 2)
    buf = buf[:int(total * SR)]
    # paso-altos de 1 polo a 70 Hz: la subgrave no se oye en portátiles y le roba
    # volumen a todo lo demás cuando la mezcla se normaliza
    a = 1.0 / (1.0 + 2 * np.pi * 70 / SR); y = np.zeros_like(buf); prev_x = prev_y = 0.0
    for k in range(buf.size):
        prev_y = a * (prev_y + buf[k] - prev_x); prev_x = buf[k]; y[k] = prev_y
    buf = y
    buf *= 0.89 / max(1e-9, np.abs(buf).max())
    pcm = (np.clip(buf, -1, 1) * 32767).astype("<i2")
    with wave.open(cfg["salida"], "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"ritmo: {cfg['bpm']} BPM, {total} s -> {cfg['salida']}")


if __name__ == "__main__":
    main(sys.argv[1])
