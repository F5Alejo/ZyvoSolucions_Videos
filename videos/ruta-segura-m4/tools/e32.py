# -*- coding: utf-8 -*-
"""Lámina 32 · Cierre. Una ruta segura se decide antes de pedalear."""
import cronometro
from base import chrome, envoltura

LAMINA = 32
DUR = cronometro.duracion(LAMINA)

CSS = """
    .x-accion { position: absolute; top: 320px; width: 396px; height: 250px; border-radius: 10px;
                background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
                opacity: 0; will-change: transform, opacity; }
    .x-n { position: absolute; left: 26px; top: 22px; font-size: 22px; font-weight: 900;
           letter-spacing: 0.12em; color: #D4A62B; }
    .x-t { position: absolute; left: 26px; top: 60px; font-size: 38px; font-weight: 900;
           letter-spacing: 0.02em; color: #FFFFFF; }
    .x-raya { position: absolute; left: 26px; top: 116px; width: 62px; height: 4px; background: #00C8D4;
              transform: scaleX(0); transform-origin: 0 50%; }
    .x-d { position: absolute; left: 26px; right: 24px; top: 144px; font-size: 24px;
           font-weight: 500; line-height: 1.34; color: #AEBCD6; }

    .x-org { position: absolute; left: 128px; top: 606px; width: 1664px; height: 132px;
             border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
             opacity: 0; }
    .x-org-t { position: absolute; left: 28px; top: 20px; font-size: 23px; font-weight: 900;
               letter-spacing: 0.14em; color: #D4A62B; }
    .x-org-l { position: absolute; left: 28px; right: 26px; top: 58px; font-size: 26px;
               font-weight: 600; line-height: 1.3; color: #DCE4F2; }

    .x-limite { position: absolute; left: 128px; top: 762px; width: 1664px; font-size: 32px;
                font-weight: 900; line-height: 1.24; color: #FFFFFF; opacity: 0; }
    .x-limite b { color: #D4A62B; font-weight: 900; }
    .x-tampoco { position: absolute; left: 128px; top: 822px; width: 1664px; font-size: 25px;
                 font-weight: 600; line-height: 1.3; color: #AEBCD6; opacity: 0; }
    .x-cierre { position: absolute; left: 128px; top: 886px; width: 1664px; font-size: 28px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

ACCIONES = [("01", "INSPECCIONA", "La bicicleta, la ruta y tu estado personal."),
            ("02", "DECIDE", "Continuar, detenerte, reportar o aplicar una alternativa."),
            ("03", "CIRCULA", "Visible y predecible, fuera de puntos ciegos, sin trasladar el riesgo al peatón."),
            ("04", "RESPONDE", "Proteger, alertar, socorrer dentro de tu competencia y reportar.")]
AA = "".join(
    '      <div class="x-accion" id="x-a%d" style="left: %dpx">\n'
    '        <div class="x-n">%s</div>\n'
    '        <div class="x-t">%s</div>\n'
    '        <div class="x-raya" id="x-r%d" data-layout-ignore></div>\n'
    '        <div class="x-d">%s</div>\n'
    '      </div>\n' % (i + 1, 128 + i * 428, n, t, i + 1, d) for i, (n, t, d) in enumerate(ACCIONES))

CUERPO = chrome("32", "CIERRE", "Una ruta segura <b style=\"color:#D4A62B\">se decide antes de pedalear</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + AA + """
      <div class="x-org" id="x-org">
        <div class="x-org-t">Y LO QUE LE CORRESPONDE A LA ORGANIZACIÓN</div>
        <div class="x-org-l">Rutas, tiempos, mantenimiento, autorización, carga, comunicación,
          investigación de incidentes y respuesta.</div>
      </div>

      <div class="x-limite" id="x-limite">Capacitar <b>no reemplaza</b> esos controles materiales.</div>
      <div class="x-tampoco" id="x-tampoco">Tampoco reemplaza una evaluación de aptitud médica, un curso certificado
        de primeros auxilios ni la práctica presencial.</div>
      <div class="x-cierre" id="x-cierre">Repite en voz alta tu compromiso de treinta días e identifica el primer control que aplicarás.</div>
    </div>
"""

TL = ""
# una acción por frase: 2.21 · 6.92 · 13.40 · 21.18
for _i, _t in enumerate([2.31, 7.02, 13.50, 21.28]):
    TL += ('      tl.fromTo("#x-a%d", { opacity: 0, y: 44, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, %.2f);\n'
           '      tl.fromTo("#x-r%d", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t, _i + 1, _t + 0.28))

TL += """
      /* 27.73 · «dependen de la persona, pero también de la organización» */
      tl.fromTo("#x-org", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 27.83);

      /* 41.09 · «capacitar no reemplaza esos controles materiales» */
      tl.fromTo("#x-limite", { opacity: 0, scale: 0.95, transformOrigin: "0% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 41.19);

      /* 44.79 · ni la aptitud médica, ni los primeros auxilios, ni la práctica */
      tl.fromTo("#x-tampoco", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 44.89);

      /* 54.26 · la última invitación */
      tl.fromTo("#x-cierre", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 54.36);
"""


def escena():
    return envoltura("e32-cierre", DUR, CSS, CUERPO, TL, lamina=LAMINA)
