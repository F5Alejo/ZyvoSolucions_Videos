# -*- coding: utf-8 -*-
"""Lámina 20 · Una maniobra segura se construye en cinco pasos."""
import cronometro
from base import chrome, envoltura

LAMINA = 20
DUR = cronometro.duracion(LAMINA)

CSS = """
    .m-paso { position: absolute; top: 336px; width: 320px; height: 236px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
              opacity: 0; will-change: transform, opacity; }
    .m-n { position: absolute; left: -1px; top: -1px; width: 54px; height: 44px;
           border-radius: 10px 0 10px 0; background: #AC841D; }
    .m-n span { position: absolute; left: 0; top: 8px; width: 54px; text-align: center;
                font-size: 23px; font-weight: 900; color: #101B33; }
    .m-t { position: absolute; left: 70px; right: 18px; top: 10px; font-size: 27px;
           font-weight: 900; letter-spacing: 0.03em; color: #D4A62B; }
    .m-d { position: absolute; left: 22px; right: 18px; top: 70px; font-size: 23px;
           font-weight: 500; line-height: 1.34; color: #DCE4F2; }
    /* la flecha entre pasos: la secuencia es una cadena, no una lista */
    .m-flecha { position: absolute; top: 448px; width: 22px; height: 3px; background: #AC841D;
                transform: scaleX(0); transform-origin: 0 50%; }

    .m-nota { position: absolute; left: 116px; top: 610px; width: 1688px; font-size: 26px;
              font-weight: 600; line-height: 1.3; color: #AEBCD6; opacity: 0; }

    .m-clima { position: absolute; left: 116px; top: 686px; width: 1688px; height: 92px;
               border-radius: 10px; background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
               opacity: 0; }
    .m-clima span { position: absolute; left: 26px; right: 22px; top: 18px; font-size: 26px;
                    font-weight: 600; line-height: 1.3; color: #DCE4F2; }
    .m-clima b { color: #7FE5EC; font-weight: 800; }

    .m-prisa { position: absolute; left: 116px; top: 802px; width: 1688px; font-size: 30px;
               font-weight: 800; color: #D4A62B; opacity: 0; }
    .m-habito { position: absolute; left: 116px; top: 864px; width: 1688px; font-size: 30px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

PASOS = [("1", "OBSERVAR", "Frente, laterales, superficie y accesos."),
         ("2", "ANTICIPAR", "Puertas, giros, cruces y cambios de velocidad."),
         ("3", "SEÑALIZAR", "Sin perder el control del manubrio."),
         ("4", "VERIFICAR", "Mi señal no obliga a los demás a cederme el paso."),
         ("5", "EJECUTAR", "Trayectoria estable, sin movimientos bruscos.")]
PP = "".join(
    '      <div class="m-paso" id="m-p%d" style="left: %dpx">\n'
    '        <div class="m-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="m-t">%s</div>\n'
    '        <div class="m-d">%s</div>\n'
    '      </div>\n' % (i + 1, 116 + i * 342, n, t, d) for i, (n, t, d) in enumerate(PASOS))
FL = "".join('      <div class="m-flecha" id="m-fl%d" style="left: %dpx" data-layout-ignore></div>\n'
             % (i + 1, 436 + i * 342) for i in range(4))

CUERPO = chrome("20", "MÓDULO 3", "Una maniobra segura <b style=\"color:#D4A62B\">se construye en cinco pasos</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + PP + FL + """
      <div class="m-nota" id="m-nota">Junto a vehículos estacionados mantengo una separación prudente:
        una puerta puede abrirse sin aviso.</div>

      <div class="m-clima" id="m-clima"><span>En lluvia, pintura húmeda, arena o material suelto:
        <b>más distancia, frenado progresivo y ninguna maniobra brusca</b>.</span></div>

      <div class="m-prisa" id="m-prisa">La prisa suele eliminar el paso de verificación.</div>
      <div class="m-habito" id="m-habito">Observar · anticipar · señalizar · verificar · ejecutar.</div>
    </div>
"""

TL = ""
# un paso por frase: 3.43 · 8.55 · 13.20 · 17.10 · 23.11
for _i, _t in enumerate([3.50, 8.62, 13.28, 17.18, 23.20]):
    TL += ('      tl.fromTo("#m-p%d", { opacity: 0, y: 40, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, %.2f);\n' % (_i + 1, _t))
for _i, _t in enumerate([8.30, 12.95, 16.90, 22.90]):
    TL += ('      tl.fromTo("#m-fl%d", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 28.10 · la puerta que se abre */
      tl.fromTo("#m-nota", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 28.20);

      /* 35.33 · lluvia, pintura húmeda, arena o material suelto */
      tl.fromTo("#m-clima", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 35.45);

      /* 46.02 · «la prisa elimina el paso de verificación» */
      tl.fromTo("#m-prisa", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 46.12);

      /* 53.14 · la secuencia repetida como hábito, con un pulso sobre los cinco pasos */
      tl.fromTo("#m-habito", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 53.24);
      tl.to(".m-paso", { y: -12, duration: 0.2, ease: "power2.out", stagger: 0.09 }, 53.40);
      tl.to(".m-paso", { y: 0, duration: 0.32, ease: "power2.inOut", stagger: 0.09 }, 53.62);
"""


def escena():
    return envoltura("e20-cinco-pasos", DUR, CSS, CUERPO, TL, lamina=LAMINA)
