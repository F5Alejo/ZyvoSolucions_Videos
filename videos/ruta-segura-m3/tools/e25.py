# -*- coding: utf-8 -*-
"""Lámina 25 · Repaso del módulo 3."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 25
DUR = cronometro.duracion(LAMINA)

CSS = """
    .z-preg { position: absolute; left: 128px; width: 1664px; height: 104px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border-left: 6px solid #AC841D;
              opacity: 0; will-change: transform, opacity; }
    .z-n { position: absolute; left: 24px; top: 26px; width: 52px; height: 52px;
           border-radius: 26px; background: rgba(172,132,29,0.28); }
    .z-n span { position: absolute; left: 0; top: 11px; width: 52px; text-align: center;
                font-size: 27px; font-weight: 900; color: #D4A62B; }
    .z-t { position: absolute; left: 100px; right: 24px; top: 21px; font-size: 28px;
           font-weight: 700; line-height: 1.3; color: #FFFFFF; }

    .z-clave { position: absolute; left: 228px; width: 1580px; font-size: 23px; font-weight: 500;
               line-height: 1.34; color: #AEBCD6; opacity: 0; }
    .z-clave b { color: #7FE5EC; font-weight: 700; }

    .z-final { position: absolute; left: 128px; top: 898px; width: 1240px; font-size: 24px;
               font-weight: 700; color: #00C8D4; opacity: 0; }
"""

PREGS = [
    (296, "1", "¿Cuál es la secuencia completa antes de cambiar de trayectoria y por qué vuelves a verificar?"),
    (500, "2", "¿Qué condiciones ponen tu aptitud en rojo y qué decisión tomas antes de pedalear?"),
    (716, "3", "Ante carga insegura, lluvia, una llamada y un camión que gira: ¿qué controles aplicas?"),
]
PP = "".join(
    '      <div class="z-preg" id="z-p%d" style="top: %dpx">\n'
    '        <div class="z-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="z-t">%s</div>\n'
    '      </div>\n' % (i + 1, top, n, t) for i, (top, n, t) in enumerate(PREGS))

CUERPO = chrome("25", "REPASO · MÓDULO 3", "Tres preguntas para <b style=\"color:#D4A62B\">cerrar el módulo</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + PP + """
      <div class="z-clave" id="z-k1" style="top: 410px">Observar · anticipar · señalizar · <b>volver a verificar</b> · ejecutar.<br />
        Se verifica otra vez porque hacer una señal no concede prioridad ni confirma que los demás te hayan visto.</div>
      <div class="z-clave" id="z-k2" style="top: 614px">Somnolencia, mareo, alcohol o sustancias, efecto sedante,
        alteración visual o dolor incapacitante. <b>En rojo: no iniciar o suspender</b>, reportar y aplicar la alternativa definida.</div>
      <div class="z-clave" id="z-k3" style="top: 830px">Detener la marcha · asegurar la carga en un sistema diseñado ·
        revisar clima y ruta · informar el retraso · <b>permanecer fuera del punto ciego</b>.</div>

      <div class="z-final" id="z-final">Organiza tus controles en tres momentos: antes, durante y después de la misión.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 0.00 · «cierro el módulo tres» */
      tl.fromTo("#z-p1", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 0.55);
      /* 4.85 · la secuencia / 12.22 · por qué se vuelve a verificar */
      tl.fromTo("#z-k1", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 4.95);

      /* 19.85 · segunda pregunta / 31.83 · la decisión en rojo */
      tl.fromTo("#z-p2", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 19.95);
      tl.fromTo("#z-k2", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 24.20);

      /* 39.26 · tercera pregunta / 54.36 · el camión */
      tl.fromTo("#z-p3", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 39.36);
      tl.fromTo("#z-k3", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 43.60);

""" + pausa_tl(60.13) + """
      /* 64.27 · «antes, durante y después de la misión» */
      tl.fromTo("#z-final", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 64.37);
"""


def escena():
    return envoltura("e25-repaso", DUR, CSS, CUERPO, TL, lamina=LAMINA)
