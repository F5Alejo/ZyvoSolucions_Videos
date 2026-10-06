"""API del estudio de video y servidor de la interfaz (Vue, en `frontend/dist`).

Todo lo que la interfaz necesita sale de `/api/*`. `/media/*` sirve los videos, logos y PDF
del repositorio de videos en solo lectura. Cualquier otra ruta devuelve la aplicación Vue.
"""

import json
import re
from collections import Counter
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from pydantic import BaseModel

from app import configuracion, datos, empresas, extractor, taller
from motor import analisis, catalogo, cola, diagnostico, empaquetar, escenas, estilos, logs, produccion, recursos, versiones, videospec
from motor import voz as motor_voz
from motor.agentes import entrega as agentes_entrega
from motor.agentes import registro as agentes
from motor.escenas import animacion, efectos

RAIZ = Path(__file__).resolve().parent.parent
DIST = RAIZ / "frontend" / "dist"
MAX_PPTX = 200 * 1024 * 1024
# Lo único que se sirve del repositorio de videos: imágenes, PDF y texto. Nunca código ni claves.
EXTENSIONES_REPO = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf", ".md", ".txt"}
EXTENSIONES_ENTREGABLES = {".mp4", ".webm", ".mp3", ".txt"}

app = FastAPI(title="Estudio de video RiskMann", docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.exception_handler(animacion.AnimacionInvalida)
def _animacion_invalida(_, e: animacion.AnimacionInvalida):
    return JSONResponse({"detail": str(e)}, status_code=400)


@app.exception_handler(agentes.ErrorAgente)
def _error_agente(_, e: agentes.ErrorAgente):
    return JSONResponse({"detail": str(e)}, status_code=400)


@app.exception_handler(ValueError)
def _valor_invalido(_, e: ValueError):
    return JSONResponse({"detail": str(e)}, status_code=400)


# ── Utilidades ───────────────────────────────────────────────────────────────

def _casos() -> list[dict]:
    casos = json.loads((datos.RAIZ_DATOS / "casos.json").read_text(encoding="utf-8"))
    for c in casos:
        c["salida"] = [p for p in (datos.proyecto(i) for i in c["sale"]) if p]
        c["videos"] = [e for p in c["salida"] for e in p["entregables_detalle"] if e["existe"]]
    return casos


def _con_medios(m: dict) -> dict:
    """Añade a la marca la URL de su logo: el del repositorio de videos o el que subió la empresa."""
    logo = m.get("logo") or {}
    if logo.get("archivo_local") and empresas.ruta_logo(logo["archivo_local"]):
        url = f"/media/empresas/{logo['archivo_local']}"
    elif logo.get("archivo") and datos.ruta_segura("repo_videos", logo["archivo"]):
        url = f"/media/repo/{logo['archivo']}"
    else:
        url = None
    return {**m, "logo_url": url, "registrada": bool(m.get("registrada"))}


def _trabajo_o_404(id_: str) -> dict:
    t = taller.cargar(id_)
    if t is None:
        raise HTTPException(404, "No encontramos ese curso")
    return t


def _trabajo_completo(t: dict) -> dict:
    """El trabajo con lo que la interfaz necesita por lámina, y su resumen sin duplicar láminas."""
    laminas = [
        {**l, "titulo": (l.get("pantalla") or {}).get("titulo") or extractor.titulo_lamina(l),
         "segundos": extractor.segundos(l["notas"]), "citas": extractor.afirmaciones_normativas(l["notas"])}
        for l in taller.laminas_efectivas(t)
    ]
    r = taller.resumen(t)
    r["videos"] = [{k: v for k, v in vid.items() if k != "laminas_detalle"} for vid in r["videos"]]
    r["sin_uso"] = [l["n"] for l in r["sin_uso"]]
    return {"trabajo": {**t, "laminas": laminas}, "resumen": r}


def _descarga(contenido, nombre: str) -> Response:
    return Response(json.dumps(contenido, ensure_ascii=False, indent=1), media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="{nombre}"'})


# ── General ──────────────────────────────────────────────────────────────────

@app.get("/api/inicio")
def api_inicio():
    proyectos = datos.proyectos()
    return {
        "cifras_ejemplo": taller.cifras_csm(),
        "ejemplo_disponible": taller.ejemplo_disponible(),
        "trabajos": taller.lista(),
        "casos": [{k: c[k] for k in ("id", "titulo", "resumen", "marca")}
                  | {"portada": c["videos"][0]["archivo"] if c["videos"] else None, "total_videos": len(c["videos"])}
                  for c in _casos()],
        "conteo_estados": Counter(p["estado"] for p in proyectos),
        "total_videos": len(proyectos),
        "pendientes_abiertos": sum(not x["hecho"] for x in datos.pendientes()),
        "repositorio_conectado": "repo_videos" in datos.CONFIG,
    }


@app.get("/api/catalogo")
def api_catalogo():
    """Lo que casi todas las pantallas necesitan: estados, tipos, marcas y voces."""
    return {
        "estados": datos.ESTADOS,
        "familias": datos.FAMILIAS,
        "formatos": taller.FORMATOS,
        "marcas": {k: _con_medios(m) for k, m in datos.marcas().items()},
        "voces": [{**v, "muestra_url": f"/media/entregables/{v['muestra']}"
                   if v.get("muestra") and datos.ruta_segura("entregables", v["muestra"]) else None,
                   "falta": motor_voz.disponible(v)}
                  for v in taller.voces()],
        "pendientes_abiertos": sum(not x["hecho"] for x in datos.pendientes()),
    }


# ── Cursos (el taller) ───────────────────────────────────────────────────────

@app.get("/api/trabajos")
def api_trabajos():
    return taller.lista()


@app.post("/api/trabajos", status_code=201)
async def api_crear_trabajo(archivo: UploadFile = File(...), nombre: str = Form(""), marca: str = Form("")):
    if not (archivo.filename or "").lower().endswith(".pptx"):
        raise ValueError("El archivo tiene que ser un .pptx de PowerPoint")
    contenido = await archivo.read(MAX_PPTX + 1)
    if len(contenido) > MAX_PPTX:
        raise ValueError("El archivo pasa de 200 MB")
    t = taller.desde_pptx(archivo.filename, contenido, nombre, marca)
    return {"id": t["id"]}


@app.post("/api/trabajos/ejemplo-csm", status_code=201)
def api_crear_ejemplo():
    return {"id": taller.desde_csm()["id"]}


@app.get("/api/trabajos/{id_}")
def api_trabajo(id_: str):
    return _trabajo_completo(_trabajo_o_404(id_))


class Ajustes(BaseModel):
    marca: str
    voz: str
    formatos: list[str]


@app.patch("/api/trabajos/{id_}")
def api_ajustar_trabajo(id_: str, ajustes: Ajustes):
    t = taller.ajustar(_trabajo_o_404(id_), ajustes.marca, ajustes.voz, ajustes.formatos)
    return _trabajo_completo(t)


@app.post("/api/trabajos/{id_}/reagrupar")
def api_reagrupar(id_: str):
    return _trabajo_completo(taller.reagrupar(_trabajo_o_404(id_)))


@app.delete("/api/trabajos/{id_}", status_code=204)
def api_eliminar_trabajo(id_: str):
    _trabajo_o_404(id_)
    taller.eliminar(id_)


@app.get("/api/trabajos/{id_}/analisis")
def api_analisis(id_: str, rehacer: bool = False):
    """Qué trae la presentación: láminas, notas, imágenes, tablas, gráficos, tema, dificultad y avisos."""
    t = _trabajo_o_404(id_)
    return analisis.guardar(t) if rehacer else analisis.leer(t)


@app.get("/api/trabajos/{id_}/curso.json")
def api_curso_json(id_: str):
    return _descarga(taller.curso_json(_trabajo_o_404(id_)), "curso.json")


@app.get("/api/trabajos/{id_}/orden.json")
def api_orden(id_: str):
    t = _trabajo_o_404(id_)
    return _descarga(taller.orden_produccion(t), f"orden-{t['id']}.json")


@app.get("/api/trabajos/{id_}/banco.json")
def api_banco(id_: str):
    t = _trabajo_o_404(id_)
    if not t.get("banco"):
        raise HTTPException(404, "Este curso no tiene banco de preguntas")
    return _descarga(t["banco"], "banco-preguntas.json")


class Edicion(BaseModel):
    cambios: dict | None  # {notas?, titulo?, vinetas?}; None vuelve al original del PPTX


@app.put("/api/trabajos/{id_}/laminas/{n}/edicion")
def api_editar_lamina(id_: str, n: int, cuerpo: Edicion):
    """Corrige la narración o lo que se ve de una lámina, sin tocar lo extraído del PPTX."""
    return _trabajo_completo(taller.editar_lamina(_trabajo_o_404(id_), n, cuerpo.cambios))


# ── Motor: producir los videos de un curso ───────────────────────────────────

# Lo que la interfaz recibe del estado de cada video en la cola.
CAMPOS_ESTADO = ("estado", "fase", "paso", "progreso", "mensaje", "codigo", "recuperacion")


def _produccion(t: dict) -> dict:
    """Estado de cada video del curso en el motor, con lo que la interfaz necesita para mostrarlo."""
    voz = next((v for v in taller.voces() if v["id"] == t["voz"]), {})
    firma_actual = produccion.firma(t)
    videos = {}
    for clave, e in cola.estados(t).items():
        if e is None:
            videos[clave] = None
            continue
        base = f"/api/trabajos/{t['id']}/salida/{clave}/"
        inf = e.get("informe")
        videos[clave] = {
            **{k: e.get(k) for k in CAMPOS_ESTADO},
            "informe": inf,
            "desactualizado": bool(inf) and inf.get("firma") != firma_actual,
            "archivos": {"mp4": f"{base}{clave}.mp4", "vtt": f"{base}{clave}.vtt", "srt": f"{base}{clave}.srt"}
            if e.get("estado") == "listo" else None,
        }
    c = cola.estado(t["id"], empaquetar.CLAVE)
    completo = None
    if c:
        base = f"/api/trabajos/{t['id']}/salida/{empaquetar.CLAVE}/"
        completo = {**{k: c.get(k) for k in CAMPOS_ESTADO}, "informe": c.get("informe"),
                    "desactualizado": bool(c.get("informe")) and c["informe"].get("firma") != firma_actual,
                    "archivos": {"mp4": f"{base}completo.mp4", "vtt": f"{base}completo.vtt", "srt": f"{base}completo.srt",
                                 "capitulos": f"{base}capitulos.txt"} if c.get("estado") == "listo" else None}
    listos = sum(1 for v in videos.values() if v and v["estado"] == "listo" and not v["desactualizado"])
    return {"voz_falta": motor_voz.disponible(voz), "voz_borrador": bool(voz.get("solo_borrador")), "videos": videos,
            "completo": completo, "listos": listos, "total": len(videos), "pendientes": empaquetar.pendientes(t)}


@app.get("/api/trabajos/{id_}/produccion")
def api_produccion(id_: str):
    """Estado de producción de cada video; la interfaz lo consulta mientras produce."""
    return _produccion(_trabajo_o_404(id_))


@app.post("/api/trabajos/{id_}/producir/{clave}", status_code=202)
def api_producir(id_: str, clave: str):
    """Pone un video del curso en la cola del motor (en segundo plano, en el carril de los renders)."""
    t = _trabajo_o_404(id_)
    if clave not in {v["clave"] for v in t["videos"]}:
        raise HTTPException(404, "Ese curso no tiene ese video")
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    falta = motor_voz.disponible(voz)
    if falta:
        raise ValueError(falta)
    cola.encolar(id_, clave)
    return _produccion(t)


@app.post("/api/trabajos/{id_}/producir-todo", status_code=202)
def api_producir_todo(id_: str, completo: bool = True):
    """Pone en la cola los videos que faltan o quedaron desactualizados y, al final, el MP4 completo."""
    t = _trabajo_o_404(id_)
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    falta = motor_voz.disponible(voz)
    if falta:
        raise ValueError(falta)
    actual = produccion.firma(t)
    for clave, e in cola.estados(t).items():
        inf = (e or {}).get("informe")
        if e and e.get("estado") == "listo" and inf and inf.get("firma") == actual:
            continue
        cola.encolar(id_, clave)
    if completo:
        cola.encolar(id_, empaquetar.CLAVE)
    return _produccion(t)


@app.post("/api/trabajos/{id_}/completo", status_code=202)
def api_armar_completo(id_: str):
    """Une los videos ya producidos en un solo MP4 con capítulos."""
    t = _trabajo_o_404(id_)
    faltan = empaquetar.pendientes(t)
    if faltan:
        raise ValueError("Antes hay que producir: " + "; ".join(faltan))
    cola.encolar(id_, empaquetar.CLAVE)
    return _produccion(t)


@app.get("/api/trabajos/{id_}/paquete.zip")
def api_paquete(id_: str):
    """Todo lo producido del curso en un ZIP, con un manifiesto que trae el SHA-256 de cada archivo."""
    t = _trabajo_o_404(id_)
    try:
        ruta = empaquetar.paquete(t)
    except empaquetar.NoSePuedeArmar as e:
        raise ValueError(str(e))
    return FileResponse(ruta, media_type="application/zip", filename=f"{t['id']}.zip")


# Lo que se puede bajar de la salida de un video.
TIPOS_SALIDA = {".mp4": "video/mp4", ".vtt": "text/vtt", ".srt": "application/x-subrip", ".json": "application/json",
                ".txt": "text/plain; charset=utf-8"}


@app.get("/api/trabajos/{id_}/salida/{clave}/{archivo}")
def api_salida(id_: str, clave: str, archivo: str, descargar: bool = False):
    """Solo el mp4, los subtítulos y el qa.json de ese video: nada más de la carpeta del curso."""
    t = _trabajo_o_404(id_)
    permitidos = {f"{clave}.mp4", f"{clave}.vtt", f"{clave}.srt", "qa.json", "capitulos.txt"}
    if not re.fullmatch(r"[a-z0-9-]+", clave) or archivo not in permitidos:
        raise HTTPException(404)
    ruta = taller.ruta_trabajo(t["id"]).parent / "salida" / clave / archivo
    if not ruta.is_file():
        raise HTTPException(404)
    return FileResponse(ruta, media_type=TIPOS_SALIDA[ruta.suffix], filename=f"{t['id']}-{archivo}" if descargar else None,
                        content_disposition_type="attachment" if descargar else "inline")


def _video_o_404(t: dict, clave: str) -> None:
    if clave not in {v["clave"] for v in t["videos"]}:
        raise HTTPException(404, "Ese curso no tiene ese video")


@app.get("/api/trabajos/{id_}/versiones/{clave}")
def api_versiones(id_: str, clave: str):
    """Las versiones producidas de un video (la más nueva primero), para compararlas."""
    t = _trabajo_o_404(id_)
    _video_o_404(t, clave)
    return [{**v, "mp4": f"/api/trabajos/{id_}/versiones/{clave}/{v['version']}/video.mp4"} for v in versiones.lista(t, clave)]


@app.get("/api/trabajos/{id_}/versiones/{clave}/{version}/{archivo}")
def api_archivo_version(id_: str, clave: str, version: str, archivo: str, descargar: bool = False):
    t = _trabajo_o_404(id_)
    ruta = versiones.archivo(t, clave, version, archivo)
    if ruta is None:
        raise HTTPException(404)
    nombre = f"{t['id']}-{clave}-{version}{ruta.suffix}" if descargar else None
    return FileResponse(ruta, media_type=TIPOS_SALIDA[ruta.suffix], filename=nombre,
                        content_disposition_type="attachment" if descargar else "inline")


class Regenerar(BaseModel):
    escena: int | None = None  # número de lámina: vuelve a dibujar solo esa escena
    voz: bool = False          # vuelve a generar solo el audio de la narración


@app.post("/api/trabajos/{id_}/regenerar/{clave}", status_code=202)
def api_regenerar(id_: str, clave: str, cuerpo: Regenerar):
    """Regenera por partes: lo que no se pide (y no cambió) se reutiliza tal cual."""
    t = _trabajo_o_404(id_)
    _video_o_404(t, clave)
    if cuerpo.escena is not None:
        if cuerpo.escena not in next(v["laminas"] for v in t["videos"] if v["clave"] == clave):
            raise HTTPException(404, "Ese video no tiene esa lámina")
        versiones.olvidar_escena(t, clave, cuerpo.escena)
    if cuerpo.voz:
        versiones.olvidar_voz(t, clave)
    return api_producir(id_, clave)


FRASE_MUESTRA = "Hola. Así sonará la narración de tu video, con esta voz."


@app.get("/api/voces/{id_}/muestra")
def api_muestra_voz(id_: str):
    """Una frase corta con esa voz, para el botón «Escuchar». Se genera una vez y queda en caché."""
    voz = next((v for v in taller.voces() if v["id"] == id_), None)
    if voz is None:
        raise HTTPException(404, "No existe esa voz")
    falta = motor_voz.disponible(voz)
    if falta:
        raise ValueError(falta)
    wav = motor_voz.frase(voz, FRASE_MUESTRA, datos.RAIZ_DATOS / "cache" / "muestras")
    return FileResponse(wav, media_type="audio/wav")


@app.get("/api/trabajos/{id_}/diagnostico/{clave}")
def api_diagnostico(id_: str, clave: str):
    """Modo diagnóstico: el registro técnico de un video (etapas, intentos, códigos y *tracebacks*)."""
    t = _trabajo_o_404(id_)
    if not re.fullmatch(r"[a-z0-9-]+", clave):
        raise HTTPException(404)
    return {"eventos": logs.leer(t["id"], clave), "estado": cola.estado(t["id"], clave)}


class AjustesVideo(BaseModel):
    ajustes: dict | None  # None: volver a la configuración global


@app.put("/api/trabajos/{id_}/ajustes-video")
def api_ajustes_video(id_: str, cuerpo: AjustesVideo):
    """Ajustes de video propios del curso (solo lo que cambie respecto a la configuración)."""
    t = configuracion.ajustar_trabajo(_trabajo_o_404(id_), cuerpo.ajustes)
    taller.guardar(t)
    return {**_trabajo_completo(t), "ajustes_efectivos": configuracion.para_trabajo(t)}


@app.get("/api/trabajos/{id_}/ajustes-video")
def api_ver_ajustes_video(id_: str):
    t = _trabajo_o_404(id_)
    return {"propios": t.get("ajustes_video") or {}, "efectivos": configuracion.para_trabajo(t)}


# ── Animaciones ──────────────────────────────────────────────────────────────

@app.get("/api/animaciones")
def api_animaciones():
    """Las plantillas y el catálogo: qué efectos admite cada elemento, curvas y límites."""
    return {
        "plantillas": list(animacion.plantillas().values()),
        "elementos": {el: {"nombre": d["nombre"],
                           "entrada": [{"id": x, "nombre": efectos.NOMBRES[x]} for x in d["entrada"]],
                           "salida": [{"id": x, "nombre": efectos.NOMBRES[x]} for x in d["salida"]]}
                      for el, d in efectos.ELEMENTOS.items()},
        "curvas": [{"id": k, "nombre": v} for k, v in efectos.NOMBRES_CURVAS.items()],
        "limites": {k: {"min": a, "max": b} for k, (a, b) in efectos.LIMITES.items()},
        "continuos": list(efectos.CONTINUOS),
    }


@app.post("/api/animaciones", status_code=201)
def api_guardar_plantilla(p: dict):
    """Guarda una plantilla propia (duplicada o editada desde un curso)."""
    return animacion.guardar_propia(p)


@app.delete("/api/animaciones/{id_}", status_code=204)
def api_borrar_plantilla(id_: str):
    animacion.borrar_propia(id_)


@app.get("/api/estilos")
def api_estilos():
    """Los estilos para elegir (Educativo, Corporativo, Social…), con lo que cambia cada uno."""
    camaras, transiciones = catalogo.CAMARA, catalogo.TRANSICION
    return [{**e, "camara_nombre": camaras[e["camara"]], "transicion_nombre": transiciones[e["transicion"]],
             "musica_nombre": estilos.ENERGIAS.get(e["musica"]) if e["musica"] else None}
            for e in estilos.estilos().values()]


class EleccionEstilo(BaseModel):
    estilo: str
    con_formato: bool = True  # también cambia el formato al sugerido por el estilo


@app.put("/api/trabajos/{id_}/estilo")
def api_aplicar_estilo(id_: str, cuerpo: EleccionEstilo):
    t = estilos.aplicar(_trabajo_o_404(id_), cuerpo.estilo, cuerpo.con_formato)
    taller.guardar(t)
    return _trabajo_completo(t)


@app.get("/api/trabajos/{id_}/linea/{clave}")
def api_linea_de_tiempo(id_: str, clave: str):
    """La línea de tiempo de un video: escenas, voz, música, efectos y subtítulos.

    Si el video ya se produjo, con los tiempos reales (`videospec.json`); si no, con los estimados del plan.
    """
    t = _trabajo_o_404(id_)
    if clave not in {v["clave"] for v in t["videos"]}:
        raise HTTPException(404, "Ese curso no tiene ese video")
    ruta = produccion.carpeta_salida(t, clave) / "videospec.json"
    real = videospec.leer(ruta) if ruta.exists() else None
    if real is not None and real.firma != produccion.firma(t):
        real = None  # se cambió algo después de producirlo: vale el plan nuevo
    return videospec.linea_de_tiempo(real or videospec.construir(t, clave, produccion.firma(t), produccion.formato(t)))


@app.get("/api/catalogo/escena")
def api_catalogo_escena():
    """Los movimientos de cámara y las transiciones que se pueden elegir (nada fuera de aquí se ejecuta)."""
    return {"camaras": [{"id": k, "nombre": v} for k, v in catalogo.CAMARA.items()],
            "transiciones": [{"id": k, "nombre": v} for k, v in catalogo.TRANSICION.items()],
            "formatos": [{"id": k, "nombre": v, "ancho": escenas.FORMATOS[k][0], "alto": escenas.FORMATOS[k][1]}
                         for k, v in taller.FORMATOS.items()]}


@app.put("/api/trabajos/{id_}/escena")
def api_guardar_escena(id_: str, e: dict):
    """Cámara y transición del curso y, si se quiere, de cada lámina."""
    t = _trabajo_o_404(id_)
    limpio = catalogo.validar_escena(e)
    if limpio:
        t["escena"] = limpio
    else:
        t.pop("escena", None)
    taller.guardar(t)
    return _trabajo_completo(t)


@app.get("/api/trabajos/{id_}/animacion")
def api_animacion_curso(id_: str):
    t = _trabajo_o_404(id_)
    a = animacion.validar_curso(t.get("animacion"))
    return {"animacion": a, "defecto": configuracion.leer()["cursos"]["animacion"],
            "plantilla": animacion.plan(t, t["laminas"][0]["n"])["plantilla"] if t["laminas"] else None}


@app.put("/api/trabajos/{id_}/animacion")
def api_guardar_animacion_curso(id_: str, a: dict):
    t = _trabajo_o_404(id_)
    t["animacion"] = animacion.validar_curso(a)
    taller.guardar(t)
    return _trabajo_completo(t)


def _escena_vista_previa(t: dict, n: int, a: dict | None, formato: str) -> str:
    """El HTML de una lámina con sus animaciones corriendo en bucle, para verla en el navegador."""
    if formato not in escenas.FORMATOS:
        raise ValueError("Formato desconocido")
    lamina = next((l for l in t["laminas"] if l["n"] == n), None)
    if lamina is None:
        raise HTTPException(404, "Ese curso no tiene esa lámina")
    video = next((v for v in t["videos"] if n in v["laminas"]), {"titulo": t["nombre"], "laminas": [n]})
    indice = video["laminas"].index(n)
    prueba = {**t, "animacion": animacion.validar_curso(a) if a is not None else t.get("animacion")}
    plan = animacion.plan(prueba, n)
    media = recursos.media(t)
    vista = escenas.vista(lamina, indice, len(video["laminas"]), video["titulo"], media, t["nombre"])
    ent, sal = animacion.duraciones(plan, vista)
    segundos = round(ent + 1.6 + sal, 2)
    marca = datos.marcas()[t["marca"]]
    logo = recursos.logo(marca)
    html = escenas.html(vista, escenas.estilo(marca, logo), formato, plan=plan, segundos=segundos)
    # En el navegador no se abren rutas locales (file://): se sirven por la API.
    html = html.replace(escenas.FUENTE.resolve().as_uri(), "/api/escenas/fuente.ttf")
    if logo:
        html = html.replace(logo.resolve().as_uri(), f"/api/escenas/logo/{t['marca']}")
    if media:
        html = html.replace(media.resolve().as_uri() + "/", f"/api/trabajos/{t['id']}/media/")
    bucle = (f"<script>setInterval(() => {{ for (const a of document.getAnimations()) {{ a.currentTime = 0; a.play(); }} }},"
             f" {int(segundos * 1000) + 700});</script>")
    return html.replace("</body>", bucle + "</body>")


class VistaPrevia(BaseModel):
    animacion: dict | None = None  # sin guardar: lo que se está editando
    formato: str = "16:9"


@app.post("/api/trabajos/{id_}/escena/{n}", response_class=HTMLResponse)
def api_vista_previa(id_: str, n: int, cuerpo: VistaPrevia):
    return HTMLResponse(_escena_vista_previa(_trabajo_o_404(id_), n, cuerpo.animacion, cuerpo.formato))


@app.get("/api/trabajos/{id_}/escena/{n}", response_class=HTMLResponse)
def api_vista_previa_guardada(id_: str, n: int, formato: str = "16:9"):
    return HTMLResponse(_escena_vista_previa(_trabajo_o_404(id_), n, None, formato))


@app.get("/api/escenas/fuente.ttf")
def api_fuente():
    # La vista previa corre en un iframe aislado (origen «null»): la fuente (OFL, pública) se permite a cualquiera.
    return FileResponse(escenas.FUENTE, media_type="font/ttf", headers={"Access-Control-Allow-Origin": "*"})


@app.get("/api/escenas/logo/{marca}")
def api_logo_escena(marca: str):
    m = datos.marcas().get(marca)
    ruta = recursos.logo(m) if m else None
    if ruta is None:
        raise HTTPException(404)
    return FileResponse(ruta)


@app.get("/api/trabajos/{id_}/media/{nombre}")
def api_media_trabajo(id_: str, nombre: str):
    """Las imágenes extraídas del PPTX del curso (solo imágenes, solo de su carpeta)."""
    t = _trabajo_o_404(id_)
    ruta = taller.ruta_trabajo(t["id"]).parent / "media" / Path(nombre).name
    imagenes = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".tif", ".tiff", ".emf", ".wmf"}
    if ruta.suffix.lower() not in imagenes or not ruta.is_file():
        raise HTTPException(404)
    return FileResponse(ruta)


# ── Agentes ──────────────────────────────────────────────────────────────────

@app.get("/api/agentes")
def api_agentes():
    """Cada agente: qué hace, dónde aparece, si está activo y si hoy puede usar IA (Ollama y su modelo)."""
    return agentes.estado_agentes()


def _agentes_curso(t: dict) -> dict:
    estados = {}
    for a in agentes.REGISTRO:
        e = cola.estado(t["id"], f"{cola.PREFIJO_AGENTE}{a}")
        estados[a] = {k: e.get(k) for k in ("estado", "paso", "progreso", "mensaje", "propuestas", "con_ia")} if e else None
    return {"agentes": agentes.estado_agentes(), "estados": estados, "propuestas": t.get("propuestas", [])}


@app.get("/api/trabajos/{id_}/agentes")
def api_agentes_curso(id_: str):
    return _agentes_curso(_trabajo_o_404(id_))


@app.post("/api/trabajos/{id_}/agentes/{agente}", status_code=202)
def api_ejecutar_agente(id_: str, agente: str):
    """Pone al agente en la cola, en su propio carril: no espera a los renders."""
    t = _trabajo_o_404(id_)
    if agente not in agentes.REGISTRO:
        raise HTTPException(404, "No existe ese agente")
    if not configuracion.leer()["agentes"]["activos"].get(agente, True):
        raise ValueError(f"{agentes.REGISTRO[agente].nombre} está desactivado en Configuración")
    cola.encolar(id_, f"{cola.PREFIJO_AGENTE}{agente}")
    return _agentes_curso(t)


@app.post("/api/trabajos/{id_}/agentes/{agente}/aceptar")
def api_aceptar_todas(id_: str, agente: str):
    """Acepta todas las propuestas pendientes de un agente en una sola petición."""
    if agente not in agentes.REGISTRO:
        raise HTTPException(404, "No existe ese agente")
    with taller.candado(id_):
        t, errores = agentes.aceptar_todas(_trabajo_o_404(id_), agente)
    return {**_trabajo_completo(t), **_agentes_curso(t), "errores": errores}


@app.post("/api/trabajos/{id_}/propuestas/{pid}/{accion}")
def api_resolver_propuesta(id_: str, pid: str, accion: str):
    """Acepta (aplica al curso) o descarta una propuesta. Devuelve el curso y los agentes."""
    if accion not in ("aceptar", "descartar"):
        raise HTTPException(404)
    with taller.candado(id_):
        t = _trabajo_o_404(id_)
        t = agentes.aceptar(t, pid) if accion == "aceptar" else agentes.descartar(t, pid)
    return {**_trabajo_completo(t), **_agentes_curso(t)}


@app.get("/api/trabajos/{id_}/banco.gift")
def api_banco_gift(id_: str):
    t = _trabajo_o_404(id_)
    if not t.get("banco"):
        raise HTTPException(404, "Este curso no tiene banco de preguntas")
    return Response(agentes_entrega.a_gift(t["banco"]), media_type="text/plain; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{t["id"]}-preguntas.gift.txt"'})


@app.get("/api/trabajos/{id_}/banco.xml")
def api_banco_moodle(id_: str):
    t = _trabajo_o_404(id_)
    if not t.get("banco"):
        raise HTTPException(404, "Este curso no tiene banco de preguntas")
    return Response(agentes_entrega.a_moodle_xml(t["banco"]), media_type="application/xml",
                    headers={"Content-Disposition": f'attachment; filename="{t["id"]}-preguntas.moodle.xml"'})


# ── Configuración y diagnóstico ──────────────────────────────────────────────

def _opciones() -> dict:
    """Los valores permitidos, para que la interfaz arme sus listas."""
    return {f"{g}.{k}": [{"valor": v, "texto": txt} for v, txt in ops.items()]
            for (g, k), ops in configuracion.OPCIONES.items()} | {
        f"{g}.{k}": {"min": a, "max": b} for (g, k), (a, b) in configuracion.RANGOS.items()}


@app.get("/api/configuracion")
def api_configuracion():
    return {"configuracion": configuracion.leer(), "opciones": _opciones(), "musica": configuracion.pistas(),
            "por_curso": list(configuracion.POR_CURSO)}


@app.put("/api/configuracion")
def api_guardar_configuracion(conf: dict):
    return {"configuracion": configuracion.guardar(conf), "opciones": _opciones(), "musica": configuracion.pistas(),
            "por_curso": list(configuracion.POR_CURSO)}


@app.get("/api/sistema")
def api_sistema(forzar: bool = False):
    """Qué tiene este equipo para producir (ffmpeg, navegador, voces, clave, Ollama, disco)."""
    return diagnostico.revisar(forzar)


MAX_MUSICA = 50 * 1024 * 1024


@app.post("/api/musica", status_code=201)
async def api_subir_musica(archivo: UploadFile = File(...), licencia: str = Form(""), fuente: str = Form(""),
                           energia: str = Form("")):
    """Sube una pista de música de fondo. La licencia es obligatoria: los videos se entregan a clientes."""
    nombre = Path(archivo.filename or "").name
    extension = Path(nombre).suffix.lower()
    if extension not in configuracion.EXTENSIONES_MUSICA:
        raise ValueError("La música tiene que ser mp3, wav, m4a, ogg o flac")
    if len(licencia.strip()) < 3:
        raise ValueError("Escribe la licencia de la pista (p. ej. «Pixabay Content License»)")
    limpio = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(nombre).stem).strip("-")[:60] or "pista"
    contenido = await archivo.read(MAX_MUSICA + 1)
    if len(contenido) > MAX_MUSICA:
        raise ValueError("La pista pasa de 50 MB")
    carpeta = configuracion.carpeta_musica()
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{limpio}{extension}").write_bytes(contenido)
    (carpeta / f"{limpio}.json").write_text(
        json.dumps({"licencia": licencia.strip(), "fuente": fuente.strip(), "energia": energia if energia in estilos.ENERGIAS else None},
                   ensure_ascii=False), encoding="utf-8")
    return configuracion.pistas()


@app.get("/api/musica/{archivo}")
def api_escuchar_musica(archivo: str):
    ruta = configuracion.carpeta_musica() / Path(archivo).name
    if ruta.suffix.lower() not in configuracion.EXTENSIONES_MUSICA or not ruta.is_file():
        raise HTTPException(404)
    return FileResponse(ruta)


# ── Videos producidos ────────────────────────────────────────────────────────

@app.get("/api/proyectos")
def api_proyectos():
    return {
        "proyectos": datos.proyectos(),
        "carpetas": len(datos.carpetas_videos()),
        "sin_registrar": datos.sin_registrar(),
    }


@app.get("/api/proyectos/{id_}")
def api_proyecto(id_: str):
    p = datos.proyecto(id_)
    if p is None:
        raise HTTPException(404, "No encontramos ese video")
    return p


class CambioEstado(BaseModel):
    estado: str
    quien: str
    nota: str = ""


@app.post("/api/proyectos/{id_}/estado")
def api_cambiar_estado(id_: str, cambio: CambioEstado):
    try:
        datos.cambiar_estado(id_, cambio.estado, cambio.quien, cambio.nota)
    except KeyError:
        raise HTTPException(404, "No encontramos ese video")
    return datos.proyecto(id_)


# ── Empresas ─────────────────────────────────────────────────────────────────

@app.get("/api/empresas")
def api_empresas():
    """Todas las empresas: las marcas de siempre y las registradas, con cuánto se usan."""
    cursos = Counter(t["marca"] for t in taller.lista())
    videos = Counter(p["marca"] for p in datos.proyectos())
    return [{**_con_medios(m), "cursos": cursos[m["id"]], "videos": videos[m["id"]]} for m in datos.marcas().values()]


async def _leer_logo(logo: UploadFile | None) -> bytes | None:
    if logo is None or not logo.filename:
        return None
    contenido = await logo.read(empresas.MAX_LOGO + 1)
    if len(contenido) > empresas.MAX_LOGO:
        raise ValueError("El logo pesa más de 5 MB")
    return contenido


def _campos(datos_json: str) -> dict:
    try:
        campos = json.loads(datos_json)
    except json.JSONDecodeError:
        raise ValueError("Los datos de la empresa no llegaron bien")
    if not isinstance(campos, dict):
        raise ValueError("Los datos de la empresa no llegaron bien")
    return campos


@app.post("/api/empresas/colores")
async def api_colores_logo(logo: UploadFile = File(...)):
    """Los colores que propone el estudio a partir del logo."""
    contenido = await _leer_logo(logo)
    if not contenido:
        raise ValueError("Sube el logo para proponer sus colores")
    return {"colores": empresas.colores_de_logo(contenido)}


@app.post("/api/empresas", status_code=201)
async def api_registrar_empresa(datos_empresa: str = Form(..., alias="datos"), logo: UploadFile | None = File(None)):
    m = empresas.registrar(_campos(datos_empresa), await _leer_logo(logo))
    return _con_medios(m)


@app.put("/api/empresas/{id_}")
async def api_editar_empresa(id_: str, datos_empresa: str = Form(..., alias="datos"), logo: UploadFile | None = File(None)):
    if id_ in datos.marcas() and not empresas.es_registrada(id_):
        raise ValueError("Esta es una de las marcas base del estudio: se edita en su ficha, no desde aquí")
    try:
        m = empresas.actualizar(id_, _campos(datos_empresa), await _leer_logo(logo))
    except KeyError:
        raise HTTPException(404, "No encontramos esa empresa")
    return _con_medios(m)


@app.delete("/api/empresas/{id_}", status_code=204)
def api_eliminar_empresa(id_: str):
    if id_ in datos.marcas() and not empresas.es_registrada(id_):
        raise ValueError("Esta es una de las marcas base del estudio: no se puede eliminar")
    try:
        empresas.eliminar(id_)
    except KeyError:
        raise HTTPException(404, "No encontramos esa empresa")


# ── Marcas, pendientes y casos ───────────────────────────────────────────────

@app.get("/api/marcas/{id_}")
def api_marca(id_: str):
    m = datos.marcas().get(id_)
    if m is None:
        raise HTTPException(404, "No encontramos esa marca")
    fuentes = [{**f, "url": f"/media/repo/{f['donde']}" if datos.ruta_segura("repo_videos", f["donde"])
                else (f["donde"] if f["donde"].startswith("https://") else None)} for f in m.get("fuentes", [])]
    return {**_con_medios(m), "fuentes": fuentes, "proyectos": [p for p in datos.proyectos() if p["marca"] == id_]}


@app.get("/api/pendientes")
def api_pendientes():
    return {
        "pendientes": [{**x, "marca": x["marca"]["id"]} for x in datos.pendientes()],
        "sin_estado": [p for p in datos.proyectos() if p["estado"] == "sin_estado"],
        "sin_registrar": datos.sin_registrar(),
    }


@app.get("/api/casos/{id_}")
def api_caso(id_: str):
    caso = next((c for c in _casos() if c["id"] == id_), None)
    if caso is None:
        raise HTTPException(404, "No encontramos ese caso")
    doc = caso.get("documento")
    return {**caso, "documento_url": f"/media/repo/{doc}" if doc and datos.ruta_segura("repo_videos", doc) else None}


# ── Archivos ─────────────────────────────────────────────────────────────────

@app.get("/media/entregables/{ruta:path}")
def media_entregable(ruta: str):
    archivo = datos.ruta_segura("entregables", ruta)
    if archivo is None or archivo.suffix.lower() not in EXTENSIONES_ENTREGABLES:
        raise HTTPException(404)
    return FileResponse(archivo)


@app.get("/media/empresas/{archivo}")
def media_logo_empresa(archivo: str):
    ruta = empresas.ruta_logo(archivo)
    if ruta is None:
        raise HTTPException(404)
    return FileResponse(ruta, media_type="image/png")


@app.get("/media/repo/{ruta:path}")
def media_repo(ruta: str):
    archivo = datos.ruta_segura("repo_videos", ruta)
    if archivo is None or archivo.suffix.lower() not in EXTENSIONES_REPO:
        raise HTTPException(404)
    return FileResponse(archivo)


# ── La aplicación Vue ────────────────────────────────────────────────────────

@app.get("/api/{resto:path}", include_in_schema=False)
def api_no_existe(resto: str):
    raise HTTPException(404, "Esa dirección de la API no existe")


@app.get("/{ruta:path}", include_in_schema=False)
def interfaz(ruta: str):
    """Archivos de `frontend/dist`; cualquier otra ruta es de la aplicación y devuelve index.html."""
    if not (DIST / "index.html").exists():
        return JSONResponse({"detail": "La interfaz no está compilada: ejecuta «npm run build» en frontend/"}, status_code=503)
    archivo = (DIST / ruta).resolve()
    if ruta and archivo.is_relative_to(DIST.resolve()) and archivo.is_file():
        return FileResponse(archivo)
    return FileResponse(DIST / "index.html")
