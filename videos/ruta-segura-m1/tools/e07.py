# -*- coding: utf-8 -*-
"""Lámina 07 · Reglas que cambian la decisión en la vía.

Los tiempos están corridos −2.3 s respecto de la medición: la nota del PPTX
arrancaba con el rótulo «GUION DE VOZ — PRIMERA PERSONA», que no se locuta.
"""
import cronometro
from base import chrome, envoltura

LAMINA = 7
DUR = cronometro.duracion(LAMINA)

CSS = """
    .r-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 31px;
              font-weight: 700; color: #FFFFFF; opacity: 0; }
    .r-lead b { color: #D4A62B; font-weight: 900; }
    .r-sub { position: absolute; left: 128px; top: 344px; width: 1664px; font-size: 27px;
             font-weight: 500; color: #AEBCD6; opacity: 0; }

    .r-celda { position: absolute; width: 540px; height: 248px; border-radius: 10px;
               background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
               opacity: 0; will-change: transform, opacity; }
    .r-tit { position: absolute; left: 26px; top: 20px; font-size: 32px; font-weight: 900;
             letter-spacing: 0.06em; color: #D4A62B; }
    .r-raya { position: absolute; left: 26px; top: 68px; width: 56px; height: 4px; background: #00C8D4;
              transform: scaleX(0); transform-origin: 0 50%; }
    .r-txt { position: absolute; left: 26px; right: 24px; top: 94px; font-size: 25px;
             font-weight: 500; line-height: 1.38; color: #DCE4F2; }
"""

REGLAS = [("CARRIL", "Puede ocupar un carril observando las reglas aplicables."),
          ("ANDÉN", "No circular en espacio peatonal salvo autorización o diseño local."),
          ("VISIBILIDAD", "Luz blanca adelante, roja atrás y prenda reflectiva cuando aplica."),
          ("SEÑALES", "Respetar semáforos y anunciar giros; señalizar no da prioridad."),
          ("CASCO", "Mínimo legal más regla territorial; la empresa puede exigirlo certificado y abrochado."),
          ("ASISTIDAS", "Clasificar antes por potencia, velocidad, asistencia y régimen vigente.")]
CELDAS = "".join(
    '      <div class="r-celda" id="r-c%d" style="left: %dpx; top: %dpx">\n'
    '        <div class="r-tit">%s</div>\n'
    '        <div class="r-raya" id="r-r%d" data-layout-ignore></div>\n'
    '        <div class="r-txt">%s</div>\n'
    '      </div>\n' % (i + 1, 120 + (i % 3) * 570, 392 + (i // 3) * 274, t, i + 1, d)
    for i, (t, d) in enumerate(REGLAS))

CUERPO = chrome("07", "MÓDULO 1", "Reglas que cambian <b style=\"color:#D4A62B\">la decisión en la vía</b>",
                "Fuente: documento base; Ley 769/2002, Ley 1811/2016 y normas citadas") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="r-lead" id="r-lead">Como ciclista soy <b>conductor y actor vial.</b></div>
      <div class="r-sub" id="r-sub">Respeto señales, semáforos, prelaciones y órdenes de la autoridad.</div>
""" + CELDAS + """    </div>
"""

TL = """      /* 5.27 · «Como ciclista soy conductor y actor vial» */
      tl.fromTo("#r-lead", { opacity: 0, x: -28 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 5.40);
      /* 7.80 · «respeto señales, semáforos, prelaciones y órdenes de la autoridad» */
      tl.fromTo("#r-sub", { opacity: 0, x: -28 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 7.95);

"""
# 13.93 carril · 20.50 andén · 28.49 visibilidad · 38.67 señales · 44.22 casco · 57.56 asistidas
for _i, _t in enumerate([14.10, 20.50, 28.65, 38.85, 44.40, 57.75]):
    TL += ('      tl.fromTo("#r-c%d", { opacity: 0, y: 46, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, %.2f);\n'
           '      tl.fromTo("#r-r%d", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t, _i + 1, _t + 0.28))


def escena():
    return envoltura("e07-reglas", DUR, CSS, CUERPO, TL, lamina=LAMINA)
