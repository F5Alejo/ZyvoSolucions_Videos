# -*- coding: utf-8 -*-
"""Las siete plantillas animadas que cubren las 88 láminas del curso.

Cada lámina del PPTX trae sus formas con nombre (`title`, `body`,
`target-label-N`, `bar-label-N`, `step-t-N`, `q-text-N`, `photo-caption`…). La
firma de nombres decide la plantilla; los textos y la narración deciden el
contenido y los tiempos. Ninguna lámina se escribe a mano.

Cada plantilla devuelve (css, cuerpo, línea de tiempo) con las marcas ya en
segundos, calculadas por `sincronia.py` sobre la locución vigente.
"""
import re

from base import (AZUL, OLIVA, ORO, ORO_TEXTO, TINTA, TINTA_2, TINTE_AZUL, TINTE_OLIVA, PAPEL,
                  esc, palabras_titulo, fromto)
import sincronia

ENTRA_ARRIBA = '{ opacity: 0, y: 34 }', '{ opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }'
ENTRA_IZQ = '{ opacity: 0, x: -60 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }'
ENTRA_DER = '{ opacity: 0, x: 90 }', '{ opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }'
APARECE = '{ opacity: 0 }', '{ opacity: 1, duration: 0.5, ease: "power1.out" }'


# ---------------------------------------------------------------- lectura del PPTX

def texto(f, k, sep=" "):
    return sep.join(f.get(k, []))


def serie(f, prefijo):
    """Formas numeradas (`bar-label-1`, `q-text-0`…) en orden."""
    claves = [k for k in f if re.fullmatch(re.escape(prefijo) + r"-\d+", k)]
    claves.sort(key=lambda k: int(k.rsplit("-", 1)[1]))
    return [f[k] for k in claves]


def vinetas(f):
    return [re.sub(r"^[•\-•·]\s*", "", p).strip() for p in f.get("body", []) if p.strip()]


def completar(etiquetas, vins):
    """Las etiquetas del mazo vienen cortadas con «…»: se recupera el texto entero
    de la viñeta que empieza igual. El original tiene este defecto en varias láminas."""
    out = []
    for e in etiquetas:
        if e.endswith("…") or e.endswith("..."):
            pref = e.rstrip("….").strip()
            out.append(next((v for v in vins if v.startswith(pref)), pref))
        else:
            out.append(e)
    return out


def pausa(f):
    p = texto(f, "autonomous-pause")
    m = re.match(r"^\s*PAUSA\s+AUT[OÓ]NOMA\s*[·:\-]\s*(.*)$", p, re.I)
    return (m.group(1).strip() if m else p.strip())


def respuesta(f):
    return " ".join(" ".join(v) for k, v in f.items() if k.startswith("CuadroTexto")).strip()


# ---------------------------------------------------------------- piezas comunes

def encabezado(d, ctx, ancho_titulo=1600, kicker=None):
    f = d["formas"]
    titulo = texto(f, "title")
    clase = "k-titulo con-kicker" if kicker else "k-titulo"
    html = ('      <div class="k-seccion" id="k-seccion">%s</div>\n'
            '      <div class="k-pagina" id="k-pagina">%s</div>\n'
            '      <div class="k-regla" id="k-regla" data-layout-ignore></div>\n'
            % (esc(texto(f, "section")), esc(texto(f, "page"))))
    if kicker:
        html += '      <div class="k-kicker" id="k-kicker">%s</div>\n' % esc(kicker)
    # una sola línea siempre que se pueda: el contenido empieza en y=310
    fs = 62 if len(titulo) <= 40 or ancho_titulo < 1600 else (54 if len(titulo) <= 46 else 48)
    html += '      <div class="%s" id="k-titulo" style="width: %dpx; font-size: %dpx">%s</div>\n' % (
        clase, ancho_titulo, fs, palabras_titulo(titulo))

    tl = fromto('"#k-seccion"', '{ opacity: 0, x: -20 }', '{ opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }', 0.15)
    tl += fromto('"#k-pagina"', '{ opacity: 0 }', '{ opacity: 1, duration: 0.45 }', 0.25)
    tl += fromto('"#k-regla"', '{ scaleX: 0 }', '{ scaleX: 1, duration: 0.7, ease: "power2.inOut" }', 0.2)
    if kicker:
        tl += fromto('"#k-kicker"', '{ opacity: 0, y: -10 }', '{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }', 0.35)
    tl += ('      tl.fromTo("#k-titulo .p", { opacity: 0, y: 46, rotationX: -40, transformOrigin: "50%% 100%%" },'
           ' { opacity: 1, y: 0, rotationX: 0, duration: 0.6, ease: "power3.out", stagger: 0.06 }, %.2f);\n' % 0.45)
    return html, tl


def pie(d, ctx, despues_de):
    """Contador, regla dorada y sello, con sus tiempos.

    Sin pausa autónoma ni respuesta: las preguntas al participante van en la
    plataforma, no en el video."""
    f = d["formas"]
    narr = ctx["narracion"]
    html, tl = "", ""
    cuenta = texto(f, "item-count")
    if cuenta:
        html += ('      <div class="k-cuenta" id="k-cuenta"><span class="k-cuenta-n">%s</span>'
                 '<span class="k-cuenta-t">%s</span></div>\n' % (esc(cuenta), esc(texto(f, "item-count-label"))))
        t = min(despues_de + 0.6, narr * 0.75)
        tl += fromto('"#k-cuenta"', '{ opacity: 0, x: -30 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "back.out(2)" }', t)

    html += '      <div class="k-oro" id="k-oro" data-layout-ignore></div>\n'
    html += '      <img class="k-sello" id="k-sello" src="assets/marca/riskmann_logo_color.png" alt="RiskMann" />\n'
    t_oro = min(despues_de + 0.9, narr * 0.78)
    tl += fromto('"#k-oro"', '{ scaleX: 0 }', '{ scaleX: 1, duration: 0.8, ease: "power2.inOut" }', t_oro)
    tl += fromto('"#k-sello"', '{ opacity: 0 }', '{ opacity: 1, duration: 0.6 }', t_oro + 0.3)
    return html, tl


def lista(items, ctx, ancho=820, top=330):
    """Viñetas de la columna izquierda, con tamaño que se ajusta al texto."""
    lineas = sum(max(1, -(-len(i) // 42)) for i in items)
    grande = lineas * 40 + 20 * len(items) <= 430
    fs = 32 if grande else 27
    html = '      <div class="v-lista" style="width: %dpx; top: %dpx">\n' % (ancho, top)
    for k, i in enumerate(items):
        html += ('        <div class="v-item" id="v-i%d"><span class="v-dot"></span>'
                 '<span class="v-t" style="font-size: %dpx">%s</span></div>\n' % (k + 1, fs, esc(i)))
    html += '      </div>\n'
    ts = sincronia.marcas(items, ctx["frases"], ctx["inicios"], desde=1.4)
    tl = "".join(fromto('"#v-i%d"' % (k + 1), ENTRA_IZQ[0], ENTRA_IZQ[1], t) for k, t in enumerate(ts))
    return html, tl, ts


# ---------------------------------------------------------------- las siete plantillas

def portada(d, ctx):
    f = d["formas"]
    css = """
    .c-panel { position: absolute; left: 0; top: 0; width: 760px; height: 1080px; background: %(azul)s; }
    .c-barra { position: absolute; left: 760px; top: 0; width: 40px; height: 1080px; background: %(oro)s;
               transform: scaleY(0); transform-origin: 50%% 0; }
    .c-marco { position: absolute; left: 800px; top: 0; width: 1120px; height: 1080px; overflow: hidden; }
    .c-foto { position: absolute; left: -260px; top: 0; width: 1620px; height: 1080px; }
    .c-kicker { position: absolute; left: 100px; top: 150px; font-size: 22px; font-weight: 800;
                letter-spacing: 0.12em; color: #FFFFFF; opacity: 0; }
    .c-linea { position: absolute; left: 100px; font-size: 84px; font-weight: 800; line-height: 1.05;
               color: #FFFFFF; opacity: 0; white-space: nowrap; }
    .c-sub { position: absolute; left: 100px; top: 540px; font-size: 30px; font-weight: 600; color: #FFFFFF; opacity: 0; }
    .c-regla { position: absolute; left: 100px; top: 600px; width: 460px; height: 4px; background: %(oro)s;
               transform: scaleX(0); transform-origin: 0 50%%; }
    .c-lleva { position: absolute; left: 100px; top: 640px; width: 600px; font-size: 32px; font-weight: 800;
               line-height: 1.3; color: #FFFFFF; opacity: 0; }
    .c-modo { position: absolute; left: 100px; top: 960px; font-size: 22px; font-weight: 700; color: #DCE7F0; opacity: 0; }
    .c-sello { position: absolute; left: 100px; top: 850px; width: 210px; height: 70px; border-radius: 35px;
               background: #FFFFFF; opacity: 0; }
    .c-sello img { position: absolute; left: 24px; top: 10px; height: 50px; }
""" % dict(azul=AZUL, oro=ORO)
    lineas = f.get("cover-title", [])
    lleva = f.get("cover-takeaway", [])
    cuerpo = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <div class="c-marco" data-layout-ignore><img class="c-foto" id="c-foto" src="assets/fotos/l%02d.jpg" alt="Motociclista con casco" /></div>
      <div class="c-panel" data-layout-ignore></div>
      <div class="c-barra" id="c-barra" data-layout-ignore></div>
    </div>
    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">
      <div class="c-kicker" id="c-kicker">%s</div>
%s      <div class="c-sub" id="c-sub">%s</div>
      <div class="c-regla" id="c-regla" data-layout-ignore></div>
      <div class="c-lleva" id="c-lleva">%s</div>
      <div class="c-sello" id="c-sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann" /></div>
      <div class="c-modo" id="c-modo">%s</div>
    </div>
""" % (d["n"], esc(texto(f, "cover-kicker")),
       "".join('      <div class="c-linea" id="c-l%d" style="top: %dpx">%s</div>\n' % (i + 1, 230 + i * 92, esc(l))
               for i, l in enumerate(lineas)),
       esc(texto(f, "cover-subtitle")), "<br />".join(esc(x) for x in lleva), esc(texto(f, "cover-mode")))

    narr, dur = ctx["narracion"], ctx["dur"]
    tl = fromto('"#c-foto"', '{ scale: 1.12, x: 40 }', '{ scale: 1, x: 0, duration: %.1f, ease: "none" }' % dur, 0)
    tl += fromto('"#c-barra"', '{ scaleY: 0 }', '{ scaleY: 1, duration: 0.8, ease: "power3.inOut" }', 0.1)
    tl += fromto('"#c-kicker"', '{ opacity: 0, y: -14 }', '{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }', 0.5)
    for i in range(len(lineas)):
        tl += fromto('"#c-l%d"' % (i + 1), '{ opacity: 0, x: -80 }', '{ opacity: 1, x: 0, duration: 0.7, ease: "power4.out" }', 0.75 + i * 0.22)
    tl += fromto('"#c-sub"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], 1.7)
    tl += fromto('"#c-regla"', '{ scaleX: 0 }', '{ scaleX: 1, duration: 0.6, ease: "power2.out" }', 2.0)
    t_lleva = sincronia.frase_con(ctx["frases"], ctx["inicios"], r"decisi|regres|vida", narr * 0.45)
    tl += fromto('"#c-lleva"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], max(t_lleva, 2.6))
    tl += fromto('"#c-sello"', '{ opacity: 0, scale: 0.8 }', '{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }', 2.4)
    tl += fromto('"#c-modo"', APARECE[0], APARECE[1], max(t_lleva + 1.5, 3.2))
    return css, cuerpo, tl


def repite(etis, vins):
    """¿El gráfico dice lo mismo que las viñetas? Entonces sobran las viñetas."""
    def igual(e):
        re_ = sincronia.raices(e)
        return any(len(re_ & sincronia.raices(v)) >= max(1, len(re_) - 1) for v in vins)
    return len(etis) > 0 and sum(1 for e in etis if igual(e)) >= len(etis) - 1


def foco(ids, ts, fin, props_on, props_off):
    """Acompaña la narración: el ítem del que se habla se destaca y el anterior vuelve."""
    tl = ""
    for k in range(1, len(ids)):
        t = ts[k] + 0.6
        tl += '      tl.to("%s", { %s, duration: 0.35, ease: "power2.out" }, %.2f);\n' % (ids[k - 1], props_off, t)
    for k, i in enumerate(ids):
        tl += '      tl.to("%s", { %s, duration: 0.35, ease: "power2.out" }, %.2f);\n' % (i, props_on, ts[k] + 0.6)
    if ids:
        tl += '      tl.to("%s", { %s, duration: 0.35, ease: "power2.out" }, %.2f);\n' % (ids[-1], props_off, max(fin, ts[-1] + 1.0))
    return tl


def diana(d, ctx):
    f = d["formas"]
    items = vinetas(f)
    h_enc, tl = encabezado(d, ctx)
    n = len(items)
    ts = sincronia.marcas(items, ctx["frases"], ctx["inicios"], desde=1.4)
    cx, cy, rx, ry = 960, 530, 540, 240
    import math
    etiquetas = ""
    for k, it in enumerate(items):
        a = -math.pi / 2 + k * 2 * math.pi / max(n, 1)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        etiquetas += ('      <div class="d-et" id="d-e%d" style="left: %dpx; top: %dpx"><span class="d-k">%02d</span>%s</div>\n'
                      % (k + 1, x - 170, y - 36, k + 1, esc(it)))
    css = """
    .d-anillo { position: absolute; border-radius: 50%%; transform: scale(0); }
    .d-num { position: absolute; left: %(dx)dpx; top: %(dy)dpx; width: 150px; height: 150px; border-radius: 75px;
             background: %(oro)s; transform: scale(0); }
    .d-num span { position: absolute; left: 0; top: 36px; width: 150px; text-align: center; font-size: 70px;
                  font-weight: 900; color: %(azul)s; line-height: 1; }
    .d-et { position: absolute; width: 340px; padding: 12px 18px; text-align: center; font-size: 26px; font-weight: 800;
            line-height: 1.22; color: %(azul)s; background: %(papel)s; border-radius: 10px; opacity: 0;
            box-shadow: 0 6px 18px rgba(31, 78, 121, 0.10); }
    .d-k { display: block; font-size: 17px; font-weight: 900; letter-spacing: 0.1em; color: inherit; opacity: 0.8; margin-bottom: 4px; }
""" % dict(dx=cx - 75, dy=cy - 75, oro=ORO, azul=AZUL, papel=PAPEL, oliva=OLIVA)
    anillos = "".join(
        '      <div class="d-anillo" id="d-a%d" style="left: %dpx; top: %dpx; width: %dpx; height: %dpx; background: %s" data-layout-ignore></div>\n'
        % (i + 1, cx - r, cy - r, 2 * r, 2 * r, c)
        for i, (r, c) in enumerate([(235, TINTE_AZUL), (175, TINTE_OLIVA), (118, "#EFE6CF")]))
    cuerpo = ('    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_enc
              + anillos + '      <div class="d-num" id="d-num"><span>%d</span></div>\n' % n + etiquetas + "{pie}    </div>\n")
    t0 = 1.0
    for i in range(3):
        tl += fromto('"#d-a%d"' % (i + 1), '{ scale: 0 }', '{ scale: 1, duration: 0.8, ease: "back.out(1.6)" }', t0 + i * 0.12)
    tl += fromto('"#d-num"', '{ scale: 0, rotation: -90 }', '{ scale: 1, rotation: 0, duration: 0.6, ease: "back.out(2.2)" }', t0 + 0.4)
    for i in range(3):
        tl += '      tl.to("#d-a%d", { scale: %.3f, duration: %.1f, ease: "sine.inOut", yoyo: true, repeat: %d }, %.2f);\n' % (
            i + 1, 1.04 - i * 0.01, 2.4 + i * 0.3, max(1, int((ctx["dur"] - 4) / (2.4 + i * 0.3)) - 1), 2.2)
    for k, t in enumerate(ts):
        tl += fromto('"#d-e%d"' % (k + 1), '{ opacity: 0, scale: 0.6, y: 20 }', '{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(2)" }', t)
        tl += '      tl.to("#d-num", { scale: 1.1, duration: 0.15, ease: "power2.out", yoyo: true, repeat: 1 }, %.2f);\n' % (t + 0.1)
    tl += foco(["#d-e%d" % (k + 1) for k in range(n)], ts, ctx["narracion"] * 0.8,
               'backgroundColor: "%s", color: "#FFFFFF", scale: 1.06' % AZUL, 'backgroundColor: "%s", color: "%s", scale: 1' % (PAPEL, AZUL))
    h_pie, tl_pie = pie(d, ctx, ts[-1] if ts else 2.0)
    return css, cuerpo.replace("{pie}", h_pie), tl + tl_pie


def _filas(d, ctx, prefijo_n, prefijo_t, escalonado):
    f = d["formas"]
    vins = vinetas(f)
    nums = [x[0] if x else "" for x in serie(f, prefijo_n)]
    etis = completar([" ".join(x) for x in serie(f, prefijo_t)], vins)
    h_enc, tl = encabezado(d, ctx)
    solo = repite(etis, vins)
    if solo:
        h_lista, tl_lista, ts_l = "", "", []
        x0, ancho = 110, 1700
    else:
        h_lista, tl_lista, ts_l = lista(vins, ctx)
        x0, ancho = 1000, 810
    n = len(etis)
    alto = min(80 if solo else 74, int((450 - 14 * (n - 1)) / max(n, 1)))
    paso = (min(90, int(420 / max(n - 1, 1))) if solo else min(56, int(260 / max(n - 1, 1)))) if escalonado else 0
    fs = 30 if solo else 23
    css = """
    .r-fila { position: absolute; border-radius: 6px; opacity: 0; transform-origin: 0 50%%; will-change: transform, opacity; }
    .r-n { position: absolute; left: 0; top: 0; bottom: 0; width: %(wn)dpx; font-size: %(fn)dpx; font-weight: 900;
           display: flex; align-items: center; justify-content: center; border-radius: 6px 0 0 6px; }
    .r-t { position: absolute; left: %(lt)dpx; right: 20px; top: 50%%; transform: translateY(-50%%); font-size: %(fs)dpx;
           font-weight: 800; line-height: 1.2; }
""" % dict(wn=74 if solo else 54, fn=30 if solo else 23, lt=100 if solo else 72, fs=fs)
    cuerpo = '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_enc + h_lista
    for k, e in enumerate(etis):
        y = 310 + k * (alto + 14)
        x = x0 + k * paso
        w = x0 + ancho - x
        if escalonado:
            fondo, tinta, nf = [(AZUL, "#FFFFFF", ORO), (OLIVA, "#FFFFFF", ORO)][k % 2]
        else:
            fondo, tinta, nf = [(TINTE_AZUL, TINTA, AZUL), (TINTE_OLIVA, TINTA, OLIVA)][k % 2]
        cuerpo += ('      <div class="r-fila" id="r-f%d" style="left: %dpx; top: %dpx; width: %dpx; height: %dpx; background: %s; color: %s">'
                   '<div class="r-n" style="background: %s; color: %s">%s</div><div class="r-t">%s</div></div>\n'
                   % (k + 1, x, y, w, alto, fondo, tinta, nf, "#FFFFFF" if not escalonado else AZUL,
                      esc(nums[k] if k < len(nums) else str(k + 1)), esc(e)))
    cuerpo += "{pie}    </div>\n"
    ts = sincronia.marcas(etis, ctx["frases"], ctx["inicios"], desde=1.6)
    tl += tl_lista
    for k, t in enumerate(ts):
        if escalonado:
            tl += fromto('"#r-f%d"' % (k + 1), '{ opacity: 0, x: 120 }', '{ opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }', t)
        else:
            tl += fromto('"#r-f%d"' % (k + 1), '{ opacity: 0, scaleX: 0.2 }', '{ opacity: 1, scaleX: 1, duration: 0.55, ease: "power3.out" }', t)
    ids = ["#r-f%d" % (k + 1) for k in range(n)]
    if escalonado:
        tl += foco(ids, ts, ctx["narracion"] * 0.8, 'x: 24', 'x: 0')
    else:
        tl += foco(ids, ts, ctx["narracion"] * 0.8, 'x: 18, boxShadow: "0 8px 22px rgba(31,78,121,0.18)"', 'x: 0, boxShadow: "0 0 0 rgba(31,78,121,0)"')
    h_pie, tl_pie = pie(d, ctx, max(ts + ts_l) if ts or ts_l else 2.0)
    return css, cuerpo.replace("{pie}", h_pie), tl + tl_pie


def barras(d, ctx):
    return _filas(d, ctx, "bar-num", "bar-label", False)


def escalera(d, ctx):
    return _filas(d, ctx, "step-n", "step-t", True)


def autochequeo(d, ctx):
    f = d["formas"]
    nums = [x[0] for x in serie(f, "q-num")]
    preguntas = serie(f, "q-text")
    h_enc, tl = encabezado(d, ctx, ancho_titulo=1600, kicker=texto(f, "eval-kicker") or "AUTOCHEQUEO")
    instruccion = texto(f, "eval-instruction") or texto(f, "pause-rule")
    css = """
    .q-fila { position: absolute; width: 800px; opacity: 0; will-change: transform, opacity; }
    .q-circ { position: absolute; left: 0; top: 0; width: 56px; height: 56px; border-radius: 28px; }
    .q-circ span { position: absolute; left: 0; top: 16px; width: 56px; text-align: center; font-size: 21px;
                   font-weight: 900; color: #FFFFFF; }
    .q-t { position: absolute; left: 78px; right: 0; top: 2px; font-size: 25px; font-weight: 700; line-height: 1.26; color: %(tinta)s; }
    .q-op { display: block; margin-top: 6px; font-size: 21px; font-weight: 600; color: %(tinta2)s; }
    .q-inst { position: absolute; left: 110px; top: 806px; width: 1480px; font-size: 25px; font-weight: 800;
              color: %(oliva)s; opacity: 0; }
""" % dict(tinta=TINTA, tinta2=TINTA_2, oliva=OLIVA)
    top0 = 350
    cuerpo = '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_enc
    textos_sync = []
    for k, p in enumerate(preguntas):
        col, fila = k % 2, k // 2
        x = 110 + col * 900
        y = top0 + fila * 148
        cabeza = p[0] if p else ""
        ops = " · ".join(p[1:])
        textos_sync.append(" ".join(p))
        color = AZUL if k % 2 == 0 else OLIVA
        cuerpo += ('      <div class="q-fila" id="q-f%d" style="left: %dpx; top: %dpx">'
                   '<div class="q-circ" style="background: %s" data-layout-ignore><span>%s</span></div>'
                   '<div class="q-t">%s%s</div></div>\n'
                   % (k + 1, x, y, color, esc(nums[k] if k < len(nums) else "%02d" % (k + 1)), esc(cabeza),
                      ('<span class="q-op">%s</span>' % esc(ops)) if ops else ""))
    if instruccion:
        cuerpo += '      <div class="q-inst" id="q-inst">%s</div>\n' % esc(instruccion)
    cuerpo += "{pie}    </div>\n"
    narr = ctx["narracion"]
    ts = sincronia.marcas(textos_sync, ctx["frases"], ctx["inicios"], desde=1.5, hasta=narr * 0.6, separacion=0.9)
    for k, t in enumerate(ts):
        tl += fromto('"#q-f%d"' % (k + 1), '{ opacity: 0, y: 30, scale: 0.96 }', '{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }', t)
    if instruccion:
        es_respuesta = re.match(r"^\s*Respuesta", instruccion, re.I)
        t_i = max((ts[-1] if ts else 2) + 1.0, narr * (0.8 if es_respuesta else 0.62))
        tl += fromto('"#q-inst"', '{ opacity: 0, x: -30 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }', t_i)
    h_pie, tl_pie = pie(d, ctx, ts[-1] if ts else 2.0)
    return css, cuerpo.replace("{pie}", h_pie), tl + tl_pie


def foto(d, ctx):
    f = d["formas"]
    vins = vinetas(f)
    h_enc, tl = encabezado(d, ctx, ancho_titulo=840)
    h_lista, tl_lista, ts = lista(vins, ctx, ancho=820, top=350)
    css = """
    .f-borde { position: absolute; left: 986px; top: 140px; width: 14px; height: 640px; background: %(oro)s;
               transform: scaleY(0); transform-origin: 50%% 0; }
    .f-marco { position: absolute; left: 1000px; top: 140px; width: 810px; height: 640px; overflow: hidden;
               clip-path: inset(0 100%% 0 0); }
    .f-img { position: absolute; left: -75px; top: -20px; width: 960px; height: 680px; object-fit: cover; }
    .f-cap { position: absolute; left: 110px; top: 734px; font-size: 22px; font-weight: 800; letter-spacing: 0.12em;
             color: %(oliva)s; opacity: 0; }
""" % dict(oro=ORO, oliva=OLIVA)
    cuerpo = ('    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n' + h_enc + h_lista
              + '      <div class="f-borde" id="f-borde" data-layout-ignore></div>\n'
              + '      <div class="f-marco" id="f-marco" data-layout-ignore><img class="f-img" id="f-img" src="assets/fotos/l%02d.jpg" alt="Motociclista en la vía" /></div>\n' % d["n"]
              + ('      <div class="f-cap" id="f-cap">%s</div>\n' % esc(texto(f, "photo-caption")) if texto(f, "photo-caption") else "")
              + "{pie}    </div>\n")
    dur = ctx["dur"]
    tl += fromto('"#f-borde"', '{ scaleY: 0 }', '{ scaleY: 1, duration: 0.6, ease: "power3.inOut" }', 0.5)
    tl += fromto('"#f-marco"', '{ clipPath: "inset(0 100% 0 0)" }', '{ clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power3.inOut" }', 0.8)
    tl += fromto('"#f-img"', '{ scale: 1.14 }', '{ scale: 1, duration: %.1f, ease: "none" }' % dur, 0)
    tl += tl_lista
    if texto(f, "photo-caption"):
        tl += fromto('"#f-cap"', '{ opacity: 0, x: -20 }', '{ opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }', (ts[-1] if ts else 2) + 0.7)
    h_pie, tl_pie = pie(d, ctx, ts[-1] if ts else 2.0)
    return css, cuerpo.replace("{pie}", h_pie), tl + tl_pie


def cierre(d, ctx):
    f = d["formas"]
    css = """
    .z-fondo { position: absolute; inset: 0; background: %(azul)s; }
    .z-kicker { position: absolute; left: 0; top: 290px; width: 1920px; text-align: center; font-size: 26px;
                font-weight: 900; letter-spacing: 0.2em; color: %(oro)s; opacity: 0; }
    .z-linea { position: absolute; left: 0; width: 1920px; text-align: center; font-size: 96px; font-weight: 800;
               line-height: 1; color: #FFFFFF; opacity: 0; }
    .z-cuerpo { position: absolute; left: 0; top: 590px; width: 1920px; text-align: center; font-size: 32px;
                font-weight: 600; line-height: 1.4; color: #DCE7F0; opacity: 0; }
    .z-seq { position: absolute; left: 0; top: 760px; width: 1920px; display: flex; justify-content: center; gap: 46px; }
    .z-w { font-size: 40px; font-weight: 900; letter-spacing: 0.08em; color: %(oro)s; opacity: 0; display: inline-block; }
    .z-sello { position: absolute; left: 855px; top: 900px; width: 210px; height: 70px; border-radius: 35px;
               background: #FFFFFF; opacity: 0; }
    .z-sello img { position: absolute; left: 24px; top: 10px; height: 50px; }
""" % dict(azul=AZUL, oro=ORO)
    lineas = f.get("close-title", [])
    palabras = [w.strip() for w in re.split(r"·", texto(f, "close-sequence")) if w.strip()]
    cuerpo = ('    <div class="clip capa z-fondo" data-start="0" data-duration="{d}" data-track-index="1"></div>\n'
              '    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">\n'
              '      <div class="z-kicker" id="z-kicker">%s</div>\n' % esc(texto(f, "close-kicker"))
              + "".join('      <div class="z-linea" id="z-l%d" style="top: %dpx">%s</div>\n' % (i + 1, 360 + i * 104, esc(l))
                        for i, l in enumerate(lineas))
              + '      <div class="z-cuerpo" id="z-cuerpo">%s</div>\n' % "<br />".join(esc(x) for x in f.get("close-body", []))
              + '      <div class="z-seq">%s</div>\n' % "".join('<span class="z-w" id="z-w%d">%s</span>' % (i + 1, esc(w)) for i, w in enumerate(palabras))
              + '      <div class="z-sello" id="z-sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann" /></div>\n'
              + '    </div>\n')
    narr = ctx["narracion"]
    tl = fromto('"#z-kicker"', '{ opacity: 0, y: -16 }', '{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }', 0.4)
    for i in range(len(lineas)):
        tl += fromto('"#z-l%d"' % (i + 1), '{ opacity: 0, y: 60, scale: 0.94 }', '{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power4.out" }', 0.8 + i * 0.3)
    t_c = sincronia.frase_con(ctx["frases"], ctx["inicios"], r"familia|organizaci|protege", narr * 0.3)
    tl += fromto('"#z-cuerpo"', ENTRA_ARRIBA[0], ENTRA_ARRIBA[1], max(t_c, 2.2))
    base = max(narr * 0.55, t_c + 2)
    for i in range(len(palabras)):
        tl += fromto('"#z-w%d"' % (i + 1), '{ opacity: 0, y: 30, scale: 0.6 }', '{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2.4)" }', base + i * 0.7)
    tl += fromto('"#z-sello"', '{ opacity: 0, scale: 0.8 }', '{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }', base + len(palabras) * 0.7 + 0.5)
    return css, cuerpo, tl


def elegir(d):
    f = d["formas"]
    if "cover-title" in f:
        return "portada", portada
    if "close-title" in f:
        return "cierre", cierre
    if any(k.startswith("q-text") for k in f):
        return "autochequeo", autochequeo
    if any(k.startswith("target-label") for k in f):
        return "diana", diana
    if any(k.startswith("bar-label") for k in f):
        return "barras", barras
    if any(k.startswith("step-t") for k in f):
        return "escalera", escalera
    if "photo-caption" in f:
        return "foto", foto
    raise ValueError("lámina %d sin plantilla" % d["n"])
