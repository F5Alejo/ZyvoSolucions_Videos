# -*- coding: utf-8 -*-
"""Renderiza las partes de un proyecto, saltando las que ya están hechas.

    python tools/render-partes.py <carpeta-del-proyecto> [más carpetas...]

En una máquina de 8 GB el sistema mata el render cada tantas partes. Un lote
corrido de diez partes pierde, con cada muerte, todo lo que venía detrás. Este
script hace el lote **reanudable**: comprueba qué partes ya existen con la
duración correcta y solo renderiza las que faltan, así que basta con volver a
invocarlo hasta que termine.

Antes de cada parte mata los `ffmpeg` y `chrome-headless-shell` huérfanos: un
render abortado deja un ffmpeg de ~650 MB, y sin limpiarlo el siguiente intento
arranca con menos margen que el anterior.
"""
import glob, io, os, re, subprocess, sys

TOLERANCIA = 0.25   # segundos de diferencia admitidos entre lo pedido y lo rendido


def duracion(ruta):
    try:
        out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                       "format=duration", "-of", "csv=p=0", ruta],
                                      stderr=subprocess.DEVNULL)
        return float(out.decode().strip())
    except Exception:
        return None


def esperada(indice):
    """La duración que declara el index parcial, para saber si el MP4 corresponde."""
    s = io.open(indice, encoding="utf-8").read(4000)
    m = re.search(r'data-composition-id="main"[^>]*data-duration="([0-9.]+)"', s, re.S)
    return float(m.group(1)) if m else None


def limpiar_huerfanos():
    for proc in ("ffmpeg.exe", "chrome-headless-shell.exe"):
        subprocess.run(["taskkill", "/F", "/IM", proc], capture_output=True)


def render(proyecto, indice, salida):
    entorno = dict(os.environ, PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS="120000")
    return subprocess.call(
        ["npx", "hyperframes", "render", "-c", os.path.basename(indice),
         "-o", os.path.join("renders", os.path.basename(salida)),
         "--quality", "high", "--low-memory-mode", "--workers", "1",
         "--browser-timeout", "240"],
        cwd=proyecto, env=entorno, shell=(os.name == "nt"))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python tools/render-partes.py <carpeta-del-proyecto> [...]")

    pendientes = 0
    for proyecto in sys.argv[1:]:
        indices = sorted(glob.glob(os.path.join(proyecto, "index-parte-*.html")),
                         key=lambda p: int(re.search(r"parte-(\d+)", p).group(1)))
        if not indices:
            print("%s: no hay partes que renderizar" % proyecto)
            continue
        print("=== %s (%d partes)" % (os.path.basename(proyecto.rstrip("/\\")), len(indices)))
        for indice in indices:
            n = int(re.search(r"parte-(\d+)", indice).group(1))
            salida = os.path.join(proyecto, "renders", "parte-%d.mp4" % n)
            quiere, hay = esperada(indice), duracion(salida)
            if hay is not None and quiere is not None and abs(hay - quiere) < TOLERANCIA:
                print("   parte %d  ya está (%.2f s)" % (n, hay))
                continue
            print("   parte %d  renderizando (%.2f s)..." % (n, quiere or 0))
            limpiar_huerfanos()
            if render(proyecto, indice, salida) != 0 or duracion(salida) is None:
                print("   parte %d  FALLÓ — vuelve a correr este script para reintentarla" % n)
                pendientes += 1
                return 1
    if pendientes:
        return 1
    print("")
    print("todas las partes están rendidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
