# -*- coding: utf-8 -*-
"""Lámina 14 · La inspección termina en una decisión: apto, con observación o no apto."""
import cronometro
from base import chrome, envoltura

LAMINA = 14
DUR = cronometro.duracion(LAMINA)

CSS = """
    .d-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 29px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .d-card { position: absolute; top: 350px; width: 540px; height: 250px; border-radius: 10px;
              opacity: 0; will-change: transform, opacity; }
    .d-t { position: absolute; left: 26px; top: 22px; font-size: 34px; font-weight: 900;
           letter-spacing: 0.04em; }
    .d-raya { position: absolute; left: 26px; top: 74px; width: 62px; height: 4px;
              transform: scaleX(0); transform-origin: 0 50%; }
    .d-d { position: absolute; left: 26px; right: 24px; top: 100px; font-size: 24px;
           font-weight: 500; line-height: 1.36; color: #DCE4F2; }

    /* verde institucional no existe en la paleta del PPTX: el estado se distingue
       por intensidad de la misma gama, no por un color inventado */
    .d-apto { background: rgba(0,200,212,0.10); border: 1.5px solid rgba(0,200,212,0.45); }
    .d-apto .d-t { color: #7FE5EC; }
    .d-apto .d-raya { background: #00C8D4; }
    .d-obs { background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.32); }
    .d-obs .d-t { color: #DCE4F2; }
    .d-obs .d-raya { background: #AEBCD6; }
    .d-noapto { background: rgba(172,132,29,0.18); border: 1.5px solid #AC841D; }
    .d-noapto .d-t { color: #D4A62B; }
    .d-noapto .d-raya { background: #AC841D; }

    /* las cuatro acciones obligatorias */
    .d-cap { position: absolute; left: 128px; top: 632px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .d-acc { position: absolute; top: 674px; width: 396px; height: 74px; border-radius: 8px;
             background: rgba(172,132,29,0.14); border-left: 5px solid #AC841D;
             opacity: 0; will-change: transform, opacity; }
    .d-acc span { position: absolute; left: 24px; top: 22px; font-size: 27px; font-weight: 800;
                  color: #FFFFFF; }

    .d-veto { position: absolute; left: 128px; top: 782px; width: 1000px; font-size: 27px;
              font-weight: 700; line-height: 1.3; color: #FFFFFF; opacity: 0; }
    .d-veto b { color: #D4A62B; font-weight: 800; }
    .d-org { position: absolute; left: 1160px; top: 782px; width: 640px; font-size: 24px;
             font-weight: 500; line-height: 1.32; color: #AEBCD6; opacity: 0; }
    .d-cierre { position: absolute; left: 128px; top: 878px; width: 1664px; font-size: 30px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

ESTADOS = [("d-apto", 120, "APTO", "Todos los puntos críticos conformes."),
           ("d-obs", 690, "CON OBSERVACIÓN",
            "La condición no compromete el control inmediato, pero se gestiona dentro del plazo definido."),
           ("d-noapto", 1260, "NO APTO",
            "La falla afecta frenos, ruedas, dirección, estructura, llantas o la visibilidad exigida.")]
CC = "".join(
    '      <div class="d-card %s" id="d-c%d" style="left: %dpx">\n'
    '        <div class="d-t">%s</div>\n'
    '        <div class="d-raya" id="d-r%d" data-layout-ignore></div>\n'
    '        <div class="d-d">%s</div>\n'
    '      </div>\n' % (c, i + 1, x, t, i + 1, d) for i, (c, x, t, d) in enumerate(ESTADOS))

ACCIONES = ["Etiquetar", "Inmovilizar", "Reportar", "Evaluar"]
AA = "".join('      <div class="d-acc" id="d-a%d" style="left: %dpx"><span>%s</span></div>\n'
             % (i + 1, 128 + i * 420, t) for i, t in enumerate(ACCIONES))

CUERPO = chrome("14", "MÓDULO 2", "La inspección termina <b style=\"color:#D4A62B\">en una decisión</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="d-lead" id="d-lead">Después de inspeccionar, clasifico la bicicleta. Son tres estados, no dos.</div>
""" + CC + """
      <div class="d-cap" id="d-cap">NO APTO NO ES ESCRIBIR EL HALLAZGO: SON CUATRO ACCIONES</div>
""" + AA + """
      <div class="d-veto" id="d-veto">No improviso reparaciones en componentes críticos:
        <b>cubrir una fisura con cinta no recupera la resistencia del marco.</b></div>
      <div class="d-org" id="d-org">La organización asegura que una bicicleta no apta no vuelva a circular
        hasta ser reparada, evaluada y liberada conforme al procedimiento.</div>
      <div class="d-cierre" id="d-cierre">Ese respaldo evita que la presión operativa anule la inspección.</div>
    </div>
"""

TL = """      /* 0.00 · «después de inspeccionar, clasifico la bicicleta» */
      tl.fromTo("#d-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

"""
# 3.33 apto · 8.00 con observación · 17.76 no apto
for _i, _t in enumerate([3.40, 8.10, 17.85]):
    TL += ('      tl.fromTo("#d-c%d", { opacity: 0, y: 46, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, %.2f);\n'
           '      tl.fromTo("#d-r%d", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t, _i + 1, _t + 0.28))

TL += """
      /* 28.61 · «no basta con escribir el hallazgo» / 32.07 · las cuatro acciones */
      tl.fromTo("#d-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 28.70);
"""
for _i, _t in enumerate([32.15, 33.25, 34.35, 35.45]):
    TL += ('      tl.fromTo("#d-a%d", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 38.59 · «no improviso reparaciones» / 41.94 · la cinta sobre la fisura */
      tl.fromTo("#d-veto", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 38.70);

      /* 47.57 · lo que le toca a la organización */
      tl.fromTo("#d-org", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 47.70);

      /* 58.08 · «evita que la presión operativa anule la inspección» */
      tl.fromTo("#d-cierre", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 58.20);
"""


def escena():
    return envoltura("e14-decision", DUR, CSS, CUERPO, TL, lamina=LAMINA)
