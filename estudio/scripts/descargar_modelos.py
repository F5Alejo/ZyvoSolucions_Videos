"""Descarga los modelos de voz que usa el motor a `modelos/` (no va a git).

    python scripts/descargar_modelos.py

Kokoro-82M (Apache 2.0) es la voz gratuita para entregar. Piper davefx queda solo para
borradores internos: ver docs/bitacora.md (licencia de la base lessac).
"""

import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "modelos"

KOKORO = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
PIPER = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/"

ARCHIVOS = {
    RAIZ / "kokoro" / "kokoro-v1.0.int8.onnx": KOKORO + "kokoro-v1.0.int8.onnx",
    RAIZ / "kokoro" / "voices-v1.0.bin": KOKORO + "voices-v1.0.bin",
    RAIZ / "voces" / "es_ES-davefx-medium.onnx": PIPER + "es_ES-davefx-medium.onnx",
    RAIZ / "voces" / "es_ES-davefx-medium.onnx.json": PIPER + "es_ES-davefx-medium.onnx.json",
}


def main() -> int:
    for destino, url in ARCHIVOS.items():
        if destino.exists():
            print(f"ya está  {destino.relative_to(RAIZ.parent)}")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        print(f"bajando  {destino.relative_to(RAIZ.parent)} …", flush=True)
        temporal = destino.with_suffix(destino.suffix + ".parcial")
        urllib.request.urlretrieve(url, temporal)
        temporal.replace(destino)
    print("Listo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
