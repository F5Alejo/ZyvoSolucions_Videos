# -*- coding: utf-8 -*-
"""Lámina 03 · Propósito. Los cuatro verbos que ordenan toda la capacitación."""
import cronometro
from base import chrome, envoltura

LAMINA = 3
DUR = cronometro.duracion(LAMINA)

CSS = """
    .v-fila { position: absolute; left: 120px; top: 300px; width: 1680px; height: 300px;
              perspective: 1600px; }
    .v-card { position: absolute; top: 0; width: 396px; height: 300px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
              opacity: 0; will-change: transform, opacity; }
    .v-card-n { position: absolute; left: 26px; top: 22px; font-size: 22px; font-weight: 900;
                letter-spacing: 0.12em; color: #D4A62B; }
    .v-card-t { position: absolute; left: 26px; top: 62px; font-size: 40px; font-weight: 900;
                letter-spacing: 0.02em; color: #FFFFFF; }
    .v-card-r { position: absolute; left: 26px; top: 122px; width: 64px; height: 4px; background: #00C8D4;
                transform: scaleX(0); transform-origin: 0 50%; }
    .v-card-d { position: absolute; left: 26px; right: 24px; top: 152px; font-size: 25px;
                font-weight: 500; line-height: 1.38; color: #AEBCD6; }

    .v-obs { position: absolute; left: 120px; top: 632px; width: 1680px; font-size: 34px;
             font-weight: 700; color: #FFFFFF; opacity: 0; }
    .v-obs b { color: #00C8D4; font-weight: 800; }

    .v-alc { position: absolute; left: 120px; top: 704px; width: 1680px; height: 216px;
             border-radius: 10px; background: rgba(172,132,29,0.12);
             border-left: 6px solid #AC841D; opacity: 0; }
    .v-alc-t { position: absolute; left: 32px; top: 22px; font-size: 24px; font-weight: 900;
               letter-spacing: 0.16em; color: #D4A62B; }
    .v-alc-l { position: absolute; left: 32px; right: 30px; font-size: 27px; font-weight: 500;
               line-height: 1.36; color: #DCE4F2; opacity: 0; }
"""

VERBOS = [("01", "PLANEAR", "Reconocer peligros de ruta y elegir una alternativa."),
          ("02", "INSPECCIONAR", "Detectar fallas críticas y retirar la bicicleta."),
          ("03", "CIRCULAR", "Ser visible, predecible y defensivo."),
          ("04", "RESPONDER", "Proteger, alertar, socorrer y reportar.")]
CARDS = "".join(
    '      <div class="v-card" id="v-c%d" style="left: %dpx">\n'
    '        <div class="v-card-n">%s</div>\n'
    '        <div class="v-card-t">%s</div>\n'
    '        <div class="v-card-r" id="v-r%d" data-layout-ignore></div>\n'
    '        <div class="v-card-d">%s</div>\n'
    '      </div>\n' % (i + 1, i * 428, n, t, i + 1, d) for i, (n, t, d) in enumerate(VERBOS))

CUERPO = chrome("03", "PROPÓSITO",
                "Decidir con seguridad <b style=\"color:#D4A62B\">antes, durante y después</b> del recorrido") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="v-fila">
""" + CARDS + """      </div>

      <div class="v-obs" id="v-obs">Estos verbos son <b>conductas observables</b>, no conocimientos abstractos.</div>

      <div class="v-alc" id="v-alc">
        <div class="v-alc-t">ALCANCE</div>
        <div class="v-alc-l" id="v-a1" style="top: 62px">Síntesis para bicicletas impulsadas por pedales.</div>
        <div class="v-alc-l" id="v-a2" style="top: 106px">Las bicicletas eléctricas o asistidas deben clasificarse antes de autorizarlas: sus requisitos pueden ser diferentes.</div>
        <div class="v-alc-l" id="v-a3" style="top: 156px">Cada empresa ajusta el contenido a sus rutas, su matriz de peligros y las reglas del municipio donde opera.</div>
      </div>
    </div>
"""

TL = ""
for _i, _t in enumerate([5.75, 10.95, 17.90, 22.40]):
    TL += ('      /* verbo %d */\n'
           '      tl.fromTo("#v-c%d", { opacity: 0, y: 60, rotationX: -34, transformOrigin: "50%% 100%%" },'
           ' { opacity: 1, y: 0, rotationX: 0, duration: 0.6, ease: "power3.out" }, %.2f);\n'
           '      tl.fromTo("#v-r%d", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _i + 1, _t, _i + 1, _t + 0.25))

TL += """
      /* 28.28 · «conductas observables, no conocimientos abstractos» */
      tl.fromTo("#v-obs", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 28.45);

      /* 32.96 · «También aclaro el alcance» */
      tl.fromTo("#v-alc", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 33.10);
      tl.fromTo("#v-a1", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 36.40);
      tl.fromTo("#v-a2", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 39.20);
      tl.fromTo("#v-a3", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 48.65);
"""


def escena():
    return envoltura("e03-proposito", DUR, CSS, CUERPO, TL, lamina=LAMINA)
