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


# Una locucion publicitaria no se lee, se interpreta. Con stability 0.5 el modelo
# entrega una lectura plana y apresurada; bajarla deja que module, y "style" le da
# intencion. "speed" se afina por plano en narracion.json: solo donde sobra tiempo
# dentro de su corte, porque la duracion de cada plano es fija.
AJUSTES = {"stability": 0.32, "similarity_boost": 0.85, "style": 0.45,
           "use_speaker_boost": True, "speed": 0.96}


def convertir(clave, voice_id, texto, modelo, extra=None):
    ajustes = dict(AJUSTES)
    ajustes.update(extra or {})
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

    tiempos, desbordes = [], []
    for p in planos:
        d = convertir(clave, voice_id, p["texto"], modelo, p.get("ajustes"))
        mp3 = os.path.join(DEST, "f%02d.mp3" % p["n"])
        io.open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        ini = inicios_de_frase(p["texto"], p["frases"], d["alignment"])
        tiempos.append({"n": p["n"], "frames": p["frames"], "frases": p["frases"], "inicios": ini,
                         "duracion": ini[-1]})
        # cada plano dura lo que dura su corte: si la voz se pasa, hay que
        # acortar el texto o subir "speed", nunca descubrirlo en el MP4 final
        tope = p.get("tope")
        aviso = ""
        if tope and ini[-1] > tope:
            aviso = "  DESBORDA el plano por %.2f s" % (ini[-1] - tope)
            desbordes.append((p["n"], ini[-1], tope))
        print("plano %02d  %5.2f s  (%d frases)  -> %s%s"
              % (p["n"], ini[-1], len(p["frases"]), mp3, aviso))

    io.open(os.path.join(AQUI, "tiempos-voz.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(tiempos, ensure_ascii=False, indent=1))
    total = sum(t["duracion"] for t in tiempos)
    print("-" * 44)
    print("narración total %.1f s  ·  voz %s, modelo %s" % (total, voice_id, modelo))
    print("escrito tools/tiempos-voz.json")
    if desbordes:
        for n, d, t in desbordes:
            print("  plano %02d: %.2f s contra un tope de %.2f s" % (n, d, t))
        raise SystemExit("FALLO: hay locucion que no cabe en su plano")


if __name__ == "__main__":
    main()
