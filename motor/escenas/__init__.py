"""Lámina de `curso.json` → escena HTML con la identidad de la marca.

No se copia la lámina: se rearma con su texto y su imagen sobre una plantilla de marca. Hay
tres tipos en la Fase 1:

- `portada`: la primera lámina de cada video (título grande).
- `imagen`: la lámina trae foto → foto a un lado, título y hasta 3 viñetas al otro.
- `lista`: título y hasta 5 viñetas.

Cómo entra y sale cada elemento lo decide la plantilla de animación (`animacion.py`): el
render dibuja cuadro a cuadro la entrada y la salida, y sostiene lo del medio.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "fuentes" / "Montserrat.ttf"

FORMATOS = {"16:9": (1920, 1080), "9:16": (1080, 1920)}

_entorno = Environment(loader=FileSystemLoader(AQUI), autoescape=select_autoescape(["html"]))


# ── Color ────────────────────────────────────────────────────────────────────

def _rgb(hexa: str) -> tuple[float, float, float]:
    h = hexa.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminancia(hexa: str) -> float:
    def canal(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in _rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a: str, b: str) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def estilo(marca: dict, logo: Path | None = None) -> dict:
    """Los colores de la escena. Si la ficha trae un bloque «video», manda; si no, se deduce de la paleta."""
    v = marca.get("video")
    if v:
        e = {k: v[k] for k in ("fondo", "superficie", "texto", "acento", "acento2")}
    else:
        colores = [p["hex"] for p in marca.get("paleta", []) if len(p.get("hex", "")) == 7]
        fondo = min(colores, key=luminancia) if colores else "#111111"
        texto = "#FFFFFF" if contraste(fondo, "#FFFFFF") >= contraste(fondo, "#111111") else "#111111"
        vivos = [c for c in colores if c != fondo and contraste(c, fondo) >= 3] or [texto]
        e = {"fondo": fondo, "superficie": fondo, "texto": texto, "acento": vivos[0],
             "acento2": vivos[1] if len(vivos) > 1 else vivos[0]}
    e["nombre"] = marca.get("nombre_corto") or marca.get("nombre", "")
    e["logo"] = logo.resolve().as_uri() if logo and logo.exists() else None
    return e


# ── Contenido ────────────────────────────────────────────────────────────────

def _recortar(texto: str, largo: int) -> str:
    return texto if len(texto) <= largo else texto[: largo - 1].rsplit(" ", 1)[0] + "…"


def vista(lamina: dict, indice: int, total: int, video: str, media: Path | None, curso: str = "") -> dict:
    """Lo que se ve de una lámina: tipo de escena, título, viñetas e imagen.

    `video` es el título del video (arriba a la derecha); `curso`, el antetítulo de la portada.
    """
    from app import extractor  # el mismo título que muestra el taller (forma «title» si la hay)

    titulo = extractor.titulo_lamina(lamina) if lamina.get("formas") else video
    seccion = extractor._forma(lamina, extractor._SECCION)
    resto = []
    for ps in lamina.get("formas", {}).values():
        for p in ps:
            p = p.strip()
            if p and p not in resto and not titulo.startswith(p[:90]) and p != seccion:
                resto.append(p)

    pantalla = lamina.get("pantalla") or {}
    if pantalla.get("titulo"):
        titulo = pantalla["titulo"]
    if pantalla.get("vinetas") is not None:
        resto = list(pantalla["vinetas"])
    decorativa = (lamina.get("imagen_info") or {}).get("decorativa")
    foto = media / lamina["foto"] if media and lamina.get("foto") and not decorativa else None
    if foto is not None and not foto.exists():
        foto = None

    if indice == 0:
        tipo = "portada"
    elif foto is not None:
        tipo = "imagen"
    else:
        tipo = "lista"
    maximo = {"portada": 2, "imagen": 3, "lista": 5}[tipo]
    return {
        "tipo": tipo,
        "titulo": _recortar(titulo, 90),
        "vinetas": [_recortar(p, 120) for p in resto[:maximo]],
        "imagen": foto.resolve().as_uri() if foto else None,
        "video": video,
        "antetitulo": curso if curso and curso != titulo else "",
        "indice": indice,
        "total": total,
    }


def html(v: dict, e: dict, formato: str = "16:9", borrador: bool = False,
         plan: dict | None = None, segundos: float = 4.0) -> str:
    """La escena. `plan` es la animación ya resuelta (animacion.plan); sin él, la plantilla por defecto.

    `segundos` es lo que dura la escena: las salidas se ubican contra su final.
    """
    from motor.escenas import animacion

    if plan is None:
        todas = animacion.plantillas()
        plan = {"plantilla": "dinamica", "elementos": todas.get("dinamica", next(iter(todas.values())))["elementos"]}
    reglas, partir = animacion.css(plan, v, segundos, 100 * v["indice"] / v["total"], 100 * (v["indice"] + 1) / v["total"])
    ancho, alto = FORMATOS[formato]
    return _entorno.get_template("escena.html").render(
        v=v, e=e, ancho=ancho, alto=alto, vertical=formato == "9:16", borrador=borrador,
        fuente=FUENTE.resolve().as_uri(), animaciones=reglas, partir=partir)
