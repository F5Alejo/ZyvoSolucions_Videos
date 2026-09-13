# -*- coding: utf-8 -*-
"""Locuta las once láminas con ElevenLabs y devuelve sus tiempos reales.

    set ELEVENLABS_API_KEY=...
    python tools/voz-eleven.py <voice_id> [modelo] [velocidad]

Tres decisiones que vienen de haberlas probado:

- **`eleven_v3`**, no `eleven_multilingual_v2`. El guion está lleno de preguntas
  («¿Ser cuidadoso basta para estar seguro?») y en español la entonación sube al
  final sin que haya palabra interrogativa; v2 las lee como afirmaciones. v3
  además habla más pausado, que es el ritmo de una capacitación.
- **Las cifras van en palabras.** En estas once láminas solo aparece «Ley 2466 de
  2025», pero un motor que la lee como «veinticuatro sesenta y seis» arruina la
  única referencia jurídica del módulo.
- **Cada lámina se encadena con la anterior** (`previous_text` / `next_text`):
  sin eso la entonación se reinicia en cada corte y se nota que son once tomas.

Pide el audio **con timestamps**: la respuesta trae el instante de cada carácter,
así que el inicio de cada frase se lee directamente en vez de estimarlo. Con eso
`tools/cronometro.py` recoloca todas las apariciones del video sobre la voz real.

La clave **no** se guarda en el repositorio: se lee del entorno.
"""
import base64, io, json, os, re, sys, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DEST = os.path.join(RAIZ, "assets", "voz")
MODELO = "eleven_v3"
CONTEXTO = 300      # caracteres de la lámina vecina que se pasan como contexto

UNIDADES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
            "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
            "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés",
            "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
DECENAS = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta",
           7: "setenta", 8: "ochenta", 9: "noventa"}
CENTENAS = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos",
            6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def en_palabras(n):
    """Números de 0 a 9999 en castellano. Basta para años y números de ley."""
    if n < 30:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DECENAS[d] + (" y " + UNIDADES[u] if u else "")
    if n < 1000:
        c, r = divmod(n, 100)
        if n == 100:
            return "cien"
        return CENTENAS[c] + (" " + en_palabras(r) if r else "")
    m, r = divmod(n, 1000)
    mil = "mil" if m == 1 else en_palabras(m) + " mil"
    return mil + (" " + en_palabras(r) if r else "")


def normalizar(texto):
    """Deja el texto como se debe leer en voz alta."""
    return re.sub(r"\b\d{1,4}\b", lambda m: en_palabras(int(m.group())), texto)


def convertir(clave, voice_id, texto, modelo, velocidad, antes, despues):
    ajustes = {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": True}
    if velocidad is not None:
        # v3 marca su propio ritmo; `speed` es para los modelos v2, que corren
        # más que el ritmo de una capacitación leída.
        ajustes["speed"] = velocidad
    cuerpo = {"text": texto, "model_id": modelo, "voice_settings": ajustes}
    # v3 todavía rechaza el encadenado («not yet supported with the eleven_v3
    # model»); en los v2 sí evita que la entonación se reinicie en cada lámina.
    if not modelo.startswith("eleven_v3"):
        if antes:
            cuerpo["previous_text"] = antes[-CONTEXTO:]
        if despues:
            cuerpo["next_text"] = despues[:CONTEXTO]

    url = ("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps"
           "?output_format=mp3_44100_128" % voice_id)
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"xi-api-key": clave, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=600).read())
    except urllib.error.HTTPError as e:
        raise SystemExit("ElevenLabs %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))


def inicios_de_frase(texto, frases, alineacion):
    """Instante en que empieza cada frase, leído del alineamiento por carácter."""
    ini = alineacion["character_start_times_seconds"]
    fin = alineacion["character_end_times_seconds"]
    out, cursor = [], 0
    for f in frases:
        i = texto.index(f, cursor)
        out.append(round(ini[min(i, len(ini) - 1)], 3))
        cursor = i + len(f)
    out.append(round(fin[-1], 3))     # final de la narración
    return out


def main():
    clave = os.environ.get("ELEVENLABS_API_KEY")
    if not clave:
        raise SystemExit("falta ELEVENLABS_API_KEY en el entorno")
    if len(sys.argv) < 2:
        raise SystemExit("uso: python tools/voz-eleven.py <voice_id> [modelo] [velocidad]")
    voice_id = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else MODELO
    velocidad = float(sys.argv[3]) if len(sys.argv) > 3 else None

    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    laminas = json.load(io.open(os.path.join(AQUI, "narracion.json"), encoding="utf-8"))
    textos = [normalizar(x["texto"]) for x in laminas]

    tiempos = []
    for i, x in enumerate(laminas):
        texto = textos[i]
        d = convertir(clave, voice_id, texto, modelo, velocidad,
                      textos[i - 1] if i else "", textos[i + 1] if i + 1 < len(textos) else "")
        mp3 = os.path.join(DEST, "s%02d.mp3" % x["n"])
        io.open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        ini = inicios_de_frase(texto, [normalizar(f) for f in x["frases"]], d["alignment"])
        tiempos.append({"n": x["n"], "inicios": ini})
        print("lámina %02d  %6.2f s  (%d frases)" % (x["n"], ini[-1], len(x["frases"])))

    io.open(os.path.join(AQUI, "tiempos-voz.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(tiempos, ensure_ascii=False, indent=1))
    total = sum(t["inicios"][-1] for t in tiempos)
    print("-" * 44)
    print("narración total %.1f s = %d:%02d  ·  voz %s, modelo %s"
          % (total, int(total // 60), int(round(total % 60)), voice_id, modelo))
    print("escrito tools/tiempos-voz.json — ahora: python tools/construir.py")


if __name__ == "__main__":
    main()
