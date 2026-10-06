"""El renderer HyperFrames: VideoSpec con sus momentos (motor/direccion.py) → video mudo.

HyperFrames (Apache 2.0, de HeyGen) dibuja una página HTML cuadro a cuadro con Chrome y la pasa
a MP4 con ffmpeg. Aquí se arma **una** composición con todo el video (cada render de HyperFrames
arranca en ~50 s en este equipo, así que no conviene uno por escena) y se renderiza con el CLI
instalado en `motor/hyperframes/node_modules` con versión fija (`package.json`).

Privacidad: la telemetría de HyperFrames va apagada (`HYPERFRAMES_NO_TELEMETRY`) y nunca se usa
su `publish`, que sube el proyecto a su nube. Todo lo que la composición carga (GSAP, la fuente,
las imágenes y los clips) se copia a la carpeta del render: no se descarga nada al renderizar.
"""

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse

from jinja2 import Environment, FileSystemLoader

AQUI = Path(__file__).resolve().parent
CLI = AQUI / "node_modules" / "hyperframes" / "bin" / "hyperframes.mjs"
GSAP = AQUI / "node_modules" / "gsap" / "dist" / "gsap.min.js"
FUENTE = AQUI.parent / "escenas" / "fuentes" / "Montserrat.ttf"
VERSION = 1
BARRIDO = 0.55  # segundos que tarda el barrido diagonal entre láminas

_entorno = Environment(loader=FileSystemLoader(AQUI), autoescape=True)


class HyperFramesNoDisponible(RuntimeError):
    """Falta Node o las dependencias de HyperFrames: `instalar.ps1` las pone."""


def disponible() -> str | None:
    """None si se puede renderizar; si no, qué falta."""
    if shutil.which("node") is None:
        return "Falta Node.js 22 o más nuevo"
    if not CLI.exists() or not GSAP.exists():
        return "Faltan las dependencias de HyperFrames: cd motor/hyperframes && npm install"
    return None


# ── Color ────────────────────────────────────────────────────────────────────

def _luz(hexa: str) -> float:
    r, g, b = (int(hexa.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4  # noqa: E731
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _sobre(fondo: str) -> str:
    """Negro o blanco, el que más contraste haga sobre `fondo`."""
    return "#0B0B0B" if _luz(fondo) > 0.36 else "#FFFFFF"


def es_oscura(imagen: Path) -> bool:
    """Si lo visible de la imagen es oscuro (un ícono negro o verde oscuro se pierde sobre el fondo)."""
    from PIL import Image
    try:
        with Image.open(imagen) as im:
            im = im.convert("RGBA").resize((48, 48))
            datos = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
            px = [(r, g, b) for r, g, b, a in datos if a > 128]
    except OSError:
        return False
    if not px:
        return False
    return sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px) / len(px) < 90


def colores(estilo: dict) -> dict:
    caja = estilo["texto"] if _luz(estilo["texto"]) > 0.5 else "#FFFFFF"
    return {**{k: estilo[k] for k in ("fondo", "superficie", "texto", "acento", "acento2")},
            "caja": caja, "caja_texto": _sobre(caja), "resalte_texto": _sobre(estilo["acento"])}


# ── Medidas por formato ──────────────────────────────────────────────────────

def capa(ancho: int, alto: int) -> dict:
    """Dónde va cada cosa. Vertical: texto arriba, como en los reels; horizontal: abajo a la izquierda."""
    vertical = alto > ancho
    base = min(ancho, alto)
    return {
        "x": round(ancho * (0.065 if vertical else 0.07)),
        "y": round(alto * (0.17 if vertical else 0.56)),
        "letra": round(base * (0.085 if vertical else 0.078)),
        "etiqueta": round(base * 0.026),
        "hueco": round(base * 0.012),
        "logo": round(base * 0.05), "logo_x": round(base * 0.05), "logo_y": round(base * 0.045),
        "icono": round(base * (0.55 if vertical else 0.42)),
        "icono_y": 62 if vertical else 40,
        "barrido": round(max(ancho, alto) * 1.6),
        "velo": ("linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,.15) 38%, rgba(0,0,0,0) 55%, rgba(0,0,0,.35) 100%)"
                 if vertical else
                 "linear-gradient(0deg, rgba(0,0,0,.65) 0%, rgba(0,0,0,.2) 50%, rgba(0,0,0,0) 70%)"),
        "ancho_texto": ancho - 2 * round(ancho * (0.065 if vertical else 0.07)),
    }


def tam_letra(palabras: list[str], estilo: str, c: dict) -> int:
    """El tamaño para que la palabra más larga quepa en una línea y el bloque no pase de 3 líneas."""
    base = c["letra"] * (1.6 if estilo == "termino" else 1.25 if estilo == "cifra" else 1.0)
    ancho = c["ancho_texto"]
    por_letra = 0.74  # ancho medio de una mayúscula de Montserrat 900, en «em» (con su caja)
    larga = max(len(p) for p in palabras) + 0.6
    base = min(base, ancho / (larga * por_letra))
    total = sum(len(p) + 0.9 for p in palabras)
    while base > 24 and total * base * por_letra / ancho > 3:
        base *= 0.92
    return int(base)


# ── La composición ───────────────────────────────────────────────────────────

def _archivo(uri_o_ruta: str | None) -> Path | None:
    if not uri_o_ruta:
        return None
    if uri_o_ruta.startswith("file:"):
        p = Path(unquote(urlparse(uri_o_ruta).path).lstrip("/"))
    else:
        p = Path(uri_o_ruta)
    return p if p.exists() else None


class _Assets:
    """Copia (o enlaza) cada archivo a `assets/` del proyecto, una vez, con un nombre estable."""

    def __init__(self, carpeta: Path):
        self.carpeta = carpeta
        self.nombres: dict[Path, str] = {}

    def __call__(self, origen: Path) -> str:
        if origen not in self.nombres:
            nombre = hashlib.sha1(str(origen).encode()).hexdigest()[:12] + origen.suffix.lower()
            destino = self.carpeta / nombre
            if not destino.exists():
                try:
                    os.link(origen, destino)  # mismo disco: no ocupa espacio
                except OSError:
                    shutil.copy2(origen, destino)
            self.nombres[origen] = nombre
        return f"assets/{self.nombres[origen]}"


def componer(spec, carpeta: Path) -> tuple[Path, list[Path]]:
    """Escribe el proyecto HyperFrames del video en `carpeta`. Devuelve el index.html y los archivos que usa."""
    v = spec.video
    ancho, alto, fps = v.ancho, v.alto, v.fps
    c = capa(ancho, alto)
    (carpeta / "assets").mkdir(parents=True, exist_ok=True)
    assets = _Assets(carpeta / "assets")
    shutil.copy2(GSAP, carpeta / "assets" / "gsap.min.js")
    shutil.copy2(FUENTE, carpeta / "assets" / "Montserrat.ttf")
    usados = [GSAP, FUENTE]
    logo = _archivo(spec.estilo.get("logo"))
    if logo is not None:
        usados.append(logo)

    tomas, beats, barridos = [], [], []
    total = round(sum(e.cuadros for e in spec.escenas) / fps, 3)
    for k, e in enumerate(spec.escenas):
        t0 = round(e.inicio, 3)
        if k > 0:
            barridos.append({"id": f"barrido-{k}", "inicio": round(max(0.0, t0 - BARRIDO / 2), 3), "duracion": BARRIDO})
        for j, b in enumerate(e.beats):
            inicio, duracion = round(t0 + b.inicio, 3), round(b.fin - b.inicio, 3)
            # Una toma que sigue igual que la anterior se alarga en vez de cortar.
            archivo = _archivo(b.toma.archivo)
            tipo = b.toma.tipo if (archivo is not None or b.toma.tipo == "marca") else "marca"
            previa = tomas[-1] if tomas else None
            if (previa and previa["tipo"] == tipo and previa["origen"] == archivo and tipo != "clip"
                    and abs(previa["inicio"] + previa["duracion"] - inicio) < 0.01 and j > 0):
                previa["duracion"] = round(previa["duracion"] + duracion, 3)
            else:
                tomas.append({"id": f"toma-{k}-{j}", "tipo": tipo, "inicio": inicio, "duracion": duracion,
                              "desde": b.toma.desde, "origen": archivo, "src": assets(archivo) if archivo else None,
                              "oscura": tipo == "lamina" and es_oscura(archivo)})
                if archivo is not None:
                    usados.append(archivo)
            palabras = b.texto.split()
            beats.append({
                "id": f"texto-{k}-{j}", "inicio": inicio, "duracion": duracion, "estilo": b.estilo,
                "etiqueta": b.etiqueta, "tam": tam_letra(palabras, b.estilo, c),
                "tiempos": [round(t0 + x, 3) for x in (b.palabras or [b.inicio] * len(palabras))],
                "palabras": [{"texto": p, "on": i in b.resaltado,
                              "cuenta": int(p) if p.isdigit() and 2 <= int(p) <= 100000 else None}
                             for i, p in enumerate(palabras)],
            })
    datos = {"tomas": [{k: x[k] for k in ("id", "tipo", "inicio", "duracion")} for x in tomas],
             "beats": [{"id": b["id"], "inicio": b["inicio"], "duracion": b["duracion"], "estilo": b["estilo"],
                        "etiqueta": bool(b["etiqueta"]), "tiempos": b["tiempos"]} for b in beats],
             "barridos": barridos}
    html = _entorno.get_template("composicion.html").render(
        ancho=ancho, alto=alto, total=total, c=colores(spec.estilo), capa=c, tomas=tomas, beats=beats,
        barridos=barridos, logo=assets(logo) if logo else None, datos=datos)
    indice = carpeta / "index.html"
    indice.write_text(html, encoding="utf-8")
    return indice, usados


def huella(indice: Path, usados: list[Path], spec) -> str:
    """Cambia si cambia la composición o cualquiera de sus archivos (por tamaño y fecha)."""
    h = hashlib.sha256(indice.read_bytes())
    for p in sorted(set(usados)):
        st = p.stat()
        h.update(f"{p}|{st.st_size}|{st.st_mtime_ns}".encode())
    h.update(json.dumps([VERSION, spec.video.fps, spec.video.crf, spec.video.escala]).encode())
    return h.hexdigest()[:24]


def _entorno_render() -> dict:
    env = {**os.environ, "HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1", "HYPERFRAMES_SKIP_SKILLS": "1"}
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:  # el PATH del servidor ya lo trae; se asegura por si Node lo busca en otro lado
        env["PATH"] = str(Path(ffmpeg).parent) + os.pathsep + env.get("PATH", "")
    return env


def renderizar(carpeta: Path, salida: Path, fps: int, crf: str, segundos: float, trabajadores: int | None = None,
               avisar=lambda hechas, total: None) -> None:
    """Corre `hyperframes render` sobre el proyecto. Lanza RuntimeError con el final del registro si falla."""
    falta = disponible()
    if falta:
        raise HyperFramesNoDisponible(falta)
    orden = ["node", str(CLI), "render", str(carpeta), "-o", str(salida), "--fps", str(fps), "--crf", str(crf),
             "--workers", str(trabajadores or "auto"), "--quiet"]
    registro = carpeta / "render.log"
    with registro.open("w", encoding="utf-8", errors="replace") as log:
        p = subprocess.run(orden, stdout=log, stderr=subprocess.STDOUT, env=_entorno_render(), cwd=carpeta,
                           timeout=600 + segundos * 20)
    if p.returncode != 0 or not salida.exists():
        final = registro.read_text(encoding="utf-8", errors="replace")[-1500:]
        raise RuntimeError(f"HyperFrames no pudo renderizar (código {p.returncode}): {final}")
    avisar(1, 1)
