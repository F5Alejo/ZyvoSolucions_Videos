"""Empresas registradas desde el estudio.

Cualquier empresa se registra sola: nombre, logo, colores y voz. Se guardan en
`datos/empresas/<id>.json` con su logo en `datos/empresas/logos/`, fuera de git (son datos
de clientes). Las marcas de siempre (`datos/marcas/`) no se tocan: esas son de solo lectura.

El logo nunca se guarda como llegó: se abre, se reduce y se vuelve a codificar en PNG, así que
lo que sirve el estudio es siempre una imagen limpia.
"""

import io
import json
import re
import unicodedata
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app import datos

MAX_LOGO = 5 * 1024 * 1024
LADO_LOGO = 1200
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
NOMBRES_COLOR = ["principal", "acento", "complementario", "apoyo", "detalle", "extra"]


def carpeta() -> Path:
    return datos.RAIZ_DATOS / "empresas"


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "empresa"


def es_registrada(id_: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9-]+", id_ or "")) and (carpeta() / f"{id_}.json").exists()


# ── Logo ─────────────────────────────────────────────────────────────────────

def _abrir_logo(contenido: bytes) -> Image.Image:
    if len(contenido) > MAX_LOGO:
        raise ValueError("El logo pesa más de 5 MB")
    try:
        im = Image.open(io.BytesIO(contenido))
        im.load()
    except (UnidentifiedImageError, OSError):
        raise ValueError("El logo tiene que ser una imagen PNG, JPG o WebP")
    if im.format not in ("PNG", "JPEG", "WEBP"):
        raise ValueError("El logo tiene que ser una imagen PNG, JPG o WebP")
    im = im.convert("RGBA")
    im.thumbnail((LADO_LOGO, LADO_LOGO))
    return im


def colores_de_logo(contenido: bytes, cuantos: int = 5) -> list[str]:
    """Los colores con más presencia en el logo, sin el fondo blanco ni lo transparente."""
    im = _abrir_logo(contenido)
    im.thumbnail((160, 160))
    pixeles = [(r, g, b) for r, g, b, a in im.getdata() if a > 200]
    if not pixeles:
        return []
    tira = Image.new("RGB", (len(pixeles), 1))
    tira.putdata(pixeles)
    reducida = tira.quantize(colors=12, method=Image.Quantize.MEDIANCUT).convert("RGB")
    conteo = Counter(reducida.getdata())
    elegidos: list[tuple[int, int, int]] = []
    for c, _ in conteo.most_common():
        casi_blanco = min(c) > 235
        parecido = any(sum((x - y) ** 2 for x, y in zip(c, e)) < 45 ** 2 for e in elegidos)
        if not casi_blanco and not parecido:
            elegidos.append(c)
        if len(elegidos) == cuantos:
            break
    return ["#%02X%02X%02X" % c for c in elegidos]


def _fondo_para(im: Image.Image) -> str:
    """«oscuro» si el logo es claro (necesita fondo oscuro para verse); si no, «claro»."""
    pix = [(r, g, b) for r, g, b, a in im.getdata() if a > 200]
    if not pix:
        return "claro"
    lum = sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in pix) / len(pix) / 255
    return "oscuro" if lum > 0.72 else "claro"


def _guardar_logo(id_: str, contenido: bytes) -> dict:
    im = _abrir_logo(contenido)
    destino = carpeta() / "logos"
    destino.mkdir(parents=True, exist_ok=True)
    nombre = f"{id_}.png"
    im.save(destino / nombre, "PNG", optimize=True)
    return {"archivo_local": nombre, "fondo": _fondo_para(im)}


def ruta_logo(nombre: str) -> Path | None:
    """El archivo de un logo registrado, solo si está dentro de la carpeta de logos."""
    raiz = (carpeta() / "logos").resolve()
    ruta = (raiz / nombre).resolve()
    return ruta if ruta.is_relative_to(raiz) and ruta.is_file() and ruta.suffix == ".png" else None


# ── Datos ────────────────────────────────────────────────────────────────────

def _limpiar(campos: dict) -> dict:
    """Valida lo que escribió la persona y lo deja listo para guardar."""
    nombre = (campos.get("nombre") or "").strip()
    if len(nombre) < 2:
        raise ValueError("Escribe el nombre de la empresa")
    if len(nombre) > 80:
        raise ValueError("El nombre de la empresa es demasiado largo (máximo 80 caracteres)")
    corto = (campos.get("nombre_corto") or "").strip() or nombre
    if len(corto) > 24:
        raise ValueError("El nombre corto es demasiado largo (máximo 24 caracteres)")
    colores = [c.strip().upper() for c in campos.get("colores") or [] if c and c.strip()]
    if not colores:
        raise ValueError("Elige al menos un color: el principal de la empresa")
    if len(colores) > 6:
        raise ValueError("Elige como máximo 6 colores")
    malos = [c for c in colores if not HEX.match(c)]
    if malos:
        raise ValueError(f"Este color no es válido: {malos[0]}. Usa el formato #RRGGBB")
    sitio = (campos.get("sitio_web") or "").strip().removeprefix("https://").removeprefix("http://").rstrip("/")
    if sitio and not re.fullmatch(r"[\w.-]+\.[a-zA-Z]{2,}(/[\w./-]*)?", sitio):
        raise ValueError("El sitio web no parece válido. Ejemplo: miempresa.com")
    voz_id = (campos.get("voz") or "").strip()
    voces = {v["id"]: v for v in json.loads((datos.RAIZ_DATOS / "voces.json").read_text(encoding="utf-8"))}
    if voz_id and voz_id not in voces:
        raise ValueError("Esa voz no existe")

    def texto(clave: str, maximo: int) -> str | None:
        v = (campos.get(clave) or "").strip()
        if len(v) > maximo:
            raise ValueError(f"El campo «{clave.replace('_', ' ')}» es demasiado largo (máximo {maximo} caracteres)")
        return v or None

    return {
        "nombre": nombre,
        "nombre_corto": corto,
        "que_es": texto("que_es", 200) or "Empresa registrada en el estudio",
        "dominio": sitio or None,
        "responsable": texto("responsable", 80),
        "tipografia": texto("tipografia", 80) or "Montserrat",
        "voz_id": voz_id or None,
        "voz": voces[voz_id]["nombre"] if voz_id else "Por elegir en cada curso",
        "cta": texto("cta", 160),
        "paleta": [{"hex": c, "nombre": NOMBRES_COLOR[i]} for i, c in enumerate(colores)],
    }


def _guardar(m: dict) -> None:
    carpeta().mkdir(parents=True, exist_ok=True)
    ruta = carpeta() / f"{m['id']}.json"
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(ruta)


def registrar(campos: dict, logo: bytes | None = None) -> dict:
    base = _limpiar(campos)
    existentes = set(datos.marcas())
    id_ = _slug(base["nombre_corto"])
    if id_ in existentes:
        n = 2
        while f"{id_}-{n}" in existentes:
            n += 1
        id_ = f"{id_}-{n}"
    m = {
        "id": id_,
        **base,
        "registrada": True,
        "creada": datetime.now().isoformat(timespec="seconds"),
        "revisada": date.today().isoformat(),
        "fuente_ficha": "Registrada en el estudio",
        "paleta_fuente": "Elegida al registrar la empresa",
        "contradicciones": [],
        "fuentes": [{"fuente": "Registro en el estudio", "tipo": "formulario", "donde": "Datos que dio la empresa al registrarse"}],
        "pendientes": [],
        "pedir_al_cliente": [],
    }
    if logo:
        m["logo"] = _guardar_logo(id_, logo)
    _guardar(m)
    return m


def actualizar(id_: str, campos: dict, logo: bytes | None = None) -> dict:
    if not es_registrada(id_):
        raise KeyError(id_)
    m = json.loads((carpeta() / f"{id_}.json").read_text(encoding="utf-8"))
    m.update(_limpiar(campos))
    if logo:
        m["logo"] = _guardar_logo(id_, logo)
    m["revisada"] = date.today().isoformat()
    _guardar(m)
    return m


def en_uso(id_: str) -> list[str]:
    """Dónde se usa la empresa: cursos del estudio y videos del catálogo."""
    from app import taller  # aquí para no crear una importación circular
    usos = [f"curso «{t['nombre']}»" for t in taller.lista() if t["marca"] == id_]
    usos += [f"video «{p.get('titulo', p['id'])}»" for p in datos.proyectos() if p["marca"] == id_]
    return usos


def eliminar(id_: str) -> None:
    if not es_registrada(id_):
        raise KeyError(id_)
    usos = en_uso(id_)
    if usos:
        raise ValueError(f"No se puede eliminar: la usa{'n' if len(usos) > 1 else ''} {', '.join(usos[:3])}"
                         + (f" y {len(usos) - 3} más" if len(usos) > 3 else ""))
    (carpeta() / f"{id_}.json").unlink()
    logo = carpeta() / "logos" / f"{id_}.png"
    if logo.exists():
        logo.unlink()
