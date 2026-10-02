"""Agentes que revisan lo producido: Descriptor de imágenes y Revisor de voz."""

import base64
import io
import json
import re
import unicodedata
from difflib import SequenceMatcher

from app import extractor, taller
from motor import normalizar
from motor.agentes.base import Agente, Contexto, ErrorAgente, en_videos, registrar

# ── Descriptor de imágenes (modelo con visión) ───────────────────────────────

ESQUEMA_IMAGEN = {"type": "object", "properties": {
    "tipo": {"type": "string", "enum": ["contenido", "decoracion", "logo"]},
    "alt": {"type": "string"}}, "required": ["tipo", "alt"]}


def _miniatura(ruta) -> tuple[str, tuple[int, int]] | None:
    """La imagen en PNG de hasta 768 px, en base64 (lo que recibe el modelo). None si no se puede abrir."""
    from PIL import Image
    try:
        with Image.open(ruta) as im:
            tam = im.size
            im = im.convert("RGB")
            im.thumbnail((768, 768))
            buf = io.BytesIO()
            im.save(buf, "PNG")
    except Exception:  # EMF, WMF y otros formatos de Office que Pillow no abre
        return None
    return base64.b64encode(buf.getvalue()).decode("ascii"), tam


def _descriptor(t: dict, ctx: Contexto) -> list[dict]:
    media = taller.ruta_trabajo(t["id"]).parent / "media"
    vistas = {}
    for video, l, _ in en_videos(t):
        if l.get("foto") and l["foto"] not in vistas and (media / l["foto"]).exists():
            vistas[l["foto"]] = l
    salida = []
    for k, (nombre, l) in enumerate(vistas.items()):
        ctx.avisar(f"Imagen {k + 1} de {len(vistas)}", k / max(1, len(vistas)))
        mini = _miniatura(media / nombre)
        if mini is None:
            continue
        datos_img, (ancho, alto) = mini
        r = ctx.chat("Describes imágenes de presentaciones de formación para personas con discapacidad visual. "
                     "Responde solo con el JSON pedido, en español.",
                     f"Esta imagen está en la lámina «{extractor.titulo_lamina(l)}». ¿Es contenido (explica algo), "
                     "decoración (fondo, adorno) o un logo? Escribe también un texto alternativo de máximo 20 palabras.",
                     ESQUEMA_IMAGEN, imagenes=[datos_img])
        con_ia = r is not None
        if r is None:  # reglas: las muy pequeñas o muy alargadas suelen ser adornos
            decor = min(ancho, alto) < 160 or max(ancho, alto) / max(1, min(ancho, alto)) > 4
            r = {"tipo": "decoracion" if decor else "contenido", "alt": f"Imagen de la lámina {l['n']}"}
        actual = (t.get("imagenes") or {}).get(nombre)
        despues = {"archivo": nombre, "tipo": r["tipo"], "alt": " ".join(r["alt"].split()[:25]),
                   "decorativa": r["tipo"] != "contenido"}
        if actual and actual.get("decorativa") == despues["decorativa"] and actual.get("alt") == despues["alt"]:
            continue
        salida.append({"lamina": l["n"], "video": None, "titulo": f"Imagen {nombre} (lámina {l['n']})",
                       "antes": actual, "despues": despues, "con_ia": con_ia,
                       "razon": ("No es contenido: la escena no la mostrará como foto" if despues["decorativa"]
                                 else "Texto alternativo para el LMS")})
    return salida


def _aplicar_imagen(t: dict, p: dict) -> None:
    d = p["despues"]
    t.setdefault("imagenes", {})[d["archivo"]] = {"alt": d["alt"], "tipo": d["tipo"], "decorativa": d["decorativa"]}


registrar(Agente("descriptor", "Descriptor de imágenes", "Texto alternativo y fotos contra logos o adornos",
                 "presentacion", "vision", _descriptor, _aplicar_imagen))


# ── Revisor de voz (faster-whisper, local) ───────────────────────────────────

def _palabras(texto: str) -> list[str]:
    t = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", t)


_modelo_whisper = None


def _transcribir(mp4) -> str:
    global _modelo_whisper
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise ErrorAgente("El Revisor de voz necesita faster-whisper: «.venv\\Scripts\\pip install faster-whisper»") from e
    if _modelo_whisper is None:
        # «small» en int8 corre en la CPU con ~1 GB de RAM; la primera vez baja el modelo (~470 MB).
        _modelo_whisper = WhisperModel("small", device="cpu", compute_type="int8")
    # El audio se decodifica con ffmpeg y se pasa como muestras: la lectura propia de faster-whisper
    # (PyAV) falla con algunas versiones («unexpected keyword argument 'metadata_errors'»).
    import subprocess

    import numpy as np
    crudo = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "16000",
                            "-f", "s16le", "-"], capture_output=True, check=True).stdout
    muestras = np.frombuffer(crudo, dtype=np.int16).astype(np.float32) / 32768.0
    segmentos, _ = _modelo_whisper.transcribe(muestras, language="es", vad_filter=True)
    return " ".join(s.text for s in segmentos)


def _revisor_voz(t: dict, ctx: Contexto) -> list[dict]:
    base = taller.ruta_trabajo(t["id"]).parent / "salida"
    listos = [v for v in t["videos"] if (base / v["clave"] / f"{v['clave']}.mp4").exists()]
    if not listos:
        raise ErrorAgente("Todavía no hay videos producidos para escuchar")
    por_n = {l["n"]: l for _, l, _ in en_videos(t)}
    salida = []
    for k, v in enumerate(listos):
        ctx.avisar(f"Escuchando «{v['titulo']}» ({k + 1} de {len(listos)})", k / len(listos))
        informe = json.loads((base / v["clave"] / "qa.json").read_text(encoding="utf-8"))
        guion = " ".join(normalizar.para_voz(por_n[n]["notas"]) for n in v["laminas"] if n in por_n)
        oido = _transcribir(base / v["clave"] / f"{v['clave']}.mp4")
        # Whisper escribe «1503»; el guion ya va en palabras: se normalizan los dos igual.
        a, b = _palabras(guion), _palabras(normalizar.para_voz(oido))
        comp = SequenceMatcher(None, a, b, autojunk=False)
        coincide = sum(m.size for m in comp.get_matching_blocks()) / max(1, len(a))
        faltan = [" ".join(a[i1:i2]) for op, i1, i2, _, _ in comp.get_opcodes() if op in ("delete", "replace") and i2 - i1 >= 2]
        salida.append({"lamina": None, "video": v["clave"], "titulo": f"Voz de «{v['titulo']}»", "antes": None,
                       "hecha_con": "whisper small",
                       "despues": {"coincidencia": round(100 * coincide), "faltan": faltan[:15],
                                   "voz": informe.get("voz"), "transcripcion": oido[:3000]},
                       "razon": (f"La voz dijo el {round(100 * coincide)} % de las palabras del guion"
                                 + (" · revisa las frases marcadas" if coincide < 0.9 else " · bien"))})
    return salida


registrar(Agente("revisor_voz", "Revisor de voz", "Escucha los videos y compara lo que dijo la voz con el guion",
                 "resultado", None, _revisor_voz, None))
