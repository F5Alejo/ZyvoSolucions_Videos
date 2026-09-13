# -*- coding: utf-8 -*-
"""Las dos láminas de selección múltiple comparten forma: tres preguntas, tres
opciones cada una, en bandas apiladas.

Se escribe una vez y se llena con datos distintos (láminas 26 y 27). Repetir el
CSS en dos archivos garantiza que en la segunda corrección uno de los dos se
quede atrás.
"""
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

CSS = """
    .e-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 27px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .e-banda { position: absolute; left: 128px; width: 1664px; height: 154px; opacity: 0; }
    .e-n { position: absolute; left: 0; top: 4px; width: 48px; height: 48px;
           border-radius: 24px; background: rgba(172,132,29,0.28); }
    .e-n span { position: absolute; left: 0; top: 10px; width: 48px; text-align: center;
                font-size: 25px; font-weight: 900; color: #D4A62B; }
    .e-preg { position: absolute; left: 68px; right: 0; top: 8px; font-size: 30px;
              font-weight: 800; color: #FFFFFF; }
    .e-op { position: absolute; top: 64px; width: 528px; height: 86px; border-radius: 8px;
            background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
            opacity: 0; will-change: transform, opacity; }
    .e-op-l { position: absolute; left: 18px; top: 14px; width: 38px; height: 38px;
              border-radius: 19px; background: rgba(0,200,212,0.18); }
    .e-op-l span { position: absolute; left: 0; top: 7px; width: 38px; text-align: center;
                   font-size: 21px; font-weight: 900; color: #7FE5EC; }
    .e-op-t { position: absolute; left: 70px; right: 18px; top: 14px; font-size: 23px;
              font-weight: 600; line-height: 1.3; color: #DCE4F2; }

    .e-aviso { position: absolute; left: 128px; top: 838px; width: 1240px; font-size: 28px;
               font-weight: 800; color: #D4A62B; opacity: 0; }
    .e-nota { position: absolute; left: 128px; top: 890px; width: 1240px; font-size: 24px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }
"""


def cuerpo(numero, titulo, lead, preguntas, aviso, nota):
    """`preguntas` es [(numero, enunciado, [(letra, texto), ...]), ...]."""
    bandas = ""
    for b, (num, enunciado, ops) in enumerate(preguntas):
        o = "".join(
            '        <div class="e-op" id="e-o%d%d" style="left: %dpx">\n'
            '          <div class="e-op-l" data-layout-ignore><span>%s</span></div>\n'
            '          <div class="e-op-t">%s</div>\n'
            '        </div>\n' % (b + 1, j + 1, j * 570, l, t) for j, (l, t) in enumerate(ops))
        bandas += ('      <div class="e-banda" id="e-b%d" style="top: %dpx">\n'
                   '        <div class="e-n" data-layout-ignore><span>%s</span></div>\n'
                   '        <div class="e-preg">%s</div>\n%s      </div>\n'
                   % (b + 1, 348 + b * 160, num, enunciado, o))

    return chrome(numero, "EVALUACIÓN FINAL", titulo) + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="e-lead" id="e-lead">""" + lead + """</div>
""" + bandas + """      <div class="e-aviso" id="e-aviso">""" + aviso + """</div>
      <div class="e-nota" id="e-nota">""" + nota + """</div>
    </div>

""" + PAUSA_HTML


def tiempos(lead_t, preguntas_t, aviso_t, pausa_t, nota_t):
    """`preguntas_t` es [(t_enunciado, t_opcion_1), ...]; las otras dos opciones
    entran a 1,1 s de distancia, que es lo que tarda la voz en enumerarlas."""
    tl = ('      tl.fromTo("#e-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, %.2f);\n'
          % lead_t)
    for b, (tq, to) in enumerate(preguntas_t):
        tl += ('\n      tl.fromTo("#e-b%d", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, %.2f);\n'
               % (b + 1, tq))
        for j in range(3):
            tl += ('      tl.fromTo("#e-o%d%d", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, %.2f);\n'
                   % (b + 1, j + 1, to + j * 1.1))
    tl += ('\n      tl.fromTo("#e-aviso", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, %.2f);\n'
           % aviso_t)
    tl += pausa_tl(pausa_t)
    tl += ('      tl.fromTo("#e-nota", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, %.2f);\n'
           % nota_t)
    return tl


def escena(cid, lamina, dur, numero, titulo, lead, preguntas, aviso, nota, tl):
    return envoltura(cid, dur, CSS, cuerpo(numero, titulo, lead, preguntas, aviso, nota),
                     tl, lamina=lamina)
