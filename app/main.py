import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import Markup, escape

from app import datos, extractor, taller
from motor import cola
from motor import voz as motor_voz

AQUI = Path(__file__).resolve().parent

app = FastAPI(title="Estudio de video RiskMann")
app.mount("/static", StaticFiles(directory=AQUI / "static"), name="static")
plantillas = Jinja2Templates(directory=AQUI / "templates")
plantillas.env.globals.update(ESTADOS=datos.ESTADOS, FAMILIAS=datos.FAMILIAS, CONFIG=datos.CONFIG)
plantillas.env.filters["en_repo"] = lambda rel: datos.ruta_segura("repo_videos", rel) is not None
plantillas.env.filters["en_entregables"] = lambda rel: bool(rel) and datos.ruta_segura("entregables", rel) is not None
plantillas.env.filters["mmss"] = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
plantillas.env.filters["titulo_lamina"] = extractor.titulo_lamina
plantillas.env.filters["segundos"] = extractor.segundos
plantillas.env.filters["cuenta"] = lambda n, uno, varios=None: f"{n} {uno if n == 1 else (varios or uno + 's')}"


def _marcar(texto: str) -> Markup:
    """Escapa el texto y resalta las cifras y normas que hay que revisar contra su fuente."""
    return Markup(extractor._NORMATIVO.sub(lambda m: f"<mark>{m.group(0)}</mark>", str(escape(texto))))


plantillas.env.filters["marcar"] = _marcar

# Lo único que se sirve del repositorio de videos: imágenes, PDF y texto. Nunca código ni claves.
EXTENSIONES_REPO = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf", ".md", ".txt"}


# Lo que se le dice a la persona después de una acción (`?ok=<clave>` en la redirección).
MENSAJES = {
    "creado": "Listo: leímos tu presentación. Revisa el guion y elige la marca y la voz.",
    "guardado": "Cambios guardados.",
    "estado": "Estado actualizado.",
    "eliminado": "El curso se eliminó.",
    "produciendo": "El video entró a la cola. Puedes seguir trabajando: aparece aquí cuando esté listo.",
}


def _pagina(request: Request, nombre: str, **contexto):
    contexto.setdefault("marcas", datos.marcas())
    contexto["ruta"] = request.url.path
    contexto["pendientes_abiertos"] = sum(not x["hecho"] for x in datos.pendientes())
    contexto["mensaje_ok"] = MENSAJES.get(request.query_params.get("ok", ""))
    return plantillas.TemplateResponse(request, nombre, contexto)


MAX_PPTX = 200 * 1024 * 1024


def _casos() -> list[dict]:
    casos = json.loads((datos.RAIZ_DATOS / "casos.json").read_text(encoding="utf-8"))
    for c in casos:
        c["salida"] = [p for p in (datos.proyecto(i) for i in c["sale"]) if p]
        c["videos"] = [e for p in c["salida"] for e in p["entregables_detalle"] if e["existe"]]
    return casos


@app.get("/")
def inicio(request: Request):
    return _pagina(request, "inicio.html", cifras=taller.cifras_csm(), trabajos=taller.lista(),
                   casos=_casos(), ejemplo=taller.ejemplo_disponible())


@app.get("/taller/nuevo")
def taller_nuevo(request: Request, error: str = ""):
    return _pagina(request, "taller_nuevo.html", error=error, ejemplo=taller.ejemplo_disponible())


@app.post("/taller/nuevo")
async def taller_subir(archivo: UploadFile = File(...), nombre: str = Form("")):
    def volver(msg):
        return RedirectResponse(f"/taller/nuevo?error={quote(msg)}", status_code=303)

    if not (archivo.filename or "").lower().endswith(".pptx"):
        return volver("El archivo tiene que ser un .pptx de PowerPoint")
    contenido = await archivo.read(MAX_PPTX + 1)
    if len(contenido) > MAX_PPTX:
        return volver("El archivo pasa de 200 MB")
    try:
        t = taller.desde_pptx(archivo.filename, contenido, nombre)
    except ValueError as e:
        return volver(str(e))
    return RedirectResponse(f"/taller/{t['id']}?ok=creado", status_code=303)


@app.post("/taller/ejemplo-csm")
def taller_ejemplo():
    try:
        t = taller.desde_csm()
    except ValueError as e:
        return RedirectResponse(f"/taller/nuevo?error={quote(str(e))}", status_code=303)
    return RedirectResponse(f"/taller/{t['id']}?ok=creado", status_code=303)


def _trabajo(id_: str) -> dict:
    t = taller.cargar(id_)
    if t is None:
        raise HTTPException(404, "Trabajo no encontrado")
    return t


@app.get("/taller/{id_}")
def taller_ver(request: Request, id_: str, error: str = ""):
    t = _trabajo(id_)
    voces = taller.voces()
    voz = next((v for v in voces if v["id"] == t["voz"]), {})
    return _pagina(request, "taller.html", t=t, r=taller.resumen(t), voces=voces,
                   FORMATOS=taller.FORMATOS, error=error, render=cola.estados(t),
                   voz_falta=motor_voz.disponible(voz), voz_borrador=bool(voz.get("solo_borrador")))


@app.post("/taller/{id_}/ajustes")
def taller_ajustes(request: Request, id_: str, marca: str = Form(...), voz: str = Form(...),
                   formatos: list[str] = Form([])):
    """Guarda marca, voz y formatos. Con JavaScript responde JSON (guardado automático)."""
    t = _trabajo(id_)
    quiere_json = "application/json" in request.headers.get("accept", "")
    try:
        taller.ajustar(t, marca, voz, formatos)
    except ValueError as e:
        if quiere_json:
            return JSONResponse({"ok": False, "mensaje": str(e)}, status_code=400)
        return RedirectResponse(f"/taller/{id_}?error={quote(str(e))}#ajustes", status_code=303)
    if quiere_json:
        return JSONResponse({"ok": True, "mensaje": MENSAJES["guardado"]})
    return RedirectResponse(f"/taller/{id_}?ok=guardado#sale", status_code=303)


@app.post("/taller/{id_}/eliminar")
def taller_eliminar(id_: str):
    _trabajo(id_)
    taller.eliminar(id_)
    return RedirectResponse("/?ok=eliminado", status_code=303)


def _descarga(contenido, nombre: str) -> Response:
    return Response(json.dumps(contenido, ensure_ascii=False, indent=1), media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="{nombre}"'})


@app.post("/taller/{id_}/producir/{clave}")
def taller_producir(id_: str, clave: str):
    """Pone un video del trabajo en la cola del motor."""
    t = _trabajo(id_)
    if clave not in {v["clave"] for v in t["videos"]}:
        raise HTTPException(404, "Video no encontrado")
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    falta = motor_voz.disponible(voz)
    if falta:
        return RedirectResponse(f"/taller/{id_}?error={quote(falta)}#sale", status_code=303)
    cola.encolar(id_, clave)
    return RedirectResponse(f"/taller/{id_}?ok=produciendo#sale", status_code=303)


@app.get("/taller/{id_}/render")
def taller_render(id_: str):
    """Estado de producción de cada video (la página lo consulta mientras produce)."""
    t = _trabajo(id_)
    return {c: ({k: e.get(k) for k in ("estado", "paso", "progreso", "mensaje")} if e else None)
            for c, e in cola.estados(t).items()}


# Lo que se puede bajar de la salida de un video.
SALIDA = {".mp4": "video/mp4", ".vtt": "text/vtt", ".srt": "application/x-subrip", ".json": "application/json"}


@app.get("/taller/{id_}/salida/{clave}/{archivo}")
def taller_salida(id_: str, clave: str, archivo: str, descargar: bool = False):
    t = _trabajo(id_)
    permitidos = {f"{clave}.mp4", f"{clave}.vtt", f"{clave}.srt", "qa.json"}
    if not re.fullmatch(r"[a-z0-9-]+", clave) or archivo not in permitidos:
        raise HTTPException(404)
    ruta = taller.ruta_trabajo(t["id"]).parent / "salida" / clave / archivo
    if not ruta.is_file():
        raise HTTPException(404)
    extension = ruta.suffix
    nombre = f"{t['id']}-{archivo}" if descargar else None
    return FileResponse(ruta, media_type=SALIDA[extension], filename=nombre,
                        content_disposition_type="attachment" if descargar else "inline")


@app.get("/taller/{id_}/curso.json")
def taller_curso_json(id_: str):
    return _descarga(taller.curso_json(_trabajo(id_)), "curso.json")


@app.get("/taller/{id_}/orden.json")
def taller_orden(id_: str):
    t = _trabajo(id_)
    return _descarga(taller.orden_produccion(t), f"orden-{t['id']}.json")


@app.get("/taller/{id_}/banco.json")
def taller_banco(id_: str):
    t = _trabajo(id_)
    if not t.get("banco"):
        raise HTTPException(404, "Este trabajo no tiene banco de preguntas")
    return _descarga(t["banco"], "banco-preguntas.json")


@app.get("/casos/{id_}")
def ver_caso(request: Request, id_: str):
    caso = next((c for c in _casos() if c["id"] == id_), None)
    if caso is None:
        raise HTTPException(404, "Caso no encontrado")
    return _pagina(request, "caso.html", c=caso)


@app.get("/proyectos")
def lista_proyectos(request: Request, marca: str = "", estado: str = "", familia: str = ""):
    todos = datos.proyectos()
    filtrados = [
        p for p in todos
        if (not marca or p["marca"] == marca)
        and (not estado or p["estado"] == estado)
        and (not familia or p["familia"] == familia)
    ]
    return _pagina(
        request, "proyectos.html",
        proyectos=filtrados, total=len(todos),
        carpetas=len(datos.carpetas_videos()), sin_registrar=len(datos.sin_registrar()),
        conteo=Counter(p["estado"] for p in todos),
        filtro={"marca": marca, "estado": estado, "familia": familia},
    )


@app.get("/proyectos/{id_}")
def ver_proyecto(request: Request, id_: str, error: str = ""):
    p = datos.proyecto(id_)
    if p is None:
        raise HTTPException(404, "Proyecto no encontrado")
    return _pagina(request, "proyecto.html", p=p, error=error)


@app.post("/proyectos/{id_}/estado")
def cambiar_estado(id_: str, estado: str = Form(...), quien: str = Form(""), nota: str = Form("")):
    try:
        datos.cambiar_estado(id_, estado, quien, nota)
    except KeyError:
        raise HTTPException(404, "Proyecto no encontrado")
    except ValueError as e:
        return RedirectResponse(f"/proyectos/{id_}?error={quote(str(e))}", status_code=303)
    return RedirectResponse(f"/proyectos/{id_}?ok=estado", status_code=303)


@app.get("/marcas/{id_}")
def ver_marca(request: Request, id_: str):
    m = datos.marcas().get(id_)
    if m is None:
        raise HTTPException(404, "Marca no encontrada")
    suyos = [p for p in datos.proyectos() if p["marca"] == id_]
    return _pagina(request, "marca.html", m=m, proyectos=suyos)


@app.get("/pendientes")
def ver_pendientes(request: Request, ver: str = "abiertos"):
    todos = datos.pendientes()
    lista = todos if ver == "todos" else [x for x in todos if not x["hecho"]]
    sin_estado = [p for p in datos.proyectos() if p["estado"] == "sin_estado"]
    return _pagina(request, "pendientes.html", lista=lista, ver=ver,
                   abiertos=sum(not x["hecho"] for x in todos), sin_estado=sin_estado,
                   sin_registrar=datos.sin_registrar())


@app.get("/media/entregables/{ruta:path}")
def media_entregable(ruta: str):
    archivo = datos.ruta_segura("entregables", ruta)
    if archivo is None or archivo.suffix.lower() not in {".mp4", ".webm", ".mp3", ".txt"}:
        raise HTTPException(404)
    return FileResponse(archivo)


@app.get("/media/repo/{ruta:path}")
def media_repo(ruta: str):
    archivo = datos.ruta_segura("repo_videos", ruta)
    if archivo is None or archivo.suffix.lower() not in EXTENSIONES_REPO:
        raise HTTPException(404)
    return FileResponse(archivo)
