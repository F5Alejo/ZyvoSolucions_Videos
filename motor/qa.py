"""Control de calidad del MP4 antes de que una persona lo revise.

Cada chequeo dice `ok` (True, False o None si solo es informativo), un título y el detalle
medido, con el mismo formato que los chequeos del taller (`taller.resumen`).
"""

import json
import re
import subprocess
from pathlib import Path

from motor import audio


def _ffprobe(archivo: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(archivo)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def _filtro(archivo: Path, *args: str) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(archivo), *args, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stderr


def revisar(mp4: Path, ancho: int, alto: int, duracion_esperada: float, estimada: float,
            fps: int = 30, lufs: float = audio.LUFS) -> list[dict]:
    info = _ffprobe(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    duracion = float(info["format"]["duration"])
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    real = num / den

    sonoridad = audio.medir(mp4) if a else None
    negros = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", _filtro(mp4, "-vf", "blackdetect=d=1.0:pix_th=0.05", "-an"))
    silencios = re.findall(r"silence_start: ([\d.]+)", _filtro(mp4, "-af", "silencedetect=noise=-50dB:d=4", "-vn"))

    def ok_rango(x, a_, b_):
        return a_ <= x <= b_

    return [
        {"ok": (v["width"], v["height"]) == (ancho, alto) and abs(real - fps) < 0.01,
         "titulo": "Resolución y cuadros por segundo", "detalle": f"{v['width']}×{v['height']} a {real:g} fps"},
        {"ok": v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p" and a is not None and a["codec_name"] == "aac",
         "titulo": "Formato que aceptan YouTube, redes y LMS",
         "detalle": f"video {v['codec_name']} {v.get('profile', '')} {v.get('pix_fmt')}; "
                    f"audio {a['codec_name'] + ' ' + a['sample_rate'] + ' Hz' if a else 'ninguno'}"},
        {"ok": abs(duracion - duracion_esperada) <= 0.25, "titulo": "La imagen y la voz duran lo mismo",
         "detalle": f"{duracion:.1f} s (se esperaban {duracion_esperada:.1f} s)"},
        {"ok": sonoridad is not None and ok_rango(float(sonoridad["input_i"]), lufs - 1, lufs + 1)
                and float(sonoridad["input_tp"]) <= audio.PICO + 0.5,
         "titulo": f"Volumen a {lufs:g} LUFS",
         "detalle": f"{sonoridad['input_i']} LUFS, pico {sonoridad['input_tp']} dBTP" if sonoridad else "sin audio"},
        {"ok": not negros, "titulo": "Sin pantallas negras",
         "detalle": ", ".join(f"{float(x):.1f}–{float(y):.1f} s" for x, y in negros) or "Ninguna de más de 1 s"},
        {"ok": not silencios, "titulo": "Sin silencios largos",
         "detalle": ", ".join(f"desde {float(x):.1f} s" for x in silencios) or "Ninguno de más de 4 s"},
        {"ok": None, "titulo": "Duración frente a la estimada del taller",
         "detalle": f"{duracion:.0f} s reales frente a {estimada:.0f} s estimados ({100 * (duracion - estimada) / estimada:+.0f} %)"
                    if estimada else f"{duracion:.0f} s"},
    ]
