# -*- coding: utf-8 -*-
"""Lámina 30 · Compromiso individual. Una conducta verificable durante 30 días."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 30
DUR = cronometro.duracion(LAMINA)

CSS = """
    .k-frase { position: absolute; left: 128px; top: 306px; width: 1664px; height: 122px;
               border-radius: 10px; background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
               opacity: 0; }
    .k-frase span { position: absolute; left: 30px; top: 32px; font-size: 46px; font-weight: 900;
                    color: #FFFFFF; }
    .k-frase b { color: #7FE5EC; font-weight: 900; }

    .k-cond { position: absolute; top: 458px; height: 62px; padding: 0 26px; display: flex;
              align-items: center; border-radius: 31px; background: rgba(172,132,29,0.16);
              border: 1.5px solid #AC841D; font-size: 25px; font-weight: 800; color: #D4A62B;
              opacity: 0; white-space: nowrap; }

    .k-ejemplo { position: absolute; left: 128px; top: 552px; width: 1010px; padding: 20px 26px;
                 border-radius: 10px; background: rgba(174,188,214,0.10); font-size: 25px;
                 font-weight: 600; font-style: italic; line-height: 1.32; color: #DCE4F2; opacity: 0; }
    .k-define { position: absolute; left: 128px; top: 704px; width: 1010px; font-size: 25px;
                font-weight: 600; line-height: 1.3; color: #AEBCD6; opacity: 0; }
    .k-define b { color: #FFFFFF; font-weight: 800; }

    .k-ncap { position: absolute; left: 1180px; top: 552px; font-size: 23px; font-weight: 900;
              letter-spacing: 0.14em; color: #D4A62B; opacity: 0; }
    .k-nivel { position: absolute; left: 1180px; width: 624px; height: 74px; border-radius: 8px;
               background: rgba(174,188,214,0.09); border-left: 5px solid #AC841D;
               opacity: 0; will-change: transform, opacity; }
    .k-n-n { position: absolute; left: 20px; top: 22px; font-size: 22px; font-weight: 900;
             letter-spacing: 0.08em; color: #D4A62B; }
    .k-n-t { position: absolute; left: 128px; top: 20px; font-size: 26px; font-weight: 800;
             color: #FFFFFF; }

    .k-sin { position: absolute; left: 128px; top: 790px; width: 1010px; font-size: 26px;
             font-weight: 700; line-height: 1.28; color: #FFFFFF; opacity: 0; }
    .k-sin b { color: #D4A62B; font-weight: 800; }
    .k-evita { position: absolute; left: 128px; top: 878px; width: 1240px; font-size: 26px;
               font-weight: 700; line-height: 1.26; color: #00C8D4; opacity: 0; }
"""

CONDICIONES = [("Específico", 128), ("Seguro", 350), ("Verificable", 530), ("Durante 30 días", 770)]
CC = "".join('      <div class="k-cond" id="k-c%d" style="left: %dpx">%s</div>\n'
             % (i + 1, x, t) for i, (t, x) in enumerate(CONDICIONES))

NIVELES = [("NIVEL 1", "Observador del riesgo"), ("NIVEL 2", "Protector preventivo"),
           ("NIVEL 3", "Guardián RiskMann")]
NN = "".join(
    '      <div class="k-nivel" id="k-n%d" style="top: %dpx">\n'
    '        <div class="k-n-n">%s</div><div class="k-n-t">%s</div>\n'
    '      </div>\n' % (i + 1, 596 + i * 84, n, t) for i, (n, t) in enumerate(NIVELES))

CUERPO = chrome("30", "COMPROMISO INDIVIDUAL",
                "Pregunta 10 · <b style=\"color:#D4A62B\">una conducta verificable durante 30 días</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="k-frase" id="k-frase"><span>Desde mañana, antes de cada recorrido <b>yo voy a…</b></span></div>
""" + CC + """
      <div class="k-ejemplo" id="k-ejemplo">«Haré y registraré la inspección antes de cada misión; si encuentro
        una falla crítica, inmovilizaré la bicicleta y la reportaré.»</div>
      <div class="k-define" id="k-define">Define también <b>con qué frecuencia</b> lo harás, <b>qué evidencia</b>
        conservarás y <b>quién</b> puede apoyarte.</div>

      <div class="k-ncap" id="k-ncap">NIVELES DEL RETO RISKMANN</div>
""" + NN + """
      <div class="k-sin" id="k-sin">Los niveles son <b>cualitativos</b>: sin umbrales numéricos inventados,
        y nunca para comparar o humillar.</div>
      <div class="k-evita" id="k-evita">Evita «seré más cuidadoso»: describe una conducta que otra persona pueda observar.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 4.92 · «completo la frase» / 6.52 · la frase */
      tl.fromTo("#k-frase", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 6.62);

      /* 10.28 · específico, seguro, verificable, treinta días */
      tl.fromTo("#k-c1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 10.90);
      tl.fromTo("#k-c2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 11.80);
      tl.fromTo("#k-c3", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 12.70);
      tl.fromTo("#k-c4", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 13.80);

      /* 17.82 · el ejemplo */
      tl.fromTo("#k-ejemplo", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 17.92);

      /* 26.95 · frecuencia, evidencia y apoyo */
      tl.fromTo("#k-define", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 27.05);

      /* 33.49 · los niveles / 37.06 · los tres nombres */
      tl.fromTo("#k-ncap", { opacity: 0, x: 24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 33.59);
      tl.fromTo("#k-n1", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 37.16);
      tl.fromTo("#k-n2", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 38.50);
      tl.fromTo("#k-n3", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 39.84);

      /* 41.77 · «no invento umbrales numéricos» */
      tl.fromTo("#k-sin", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 41.87);

""" + pausa_tl(47.61) + """
      /* 50.53 · «evita seré más cuidadoso» */
      tl.fromTo("#k-evita", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 50.63);
"""


def escena():
    return envoltura("e30-compromiso", DUR, CSS, CUERPO, TL, lamina=LAMINA)
