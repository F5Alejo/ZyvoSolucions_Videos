# -*- coding: utf-8 -*-
"""Lámina 23 · Reto RiskMann. Anticipar antes de exponerse."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 23
DUR = cronometro.duracion(LAMINA)

CSS = """
    .t-escudo { position: absolute; right: 128px; top: 150px; width: 208px; height: 96px;
                border-radius: 10px; background: #AC841D; opacity: 0; }
    .t-escudo-n { position: absolute; left: 0; top: 10px; width: 208px; text-align: center;
                  font-size: 46px; font-weight: 900; color: #101B33; line-height: 1; }
    .t-escudo-t { position: absolute; left: 0; top: 64px; width: 208px; text-align: center;
                  font-size: 17px; font-weight: 800; letter-spacing: 0.1em; color: #101B33; }

    .t-bloque { position: absolute; left: 128px; width: 1664px; opacity: 0; }
    .t-preg { position: absolute; left: 0; top: 0; width: 1664px; font-size: 34px;
              font-weight: 800; color: #FFFFFF; }
    .t-op { position: absolute; top: 56px; width: 540px; height: 124px; border-radius: 8px;
            background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
            opacity: 0; will-change: transform, opacity; }
    .t-op-l { position: absolute; left: 20px; top: 18px; width: 44px; height: 44px;
              border-radius: 22px; background: rgba(0,200,212,0.18); }
    .t-op-l span { position: absolute; left: 0; top: 9px; width: 44px; text-align: center;
                   font-size: 24px; font-weight: 900; color: #7FE5EC; }
    .t-op-t { position: absolute; left: 80px; right: 20px; top: 20px; font-size: 25px;
              font-weight: 600; line-height: 1.32; color: #DCE4F2; }

    .t-aviso { position: absolute; left: 128px; top: 800px; width: 1664px; font-size: 30px;
               font-weight: 800; line-height: 1.26; color: #D4A62B; opacity: 0; }
    .t-barrera { position: absolute; left: 128px; top: 872px; width: 1240px; font-size: 27px;
                 font-weight: 600; color: #AEBCD6; opacity: 0; }
"""

PREGUNTAS = [
    (300, "1 · Antes de cambiar de trayectoria.",
     [("A", "Girar y luego avisar."),
      ("B", "Observar, señalizar, verificar y ejecutar."),
      ("C", "Tocar el timbre y cruzar.")]),
    (558, "2 · Un camión detenido con la direccional derecha.",
     [("A", "Pasar rápido entre el camión y el borde."),
      ("B", "Quedar fuera del punto ciego y de la trayectoria de giro."),
      ("C", "Tocar el timbre y avanzar.")]),
]

BLOQUES = ""
for _b, (_top, _q, _ops) in enumerate(PREGUNTAS):
    _o = "".join(
        '        <div class="t-op" id="t-o%d%d" style="left: %dpx">\n'
        '          <div class="t-op-l" data-layout-ignore><span>%s</span></div>\n'
        '          <div class="t-op-t">%s</div>\n'
        '        </div>\n' % (_b + 1, j + 1, j * 570, l, t) for j, (l, t) in enumerate(_ops))
    BLOQUES += ('      <div class="t-bloque" id="t-b%d" style="top: %dpx">\n'
                '        <div class="t-preg">%s</div>\n%s      </div>\n' % (_b + 1, _top, _q, _o))

CUERPO = chrome("23", "RETO RISKMANN", "Módulo 3 · <b style=\"color:#D4A62B\">anticipar antes de exponerse</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="t-escudo" id="t-escudo">
        <div class="t-escudo-n">+200</div><div class="t-escudo-t">EN JUEGO</div>
      </div>
""" + BLOQUES + """      <div class="t-aviso" id="t-aviso">Hacer una señal o un sonido no garantiza que te hayan visto, ni te concede prioridad.</div>
      <div class="t-barrera" id="t-barrera">Escribe qué indicio necesitas observar antes de ejecutar, y cuál sería tu ruta de escape.</div>
    </div>

""" + PAUSA_HTML

TL = """      tl.fromTo("#t-escudo", { opacity: 0, scale: 0.8, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 0.50);

      /* 3.83 · el cambio de trayectoria / 6.4 · las tres salidas */
      tl.fromTo("#t-b1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 3.90);
      tl.fromTo("#t-o11", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 6.40);
      tl.fromTo("#t-o12", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 9.20);
      tl.fromTo("#t-o13", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 12.00);

      /* 15.13 · el camión con direccional / 19.99 · las tres salidas */
      tl.fromTo("#t-b2", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 15.20);
      tl.fromTo("#t-o21", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 20.10);
      tl.fromTo("#t-o22", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 23.40);
      tl.fromTo("#t-o23", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 26.70);

      /* 42.15 · el indicio y la ruta de escape */
      tl.fromTo("#t-barrera", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 42.25);

      /* 30.68 · «señalizar no garantiza que te hayan visto» */
      tl.fromTo("#t-aviso", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 30.78);

""" + pausa_tl(38.34)


def escena():
    return envoltura("e23-reto", DUR, CSS, CUERPO, TL, lamina=LAMINA)
