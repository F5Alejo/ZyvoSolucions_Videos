"""Un video del trabajo, por etapas: plan → voz → escenas → audio → subtítulos → control de calidad.

Cada etapa lee y escribe archivos en `datos/trabajos/<id>/salida/<clave>/`, así que se puede
repetir sola y lo que ya está hecho no se vuelve a hacer:

    videospec.plan.json   el plan del video (motor/videospec.py), con duraciones estimadas
    videospec.json        el plan resuelto: cada frase con su audio y cada escena en cuadros
    escenas/<huella>.mp4  cada escena dibujada; si no cambió, no se vuelve a dibujar
    <clave>.mp4           el video (H.264 + AAC, 1920×1080, 30 fps, -14 LUFS)
    <clave>.vtt / .srt    subtítulos para el LMS, la web y YouTube
    qa.json               control de calidad y línea de tiempo por lámina

La voz tiene su propia caché por (voz + texto) en `datos/trabajos/<id>/cache/voz/`.
"""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

from app import configuracion, taller
from motor import audio, escenas, render, subtitulos, videospec
from motor import voz as motor_voz
from motor.qa import revisar


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


# ── Etapas ───────────────────────────────────────────────────────────────────

def etapa_plan(t: dict, clave: str, salida: Path, formato: str = "16:9") -> videospec.VideoSpec:
    try:
        spec = videospec.construir(t, clave, firma(t), formato)
    except videospec.VideoSpecInvalido as e:
        raise ErrorProduccion(str(e)) from e
    spec.guardar(salida / "videospec.plan.json")
    return spec


def etapa_voz(t: dict, spec: videospec.VideoSpec, voz: dict, salida: Path, avisar) -> videospec.VideoSpec:
    import soundfile as sf
    cache = taller.ruta_trabajo(t["id"]).parent / "cache" / "voz"
    spec = videospec.resolver(spec, generar=lambda texto: motor_voz.frase(voz, texto, cache),
                              duracion_de=lambda wav: sf.info(str(wav)).duration,
                              avisar=lambda paso, x: avisar(paso, 0.05 + 0.45 * x))
    spec.guardar(salida / "videospec.json")
    return spec


def escenas_html(spec: videospec.VideoSpec) -> list[tuple]:
    """(html, cuadros, entrada, salida, huella) de cada escena, lo que recibe el render."""
    v, fps = spec.video, spec.video.fps
    salida = []
    for e in spec.escenas:
        html = escenas.html(e.vista, spec.estilo, v.formato, spec.voz.solo_borrador, e.animacion, e.cuadros / fps)
        huella = videospec.huella(html, e.cuadros, e.entrada, e.salida, fps, v.escala, v.crf, v.preset,
                                  e.camara, e.transicion)
        salida.append((html, e.cuadros, e.entrada, e.salida, huella))
    return salida


def etapa_escenas(spec: videospec.VideoSpec, salida: Path, tmp: Path, avisar) -> tuple[Path, list[dict]]:
    """Dibuja (o toma de la caché) cada escena y las une en un video mudo."""
    v = spec.video
    lista = escenas_html(spec)
    cache = salida / "escenas"
    mudo = tmp / "mudo.mp4"
    encuadre = render.video(lista, v.ancho, v.alto, mudo, tmp / "escenas",
                            avisar=lambda h, n: avisar(f"Imagen: lámina {h} de {n}", 0.5 + 0.33 * h / n),
                            fps=v.fps, escala=v.escala, crf=v.crf, preset=v.preset, cache=cache)
    # Las escenas que ya no usa el video (se editó la lámina) no se guardan para siempre.
    vigentes = {x[4] for x in lista}
    for viejo in cache.glob("*.*"):
        if viejo.stem not in vigentes:
            viejo.unlink()
    return mudo, encuadre


def etapa_audio(spec: videospec.VideoSpec, tmp: Path, avisar) -> Path:
    avisar("Mezclando el audio", 0.85)
    crudo, norma = tmp / "narracion.wav", tmp / "narracion-norma.wav"
    segmentos = [(f.inicio, Path(f.audio)) for e in spec.escenas for f in e.narracion]
    audio.armar_pista(segmentos, spec.duracion, crudo)
    musica = configuracion.carpeta_musica() / spec.audio.musica if spec.audio.musica else None
    if musica is not None and musica.exists():
        con_musica = tmp / "con-musica.wav"
        audio.mezclar_musica(crudo, musica, con_musica, spec.duracion, spec.audio.musica_volumen)
        crudo = con_musica
    audio.normalizar(crudo, norma, spec.audio.lufs)
    return norma


def etapa_subtitulos(spec: videospec.VideoSpec, mp4: Path, salida: Path, tmp: Path, avisar) -> None:
    clave = spec.clave
    cues = subtitulos.cues([(f.inicio, f.inicio + f.duracion, f.texto) for e in spec.escenas for f in e.narracion])
    subtitulos.escribir_vtt(cues, salida / f"{clave}.vtt")
    subtitulos.escribir_srt(cues, salida / f"{clave}.srt")
    if spec.video.subtitulos_quemados:
        avisar("Quemando los subtítulos", 0.9)
        v = spec.video
        render.quemar_subtitulos(mp4, salida / f"{clave}.srt", tmp / "quemar", v.fps, v.crf, v.preset)


def linea_de_tiempo(spec: videospec.VideoSpec) -> list[dict]:
    return [{"lamina": e.lamina, "inicio": round(e.inicio, 3), "cuadros": e.cuadros, "plantilla": e.animacion["plantilla"],
             "entrada": e.entrada, "salida": e.salida, "camara": e.camara, "transicion": e.transicion}
            for e in spec.escenas]


# ── El video completo ────────────────────────────────────────────────────────

def producir(t: dict, clave: str, avisar=lambda paso, progreso: None) -> dict:
    if clave not in {v["clave"] for v in t["videos"]}:
        raise ErrorProduccion(f"El trabajo no tiene un video «{clave}»")
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    motor_voz.proveedor(voz)  # falla pronto si la voz no se puede usar
    estimada = next(v["segundos"] for v in taller.resumen(t)["videos"] if v["clave"] == clave)

    salida = carpeta_salida(t, clave)
    tmp = salida / "tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    spec = etapa_plan(t, clave, salida)
    spec = etapa_voz(t, spec, voz, salida, avisar)
    mudo, encuadre = etapa_escenas(spec, salida, tmp, avisar)
    norma = etapa_audio(spec, tmp, avisar)
    mp4 = salida / f"{clave}.mp4"
    render.unir(mudo, norma, mp4)
    etapa_subtitulos(spec, mp4, salida, tmp, avisar)

    avisar("Revisando el resultado", 0.95)
    v = spec.video
    chequeos = revisar(mp4, v.ancho_real, v.alto_real, spec.duracion, estimada, v.fps, spec.audio.lufs)
    chequeos.insert(2, {"ok": not encuadre, "titulo": "Todo el texto cabe",
                        "detalle": "; ".join(f"lámina {spec.escenas[x['escena']].lamina}: {x['detalle']}" for x in encuadre)
                        or "Ningún texto se sale de la pantalla ni de su caja"})
    conf = configuracion.para_trabajo(t)
    informe = {
        "trabajo": t["id"], "video": clave, "titulo": spec.titulo,
        "creado": datetime.now().isoformat(timespec="seconds"),
        "marca": t["marca"], "voz": voz["id"], "borrador": spec.voz.solo_borrador, "formato": v.formato,
        "firma": spec.firma, "ajustes": {g: conf[g] for g in configuracion.POR_CURSO},
        "duracion": round(spec.duracion, 2), "linea_de_tiempo": linea_de_tiempo(spec), "chequeos": chequeos,
        "avisos": spec.avisos, "videospec": "videospec.json",
        "archivos": [mp4.name, f"{clave}.vtt", f"{clave}.srt"],
    }
    (salida / "qa.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    return informe
