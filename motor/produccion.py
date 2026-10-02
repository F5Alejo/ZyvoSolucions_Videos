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
from motor import audio, bugs, errores, escenas, logs, render, renderers, subtitulos, videospec
from motor import voz as motor_voz
from motor.qa import revisar


def firma(t: dict) -> str:
    """Lo que cambia el resultado de un video. Si cambia, el video producido queda desactualizado."""
    conf = configuracion.para_trabajo(t)
    grupos = {g: dict(conf[g]) for g in configuracion.POR_CURSO}
    # Lo que no cambia el video, o que vale lo de siempre, no entra: así una opción nueva en la
    # configuración no deja desactualizados los videos que ya estaban producidos.
    grupos["audio"].pop("respaldo_voz", None)
    if grupos["video"].get("renderer") == renderers.RENDERER_DEFECTO:
        grupos["video"].pop("renderer")
    base = {"marca": t["marca"], "voz": t["voz"], "conf": grupos,
            "animacion": t.get("animacion"), "ediciones": t.get("ediciones")}
    # Solo si no son los de siempre: así la firma de un curso de antes no cambia.
    if formato(t) != "16:9":
        base["formato"] = formato(t)
    if t.get("escena"):  # cámara y transiciones
        base["escena"] = t["escena"]
    return hashlib.sha256(json.dumps(base, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def formato(t: dict) -> str:
    """El formato en que se produce el curso: el primero que eligió la persona."""
    return next((f for f in t.get("formatos") or [] if f in escenas.FORMATOS), "16:9")


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


def etapa_escenas(spec: videospec.VideoSpec, salida: Path, tmp: Path, avisar, renderer: str | None = None):
    """Dibuja (o toma de la caché `escenas/`) cada escena y las une en un video mudo."""
    return renderers.renderer(renderer).render(
        spec, salida / "escenas", tmp, avisar=lambda h, n: avisar(f"Imagen: lámina {h} de {n}", 0.5 + 0.33 * h / n))


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


# ── Reintentos y respaldo ────────────────────────────────────────────────────

REINTENTOS = {"voz": 3, "escenas": 2}  # el resto se repetiría igual: no se reintenta

# Estado del video mientras se produce: (al empezar la etapa, al terminarla). La interfaz los dice
# en lenguaje humano; la cola agrega COMPLETED y FAILED.
FASES = {"plan": ("SCRIPTING", "SCRIPT_READY"), "voz": ("GENERATING_AUDIO", "AUDIO_READY"),
         "escenas": ("BUILDING_SCENES", "SCENES_READY"), "audio": ("RENDERING", None), "unir": ("RENDERING", None),
         "subtitulos": ("RENDERING", "RENDERED"), "qa": ("QA_RUNNING", None)}


def correr(t: dict, clave: str, etapa: str, fn, fase=lambda nombre: None):
    """Corre una etapa con su registro y, si la falla es pasajera, la reintenta (hasta REINTENTOS)."""
    maximo = REINTENTOS.get(etapa, 1)
    al_empezar, al_terminar = FASES.get(etapa, (None, None))
    if al_empezar:
        fase(al_empezar)
    for intento in range(1, maximo + 1):
        logs.escribir(t["id"], clave, etapa, "inicio", intento=intento)
        try:
            r = fn()
        except Exception as e:
            error = errores.clasificar(e, etapa)
            if error is not e:
                error.__cause__ = e
            otra = error.transitorio and intento < maximo
            logs.escribir(t["id"], clave, etapa, "reintento" if otra else "error", str(error), error, intento)
            if otra:
                continue
            raise error from e
        logs.escribir(t["id"], clave, etapa, "ok", intento=intento)
        if al_terminar:
            fase(al_terminar)
        return r


def voz_respaldo(voz: dict, conf: dict) -> dict | None:
    """La voz con la que se rehace el video si falla ElevenLabs: la primera Kokoro lista.

    Nunca Piper (no se puede entregar), y nada si la configuración apagó el respaldo.
    """
    if voz.get("proveedor") != "ElevenLabs" or not conf["audio"].get("respaldo_voz", True):
        return None
    return next((v for v in taller.voces() if v["proveedor"] == "Kokoro" and motor_voz.disponible(v) is None), None)


def _con_voz(spec: videospec.VideoSpec, voz: dict, aviso: str) -> videospec.VideoSpec:
    d = spec.model_dump()
    d["voz"] = {k: voz.get(k) for k in ("id", "nombre", "proveedor")} | {"solo_borrador": bool(voz.get("solo_borrador"))}
    d["avisos"].append(aviso)
    return videospec.validar(d)


# ── El video completo ────────────────────────────────────────────────────────

def producir(t: dict, clave: str, avisar=lambda paso, progreso: None, fase=lambda nombre: None) -> dict:
    if clave not in {v["clave"] for v in t["videos"]}:
        raise ErrorProduccion(f"El trabajo no tiene un video «{clave}»")
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    motor_voz.proveedor(voz)  # falla pronto si la voz no se puede usar
    video = next(v for v in taller.resumen(t)["videos"] if v["clave"] == clave)
    estimada, laminas = video["segundos"], video["laminas_detalle"]
    conf = configuracion.para_trabajo(t)

    salida = carpeta_salida(t, clave)
    tmp = salida / "tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    spec = correr(t, clave, "plan", lambda: etapa_plan(t, clave, salida, formato(t)), fase)
    respaldo = None
    try:
        spec = correr(t, clave, "voz", lambda: etapa_voz(t, spec, voz, salida, avisar), fase)
    except errores.ErrorZyvo as e:
        otra = voz_respaldo(voz, conf) if e.codigo in ("TTS_001", "TTS_002") else None
        if otra is None:
            raise
        # Todo el video con la misma voz: no se mezclan dos voces aunque algunas frases ya estuvieran.
        respaldo = {"pedida": voz["id"], "usada": otra["id"], "motivo": str(e)}
        aviso = f"Se usó la voz {otra['nombre']} porque {voz['nombre']} falló: {e}"
        logs.escribir(t["id"], clave, "voz", "respaldo", aviso)
        avisar(f"Usando la voz {otra['nombre']}", 0.05)
        spec, voz = _con_voz(spec, otra, aviso), otra
        spec = correr(t, clave, "voz", lambda: etapa_voz(t, spec, voz, salida, avisar), fase)
    mudo, encuadre = correr(t, clave, "escenas", lambda: etapa_escenas(spec, salida, tmp, avisar, conf["video"].get("renderer")), fase)
    norma = correr(t, clave, "audio", lambda: etapa_audio(spec, tmp, avisar), fase)
    mp4 = salida / f"{clave}.mp4"
    correr(t, clave, "unir", lambda: render.unir(mudo, norma, mp4), fase)
    correr(t, clave, "subtitulos", lambda: etapa_subtitulos(spec, mp4, salida, tmp, avisar), fase)

    avisar("Revisando el resultado", 0.95)
    v = spec.video
    chequeos = correr(t, clave, "qa", lambda: revisar(mp4, v.ancho_real, v.alto_real, spec.duracion, estimada,
                                                      v.fps, spec.audio.lufs), fase)
    chequeos.insert(2, {"id": "encuadre", "ok": not encuadre, "titulo": "Todo el texto cabe",
                        "detalle": "; ".join(f"lámina {spec.escenas[x['escena']].lamina}: {x['detalle']}" for x in encuadre)
                        or "Ningún texto se sale de la pantalla ni de su caja",
                        "escenas": sorted({spec.escenas[x["escena"]].id for x in encuadre})})
    chequeos += bugs.chequeos_de_contenido(spec, laminas)
    encontrados = bugs.detectar(chequeos, spec)
    fase("QA_FAILED" if encontrados else "QA_PASSED")
    informe = {
        "trabajo": t["id"], "video": clave, "titulo": spec.titulo,
        "creado": datetime.now().isoformat(timespec="seconds"),
        "marca": t["marca"], "voz": voz["id"], "borrador": spec.voz.solo_borrador, "formato": v.formato,
        "firma": spec.firma, "ajustes": {g: conf[g] for g in configuracion.POR_CURSO},
        "duracion": round(spec.duracion, 2), "linea_de_tiempo": linea_de_tiempo(spec), "chequeos": chequeos,
        "bugs": encontrados, "avisos": spec.avisos, "respaldo_voz": respaldo, "videospec": "videospec.json",
        "archivos": [mp4.name, f"{clave}.vtt", f"{clave}.srt"],
    }
    (salida / "qa.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    return informe
