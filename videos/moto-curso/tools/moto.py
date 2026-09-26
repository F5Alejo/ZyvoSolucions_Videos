# -*- coding: utf-8 -*-
"""Curso «Motociclista laboral seguro»: un video HyperFrames por módulo.

    set ELEVENLABS_API_KEY=...
    python videos/moto-curso/tools/moto.py voz apertura        # locución + tiempos (salta lo ya locutado)
    python videos/moto-curso/tools/moto.py construir apertura  # videos/moto-apertura/ con index y partes
    python tools/render-partes.py videos/moto-apertura
    python videos/moto-curso/tools/moto.py montar apertura     # pista de voz + unión + mezcla

Todo sale de `datos/curso.json` (formas con nombre y notas de orador del PPTX).
Cada lámina dura su narración más un respiro; las apariciones caen sobre la
frase que nombra cada elemento (`sincronia.py`). La clave nunca se escribe en
disco: se lee del entorno.
"""
import base64, glob, io, json, os, re, shutil, subprocess, sys, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
CURSO = os.path.dirname(AQUI)
VIDEOS = os.path.dirname(CURSO)
VOZ_DIR = os.path.join(CURSO, "assets", "voz")
TIEMPOS = os.path.join(CURSO, "datos", "tiempos-voz.json")

import base, plantillas

VOICE_ID = "4PN5DHmrfIgZksvIrawS"      # «Carlos», colombiana, la del curso Ruta Segura
MODELO = "eleven_v3"
ANTES = 1.0     # el título entra antes de que hable la voz
COLA = 1.3      # respiro después de la última frase

# límites exactos del mazo
LIMITES = {"apertura": (1, 6), "m01": (7, 11), "m02": (12, 17), "m03": (18, 23), "m04": (24, 29),
           "m05": (30, 35), "m06": (36, 41), "m07": (42, 47), "m08": (48, 53), "m09": (54, 59),
           "m10": (60, 65), "m11": (66, 71), "m12": (72, 77), "m13": (78, 83), "cierre": (84, 88)}
NOMBRES = {"apertura": "Apertura", "cierre": "Cierre"}
NOMBRES.update({"m%02d" % i: "Módulo %d" % i for i in range(1, 14)})


def curso():
    return {d["n"]: d for d in json.load(io.open(os.path.join(CURSO, "datos", "curso.json"), encoding="utf-8"))}


# Los videos son solo de contenido: las preguntas al participante (autochequeos,
# evaluaciones V/F y A/B/C, pausas autónomas y sus respuestas) van en la plataforma.
PAUSA = re.compile(r"(Antes de continuar|¿|Compare su respuesta|Respuesta:|OJO)")


def es_evaluacion(d):
    return any(k.startswith("q-text") for k in d["formas"])


def sin_preguntas(d):
    """Corta la nota donde empieza el bloque de pausa: siempre va al final."""
    d = dict(d)
    fr = d["frases"]
    i = next((i for i, f in enumerate(fr) if PAUSA.match(f)), len(fr))
    d["frases"] = fr[:i]
    d["texto"] = " ".join(fr[:i])
    return d


def laminas(clave):
    a, b = LIMITES[clave]
    c = curso()
    return [sin_preguntas(c[n]) for n in range(a, b + 1) if not es_evaluacion(c[n])]


def leer_tiempos():
    if os.path.exists(TIEMPOS):
        return {int(k): v for k, v in json.load(io.open(TIEMPOS, encoding="utf-8")).items()}
    return {}


def duracion(ruta):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", ruta])
    return float(out.decode().strip())


# ---------------------------------------------------------------- voz

UNIDADES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
            "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
            "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés",
            "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
DECENAS = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
CENTENAS = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos",
            6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def en_palabras(n):
    if n < 30:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DECENAS[d] + (" y " + UNIDADES[u] if u else "")
    if n < 1000:
        if n == 100:
            return "cien"
        c, r = divmod(n, 100)
        return CENTENAS[c] + (" " + en_palabras(r) if r else "")
    m, r = divmod(n, 1000)
    return ("mil" if m == 1 else en_palabras(m) + " mil") + (" " + en_palabras(r) if r else "")


def normalizar(t):
    t = t.replace("PESV", "P E S V").replace("SG-SST", "S G S S T")
    t = re.sub(r"(\d+)\s*%", lambda m: en_palabras(int(m.group(1))) + " por ciento", t)
    t = re.sub(r"(\d+)\s*km/h", lambda m: en_palabras(int(m.group(1))) + " kilómetros por hora", t)
    return re.sub(r"\b\d{1,4}\b", lambda m: en_palabras(int(m.group())), t)


def locutar(clave_api, texto):
    cuerpo = {"text": texto, "model_id": MODELO,
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "use_speaker_boost": True}}
    url = ("https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % VOICE_ID)
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"xi-api-key": clave_api, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=600).read())
    except urllib.error.HTTPError as e:
        raise SystemExit("ElevenLabs %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:400]))


def inicios_de_frase(texto, frases, al):
    ini, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cursor = [], 0
    for f in frases:
        i = texto.find(f, cursor)
        if i < 0:
            i = cursor
        out.append(round(ini[min(i, len(ini) - 1)], 3))
        cursor = i + len(f)
    out.append(round(fin[-1], 3))
    return out


def voz(clave):
    api = os.environ.get("ELEVENLABS_API_KEY")
    if not api:
        raise SystemExit("falta ELEVENLABS_API_KEY en el entorno")
    os.makedirs(VOZ_DIR, exist_ok=True)
    tiempos = leer_tiempos()
    for d in laminas(clave):
        mp3 = os.path.join(VOZ_DIR, "s%02d.mp3" % d["n"])
        if d["n"] in tiempos and os.path.exists(mp3):
            print("lámina %02d  ya locutada (%.2f s)" % (d["n"], tiempos[d["n"]][-1]))
            continue
        texto = normalizar(d["texto"])
        r = locutar(api, texto)
        io.open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
        tiempos[d["n"]] = inicios_de_frase(texto, [normalizar(f) for f in d["frases"]], r["alignment"])
        io.open(TIEMPOS, "w", encoding="utf-8", newline="\n").write(
            json.dumps({str(k): v for k, v in sorted(tiempos.items())}, indent=1))
        print("lámina %02d  %6.2f s  (%d frases)" % (d["n"], tiempos[d["n"]][-1], len(d["frases"])))


# ---------------------------------------------------------------- construir

INDEX = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #F3F0E8; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #F3F0E8; }}
      .escena {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
         data-width="1920" data-height="1080">
{escenas}
{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def estimar(d):
    """Sin locución: 0,068 s por carácter, repartido por frase (ajuste de Ruta Segura)."""
    t, ini = 0.0, []
    for f in d["frases"]:
        ini.append(round(t, 3))
        t += 0.06786 * len(f) + 0.374
    ini.append(round(t, 3))
    return ini


def plan(clave):
    tiempos = leer_tiempos()
    t, out = 0.0, []
    for d in laminas(clave):
        ini = tiempos.get(d["n"]) or estimar(d)
        if len(ini) > len(d["frases"]) + 1:
            # locutada con la pausa incluida: se usa hasta donde empieza la pregunta
            ini = ini[:len(d["frases"])] + [ini[len(d["frases"])] - 0.15]
        narr = ini[-1]
        dur = round(ANTES + narr + COLA, 2)
        out.append({"d": d, "inicios": [round(x + ANTES, 3) for x in ini[:-1]], "narracion": ANTES + narr,
                    "dur": dur, "inicio": round(t, 3), "voz": d["n"] in tiempos})
        t += dur
    return out, round(t, 2)


OBJETIVO = 60.0     # cada video del módulo dura alrededor de un minuto


def tramos(escenas):
    """Reparte las láminas del módulo en videos de ~1 minuto, sin cortar ninguna.

    No es un minuto exacto: se elige el reparto cuya suma de desviaciones al
    minuto sea menor, con uno a tres láminas por video. Así cada entrega es una
    sección completa y no un corte a mitad de explicación.
    """
    n = len(escenas)
    mejor = [None] * (n + 1)
    mejor[0] = (0.0, [])
    for i in range(1, n + 1):
        for k in range(1, min(3, i) + 1):
            if mejor[i - k] is None:
                continue
            dur = sum(e["dur"] for e in escenas[i - k:i])
            coste = mejor[i - k][0] + (dur - OBJETIVO) ** 2
            if mejor[i] is None or coste < mejor[i][0]:
                mejor[i] = (coste, mejor[i - k][1] + [escenas[i - k:i]])
    return mejor[n][1]


def escribir_index(ruta, escenas, desde, hasta, audio=""):
    filas = ['      <div id="el-%s" class="escena" data-composition-id="%s"\n'
             '           data-composition-src="compositions/%s.html"\n'
             '           data-start="%g" data-duration="%g" data-track-index="1"></div>'
             % (e["cid"], e["cid"], e["cid"], round(e["inicio"] - desde, 3), e["dur"]) for e in escenas]
    io.open(ruta, "w", encoding="utf-8", newline="\n").write(
        INDEX.format(total=round(hasta - desde, 3), escenas="\n".join(filas), audio=audio))


def construir(clave, con_tramos=False):
    dest = os.path.join(VIDEOS, "moto-" + clave)
    comp = os.path.join(dest, "compositions")
    os.makedirs(comp, exist_ok=True)
    os.makedirs(os.path.join(dest, "assets", "fotos"), exist_ok=True)
    for sub in ("fonts", "marca"):
        src = os.path.join(CURSO, "assets", sub)
        shutil.copytree(src, os.path.join(dest, "assets", sub), dirs_exist_ok=True)
    for f in ("package.json", "hyperframes.json", "CLAUDE.md", "AGENTS.md"):
        src = os.path.join(VIDEOS, "ruta-segura-m4", f)
        if os.path.exists(src) and not os.path.exists(os.path.join(dest, f)):
            s = io.open(src, encoding="utf-8").read().replace("ruta-segura-m4", "moto-" + clave)
            io.open(os.path.join(dest, f), "w", encoding="utf-8", newline="\n").write(s)
    io.open(os.path.join(dest, "meta.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"id": "moto-" + clave, "name": "moto-" + clave}, indent=2))
    for p in glob.glob(os.path.join(comp, "*.html")):
        os.remove(p)

    escenas, total = plan(clave)
    for e in escenas:
        d = e["d"]
        foto = os.path.join(CURSO, "assets", "fotos", "l%02d.jpg" % d["n"])
        if os.path.exists(foto):
            shutil.copy(foto, os.path.join(dest, "assets", "fotos"))
        tipo, fn = plantillas.elegir(d)
        ctx = {"frases": d["frases"], "inicios": e["inicios"], "narracion": e["narracion"], "dur": e["dur"]}
        css, cuerpo, tl = fn(d, ctx)
        cid = "l%02d-%s" % (d["n"], tipo)
        e["cid"] = cid
        html = base.envoltura(cid, e["dur"], css, cuerpo.replace("{d}", "%g" % e["dur"]), tl)
        io.open(os.path.join(comp, cid + ".html"), "w", encoding="utf-8", newline="\n").write(html)
        print("%-18s inicia %7.2f  dura %6.2f  %s" % (cid, e["inicio"], e["dur"], "voz" if e["voz"] else "estimada"))

    for p in glob.glob(os.path.join(dest, "index-parte-*.html")):
        os.remove(p)
    escribir_index(os.path.join(dest, "index.html"), escenas, 0.0, total)
    print("TOTAL %.2f s = %d:%02d" % (total, int(total // 60), int(round(total % 60)) % 60))

    # Los index-parte-N.html son insumos del render: con ellos presentes `lint`
    # ve varias raíces y falla, así que se escriben después de validar.
    if not con_tramos:
        return
    for k, g in enumerate(tramos(escenas), 1):
        desde, hasta = g[0]["inicio"], round(g[-1]["inicio"] + g[-1]["dur"], 3)
        escribir_index(os.path.join(dest, "index-parte-%d.html" % k), g, desde, hasta)
        print("  video %d  %5.1f s  láminas %s" % (k, hasta - desde, ", ".join(str(e["d"]["n"]) for e in g)))


# ---------------------------------------------------------------- montar

def pista_de(g, destino):
    """Voz del tramo, con cada lámina en su sitio dentro de ese video."""
    origen = g[0]["inicio"]
    dur = round(g[-1]["inicio"] + g[-1]["dur"] - origen, 3)
    entradas, filtros = [], []
    for k, e in enumerate(g):
        mp3 = os.path.join(VOZ_DIR, "s%02d.mp3" % e["d"]["n"])
        if not os.path.exists(mp3):
            raise SystemExit("falta la voz de la lámina %d" % e["d"]["n"])
        ms = int((e["inicio"] - origen + ANTES) * 1000)
        entradas += ["-i", mp3]
        filtros.append("[%d:a]atrim=0:%.3f,aresample=44100,adelay=%d|%d[v%d]"
                       % (k, e["narracion"] - ANTES, ms, ms, k))
    cadena = ";".join(filtros) + ";" + "".join("[v%d]" % k for k in range(len(g)))
    cadena += ("amix=inputs=%d:normalize=0,apad,atrim=0:%s,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[out]"
               % (len(g), dur))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y"] + entradas +
                          ["-filter_complex", cadena, "-map", "[out]", "-ac", "1",
                           "-c:a", "libmp3lame", "-b:a", "128k", destino])
    return dur


def montar(clave):
    """Un MP4 narrado por tramo: el módulo se entrega en videos de ~1 minuto."""
    dest = os.path.join(VIDEOS, "moto-" + clave)
    renders = os.path.join(dest, "renders")
    escenas, _ = plan(clave)
    hechos = []
    for k, g in enumerate(tramos(escenas), 1):
        mudo = os.path.join(renders, "parte-%d.mp4" % k)
        if not os.path.exists(mudo):
            print("falta renders/parte-%d.mp4 — corre antes tools/render-partes.py" % k)
            continue
        pista = os.path.join(dest, "assets", "voz", "tramo-%d.mp3" % k)
        dur = pista_de(g, pista)
        dv = duracion(mudo)
        if abs(dv - dur) > 0.6:
            raise SystemExit("el video %d mide %.2f s y su tramo %.2f s: el render no es de esta construcción"
                             % (k, dv, dur))
        final = os.path.join(renders, "moto-%s-%d.mp4" % (clave, k))
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mudo, "-i", pista,
                               "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
                               "-b:a", "160k", "-movflags", "+faststart", "-shortest", final])
        hechos.append(final)
        print("%s  %.1f MB  %.1f s" % (os.path.basename(final), os.path.getsize(final) / 1e6, duracion(final)))
    if len(hechos) == len(tramos(escenas)):
        for p in glob.glob(os.path.join(dest, "index-parte-*.html")):
            os.remove(p)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[2] not in LIMITES:
        raise SystemExit("uso: moto.py voz|construir|montar <%s> [--tramos]" % "|".join(LIMITES))
    accion, clave = sys.argv[1], sys.argv[2]
    if accion == "voz":
        voz(clave)
    elif accion == "construir":
        construir(clave, "--tramos" in sys.argv)
    elif accion == "montar":
        montar(clave)
    else:
        raise SystemExit("acción desconocida: " + accion)
