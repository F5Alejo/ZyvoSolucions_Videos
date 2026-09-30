"""El curso completo en un solo MP4, y el paquete ZIP para entregar.

`salida/completo/` guarda:

    completo.mp4    todos los videos en orden (con tarjeta de título entre ellos si se pide),
                    con capítulos dentro del MP4
    completo.vtt    subtítulos unidos, con los tiempos corridos
    completo.srt
    capitulos.txt   para pegar en la descripción de YouTube («0:00 Título»)
    qa.json         qué videos entraron, en qué minuto empieza cada uno y la firma

Los videos se unen sin recodificar (todos salen del mismo motor con los mismos parámetros):
tarda segundos y no pierde calidad.
"""

import hashlib
import json
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf

from app import configuracion, datos, taller
from motor import escenas, render, subtitulos
from motor.voz import FRECUENCIA

CLAVE = "completo"


class NoSePuedeArmar(RuntimeError):
    """Faltan videos o están desactualizados: se dice cuáles."""


def carpeta(t: dict) -> Path:
    return taller.ruta_trabajo(t["id"]).parent / "salida" / CLAVE


def _informe(t: dict, clave: str) -> dict | None:
    ruta = taller.ruta_trabajo(t["id"]).parent / "salida" / clave / "qa.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def pendientes(t: dict) -> list[str]:
    """Los videos que faltan o quedaron desactualizados (por título)."""
    from motor.produccion import firma
    actual = firma(t)
    salida = []
    for v in t["videos"]:
        inf = _informe(t, v["clave"])
        mp4 = taller.ruta_trabajo(t["id"]).parent / "salida" / v["clave"] / f"{v['clave']}.mp4"
        if inf is None or not mp4.exists():
            salida.append(f"{v['titulo']} (sin producir)")
        elif inf.get("firma") != actual:
            salida.append(f"{v['titulo']} (desactualizado)")
    return salida


def _duracion(mp4: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def _tarjeta(t: dict, titulo: str, numero: int, conf: dict, destino: Path, trabajo: Path) -> None:
    """Una tarjeta con el título del video, del mismo formato que los videos (para unir sin recodificar)."""
    from motor.produccion import _logo

    cv = conf["video"]
    fps, escala = int(cv["fps"]), configuracion.RESOLUCIONES[cv["resolucion"]]
    crf, preset = configuracion.CALIDADES[cv["calidad"]]
    ancho, alto = escenas.FORMATOS["16:9"]
    marca = datos.marcas()[t["marca"]]
    lamina = {"n": 0, "formas": {"title": [titulo]}, "foto": None}
    vista = escenas.vista(lamina, 0, 1, titulo, None, f"Video {numero} · {t['nombre']}")
    html = escenas.html(vista, escenas.estilo(marca, _logo(marca)))
    segundos = conf["completo"]["duracion_tarjeta"]
    mudo = trabajo / "tarjeta-mudo.mp4"
    render.video([(html, render.cuadros(segundos, fps))], ancho, alto, mudo, trabajo / "escenas",
                 fps=fps, escala=escala, crf=crf, preset=preset)
    silencio = trabajo / "silencio.wav"
    sf.write(str(silencio), np.zeros((int(segundos * FRECUENCIA), 2), dtype=np.float32), FRECUENCIA, subtype="PCM_16")
    render.unir(mudo, silencio, destino)


def _mmss(s: float) -> str:
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def armar_completo(t: dict, avisar=lambda paso, progreso: None) -> dict:
    faltan = pendientes(t)
    if faltan:
        raise NoSePuedeArmar("Antes hay que producir: " + "; ".join(faltan))
    from motor.produccion import firma

    conf = configuracion.para_trabajo(t)
    salida = carpeta(t)
    tmp = salida / "tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    base = taller.ruta_trabajo(t["id"]).parent / "salida"

    partes, capitulos, cues, inicio = [], [], [], 0.0
    for i, v in enumerate(t["videos"], start=1):
        avisar(f"Uniendo: video {i} de {len(t['videos'])}", 0.1 + 0.7 * (i - 1) / len(t["videos"]))
        if conf["completo"]["tarjetas"]:
            tarjeta = tmp / f"tarjeta-{i:03d}.mp4"
            _tarjeta(t, v["titulo"], i, conf, tarjeta, tmp / f"t{i}")
            partes.append(tarjeta)
            capitulos.append((inicio, v["titulo"]))
            inicio += _duracion(tarjeta)
        else:
            capitulos.append((inicio, v["titulo"]))
        mp4 = base / v["clave"] / f"{v['clave']}.mp4"
        partes.append(mp4)
        cues += [(a + inicio, b + inicio, txt) for a, b, txt in subtitulos.leer_srt(base / v["clave"] / f"{v['clave']}.srt")]
        inicio += _duracion(mp4)
    total = inicio

    avisar("Uniendo los videos", 0.85)
    lista = tmp / "partes.txt"
    lista.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in partes), encoding="utf-8")
    unido = tmp / "unido.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(unido)], check=True)

    destino = salida / f"{CLAVE}.mp4"
    if conf["completo"]["capitulos"]:
        meta = tmp / "capitulos.ffmeta"
        bloques = [";FFMETADATA1", f"title={t['nombre']}"]
        for j, (a, titulo) in enumerate(capitulos):
            b = capitulos[j + 1][0] if j + 1 < len(capitulos) else total
            limpio = titulo.replace("=", "\\=").replace(";", "\\;").replace("#", "\\#").replace("\n", " ")
            bloques += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(a * 1000)}", f"END={int(b * 1000)}", f"title={limpio}"]
        meta.write_text("\n".join(bloques) + "\n", encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(unido), "-i", str(meta), "-map", "0",
                        "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", "-movflags", "+faststart",
                        str(destino)], check=True)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(unido), "-c", "copy", "-movflags", "+faststart",
                        str(destino)], check=True)

    subtitulos.escribir_vtt(cues, salida / f"{CLAVE}.vtt")
    subtitulos.escribir_srt(cues, salida / f"{CLAVE}.srt")
    (salida / "capitulos.txt").write_text("".join(f"{_mmss(a)} {titulo}\n" for a, titulo in capitulos), encoding="utf-8")

    informe = {
        "trabajo": t["id"], "video": CLAVE, "titulo": t["nombre"],
        "creado": datetime.now().isoformat(timespec="seconds"), "marca": t["marca"], "voz": t["voz"],
        "firma": firma(t), "duracion": round(total, 2),
        "capitulos": [{"inicio": round(a, 2), "titulo": x} for a, x in capitulos],
        "chequeos": [{"ok": abs(_duracion(destino) - total) < 0.5, "titulo": "El MP4 completo dura la suma de sus partes",
                      "detalle": f"{_duracion(destino):.1f} s de {total:.1f} s"}],
        "archivos": [destino.name, f"{CLAVE}.vtt", f"{CLAVE}.srt", "capitulos.txt"],
    }
    (salida / "qa.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    avisar("Listo", 1.0)
    return informe


# ── Paquete ZIP ──────────────────────────────────────────────────────────────

def _sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for trozo in iter(lambda: f.read(1 << 20), b""):
            h.update(trozo)
    return h.hexdigest()


def paquete(t: dict) -> Path:
    """Arma `salida/<id>.zip` con todo lo producido y un manifiesto con el SHA-256 de cada archivo."""
    base = taller.ruta_trabajo(t["id"]).parent / "salida"
    archivos: list[tuple[Path, str]] = []
    for v in t["videos"] + [{"clave": CLAVE}]:
        carpeta_v = base / v["clave"]
        inf = _informe(t, v["clave"])
        if not inf:
            continue
        for nombre in inf.get("archivos", []) + ["qa.json"]:
            if (carpeta_v / nombre).is_file():
                archivos.append((carpeta_v / nombre, f"{v['clave']}/{nombre}"))
    if not archivos:
        raise NoSePuedeArmar("Todavía no hay videos producidos en este curso")

    extras = {}
    if t.get("banco"):
        extras["banco-preguntas.json"] = json.dumps(t["banco"], ensure_ascii=False, indent=1)
    manifiesto = {
        "curso": t["nombre"], "trabajo": t["id"], "marca": t["marca"], "voz": t["voz"],
        "creado": datetime.now().isoformat(timespec="seconds"), "pendientes": pendientes(t),
        "archivos": [{"ruta": destino, "bytes": ruta.stat().st_size, "sha256": _sha256(ruta)} for ruta, destino in archivos],
    }
    zip_ = base / f"{t['id']}.zip"
    with zipfile.ZipFile(zip_, "w") as z:
        for ruta, destino in archivos:
            # El video ya viene comprimido: guardarlo tal cual es igual de liviano y mucho más rápido.
            modo = zipfile.ZIP_STORED if ruta.suffix == ".mp4" else zipfile.ZIP_DEFLATED
            z.write(ruta, destino, compress_type=modo)
        for nombre, texto in extras.items():
            z.writestr(nombre, texto, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("manifiesto.json", json.dumps(manifiesto, ensure_ascii=False, indent=1), compress_type=zipfile.ZIP_DEFLATED)
    return zip_
