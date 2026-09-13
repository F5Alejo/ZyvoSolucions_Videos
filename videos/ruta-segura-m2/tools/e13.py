# -*- coding: utf-8 -*-
"""Lámina 13 · Los ocho puntos de la inspección, en el orden en que se narran."""
import cronometro
from base import chrome, envoltura

LAMINA = 13
DUR = cronometro.duracion(LAMINA)

CSS = """
    .o-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 29px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .o-punto { position: absolute; width: 396px; height: 176px; border-radius: 10px;
               background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
               opacity: 0; will-change: transform, opacity; }
    .o-n { position: absolute; left: -1px; top: -1px; width: 58px; height: 46px;
           border-radius: 10px 0 10px 0; background: #AC841D; }
    .o-n span { position: absolute; left: 0; top: 8px; width: 58px; text-align: center;
                font-size: 24px; font-weight: 900; color: #101B33; }
    .o-t { position: absolute; left: 74px; right: 20px; top: 12px; font-size: 26px;
           font-weight: 900; letter-spacing: 0.02em; line-height: 1.1; color: #D4A62B; }
    .o-d { position: absolute; left: 22px; right: 20px; top: 74px; font-size: 23px;
           font-weight: 500; line-height: 1.34; color: #DCE4F2; }

    /* la prueba con que se cierra la secuencia */
    .o-prueba { position: absolute; left: 120px; top: 776px; width: 1010px; height: 78px;
                border-radius: 10px; background: rgba(0,200,212,0.12); border-left: 6px solid #00C8D4;
                opacity: 0; }
    .o-prueba span { position: absolute; left: 26px; top: 22px; font-size: 28px; font-weight: 800;
                     color: #FFFFFF; white-space: nowrap; }
    .o-prueba b { color: #7FE5EC; font-weight: 800; }
    .o-registro { position: absolute; left: 1158px; top: 776px; width: 642px; height: 78px;
                  border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
                  opacity: 0; }
    .o-registro span { position: absolute; left: 24px; right: 20px; top: 14px; font-size: 23px;
                       font-weight: 600; line-height: 1.3; color: #DCE4F2; }
    .o-cierre { position: absolute; left: 120px; top: 874px; width: 1680px; font-size: 30px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

PUNTOS = [("1", "MARCO + HORQUILLA", "Fisuras, deformaciones, corrosión o piezas sueltas."),
          ("2", "DIRECCIÓN + MANUBRIO", "Alineación, juego y fijación."),
          ("3", "RUEDAS + LLANTAS", "Presión, cortes, desgaste, radios y sujeción."),
          ("4", "FRENOS", "Ambos, comprobados."),
          ("5", "TRANSMISIÓN", "Cadena, platos, piñones y cambios."),
          ("6", "PEDALES + SILLÍN", "Pedales, bielas y sillín."),
          ("7", "LUCES + REFLECTIVOS", "Y el dispositivo sonoro."),
          ("8", "CARGA + ACCESORIOS", "Que nada interfiera con dirección, frenado o visibilidad.")]
PP = "".join(
    '      <div class="o-punto" id="o-p%d" style="left: %dpx; top: %dpx">\n'
    '        <div class="o-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="o-t">%s</div>\n'
    '        <div class="o-d">%s</div>\n'
    '      </div>\n' % (i + 1, 120 + (i % 4) * 428, 366 + (i // 4) * 196, n, t, d)
    for i, (n, t, d) in enumerate(PUNTOS))

CUERPO = chrome("13", "MÓDULO 2", "Ocho puntos <b style=\"color:#D4A62B\">antes de cada uso</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="o-lead" id="o-lead">Sigo siempre el mismo orden: es lo que evita las omisiones.</div>
""" + PP + """
      <div class="o-prueba" id="o-prueba"><span>Prueba <b>estática</b> de frenos y, en zona segura, prueba <b>dinámica</b>.</span></div>
      <div class="o-registro" id="o-registro"><span>La inspección debe dejar un resultado, la novedad encontrada
        y la acción tomada.</span></div>
      <div class="o-cierre" id="o-cierre">Sin registro, la inspección no ocurrió.</div>
    </div>
"""

TL = """      /* 0.00 · «sigo un orden para evitar omisiones» */
      tl.fromTo("#o-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.60);

"""
# un punto por frase: 3.94 · 11.50 · 17.76 · 26.93 · 29.92 · 35.26 · 39.52 · 44.48
for _i, _t in enumerate([4.00, 11.60, 17.85, 27.00, 30.00, 35.35, 39.60, 44.55]):
    TL += ('      tl.fromTo("#o-p%d", { opacity: 0, y: 34, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, %.2f);\n' % (_i + 1, _t))

TL += """
      /* 52.37 · la prueba estática y la dinámica */
      tl.fromTo("#o-prueba", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 52.45);

      /* 58.96 · «debe dejar un resultado, la novedad y la acción» */
      tl.fromTo("#o-registro", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 59.05);
      tl.fromTo("#o-cierre", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 61.60);
"""


def escena():
    return envoltura("e13-ocho-puntos", DUR, CSS, CUERPO, TL, lamina=LAMINA)
