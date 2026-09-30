"""El taller: lo que entra (un PPTX) y lo que sale (el curso en video).

Un *trabajo* es una carpeta en `datos/trabajos/<id>/` con `trabajo.json` y, si se subió,
`entrada.pptx`. No se guarda en git: es material del cliente.
"""

import ast
import json
import re
import secrets
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path

from app import datos, extractor

FORMATOS = {"16:9": "Horizontal 16:9", "9:16": "Vertical 9:16"}


def _raiz() -> Path:
    return datos.RAIZ_DATOS / "trabajos"


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "curso"


def voces() -> list[dict]:
    return json.loads((datos.RAIZ_DATOS / "voces.json").read_text(encoding="utf-8"))


# ── Crear ────────────────────────────────────────────────────────────────────

def _nuevo(nombre: str, origen: dict, laminas: list[dict], videos: list[dict],
           excluidas: dict, banco: dict | None = None) -> dict:
    from app import configuracion  # aquí para evitar un import circular al arrancar

    id_ = f"{_slug(nombre)}-{secrets.token_hex(3)}"
    defecto = configuracion.leer()["cursos"]
    t = {
        "id": id_,
        "nombre": nombre,
        "creado": datetime.now().isoformat(timespec="seconds"),
        "origen": origen,
        "marca": defecto["marca"],
        "voz": defecto["voz"],
        "formatos": list(defecto["formatos"]),
        "laminas": laminas,
        "videos": videos,
        "excluidas": {str(k): v for k, v in excluidas.items()},
        "banco": banco,
    }
    (_raiz() / id_).mkdir(parents=True)
    guardar(t)
    return t


def desde_pptx(nombre_archivo: str, contenido: bytes, nombre: str = "") -> dict:
    tmp = _raiz() / f"_subida-{secrets.token_hex(4)}.pptx"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_bytes(contenido)
    try:
        laminas = extractor.leer_pptx(tmp)
    except Exception:
        tmp.unlink()
        raise ValueError("No se pudo leer el archivo: ¿es un PPTX de PowerPoint?")
    if not laminas:
        tmp.unlink()
        raise ValueError("El PPTX no tiene láminas")
    nombre = nombre.strip() or Path(nombre_archivo).stem
    t = _nuevo(
        nombre,
        {"tipo": "pptx", "archivo": nombre_archivo, "bytes": len(contenido)},
        laminas, extractor.agrupar(laminas), excluidas={},
    )
    entrada = _raiz() / t["id"] / "entrada.pptx"
    tmp.replace(entrada)
    extractor.guardar_imagenes(entrada, _raiz() / t["id"] / "media")
    return t


def _csm_dir() -> Path | None:
    repo = datos.CONFIG.get("repo_videos")
    d = repo / "videos" / "csm-curso" / "datos" if repo else None
    return d if d and (d / "curso.json").exists() else None


def ejemplo_disponible() -> bool:
    return _csm_dir() is not None


def _leer_banco(ruta: Path) -> dict | None:
    """Lee CURSO, VIDEOS y FINAL de banco_preguntas.py sin ejecutarlo (solo literales)."""
    if not ruta.exists():
        return None
    valores = {}
    for nodo in ast.parse(ruta.read_text(encoding="utf-8")).body:
        if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name):
            try:
                valores[nodo.targets[0].id] = ast.literal_eval(nodo.value)
            except ValueError:
                pass
    videos = list(valores.get("VIDEOS", []))
    if "FINAL" in valores:
        videos.append(valores["FINAL"])
    return {
        "nombre": valores.get("CURSO", {}).get("nombre"),
        "grupos": [
            {"clave": c, "titulo": t, "tema": tema,
             "preguntas": [{"enunciado": p[0], "correcta": p[1], "distractores": list(p[2:4]), "fuente": p[4]}
                           for p in ps]}
            for c, t, tema, ps in videos
        ],
    }


def _armar_csm() -> dict:
    """El curso csm tal como se produjo: su curso.json, sus módulos y su banco de preguntas."""
    d = _csm_dir()
    if d is None:
        raise ValueError("El repositorio de videos no está configurado")
    laminas = json.loads((d / "curso.json").read_text(encoding="utf-8"))
    partes = json.loads((d / "guion-partes.json").read_text(encoding="utf-8")) if (d / "guion-partes.json").exists() else {}
    for l in laminas:
        # Las Partes 2 y 3 se narraron con guion-partes.json: sus notas del PPTX solo dicen «Parte N…».
        if str(l["n"]) in partes:
            l["notas_pptx"] = l["notas"]
            l["notas"] = partes[str(l["n"])]
            l["frases"] = extractor.frases(l["notas"])
            l["fuente_narracion"] = "guion-partes.json (armado con lo que muestra la lámina)"

    banco = _leer_banco(d / "banco_preguntas.py")
    titulos = {g["clave"]: g["titulo"] + " · " + g["tema"] for g in (banco or {}).get("grupos", [])}
    # Los grupos de csm.py (LIMITES), con la apertura partida como en el banco.
    grupos = [("ap1", [1, 2]), ("ap2", [3])]
    grupos += [(f"m{m:02d}", [4 * m, 4 * m + 1, 4 * m + 2]) for m in range(1, 13)]
    grupos += [("cierre", [54, 55])]
    videos = [{"clave": c, "titulo": titulos.get(c, c), "laminas": ls} for c, ls in grupos]

    excluidas = {4 * m + 3: "Parte 4: evaluación del módulo; va a la plataforma, no al video" for m in range(1, 13)}
    excluidas.update({52: "Evaluación final (caso integrador); va al banco de preguntas",
                      53: "Estructura pedagógica: describe las evaluaciones"})
    return {
        "nombre": "Conducción Segura y Manejo Defensivo",
        "origen": {"tipo": "ejemplo", "archivo": "videos/csm-curso/datos/curso.json",
                   "nota": "El PPTX original no está en el repositorio: se parte del curso.json que se extrajo de él."},
        "laminas": laminas, "videos": videos, "excluidas": excluidas, "banco": banco,
    }


def desde_csm() -> dict:
    c = _armar_csm()
    return _nuevo(c["nombre"], c["origen"], c["laminas"], c["videos"], c["excluidas"], c["banco"])


def cifras_csm() -> dict | None:
    """Las cifras reales del curso csm, para la portada: lo que entró y lo que salió."""
    if not ejemplo_disponible():
        return None
    c = _armar_csm()
    r = resumen({**c, "excluidas": {str(k): v for k, v in c["excluidas"].items()}, "marca": "riskmann"})
    return {"laminas": len(c["laminas"]), "videos": len(r["videos"]), "minutos": round(r["segundos"] / 60),
            "frases": r["frases"], "preguntas": r["preguntas"], "palabras": r["palabras"]}


# ── Leer y guardar ──────────────────────────────────────────────────────────

def ruta_trabajo(id_: str) -> Path | None:
    if not re.fullmatch(r"[a-z0-9-]+", id_ or ""):
        return None
    ruta = _raiz() / id_ / "trabajo.json"
    return ruta if ruta.exists() else None


def cargar(id_: str) -> dict | None:
    ruta = ruta_trabajo(id_)
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta else None


def guardar(t: dict) -> None:
    ruta = _raiz() / t["id"] / "trabajo.json"
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(ruta)


def eliminar(id_: str) -> None:
    """Borra la carpeta del trabajo (su PPTX incluido). Solo ids que existen y pasan la validación."""
    ruta = ruta_trabajo(id_)
    if ruta is None:
        raise KeyError(id_)
    shutil.rmtree(ruta.parent)


def lista() -> list[dict]:
    if not _raiz().exists():
        return []
    salida = []
    for r in _raiz().glob("*/trabajo.json"):
        t = json.loads(r.read_text(encoding="utf-8"))
        salida.append({k: t[k] for k in ("id", "nombre", "creado", "origen", "marca", "voz")} |
                      {"videos": len(t["videos"]), "laminas": len(t["laminas"]),
                       "segundos": resumen(t)["segundos"]})
    return sorted(salida, key=lambda t: t["creado"], reverse=True)


def reagrupar(t: dict) -> dict:
    """Vuelve a proponer los videos a partir de las láminas (p. ej. tras mejorar el extractor)."""
    if t["origen"]["tipo"] != "pptx":
        raise ValueError("Los videos de este curso vienen de su producción real: no se vuelven a proponer")
    t["videos"] = extractor.agrupar(t["laminas"])
    guardar(t)
    return t


def ajustar(t: dict, marca: str, voz: str, formatos: list[str]) -> dict:
    if marca not in datos.marcas():
        raise ValueError("Marca desconocida")
    if voz not in {v["id"] for v in voces()}:
        raise ValueError("Voz desconocida")
    formatos = [f for f in formatos if f in FORMATOS]
    if not formatos:
        raise ValueError("Elige al menos un formato")
    t.update(marca=marca, voz=voz, formatos=formatos)
    guardar(t)
    return t


# ── Lo que sale ──────────────────────────────────────────────────────────────

def resumen(t: dict) -> dict:
    """Todo lo calculado sobre el trabajo: guion por video, duraciones y verificación."""
    por_n = {l["n"]: l for l in t["laminas"]}
    videos = []
    for v in t["videos"]:
        ls = [por_n[n] for n in v["laminas"] if n in por_n]
        dur = sum(extractor.segundos(l["notas"]) for l in ls)
        videos.append({**v, "laminas_detalle": ls, "segundos": round(dur),
                       "frases": sum(len(l["frases"]) for l in ls)})

    en_video = {n for v in t["videos"] for n in v["laminas"]}
    excluidas = t.get("excluidas", {})
    sin_uso = [l for l in t["laminas"] if l["n"] not in en_video and str(l["n"]) not in excluidas]
    sin_notas = [l for l in t["laminas"] if l["n"] in en_video and not l["notas"].strip()]
    normativas = [
        {"lamina": l["n"], "citas": extractor.afirmaciones_normativas(l["notas"])}
        for l in t["laminas"] if l["n"] in en_video and extractor.afirmaciones_normativas(l["notas"])
    ]
    largos = [v for v in videos if v["segundos"] > 240]
    marca = datos.marcas().get(t["marca"], {})
    avisos_marca = [p["texto"] for p in marca.get("pendientes", [])
                    if not p["hecho"] and re.search(r"licencia|voz|umbral", p["texto"], re.I)]

    frases_total = sum(v["frases"] for v in videos)
    chequeos = [
        {"ok": True, "titulo": "Cada frase del guion dice de qué lámina sale",
         "detalle": f"{frases_total} frases trazadas a su lámina y a las notas del orador"},
        {"ok": not sin_notas, "titulo": "Todas las láminas del video tienen narración",
         "detalle": ", ".join(f"lámina {l['n']}" for l in sin_notas) or "Ninguna lámina queda muda"},
        {"ok": not sin_uso, "titulo": "Ninguna lámina se queda fuera sin motivo",
         "detalle": ", ".join(f"lámina {l['n']}" for l in sin_uso) or
                    (f"{len(excluidas)} excluidas con su motivo" if excluidas else "Todas entran a un video")},
        {"ok": not largos, "titulo": "Ningún video pasa de 4 minutos",
         "detalle": ", ".join(v["titulo"] for v in largos) or "Todos dentro del rango"},
        {"ok": None if normativas else True, "titulo": "Cifras y normas para revisar contra su fuente",
         "detalle": f"{sum(len(x['citas']) for x in normativas)} citas en {len(normativas)} láminas"
                    if normativas else "El guion no cita normas ni cifras"},
        {"ok": None if avisos_marca else True, "titulo": f"Pendientes de la marca {marca.get('nombre_corto', '')}",
         "detalle": "; ".join(avisos_marca) or "Sin pendientes que afecten la producción"},
    ]
    return {
        "videos": videos,
        "segundos": sum(v["segundos"] for v in videos),
        "frases": frases_total,
        "palabras": sum(len(l["notas"].split()) for l in t["laminas"] if l["n"] in en_video),
        "normativas": normativas,
        "chequeos": chequeos,
        "preguntas": sum(len(g["preguntas"]) for g in (t.get("banco") or {}).get("grupos", [])),
        "sin_uso": sin_uso,
    }


def curso_json(t: dict) -> list[dict]:
    """El curso.json en el formato de csm/moto: lo que recibe el generador de plantillas."""
    campos = ("n", "formas", "notas", "frases", "foto", "icono")
    return [{k: l.get(k) for k in campos} for l in t["laminas"]]


def orden_produccion(t: dict) -> dict:
    """El contrato con el motor (fase 1): qué producir, con qué marca, voz y formatos."""
    marca = datos.marcas()[t["marca"]]
    voz = next(v for v in voces() if v["id"] == t["voz"])
    r = resumen(t)
    return {
        "version": 1,
        "trabajo": t["id"],
        "nombre": t["nombre"],
        "entrada": t["origen"],
        "marca": {k: marca.get(k) for k in ("id", "nombre", "paleta", "tipografia", "logo", "cta")},
        "voz": {k: voz.get(k) for k in ("id", "nombre", "proveedor", "voice_id", "modelo", "ajustes")},
        "formatos": t["formatos"],
        "videos": [{"clave": v["clave"], "titulo": v["titulo"], "laminas": v["laminas"],
                    "segundos_estimados": v["segundos"]} for v in r["videos"]],
        "excluidas": t.get("excluidas", {}),
        "verificacion": r["chequeos"],
        "curso_json": "curso.json",
    }
