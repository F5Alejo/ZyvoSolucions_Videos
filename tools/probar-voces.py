# -*- coding: utf-8 -*-
"""Genera la MISMA frase con varias voces de ElevenLabs para poder compararlas.

    set ELEVENLABS_API_KEY=...
    python tools/probar-voces.py <carpeta-destino>

El acento no es un ajuste que se aplique a una voz: es una propiedad de la voz.
Para cambiarlo hay que cambiar de voz, y la unica forma honesta de elegir es
oir la misma frase en todas, con los mismos ajustes.

No se usa curl: el cuerpo lleva acentos y hay que mandarlo en UTF-8 explicito o
la API responde 400 invalid_unicode.
"""
import base64, io, json, os, sys, urllib.error, urllib.request

FRASE = ("Sábado 3 de octubre, diez de la mañana. En vivo con el doctor "
         "Yezid Ricaurte. Cupo gratuito y limitado.")

# Mismos ajustes que la locucion real, para que la comparacion sea justa
AJUSTES = {"stability": 0.32, "similarity_boost": 0.85, "style": 0.45,
           "use_speaker_boost": True, "speed": 0.97}

VOCES = [
    ("0-ACTUAL-Carlos",      "4PN5DHmrfIgZksvIrawS", "la que se uso en la pieza"),
    ("1-Jerome-calmado",     "qqab7XtemzUr6wYwGSrQ", "colombiano, calmado y cercano"),
    ("2-Alejo-COSTENO",      "SsO7anq9lnFq4QW8bfch", "colombiano de la costa: otro acento"),
    ("3-Ivan-contundente",   "OwXM764IiSDeqYNU1rbL", "colombiano, contundente"),
    ("4-Juan-claro",         "FA1FBP9TKxnBiw45fHmS", "colombiano, claro y expresivo"),
    ("5-Gabriel",            "l7mz7X0JldPlSP6WNhdd", "colombiano, neutro"),
    ("6-Sandra-ejecutiva",   "mvUcswqyALvhz2mIGROO", "latinoamericana, femenina ejecutiva"),
]


def main(destino):
    clave = os.environ.get("ELEVENLABS_API_KEY")
    if not clave:
        raise SystemExit("falta ELEVENLABS_API_KEY en el entorno")
    if not os.path.isdir(destino):
        os.makedirs(destino)

    for nombre, vid, nota in VOCES:
        cuerpo = json.dumps({"text": FRASE, "model_id": "eleven_multilingual_v2",
                             "voice_settings": AJUSTES}).encode("utf-8")
        url = ("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps"
               "?output_format=mp3_44100_128" % vid)
        req = urllib.request.Request(url, data=cuerpo, method="POST",
                                     headers={"xi-api-key": clave,
                                              "Content-Type": "application/json"})
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as e:
            print("  %-22s FALLO %d: %s" % (nombre, e.code,
                                            e.read().decode("utf-8", "replace")[:90]))
            continue
        ruta = os.path.join(destino, nombre + ".mp3")
        io.open(ruta, "wb").write(base64.b64decode(d["audio_base64"]))
        dur = d["alignment"]["character_end_times_seconds"][-1]
        print("  %-22s %5.2f s   %s" % (nombre, dur, nota))

    io.open(os.path.join(destino, "LEEME.txt"), "w", encoding="utf-8", newline="\n").write(
        u"""Muestras de voz — ElevenLabs
=============================

Todas dicen LA MISMA frase con LOS MISMOS ajustes, para que la comparacion sea
justa. Lo unico que cambia es la voz.

El acento no se aplica como un ajuste: es una propiedad de la voz. Por eso la
forma de cambiarlo es cambiar de voz.

  0-ACTUAL-Carlos      la que esta en la pieza hoy
  1-Jerome-calmado     colombiano, calmado y cercano
  2-Alejo-COSTENO      colombiano de la COSTA: acento marcadamente distinto
  3-Ivan-contundente   colombiano, contundente
  4-Juan-claro         colombiano, claro y expresivo
  5-Gabriel            colombiano, neutro
  6-Sandra-ejecutiva   latinoamericana, femenina, registro ejecutivo

Si ninguna convence, hay ~60 voces mas en la biblioteca con la misma clave.
Dime el perfil que buscas -mas grave, mas joven, mas pausado- y saco otra tanda.

Cambiar de voz obliga a regenerar la locucion y a recolocar las animaciones
sobre los tiempos nuevos, porque cada voz dura distinto. Es un paso mecanico:
voz-eleven.py devuelve los tiempos reales por frase.
""")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pruebas-de-voz")
