"""Locucion de la serie: un WAV por linea de guion, con la voz aprobada.

Uso (desde la carpeta del proyecto):
    python ../../tools/voz.py tools/guion.json

guion.json:
    {
      "voz": "es_ES-davefx-medium",        (opcional; es la aprobada)
      "velocidad": 1.0,                    (opcional; >1 mas lento, <1 mas rapido)
      "lineas": [
        { "id": "h1", "texto": "Tu no conduces.", "maximo": 3.0 },
        { "id": "02", "texto": "No manejar no significa ser un actor pasivo." }
      ]
    }

Escribe assets/vo/<id>.wav y lista la duracion de cada linea. Si una linea trae
"maximo" (segundos disponibles en su plano) y se pasa, lo avisa: la regla es
acortar la frase o ajustar la velocidad, NUNCA re-cronometrar el plano, porque
eso desincroniza todas las animaciones que ya estaban ajustadas a la voz.

Cada texto debe poder rastrearse a un archivo entregado por RiskMann.

Requiere:  pip install piper-tts
           python tools/descargar-voz.py   (una vez: baja el modelo a tools/voces/)
"""

import json, os, subprocess, sys, wave

VOCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voces")


def main(cfg_path):
    sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    modelo = os.path.join(VOCES, cfg.get("voz", "es_ES-davefx-medium") + ".onnx")
    if not os.path.exists(modelo):
        sys.exit("no encuentro el modelo de voz: " + modelo +
                 "\nbájalo una vez con:  python tools/descargar-voz.py")
    os.makedirs("assets/vo", exist_ok=True)
    pasadas = 0
    for ln in cfg["lineas"]:
        out = os.path.join("assets", "vo", ln["id"] + ".wav")
        subprocess.run([sys.executable, "-m", "piper", "-m", modelo, "-f", out,
                        "--length-scale", str(cfg.get("velocidad", 1.0))],
                       input=ln["texto"].encode("utf-8"), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with wave.open(out) as w:
            dur = w.getnframes() / float(w.getframerate())
        aviso = ""
        if "maximo" in ln and dur > ln["maximo"]:
            aviso = f"   <-- SE PASA de {ln['maximo']:.1f} s: acorta la frase"
            pasadas += 1
        print(f"{ln['id']:>4}  {dur:5.2f} s  {ln['texto'][:60]}{aviso}")
    if pasadas:
        sys.exit(f"{pasadas} linea(s) no caben en su plano.")


if __name__ == "__main__":
    main(sys.argv[1])
