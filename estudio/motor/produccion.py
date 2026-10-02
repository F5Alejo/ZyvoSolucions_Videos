"""Un video del trabajo, de principio a fin: voz → escenas → render → audio → subtítulos → QA.

Todo sale en `datos/trabajos/<id>/salida/<clave>/`:

    <clave>.mp4   el video (H.264 + AAC, 1920×1080, 30 fps, -14 LUFS)
    <clave>.vtt   subtítulos para el LMS y la web
    <clave>.srt   subtítulos para YouTube
    qa.json       control de calidad y línea de tiempo por lámina
"""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

from app import configuracion, datos, extractor, taller
from motor import audio, escenas, normalizar, render, subtitulos, voz as motor_voz
from motor.escenas import animacion
from motor.qa import revisar

# Los tiempos (entrada antes de la voz, pausa entre frases, respiro final) salen de la
# configuración; por defecto son los de csm.py: 1,0 s, 0,35 s y 1,3 s.
MUDA = 3.0     # una lámina sin narración (no debería pasar: el taller lo marca)


def firma(t: dict) -> str:
    """Lo que cambia el resultado de un video. Si cambia, el video producido queda desactualizado."""
    conf = configuracion.para_trabajo(t)
    base = {"marca": t["marca"], "voz": t["voz"], "conf": {g: conf[g] for g in configuracion.POR_CURSO},
            "animacion": t.get("animacion"), "ediciones": t.get("ediciones")}
    return hashlib.sha256(json.dumps(base, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


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
    conf = configuracion.para_trabajo(t)
    tiempos, cv, ca = conf["tiempos"], conf["video"], conf["audio"]
    fps = int(cv["fps"])
    escala = configuracion.RESOLUCIONES[cv["resolucion"]]
    crf, preset = configuracion.CALIDADES[cv["calidad"]]
    formato = "16:9"  # el 9:16 llega en la Fase 3 (docs/plan-motor.md)
    ancho, alto = escenas.FORMATOS[formato]
    ancho_real, alto_real = round(ancho * escala), round(alto * escala)

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
    entrada, pausa, respiro = tiempos["entrada"], tiempos["pausa"], tiempos["salida"]
    estilo = escenas.estilo(marca, _logo(marca))
    media = _media(t)
    vistas = [escenas.vista(l, i, len(laminas), video["titulo"], media, t["nombre"]) for i, l in enumerate(laminas)]
    planes = [animacion.plan(t, l["n"]) for l in laminas]
    for l, propios, v, p in zip(laminas, audios, vistas, planes):
        ent_s, sal_s = animacion.duraciones(p, v)
        # La lámina respira al menos lo que tarda en salir, para que la salida no pise la voz.
        dur = entrada + max(respiro, sal_s + 0.3) if propios else max(MUDA, ent_s + sal_s + 1.0)
        cursor = t0 + entrada
        for i, (texto, wav) in enumerate(propios):
            d = sf.info(str(wav)).duration
            segmentos.append((cursor, wav))
            frases_tiempo.append((cursor, cursor + d, texto))
            cursor += d + (pausa if i < len(propios) - 1 else 0)
            dur += d + (pausa if i < len(propios) - 1 else 0)
        n = render.cuadros(dur, fps)
        linea.append({"lamina": l["n"], "inicio": round(t0, 3), "cuadros": n, "plantilla": p["plantilla"],
                      "entrada": ent_s, "salida": sal_s})
        t0 += n / fps
    duracion = t0

    # 3. Escenas y render.
    borrador = bool(voz.get("solo_borrador"))
    htmls = [(escenas.html(v, estilo, formato, borrador, p, x["cuadros"] / fps), x["cuadros"], x["entrada"], x["salida"])
             for v, p, x in zip(vistas, planes, linea)]
    mudo = tmp / "mudo.mp4"
    encuadre = render.video(htmls, ancho, alto, mudo, tmp / "escenas",
                 avisar=lambda h, n: avisar(f"Imagen: lámina {h} de {n}", 0.5 + 0.33 * h / n),
                 fps=fps, escala=escala, crf=crf, preset=preset)

    # 4. Audio: narración, música de fondo si la hay, y volumen a la norma.
    avisar("Mezclando el audio", 0.85)
    crudo, norma = tmp / "narracion.wav", tmp / "narracion-norma.wav"
    audio.armar_pista(segmentos, duracion, crudo)
    musica = configuracion.carpeta_musica() / ca["musica"] if ca["musica"] else None
    if musica is not None and musica.exists():
        con_musica = tmp / "con-musica.wav"
        audio.mezclar_musica(crudo, musica, con_musica, duracion, ca["musica_volumen"])
        crudo = con_musica
    audio.normalizar(crudo, norma, ca["lufs"])
    mp4 = salida / f"{clave}.mp4"
    render.unir(mudo, norma, mp4)

    # 5. Subtítulos (y quemados en la imagen si la configuración lo pide).
    cues = subtitulos.cues(frases_tiempo)
    subtitulos.escribir_vtt(cues, salida / f"{clave}.vtt")
    subtitulos.escribir_srt(cues, salida / f"{clave}.srt")
    if cv["subtitulos_quemados"]:
        avisar("Quemando los subtítulos", 0.9)
        render.quemar_subtitulos(mp4, salida / f"{clave}.srt", tmp / "quemar", fps, crf, preset)

    # 6. Control de calidad.
    avisar("Revisando el resultado", 0.95)
    chequeos = revisar(mp4, ancho_real, alto_real, duracion, video["segundos"], fps, ca["lufs"])
    chequeos.insert(2, {"ok": not encuadre, "titulo": "Todo el texto cabe",
                        "detalle": "; ".join(f"lámina {laminas[x['escena']]['n']}: {x['detalle']}" for x in encuadre)
                        or "Ningún texto se sale de la pantalla ni de su caja"})
    informe = {
        "trabajo": t["id"], "video": clave, "titulo": video["titulo"],
        "creado": datetime.now().isoformat(timespec="seconds"),
        "marca": t["marca"], "voz": voz["id"], "borrador": borrador, "formato": formato,
        "firma": firma(t), "ajustes": {g: conf[g] for g in configuracion.POR_CURSO},
        "duracion": round(duracion, 2), "linea_de_tiempo": linea, "chequeos": chequeos,
        "archivos": [mp4.name, f"{clave}.vtt", f"{clave}.srt"],
    }
    (salida / "qa.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    return informe
