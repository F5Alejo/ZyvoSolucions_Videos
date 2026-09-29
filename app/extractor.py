"""PPTX → `curso.json`: lo que entra al motor.

Produce el mismo formato que `videos/csm-curso/datos/curso.json`: por lámina, sus formas
con nombre (texto por párrafo), las notas del orador, las frases de la narración y las
imágenes. Es la tarea 0.1 de PLATAFORMA.md: el extractor que no estaba en ninguna rama.
"""

import re
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

# Velocidad medida en el curso csm: 4 571 palabras locutadas en 1 909 s por Carlos
# (eleven_v3), 41 láminas (`csm-curso/datos/tiempos-voz.json`).
PALABRAS_POR_SEGUNDO = 2.394
# Lo que csm.py añade a cada lámina: el título entra 1,0 s antes y 1,3 s de respiro al final.
RELLENO_POR_LAMINA = 2.3

# Afirmaciones que en contenido normativo necesitan su fuente a la vista (PLATAFORMA §3.4).
_NORMATIVO = re.compile(
    r"\b(?:Ley|Decreto|Resoluci[oó]n|Circular|Art[ií]culo|Art\.)\s+(?:No\.?\s*)?\d[\d\.]*(?:\s+de\s+\d{4})?"
    r"|\d+(?:[\.,]\d+)?\s?%"
    r"|\d[\d\.]*\s+SMMLV"
    r"|\d[\d\.,]*\s+(?:metros?|kil[oó]metros(?:\s+por\s+hora)?|km/h|segundos|minutos|horas|años|veh[ií]culos|unidades)\b"
    r"|\$\s?\d[\d\.,]*",
    re.IGNORECASE,
)


def frases(texto: str) -> list[str]:
    """Parte la narración igual que csm.py: tras punto, interrogación, exclamación o dos puntos."""
    return [x for x in re.split(r"(?<=[\.\?\!:])\s+", (texto or "").strip()) if x.strip()]


def segundos(texto: str) -> float:
    palabras = len((texto or "").split())
    return round(palabras / PALABRAS_POR_SEGUNDO + (RELLENO_POR_LAMINA if palabras else 0), 1)


def afirmaciones_normativas(texto: str) -> list[str]:
    vistas = []
    for m in _NORMATIVO.finditer(texto or ""):
        cita = m.group(0).strip()
        if cita not in vistas:
            vistas.append(cita)
    return vistas


def _formas(shapes):
    """Recorre las formas, también dentro de grupos."""
    for s in shapes:
        if s.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _formas(s.shapes)
        else:
            yield s


def _nombre_imagen(lamina, forma) -> str:
    """El nombre del archivo en ppt/media/ (p. ej. `image1.jpg`), como en el curso.json de csm."""
    try:
        return Path(str(lamina.part.related_part(forma._element.blip_rId).partname)).name
    except Exception:
        return f"imagen.{forma.image.ext}"


def leer_pptx(ruta: Path) -> list[dict]:
    pres = Presentation(str(ruta))
    laminas = []
    for n, lamina in enumerate(pres.slides, start=1):
        formas, imagenes = {}, []
        for s in _formas(lamina.shapes):
            if s.has_text_frame:
                parrafos = [p.text.strip() for p in s.text_frame.paragraphs if p.text.strip()]
                if parrafos:
                    nombre, i = s.name, 2
                    while nombre in formas:  # dos formas con el mismo nombre: no se pisa ninguna
                        nombre, i = f"{s.name} ({i})", i + 1
                    formas[nombre] = parrafos
            if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
                imagenes.append((s.width * s.height, _nombre_imagen(lamina, s)))

        notas = ""
        if lamina.has_notes_slide:
            notas = lamina.notes_slide.notes_text_frame.text.strip()

        imagenes.sort(reverse=True)
        laminas.append({
            "n": n,
            "formas": formas,
            "notas": notas,
            "frases": frases(notas),
            "foto": imagenes[0][1] if imagenes else None,
            "icono": imagenes[-1][1] if len(imagenes) > 1 else None,
        })
    return laminas


def titulo_lamina(lamina: dict) -> str:
    """El primer texto de la lámina, para nombrarla en pantalla."""
    for parrafos in lamina.get("formas", {}).values():
        if parrafos:
            return parrafos[0][:90]
    return f"Lámina {lamina['n']}"


def agrupar(laminas: list[dict], objetivo: float = 120.0) -> list[dict]:
    """Propuesta de videos: láminas seguidas hasta rondar `objetivo` segundos de narración."""
    grupos, actual, dur = [], [], 0.0
    for l in laminas:
        s = segundos(l["notas"])
        if actual and dur + s > objetivo * 1.25:
            grupos.append(actual)
            actual, dur = [], 0.0
        actual.append(l["n"])
        dur += s
    if actual:
        grupos.append(actual)
    por_n = {l["n"]: l for l in laminas}
    return [
        {"clave": f"v{i:02d}", "titulo": titulo_lamina(por_n[g[0]]), "laminas": g}
        for i, g in enumerate(grupos, start=1)
    ]
