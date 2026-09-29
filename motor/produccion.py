"""Un video del trabajo, de principio a fin: voz → escenas → render → audio → subtítulos → QA.

Todo sale en `datos/trabajos/<id>/salida/<clave>/`:

    <clave>.mp4   el video (H.264 + AAC, 1920×1080, 30 fps, -14 LUFS)
    <clave>.vtt   subtítulos para el LMS y la web
    <clave>.srt   subtítulos para YouTube
    qa.json       control de calidad y línea de tiempo por lámina
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

from app import datos, extractor, taller
from motor import audio, escenas, normalizar, render, subtitulos, voz as motor_voz
from motor.qa import revisar

# Tiempos de csm.py: el título entra 1,0 s antes de la voz y la lámina respira 1,3 s al final.
ENTRADA = 1.0
PAUSA = 0.35   # entre frases de la misma lámina
SALIDA = 1.3
MUDA = 3.0     # una lámina sin narración (no debería pasar: el taller lo marca)


class ErrorProduccion(RuntimeError):
    """Algo que la persona puede resolver (voz sin clave, video que no existe…)."""


def carpeta_salida(t: dict, clave: str) -> Path:
    return taller.ruta_trabajo(t["id"]).parent / "salida" / clave


def _media(t: dict) -> Path | None:
    base = taller.ruta_trabajo(t["id"]).parent
    media, entrada = base / "media", base / "entrada.pptx"
    if not media.exists() and entrada.exists():
        extractor.guardar_imagenes(entrada, media)  # trabajos creados antes de que existiera este paso
    return media if media.exists() else None


def _logo(marca: dict) -> Path | None:
    local = (marca.get("video") or {}).get("logo_local")
    if local and (datos.RAIZ / local).exists():
        return datos.RAIZ / local
    archivo = (marca.get("logo") or {}).get("archivo")
    if archivo and (marca.get("logo") or {}).get("fondo") == "oscuro":
        return datos.ruta_segura("repo_videos", archivo)
    return None  # sin logo apto para fondo oscuro: se escribe el nombre de la marca


def producir(t: dict, clave: str, avisar=lambda paso, progreso: None) -> dict:
    r = taller.resumen(t)
    video = next((v for v in r["videos"] if v["clave"] == clave), None)
    if video is None:
        raise ErrorProduccion(f"El trabajo no tiene un video «{clave}»")
    marca = datos.marcas()[t["marca"]]
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    motor_voz.proveedor(voz)  # falla pronto si la voz no se puede usar
    formato = "16:9"  # Fase 1; el 9:16 llega en la Fase 3 (docs/plan-motor.md)
    ancho, alto = escenas.FORMATOS[formato]

    salida = carpeta_salida(t, clave)
    tmp = salida / "tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    cache = taller.ruta_trabajo(t["id"]).parent / "cache" / "voz"

    # 1. Voz, frase por frase.
    laminas = video["laminas_detalle"]
    total_frases = sum(len(l["frases"]) for l in laminas) or 1
    hechas, audios = 0, []
    for l in laminas:
        propios = []
        for f in l["frases"]:
            avisar(f"Voz: frase {hechas + 1} de {total_frases}", 0.05 + 0.45 * hechas / total_frases)
            propios.append((f, motor_voz.frase(voz, normalizar.para_voz(f, marca.get("pronunciacion")), cache)))
            hechas += 1
        audios.append(propios)

    # 2. Línea de tiempo en cuadros exactos: la imagen y la voz no se pueden separar.
    import soundfile as sf
    linea, segmentos, frases_tiempo, t0 = [], [], [], 0.0
    for l, propios in zip(laminas, audios):
        dur = ENTRADA + SALIDA if propios else MUDA
        cursor = t0 + ENTRADA
        for i, (texto, wav) in enumerate(propios):
            d = sf.info(str(wav)).duration
            segmentos.append((cursor, wav))
            frases_tiempo.append((cursor, cursor + d, texto))
            cursor += d + (PAUSA if i < len(propios) - 1 else 0)
            dur += d + (PAUSA if i < len(propios) - 1 else 0)
        n = render.cuadros(dur)
        linea.append({"lamina": l["n"], "inicio": round(t0, 3), "cuadros": n})
        t0 += n / render.FPS
    duracion = t0

    # 3. Escenas y render.
    estilo = escenas.estilo(marca, _logo(marca))
    media = _media(t)
    borrador = bool(voz.get("solo_borrador"))
    htmls = [(escenas.html(escenas.vista(l, i, len(laminas), video["titulo"], media, t["nombre"]), estilo, formato, borrador), x["cuadros"])
             for i, (l, x) in enumerate(zip(laminas, linea))]
    mudo = tmp / "mudo.mp4"
    render.video(htmls, ancho, alto, mudo, tmp / "escenas",
                 avisar=lambda h, n: avisar(f"Imagen: lámina {h} de {n}", 0.5 + 0.35 * h / n))

    # 4. Audio a la norma y unión.
    avisar("Mezclando el audio", 0.87)
    crudo, norma = tmp / "narracion.wav", tmp / "narracion-norma.wav"
    audio.armar_pista(segmentos, duracion, crudo)
    audio.normalizar(crudo, norma)
    mp4 = salida / f"{clave}.mp4"
    render.unir(mudo, norma, mp4)

    # 5. Subtítulos.
    cues = subtitulos.cues(frases_tiempo)
    subtitulos.escribir_vtt(cues, salida / f"{clave}.vtt")
    subtitulos.escribir_srt(cues, salida / f"{clave}.srt")

    # 6. Control de calidad.
    avisar("Revisando el resultado", 0.95)
    chequeos = revisar(mp4, ancho, alto, duracion, video["segundos"])
    informe = {
        "trabajo": t["id"], "video": clave, "titulo": video["titulo"],
        "creado": datetime.now().isoformat(timespec="seconds"),
        "marca": t["marca"], "voz": voz["id"], "borrador": borrador, "formato": formato,
        "duracion": round(duracion, 2), "linea_de_tiempo": linea, "chequeos": chequeos,
        "archivos": [mp4.name, f"{clave}.vtt", f"{clave}.srt"],
    }
    (salida / "qa.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    return informe
