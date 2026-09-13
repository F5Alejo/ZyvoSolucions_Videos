# -*- coding: utf-8 -*-
"""Lámina 22 · Caso integrador. Una entrega acumula cuatro señales de alerta."""
import cronometro
from base import chrome, envoltura

LAMINA = 22
DUR = cronometro.duracion(LAMINA)

CSS = """
    .a-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 28px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .a-senal { position: absolute; top: 352px; width: 396px; height: 234px; border-radius: 10px;
               background: rgba(172,132,29,0.14); border-top: 5px solid #AC841D;
               opacity: 0; will-change: transform, opacity; }
    .a-t { position: absolute; left: 24px; top: 20px; font-size: 26px; font-weight: 900;
           letter-spacing: 0.08em; color: #D4A62B; }
    .a-q { position: absolute; left: 24px; right: 20px; top: 60px; font-size: 25px;
           font-weight: 800; line-height: 1.24; color: #FFFFFF; }
    .a-d { position: absolute; left: 24px; right: 20px; top: 140px; font-size: 22px;
           font-weight: 500; line-height: 1.3; color: #AEBCD6; }

    .a-cap { position: absolute; left: 128px; top: 622px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #7FE5EC; opacity: 0; }
    .a-acc { position: absolute; top: 664px; height: 76px; padding: 0 22px; display: flex;
             align-items: center; border-radius: 8px; background: rgba(0,200,212,0.12);
             border-left: 5px solid #00C8D4; font-size: 24px; font-weight: 700; color: #FFFFFF;
             opacity: 0; white-space: nowrap; }

    .a-personal { position: absolute; left: 128px; top: 778px; width: 812px; font-size: 25px;
                  font-weight: 600; line-height: 1.3; color: #DCE4F2; opacity: 0; }
    .a-org { position: absolute; left: 980px; top: 778px; width: 812px; font-size: 25px;
             font-weight: 600; line-height: 1.3; color: #DCE4F2; opacity: 0; }
    .a-personal b, .a-org b { color: #D4A62B; font-weight: 800; }
    .a-cierre { position: absolute; left: 128px; top: 878px; width: 1664px; font-size: 29px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

SENALES = [("CARGA", "Bolsa colgada del manubrio", "Altera la dirección y el frenado."),
           ("CLIMA", "Lluvia intensa próxima", "Revisar visibilidad, adherencia y criterio de suspensión."),
           ("DISTRACCIÓN", "Llamada urgente en marcha", "No se atiende en movimiento: detenerse fuera del flujo."),
           ("TRÁFICO", "Camión gira a la derecha", "Lejos del punto ciego y de la trayectoria de giro.")]
SS = "".join(
    '      <div class="a-senal" id="a-s%d" style="left: %dpx">\n'
    '        <div class="a-t">%s</div>\n'
    '        <div class="a-q">%s</div>\n'
    '        <div class="a-d">%s</div>\n'
    '      </div>\n' % (i + 1, 128 + i * 428, t, q, d) for i, (t, q, d) in enumerate(SENALES))

ACCIONES = [("Detenerme", 128), ("Asegurar la carga", 340), ("Revisar clima y ruta", 640),
            ("Informar el retraso", 1000), ("Fuera del punto ciego", 1340)]
AA = "".join('      <div class="a-acc" id="a-a%d" style="left: %dpx">%s</div>\n'
             % (i + 1, x, t) for i, (t, x) in enumerate(ACCIONES))

CUERPO = chrome("22", "CASO INTEGRADOR", "Una entrega acumula <b style=\"color:#D4A62B\">cuatro señales de alerta</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="a-lead" id="a-lead">Ninguna de las cuatro, por separado, parece motivo para detenerse.</div>
""" + SS + """
      <div class="a-cap" id="a-cap">LA DECISIÓN SEGURA INTEGRA VARIAS ACCIONES</div>
""" + AA + """
      <div class="a-personal" id="a-personal"><b>Controles personales:</b> detener, asegurar, revisar,
        informar y posicionarse.</div>
      <div class="a-org" id="a-org"><b>Controles de la organización:</b> tiempos razonables, alternativas
        y canales de comunicación.</div>
      <div class="a-cierre" id="a-cierre">La empresa no debe transferir al ciclista una presión que ella puede evitar.</div>
    </div>
"""

TL = """      /* 0.00 · «una entrega con cuatro señales de alerta» */
      tl.fromTo("#a-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

"""
# una señal por frase: 4.11 · 9.71 · 16.93 · 23.35
for _i, _t in enumerate([4.20, 9.80, 17.02, 23.45]):
    TL += ('      tl.fromTo("#a-s%d", { opacity: 0, y: 40, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, %.2f);\n' % (_i + 1, _t))

TL += """
      /* 30.85 · «la decisión segura integra varias acciones» / 34.14 · las cinco */
      tl.fromTo("#a-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 30.95);
"""
for _i, _t in enumerate([34.25, 35.55, 36.85, 38.15, 39.45]):
    TL += ('      tl.fromTo("#a-a%d", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 45.03 · «separo los controles personales de los organizacionales» */
      tl.fromTo("#a-personal", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 45.15);
      tl.fromTo("#a-org", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 46.20);

      /* 49.41 · «no debe transferir al ciclista una presión que puede evitar» */
      tl.fromTo("#a-cierre", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 52.60);
"""


def escena():
    return envoltura("e22-caso", DUR, CSS, CUERPO, TL, lamina=LAMINA)
