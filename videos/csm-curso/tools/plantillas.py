# -*- coding: utf-8 -*-
"""Plantillas animadas del curso «Conducción Segura y Manejo Defensivo».

Seis formas cubren todas las láminas que entran al video:

- `portada` (1) y `final` (55): foto a sangre con velo azul noche.
- `objetivo` (2): objetivo, foto y las cuatro competencias.
- `ruta` (3): los doce módulos en mosaico.
- `parte` (las 36 láminas de módulo, partes 1 a 3): banda con el código,
  dos columnas de viñetas, foto (o el icono del módulo cuando el PPTX solo trae
  el recuadro de video interactivo), franja amarilla y dos tarjetas.
- `marco` (54): las seis normas de referencia.

Cada aparición cae sobre la frase de la narración que la nombra (`sincronia.py`).
"""
import re

from base import AZUL, NOCHE, AMARILLO, HIELO, PAPEL, TINTA, TINTA_2, esc, palabras, fromto
import sincronia

ENTRA_IZQ = '{ opacity: 0, x: -40 }', '{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }'
ENTRA_ARRIBA = '{ opacity: 0, y: 30 }', '{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }'
POP = '{ opacity: 0, scale: 0.85 }', '{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }'


def t(f, k, sep=" "):
    return sep.join(f.get(k, []))


def sello(tiempo):
    html = '      <div class="sello" id="sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann" /></div>\n'
    return html, fromto('"#sello"', '{ opacity: 0 }', '{ opacity: 1, duration: 0.6 }', tiempo)


def foco(ids, ts, fin, on, off):
    """El elemento del que habla la voz se destaca y el anterior vuelve."""
    tl = ""
    for k, i in enumerate(ids):
        tl += '      tl.to("%s", { %s, duration: 0.3, ease: "power2.out" }, %.2f);\n' % (i, on, ts[k] + 0.5)
        salida = ts[k + 1] + 0.5 if k + 1 < len(ids) else max(fin, ts[k] + 1.2)
        tl += '      tl.to("%s", { %s, duration: 0.3, ease: "power2.out" }, %.2f);\n' % (i, off, salida)
    return tl


# ---------------------------------------------------------------- banda superior

BANDA_CSS = """
    .b-banda { position: absolute; left: 0; top: 0; width: 1920px; height: 170px; background: %(azul)s; }
    .b-cod { position: absolute; left: 0; top: 0; width: 170px; height: 170px; background: %(amarillo)s;
             transform: scale(0); transform-origin: 0 0; }
    .b-cod span { position: absolute; left: 0; top: 56px; width: 170px; text-align: center; font-size: 46px;
                  font-weight: 900; color: %(noche)s; }
    .b-tit { position: absolute; left: 210px; top: 34px; width: 1440px; font-size: 42px; font-weight: 800;
             line-height: 1.12; color: #FFFFFF; }
    .b-tit .p { display: inline-block; opacity: 0; }
    .b-sub { position: absolute; left: 210px; top: 124px; font-size: 20px; font-weight: 600; color: %(hielo)s; opacity: 0; }
    .b-ico { position: absolute; left: 1730px; top: 35px; width: 100px; height: 100px; opacity: 0; }
""" % dict(azul=AZUL, amarillo=AMARILLO, noche=NOCHE, hielo=HIELO)


def banda(titulo, sub, codigo=None, icono=None):
    """Banda azul con el código, el título y el icono del módulo. Los textos van
    dentro de la banda: así el fondo sobre el que se leen es el azul, también
    para la verificación de contraste."""
    html = '      <div class="b-banda" id="b-banda">\n'
    if codigo:
        html += '        <div class="b-cod" id="b-cod" data-layout-ignore><span>%s</span></div>\n' % esc(codigo)
    izq = 210 if codigo else 70
    top = 34 if sub else 58
    html += '        <div class="b-tit" id="b-tit" style="left: %dpx; top: %dpx">%s</div>\n' % (izq, top, palabras(titulo))
    if sub:
        html += '        <div class="b-sub" id="b-sub" style="left: %dpx">%s</div>\n' % (izq, esc(sub))
    if icono:
        html += '        <img class="b-ico" id="b-ico" src="assets/iconos/%s" alt="" />\n' % icono
    html += '      </div>\n'
    tl = fromto('"#b-banda"', '{ yPercent: -100 }', '{ yPercent: 0, duration: 0.6, ease: "power3.out" }', 0.0)
    if codigo:
        tl += fromto('"#b-cod"', '{ scale: 0 }', '{ scale: 1, duration: 0.5, ease: "back.out(1.6)" }', 0.3)
    tl += ('      tl.fromTo("#b-tit .p", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, '
           'ease: "power3.out", stagger: 0.05 }, 0.45);\n')
    if sub:
        tl += fromto('"#b-sub"', '{ opacity: 0, x: -20 }', '{ opacity: 1, x: 0, duration: 0.45 }', 0.9)
    if icono:
        tl += fromto('"#b-ico"', '{ opacity: 0, scale: 0.4, rotation: -30 }',
                     '{ opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2)" }', 0.7)
    return html, tl


# ---------------------------------------------------------------- lámina de módulo

PARTE_CSS = """
    .m-col { position: absolute; top: 215px; width: 560px; }
    .m-h { font-size: 25px; font-weight: 800; color: %(azul)s; margin-bottom: 14px; opacity: 0; }
    .m-item { position: relative; padding: 6px 10px 6px 34px; margin-bottom: 6px; border-radius: 6px;
              font-size: 21px; font-weight: 600; line-height: 1.26; color: %(tinta)s; opacity: 0; }
    .m-item::before { content: ""; position: absolute; left: 10px; top: 15px; width: 11px; height: 11px;
                      background: %(amarillo)s; }
    .m-foto { position: absolute; left: 1300px; top: 215px; width: 560px; height: 360px; overflow: hidden;
              border-radius: 8px; clip-path: inset(0 100%% 0 0); }
    .m-foto img { position: absolute; left: -30px; top: -20px; width: 620px; height: 400px; object-fit: cover; }
    .m-ico { position: absolute; left: 1300px; top: 215px; width: 560px; height: 360px; border-radius: 8px;
             background: %(azul)s; clip-path: inset(0 100%% 0 0); }
    .m-ico img { position: absolute; left: 190px; top: 60px; width: 180px; height: 180px; }
    .m-ico span { position: absolute; left: 0; top: 262px; width: 560px; text-align: center; font-size: 26px;
                  font-weight: 900; letter-spacing: 0.12em; color: %(amarillo)s; }
    .m-franja { position: absolute; left: 60px; top: 628px; width: 1800px; height: 78px; background: %(amarillo)s;
                border-radius: 6px; transform: scaleX(0); transform-origin: 0 50%%; }
    .m-franja-t { position: absolute; left: 92px; top: 628px; width: 1740px; height: 78px; display: flex;
                  align-items: center; font-size: 24px; font-weight: 800; color: %(noche)s; opacity: 0; }
    .m-card { position: absolute; top: 740px; width: 880px; height: 200px; background: %(papel)s; border-radius: 8px;
              box-shadow: 0 6px 20px rgba(20, 25, 63, 0.10); opacity: 0; }
    .m-card .l { position: absolute; left: 32px; top: 28px; font-size: 18px; font-weight: 900; letter-spacing: 0.14em;
                 color: %(tinta2)s; }
    .m-card .x { position: absolute; left: 32px; top: 66px; width: 816px; font-size: 23px; font-weight: 500;
                 line-height: 1.3; color: %(tinta)s; }
    .m-card .s { position: absolute; left: 32px; top: 146px; width: 816px; font-size: 23px; font-weight: 800;
                 color: %(azul)s; }
""" % dict(azul=AZUL, tinta=TINTA, amarillo=AMARILLO, noche=NOCHE, papel=PAPEL, tinta2=TINTA_2)


def parte(d, ctx):
    f = d["formas"]
    sub = re.sub(r"Parte (\d) de 4", r"Parte \1", t(f, "Text 4"))
    h_b, tl = banda(t(f, "Text 3"), sub, t(f, "Text 2"), d.get("icono"))

    col1 = f.get("Text 6", [])
    # la pregunta de la «Decisión crítica» no va: el video no pregunta
    col2 = [x for x in f.get("Text 8", []) if not x.strip().startswith("¿")]
    cuerpo = '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_b
    for c, (izq, cab, items) in enumerate([(60, t(f, "Text 5"), col1), (680, t(f, "Text 7"), col2)]):
        cuerpo += '      <div class="m-col" style="left: %dpx">\n        <div class="m-h" id="m-h%d">%s</div>\n' % (izq, c + 1, esc(cab))
        for k, it in enumerate(items):
            cuerpo += '        <div class="m-item" id="m-i%d-%d">%s</div>\n' % (c + 1, k + 1, esc(it))
        cuerpo += '      </div>\n'
    if d.get("foto"):
        cuerpo += ('      <div class="m-foto" id="m-foto" data-layout-ignore><img id="m-img" src="assets/fotos/%s" alt="" /></div>\n'
                   % d["foto"])
    else:
        cuerpo += ('      <div class="m-ico" id="m-foto" data-layout-ignore><img src="assets/iconos/%s" alt="" /><span>%s</span></div>\n'
                   % (d.get("icono"), esc(t(f, "Text 2"))))
    cuerpo += '      <div class="m-franja" id="m-franja" data-layout-ignore></div>\n'
    cuerpo += '      <div class="m-franja-t" id="m-franja-t">%s</div>\n' % esc(t(f, "Text 10"))
    for c, (izq, l, x, s) in enumerate([(60, "Text 12", "Text 13", "Text 14"), (980, "Text 16", "Text 17", "Text 18")]):
        cuerpo += ('      <div class="m-card" id="m-c%d" style="left: %dpx"><div class="l">%s</div>'
                   '<div class="x">%s</div><div class="s">%s</div></div>\n'
                   % (c + 1, izq, esc(t(f, l)), esc(t(f, x)), esc(t(f, s))))
    h_s, tl_s = sello(ctx["narracion"] * 0.9)
    cuerpo += h_s + "    </div>\n"

    # orden de aparición = orden de lectura de la lámina
    n1, n2 = len(col1), len(col2)
    ids = (["#m-i1-%d" % (k + 1) for k in range(n1)] + ["#m-i2-%d" % (k + 1) for k in range(n2)]
           + ["#m-franja-t", "#m-c1", "#m-c2"])
    tarjetas = [t(f, "Text 10"), t(f, "Text 13") + " " + t(f, "Text 14"), t(f, "Text 17") + " " + t(f, "Text 18")]
    narr = ctx["narracion"]
    if narr / float(n1 + n2 + 3) >= 3.0:
        # lámina larga (Parte 1): cada viñeta entra cuando la voz la nombra
        ts = sincronia.marcas(col1 + col2 + tarjetas, ctx["frases"], ctx["inicios"],
                              desde=1.5, hasta=narr * 0.9, separacion=0.45)
    else:
        # lámina corta (Partes 2 y 3, ~25 s): trece entradas sueltas no caben, así
        # que cada columna entra como bloque, con sus viñetas en cascada
        g = sincronia.marcas([" ".join(col1), " ".join(col2)] + tarjetas, ctx["frases"], ctx["inicios"],
                             desde=1.4, hasta=narr * 0.7, separacion=1.2)
        ts = ([g[0] + 0.22 * k for k in range(n1)] + [g[1] + 0.22 * k for k in range(n2)] + g[2:])

    dur = ctx["dur"]
    tl += fromto('"#m-foto"', '{ clipPath: "inset(0 100% 0 0)" }', '{ clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power3.inOut" }', 0.8)
    if d.get("foto"):
        tl += fromto('"#m-img"', '{ scale: 1.12 }', '{ scale: 1, duration: %.1f, ease: "none" }' % dur, 0)
    tl += fromto('"#m-h1"', ENTRA_IZQ[0], ENTRA_IZQ[1], max(1.1, ts[0] - 0.4))
    if n2:
        tl += fromto('"#m-h2"', ENTRA_IZQ[0], ENTRA_IZQ[1], ts[n1] - 0.35)
    for k in range(n1 + n2):
        tl += fromto('"%s"' % ids[k], ENTRA_IZQ[0], ENTRA_IZQ[1], ts[k])
    t_fr = max(ts[n1 + n2], ts[n1 + n2 - 1] + 0.6)
    tl += fromto('"#m-franja"', '{ scaleX: 0 }', '{ scaleX: 1, duration: 0.6, ease: "power3.inOut" }', t_fr)
    tl += fromto('"#m-franja-t"', '{ opacity: 0, x: -20 }', '{ opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }', t_fr + 0.35)
    tl += fromto('"#m-c1"', POP[0], POP[1], ts[n1 + n2 + 1])
    tl += fromto('"#m-c2"', POP[0], POP[1], ts[n1 + n2 + 2])
    if narr / float(n1 + n2 + 3) >= 3.0:
        tl += foco(ids[:n1 + n2], ts[:n1 + n2], t_fr, 'backgroundColor: "#FFF1BF"', 'backgroundColor: "rgba(255,241,191,0)"')
    return PARTE_CSS + BANDA_CSS, cuerpo, tl + tl_s


# ---------------------------------------------------------------- portada y final

FOTO_CSS = """
    .p-marco { position: absolute; inset: 0; overflow: hidden; }
    .p-img { position: absolute; left: -60px; top: -40px; width: 2040px; height: 1160px; object-fit: cover; }
    .p-velo { position: absolute; inset: 0;
              background: linear-gradient(90deg, rgba(20,25,63,0.96) 0%%, rgba(20,25,63,0.88) 42%%, rgba(20,25,63,0.35) 100%%); }
    .p-kick { position: absolute; left: 110px; top: 250px; padding: 10px 22px; background: %(amarillo)s; font-size: 22px;
              font-weight: 900; letter-spacing: 0.12em; color: %(noche)s; opacity: 0; }
    .p-lin { position: absolute; left: 110px; font-size: 84px; font-weight: 800; line-height: 1.06; color: #FFFFFF;
             white-space: nowrap; opacity: 0; }
    .p-sub { position: absolute; left: 110px; width: 1100px; font-size: 30px; font-weight: 600; line-height: 1.35;
             color: #FFFFFF; opacity: 0; }
    .p-amar { position: absolute; left: 110px; font-size: 24px; font-weight: 800; color: %(amarillo)s; opacity: 0; }
    .p-peq { position: absolute; left: 110px; font-size: 22px; font-weight: 600; color: %(hielo)s; opacity: 0; }
    .p-sello { position: absolute; left: 110px; top: 930px; width: 190px; height: 62px; border-radius: 31px;
               background: #FFFFFF; opacity: 0; }
    .p-sello img { position: absolute; left: 22px; top: 9px; height: 44px; }
""" % dict(amarillo=AMARILLO, noche=NOCHE, hielo=HIELO)


def _foto_fondo(foto, dur):
    html = ('    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">\n'
            '      <div class="p-marco" data-layout-ignore><img class="p-img" id="p-img" src="assets/fotos/%s" alt="" /></div>\n'
            '      <div class="p-velo" data-layout-ignore></div>\n    </div>\n' % foto)
    tl = fromto('"#p-img"', '{ scale: 1.1, x: 30 }', '{ scale: 1, x: 0, duration: %.1f, ease: "none" }' % dur, 0)
    return html, tl


def portada(d, ctx):
    f = d["formas"]
    h_f, tl = _foto_fondo(d["foto"], ctx["dur"])
    lineas = f.get("Text 4", [])
    cuerpo = h_f + '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n'
    cuerpo += '      <div class="p-kick" id="p-kick">%s</div>\n' % esc(t(f, "Text 3"))
    for i, l in enumerate(lineas):
        cuerpo += '      <div class="p-lin" id="p-l%d" style="top: %dpx">%s</div>\n' % (i + 1, 320 + i * 92, esc(l))
    y = 320 + len(lineas) * 92 + 40
    cuerpo += '      <div class="p-sub" id="p-sub" style="top: %dpx">%s</div>\n' % (y, esc(t(f, "Text 5")))
    cuerpo += '      <div class="p-amar" id="p-amar" style="top: %dpx">%s</div>\n' % (y + 70, esc(t(f, "Text 6")))
    cuerpo += '      <div class="p-peq" id="p-peq" style="top: %dpx">%s</div>\n' % (y + 124, esc(t(f, "Text 7")))
    cuerpo += '      <div class="p-sello" id="p-sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann" /></div>\n'
    cuerpo += '    </div>\n'
    fr, ini, narr = ctx["frases"], ctx["inicios"], ctx["narracion"]
    tl += fromto('"#p-kick"', '{ opacity: 0, x: -30 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }', 0.4)
    for i in range(len(lineas)):
        tl += fromto('"#p-l%d"' % (i + 1), '{ opacity: 0, x: -80 }', '{ opacity: 1, x: 0, duration: 0.7, ease: "power4.out" }', 0.7 + i * 0.25)
    tl += fromto('"#p-sub"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], 1.6)
    t_a = max(sincronia.frase_con(fr, ini, r"Plan Estrat|Seguridad Vial", narr * 0.4), 2.4)
    tl += fromto('"#p-amar"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], t_a)
    t_p = max(sincronia.frase_con(fr, ini, r"doce m[oó]dulos", narr * 0.65), t_a + 1)
    tl += fromto('"#p-peq"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], t_p)
    tl += fromto('"#p-sello"', POP[0], POP[1], 2.2)
    return FOTO_CSS, cuerpo, tl


def final(d, ctx):
    f = d["formas"]
    h_f, tl = _foto_fondo(d["foto"], ctx["dur"])
    lineas = f.get("Text 3", [])
    cuerpo = h_f + '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n'
    cuerpo += '      <div class="p-kick" id="p-kick">%s</div>\n' % esc(t(f, "Text 2"))
    for i, l in enumerate(lineas):
        cuerpo += '      <div class="p-lin" id="p-l%d" style="top: %dpx">%s</div>\n' % (i + 1, 330 + i * 96, esc(l))
    y = 330 + len(lineas) * 96 + 50
    cuerpo += '      <div class="p-sub" id="p-sub" style="top: %dpx">%s</div>\n' % (y, esc(t(f, "Text 4")))
    cuerpo += '      <div class="p-sello" id="p-sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann" /></div>\n'
    cuerpo += '    </div>\n'
    fr, ini, narr = ctx["frases"], ctx["inicios"], ctx["narracion"]
    tl += fromto('"#p-kick"', '{ opacity: 0, x: -30 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }', 0.4)
    for i in range(len(lineas)):
        tl += fromto('"#p-l%d"' % (i + 1), '{ opacity: 0, y: 50 }', '{ opacity: 1, y: 0, duration: 0.8, ease: "power4.out" }', 0.8 + i * 0.35)
    t_s = max(sincronia.frase_con(fr, ini, r"cadena de decisiones|salida laboral", narr * 0.3), 2.0)
    tl += fromto('"#p-sub"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], t_s)
    tl += fromto('"#p-sello"', POP[0], POP[1], max(t_s + 2, narr * 0.7))
    return FOTO_CSS, cuerpo, tl


# ---------------------------------------------------------------- objetivo

OBJ_CSS = """
    .o-txt { position: absolute; left: 70px; top: 225px; width: 1060px; font-size: 27px; font-weight: 500;
             line-height: 1.45; color: %(tinta)s; opacity: 0; }
    .o-ital { position: absolute; left: 70px; top: 455px; width: 1060px; font-size: 23px; font-style: italic;
              font-weight: 600; color: %(azul)s; opacity: 0; }
    .o-sec { position: absolute; left: 70px; top: 510px; width: 1060px; font-size: 22px; font-weight: 700;
             color: %(tinta2)s; opacity: 0; }
    .o-foto { position: absolute; left: 1250px; top: 215px; width: 600px; height: 330px; overflow: hidden; border-radius: 8px;
              clip-path: inset(0 100%% 0 0); }
    .o-foto img { position: absolute; left: -30px; top: -20px; width: 660px; height: 370px; object-fit: cover; }
    .o-cap { position: absolute; left: 1250px; top: 556px; font-size: 19px; font-weight: 700; color: %(azul)s; opacity: 0; }
    .o-card { position: absolute; top: 640px; width: 420px; height: 280px; background: %(papel)s; border-radius: 8px;
              box-shadow: 0 6px 20px rgba(20, 25, 63, 0.10); opacity: 0; overflow: hidden; }
    .o-card .bar { position: absolute; left: 0; top: 0; width: 420px; height: 10px; background: %(amarillo)s; }
    .o-card .n { position: absolute; left: 30px; top: 34px; font-size: 44px; font-weight: 900; color: %(hielo)s; }
    .o-card .k { position: absolute; left: 30px; top: 110px; font-size: 30px; font-weight: 900; color: %(noche)s; }
    .o-card .dsc { position: absolute; left: 30px; top: 165px; width: 360px; font-size: 22px; font-weight: 500;
                   line-height: 1.3; color: %(tinta2)s; }
""" % dict(tinta=TINTA, azul=AZUL, tinta2=TINTA_2, papel=PAPEL, amarillo=AMARILLO, hielo="#4F63A8", noche=NOCHE)


def objetivo(d, ctx):
    f = d["formas"]
    h_b, tl = banda(t(f, "Text 1"), None)
    cards = [(t(f, "Text 6"), t(f, "Text 7"), t(f, "Text 8")), (t(f, "Text 11"), t(f, "Text 12"), t(f, "Text 13")),
             (t(f, "Text 16"), t(f, "Text 17"), t(f, "Text 18")), (t(f, "Text 21"), t(f, "Text 22"), t(f, "Text 23"))]
    cuerpo = '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_b
    cuerpo += '      <div class="o-txt" id="o-txt">%s</div>\n' % esc(t(f, "Text 2"))
    cuerpo += '      <div class="o-ital" id="o-ital">%s</div>\n' % esc(t(f, "Text 3"))
    cuerpo += '      <div class="o-sec" id="o-sec">%s</div>\n' % esc(t(f, "Text 25"))
    cuerpo += '      <div class="o-foto" id="o-foto" data-layout-ignore><img id="o-img" src="assets/fotos/%s" alt="" /></div>\n' % d["foto"]
    cuerpo += '      <div class="o-cap" id="o-cap">%s</div>\n' % esc(t(f, "Text 24"))
    for i, (n, k, ds) in enumerate(cards):
        cuerpo += ('      <div class="o-card" id="o-c%d" style="left: %dpx"><div class="bar"></div><div class="n">%s</div>'
                   '<div class="k">%s</div><div class="dsc">%s</div></div>\n' % (i + 1, 70 + i * 450, esc(n), esc(k), esc(ds)))
    cuerpo += "    </div>\n"
    fr, ini, narr, dur = ctx["frases"], ctx["inicios"], ctx["narracion"], ctx["dur"]
    tl += fromto('"#o-txt"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], 1.2)
    tl += fromto('"#o-foto"', '{ clipPath: "inset(0 100% 0 0)" }', '{ clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power3.inOut" }', 0.9)
    tl += fromto('"#o-img"', '{ scale: 1.12 }', '{ scale: 1, duration: %.1f, ease: "none" }' % dur, 0)
    tl += fromto('"#o-cap"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], 2.0)
    t_i = max(sincronia.frase_con(fr, ini, r"diferencia entre conocer", narr * 0.25), 3.0)
    tl += fromto('"#o-ital"', ENTRA_IZQ[0], ENTRA_IZQ[1], t_i)
    t_c = max(sincronia.frase_con(fr, ini, r"cuatro competencias", narr * 0.5), t_i + 1.5)
    for i in range(4):
        tl += fromto('"#o-c%d"' % (i + 1), '{ opacity: 0, y: 60 }', '{ opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)" }', t_c + 0.5 + i * 1.3)
    t_s = max(sincronia.frase_con(fr, ini, r"secuencia defensiva", narr * 0.75), t_c + 6)
    tl += fromto('"#o-sec"', ENTRA_IZQ[0], ENTRA_IZQ[1], t_s)
    return OBJ_CSS + BANDA_CSS, cuerpo, tl


# ---------------------------------------------------------------- ruta formativa

RUTA_CSS = """
    .r-fondo { position: absolute; inset: 0; background: %(noche)s; }
    .r-tit { position: absolute; left: 90px; top: 80px; font-size: 60px; font-weight: 800; color: #FFFFFF; }
    .r-tit .p { display: inline-block; opacity: 0; }
    .r-sub { position: absolute; left: 90px; top: 168px; width: 1500px; font-size: 24px; font-weight: 500; color: %(hielo)s; opacity: 0; }
    .r-tile { position: absolute; width: 420px; height: 190px; background: %(azul)s; border-radius: 6px; overflow: hidden; opacity: 0; }
    .r-tile .n { position: absolute; left: 0; top: 0; width: 88px; height: 190px; background: %(amarillo)s; }
    .r-tile .n span { position: absolute; left: 0; top: 70px; width: 88px; text-align: center; font-size: 36px;
                      font-weight: 900; color: %(noche)s; }
    .r-tile .l { position: absolute; left: 116px; top: 50%%; width: 280px; transform: translateY(-50%%); font-size: 26px;
                 font-weight: 800; line-height: 1.2; color: #FFFFFF; }
""" % dict(noche=NOCHE, hielo=HIELO, azul=AZUL, amarillo=AMARILLO)


def ruta(d, ctx):
    f = d["formas"]
    tiles = [(t(f, "Text %d" % (4 + i * 4)), t(f, "Text %d" % (5 + i * 4))) for i in range(12)]
    cuerpo = '    <div class="clip capa r-fondo" data-start="0" data-duration="{d}" data-track-index="1"></div>\n'
    cuerpo += '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n'
    cuerpo += '      <div class="r-tit" id="r-tit">%s</div>\n' % palabras(t(f, "Text 0"))
    cuerpo += '      <div class="r-sub" id="r-sub">%s</div>\n' % esc(t(f, "Text 1"))
    for i, (n, l) in enumerate(tiles):
        x, y = 90 + (i % 4) * 445, 280 + (i // 4) * 225
        cuerpo += ('      <div class="r-tile" id="r-t%d" style="left: %dpx; top: %dpx"><div class="n"><span>%s</span></div>'
                   '<div class="l">%s</div></div>\n' % (i + 1, x, y, esc(n), esc(l)))
    h_s, tl_s = sello(ctx["narracion"] * 0.9)
    cuerpo += h_s + "    </div>\n"
    tl = ('      tl.fromTo("#r-tit .p", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.55, '
          'ease: "power3.out", stagger: 0.07 }, 0.3);\n')
    tl += fromto('"#r-sub"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], 1.0)
    ts = sincronia.marcas([l for _, l in tiles], ctx["frases"], ctx["inicios"], desde=2.0,
                          hasta=ctx["narracion"] * 0.7, separacion=0.35)
    for i, tt in enumerate(ts):
        tl += fromto('"#r-t%d"' % (i + 1), '{ opacity: 0, y: 40, scale: 0.92 }',
                     '{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.7)" }', tt)
    return RUTA_CSS, cuerpo, tl + tl_s


# ---------------------------------------------------------------- marco jurídico

MARCO_CSS = """
    .j-card { position: absolute; width: 860px; height: 140px; background: %(papel)s; border-radius: 6px;
              box-shadow: 0 6px 20px rgba(20, 25, 63, 0.08); opacity: 0; overflow: hidden; }
    .j-card .e { position: absolute; left: 0; top: 0; width: 10px; height: 140px; background: %(amarillo)s; }
    .j-card .k { position: absolute; left: 40px; top: 28px; font-size: 28px; font-weight: 900; color: %(azul)s; }
    .j-card .x { position: absolute; left: 40px; top: 76px; width: 790px; font-size: 21px; font-weight: 500;
                 line-height: 1.3; color: %(tinta2)s; }
    .j-nota { position: absolute; left: 70px; top: 760px; width: 1780px; height: 130px; background: %(azul)s; border-radius: 6px;
              padding: 28px 40px; font-size: 23px; font-weight: 600; line-height: 1.4; color: #FFFFFF; opacity: 0; }
""" % dict(papel=PAPEL, amarillo=AMARILLO, azul=AZUL, tinta2=TINTA_2)


def marco(d, ctx):
    f = d["formas"]
    h_b, tl = banda(t(f, "Text 1"), None)
    normas = [(t(f, "Text %d" % (4 + i * 4)), t(f, "Text %d" % (5 + i * 4))) for i in range(6)]
    cuerpo = '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_b
    for i, (k, x) in enumerate(normas):
        cuerpo += ('      <div class="j-card" id="j-c%d" style="left: %dpx; top: %dpx"><div class="e"></div>'
                   '<div class="k">%s</div><div class="x">%s</div></div>\n'
                   % (i + 1, 70 + (i % 2) * 920, 225 + (i // 2) * 170, esc(k), esc(x)))
    cuerpo += '      <div class="j-nota" id="j-nota">%s</div>\n' % esc(t(f, "Text 27"))
    h_s, tl_s = sello(ctx["narracion"] * 0.95)
    cuerpo += h_s + "    </div>\n"
    textos = [k + " " + x for k, x in normas] + [t(f, "Text 27")]
    ts = sincronia.marcas(textos, ctx["frases"], ctx["inicios"], desde=1.4, hasta=ctx["narracion"] * 0.85, separacion=0.6)
    for i in range(6):
        tl += fromto('"#j-c%d"' % (i + 1), '{ opacity: 0, x: %d }' % (-60 if i % 2 == 0 else 60),
                     '{ opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }', ts[i])
    tl += fromto('"#j-nota"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], ts[6])
    return MARCO_CSS + BANDA_CSS, cuerpo, tl + tl_s


def elegir(d):
    n = d["n"]
    if n == 1:
        return "portada", portada
    if n == 2:
        return "objetivo", objetivo
    if n == 3:
        return "ruta", ruta
    if n == 54:
        return "marco", marco
    if n == 55:
        return "final", final
    return "parte", parte
