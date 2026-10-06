"""¿Qué tiene este equipo para producir? Solo lectura: nunca instala ni cambia nada."""

import os
import shutil
import subprocess
import time

from app import datos, taller
from motor import voz as motor_voz
from motor.agentes import ollama

_cache: dict = {"hora": 0.0, "datos": None}


def _ffmpeg() -> dict:
    ruta = shutil.which("ffmpeg")
    if not ruta:
        return {"ok": False, "detalle": "No está en el PATH", "arreglo": "winget install Gyan.FFmpeg"}
    linea = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[0]
    return {"ok": True, "detalle": linea.split(" Copyright")[0]}


def _chromium() -> dict:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            ruta = p.chromium.executable_path
        if os.path.exists(ruta):
            return {"ok": True, "detalle": "Chromium de Playwright instalado"}
    except Exception:  # sin playwright o sin navegador
        pass
    return {"ok": False, "detalle": "Falta el navegador que dibuja las escenas",
            "arreglo": r".venv\Scripts\python.exe -m playwright install chromium"}


def _hyperframes() -> dict:
    from motor import hyperframes
    falta = hyperframes.disponible()
    return {"ok": falta is None, "detalle": falta or "Listo: texto cinético al ritmo de la voz",
            "arreglo": "cd motor/hyperframes && npm install" if falta else None}


def _ia() -> dict:
    """La IA que dirige los videos y los agentes (Configuración → agentes.proveedor)."""
    from app import configuracion
    conf = configuracion.leer()["agentes"]
    if conf["proveedor"] != "claude":
        return {"ok": True, "proveedor": "ollama", "detalle": "Ollama (local): el material no sale del equipo"}
    con_clave = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return {"ok": con_clave, "proveedor": "claude",
            "detalle": f"Claude ({conf['modelo_claude']}): el texto del curso sale a la API de Anthropic" if con_clave
            else "Claude elegido pero sin clave: pon ANTHROPIC_API_KEY en .env (mientras tanto, reglas sin IA)"}


def revisar(forzar: bool = False) -> dict:
    """El diagnóstico completo (se guarda 60 s: revisar Chromium tarda ~1 s)."""
    if not forzar and _cache["datos"] and time.time() - _cache["hora"] < 60:
        return _cache["datos"]
    voces = []
    for v in taller.voces():
        falta = motor_voz.disponible(v)
        voces.append({"id": v["id"], "nombre": v["nombre"], "proveedor": v["proveedor"], "ok": falta is None,
                      "detalle": ("Falta su voice_id" if falta and "voice_id" in falta else falta)
                      or ("Solo borradores" if v.get("solo_borrador") else "Lista")})
    o = ollama.estado()
    libre = shutil.disk_usage(datos.RAIZ_DATOS).free / 1024 ** 3
    resultado = {
        "ffmpeg": _ffmpeg(),
        "chromium": _chromium(),
        "hyperframes": _hyperframes(),
        "ia": _ia(),
        "elevenlabs": {"ok": bool(os.environ.get("ELEVENLABS_API_KEY")),
                       "detalle": "Clave cargada desde .env" if os.environ.get("ELEVENLABS_API_KEY")
                       else "Sin clave: pon ELEVENLABS_API_KEY en .env"},
        "voces": voces,
        "ollama": {"ok": o["encendido"] and not o["faltan"], "encendido": o["encendido"], "modelos": o["modelos"],
                   "detalle": ("Listo" if o["encendido"] and not o["faltan"] else
                               f"Faltan modelos: {', '.join(o['faltan'])}" if o["encendido"] else
                               "Ollama no está encendido: los agentes usan reglas sin IA"),
                   "arreglo": " ; ".join(f"ollama pull {m}" for m in o["faltan"]) if o["encendido"] and o["faltan"] else None},
        "disco": {"ok": libre > 5, "detalle": f"{libre:.1f} GB libres"},
    }
    _cache.update(hora=time.time(), datos=resultado)
    return resultado
