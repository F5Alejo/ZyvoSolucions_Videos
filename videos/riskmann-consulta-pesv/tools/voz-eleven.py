# -*- coding: utf-8 -*-
"""Locuta los 6 planos de riskmann-consulta-pesv con ElevenLabs y devuelve sus
tiempos reales por frase (con-timestamps, sin pasada de Whisper).

    set ELEVENLABS_API_KEY=...
    python tools/voz-eleven.py <voice_id> [modelo]

Adaptado de videos/ruta-segura-m1/tools/voz-eleven.py — mismo endpoint
con-timestamps, mismo principio (el inicio de cada frase se lee del
alineamiento por carácter, nunca se estima). La clave no se guarda en el
repositorio: se lee del entorno.
"""
import base64, io, json, os, sys, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DEST = os.path.join(RAIZ, "assets", "voz")
MODELO = "eleven_multilingual_v2"


def convertir(clave, voice_id, texto, modelo):
    ajustes = {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": True}
    cuerpo = {"text": texto, "model_id": modelo, "voice_settings": ajustes}
    url = ("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps"
           "?output_format=mp3_44100_128" % voice_id)
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"xi-api-key": clave, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=600).read())
    except urllib.error.HTTPError as e:
        raise SystemExit("ElevenLabs %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))


def inicios_de_frase(texto, frases, alineacion):
    ini = alineacion["character_start_times_seconds"]
    fin = alineacion["character_end_times_seconds"]
    out, cursor = [], 0
    for f in frases:
        i = texto.index(f, cursor)
        out.append(round(ini[min(i, len(ini) - 1)], 3))
        cursor = i + len(f)
    out.append(round(fin[-1], 3))
    return out


def main():
    clave = os.environ.get("ELEVENLABS_API_KEY")
    if not clave:
        raise SystemExit("falta ELEVENLABS_API_KEY en el entorno")
    if len(sys.argv) < 2:
        raise SystemExit("uso: python tools/voz-eleven.py <voice_id> [modelo]")
    voice_id = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else MODELO

    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    planos = json.load(io.open(os.path.join(AQUI, "narracion.json"), encoding="utf-8"))

    tiempos = []
    for p in planos:
        d = convertir(clave, voice_id, p["texto"], modelo)
        mp3 = os.path.join(DEST, "f%02d.mp3" % p["n"])
        io.open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        ini = inicios_de_frase(p["texto"], p["frases"], d["alignment"])
        tiempos.append({"n": p["n"], "frames": p["frames"], "frases": p["frases"], "inicios": ini,
                         "duracion": ini[-1]})
        print("plano %02d  %5.2f s  (%d frases)  -> %s" % (p["n"], ini[-1], len(p["frases"]), mp3))

    io.open(os.path.join(AQUI, "tiempos-voz.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(tiempos, ensure_ascii=False, indent=1))
    total = sum(t["duracion"] for t in tiempos)
    print("-" * 44)
    print("narración total %.1f s  ·  voz %s, modelo %s" % (total, voice_id, modelo))
    print("escrito tools/tiempos-voz.json")


if __name__ == "__main__":
    main()
