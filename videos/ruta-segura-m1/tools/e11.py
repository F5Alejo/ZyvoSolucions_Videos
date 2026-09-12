# -*- coding: utf-8 -*-
"""Lámina 11 · Repaso del módulo 1.

Tiempos corridos −2.3 s: la nota del PPTX empezaba con el rótulo
«GUION DE VOZ — PRIMERA PERSONA», que no se locuta.
"""
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

DUR = 71

CSS = """
    .z-preg { position: absolute; left: 128px; width: 1664px; height: 108px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border-left: 6px solid #AC841D;
              opacity: 0; will-change: transform, opacity; }
    .z-n { position: absolute; left: 24px; top: 28px; width: 52px; height: 52px;
           border-radius: 26px; background: rgba(172,132,29,0.28); }
    .z-n span { position: absolute; left: 0; top: 11px; width: 52px; text-align: center;
                font-size: 27px; font-weight: 900; color: #D4A62B; }
    .z-t { position: absolute; left: 100px; right: 24px; top: 24px; font-size: 30px;
           font-weight: 700; line-height: 1.3; color: #FFFFFF; }

    .z-clave { position: absolute; left: 228px; width: 1560px; font-size: 25px; font-weight: 500;
               line-height: 1.36; color: #AEBCD6; opacity: 0; }
    .z-clave b { color: #7FE5EC; font-weight: 700; }

    .z-final { position: absolute; left: 128px; top: 864px; width: 1660px; font-size: 28px;
               font-weight: 700; line-height: 1.26; color: #00C8D4; opacity: 0; }
"""

PREGS = [
    (296, "1", "Si una persona se equivoca, ¿qué capas del Sistema Seguro deben impedir una lesión grave?"),
    (496, "2", "¿Cuándo puede un ciclista circular por un andén o espacio destinado a peatones?"),
    (692, "3", "La ruta laboral está inundada y sin iluminación: ¿qué tres acciones realizas antes de continuar?"),
]
PP = "".join(
    '      <div class="z-preg" id="z-p%d" style="top: %dpx">\n'
    '        <div class="z-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="z-t">%s</div>\n'
    '      </div>\n' % (i + 1, top, n, t) for i, (top, n, t) in enumerate(PREGS))

CUERPO = chrome("11", "REPASO · MÓDULO 1",
                "Tres preguntas para <b style=\"color:#D4A62B\">cerrar el módulo</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + PP + """
      <div class="z-clave" id="z-k1" style="top: 414px">Bicicleta en condición segura · <b>vía y velocidad</b> que reduzcan la exposición ·
        organización que define tiempos y alternativas · respuesta que evita agravar el evento.</div>
      <div class="z-clave" id="z-k2" style="top: 614px">Solo si existe <b>autorización o un diseño local</b> que permita el uso compartido.
        El casco o el timbre no vuelven permitida esa conducta.</div>
      <div class="z-clave" id="z-k3" style="top: 810px">Me detengo en un lugar seguro · <b>aviso por el canal definido</b> · aplico una ruta, un tiempo o un medio alterno.</div>

      <div class="z-final" id="z-final">Continúa solo cuando puedas explicar también por qué las demás decisiones aumentarían el riesgo.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 5.44 · «la seguridad no depende de una sola persona» — primera pregunta */
      tl.fromTo("#z-p1", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 5.55);
      /* 13.33 · las capas que deben actuar */
      tl.fromTo("#z-k1", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 13.50);

      /* 27.76 · segunda pregunta / 42.13 · su límite */
      tl.fromTo("#z-p2", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 27.90);
      tl.fromTo("#z-k2", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 33.00);

      /* 45.32 · tercera pregunta / 50.26 · las tres acciones */
      tl.fromTo("#z-p3", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 45.45);
      tl.fromTo("#z-k3", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 50.40);

""" + pausa_tl(56.10) + """
      /* 62.00 · la condición para continuar */
      tl.fromTo("#z-final", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 62.00);
"""


def escena():
    return envoltura("e11-repaso", DUR, CSS, CUERPO, TL)
