"""PPTX → la geometría de cada lámina: dónde está cada forma y cómo se ve.

`app/extractor.py` lee **lo que dice** una lámina (sus textos, sus notas, sus tablas) y tira
todo lo demás. Sirve para armar una escena nueva con la plantilla de la marca, pero no para
*animar la diapositiva*: para eso hace falta saber dónde está cada cosa.

Este módulo lee **cómo se ve**: posición, tamaño, giro, relleno, borde, y el texto con sus
tipografías, tamaños y colores, forma por forma y en orden de pintado. Con eso
`motor/escenas/lamina.py` redibuja la lámina en HTML tal como está en PowerPoint y anima cada
forma por separado.

Las coordenadas salen **normalizadas** (0..1 sobre el ancho y el alto de la lámina), no en
píxeles: así la misma disposición sirve para 1920×1080, para 9:16 o para lo que venga. Los
tamaños de letra salen en puntos sobre una lámina de 7,5 pulgadas de alto, que es la medida con
la que PowerPoint los guarda; `lamina.py` los convierte al lienzo que toque.

Lo que **no** se replica (y el control de calidad avisa): degradados de varias paradas, sombras,
WordArt, SmartArt vivo (se lee como el grupo de formas que es) y los efectos 3-D. El resto
—cajas, textos, imágenes, líneas, tablas— se reconstruye fiel.
"""

import re
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN

# PowerPoint guarda los tamaños de letra pensando en una lámina de 7,5 pulgadas de alto.
# Es la referencia para pasar puntos a píxeles sea cual sea el lienzo.
ALTO_REFERENCIA_PULGADAS = 7.5
EMU_POR_PULGADA = 914400

_ALINEACION = {
    PP_ALIGN.LEFT: "left", PP_ALIGN.CENTER: "center", PP_ALIGN.RIGHT: "right",
    PP_ALIGN.JUSTIFY: "justify", PP_ALIGN.JUSTIFY_LOW: "justify", PP_ALIGN.DISTRIBUTE: "justify",
}
_ANCLA = {1: "flex-start", 2: "center", 3: "flex-end"}  # MSO_ANCHOR: TOP, MIDDLE, BOTTOM

# Las formas cuyo nombre empieza así no se animan por separado: son el fondo de la lámina.
# Entran de una con la escena para que nunca se vea el lienzo vacío.
FONDO = ("fondo", "background", "bg-", "cover-field", "field", "banda", "band", "hero")

# El marco de la lámina: lo que la enmarca y no es una idea que la voz vaya desarrollando.
# Entra con el fondo, igual que en una diapositiva de verdad ya está ahí cuando empiezas a hablar.
MARCO = ("title", "titulo", "título", "cover-title", "cover-kicker", "kicker", "section", "seccion",
         "sección", "page", "pagina", "página", "header", "footer", "pie", "logo", "marca")


def _color(objeto) -> str | None:
    """El color de un relleno o una letra, en `#rrggbb`. None si hereda del tema o no tiene."""
    if objeto is None:
        return None
    try:
        if objeto.type is None:
            return None
        rgb = objeto.rgb  # lanza si es un color de tema sin resolver
    except (AttributeError, ValueError, TypeError):
        return None
    return f"#{rgb}".lower()


def _relleno(forma) -> str | None:
    f = getattr(forma, "fill", None)
    if f is None:
        return None
    try:
        if f.type != 1:  # solo sólido: MSO_FILL.SOLID
            return None
        return _color(f.fore_color)
    except (AttributeError, ValueError, TypeError):
        return None


def _borde(forma) -> dict | None:
    linea = getattr(forma, "line", None)
    if linea is None:
        return None
    try:
        color, grosor = _color(linea.color), linea.width
    except (AttributeError, ValueError, TypeError):
        return None
    if not color or not grosor:
        return None
    return {"color": color, "grosor_pt": round(grosor / 12700, 2)}


def _runs(parrafo) -> list[dict]:
    salida = []
    for r in parrafo.runs:
        if not r.text:
            continue
        f = r.font
        salida.append({
            "texto": r.text,
            "fuente": f.name,
            "pt": round(f.size.pt, 2) if f.size is not None else None,
            "negrita": bool(f.bold),
            "cursiva": bool(f.italic),
            "subrayado": bool(f.underline),
            "color": _color(f.color),
        })
    return salida


def _parrafos(forma) -> list[dict]:
    if not forma.has_text_frame:
        return []
    salida = []
    for p in forma.text_frame.paragraphs:
        runs = _runs(p)
        if not runs:
            # Un párrafo vacío es un espacio en blanco intencional: se conserva su altura.
            salida.append({"runs": [], "alineacion": None, "nivel": p.level, "vacio": True})
            continue
        salida.append({
            "runs": runs,
            "alineacion": _ALINEACION.get(p.alignment),
            "nivel": p.level,
            "vacio": False,
            # `line_spacing` es un múltiplo (1,5) o una medida (Pt): solo sirve el múltiplo.
            "interlineado": p.line_spacing if isinstance(p.line_spacing, (int, float)) else None,
        })
    return salida


def _nombre_imagen(lamina, forma) -> str:
    """El mismo nombre que usa `extractor.guardar_imagenes`, para reusar las imágenes ya copiadas."""
    try:
        return Path(str(lamina.part.related_part(forma._element.blip_rId).partname)).name
    except Exception:
        return f"imagen.{forma.image.ext}"


def _tabla(forma) -> dict:
    t = forma.table
    filas = []
    for fila in t.rows:
        filas.append([{"texto": c.text.strip(), "relleno": _relleno(c), "parrafos": _parrafos(c)}
                      for c in fila.cells])
    return {"filas": filas,
            "anchos": [c.width for c in t.columns],
            "altos": [f.height for f in t.rows]}


def _marco(forma) -> dict:
    """Los márgenes internos y el anclaje vertical de un cuadro de texto."""
    if not forma.has_text_frame:
        return {}
    tf = forma.text_frame
    pt = lambda v: round(v / 12700, 2) if v is not None else None  # noqa: E731
    return {
        "margenes_pt": [pt(tf.margin_top), pt(tf.margin_right), pt(tf.margin_bottom), pt(tf.margin_left)],
        "ancla": _ANCLA.get(tf.vertical_anchor, "flex-start"),
        "ajustar_texto": bool(tf.word_wrap) if tf.word_wrap is not None else True,
    }


def _transformar(x, y, cx, cy, t):
    """Lleva la caja de una forma del sistema de su grupo al de la lámina."""
    if t is None:
        return x, y, cx, cy
    ox, oy, ex, ey, gx, gy, gw, gh = t
    kx = gw / ex if ex else 1
    ky = gh / ey if ey else 1
    return gx + (x - ox) * kx, gy + (y - oy) * ky, cx * kx, cy * ky


def _transformacion_grupo(grupo, t):
    """El sistema de coordenadas de los hijos de un grupo, ya compuesto con el de sus padres."""
    xfrm = grupo._element.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")
    if xfrm is None:
        return t
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    off, ext = xfrm.find(f"{ns}chOff"), xfrm.find(f"{ns}chExt")
    if off is None or ext is None:
        return t
    gx, gy, gw, gh = _transformar(grupo.left or 0, grupo.top or 0, grupo.width or 0, grupo.height or 0, t)
    return (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")), gx, gy, gw, gh)


def _es_fondo(nombre: str, x: float, y: float, w: float, h: float) -> bool:
    """Una forma es fondo si lo dice su nombre o si cubre casi toda la lámina."""
    return nombre.lower().startswith(FONDO) or (w >= 0.92 and h >= 0.92 and x <= 0.04 and y <= 0.04)


def _es_marco(nombre: str) -> bool:
    return nombre.lower().startswith(MARCO)


def _fondo_lamina(lamina) -> str | None:
    """El color de fondo de la lámina: el suyo, el de su diseño o el del patrón.

    No es una forma: PowerPoint lo hereda por capas, así que hay que ir a buscarlo. Sin esto,
    una lámina cuyo fondo viene del patrón sale del color del lienzo y se ve todo mal.
    """
    for origen in (lamina, lamina.slide_layout, lamina.slide_layout.slide_master):
        try:
            fondo = origen.background
            if fondo.fill.type == 1:  # sólido
                c = _color(fondo.fill.fore_color)
                if c:
                    return c
        except (AttributeError, ValueError, TypeError, NotImplementedError):
            continue
    return None


def _forma(lamina, sh, ancho: int, alto: int, z: int, t) -> dict | None:
    x, y, cx, cy = _transformar(sh.left or 0, sh.top or 0, sh.width or 0, sh.height or 0, t)
    caja = {"x": x / ancho, "y": y / alto, "w": cx / ancho, "h": cy / alto}
    if caja["w"] <= 0 and caja["h"] <= 0:
        return None

    tipo = "figura"
    extra: dict = {}
    if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
        tipo, extra = "imagen", {"archivo": _nombre_imagen(lamina, sh)}
    elif getattr(sh, "has_table", False) and sh.has_table:
        tipo, extra = "tabla", {"tabla": _tabla(sh)}
    elif getattr(sh, "has_chart", False) and sh.has_chart:
        tipo = "grafico"

    parrafos = _parrafos(sh)
    texto = "\n".join(r["texto"] for p in parrafos for r in p["runs"])
    if tipo == "figura" and texto.strip():
        tipo = "texto"
    elif tipo == "figura" and caja["h"] <= 0.002:
        # Una caja sin alto es una línea: se dibuja con su borde (o su relleno si no tiene).
        tipo = "linea"

    nombre = sh.name or f"forma{z}"
    return {
        "id": re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-") or f"forma{z}",
        "nombre": nombre,
        "tipo": tipo,
        "z": z,
        **caja,
        "giro": round(sh.rotation, 2) if getattr(sh, "rotation", 0) else 0,
        "relleno": _relleno(sh),
        "borde": _borde(sh),
        "parrafos": parrafos,
        "texto": texto,
        "marco": _marco(sh),
        "fondo": _es_fondo(nombre, caja["x"], caja["y"], caja["w"], caja["h"]),
        "es_marco": _es_marco(nombre),
        **extra,
    }


def _recorrer(lamina, shapes, ancho, alto, z, t, salida):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            z = _recorrer(lamina, sh.shapes, ancho, alto, z, _transformacion_grupo(sh, t), salida)
            continue
        f = _forma(lamina, sh, ancho, alto, z, t)
        if f is not None:
            salida.append(f)
            z += 1
    return z


def leer(ruta) -> dict:
    """La disposición de todas las láminas de un PPTX (una ruta o un archivo abierto).

    Devuelve `{"ancho": EMU, "alto": EMU, "proporcion": 1.777…, "laminas": [{n, formas: [...]}]}`.
    Cada forma trae su caja normalizada (0..1), su z y cómo se ve. Ver el encabezado del módulo.
    """
    pres = Presentation(str(ruta) if isinstance(ruta, (str, Path)) else ruta)
    ancho, alto = pres.slide_width, pres.slide_height
    laminas = []
    for n, lamina in enumerate(pres.slides, start=1):
        formas: list[dict] = []
        _recorrer(lamina, lamina.shapes, ancho, alto, 0, None, formas)
        laminas.append({"n": n, "formas": formas, "disposicion": lamina.slide_layout.name,
                        "fondo": _fondo_lamina(lamina)})
    return {
        "ancho": ancho,
        "alto": alto,
        "proporcion": round(ancho / alto, 4),
        "escala_pt": (alto / EMU_POR_PULGADA) / ALTO_REFERENCIA_PULGADAS,
        "laminas": laminas,
    }
