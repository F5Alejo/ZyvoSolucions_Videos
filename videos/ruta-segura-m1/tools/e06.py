# -*- coding: utf-8 -*-
"""Lámina 06 · Sistema Seguro. Las capas que impiden que un error termine en daño grave."""
from base import chrome, envoltura

DUR = 59

CSS = """
    .c-hecho { position: absolute; top: 300px; width: 820px; height: 104px; border-radius: 8px;
               background: rgba(174,188,214,0.10); border-left: 5px solid #AC841D;
               opacity: 0; will-change: transform, opacity; }
    .c-hecho span { position: absolute; left: 26px; right: 22px; top: 22px; font-size: 27px;
                    font-weight: 700; line-height: 1.3; color: #FFFFFF; }

    .c-barrera { position: absolute; left: 128px; top: 430px; width: 1664px; font-size: 32px;
                 font-weight: 800; color: #00C8D4; opacity: 0; }

    .c-capa { position: absolute; left: 128px; width: 1664px; height: 66px; border-radius: 6px;
              background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
              opacity: 0; will-change: transform, opacity; }
    .c-capa-t { position: absolute; left: 26px; top: 17px; font-size: 29px; font-weight: 900;
                letter-spacing: 0.06em; color: #FFFFFF; white-space: nowrap; }
    .c-capa-d { position: absolute; left: 524px; right: 24px; top: 20px; font-size: 25px;
                font-weight: 500; color: #AEBCD6; }

    .c-claim { position: absolute; left: 128px; top: 884px; width: 1664px; font-size: 29px;
               font-weight: 800; line-height: 1.2; color: #FFFFFF; opacity: 0; }
    .c-claim b { color: #D4A62B; font-weight: 900; }
    .c-cierre { position: absolute; left: 128px; top: 884px; width: 1664px; font-size: 29px;
                font-weight: 800; line-height: 1.2; color: #00C8D4; opacity: 0; }
"""

HECHOS = [("Las personas pueden cometer errores.", 128),
          ("El cuerpo humano tiene una tolerancia limitada al impacto.", 972)]
HH = "".join('      <div class="c-hecho" id="c-h%d" style="left: %dpx"><span>%s</span></div>\n'
             % (i + 1, x, t) for i, (t, x) in enumerate(HECHOS))

CAPAS = [("PERSONA", "Aptitud, atención y conducta."),
         ("BICICLETA", "Diseño, inspección y mantenimiento."),
         ("VÍA + VELOCIDAD", "Determinan la exposición y la gravedad potencial."),
         ("ORGANIZACIÓN", "Rutas, tiempos, autorizaciones, equipos y canales de reporte."),
         ("RESPUESTA POSTERIOR", "Evita que un evento ya ocurrido empeore.")]
CP = "".join('      <div class="c-capa" id="c-c%d" style="top: %dpx">\n'
             '        <div class="c-capa-t">%s</div><div class="c-capa-d">%s</div>\n'
             '      </div>\n' % (i + 1, 494 + i * 78, t, d) for i, (t, d) in enumerate(CAPAS))

CUERPO = chrome("06", "MÓDULO 1",
                "El error es posible; <b style=\"color:#D4A62B\">el daño grave no debe ser inevitable</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + HH + """      <div class="c-barrera" id="c-barrera">Por eso la prevención no puede depender de una única barrera.</div>
""" + CP + """      <div class="c-claim" id="c-claim">Cuando las capas se apoyan entre sí, <b>un error no tiene que terminar en muerte o lesión grave.</b></div>
      <div class="c-cierre" id="c-cierre">Esa es la diferencia entre culpar y gestionar el riesgo.</div>
    </div>
"""

TL = """      /* 2.60 · «Parto de dos hechos» / 4.00 · los dos hechos */
      tl.fromTo("#c-h1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 4.10);
      tl.fromTo("#c-h2", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 6.20);

      /* 9.63 · «la prevención no puede depender de una única barrera» */
      tl.fromTo("#c-barrera", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.55, ease: "power2.out" }, 9.80);

"""
for _i, _t in enumerate([14.50, 18.25, 24.05, 29.45, 35.25]):
    TL += ('      tl.fromTo("#c-c%d", { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 38.86 · «un error no tiene que terminar en muerte o lesión grave» */
      tl.fromTo("#c-claim", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 39.05);

      /* 51.06 · «si una capa falla, las demás deben seguir protegiendo» — pulso sobre las capas */
      tl.to(".c-capa", { x: 16, duration: 0.22, ease: "power2.out", stagger: 0.07 }, 51.20);
      tl.to(".c-capa", { x: 0, duration: 0.34, ease: "power2.inOut", stagger: 0.07 }, 51.50);

      /* 54.52 · «la diferencia entre culpar y gestionar el riesgo» */
      tl.to("#c-claim", { opacity: 0, duration: 0.4, ease: "power1.in" }, 54.30);
      tl.fromTo("#c-cierre", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 54.80);
"""


def escena():
    return envoltura("e06-sistema", DUR, CSS, CUERPO, TL)
