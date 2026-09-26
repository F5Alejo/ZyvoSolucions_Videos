# -*- coding: utf-8 -*-
"""RiskMann · Modulo Capacitaciones — promo vertical 9:16 (~35 s).

FUENTE UNICA DEL CONTENIDO: riskmann.com/capacitaciones (captura del 26-sep-2026 en
"landig page capacitaciones/"). Cada frase de la voz y cada texto en pantalla sale
de esa pagina; la columna "fuente" de GUION lo dice. Sin cifras inventadas.
IDENTIDAD: la de la landing (decision del cliente, 26-sep): negro #040404/#0A0A0A,
dorado #AC841D, Montserrat (titulos) + Open Sans (texto). Logo: archivo oficial
assets/public/riskmann_logo_blanco.png. QR: el oficial qr-app-riskmann-com
(-> https://app.riskmann.com/entrada), sin redibujar.

    python tools/construir.py voz          # locucion ElevenLabs (Carlos, semilla fija)
    python tools/construir.py musica       # cama + efectos (ElevenLabs), una vez
    python tools/construir.py construir    # index.html + compositions/ desde los tiempos reales
    python tools/construir.py              # todo lo que falte

Despues de construir, la fuente editable es index.html + compositions/ (Studio).
Volver a construir las reescribe.
"""
import base64, html, io, json, os, re, shutil, subprocess, sys, urllib.request, urllib.error

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(RAIZ, "assets", *p)
VOZ_ID, MODELO, SEMILLA = "4PN5DHmrfIgZksvIrawS", "eleven_multilingual_v2", 20261003
AJUSTES = {"stability": 0.33, "similarity_boost": 0.85, "style": 0.45, "use_speaker_boost": True, "speed": 1.05}

# (texto para la voz, marcas = fragmentos cuyo instante se mide, fuente en la landing)
GUION = [
  ("La capacitación ocurrió... ¿Pero puedes demostrarlo?", ["La capacitación", "¿Pero puedes"],
   "hero: «La capacitación ocurrió. ¿Pero puedes demostrarlo?»"),
  ("Una lista firmada en papel no alcanza. Un certificado en Word, tampoco.", ["Una lista", "Un certificado"],
   "hero: «Una lista firmada en papel no alcanza. Un certificado en Word tampoco.»"),
  ("Armas el curso con videos de YouTube, pe de efe o Google Drive.",
   ["Armas", "YouTube", "pe de efe", "Google Drive"],
   "paso 1: «Agrega videos de YouTube, documentos PDF o archivos de Google Drive»"),
  ("Tu gente lo toma desde el celular o el computador.", ["Tu gente", "desde el celular"],
   "paso 2: «Tu gente lo toma cuando puede. Desde el celular o el computador»"),
  ("La plataforma califica sola.", ["La plataforma"], "paso 3: «La plataforma califica sola»"),
  ("Y queda el certificado en pe de efe, con nombre, documento, curso y fecha.",
   ["Y queda", "con nombre", "documento", "curso y", "fecha"],
   "paso 4: «Un PDF con el nombre y el documento de la persona, el curso y la fecha de aprobación»"),
  ("Quién aprobó, quién reprobó, quién está pendiente... todo en Excel.",
   ["Quién aprobó", "quién reprobó", "quién está", "todo en Excel"],
   "«el registro se arma solo» + Reportes en Excel: «quién aprobó, quién reprobó, quién está pendiente»"),
  ("Todo con la misma cuenta de RiskMann.", ["Todo con"], "«Todo con la misma cuenta de RiskMann»"),
  ("Actívalo gratis hasta el primero de enero de dos mil veintisiete.", ["Actívalo", "hasta el primero"],
   "«Módulo Capacitaciones · Gratis hasta el 1 de enero de 2027» + botón «Activar ahora»"),
  ("Deja de capacitar con papel y Word.", ["Deja de"], "cierre: «Deja de capacitar con papel y Word.»"),
]
# escena -> frases que la componen
ESCENAS = [("gancho", [1]), ("problema", [2]), ("armar", [3]), ("tomar", [4]),
           ("certificado", [5, 6]), ("registro", [7, 8]), ("cierre", [9, 10])]
GAP_FRASE, GAP_ESCENA, ANTES, COLA = 0.28, 0.65, 0.30, 1.4

MUSICA_PROMPT = ("Modern elegant corporate technology background music, 112 BPM, confident and optimistic, "
                 "warm synth pads, soft plucks, light punchy drums, premium feel, no vocals, instrumental only.")
SFX = {  # nombre: (prompt, duracion)
    "whoosh": ("smooth soft airy whoosh transition, short, clean, no music", 1.0),
    "pop": ("soft bubbly UI pop, friendly, short, no music", 0.5),
    "golpe": ("warm deep cinematic low hit with short tail, subtle, no music", 1.5),
    "papel": ("sheet of paper being crumpled quickly, short, no music", 0.9),
    "visto": ("quick pen check mark stroke swoosh on paper, crisp, no music", 0.8),
    "brillo": ("gentle magical shimmer chime reveal, bright, short, no music", 1.6),
    "tecla": ("soft single computer key click, short, no music", 0.5),
}


# ------------------------------------------------------------------ ElevenLabs
def clave():
    f = os.path.join(os.path.expanduser("~"), ".elevenlabs-key.txt")
    k = os.environ.get("ELEVENLABS_API_KEY") or (io.open(f, encoding="utf-8-sig").read().strip() if os.path.isfile(f) else "")
    if not k.startswith("sk_"):
        raise SystemExit("falta la clave de ElevenLabs (sk_...)")
    return k


def pedir(ruta, cuerpo):
    req = urllib.request.Request("https://api.elevenlabs.io/v1" + ruta, data=json.dumps(cuerpo).encode("utf-8"),
                                 method="POST", headers={"xi-api-key": clave(), "Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=600).read()
    except urllib.error.HTTPError as e:
        raise SystemExit("ElevenLabs %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)


def integrado(f):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def nivelar(src, dst, lufs=-16):
    tmp = dst + ".tmp.wav"
    ff("-i", src, "-af", "aresample=48000", "-ac", "2", "-ar", "48000", tmp)
    ff("-i", tmp, "-af", "volume=%.2fdB,alimiter=limit=0.89" % (lufs - integrado(tmp)), "-ar", "48000", dst)
    os.remove(tmp)


def voz(solo=None):
    os.makedirs(A("voz"), exist_ok=True); os.makedirs(A("mezcla"), exist_ok=True)
    ruta = os.path.join(RAIZ, "tools", "tiempos-voz.json")
    previos = {x["n"]: x for x in json.load(io.open(ruta, encoding="utf-8"))} if os.path.isfile(ruta) else {}
    tiempos = []
    for n, (texto, marcas, fuente) in enumerate(GUION, 1):
        if (solo and n not in solo) or (not solo and n in previos and previos[n]["texto"] == texto):
            tiempos.append(previos[n]); continue
        d = json.loads(pedir("/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % VOZ_ID,
                             {"text": texto, "model_id": MODELO, "voice_settings": AJUSTES, "seed": SEMILLA}))
        open(A("voz", "f%02d.mp3" % n), "wb").write(base64.b64decode(d["audio_base64"]))
        ini, fin = d["alignment"]["character_start_times_seconds"], d["alignment"]["character_end_times_seconds"]
        tiempos.append({"n": n, "texto": texto, "fuente": fuente, "dur": round(fin[-1], 3),
                        "marcas": {m: round(ini[texto.index(m)], 3) for m in marcas}})
        nivelar(A("voz", "f%02d.mp3" % n), A("mezcla", "voz-%d.wav" % n))
        print("f%02d  %.2f s  %s" % (n, fin[-1], texto))
    io.open(ruta, "w", encoding="utf-8", newline="\n").write(json.dumps(tiempos, ensure_ascii=False, indent=1))


def musica():
    os.makedirs(A("musica"), exist_ok=True); os.makedirs(A("sfx"), exist_ok=True)
    if not os.path.isfile(A("musica", "cama.mp3")):
        # sin permiso de Eleven Music: generacion de sonido en bucle (22 s) y se encadena
        open(A("musica", "cama-22s.mp3"), "wb").write(pedir("/sound-generation", {
            "text": MUSICA_PROMPT, "duration_seconds": 22, "prompt_influence": 0.55, "loop": True}))
        ff("-stream_loop", "2", "-i", A("musica", "cama-22s.mp3"), "-t", "60", "-b:a", "192k", A("musica", "cama.mp3"))
        io.open(A("musica", "ORIGEN.txt"), "w", encoding="utf-8").write(
            "cama.mp3: ElevenLabs sound-generation en bucle (22 s x3). Prompt:\n" + MUSICA_PROMPT + "\n")
    for n, (prompt, dur) in SFX.items():
        if not os.path.isfile(A("sfx", n + ".mp3")):
            open(A("sfx", n + ".mp3"), "wb").write(pedir("/sound-generation", {
                "text": prompt, "duration_seconds": dur, "prompt_influence": 0.6}))
            print("sfx", n)


# ------------------------------------------------------------------ plantillas
FUENTES = '''        @font-face { font-family: "Montserrat"; font-weight: 100 900; font-display: block;
          src: url("assets/fonts/montserrat-latin-ext.woff2") format("woff2");
          unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1E00-1E9F, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
        @font-face { font-family: "Montserrat"; font-weight: 100 900; font-display: block;
          src: url("assets/fonts/montserrat-latin.woff2") format("woff2");
          unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
''' + "".join('''        @font-face { font-family: "Open Sans"; font-weight: %s; font-display: block;
          src: url("assets/fonts/open-sans-latin-%s.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+2000-206F, U+20AC, U+2122, U+FEFF; }
        @font-face { font-family: "Open Sans"; font-weight: %s; font-display: block;
          src: url("assets/fonts/open-sans-latin-ext-%s.woff2") format("woff2"); unicode-range: U+0100-02BA, U+1E00-1E9F, U+2C60-2C7F, U+A720-A7FF; }
''' % (w, w, w, w) for w in (400, 600, 700))

BASE_CSS = '''        #root {
          position: absolute; inset: 0; overflow: hidden; background: transparent;
          font-family: "Open Sans", sans-serif; color: #fff;
          --negro: #040404; --negro2: #0A0A0A; --tarjeta: #121212; --borde: #262626;
          --dorado: #AC841D; --dorado-claro: #d9b04a; --gris: #F5F5F5; --texto2: #b9b9b9; --marino: #192744;
        }
        .t { font-family: "Montserrat", sans-serif; font-weight: 800; letter-spacing: -0.02em; line-height: 1.12; }
        .oro { color: var(--dorado-claro); }
        .l { display: block; overflow: hidden; padding-bottom: 6px; }
        .l > span { display: inline-block; }
        #c { position: absolute; inset: 0; }
        .card { background: linear-gradient(160deg, #161616, #0e0e0e); border: 1px solid var(--borde); border-radius: 28px;
          box-shadow: 0 30px 70px rgba(0,0,0,0.55); }
        .chip { display: inline-flex; align-items: center; gap: 14px; padding: 14px 30px; border-radius: 100px;
          border: 1px solid rgba(172,132,29,0.55); background: rgba(172,132,29,0.10); color: var(--dorado-claro);
          font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; text-transform: uppercase; }
        .num { width: 64px; height: 64px; border-radius: 50%; border: 2px solid var(--dorado); color: var(--dorado-claro);
          display: flex; align-items: center; justify-content: center; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 30px;
          background: rgba(172,132,29,0.12); flex-shrink: 0; }
'''


def sub(cid, css, cuerpo, js):
    return '''<!doctype html>
<html lang="es">
  <head><meta charset="UTF-8"><title>%s</title></head>
  <body>
    <template>
      <style>
%s%s%s
      </style>
      <div id="root" data-composition-id="%s" data-width="1080" data-height="1920">
        <div id="c">
%s
        </div>
      </div>
      <script>
      (function () {
        window.__timelines = window.__timelines || {};
        var tl = gsap.timeline({ paused: true });
%s
        window.__timelines["%s"] = tl;
      })();
      </script>
    </template>
  </body>
</html>
''' % (cid, FUENTES, BASE_CSS, css.replace("%%", "%"), cid, cuerpo, js, cid)


def lineas(txt_lineas, clase=""):
    return "\n".join('          <div class="l %s"><span>%s</span></div>' % (clase, x) for x in txt_lineas)


# ------------------------------------------------------------------ construir
def construir():
    t = {x["n"]: x for x in json.load(io.open(os.path.join(RAIZ, "tools", "tiempos-voz.json"), encoding="utf-8"))}
    # --- colocacion: cada frase detras de la anterior; hueco mayor al cambiar de escena
    primera = {fr[0] for _, fr in ESCENAS}
    V, cur = {}, ANTES + 0.2
    for n in range(1, len(GUION) + 1):
        if n > 1:
            cur = V[n - 1] + t[n - 1]["dur"] + (GAP_ESCENA if n in primera else GAP_FRASE)
        V[n] = round(cur, 2)
    FIN = round(V[len(GUION)] + t[len(GUION)]["dur"] + COLA, 1)
    M = lambda n, k: round(V[n] + t[n]["marcas"][k], 3)          # instante global de una marca
    S = {}
    for i, (nombre, fr) in enumerate(ESCENAS):
        S[nombre] = 0.0 if i == 0 else round(V[fr[0]] - ANTES, 2)
    nombres = [e for e, _ in ESCENAS]
    FINES = {e: (S[nombres[i + 1]] if i + 1 < len(nombres) else FIN) for i, e in enumerate(nombres)}
    for i in range(1, len(nombres)):   # la escena anterior termina su frase antes de irse
        ult = ESCENAS[i - 1][1][-1]
        assert V[ult] + t[ult]["dur"] <= FINES[nombres[i - 1]] - 0.35 + 0.02, (nombres[i - 1],)   # sale (0.35 s) tras acabar la frase

    def cab(e, extra=()):
        js = ["        /* TIEMPOS globales (s), de tools/tiempos-voz.json. S = data-start de esta escena en index.html;",
              "           si la mueves en el Studio, cambia S. FINE = cuando esta escena cede el paso. */",
              "        var S = %s, FINE = %s;" % (S[e], FINES[e]),
              "        var L = function (g) { return g - S; };"]
        js += ["        var %s = %s;   // %s" % (k, v, c) for k, v, c in extra]
        # salida comun: el contenido sube y se desvanece (power2.in), ultima escena no sale
        return "\n".join(js) + "\n"
    SALIDA = '''
        if (FINE - S < 900) tl.to("#c", { opacity: 0, y: -90, duration: 0.35, ease: "power2.in" }, L(FINE) - 0.35);'''
    comps = {}

    # ===== 1 · gancho
    comps["gancho"] = ('''        #t1 { position: absolute; left: 108px; top: 640px; width: 864px; font-size: 104px; }
        #t2 { position: absolute; left: 108px; top: 930px; width: 864px; font-size: 104px; }
        #sub { position: absolute; left: 108px; top: 1250px; width: 864px; font-size: 34px; color: var(--texto2); line-height: 1.5; }
''', '''          <div id="t1" class="t">
%s
          </div>
          <div id="t2" class="t oro">
%s
          </div>''' % (lineas(["La capacitación", "ocurrió."]), lineas(["¿Pero puedes", "demostrarlo?"])),
        cab("gancho", [("a", M(1, "La capacitación"), "'La capacitación'"), ("b", M(1, "¿Pero puedes"), "'¿Pero puedes'")]) + '''
        tl.fromTo("#t1 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.16 }, L(a) - 0.05);
        tl.fromTo("#t2 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.16 }, L(b) - 0.05);
        tl.fromTo("#t2", { textShadow: "0 0 0px rgba(217,176,74,0)" }, { textShadow: "0 0 46px rgba(217,176,74,0.55)", duration: 0.6, ease: "power2.out" }, L(b) + 0.4);
        tl.to("#t2", { textShadow: "0 0 18px rgba(217,176,74,0.25)", duration: 1.0, ease: "sine.inOut" }, L(b) + 1.0);''' + SALIDA)

    # ===== 2 · problema: la hoja de asistencia y el Word, tachados
    filas = "\n".join('''              <div class="fila"><span class="lin"></span><span class="firma"></span></div>''' for _ in range(5))
    comps["problema"] = ('''        #hoja { position: absolute; left: 150px; top: 330px; width: 520px; height: 640px; background: #efece4; border-radius: 10px;
          box-shadow: 0 30px 70px rgba(0,0,0,0.6); padding: 44px 40px; color: #3a3a3a; transform: rotate(-5deg); }
        #hoja h4 { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 26px; letter-spacing: 0.08em; margin-bottom: 30px; }
        .fila { display: flex; gap: 18px; align-items: flex-end; height: 86px; border-bottom: 2px solid #c9c3b3; }
        .lin { flex: 1; height: 10px; background: #d7d1c2; border-radius: 5px; margin-bottom: 18px; }
        .firma { width: 150px; height: 34px; border-bottom: 3px solid #5a5a8a; border-radius: 0 0 60% 40%; margin-bottom: 14px; transform: skewX(-20deg); }
        #word { position: absolute; left: 560px; top: 560px; width: 380px; height: 470px; background: #fff; border-radius: 10px;
          box-shadow: 0 30px 70px rgba(0,0,0,0.6); transform: rotate(6deg); overflow: hidden; }
        #word .barra { height: 70px; background: #2b579a; color: #fff; font-family: "Open Sans"; font-weight: 700; font-size: 26px; display: flex; align-items: center; padding-left: 26px; }
        #word .cuerpo { padding: 40px 30px; color: #333; font-family: "Open Sans"; }
        #word .cuerpo b { display: block; text-align: center; font-size: 30px; letter-spacing: 0.06em; margin-bottom: 26px; }
        #word .cuerpo i { display: block; height: 12px; background: #dcdcdc; border-radius: 6px; margin: 16px 0; }
        .tacha { position: absolute; height: 10px; background: var(--dorado-claro); border-radius: 5px; transform-origin: left center;
          box-shadow: 0 0 24px rgba(217,176,74,0.7); }
        #x1 { left: 110px; top: 640px; width: 640px; transform: rotate(-35deg) scaleX(0); }
        #x2 { left: 520px; top: 900px; width: 480px; transform: rotate(-30deg) scaleX(0); }
        #f1 { position: absolute; left: 108px; top: 1170px; width: 864px; font-size: 64px; }
        #f2 { position: absolute; left: 108px; top: 1370px; width: 864px; font-size: 64px; }
''', '''          <div id="hoja"><h4>LISTA DE ASISTENCIA</h4>
%s
          </div>
          <div id="word"><div class="barra">Certificado.docx</div>
            <div class="cuerpo"><b>CERTIFICADO</b><i></i><i style="width:80%%"></i><i></i><i style="width:60%%"></i></div></div>
          <div id="x1" class="tacha"></div>
          <div id="x2" class="tacha"></div>
          <div id="f1" class="t">
%s
          </div>
          <div id="f2" class="t">
%s
          </div>''' % (filas, lineas(["Una lista firmada en papel", '<span class="oro">no alcanza.</span>']),
                        lineas(["Un certificado en Word,", '<span class="oro">tampoco.</span>'])),
        cab("problema", [("a", M(2, "Una lista"), "'Una lista'"), ("b", M(2, "Un certificado"), "'Un certificado'")]) + '''
        tl.fromTo("#hoja", { opacity: 0, y: 120, rotation: -14 }, { opacity: 1, y: 0, rotation: -5, duration: 0.8, ease: "back.out(1.3)" }, L(a) - 0.1);
        tl.fromTo("#f1 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a));
        tl.fromTo("#x1", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, L(b) - 0.55);
        tl.to("#hoja", { opacity: 0.35, duration: 0.4, ease: "power2.out" }, L(b) - 0.3);
        tl.fromTo("#word", { opacity: 0, x: 200, rotation: 18 }, { opacity: 1, x: 0, rotation: 6, duration: 0.8, ease: "back.out(1.3)" }, L(b) - 0.05);
        tl.fromTo("#f2 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(b));
        tl.fromTo("#x2", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, L(FINE) - 0.75);
        tl.to("#word", { opacity: 0.35, duration: 0.3, ease: "power2.out" }, L(FINE) - 0.6);''' + SALIDA)

    # ===== 3 · armar el curso (paso 1)
    fuentesF = [("YouTube", "video", "YouTube"), ("PDF", "pdf", "documentos"), ("Google Drive", "drive", "Google Drive")]
    iconos = {
        "video": '<svg viewBox="0 0 80 80"><rect x="8" y="16" width="64" height="48" rx="12" fill="none" stroke="currentColor" stroke-width="5"/><path d="M34 30 L52 40 L34 50 Z" fill="currentColor"/></svg>',
        "pdf": '<svg viewBox="0 0 80 80"><path d="M20 8 H48 L62 22 V72 H20 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><path d="M48 8 V22 H62" fill="none" stroke="currentColor" stroke-width="5"/><text x="41" y="56" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="17" fill="currentColor">PDF</text></svg>',
        "drive": '<svg viewBox="0 0 80 80"><path d="M10 26 H32 L38 32 H70 V66 H10 Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/></svg>'}
    tiles = "\n".join('''            <div class="tile" id="tile%d"><div class="ico">%s</div><span>%s</span></div>''' % (i, iconos[k], nom)
                      for i, (nom, k, _) in enumerate(fuentesF, 1))
    comps["armar"] = ('''        #cab { position: absolute; left: 108px; top: 500px; width: 864px; display: flex; align-items: center; gap: 24px; }
        #cab .t { font-size: 58px; }
        #desc { position: absolute; left: 108px; top: 620px; width: 864px; font-size: 36px; color: var(--texto2); line-height: 1.45; }
        #tiles { position: absolute; left: 108px; top: 820px; width: 864px; display: flex; flex-direction: column; gap: 26px; }
        .tile { display: flex; align-items: center; gap: 34px; padding: 30px 40px; font-family: "Montserrat"; font-weight: 700; font-size: 46px; }
        .tile .ico { width: 96px; height: 96px; color: var(--dorado-claro); flex-shrink: 0; }
        .tile .ico svg { width: 100%%; height: 100%%; }
        #curso { position: absolute; left: 108px; top: 1420px; width: 864px; padding: 34px 40px; font-family: "Montserrat"; font-weight: 800;
          font-size: 40px; color: #111; background: linear-gradient(135deg, #c99a2a, #AC841D); border-radius: 22px; text-align: center;
          box-shadow: 0 24px 60px rgba(172,132,29,0.35); }
''', '''          <div id="cab"><div class="num">1</div><div class="t">Armas el curso</div></div>
          <div id="desc">Organizado en módulos fáciles de seguir.</div>
          <div id="tiles">
%s
          </div>''' % tiles.replace('class="tile"', 'class="tile card"'),
        cab("armar", [("a", M(3, "Armas"), "'Armas el curso'"), ("y1", M(3, "YouTube"), "'YouTube'"),
                      ("y2", M(3, "pe de efe"), "'pe de efe'"), ("y3", M(3, "Google Drive"), "'Google Drive'")]) + '''
        tl.fromTo("#cab", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.6, ease: "expo.out" }, L(a) - 0.1);
        tl.fromTo("#desc", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(a) + 0.25);
        tl.fromTo("#tile1", { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.55, ease: "back.out(1.6)" }, L(y1) - 0.1);
        tl.fromTo("#tile2", { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.55, ease: "back.out(1.6)" }, L(y2) - 0.1);
        tl.fromTo("#tile3", { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.55, ease: "back.out(1.6)" }, L(y3) - 0.1);
''' + SALIDA)

    # ===== 4 · tomarlo cuando pueda (paso 2) — foto real + maqueta real de dispositivos
    comps["tomar"] = ('''        #foto { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
        #foto img { position: absolute; left: -900px; top: 0; height: 1920px; width: auto;
          filter: grayscale(0.5) sepia(0.3) brightness(0.72) contrast(1.08); }
        #velo { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(4,4,4,0.35) 0%, rgba(4,4,4,0.55) 45%, rgba(4,4,4,0.96) 72%, #040404 100%); }
        #cab { position: absolute; left: 108px; top: 1160px; width: 864px; display: flex; align-items: center; gap: 24px; }
        #cab .t { font-size: 56px; }
        #desc { position: absolute; left: 108px; top: 1340px; width: 864px; font-size: 38px; color: #e6e6e6; line-height: 1.45; }
        #disp { position: absolute; left: 180px; top: 1470px; width: 720px; height: auto; }
''', '''          <div id="foto"><img src="assets/img/capacitaciones_imagen_cabecera.webp" alt=""></div>
          <div id="velo"></div>
          <div id="cab"><div class="num">2</div><div class="t">Tu gente lo toma<br>cuando puede</div></div>
          <div id="desc">Desde el celular o el computador, con su cuenta de RiskMann.</div>''',
        cab("tomar", [("a", M(4, "Tu gente"), "'Tu gente'"), ("b", M(4, "desde el celular"), "'desde el celular'")]) + '''
        tl.fromTo("#foto img", { scale: 1.12, x: 0 }, { scale: 1.0, x: 60, duration: FINE - S, ease: "none" }, 0);
        tl.fromTo("#foto", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 0);
        tl.fromTo("#cab", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, L(a) - 0.1);
        tl.fromTo("#desc", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(b) - 0.15);''' + SALIDA)
    # la maqueta de dispositivos es de otra landing de RiskMann: se deja fuera para no mezclar

    # ===== 5 · califica sola + certificado (pasos 3 y 4)
    comps["certificado"] = ('''        #cab3 { position: absolute; left: 108px; top: 300px; width: 864px; display: flex; align-items: center; gap: 24px; }
        #cab3 .t { font-size: 52px; }
        #nota { position: absolute; left: 50%%; top: 440px; transform: translateX(-50%%); display: flex; align-items: center; gap: 18px;
          padding: 20px 40px; border-radius: 18px; background: #fff; color: #111; font-family: "Montserrat"; font-weight: 800; font-size: 36px; white-space: nowrap;
          box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        #nota .ok { width: 50px; height: 50px; border-radius: 50%%; background: var(--dorado); display: flex; align-items: center; justify-content: center; }
        #nota svg { width: 30px; height: 30px; }
        #cert { position: absolute; left: 110px; top: 620px; width: 860px; height: 700px; background: #fff; color: #1a1a1a; border-radius: 14px;
          box-shadow: 0 40px 90px rgba(0,0,0,0.6); padding: 50px 60px; text-align: center; }
        #cert .marco { position: absolute; inset: 18px; border: 2px solid #e2e2e2; border-radius: 8px; }
        #cert img { height: 64px; width: auto; margin-bottom: 18px; }   /* logo oficial a color, sin filtros */
        #cert h3 { font-family: "Montserrat"; font-weight: 800; font-size: 50px; letter-spacing: 0.06em; margin-bottom: 8px; }
        #cert .p { display: block; font-size: 22px; color: #666; margin: 6px 0; }
        #cert .campo { display: block; width: fit-content; margin-left: auto !important; margin-right: auto !important; font-family: "Montserrat"; font-weight: 800; font-size: 34px; padding: 4px 16px; border-radius: 8px; margin: 6px 0; }
        #cert .linea { width: 360px; height: 2px; background: #999; margin: 26px auto 8px; }
        .luz { background: rgba(172,132,29,0); }
        #cab4 { position: absolute; left: 108px; top: 1420px; width: 864px; display: flex; align-items: center; gap: 24px; }
        #cab4 .t { font-size: 50px; }
        #pdf { position: absolute; left: 108px; top: 1540px; width: 864px; font-size: 36px; color: var(--texto2); line-height: 1.45; }
''', '''          <div id="cab3"><div class="num">3</div><div class="t">La plataforma califica sola</div></div>
          <div id="nota"><span class="ok"><svg viewBox="0 0 30 30"><path id="chk" d="M6 16 L12 22 L24 8" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Evaluación calificada</div>
          <div id="cert"><div class="marco"></div>
            <img src="assets/logo/riskmann_logo_color.png" alt="RiskMann">
            <h3>CERTIFICADO</h3>
            <div class="p">concedido a</div>
            <div class="campo luz" id="k1">NOMBRE DEL TRABAJADOR</div>
            <div class="p campo luz" id="k2" style="font-size:24px;font-family:'Open Sans';font-weight:600">Documento de identidad</div>
            <div class="p">por haber concluido de manera satisfactoria la capacitación:</div>
            <div class="campo luz" id="k3" style="font-size:30px">CAPACITACIÓN PARA CICLISTAS</div>
            <div class="p campo luz" id="k4" style="font-size:24px;font-family:'Open Sans';font-weight:600">Fecha de aprobación</div>
            <div class="linea"></div><div class="p">Representante legal · SOFU</div>
          </div>
          <div id="cab4"><div class="num">4</div><div class="t">Queda el certificado</div></div>
          <div id="pdf">Un PDF para cada persona que aprueba.</div>''',
        cab("certificado", [("a", M(5, "La plataforma"), "'La plataforma califica sola'"), ("b", M(6, "Y queda"), "'Y queda'"),
                            ("k1", M(6, "con nombre"), "'con nombre'"), ("k2", M(6, "documento"), "'documento'"),
                            ("k3", M(6, "curso y"), "'curso'"), ("k4", M(6, "fecha"), "'fecha'")]) + '''
        tl.fromTo("#cab3", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.6, ease: "expo.out" }, L(a) - 0.1);
        tl.fromTo("#nota", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.55, ease: "back.out(2)" }, L(a) + 0.35);
        tl.fromTo("#chk", { strokeDasharray: 40, strokeDashoffset: 40 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, L(a) + 0.6);
        tl.fromTo("#cert", { opacity: 0, y: 260, rotation: 8, scale: 0.85 }, { opacity: 1, y: 0, rotation: 0, scale: 1, duration: 0.9, ease: "back.out(1.3)" }, L(b) - 0.15);
        tl.fromTo("#cab4", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(b));
        ["#k1", "#k2", "#k3", "#k4"].forEach(function (sel, i) {
          var tk = [k1, k2, k3, k4][i];
          tl.fromTo(sel, { backgroundColor: "rgba(172,132,29,0)" }, { backgroundColor: "rgba(172,132,29,0.28)", duration: 0.25, ease: "power2.out" }, L(tk) - 0.05);
          tl.to(sel, { backgroundColor: "rgba(172,132,29,0.10)", duration: 0.6, ease: "power2.inOut" }, L(tk) + 0.35);
        });
        tl.fromTo("#pdf", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(k4) + 0.3);''' + SALIDA)

    # ===== 6 · el registro se arma solo + Excel + misma cuenta
    filasR = [("Colaborador 1", "Aprobó", "ap"), ("Colaborador 2", "Reprobó", "re"), ("Colaborador 3", "Pendiente", "pe")]
    trs = "\n".join('''            <div class="tr" id="r%d"><span class="nom">%s</span><span class="est %s">%s</span></div>''' % (i, a, c, b)
                    for i, (a, b, c) in enumerate(filasR, 1))
    comps["registro"] = ('''        #tit { position: absolute; left: 108px; top: 300px; width: 864px; font-size: 76px; }
        #tabla { position: absolute; left: 108px; top: 600px; width: 864px; padding: 20px 0; }
        .th, .tr { display: flex; justify-content: space-between; align-items: center; padding: 26px 40px; }
        .th { font-family: "Montserrat"; font-weight: 700; font-size: 24px; letter-spacing: 0.16em; color: var(--texto2); text-transform: uppercase; border-bottom: 1px solid var(--borde); }
        .tr { font-size: 38px; font-weight: 600; border-bottom: 1px solid #1c1c1c; }
        .est { font-family: "Montserrat"; font-weight: 800; font-size: 28px; padding: 10px 26px; border-radius: 100px; }
        .ap { background: rgba(172,132,29,0.9); color: #111; }
        .re { background: #2a2a2a; color: #eee; border: 1px solid #444; }
        .pe { background: transparent; color: var(--dorado-claro); border: 1px dashed var(--dorado); }
        #excel { position: absolute; left: 50%%; top: 1090px; transform: translateX(-50%%); display: flex; align-items: center; gap: 18px; white-space: nowrap;
          padding: 24px 44px; border-radius: 18px; background: var(--gris); color: #111; font-family: "Montserrat"; font-weight: 800; font-size: 36px; }
        #excel .x { width: 54px; height: 54px; border-radius: 10px; background: #1f6e43; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 30px; }
        #cuenta { position: absolute; left: 108px; top: 1400px; width: 864px; text-align: center; font-size: 58px; }
        #logo { position: absolute; left: 50%%; top: 1600px; width: 420px; margin-left: -210px; height: auto; }
''', '''          <div id="tit" class="t">
%s
          </div>
          <div id="tabla" class="card">
            <div class="th"><span>Colaborador</span><span>Resultado</span></div>
%s
          </div>
          <div id="excel"><span class="x">X</span>Reporte en Excel</div>
          <div id="cuenta" class="t">
%s
          </div>
          <img id="logo" src="assets/logo/riskmann_logo_blanco.png" alt="RiskMann">''' % (
            lineas(["El registro", '<span class="oro">se arma solo</span>']), trs, lineas(["Todo con la misma", 'cuenta de <span class="oro">RiskMann</span>'])),
        cab("registro", [("a", M(7, "Quién aprobó") - 0.35, "antes de 'Quién aprobó'"), ("r1", M(7, "Quién aprobó"), "'Quién aprobó'"),
                         ("r2", M(7, "quién reprobó"), "'quién reprobó'"), ("r3", M(7, "quién está"), "'quién está pendiente'"),
                         ("x", M(7, "todo en Excel"), "'todo en Excel'"), ("c", M(8, "Todo con"), "'Todo con la misma cuenta'")]) + '''
        tl.fromTo("#tit .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a) - 0.1);
        tl.fromTo("#tabla", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(a) + 0.3);
        tl.fromTo("#r1", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, L(r1) - 0.05);
        tl.fromTo("#r2", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, L(r2) - 0.05);
        tl.fromTo("#r3", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, L(r3) - 0.05);
        tl.fromTo("#excel", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.55, ease: "back.out(2)" }, L(x));
        tl.fromTo("#cuenta .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(c) - 0.05);
        tl.fromTo("#logo", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, L(c) + 0.5);''' + SALIDA)

    # ===== 7 · cierre: gratis hasta 2027, boton, QR oficial
    comps["cierre"] = ('''        #badge { position: absolute; left: 50%%; top: 300px; transform: translateX(-50%%); white-space: nowrap; font-size: 22px; }
        #gratis { position: absolute; left: 108px; top: 380px; width: 864px; text-align: center; font-size: 84px; }
        #fecha { position: absolute; left: 108px; top: 620px; width: 864px; text-align: center; font-family: "Montserrat"; font-weight: 700;
          font-size: 44px; color: var(--dorado-claro); }
        #boton { position: absolute; left: 50%%; top: 740px; transform: translateX(-50%%); white-space: nowrap; display: flex; align-items: center; gap: 18px;
          padding: 34px 60px; border-radius: 18px; background: linear-gradient(135deg, #AC841D, #8a6813); color: #fff;
          font-family: "Montserrat"; font-weight: 800; font-size: 42px; box-shadow: 0 26px 70px rgba(172,132,29,0.45); }
        #boton svg { width: 40px; height: 40px; }
        #web { position: absolute; left: 0; top: 900px; width: 1080px; text-align: center; font-size: 36px; font-weight: 600; color: #e6e6e6; }
        #qrbox { position: absolute; left: 50%%; top: 1000px; margin-left: -150px; width: 300px; padding: 22px 22px 16px; background: #fff; border-radius: 22px; text-align: center; }
        #qrbox img { width: 256px; height: 256px; display: block; image-rendering: pixelated; }
        #qrbox span { display: block; color: #111; font-family: "Montserrat"; font-weight: 700; font-size: 20px; margin-top: 8px; }
        #lema { position: absolute; left: 108px; top: 1400px; width: 864px; text-align: center; font-size: 66px; }
        #logo { position: absolute; left: 50%%; top: 1630px; width: 360px; margin-left: -180px; height: auto; }
''', '''          <div id="badge" class="chip">● Módulo Capacitaciones</div>
          <div id="gratis" class="t">
%s
          </div>
          <div id="fecha">hasta el 1 de enero de 2027</div>
          <div id="boton">Quiero activar Capacitaciones <svg viewBox="0 0 40 40"><path d="M8 20 H30 M22 12 L30 20 L22 28" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div id="web">riskmann.com/capacitaciones</div>
          <div id="qrbox"><img src="assets/qr/qr-app-riskmann-com.svg" alt="QR app.riskmann.com"><span>app.riskmann.com</span></div>
          <div id="lema" class="t">
%s
          </div>
          <img id="logo" src="assets/logo/riskmann_logo_blanco.png" alt="RiskMann">''' % (
            lineas(["Actívalo", '<span class="oro">gratis</span>']),
            lineas(["Deja de capacitar con", '<span class="oro">papel y Word.</span>'])),
        cab("cierre", [("a", M(9, "Actívalo"), "'Actívalo gratis'"), ("h", M(9, "hasta el primero"), "'hasta el primero de enero'"),
                       ("d", M(10, "Deja de"), "'Deja de capacitar'"), ("FIN", FIN, "fin del video")]) + '''
        tl.fromTo("#badge", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(a) - 0.2);
        tl.fromTo("#gratis .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a) - 0.05);
        tl.fromTo("#fecha", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.55, ease: "power4.out" }, L(h));
        tl.fromTo("#boton", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.9)" }, L(h) + 0.5);
        tl.fromTo("#web", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(h) + 0.8);
        tl.fromTo("#qrbox", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(h) + 1.0);
        tl.fromTo("#lema .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(d) - 0.05);
        tl.fromTo("#logo", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, L(d) + 0.6);
        for (var b = 0; L(h) + 1.4 + b * 1.2 < L(FIN) - 0.6; b++) {   // el boton respira (tweens explicitos)
          tl.to("#boton", { scale: 1.045, duration: 0.6, ease: "sine.inOut" }, L(h) + 1.4 + b * 1.2);
          tl.to("#boton", { scale: 1.0, duration: 0.6, ease: "sine.inOut" }, L(h) + 2.0 + b * 1.2);
        }''')

    # ===== fondo persistente: negro con resplandor dorado y fichas que flotan (como el hero de la landing)
    fichas = [(80, 260, 0), (860, 420, 1), (120, 1500, 2), (880, 1320, 0), (560, 150, 2), (720, 1760, 1)]
    icon = ['<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="24" fill="none" stroke="currentColor" stroke-width="4"/><path d="M19 31 L27 38 L42 22" fill="none" stroke="currentColor" stroke-width="4"/></svg>',
            '<svg viewBox="0 0 60 60"><rect x="6" y="12" width="48" height="36" rx="6" fill="none" stroke="currentColor" stroke-width="4"/><path d="M14 24 H40 M14 32 H32" stroke="currentColor" stroke-width="4"/><circle cx="44" cy="40" r="6" fill="currentColor"/></svg>',
            '<svg viewBox="0 0 60 60"><rect x="8" y="8" width="44" height="44" rx="12" fill="none" stroke="currentColor" stroke-width="4"/><path d="M25 21 L39 30 L25 39 Z" fill="currentColor"/></svg>']
    fichasH = "\n".join('          <div class="ficha" id="fi%d" style="left:%dpx;top:%dpx">%s</div>' % (i, x, y, icon[k]) for i, (x, y, k) in enumerate(fichas))
    comps["fondo"] = ('''        #base { position: absolute; inset: 0; background: #040404; }
        #brillo { position: absolute; left: -300px; top: -200px; width: 1400px; height: 1400px; border-radius: 50%%;
          background: radial-gradient(circle, rgba(172,132,29,0.26) 0%%, rgba(172,132,29,0.07) 40%%, rgba(4,4,4,0) 68%%); }
        #brillo2 { position: absolute; left: 200px; top: 1100px; width: 1300px; height: 1300px; border-radius: 50%%;
          background: radial-gradient(circle, rgba(25,39,68,0.55) 0%%, rgba(4,4,4,0) 65%%); }
        .ficha { position: absolute; width: 110px; height: 110px; color: rgba(217,176,74,0.28); }
        .ficha svg { width: 100%%; height: 100%%; }
        #barrido { position: absolute; left: -200px; top: 0; width: 160px; height: 1920px; opacity: 0;
          background: linear-gradient(90deg, rgba(217,176,74,0), rgba(217,176,74,0.22), rgba(217,176,74,0)); transform: skewX(-18deg); }
''', '''          <div id="base"></div><div id="brillo"></div><div id="brillo2"></div>
%s
          <div id="barrido"></div>''' % fichasH,
        '''        var FIN = %s;
        var CORTES = %s;   // cambios de escena (s): un barrido dorado cruza la pantalla
        tl.fromTo("#brillo", { x: 0, y: 0 }, { x: 420, y: 520, duration: FIN, ease: "none" }, 0);
        tl.fromTo("#brillo2", { x: 0, y: 0 }, { x: -380, y: -300, duration: FIN, ease: "none" }, 0);
        gsap.utils.toArray(".ficha").forEach(function (f, i) {
          tl.fromTo(f, { y: 0, rotation: -8 + i * 3 }, { y: -140 - i * 20, rotation: 8 - i * 2, duration: FIN, ease: "none" }, 0);
        });
        CORTES.forEach(function (tc) {
          tl.fromTo("#barrido", { x: 0, opacity: 0 }, { x: 1400, opacity: 1, duration: 0.6, ease: "power2.inOut", immediateRender: false }, tc - 0.3);
          tl.to("#barrido", { opacity: 0, duration: 0.15 }, tc + 0.15);
        });''' % (FIN, json.dumps([S[e] for e in nombres[1:]])))

    # --- escribir sub-composiciones
    os.makedirs(os.path.join(RAIZ, "compositions"), exist_ok=True)
    for e, (css, cuerpo, js) in comps.items():
        io.open(os.path.join(RAIZ, "compositions", "escena-%s.html" % e if e != "fondo" else "fondo.html"), "w",
                encoding="utf-8", newline="\n").write(sub("escena-" + e if e != "fondo" else "fondo", css, cuerpo, js))

    # --- index: anfitriones + audio
    hosts = ['''      <!-- fondo persistente: negro, resplandor dorado, fichas flotando -->
      <div id="fondo" data-composition-id="fondo" data-composition-src="compositions/fondo.html"
        data-track-kind="graphics" data-start="0" data-duration="%s" data-track-index="1"
        data-width="1080" data-height="1920" style="z-index:1"></div>''' % FIN]
    for i, e in enumerate(nombres):
        hosts.append('''      <!-- %d · %s -->
      <div id="escena-%s" data-composition-id="escena-%s" data-composition-src="compositions/escena-%s.html"
        data-track-kind="graphics" data-start="%s" data-duration="%s" data-track-index="2"
        data-width="1080" data-height="1920" style="z-index:%d"></div>''' % (i + 1, e, e, e, e, S[e], round(FINES[e] - S[e], 2), 10 + i))
    # ganancia por toma: las frases cortas miden mas bajo en la mezcla (medido sobre el MP4 final)
    GAN = {}   # data-volume > 1 no sube nada: las tomas 5 y 8 se nivelan a disco mas alto (ver LEEME)
    voces = ['      <audio id="voz-%d" src="assets/mezcla/voz-%d.wav" data-start="%.2f" data-duration="%.2f" data-track-index="10" data-volume="%.2f"></audio>'
             % (n, n, V[n], t[n]["dur"], GAN.get(n, 1.0)) for n in V]
    ev = [("golpe", V[1] - 0.05, 0.45)]
    ev += [("whoosh", S[e] - 0.25, 0.30) for e in nombres[1:]]
    ev += [("papel", M(2, "Un certificado") - 0.55, 0.40), ("tecla", M(3, "YouTube") - 0.1, 0.35),
           ("tecla", M(3, "pe de efe") - 0.1, 0.35), ("tecla", M(3, "Google Drive") - 0.1, 0.35),
           ("visto", V[5] + 0.6, 0.45), ("brillo", V[6] - 0.15, 0.35),
           ("pop", M(7, "Quién aprobó") - 0.05, 0.30), ("pop", M(7, "quién reprobó") - 0.05, 0.30),
           ("pop", M(7, "quién está") - 0.05, 0.30), ("pop", M(7, "todo en Excel"), 0.35),
           ("brillo", M(9, "hasta el primero"), 0.40), ("pop", M(9, "hasta el primero") + 0.5, 0.35)]
    ev.sort(key=lambda x: x[1])
    fin_pista, cont, efectos = {11: -1.0, 12: -1.0, 13: -1.0}, {}, []
    for nom, t0, g in ev:
        d = SFX[nom][1]
        pista = next(p for p in (11, 12, 13) if fin_pista[p] <= t0)
        fin_pista[pista] = t0 + d
        cont[nom] = cont.get(nom, 0) + 1
        efectos.append('      <audio id="sfx-%s-%d" src="assets/sfx/%s.mp3" data-start="%.2f" data-duration="%.2f" data-track-index="%d" data-volume="%.2f"></audio>'
                       % (nom, cont[nom], nom, t0, d, pista, g))
    ult = V[len(GUION)] + t[len(GUION)]["dur"]
    pts = [(0.0, 0.0), (0.2, 0.12), (round(ult, 2), 0.12), (round(ult + 0.35, 2), 0.28), (round(FIN - 0.1, 2), 0.0)]
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": a, "v": b} for a, b in pts]}]}, separators=(",", ":"))
    musicaH = ('      <audio id="musica-cama" src="assets/musica/cama.mp3" data-start="0" data-duration="%s" data-track-index="14" data-volume="1"\n'
               '        data-automation="%s"></audio>' % (FIN, html.escape(auto, quote=True)))
    index = '''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
    <style>
      /* RiskMann · Modulo Capacitaciones — promo vertical. Generado por tools/construir.py.
         Fuente: riskmann.com/capacitaciones. Identidad de la landing: negro + dorado #AC841D,
         Montserrat + Open Sans. Una fila por escena en el Studio; el apilado lo da el z-index. */
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #040404; }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #040404; }
      #root > div { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1080" data-height="1920">
%s

      <!-- VOZ · Carlos (ElevenLabs, eleven_multilingual_v2, semilla fija), tomas niveladas -->
%s

      <!-- EFECTOS · ElevenLabs -->
%s

      <!-- MUSICA · generada para esta pieza; baja bajo la voz y sube al final -->
%s
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
''' % (FIN, "\n".join(hosts), "\n".join(voces), "\n".join(efectos), musicaH)
    io.open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8", newline="\n").write(index)
    io.open(os.path.join(RAIZ, "meta.json"), "w").write('{"id":"riskmann-capacitaciones-promo","name":"riskmann-capacitaciones-promo"}')
    pk = os.path.join(RAIZ, "package.json")
    if not os.path.isfile(pk):
        shutil.copyfile(os.path.join(RAIZ, "..", "fegir-envivo", "package.json"), pk)
    print("FIN %.1f s · escenas %s" % (FIN, {e: (S[e], FINES[e]) for e in nombres}))


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso in ("voz", "todo"):
        voz(set(int(x) for x in sys.argv[2].split(",")) if paso == "voz" and len(sys.argv) > 2 else None)
    if paso in ("musica", "todo"):
        musica()
    if paso in ("construir", "todo"):
        construir()
