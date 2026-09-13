# -*- coding: utf-8 -*-
"""Lámina 31 · Retroalimentación final. Clave 1–9 y criterio para la 10."""
import cronometro
from base import chrome, envoltura

LAMINA = 31
DUR = cronometro.duracion(LAMINA)

CSS = """
    .w-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 27px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .w-grupo { position: absolute; width: 324px; height: 208px; border-radius: 10px;
               background: rgba(0,200,212,0.10); border-top: 5px solid #00C8D4;
               opacity: 0; will-change: transform, opacity; }
    .w-rango { position: absolute; left: 0; top: 22px; width: 324px; text-align: center;
               font-size: 24px; font-weight: 900; letter-spacing: 0.12em; color: #7FE5EC; }
    .w-clave { position: absolute; left: 0; top: 62px; width: 324px; text-align: center;
               font-size: 46px; font-weight: 900; color: #FFFFFF; line-height: 1; }
    .w-que { position: absolute; left: 22px; right: 20px; top: 128px; font-size: 21px;
             font-weight: 500; line-height: 1.3; color: #AEBCD6; text-align: center; }

    .w-abierta { background: rgba(172,132,29,0.14); border-top-color: #AC841D; }
    .w-abierta .w-rango { color: #D4A62B; }
    .w-abierta .w-clave { font-size: 26px; line-height: 1.2; }

    .w-porque { position: absolute; left: 128px; top: 594px; width: 1664px; font-size: 26px;
                font-weight: 600; line-height: 1.32; color: #DCE4F2; opacity: 0; }
    .w-porque b { color: #FFFFFF; font-weight: 800; }

    .w-brecha { position: absolute; left: 128px; top: 704px; width: 1664px; height: 98px;
                border-radius: 10px; background: rgba(172,132,29,0.16); border-left: 6px solid #AC841D;
                opacity: 0; }
    .w-brecha span { position: absolute; left: 28px; right: 24px; top: 22px; font-size: 28px;
                     font-weight: 800; line-height: 1.26; color: #FFFFFF; }

    .w-aviso { position: absolute; left: 128px; top: 834px; width: 1664px; height: 92px;
               border-radius: 10px; background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
               opacity: 0; }
    .w-aviso span { position: absolute; left: 28px; right: 24px; top: 18px; font-size: 25px;
                    font-weight: 600; line-height: 1.3; color: #DCE4F2; }
    .w-aviso b { color: #7FE5EC; font-weight: 800; }
"""

GRUPOS = [("", "1 – 3", "B · B · B", "Visibilidad nocturna, andén y freno inoperante."),
          ("", "4 – 6", "B · B · B", "Secuencia de maniobra, elección de ruta y distracción."),
          ("", "7 – 8", "B · B", "Somnolencia y punto ciego del camión."),
          (" w-abierta", "9", "≥ 4 peligros<br />+ controles", "Con un control aplicable para cada uno."),
          (" w-abierta", "10", "Compromiso<br />verificable", "Abierta, pero verificable y segura.")]
GG = "".join(
    '      <div class="w-grupo%s" id="w-g%d" style="left: %dpx; top: 358px">\n'
    '        <div class="w-rango">%s</div>\n'
    '        <div class="w-clave">%s</div>\n'
    '        <div class="w-que">%s</div>\n'
    '      </div>\n' % (c, i + 1, 128 + i * 344, r, k, q) for i, (c, r, k, q) in enumerate(GRUPOS))

CUERPO = chrome("31", "RETROALIMENTACIÓN FINAL",
                "Clave 1–9 y <b style=\"color:#D4A62B\">criterio para la pregunta 10</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="w-lead" id="w-lead">Ocho preguntas de selección múltiple, una de identificación y una abierta.</div>
""" + GG + """
      <div class="w-porque" id="w-porque">La B se repite porque en las ocho la alternativa correcta es la que
        <b>conserva una barrera</b> en lugar de compensarla con cuidado, velocidad o cambio de ruta.</div>

      <div class="w-brecha" id="w-brecha"><span>Si aparece una brecha crítica: no autorizar la misión hasta
        completar entrenamiento y reevaluación.</span></div>

      <div class="w-aviso" id="w-aviso"><span>La calificación recomendada es un <b>criterio interno de competencia</b>:
        no es un umbral legal expresamente fijado por las normas citadas.</span></div>
    </div>
"""

TL = """      /* 0.00 · «ahora reviso la evaluación» */
      tl.fromTo("#w-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

      /* 2.21 · 1 a 3 / 17.48 · 4 a 6 / 32.20 · 7 y 8 / 40.21 · la nueve / 46.02 · la diez */
      tl.fromTo("#w-g1", { opacity: 0, y: 34, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 2.31);
      tl.fromTo("#w-g2", { opacity: 0, y: 34, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 17.58);
      tl.fromTo("#w-g3", { opacity: 0, y: 34, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 32.30);
      tl.fromTo("#w-g4", { opacity: 0, y: 34, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 40.31);
      tl.fromTo("#w-g5", { opacity: 0, y: 34, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 46.12);

      /* el porqué de que todas sean B entra con la tercera pareja, ya visible el patrón */
      tl.fromTo("#w-porque", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 35.20);

      /* 50.12 · la brecha crítica */
      tl.fromTo("#w-brecha", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 50.22);

      /* 57.15 · «criterio interno, no umbral legal» */
      tl.fromTo("#w-aviso", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 57.25);
"""


def escena():
    return envoltura("e31-clave", DUR, CSS, CUERPO, TL, lamina=LAMINA)
