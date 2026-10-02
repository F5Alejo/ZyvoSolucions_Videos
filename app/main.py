"""API del estudio de video y servidor de la interfaz (Vue, en `frontend/dist`).

Todo lo que la interfaz necesita sale de `/api/*`. `/media/*` sirve los videos, logos y PDF
del repositorio de videos en solo lectura. Cualquier otra ruta devuelve la aplicación Vue.
"""

import json
from collections import Counter
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel

from app import datos, empresas, extractor, taller

RAIZ = Path(__file__).resolve().parent.parent
DIST = RAIZ / "frontend" / "dist"
MAX_PPTX = 200 * 1024 * 1024
# Lo único que se sirve del repositorio de videos: imágenes, PDF y texto. Nunca código ni claves.
EXTENSIONES_REPO = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf", ".md", ".txt"}
EXTENSIONES_ENTREGABLES = {".mp4", ".webm", ".mp3", ".txt"}

app = FastAPI(title="Estudio de video RiskMann", docs_url="/api/docs", openapi_url="/api/openapi.json")


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
        {**l, "titulo": extractor.titulo_lamina(l), "segundos": extractor.segundos(l["notas"]),
         "citas": extractor.afirmaciones_normativas(l["notas"])}
        for l in t["laminas"]
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
                   if v.get("muestra") and datos.ruta_segura("entregables", v["muestra"]) else None}
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
