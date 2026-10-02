"""Agentes de la entrega: Evaluador (preguntas por video) y Publicador (textos para publicar)."""

from app import configuracion, datos, taller
from motor.agentes.base import Agente, Contexto, en_videos, registrar
from motor.agentes.guardas import inventado
from motor.agentes.textos import SISTEMA

# ── Evaluador ────────────────────────────────────────────────────────────────

ESQUEMA_PREGUNTAS = {"type": "object", "properties": {"preguntas": {"type": "array", "minItems": 3, "maxItems": 5, "items": {
    "type": "object", "properties": {
        "enunciado": {"type": "string"}, "correcta": {"type": "string"},
        "distractores": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 2},
        "lamina": {"type": "integer"}},
    "required": ["enunciado", "correcta", "distractores", "lamina"]}}}, "required": ["preguntas"]}


def _evaluador(t: dict, ctx: Contexto) -> list[dict]:
    por_video: dict[str, list[dict]] = {}
    for video, l, _ in en_videos(t):
        por_video.setdefault(video["clave"], []).append(l)
    salida = []
    videos = [v for v in t["videos"] if por_video.get(v["clave"])]
    for k, v in enumerate(videos):
        ctx.avisar(f"Video {k + 1} de {len(videos)}: {v['titulo']}", k / len(videos))
        laminas = por_video[v["clave"]]
        contenido = "\n".join(f"Lámina {l['n']}: {l['notas']}" for l in laminas if l["notas"].strip())
        if not contenido:
            continue
        r = ctx.chat(SISTEMA + " Escribes evaluaciones de opción múltiple para cursos de formación.",
                     "Escribe de 3 a 5 preguntas de opción múltiple sobre este contenido. Cada una con la respuesta "
                     "correcta, 2 distractores creíbles pero claramente incorrectos, y el número de la lámina de la que "
                     f"sale. Solo sobre lo que dice el contenido.\n\n{contenido[:4000]}", ESQUEMA_PREGUNTAS)
        if r is None:
            continue
        numeros = {l["n"] for l in laminas}
        preguntas = []
        for p in r.get("preguntas", []):
            if p.get("lamina") not in numeros or len(p.get("distractores", [])) != 2:
                continue
            if inventado(f"{p['enunciado']} {p['correcta']}", contenido):
                continue  # la respuesta correcta no puede traer cifras que no dijo el curso
            preguntas.append({"enunciado": p["enunciado"].strip(), "correcta": p["correcta"].strip(),
                              "distractores": [d.strip() for d in p["distractores"]], "fuente": f"Lámina {p['lamina']}"})
        if preguntas:
            salida.append({"lamina": None, "video": v["clave"], "titulo": f"Preguntas: {v['titulo']}",
                           "antes": None, "despues": {"clave": f"ia-{v['clave']}", "titulo": v["titulo"],
                                                      "tema": "Propuestas por el Evaluador", "preguntas": preguntas},
                           "razon": f"{len(preguntas)} preguntas, cada una con la lámina de la que sale", "con_ia": True})
    return salida


def _aplicar_preguntas(t: dict, p: dict) -> None:
    banco = t.get("banco") or {"nombre": t["nombre"], "grupos": []}
    banco["grupos"] = [g for g in banco["grupos"] if g["clave"] != p["despues"]["clave"]] + [p["despues"]]
    t["banco"] = banco


registrar(Agente("evaluador", "Evaluador", "Preguntas de opción múltiple por video, exportables a Moodle",
                 "resultado", "texto", _evaluador, _aplicar_preguntas, necesita_ia=True))


# ── Exportar el banco (sin IA) ───────────────────────────────────────────────

def _gift_escapar(texto: str) -> str:
    for c in "\\~=#{}:":
        texto = texto.replace(c, "\\" + c)
    return texto


def a_gift(banco: dict) -> str:
    """Formato GIFT de Moodle: se importa en Banco de preguntas → Importar → GIFT."""
    lineas = []
    for g in banco.get("grupos", []):
        lineas.append(f"$CATEGORY: {_gift_escapar(g['titulo'])}\n")
        for i, p in enumerate(g["preguntas"], start=1):
            opciones = [f"={_gift_escapar(p['correcta'])}"] + [f"~{_gift_escapar(d)}" for d in p["distractores"]]
            lineas.append(f"::{_gift_escapar(g['clave'])}-{i}::{_gift_escapar(p['enunciado'])} "
                          f"{{\n  " + "\n  ".join(opciones) + f"\n}}\n// Fuente: {p.get('fuente', '')}\n")
    return "\n".join(lineas)


def a_moodle_xml(banco: dict) -> str:
    """Formato Moodle XML (también lo leen otros LMS)."""
    from xml.sax.saxutils import escape
    partes = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    for g in banco.get("grupos", []):
        partes.append(f'<question type="category"><category><text>$course$/{escape(g["titulo"])}</text></category></question>')
        for i, p in enumerate(g["preguntas"], start=1):
            respuestas = [f'<answer fraction="100"><text>{escape(p["correcta"])}</text></answer>']
            respuestas += [f'<answer fraction="0"><text>{escape(d)}</text></answer>' for d in p["distractores"]]
            partes.append(
                f'<question type="multichoice"><name><text>{escape(g["clave"])}-{i}</text></name>'
                f'<questiontext format="plain_text"><text>{escape(p["enunciado"])}</text></questiontext>'
                f'<generalfeedback><text>Fuente: {escape(p.get("fuente", ""))}</text></generalfeedback>'
                f"<single>true</single><shuffleanswers>1</shuffleanswers>{''.join(respuestas)}</question>")
    partes.append("</quiz>")
    return "\n".join(partes)


# ── Publicador ───────────────────────────────────────────────────────────────

ESQUEMA_PUBLICAR = {"type": "object", "properties": {
    "titulo": {"type": "string"}, "descripcion": {"type": "string"},
    "etiquetas": {"type": "array", "items": {"type": "string"}, "maxItems": 12},
    "historias": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 3}},
    "required": ["titulo", "descripcion", "etiquetas", "historias"]}


def capitulos(t: dict) -> str:
    """Los capítulos del curso completo («0:00 Título»): los reales si ya se armó, si no estimados."""
    ruta = taller.ruta_trabajo(t["id"]).parent / "salida" / "completo" / "capitulos.txt"
    if ruta.exists():
        return ruta.read_text(encoding="utf-8").strip()
    conf = configuracion.leer()["completo"]
    tarjeta = conf["duracion_tarjeta"] if conf["tarjetas"] else 0
    lineas, t0 = [], 0.0
    for v in taller.resumen(t)["videos"]:
        s = int(t0)
        lineas.append(f"{s // 60}:{s % 60:02d} {v['titulo']}")
        t0 += tarjeta + v["segundos"]
    return "\n".join(lineas)


def _publicador(t: dict, ctx: Contexto) -> list[dict]:
    marca = datos.marcas().get(t["marca"], {})
    caps = capitulos(t)
    ctx.avisar("Escribiendo los textos para publicar", 0.3)
    temas = "\n".join(f"- {v['titulo']}" for v in t["videos"])
    r = ctx.chat(SISTEMA + " Escribes textos para publicar videos de formación en YouTube y redes.",
                 f"Curso: {t['nombre']}\nMarca: {marca.get('nombre', '')} ({marca.get('que_es', '')})\n"
                 f"Llamado a la acción de la marca: {marca.get('cta') or 'ninguno'}\nVideos:\n{temas}\n\n"
                 "Escribe: un título para YouTube (máximo 70 caracteres), una descripción de 2 párrafos cortos, "
                 "hasta 12 etiquetas y 3 textos para historias de Instagram o WhatsApp (máximo 120 caracteres cada uno, "
                 "con un gancho al principio).", ESQUEMA_PUBLICAR)
    con_ia = r is not None
    if r is None:
        r = {"titulo": t["nombre"][:70],
             "descripcion": f"Curso «{t['nombre']}» de {marca.get('nombre', '')}.\n\nEn este curso:\n{temas}",
             "etiquetas": [marca.get("nombre_corto", ""), "formación", "capacitación"] + [v["titulo"] for v in t["videos"][:5]],
             "historias": [f"{v['titulo']}: míralo completo en el curso." for v in t["videos"][:3]]}
    texto = f"{r['titulo']}\n{r['descripcion']}\n" + "\n".join(r["historias"])
    fuente = "\n".join([t["nombre"], marca.get("cta") or "", temas, *(l["notas"] for _, l, _ in en_videos(t))])
    if inventado(texto, fuente):
        r["descripcion"] += "\n\n⚠ Revisa las cifras: no todas salen del curso."
    despues = {"titulo": r["titulo"][:100], "descripcion": r["descripcion"].strip() + "\n\nCapítulos:\n" + caps,
               "etiquetas": [e.strip() for e in r["etiquetas"] if e.strip()][:12],
               "historias": [h.strip()[:160] for h in r["historias"]][:3]}
    return [{"lamina": None, "video": None, "titulo": "Textos para publicar", "antes": t.get("publicacion"),
             "despues": despues, "con_ia": con_ia,
             "razon": "Título, descripción con capítulos, etiquetas e historias" + ("" if con_ia else " (plantilla sin IA)")}]


def _aplicar_publicacion(t: dict, p: dict) -> None:
    t["publicacion"] = p["despues"]


def publicacion_md(pub: dict) -> str:
    return (f"# {pub['titulo']}\n\n{pub['descripcion']}\n\n## Etiquetas\n\n{', '.join(pub['etiquetas'])}\n\n"
            "## Historias\n\n" + "\n".join(f"- {h}" for h in pub["historias"]) + "\n")


registrar(Agente("publicador", "Publicador", "Título, descripción con capítulos, etiquetas e historias",
                 "resultado", "texto", _publicador, _aplicar_publicacion))

