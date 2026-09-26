# -*- coding: utf-8 -*-
"""Serie de recordatorios FEGIR para el En Vivo PESV (3 de octubre).

Tres videos, uno por correo de la secuencia (Documentos_contexto/correos-en-vivo-pesv):
  1-pocos-dias  acompana al correo de reserva ("Faltan 18 dias")
  2-manana      acompana al correo "Manana"
  3-hoy         acompana al correo "Hoy"

Identidad y escenas heredadas de videos/fegir-envivo (aprobado). Nada de la
marca de Yezid: del correo solo se toman los datos del evento y los pasos.

    python serie.py voz          # locucion ElevenLabs (Carlos, semilla fija) + tiempos
    python serie.py construir    # escribe cada proyecto (index.html + compositions/)
    python serie.py              # las dos cosas

Cada carpeta N-xxx/ es un proyecto HyperFrames normal: se abre en el Studio con
`npx hyperframes preview` y se renderiza con `npx hyperframes render`.
La clave de ElevenLabs se lee del entorno o de ~/.elevenlabs-key.txt.
"""
import base64, html, importlib.util, io, json, os, shutil, subprocess, sys, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(AQUI), "fegir-envivo")      # video aprobado
VOZ_ID, MODELO, SEMILLA = "4PN5DHmrfIgZksvIrawS", "eleven_multilingual_v2", 20261003
AJUSTES = {"stability": 0.32, "similarity_boost": 0.85, "style": 0.5, "use_speaker_boost": True, "speed": 0.97}

# La toma de cierre es la APROBADA del video principal ("FEGIR... tu seguridad, nuestra prioridad.")
CIERRE = {"archivo": os.path.join(BASE, "assets", "mezcla", "voz-6.wav"), "dur": 2.322, "lema": 0.673}

SERIE = [
  {"carpeta": "1-pocos-dias", "sello": "En vivo · 3 oct",
   "titular": ["Faltan", "pocos días"], "titular_px": 170, "kicker": "En vivo · Informe de Autogestión PESV",
   "cal_rot": "", "canales": True,
   "paso1": "Entra al grupo oficial", "boton": "Entrar al grupo de WhatsApp",
   "paso2": "Crea tu cuenta en",
   "voz": [
     ("Faltan pocos días para el en vivo pe e ese ve.", ["Faltan pocos días", "para el en vivo"]),
     ("Sábado tres de octubre, a las diez de la mañana, por Instagram, TikTok y YouTube.",
      ["Sábado tres de octubre", "a las diez", "por Instagram"]),
     ("Entra al grupo oficial de WhatsApp: allí van los enlaces.", ["Entra al grupo"]),
     ("Y crea tu cuenta en app punto riskmann punto com.", ["Y crea tu cuenta", "app punto"]),
   ]},
  {"carpeta": "2-manana", "sello": "Mañana · 10:00 a. m.",
   "titular": ["¡Es mañana!"], "titular_px": 150, "kicker": "En vivo · Informe de Autogestión PESV",
   "cal_rot": "Mañana", "canales": True,
   "paso1": "Los enlaces van por el grupo oficial", "boton": "Entrar al grupo de WhatsApp",
   "paso2": "Ten lista tu cuenta en",
   "voz": [
     ("¡Mañana es el en vivo pe e ese ve!", ["¡Mañana es", "el en vivo"]),
     ("A las diez de la mañana, por Instagram, TikTok y YouTube.", ["A las diez", "por Instagram"]),
     ("Los enlaces van por el grupo oficial de WhatsApp.", ["Los enlaces"]),
     ("Ten lista tu cuenta en app punto riskmann punto com.", ["Ten lista tu cuenta", "app punto"]),
   ]},
  {"carpeta": "3-hoy", "sello": "Hoy · 10:00 a. m.",
   "titular": ["¡Es hoy!"], "titular_px": 220, "kicker": "En vivo · Informe de Autogestión PESV",
   "cal_rot": "Hoy", "canales": True,
   "paso1": "Los enlaces, en el grupo oficial", "boton": "Ir al grupo de WhatsApp",
   "paso2": "Ten abierta tu cuenta en",
   "voz": [
     ("¡Hoy es el en vivo pe e ese ve!", ["¡Hoy es", "el en vivo"]),
     ("A las diez de la mañana, por Instagram, TikTok y YouTube.", ["A las diez", "por Instagram"]),
     ("Entra ya al grupo oficial de WhatsApp.", ["Entra ya"]),
     ("Ten abierta tu cuenta en app punto riskmann punto com.", ["Ten abierta tu cuenta", "app punto"]),
   ]},
]

CORT = 0.40          # la cortina entra 0.40 s antes de la frase que abre su escena
GAP_ESCENA = 0.45    # hueco entre una frase y la que abre escena nueva (la cortina cae despues)
GAP_FRASE = 0.35     # hueco entre frases de la misma escena
COLA = 0.9           # musica sola tras la ultima frase


# ------------------------------------------------------------------ voz
def clave():
    f = os.path.join(os.path.expanduser("~"), ".elevenlabs-key.txt")
    k = os.environ.get("ELEVENLABS_API_KEY") or (io.open(f, encoding="utf-8-sig").read().strip() if os.path.isfile(f) else "")
    if not k.startswith("sk_"):
        raise SystemExit("falta la clave de ElevenLabs (sk_...)")
    return k


def locutar(texto):
    cuerpo = {"text": texto, "model_id": MODELO, "voice_settings": AJUSTES, "seed": SEMILLA}
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % VOZ_ID
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"xi-api-key": clave(), "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())


def voz(solo=None):
    """solo: {"1-pocos-dias": {2}, ...} regenera solo esas frases y conserva el resto."""
    for v in SERIE:
        if solo is not None and v["carpeta"] not in solo:
            continue
        raiz = os.path.join(AQUI, v["carpeta"])
        os.makedirs(os.path.join(raiz, "assets", "voz"), exist_ok=True)
        ruta_t = os.path.join(raiz, "tools", "tiempos-voz.json")
        previos = {x["n"]: x for x in json.load(io.open(ruta_t, encoding="utf-8"))} if solo and os.path.isfile(ruta_t) else {}
        tiempos = []
        for n, (texto, marcas) in enumerate(v["voz"], 1):
            if solo is not None and n not in solo[v["carpeta"]]:
                tiempos.append(previos[n])
                continue
            d = locutar(texto)
            open(os.path.join(raiz, "assets", "voz", "f%02d.mp3" % n), "wb").write(base64.b64decode(d["audio_base64"]))
            ini = d["alignment"]["character_start_times_seconds"]
            fin = d["alignment"]["character_end_times_seconds"]
            m = [round(ini[texto.index(x)], 3) for x in marcas]
            tiempos.append({"n": n, "texto": texto, "marcas": dict(zip(marcas, m)), "dur": round(fin[-1], 3)})
            print("%-14s f%d  %.2f s  %s" % (v["carpeta"], n, fin[-1], texto))
        os.makedirs(os.path.join(raiz, "tools"), exist_ok=True)
        io.open(os.path.join(raiz, "tools", "tiempos-voz.json"), "w", encoding="utf-8", newline="\n").write(
            json.dumps(tiempos, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ construir
def _audio_tools():
    spec = importlib.util.spec_from_file_location("audio_base", os.path.join(BASE, "tools", "audio.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


FUENTES = '''        @font-face { font-family: "FEGIR Sans"; font-weight: 300; src: url("assets/fonts/segoeuil.ttf") format("truetype"); }
        @font-face { font-family: "FEGIR Sans"; font-weight: 400; src: url("assets/fonts/segoeui.ttf") format("truetype"); }
        @font-face { font-family: "FEGIR Sans"; font-weight: 600; src: url("assets/fonts/segoeuisb.ttf") format("truetype"); }
        @font-face { font-family: "FEGIR Sans"; font-weight: 700; src: url("assets/fonts/segoeuib.ttf") format("truetype"); }
        #root {
          position: absolute; inset: 0; overflow: hidden; background: %s;
          font-family: "FEGIR Sans", sans-serif; color: #fff;
          --verde: #45a035; --verde-claro: #a8c875; --crema: #f1ecb0;
          --banda-a: #50cd72; --banda-b: #4ecd25; --verde-fondo: #3a8f2c;
          --verde-hondo: #22621a; --tinta: #1d2b1a;
        }
        .capa { position: absolute; inset: 0; }
        .cortina { position: absolute; left: -400px; top: -300px; width: 1900px; height: 2600px; transform-origin: 50%% 50%%; }
        .filo { position: absolute; left: 0; top: 0; width: 100%%; height: 38px; }
'''


def sub(cid, fondo, css, cuerpo, js):
    return '''<!doctype html>
<html lang="es">
  <head><meta charset="UTF-8"><title>%s</title></head>
  <body>
    <template>
      <style>
%s%s
      </style>

      <div id="root" data-composition-id="%s" data-width="1080" data-height="1920">
%s
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
''' % (cid, FUENTES % fondo, css, cid, cuerpo, js, cid)


def tabla_js(V, S, extra):
    lineas = ["        /* TIEMPOS globales (s). V: inicio de cada frase de voz; S: inicio de esta escena",
              "           (su data-start en index.html). Si mueves la escena, cambia S tambien. */",
              "        var V = %s;" % json.dumps({"f%d" % k: v for k, v in V.items()}),
              "        var S = %s;" % S,
              "        var L = function (t) { return t - S; };"]
    lineas += ["        var %s = %s;   // %s" % (k, v, c) for k, v, c in extra]
    return "\n".join(lineas) + "\n"


def construir():
    au = _audio_tools()
    for v in SERIE:
        raiz = os.path.join(AQUI, v["carpeta"])
        t = json.load(io.open(os.path.join(raiz, "tools", "tiempos-voz.json"), encoding="utf-8"))
        # --- copia de recursos del video aprobado
        for d in ("fonts", "logo", "fotos", "sfx", "musica"):
            dst = os.path.join(raiz, "assets", d)
            if not os.path.isdir(dst):
                shutil.copytree(os.path.join(BASE, "assets", d), dst)
        os.makedirs(os.path.join(raiz, "assets", "mezcla"), exist_ok=True)
        os.makedirs(os.path.join(raiz, "compositions"), exist_ok=True)
        for n in range(1, 5):
            au.nivelar(os.path.join(raiz, "assets", "voz", "f%02d.mp3" % n),
                       os.path.join(raiz, "assets", "mezcla", "voz-%d.wav" % n), -16)
        shutil.copyfile(CIERRE["archivo"], os.path.join(raiz, "assets", "mezcla", "voz-5.wav"))

        # --- tiempos: cada frase detras de la anterior; escenas nuevas en f2 y f3
        DUR = {x["n"]: x["dur"] for x in t}
        DUR[5] = CIERRE["dur"]
        M = {x["n"]: list(x["marcas"].values()) for x in t}
        V = {1: 0.30}
        for n in range(2, 6):
            V[n] = round(V[n - 1] + DUR[n - 1] + (GAP_ESCENA if n in (2, 3) else GAP_FRASE), 2)
        FIN = round(V[5] + DUR[5] + COLA, 1)
        for n in (1, 2):
            assert V[n] + DUR[n] <= V[n + 1] - CORT + 0.001
        S = {"a": 0, "b": round(V[2] - 0.45, 2), "c": round(V[3] - 0.45, 2)}
        FINES = {"a": round(V[2] + 0.35, 2), "b": round(V[3] + 0.35, 2), "c": FIN}

        # ============ escena A · titular sobre la foto del manual
        titular = "\n".join('          <div class="l"><span>%s</span></div>' % html.escape(x) for x in v["titular"])
        cssA = '''        #foto-caja { overflow: hidden; }
        #foto { position: absolute; left: -60px; top: -80px; width: 1200px; height: auto;
          filter: grayscale(1) contrast(1.08) brightness(1.05); }
        #foto-tinte { background: linear-gradient(160deg, #50cd72 0%, #3fa532 55%, #4ecd25 100%); mix-blend-mode: multiply; }
        #foto-sombra { background: linear-gradient(180deg, rgba(20,60,16,0) 34%, rgba(20,60,16,0.80) 74%, rgba(20,60,16,0.94) 100%); }
        #kicker { position: absolute; left: 80px; top: 1040px; width: 920px;
          font-size: 30px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--crema); }
        #titular { position: absolute; left: 76px; top: 1110px; width: 940px;
          font-size: __PX__px; font-weight: 700; line-height: 1.02; letter-spacing: -0.035em;
          text-shadow: 0 8px 34px rgba(10, 40, 8, 0.55); }
        #titular .l { display: block; overflow: hidden; padding-bottom: 10px; }
        #titular .l span { display: inline-block; }
'''.replace("__PX__", str(v["titular_px"]))
        cuerpoA = '''        <div id="foto-caja" class="capa">
          <img id="foto" src="assets/fotos/portada-manual-vertical.jpg" alt="">
          <div id="foto-tinte" class="capa"></div>
          <div id="foto-sombra" class="capa"></div>
          <div id="kicker">%s</div>
          <div id="titular">
%s
          </div>
        </div>''' % (html.escape(v["kicker"]), titular)
        jsA = tabla_js(V, S["a"], [("kick", round(V[1] + M[1][1], 3), "marca de voz: '%s'" % list(t[0]["marcas"])[1])]) + '''
        tl.fromTo("#foto", { scale: 1.12, y: 0 }, { scale: 1.0, y: -40, duration: %s, ease: "none" }, 0);
        tl.fromTo("#titular .l span", { yPercent: 110 },
          { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.22 }, L(V.f1));
        tl.fromTo("#kicker", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(kick));''' % FINES["a"]

        # ============ escena B · calendario (verde)
        rot = ('        <div id="cal-rot">%s</div>\n' % html.escape(v["cal_rot"])) if v["cal_rot"] else ""
        canales = ('''        <div id="canales"><span class="ch">Instagram</span><span class="ch">TikTok</span><span class="ch">YouTube</span></div>\n'''
                   if v["canales"] else "")
        cssB = '''        #cortina-verde { background: linear-gradient(135deg, var(--banda-b) 0%, var(--verde-fondo) 34%, #2e7a22 100%); }
        #cortina-verde .filo { background: var(--verde-claro); }
        #cal-rot { position: absolute; left: 0; top: 400px; width: 1080px; text-align: center;
          font-size: 64px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--crema); }
        #cal { position: absolute; left: 50%; top: 520px; width: 540px; margin-left: -270px;
          border-radius: 40px; overflow: hidden; background: #fff; box-shadow: 0 40px 90px rgba(10,40,8,0.40); }
        #cal-cab { background: var(--crema); color: var(--verde-hondo); text-align: center;
          font-size: 38px; font-weight: 700; letter-spacing: 0.3em; padding: 26px 0 22px; }
        #cal-num { text-align: center; font-size: 260px; font-weight: 700; line-height: 1.2; color: var(--tinta); letter-spacing: -0.04em; }
        #cal-mes { text-align: center; font-size: 48px; font-weight: 700; letter-spacing: 0.22em; color: var(--verde-hondo); padding: 0 0 38px; }
        #hora { position: absolute; left: 0; top: 1150px; width: 1080px; text-align: center;
          font-size: 96px; font-weight: 700; letter-spacing: -0.01em; }
        #zona { position: absolute; left: 0; top: 1285px; width: 1080px; text-align: center;
          font-size: 30px; font-weight: 600; letter-spacing: 0.26em; text-transform: uppercase; color: var(--crema); }
        #canales { position: absolute; left: 0; top: 1400px; width: 1080px; display: flex; justify-content: center; gap: 20px; }
        .ch { padding: 16px 34px; border-radius: 100px; background: #1f5a17; color: #fff;
          font-size: 34px; font-weight: 700; }
'''
        cuerpoB = '''        <div id="cortina-verde" class="cortina"><div class="filo"></div></div>
%s        <div id="cal">
          <div id="cal-cab">SÁBADO</div>
          <div id="cal-num">3</div>
          <div id="cal-mes">OCTUBRE</div>
        </div>
        <div id="hora">10:00 a. m.</div>
        <div id="zona">Hora Colombia</div>
%s''' % (rot, canales)
        marca = lambda n, clave: next(V[n] + x for k, x in t[n - 1]["marcas"].items() if clave in k)
        extra = [("hora", round(marca(2, "diez") - 0.1, 3), "'a las diez'")]
        if v["canales"]:
            extra.append(("canal", round(marca(2, "Instagram"), 3), "'por Instagram'"))
        jsB = tabla_js(V, S["b"], extra) + '''
        tl.fromTo("#cortina-verde", { rotation: -32, yPercent: 105 },
          { rotation: -32, yPercent: 0, duration: 0.75, ease: "power3.inOut" }, L(V.f2) - %s);
        tl.fromTo("#cortina-verde", { rotation: -32 }, { rotation: 0, immediateRender: false, duration: 0.9, ease: "power2.out" }, L(V.f2 + 0.2));
''' % CORT
        if v["cal_rot"]:
            jsB += '''        tl.fromTo("#cal-rot", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.55, ease: "power4.out" }, L(V.f2 - 0.05));
'''
        jsB += '''        tl.fromTo("#cal", { opacity: 0, y: -260, rotation: -8 },
          { opacity: 1, y: 0, rotation: 0, duration: 0.9, ease: "back.out(1.4)" }, L(V.f2 + 0.1));
        tl.fromTo("#cal-num", { scale: 0.4 }, { scale: 1, duration: 0.7, ease: "back.out(2.4)" }, L(V.f2 + 0.55));
        tl.fromTo("#hora", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(hora));
        tl.fromTo("#zona", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(hora + 0.25));
'''
        if v["canales"]:
            jsB += '''        tl.fromTo("#canales .ch", { opacity: 0, y: 30, scale: 0.8 },
          { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(2)", stagger: 0.18 }, L(canal));
'''
        jsB += '''        // el texto blanco se va mientras sube la cortina blanca de la escena siguiente
        tl.to(["#hora", "#zona"%s], { opacity: 0, duration: 0.25, ease: "power2.in" }, L(V.f3) - %s);''' % (
            ', "#canales"' if v["canales"] else "", CORT)

        # ============ escena C · los dos pasos + cierre (blanco)
        cssC = '''        #cortina-blanca { background: #ffffff; }
        #cortina-blanca .filo { background: var(--crema); }
        .paso { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; gap: 18px;
          font-size: 34px; font-weight: 600; color: var(--verde-hondo); }
        .num { width: 54px; height: 54px; border-radius: 50%; background: var(--verde-hondo); color: #fff;
          display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 700; flex-shrink: 0; }
        #paso1 { top: 420px; }
        #boton { position: absolute; left: 50%; top: 510px; transform: translateX(-50%); white-space: nowrap;
          padding: 36px 70px; border-radius: 100px; background: linear-gradient(135deg, #3f9a30, #2e7a22); color: #fff;
          font-size: 50px; font-weight: 700; box-shadow: 0 26px 60px rgba(46,122,34,0.40), inset 0 2px 0 rgba(255,255,255,0.25); }
        #paso2 { top: 810px; }
        #web { position: absolute; left: 0; top: 890px; width: 1080px; text-align: center;
          font-size: 84px; font-weight: 700; color: var(--tinta); letter-spacing: -0.01em; }
        #logo-color { position: absolute; left: 50%; top: 1270px; width: 720px; margin-left: -360px; height: auto; }
        #lema { position: absolute; left: 0; top: 1600px; width: 1080px; text-align: center;
          font-size: 50px; font-weight: 700; color: var(--verde-hondo); letter-spacing: -0.01em; }
'''
        cuerpoC = '''        <div id="cortina-blanca" class="cortina"><div class="filo"></div></div>
        <div id="paso1" class="paso"><span class="num">1</span><span>%s</span></div>
        <div id="boton">%s</div>
        <div id="paso2" class="paso"><span class="num">2</span><span>%s</span></div>
        <div id="web">app.riskmann.com</div>
        <img id="logo-color" src="assets/logo/fegir-logo-color.png" alt="FEGIR - Fundación Especializada en Gestión Integral del Riesgo">
        <div id="lema">¡Tu seguridad, nuestra prioridad!</div>''' % (html.escape(v["paso1"]), html.escape(v["boton"]), html.escape(v["paso2"]))
        jsC = tabla_js(V, S["c"], [("web", round(V[4] + M[4][1] - 0.05, 3), "'app punto'"),
                                   ("lema", round(V[5] + CIERRE["lema"], 3), "'tu seguridad'"),
                                   ("FIN", FIN, "fin del video")]) + '''
        tl.fromTo("#cortina-blanca", { rotation: 28, yPercent: 105 },
          { rotation: 28, yPercent: 0, duration: 0.75, ease: "power3.inOut" }, L(V.f3) - %s);
        tl.fromTo("#cortina-blanca", { rotation: 28 }, { rotation: 0, immediateRender: false, duration: 0.9, ease: "power2.out" }, L(V.f3 + 0.2));
        tl.fromTo("#paso1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(V.f3));
        tl.fromTo("#boton", { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: 0.75, ease: "back.out(1.9)" }, L(V.f3 + 0.15));
        tl.fromTo("#paso2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(V.f4));
        tl.fromTo("#web", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(web));
        tl.fromTo("#logo-color", { opacity: 0, y: 40, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: "expo.out" }, L(V.f5 - 0.10));
        tl.fromTo("#lema", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(lema));
        // el boton respira hasta el final (tweens explicitos, seek-safe)
        for (var b = 0; V.f3 + 1.2 + b * 1.2 < FIN - 0.6; b++) {
          var tb = V.f3 + 1.2 + b * 1.2;
          tl.to("#boton", { scale: 1.045, duration: 0.6, ease: "sine.inOut" }, L(tb));
          tl.to("#boton", { scale: 1.0, duration: 0.6, ease: "sine.inOut" }, L(tb + 0.6));
        }''' % CORT

        # ============ sello
        cssS = '''        #sello { position: absolute; left: 50%; top: 120px; transform: translateX(-50%);
          display: flex; align-items: center; gap: 16px; white-space: nowrap; padding: 16px 38px; border-radius: 100px;
          background: #1f5a17; color: var(--crema); font-size: 28px; font-weight: 700; letter-spacing: 0.22em;
          text-transform: uppercase; box-shadow: 0 14px 34px rgba(8,30,6,0.35); }
        #latido { position: relative; width: 16px; height: 16px; flex-shrink: 0; }
        #latido i { position: absolute; inset: 0; border-radius: 50%; background: var(--crema); }
        #aro { position: absolute; inset: -7px; border-radius: 50%; border: 2px solid var(--crema); opacity: 0; }
'''
        cuerpoS = '''        <div id="sello"><span id="latido"><i></i><span id="aro"></span></span>%s</div>''' % html.escape(v["sello"])
        jsS = '''        var FIN = %s;
        tl.fromTo("#sello", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)" }, 0.3);
        for (var k = 0; 0.7 + 1.2 * k < FIN - 1.0; k++) {
          var tp = 0.7 + 1.2 * k;
          tl.to("#latido i", { scale: 1.3, duration: 0.16, ease: "power2.out" }, tp);
          tl.to("#latido i", { scale: 1.0, duration: 0.44, ease: "power2.inOut" }, tp + 0.16);
          tl.fromTo("#aro", { scale: 0.55, opacity: 0.8 },
            { scale: 2.1, opacity: 0, immediateRender: false, duration: 0.9, ease: "power2.out" }, tp);
        }''' % FIN

        escenas = [("escena-titular", "#2e7a22", cssA, cuerpoA, jsA, S["a"], FINES["a"], 1, 1, "A · titular sobre la foto del manual"),
                   ("escena-fecha", "transparent", cssB, cuerpoB, jsB, S["b"], FINES["b"], 2, 2, "B · la fecha (verde)"),
                   ("escena-pasos", "transparent", cssC, cuerpoC, jsC, S["c"], FINES["c"], 1, 3, "C · los dos pasos y el cierre (blanco)"),
                   ("sello-envivo", "transparent", cssS, cuerpoS, jsS, 0, FIN, 3, 10, "sello, todo el video")]
        hosts = []
        for cid, fondo, css, cuerpo, js, s0, s1, pista, z, nota in escenas:
            io.open(os.path.join(raiz, "compositions", cid + ".html"), "w", encoding="utf-8", newline="\n").write(
                sub(cid, fondo, css, cuerpo, js))
            hosts.append('''      <!-- %s -->
      <div id="%s" data-composition-id="%s" data-composition-src="compositions/%s.html"
        data-track-kind="graphics" data-start="%s" data-duration="%s" data-track-index="%d"
        data-width="1080" data-height="1920" style="z-index:%d"></div>''' % (nota, cid, cid, cid, s0, round(s1 - s0, 2), pista, z))

        # --- audio
        voces = ['      <audio id="voz-%d" src="assets/mezcla/voz-%d.wav" data-start="%.2f" data-duration="%.2f" '
                 'data-track-index="10" data-volume="1"></audio>' % (n, n, V[n], DUR[n]) for n in V]
        ev = [("cortina", V[2] - CORT, 1.0, 0.35), ("cortina", V[3] - CORT, 1.0, 0.35),
              ("golpe", V[1] + 0.05, 1.5, 0.45), ("hoja", V[2] + 0.1, 0.9, 0.45),
              ("pop", V[3] + 0.15, 0.5, 0.40), ("pop", V[4] + M[4][1] - 0.05, 0.5, 0.35),
              ("brillo", V[5] - 0.10, 1.6, 0.40)]
        if v["canales"]:
            ev.append(("pop", marca(2, "Instagram"), 0.5, 0.30))
        ev.sort(key=lambda e: e[1])
        fin_pista, cont, efectos = {11: -1.0, 12: -1.0}, {}, []
        for nombre, t0, d, g in ev:
            pista = 11 if fin_pista[11] <= t0 else 12
            fin_pista[pista] = t0 + d
            cont[nombre] = cont.get(nombre, 0) + 1
            efectos.append('      <audio id="sfx-%s-%d" src="assets/sfx/%s.mp3" data-start="%.2f" data-duration="%.2f" '
                           'data-track-index="%d" data-volume="%.2f"></audio>' % (nombre, cont[nombre], nombre, t0, d, pista, g))
        fin5 = V[5] + DUR[5]
        pts = [(0.0, 0.0), (0.25, 0.14), (round(fin5, 2), 0.14), (round(fin5 + 0.3, 2), 0.30), (round(FIN - 0.1, 2), 0.0)]
        assert [p[0] for p in pts] == sorted(p[0] for p in pts)
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": a, "v": b} for a, b in pts]}]},
                          separators=(",", ":"))
        musica = ('      <audio id="musica-cama" src="assets/musica/cama.mp3" data-start="0" data-duration="%s" '
                  'data-track-index="13" data-volume="1"\n        data-automation="%s"></audio>' % (FIN, html.escape(auto, quote=True)))

        index = '''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
    <style>
      /* FEGIR · En Vivo PESV · recordatorio "%s" — generado por ../serie.py.
         Identidad: la del video aprobado videos/fegir-envivo (manual FEGIR).
         Solo anfitriones (una fila por escena en el Studio) y audio. */
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #2e7a22; }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #2e7a22; }
      #root > div { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1080" data-height="1920">
%s

      <!-- VOZ · Carlos (ElevenLabs); la 5 es la toma de cierre aprobada del video principal -->
%s

      <!-- EFECTOS -->
%s

      <!-- MUSICA · la cama del video principal, baja bajo la voz -->
%s
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
''' % (v["carpeta"], FIN, "\n".join(hosts), "\n".join(voces), "\n".join(efectos), musica)
        io.open(os.path.join(raiz, "index.html"), "w", encoding="utf-8", newline="\n").write(index)
        io.open(os.path.join(raiz, "meta.json"), "w", encoding="utf-8").write(
            json.dumps({"id": "fegir-rec-" + v["carpeta"], "name": "fegir-rec-" + v["carpeta"]}))
        shutil.copyfile(os.path.join(BASE, "package.json"), os.path.join(raiz, "package.json"))
        print("%-14s %.1f s  V=%s" % (v["carpeta"], FIN, V))


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso in ("voz", "todo"):
        # "voz 1-pocos-dias:2 2-manana:2" -> solo esas frases
        sel = {}
        for a in sys.argv[2:]:
            c, ns = a.split(":")
            sel[c] = set(int(x) for x in ns.split(","))
        voz(sel or None)
    if paso in ("construir", "todo"):
        construir()
