# -*- coding: utf-8 -*-
"""Prueba de pronunciacion de la sigla PESV (las dos frases que la dicen).

Para cada forma de escribir la sigla genera f1 y f3 con la MISMA semilla y mide,
con el alineamiento por caracter de ElevenLabs, cuanto dura la sigla en cada
frase. Duraciones parecidas en f1 y f3 = la lee igual las dos veces.
Deja un MP3 por variante (f1 + silencio + f3) para escucharlas.

    python tools/prueba-sigla.py
"""
import base64, io, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
ve = importlib.import_module("voz-eleven")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "..", "..", "..", "ENTREGABLES-VIDEO", "fegir-envivo", "prueba-sigla-PESV")
VOZ, MODELO, SEMILLA = "4PN5DHmrfIgZksvIrawS", "eleven_multilingual_v2", 20261003

VARIANTES = {
    "A-como-esta": "P-E-S-V",
    "B-letras-sueltas": "pe e ese ve",
    "C-con-puntos": "P.E.S.V.",
    "D-guiones-minuscula": "pe-e-ese-ve",
}
F1 = "¿Tu informe del {s} todavía se arma a mano?..."
F3 = "Informe de Autogestión {s}... en un solo clic."
AJ1 = {"speed": 0.97, "style": 0.5}
AJ3 = {"speed": 1.0}


def clave():
    f = os.path.join(os.path.expanduser("~"), ".elevenlabs-key.txt")
    return os.environ.get("ELEVENLABS_API_KEY") or io.open(f, encoding="utf-8-sig").read().strip()


def pedir(texto, ajustes):
    os.environ["ELEVENLABS_API_KEY"] = clave()
    ajustes = dict(ajustes)
    cuerpo_extra = {"seed": SEMILLA}
    # convertir() no admite seed: se llama al endpoint directamente con los mismos ajustes
    import urllib.request
    cuerpo = {"text": texto, "model_id": MODELO, "voice_settings": dict(ve.AJUSTES, **ajustes)}
    cuerpo.update(cuerpo_extra)
    url = ("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % VOZ)
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"xi-api-key": clave(), "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())


def dur_sigla(texto, sigla, al):
    i = texto.index(sigla)
    j = i + len(sigla) - 1
    return al["character_end_times_seconds"][j] - al["character_start_times_seconds"][i]


def main():
    os.makedirs(DEST, exist_ok=True)
    filas = []
    for nombre, sigla in VARIANTES.items():
        partes, durs = [], []
        for k, (plantilla, aj) in enumerate(((F1, AJ1), (F3, AJ3)), 1):
            texto = plantilla.format(s=sigla)
            d = pedir(texto, aj)
            mp3 = os.path.join(DEST, "_%s-f%d.mp3" % (nombre, k))
            open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
            partes.append(mp3)
            durs.append(dur_sigla(texto, sigla, d["alignment"]))
        salida = os.path.join(DEST, "%s.mp3" % nombre)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", partes[0], "-f", "lavfi", "-t", "0.8",
                        "-i", "anullsrc=r=44100:cl=mono", "-i", partes[1], "-filter_complex",
                        "[0][1][2]concat=n=3:v=0:a=1", "-b:a", "128k", salida], check=True)
        for p in partes:
            os.remove(p)
        filas.append((nombre, sigla, durs[0], durs[1]))
        print("%-22s %-14s frase1 %.2f s  frase3 %.2f s  diferencia %.2f s"
              % (nombre, sigla, durs[0], durs[1], abs(durs[0] - durs[1])))
    io.open(os.path.join(DEST, "medidas.json"), "w", encoding="utf-8").write(
        json.dumps(filas, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
