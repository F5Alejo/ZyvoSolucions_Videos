"""Descarga la voz aprobada de la serie (Piper es_ES-davefx-medium) en tools/voces/.

Uso:  python tools/descargar-voz.py

El modelo pesa ~60 MB y no va en el repositorio (GitHub avisa desde 50 MB). Se baja
de la fuente oficial de Piper y se verifica su huella SHA-256: si no coincide, no es
la voz que el cliente aprobó y el script falla.
"""

import hashlib, os, sys, urllib.request

BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/"
ARCHIVOS = {
    "es_ES-davefx-medium.onnx": "6658b03b1a6c316ee4c265a9896abc1393353c2d9e1bca7d66c2c442e222a917",
    "es_ES-davefx-medium.onnx.json": "0e0dda87c732f6f38771ff274a6380d9252f327dca77aa2963d5fbdf9ec54842",
}
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voces")


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(DESTINO, exist_ok=True)
    for nombre, huella in ARCHIVOS.items():
        ruta = os.path.join(DESTINO, nombre)
        if os.path.exists(ruta) and sha256(ruta) == huella:
            print("ya está:", nombre)
            continue
        print("descargando:", nombre)
        urllib.request.urlretrieve(BASE + nombre, ruta)
        if sha256(ruta) != huella:
            os.remove(ruta)
            sys.exit("FALLO: la huella de " + nombre + " no coincide con la voz aprobada.")
        print("verificado:", nombre)


if __name__ == "__main__":
    main()
