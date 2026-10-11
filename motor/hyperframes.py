"""HyperFrames: armar el proyecto de un video y renderizarlo.

HyperFrames (HeyGen, Apache 2.0) convierte HTML en MP4. A diferencia de lo que hace
`motor/render.py` con Playwright —que dibuja cuadro a cuadro solo la entrada y la salida de
cada escena y deja congelado lo del medio—, HyperFrames dibuja **todos** los cuadros buscando
cada instante en una línea de tiempo en pausa. Eso es lo que permite que los elementos de una
lámina vayan entrando mientras habla la voz, en vez de aparecer todos de golpe al principio.

El proyecto que se arma es una carpeta normal de HyperFrames:

    salida/<clave>/hf/
    ├── hyperframes.json · package.json
    ├── index.html              el video: una sub-composición por lámina
    ├── compositions/lamina-NN.html
    └── assets/
        ├── fuentes/…           la tipografía (no se baja de internet: el render es offline)
        └── media/…             las imágenes del PPTX

Se renderiza **mudo**: la voz, la música y los efectos los sigue mezclando ffmpeg en
`motor/audio.py`, que es donde viven el ducking y el -14 LUFS, y de ahí salen los subtítulos y
el control de calidad. HyperFrames solo pone la imagen.

Requisitos: Node 20+ (HyperFrames pide 22+) y ffmpeg en el PATH. `disponible()` lo comprueba y
`motor/diagnostico.py` lo muestra en `/configuracion`.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

from motor import errores

VERSION = "0.8.145"  # fijada: un render tiene que dar lo mismo hoy y dentro de un año
PAQUETE = f"hyperframes@{VERSION}"
NODE_MINIMO = 22

_CONFIG = {
    "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
    "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
    "media": {"autoProxy": False},
}


def _npx() -> str | None:
    return shutil.which("npx") or shutil.which("npx.cmd")


def _correr(args: list[str], cwd: Path, tiempo: int = 3600) -> subprocess.CompletedProcess:
    npx = _npx()
    if npx is None:
        raise errores.ErrorZyvo("RENDER_002", etapa="escenas")
    # `--yes` para que no pregunte nada: el motor corre sin nadie delante.
    entorno = {**os.environ, "HYPERFRAMES_TELEMETRY": "0", "DO_NOT_TRACK": "1"}
    return subprocess.run([npx, "--yes", PAQUETE, *args], cwd=str(cwd), env=entorno,
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=tiempo)


def version_node() -> tuple[int, str] | None:
    """(mayor, versión) de Node, o None si no está."""
    node = shutil.which("node") or shutil.which("node.exe")
    if node is None:
        return None
    try:
        v = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
        return int(v.lstrip("v").split(".")[0]), v
    except (ValueError, IndexError, subprocess.SubprocessError):
        return None


def disponible() -> dict:
    """Si se puede renderizar con HyperFrames en este equipo, y qué falta si no."""
    if _npx() is None:
        return {"ok": False, "detalle": "Node no está instalado (HyperFrames lo necesita)",
                "arreglo": "winget install OpenJS.NodeJS.LTS"}
    node = version_node()
    if node is None:
        return {"ok": False, "detalle": "No se pudo leer la versión de Node",
                "arreglo": "winget install OpenJS.NodeJS.LTS"}
    if node[0] < NODE_MINIMO:
        return {"ok": False, "detalle": f"Node {node[1]}: HyperFrames necesita {NODE_MINIMO} o superior",
                "arreglo": "winget upgrade OpenJS.NodeJS.LTS"}
    if not (shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")):
        return {"ok": False, "detalle": "Falta ffmpeg, que es el que codifica",
                "arreglo": "winget install Gyan.FFmpeg"}
    return {"ok": True, "detalle": f"HyperFrames {VERSION} · Node {node[1]}"}


# ── El proyecto ───────────────────────────────────────────────────────────────

def preparar(carpeta: Path, nombre: str = "zyvo") -> Path:
    """Deja la carpeta lista para recibir las composiciones. Devuelve la carpeta."""
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "compositions").mkdir(exist_ok=True)
    (carpeta / "assets" / "fuentes").mkdir(parents=True, exist_ok=True)
    (carpeta / "assets" / "media").mkdir(parents=True, exist_ok=True)
    (carpeta / "hyperframes.json").write_text(json.dumps(_CONFIG, indent=2), encoding="utf-8")
    (carpeta / "package.json").write_text(
        json.dumps({"name": nombre, "private": True, "type": "module"}, indent=2), encoding="utf-8")
    return carpeta


def copiar_recursos(carpeta: Path, fuente: Path, media: Path | None) -> None:
    """Mete en el proyecto la tipografía y las imágenes: el render no sale a internet."""
    if fuente.exists():
        shutil.copy2(fuente, carpeta / "assets" / "fuentes" / fuente.name)
    if media is not None and media.exists():
        for img in media.iterdir():
            if img.is_file():
                shutil.copy2(img, carpeta / "assets" / "media" / img.name)


def escribir(carpeta: Path, indice: str, laminas: dict[str, str]) -> None:
    """`index.html` y una composición por lámina."""
    (carpeta / "index.html").write_text(indice, encoding="utf-8")
    for archivo, html in laminas.items():
        (carpeta / archivo).write_text(html, encoding="utf-8")


# ── Render ────────────────────────────────────────────────────────────────────

# Las secciones del informe de `check`. `lint` es estática; las demás necesitan el navegador.
SECCIONES = ("lint", "runtime", "layout", "motion", "contrast")


def revisar(carpeta: Path) -> list[str]:
    """Pasa `hyperframes check`. Devuelve los errores encontrados (vacío si está limpio).

    Ojo con el informe: un error de `lint` **apaga** la sesión de navegador, y entonces
    `layout`, `motion` y `contrast` vienen con cero hallazgos aunque no se haya mirado nada
    (`browserSkipped`). Leer solo los contadores da un «limpio» que no significa nada: por eso
    aquí se avisa explícitamente de que la auditoría no llegó a correr.
    """
    r = _correr(["check", "--json"], carpeta, tiempo=900)
    try:
        datos = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        cola = (r.stdout or "") + (r.stderr or "")
        return [f"no se pudo leer el informe de check: {cola.strip()[-300:]}"] if r.returncode else []

    problemas = []
    for seccion in SECCIONES:
        for h in (datos.get(seccion) or {}).get("findings") or []:
            if str(h.get("severity", "error")).lower() != "error":
                continue
            donde = Path(h.get("sourceFile", "")).name or seccion
            problemas.append(f"[{seccion}] {h.get('code', '?')} en {donde}: "
                             f"{(h.get('message') or '').splitlines()[0][:200]}")
    if datos.get("browserSkipped") and problemas:
        problemas.append("[check] la auditoría de layout y contraste no llegó a correr: "
                         "arregla primero los errores de lint")
    return problemas


def render(carpeta: Path, destino: Path, fps: int = 30, calidad: str = "looks",
           avisar=lambda hechas, total: None) -> Path:
    """Renderiza el proyecto a `destino` (MP4 mudo). Lanza `ErrorZyvo` si falla."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    avisar(0, 1)
    r = _correr(["render", "--output", str(destino.resolve()), "--fps", str(fps),
                 "--quality", calidad, "--quiet"], carpeta)
    if r.returncode != 0 or not destino.exists():
        cola = "\n".join((r.stderr or r.stdout or "").strip().splitlines()[-12:])
        error = errores.ErrorZyvo("RENDER_003", etapa="escenas")
        error.__cause__ = RuntimeError(cola)
        raise error
    avisar(1, 1)
    return destino
