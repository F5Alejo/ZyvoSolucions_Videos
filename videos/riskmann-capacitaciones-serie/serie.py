# -*- coding: utf-8 -*-
"""RiskMann · Modulo Capacitaciones — serie de 4 anuncios verticales (12-15 s).

Hermana del promo (videos/riskmann-capacitaciones-promo): misma fuente unica
(riskmann.com/capacitaciones), misma identidad de la landing (negro + dorado
#AC841D, Montserrat + Open Sans), misma voz (Carlos, semilla fija), misma musica,
efectos, logo oficial y QR oficial. Cada anuncio: gancho -> valor -> CTA, y cada
CTA usa un boton literal de la landing.

    python serie.py voz          # locucion de los 4 (solo lo que falte o cambie)
    python serie.py construir    # escribe cada proyecto N-xxx/ (index.html + compositions/)

Cada carpeta N-xxx/ es un proyecto HyperFrames: `npx hyperframes preview` / `render`.
"""
import html, importlib.util, io, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PROMO = os.path.join(os.path.dirname(AQUI), "riskmann-capacitaciones-promo")
_spec = importlib.util.spec_from_file_location("promo", os.path.join(PROMO, "tools", "construir.py"))
P = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(P)   # reutiliza plantillas y voz

GRATIS_HASTA = "hasta el primero de enero de dos mil veintisiete"
SERIE = [
  {"carpeta": "1-papel-vs-registro", "boton": "Quiero activar Capacitaciones", "sub": "Gratis hasta el 1 de enero de 2027",
   "escenas": ["papel", "registro", "cta"], "cta_titulo": ["Deja de capacitar", 'con <span class="oro">papel y Word.</span>'],
   "voz": [("Una lista firmada en papel... no alcanza.", ["Una lista", "no alcanza"]),
           ("Cada vez que alguien presenta una evaluación, la plataforma guarda el resultado, los intentos y la fecha.",
            ["Cada vez", "el resultado", "los intentos", "y la fecha"]),
           ("Deja de capacitar con papel y Word... actívalo gratis.", ["Deja de", "actívalo"])]},
  {"carpeta": "2-cuatro-pasos", "boton": "Quiero empezar ahora", "sub": "Gratis hasta el 1 de enero de 2027",
   "escenas": ["titular", "pasos", "cta"], "titular": ["Capacita a tu gente", 'con la misma cuenta', 'de <span class="oro">RiskMann</span>'],
   "cta_titulo": ["Empieza", '<span class="oro">ahora</span>'],
   "voz": [("Capacita a tu gente con la misma cuenta de RiskMann.", ["Capacita", "con la misma"]),
           ("Armas el curso. Tu gente lo toma cuando puede. La plataforma califica sola. Y queda el certificado.",
            ["Armas", "Tu gente", "La plataforma", "Y queda"]),
           ("Empieza ahora: es gratis " + GRATIS_HASTA + ".", ["Empieza", "es gratis"])]},
  {"carpeta": "3-certificado", "boton": "Quiero activar Capacitaciones", "sub": "Gratis hasta el 1 de enero de 2027",
   "escenas": ["titular", "certificado", "cta"],
   "titular": ["La capacitación", "ocurrió.", '<span class="oro">¿Pero puedes</span>', '<span class="oro">demostrarlo?</span>'],
   "cta_titulo": ["Actívalo", '<span class="oro">gratis</span>'],
   "voz": [("La capacitación ocurrió... ¿Pero puedes demostrarlo?", ["La capacitación", "¿Pero puedes"]),
           ("Con RiskMann, cada persona que aprueba recibe un certificado en pe de efe: nombre, documento, curso y fecha.",
            ["Con RiskMann", "nombre", "documento", "curso y", "fecha"]),
           ("Actívalo gratis " + GRATIS_HASTA + ".", ["Actívalo", "hasta el primero"])]},
  {"carpeta": "4-gratis-2027", "boton": "Activar ahora", "sub": "Gratis hasta el 1 de enero de 2027",
   "escenas": ["gratis", "cuenta", "cta"], "cta_titulo": ["Crear tu cuenta", 'es <span class="oro">gratis</span>'],
   "voz": [("El módulo de Capacitaciones es gratis... " + GRATIS_HASTA + ".", ["El módulo", "gratis", "hasta el primero"]),
           ("Si tu gente ya usa RiskMann, ya tiene la cuenta. Solo falta activar Capacitaciones.", ["Si tu gente", "Solo falta"]),
           ("Crear tu cuenta es gratis. ¡Actívalo ahora!", ["Crear tu cuenta", "Actívalo"])]},
]
ANTES, GAP_ESCENA, COLA = 0.30, 0.65, 1.3


# ------------------------------------------------------------------ voz
def voz():
    import base64
    for v in SERIE:
        raiz = os.path.join(AQUI, v["carpeta"])
        for d in ("voz", "mezcla"):
            os.makedirs(os.path.join(raiz, "assets", d), exist_ok=True)
        os.makedirs(os.path.join(raiz, "tools"), exist_ok=True)
        ruta = os.path.join(raiz, "tools", "tiempos-voz.json")
        previos = {x["n"]: x for x in json.load(io.open(ruta, encoding="utf-8"))} if os.path.isfile(ruta) else {}
        tiempos = []
        for n, (texto, marcas) in enumerate(v["voz"], 1):
            if n in previos and previos[n]["texto"] == texto:
                tiempos.append(previos[n]); continue
            d = json.loads(P.pedir("/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % P.VOZ_ID,
                                   {"text": texto, "model_id": P.MODELO, "voice_settings": P.AJUSTES, "seed": P.SEMILLA}))
            mp3 = os.path.join(raiz, "assets", "voz", "f%02d.mp3" % n)
            open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
            ini, fin = d["alignment"]["character_start_times_seconds"], d["alignment"]["character_end_times_seconds"]
            tiempos.append({"n": n, "texto": texto, "dur": round(fin[-1], 3),
                            "marcas": {m: round(ini[texto.index(m)], 3) for m in marcas}})
            P.nivelar(mp3, os.path.join(raiz, "assets", "mezcla", "voz-%d.wav" % n))
            print("%-20s f%d %.2f s  %s" % (v["carpeta"], n, fin[-1], texto))
        io.open(ruta, "w", encoding="utf-8", newline="\n").write(json.dumps(tiempos, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ escenas
SALIDA = '''
        if (!ULTIMA) tl.to("#c", { opacity: 0, y: -90, duration: 0.35, ease: "power2.in" }, L(FINE) - 0.35);'''


def cab(S, FINE, ultima, extra):
    js = ["        /* TIEMPOS globales (s), de tools/tiempos-voz.json. S = data-start de esta escena en index.html. */",
          "        var S = %s, FINE = %s, ULTIMA = %s;" % (S, FINE, "true" if ultima else "false"),
          "        var L = function (g) { return g - S; };"]
    js += ["        var %s = %s;   // %s" % (k, val, c) for k, val, c in extra]
    return "\n".join(js) + "\n"


def e_titular(v, m, S, FINE, ult):
    # titular grande a dos colores, linea a linea (gancho del anuncio)
    n = len(v["titular"])
    import re as _re
    largo = max(len(_re.sub(r"<[^>]+>", "", x)) for x in v["titular"])
    fs = int(min(104, 864 / (largo * 0.62)))   # cada linea cabe entera en el ancho util
    return ('''        #tt { position: absolute; left: 108px; top: %dpx; width: 864px; font-size: %dpx; }
''' % (960 - n * fs * 0.62, fs), '''          <div id="tt" class="t">
%s
          </div>''' % P.lineas(v["titular"]),
        cab(S, FINE, ult, [("a", m[1][0], "1a marca"), ("b", m[1][1], "2a marca")]) + '''
        var spans = gsap.utils.toArray("#tt .l > span");
        var mitad = Math.ceil(spans.length / 2);
        tl.fromTo(spans.slice(0, mitad), { yPercent: 115 }, { yPercent: 0, duration: 0.75, ease: "expo.out", stagger: 0.14 }, L(a) - 0.05);
        tl.fromTo(spans.slice(mitad), { yPercent: 115 }, { yPercent: 0, duration: 0.75, ease: "expo.out", stagger: 0.14 }, L(b) - 0.05);''' + SALIDA)


def e_papel(v, m, S, FINE, ult):
    filas = "\n".join('''              <div class="fila"><span class="lin"></span><span class="firma"></span></div>''' for _ in range(5))
    return ('''        #hoja { position: absolute; left: 230px; top: 330px; width: 620px; height: 760px; background: #efece4; border-radius: 10px;
          box-shadow: 0 30px 70px rgba(0,0,0,0.6); padding: 50px 46px; color: #3a3a3a; transform: rotate(-4deg); }
        #hoja h4 { font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 30px; letter-spacing: 0.08em; margin-bottom: 34px; }
        .fila { display: flex; gap: 18px; align-items: flex-end; height: 104px; border-bottom: 2px solid #c9c3b3; }
        .lin { flex: 1; height: 12px; background: #d7d1c2; border-radius: 6px; margin-bottom: 22px; }
        .firma { width: 180px; height: 40px; border-bottom: 3px solid #5a5a8a; border-radius: 0 0 60% 40%; margin-bottom: 16px; transform: skewX(-20deg); }
        #x1 { position: absolute; left: 170px; top: 700px; width: 760px; height: 12px; background: var(--dorado-claro); border-radius: 6px;
          transform-origin: left center; transform: rotate(-38deg) scaleX(0); box-shadow: 0 0 26px rgba(217,176,74,0.7); }
        #f1 { position: absolute; left: 108px; top: 1260px; width: 864px; font-size: 86px; }
''', '''          <div id="hoja"><h4>LISTA DE ASISTENCIA</h4>
%s
          </div>
          <div id="x1"></div>
          <div id="f1" class="t">
%s
          </div>''' % (filas, P.lineas(["Una lista firmada", "en papel...", '<span class="oro">no alcanza.</span>'])),
        cab(S, FINE, ult, [("a", m[1][0], "'Una lista'"), ("b", m[1][1], "'no alcanza'")]) + '''
        tl.fromTo("#hoja", { opacity: 0, y: 140, rotation: -14 }, { opacity: 1, y: 0, rotation: -4, duration: 0.8, ease: "back.out(1.3)" }, L(a) - 0.2);
        var sp = gsap.utils.toArray("#f1 .l > span");
        tl.fromTo(sp.slice(0, 2), { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a));
        tl.fromTo(sp.slice(2), { yPercent: 115 }, { yPercent: 0, duration: 0.6, ease: "expo.out" }, L(b) - 0.05);
        tl.fromTo("#x1", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, L(b) - 0.05);
        tl.to("#hoja", { opacity: 0.35, duration: 0.4, ease: "power2.out" }, L(b) + 0.2);''' + SALIDA)


def e_registro(v, m, S, FINE, ult):
    filas = [("Colaborador 1", "Aprobó", "ap", "1"), ("Colaborador 2", "Reprobó", "re", "2"), ("Colaborador 3", "Aprobó", "ap", "2")]
    trs = "\n".join('''            <div class="tr"><span class="nom">%s</span><span class="c1"><b class="est %s">%s</b></span><span class="c2">%s</span><span class="c3">dd/mm/aaaa</span></div>'''
                    % (a, c, b, i) for a, b, c, i in filas)
    return ('''        #tit { position: absolute; left: 108px; top: 330px; width: 864px; font-size: 64px; }
        #tabla { position: absolute; left: 60px; top: 640px; width: 960px; padding: 16px 0; }
        .th, .tr { display: grid; grid-template-columns: 1.35fr 1.1fr 0.75fr 1.2fr; align-items: center; padding: 24px 30px; gap: 10px; }
        .th { font-family: "Montserrat"; font-weight: 700; font-size: 22px; letter-spacing: 0.12em; color: var(--texto2); text-transform: uppercase; border-bottom: 1px solid var(--borde); }
        .tr { font-size: 30px; font-weight: 600; border-bottom: 1px solid #1c1c1c; }
        .c2 { text-align: center; } .c3 { color: var(--texto2); font-size: 26px; }
        .est { font-family: "Montserrat"; font-weight: 800; font-size: 24px; padding: 8px 20px; border-radius: 100px; }
        .ap { background: rgba(172,132,29,0.9); color: #111; } .re { background: #2a2a2a; color: #eee; border: 1px solid #444; }
        .col { opacity: 0.25; }
        #pie { position: absolute; left: 108px; top: 1180px; width: 864px; font-size: 36px; color: var(--texto2); line-height: 1.45; }
''', '''          <div id="tit" class="t">
%s
          </div>
          <div id="tabla" class="card">
            <div class="th"><span>Colaborador</span><span class="h1">Resultado</span><span class="h2" style="text-align:center">Intentos</span><span class="h3">Fecha</span></div>
%s
          </div>
          <div id="pie">No tienes que pasar nada a limpio.</div>''' % (P.lineas(["La plataforma", '<span class="oro">guarda todo</span>']), trs),
        cab(S, FINE, ult, [("a", m[2][0], "'Cada vez'"), ("r", m[2][1], "'el resultado'"), ("i", m[2][2], "'los intentos'"),
                           ("f", m[2][3], "'y la fecha'")]) + '''
        tl.fromTo("#tit .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a) - 0.1);
        tl.fromTo("#tabla", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(a) + 0.4);
        tl.fromTo(".tr .nom", { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.08 }, L(a) + 0.6);
        [["c1", "h1", r], ["c2", "h2", i], ["c3", "h3", f]].forEach(function (x) {
          tl.fromTo(".tr ." + x[0], { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.8)", stagger: 0.08 }, L(x[2]) - 0.05);
          tl.fromTo(".th ." + x[1], { color: "#b9b9b9" }, { color: "#d9b04a", duration: 0.3 }, L(x[2]) - 0.05);
        });
        tl.fromTo("#pie", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(f) + 0.5);''' + SALIDA)


def e_pasos(v, m, S, FINE, ult):
    pasos = [("Armas el curso", "Videos de YouTube, PDF o Google Drive."), ("Tu gente lo toma cuando puede", "Desde el celular o el computador."),
             ("La plataforma califica sola", "No revisas examen por examen."), ("Y queda el certificado", "Un PDF listo para mostrar.")]
    cards = "\n".join('''            <div class="paso card" id="p%d"><div class="num">%d</div><div><div class="pt">%s</div><div class="pd">%s</div></div></div>'''
                      % (i, i, a, b) for i, (a, b) in enumerate(pasos, 1))
    return ('''        #lista { position: absolute; left: 90px; top: 420px; width: 900px; display: flex; flex-direction: column; gap: 30px; }
        .paso { display: flex; align-items: center; gap: 30px; padding: 36px 40px; }
        .pt { font-family: "Montserrat"; font-weight: 800; font-size: 44px; line-height: 1.15; }
        .pd { font-size: 30px; color: var(--texto2); margin-top: 8px; }
''', '''          <div id="lista">
%s
          </div>''' % cards,
        cab(S, FINE, ult, [("p1", m[2][0], "'Armas'"), ("p2", m[2][1], "'Tu gente'"), ("p3", m[2][2], "'La plataforma'"), ("p4", m[2][3], "'Y queda'")]) + '''
        [["#p1", p1], ["#p2", p2], ["#p3", p3], ["#p4", p4]].forEach(function (x, k) {
          tl.fromTo(x[0], { opacity: 0, x: k % 2 ? 160 : -160, scale: 0.94 }, { opacity: 1, x: 0, scale: 1, duration: 0.55, ease: "back.out(1.6)" }, L(x[1]) - 0.1);
          tl.fromTo(x[0] + " .num", { backgroundColor: "rgba(172,132,29,0.12)" }, { backgroundColor: "rgba(172,132,29,0.85)", color: "#111", duration: 0.3 }, L(x[1]));
        });''' + SALIDA)


def e_certificado(v, m, S, FINE, ult):
    return ('''        #tit { position: absolute; left: 108px; top: 300px; width: 864px; font-size: 60px; }
        #cert { position: absolute; left: 110px; top: 560px; width: 860px; height: 720px; background: #fff; color: #1a1a1a; border-radius: 14px;
          box-shadow: 0 40px 90px rgba(0,0,0,0.6); padding: 54px 60px; text-align: center; }
        #cert .marco { position: absolute; inset: 18px; border: 2px solid #e2e2e2; border-radius: 8px; }
        #cert img { height: 64px; width: auto; margin-bottom: 18px; }
        #cert h3 { font-family: "Montserrat"; font-weight: 800; font-size: 52px; letter-spacing: 0.06em; margin-bottom: 8px; }
        #cert .p { display: block; font-size: 22px; color: #666; margin: 6px 0; }
        #cert .campo { display: block; width: fit-content; margin: 8px auto; font-family: "Montserrat"; font-weight: 800; font-size: 34px; padding: 4px 16px; border-radius: 8px; }
        #cert .linea { width: 360px; height: 2px; background: #999; margin: 26px auto 8px; }
        #pdf { position: absolute; left: 108px; top: 1380px; width: 864px; text-align: center; font-size: 38px; color: #e6e6e6; }
''', '''          <div id="tit" class="t">
%s
          </div>
          <div id="cert"><div class="marco"></div>
            <img src="assets/logo/riskmann_logo_color.png" alt="RiskMann">
            <h3>CERTIFICADO</h3>
            <div class="p">concedido a</div>
            <div class="campo" id="k1">NOMBRE DEL TRABAJADOR</div>
            <div class="campo" id="k2" style="font-size:24px;font-family:'Open Sans';font-weight:600">Documento de identidad</div>
            <div class="p">por haber concluido de manera satisfactoria la capacitación:</div>
            <div class="campo" id="k3" style="font-size:30px">CAPACITACIÓN PARA CICLISTAS</div>
            <div class="campo" id="k4" style="font-size:24px;font-family:'Open Sans';font-weight:600">Fecha de aprobación</div>
            <div class="linea"></div><div class="p">Representante legal · SOFU</div>
          </div>
          <div id="pdf">Un PDF para cada persona que aprueba.</div>''' % P.lineas(["Quien aprueba,", '<span class="oro">recibe su certificado</span>']),
        cab(S, FINE, ult, [("a", m[2][0], "'Con RiskMann'"), ("k1", m[2][1], "'nombre'"), ("k2", m[2][2], "'documento'"),
                           ("k3", m[2][3], "'curso'"), ("k4", m[2][4], "'fecha'")]) + '''
        tl.fromTo("#tit .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a) - 0.1);
        tl.fromTo("#cert", { opacity: 0 }, { opacity: 1, duration: 0.01, ease: "none" }, L(a) + 0.3);   // aparece de golpe mientras sube
        tl.fromTo("#cert", { y: 260, scale: 0.85 }, { y: 0, scale: 1, duration: 0.9, ease: "back.out(1.3)", immediateRender: false }, L(a) + 0.3);
        [["#k1", k1], ["#k2", k2], ["#k3", k3], ["#k4", k4]].forEach(function (x) {
          tl.fromTo(x[0], { backgroundColor: "rgba(172,132,29,0)" }, { backgroundColor: "rgba(172,132,29,0.30)", duration: 0.25, ease: "power2.out" }, L(x[1]) - 0.05);
          tl.to(x[0], { backgroundColor: "rgba(172,132,29,0.10)", duration: 0.6, ease: "power2.inOut" }, L(x[1]) + 0.35);
        });
        tl.fromTo("#pdf", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(k4) + 0.3);''' + SALIDA)


def e_gratis(v, m, S, FINE, ult):
    return ('''        #badge { position: absolute; left: 50%; top: 520px; transform: translateX(-50%); white-space: nowrap; }
        #g { position: absolute; left: 0; top: 640px; width: 1080px; text-align: center; font-family: "Montserrat"; font-weight: 900;
          font-size: 230px; letter-spacing: -0.04em; color: var(--dorado-claro); line-height: 1.1; }
        #hasta { position: absolute; left: 0; top: 960px; width: 1080px; text-align: center; font-family: "Montserrat"; font-weight: 700; font-size: 50px; }
        #anio { position: absolute; left: 0; top: 1040px; width: 1080px; text-align: center; font-family: "Montserrat"; font-weight: 900; font-size: 150px; color: #fff; }
        #halo { position: absolute; left: 90px; top: 520px; width: 900px; height: 900px; border-radius: 50%;
          background: radial-gradient(circle, rgba(217,176,74,0.35) 0%, rgba(4,4,4,0) 65%); opacity: 0; }
''', '''          <div id="halo"></div>
          <div id="badge" class="chip">● Módulo Capacitaciones</div>
          <div id="g">GRATIS</div>
          <div id="hasta">hasta el 1 de enero de</div>
          <div id="anio">2027</div>''',
        cab(S, FINE, ult, [("a", m[1][0], "'El modulo'"), ("g", m[1][1], "'gratis'"), ("h", m[1][2], "'hasta el primero'")]) + '''
        tl.fromTo("#badge", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(a) - 0.1);
        tl.set("#g", { opacity: 1 }, L(g) - 0.05);
        tl.fromTo("#g", { scale: 0.3, opacity: 0 }, { scale: 1.25, opacity: 1, duration: 0.4, ease: "expo.out" }, L(g) - 0.05);
        tl.to("#g", { scale: 1, duration: 0.7, ease: "back.out(2.6)" }, L(g) + 0.35);
        tl.fromTo("#halo", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, L(g) - 0.05);
        tl.to("#halo", { opacity: 0.5, scale: 1.12, duration: 2.5, ease: "sine.inOut" }, L(g) + 0.5);
        tl.fromTo("#hasta", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(h));
        tl.fromTo("#anio", { opacity: 0, scale: 1.5, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power4.out" }, L(h) + 0.9);''' + SALIDA)


def e_cuenta(v, m, S, FINE, ult):
    return ('''        #logo { position: absolute; left: 50%; top: 520px; width: 560px; margin-left: -280px; height: auto; }
        #t1 { position: absolute; left: 108px; top: 820px; width: 864px; text-align: center; font-size: 66px; }
        #t2 { position: absolute; left: 108px; top: 1120px; width: 864px; text-align: center; font-size: 58px; }
''', '''          <img id="logo" src="assets/logo/riskmann_logo_blanco.png" alt="RiskMann">
          <div id="t1" class="t">
%s
          </div>
          <div id="t2" class="t">
%s
          </div>''' % (P.lineas(["Si tu gente ya usa RiskMann,", '<span class="oro">ya tiene la cuenta.</span>']),
                        P.lineas(["Solo falta activar", '<span class="oro">Capacitaciones.</span>'])),
        cab(S, FINE, ult, [("a", m[2][0], "'Si tu gente'"), ("b", m[2][1], "'Solo falta'")]) + '''
        tl.fromTo("#logo", { opacity: 0, y: 30, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }, L(a) - 0.2);
        tl.fromTo("#t1 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.3 }, L(a));
        tl.fromTo("#t2 .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.16 }, L(b) - 0.05);''' + SALIDA)


def e_cta(v, m, S, FINE, ult):
    return ('''        #tit { position: absolute; left: 108px; top: 340px; width: 864px; text-align: center; font-size: 80px; }
        #sub { position: absolute; left: 108px; top: 600px; width: 864px; text-align: center; font-family: "Montserrat"; font-weight: 700;
          font-size: 40px; color: var(--dorado-claro); }
        #boton { position: absolute; left: 50%; top: 720px; transform: translateX(-50%); white-space: nowrap; display: flex; align-items: center; gap: 18px;
          padding: 34px 60px; border-radius: 18px; background: linear-gradient(135deg, #AC841D, #8a6813); color: #fff;
          font-family: "Montserrat"; font-weight: 800; font-size: 44px; box-shadow: 0 26px 70px rgba(172,132,29,0.45); }
        #boton svg { width: 40px; height: 40px; }
        #web { position: absolute; left: 0; top: 880px; width: 1080px; text-align: center; font-size: 36px; font-weight: 600; color: #e6e6e6; }
        #qrbox { position: absolute; left: 50%; top: 990px; margin-left: -150px; width: 300px; padding: 22px 22px 16px; background: #fff; border-radius: 22px; text-align: center; }
        #qrbox img { width: 256px; height: 256px; display: block; }
        #qrbox span { display: block; color: #111; font-family: "Montserrat"; font-weight: 700; font-size: 20px; margin-top: 8px; }
        #logo { position: absolute; left: 50%; top: 1500px; width: 420px; margin-left: -210px; height: auto; }
''', '''          <div id="tit" class="t">
%s
          </div>
          <div id="sub">%s</div>
          <div id="boton">%s <svg viewBox="0 0 40 40"><path d="M8 20 H30 M22 12 L30 20 L22 28" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div id="web">riskmann.com/capacitaciones</div>
          <div id="qrbox"><img src="assets/qr/qr-app-riskmann-com.svg" alt="QR app.riskmann.com"><span>app.riskmann.com</span></div>
          <img id="logo" src="assets/logo/riskmann_logo_blanco.png" alt="RiskMann">''' % (P.lineas(v["cta_titulo"]), html.escape(v["sub"]), html.escape(v["boton"])),
        cab(S, FINE, ult, [("a", m[3][0], "1a marca de la frase CTA"), ("b", m[3][1], "2a marca"), ("FIN", FINE, "fin del video")]) + '''
        tl.fromTo("#tit .l > span", { yPercent: 115 }, { yPercent: 0, duration: 0.7, ease: "expo.out", stagger: 0.14 }, L(a) - 0.1);
        tl.fromTo("#sub", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power4.out" }, L(b));
        tl.fromTo("#boton", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.9)" }, L(b) + 0.3);
        tl.fromTo("#web", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(b) + 0.6);
        tl.fromTo("#qrbox", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(b) + 0.8);
        tl.fromTo("#logo", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7, ease: "expo.out" }, L(b) + 1.0);
        for (var k = 0; L(b) + 1.4 + k * 1.2 < L(FIN) - 0.6; k++) {   // el boton respira (tweens explicitos)
          tl.to("#boton", { scale: 1.045, duration: 0.6, ease: "sine.inOut" }, L(b) + 1.4 + k * 1.2);
          tl.to("#boton", { scale: 1.0, duration: 0.6, ease: "sine.inOut" }, L(b) + 2.0 + k * 1.2);
        }''')


ESC = {"titular": e_titular, "papel": e_papel, "registro": e_registro, "pasos": e_pasos,
       "certificado": e_certificado, "gratis": e_gratis, "cuenta": e_cuenta, "cta": e_cta}


def fondo(FIN, cortes):
    fichas = [(80, 260, 0), (860, 420, 1), (120, 1500, 2), (880, 1320, 0), (560, 150, 2), (720, 1760, 1)]
    icon = ['<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="24" fill="none" stroke="currentColor" stroke-width="4"/><path d="M19 31 L27 38 L42 22" fill="none" stroke="currentColor" stroke-width="4"/></svg>',
            '<svg viewBox="0 0 60 60"><rect x="6" y="12" width="48" height="36" rx="6" fill="none" stroke="currentColor" stroke-width="4"/><path d="M14 24 H40 M14 32 H32" stroke="currentColor" stroke-width="4"/><circle cx="44" cy="40" r="6" fill="currentColor"/></svg>',
            '<svg viewBox="0 0 60 60"><rect x="8" y="8" width="44" height="44" rx="12" fill="none" stroke="currentColor" stroke-width="4"/><path d="M25 21 L39 30 L25 39 Z" fill="currentColor"/></svg>']
    fichasH = "\n".join('          <div class="ficha" style="left:%dpx;top:%dpx">%s</div>' % (x, y, icon[k]) for x, y, k in fichas)
    return ('''        #base { position: absolute; inset: 0; background: #040404; }
        #brillo { position: absolute; left: -300px; top: -200px; width: 1400px; height: 1400px; border-radius: 50%;
          background: radial-gradient(circle, rgba(172,132,29,0.26) 0%, rgba(172,132,29,0.07) 40%, rgba(4,4,4,0) 68%); }
        #brillo2 { position: absolute; left: 200px; top: 1100px; width: 1300px; height: 1300px; border-radius: 50%;
          background: radial-gradient(circle, rgba(25,39,68,0.55) 0%, rgba(4,4,4,0) 65%); }
        .ficha { position: absolute; width: 110px; height: 110px; color: rgba(217,176,74,0.28); }
        .ficha svg { width: 100%; height: 100%; }
        #barrido { position: absolute; left: -200px; top: 0; width: 160px; height: 1920px; opacity: 0;
          background: linear-gradient(90deg, rgba(217,176,74,0), rgba(217,176,74,0.22), rgba(217,176,74,0)); transform: skewX(-18deg); }
''', '''          <div id="base"></div><div id="brillo"></div><div id="brillo2"></div>
%s
          <div id="barrido"></div>''' % fichasH, '''        var FIN = %s, CORTES = %s;
        tl.fromTo("#brillo", { x: 0, y: 0 }, { x: 300, y: 380, duration: FIN, ease: "none" }, 0);
        tl.fromTo("#brillo2", { x: 0, y: 0 }, { x: -260, y: -220, duration: FIN, ease: "none" }, 0);
        gsap.utils.toArray(".ficha").forEach(function (f, i) {
          tl.fromTo(f, { y: 0, rotation: -8 + i * 3 }, { y: -90 - i * 14, rotation: 8 - i * 2, duration: FIN, ease: "none" }, 0);
        });
        CORTES.forEach(function (tc) {
          tl.fromTo("#barrido", { x: 0, opacity: 0 }, { x: 1400, opacity: 1, duration: 0.6, ease: "power2.inOut", immediateRender: false }, tc - 0.3);
          tl.to("#barrido", { opacity: 0, duration: 0.15 }, tc + 0.15);
        });''' % (FIN, json.dumps(cortes)))


def construir():
    for v in SERIE:
        raiz = os.path.join(AQUI, v["carpeta"])
        t = {x["n"]: x for x in json.load(io.open(os.path.join(raiz, "tools", "tiempos-voz.json"), encoding="utf-8"))}
        for d in ("fonts", "logo", "qr", "sfx", "musica"):
            dst = os.path.join(raiz, "assets", d)
            if not os.path.isdir(dst):
                shutil.copytree(os.path.join(PROMO, "assets", d), dst)
        os.makedirs(os.path.join(raiz, "compositions"), exist_ok=True)
        # una frase por escena
        V = {1: ANTES + 0.2}
        for n in (2, 3):
            V[n] = round(V[n - 1] + t[n - 1]["dur"] + GAP_ESCENA, 2)
        FIN = round(V[3] + t[3]["dur"] + COLA, 1)
        m = {n: [round(V[n] + x, 3) for x in t[n]["marcas"].values()] for n in V}
        S = [0.0, round(V[2] - ANTES, 2), round(V[3] - ANTES, 2)]
        FINES = [S[1], S[2], FIN]
        for k in (0, 1):
            assert V[k + 1] + t[k + 1]["dur"] <= FINES[k] - 0.35 + 0.02
        hosts = ['''      <!-- fondo persistente -->
      <div id="fondo" data-composition-id="fondo" data-composition-src="compositions/fondo.html"
        data-track-kind="graphics" data-start="0" data-duration="%s" data-track-index="1"
        data-width="1080" data-height="1920" style="z-index:1"></div>''' % FIN]
        css, cuerpo, js = fondo(FIN, S[1:])
        io.open(os.path.join(raiz, "compositions", "fondo.html"), "w", encoding="utf-8", newline="\n").write(P.sub("fondo", css, cuerpo, js))
        for k, e in enumerate(v["escenas"]):
            css, cuerpo, js = ESC[e](v, m, S[k], FINES[k], k == 2)
            cid = "escena-%d-%s" % (k + 1, e)
            io.open(os.path.join(raiz, "compositions", cid + ".html"), "w", encoding="utf-8", newline="\n").write(P.sub(cid, css, cuerpo, js))
            hosts.append('''      <div id="%s" data-composition-id="%s" data-composition-src="compositions/%s.html"
        data-track-kind="graphics" data-start="%s" data-duration="%s" data-track-index="2"
        data-width="1080" data-height="1920" style="z-index:%d"></div>''' % (cid, cid, cid, S[k], round(FINES[k] - S[k], 2), 10 + k))
        voces = ['      <audio id="voz-%d" src="assets/mezcla/voz-%d.wav" data-start="%.2f" data-duration="%.2f" data-track-index="10" data-volume="1"></audio>'
                 % (n, n, V[n], t[n]["dur"]) for n in V]
        ev = [("golpe", V[1] - 0.05, 0.40), ("whoosh", S[1] - 0.25, 0.30), ("whoosh", S[2] - 0.25, 0.30),
              ("brillo", m[3][1], 0.35), ("pop", m[3][1] + 0.3, 0.35)]
        esc2 = v["escenas"][1]
        if esc2 in ("registro", "pasos"):
            ev += [("pop", x - 0.05, 0.28) for x in m[2][1 if esc2 == "registro" else 0:]]
        if esc2 == "certificado":
            ev += [("brillo", V[2] + 0.3, 0.30)]
        if v["escenas"][0] == "papel":
            ev += [("papel", m[1][1] - 0.05, 0.40)]
        if v["escenas"][0] == "gratis":
            ev += [("brillo", m[1][1] - 0.05, 0.40)]
        ev.sort(key=lambda x: x[1])
        fin_p, cont, efectos = {11: -1.0, 12: -1.0, 13: -1.0}, {}, []
        for nom, t0, g in ev:
            d = P.SFX[nom][1]
            pista = next(p for p in (11, 12, 13) if fin_p[p] <= t0)
            fin_p[pista] = t0 + d
            cont[nom] = cont.get(nom, 0) + 1
            efectos.append('      <audio id="sfx-%s-%d" src="assets/sfx/%s.mp3" data-start="%.2f" data-duration="%.2f" data-track-index="%d" data-volume="%.2f"></audio>'
                           % (nom, cont[nom], nom, t0, d, pista, g))
        ult = V[3] + t[3]["dur"]
        pts = [(0.0, 0.0), (0.2, 0.12), (round(ult, 2), 0.12), (round(ult + 0.35, 2), 0.28), (round(FIN - 0.1, 2), 0.0)]
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": a, "v": b} for a, b in pts]}]}, separators=(",", ":"))
        musica = ('      <audio id="musica-cama" src="assets/musica/cama.mp3" data-start="0" data-duration="%s" data-track-index="14" data-volume="1"\n'
                  '        data-automation="%s"></audio>' % (FIN, html.escape(auto, quote=True)))
        index = '''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
    <style>
      /* RiskMann · Capacitaciones · anuncio "%s" — generado por ../serie.py. Fuente: riskmann.com/capacitaciones. */
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #040404; }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #040404; }
      #root > div { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1080" data-height="1920">
%s

      <!-- VOZ · Carlos (ElevenLabs, semilla fija) -->
%s

      <!-- EFECTOS -->
%s

      <!-- MUSICA · la del promo; baja bajo la voz y sube al final -->
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
        io.open(os.path.join(raiz, "meta.json"), "w").write(json.dumps({"id": "rm-capac-" + v["carpeta"], "name": "rm-capac-" + v["carpeta"]}))
        shutil.copyfile(os.path.join(PROMO, "package.json"), os.path.join(raiz, "package.json"))
        print("%-20s %.1f s  V=%s" % (v["carpeta"], FIN, V))


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso in ("voz", "todo"):
        voz()
    if paso in ("construir", "todo"):
        construir()
