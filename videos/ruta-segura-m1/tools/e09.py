# -*- coding: utf-8 -*-
"""Lámina 09 · Reto RiskMann. Dos decisiones, sin pistas."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 9
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
    .t-op { position: absolute; top: 56px; width: 540px; height: 132px; border-radius: 8px;
            background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
            opacity: 0; will-change: transform, opacity; }
    .t-op-l { position: absolute; left: 20px; top: 18px; width: 44px; height: 44px;
              border-radius: 22px; background: rgba(0,200,212,0.18); }
    .t-op-l span { position: absolute; left: 0; top: 9px; width: 44px; text-align: center;
                   font-size: 24px; font-weight: 900; color: #7FE5EC; }
    .t-op-t { position: absolute; left: 80px; right: 20px; top: 20px; font-size: 25px;
              font-weight: 600; line-height: 1.34; color: #DCE4F2; }

    .t-aviso { position: absolute; left: 128px; top: 872px; width: 1664px; font-size: 30px;
               font-weight: 700; color: #D4A62B; opacity: 0; }
"""

PREGUNTAS = [
    (300, "1 · ¿Qué representa el Sistema Seguro?",
     [("A", "Todo depende del cuidado individual."),
      ("B", "El sistema limita el daño cuando alguien se equivoca."),
      ("C", "El ciclista siempre tiene prioridad.")]),
    (566, "2 · El descanso por uso de bicicleta en el sector privado…",
     [("A", "Se causa automáticamente cada seis meses."),
      ("B", "Puede acordarse y exige certificación."),
      ("C", "Sustituye las vacaciones.")]),
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

CUERPO = chrome("09", "RETO RISKMANN",
                "Módulo 1 · <b style=\"color:#D4A62B\">dos decisiones, sin pistas</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="t-escudo" id="t-escudo">
        <div class="t-escudo-n">+200</div><div class="t-escudo-t">EN JUEGO</div>
      </div>
""" + BLOQUES + """      <div class="t-aviso" id="t-aviso">No elijas por intuición: identifica la condición que hace correcta una opción y descarta las demás.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 1.47 · «Llegamos al primer reto» */
      tl.fromTo("#t-escudo", { opacity: 0, scale: 0.8, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 1.60);

      /* 8.29 · primera pregunta / 14.79 · sus tres opciones */
      tl.fromTo("#t-b1", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 8.45);
      tl.fromTo("#t-o11", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 15.00);
      tl.fromTo("#t-o12", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 17.60);
      tl.fromTo("#t-o13", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 20.20);

      /* 23.35 · segunda pregunta / 29.70 · sus tres opciones */
      tl.fromTo("#t-b2", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 23.50);
      tl.fromTo("#t-o21", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 29.90);
      tl.fromTo("#t-o22", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 32.30);
      tl.fromTo("#t-o23", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 34.70);

      /* 37.12 · «No elijas por intuición» */
      tl.fromTo("#t-aviso", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 37.30);

""" + pausa_tl(47.60)


def escena():
    return envoltura("e09-reto", DUR, CSS, CUERPO, TL, lamina=LAMINA)
