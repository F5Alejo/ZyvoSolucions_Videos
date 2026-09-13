# -*- coding: utf-8 -*-
"""Lámina 33 · Fuentes. Las normas que cita el documento base.

Las dieciséis referencias se reparten en tres columnas y entran por grupos,
siguiendo el orden en que la narración las agrupa. Ninguna se abrevia: es la
lámina que permite rastrear todo lo afirmado en los cuatro videos.
"""
import cronometro
from base import chrome, envoltura

LAMINA = 33
DUR = cronometro.duracion(LAMINA)

CSS = """
    .n-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 26px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .n-grupo { position: absolute; top: 362px; width: 540px; opacity: 0; }
    .n-g-t { font-size: 21px; font-weight: 900; letter-spacing: 0.13em; color: #D4A62B;
             line-height: 1.3; margin-bottom: 16px; }
    .n-g-l { font-size: 22px; font-weight: 600; line-height: 1.26; color: #DCE4F2;
             margin-bottom: 12px; }

    .n-trazable { position: absolute; left: 128px; top: 714px; width: 1664px; font-size: 27px;
                  font-weight: 700; line-height: 1.3; color: #FFFFFF; opacity: 0; }
    .n-trazable b { color: #7FE5EC; font-weight: 800; }

    .n-antes { position: absolute; left: 128px; top: 782px; width: 1664px; height: 104px;
               border-radius: 10px; background: rgba(172,132,29,0.16); border-left: 6px solid #AC841D;
               opacity: 0; }
    .n-antes span { position: absolute; left: 28px; right: 24px; top: 20px; font-size: 25px;
                    font-weight: 600; line-height: 1.3; color: #DCE4F2; }
    .n-antes b { color: #D4A62B; font-weight: 800; }

    .n-fin { position: absolute; left: 128px; top: 904px; width: 1664px; font-size: 30px;
             font-weight: 900; color: #00C8D4; opacity: 0; }
"""

GRUPOS = [
    (128, "TRÁNSITO Y CICLISTAS",
     ["Ley 769 de 2002", "Ley 1811 de 2016", "Ley 1503 de 2011",
      "Decreto Ley 2106 de 2019", "Ley 2050 de 2020", "Ley 2251 de 2022"]),
    (698, "PESV Y TRANSPORTE",
     ["Decreto 1079 de 2015", "Decreto 1252 de 2021",
      "Resoluciones 20223040040595 y 20223040045295 de 2022 (Anexo 63)",
      "Concepto MinTransporte 20251340739071 (12 jun. 2025)"]),
    (1268, "SEGURIDAD Y SALUD EN EL TRABAJO",
     ["Decreto 1072 de 2015", "Resolución 0312 de 2019", "Ley 1562 de 2012",
      "Ley 2466 de 2025", "Decreto 402 de 2025", "OMS · Cyclist safety"]),
]
GG = ""
for _i, (_x, _t, _items) in enumerate(GRUPOS):
    _l = "".join('        <div class="n-g-l">· %s</div>\n' % it for it in _items)
    GG += ('      <div class="n-grupo" id="n-g%d" style="left: %dpx">\n'
           '        <div class="n-g-t">%s</div>\n%s      </div>\n' % (_i + 1, _x, _t, _l))

CUERPO = chrome("33", "FUENTES", "Normas e instrumentos <b style=\"color:#D4A62B\">citados por el documento base</b>",
                "Documento base: programa integral «Ruta Segura», versión septiembre de 2026") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="n-lead" id="n-lead">Tránsito, ciclistas, PESV y Sistema de Gestión de SST.</div>
""" + GG + """
      <div class="n-trazable" id="n-trazable">No es una lista para memorizar: está aquí para
        <b>asegurar trazabilidad y consulta</b>.</div>

      <div class="n-antes" id="n-antes"><span>Antes de adoptar el programa, cada empresa debe verificar el
        <b>texto vigente</b>, revisar las reglas territoriales y ajustarlo a su actividad, sedes, rutas,
        PESV y matriz de peligros.</span></div>

      <div class="n-fin" id="n-fin">Ruta Segura · cada pedaleo cuenta.</div>
    </div>
"""

TL = """      /* 0.00 · «finalizo indicando las fuentes» */
      tl.fromTo("#n-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

      /* 4.31 · la enumeración: un grupo por tercio de la frase larga */
      tl.fromTo("#n-g1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 5.40);
      tl.fromTo("#n-g2", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 13.60);
      tl.fromTo("#n-g3", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 21.80);

      /* 30.13 · «no las leo como una lista para memorizar» */
      tl.fromTo("#n-trazable", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 30.23);

      /* 37.77 · lo que cada empresa debe verificar antes de adoptar */
      tl.fromTo("#n-antes", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 37.87);

      /* 53.61 · «con esto concluyo la capacitación» / 57.11 · «cada pedaleo cuenta» */
      tl.fromTo("#n-fin", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 53.71);
"""


def escena():
    return envoltura("e33-fuentes", DUR, CSS, CUERPO, TL, lamina=LAMINA)
