# -*- coding: utf-8 -*-
"""Lámina 28 · Evaluación final 3/4. Dos casos de decisión."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 28
DUR = cronometro.duracion(LAMINA)

CSS = """
    .c-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 27px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    .c-bloque { position: absolute; left: 128px; width: 1664px; opacity: 0; }
    .c-preg { position: absolute; left: 0; top: 0; width: 1664px; font-size: 32px;
              font-weight: 800; color: #FFFFFF; }
    .c-op { position: absolute; top: 52px; width: 528px; height: 112px; border-radius: 8px;
            background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
            opacity: 0; will-change: transform, opacity; }
    .c-op-l { position: absolute; left: 18px; top: 16px; width: 40px; height: 40px;
              border-radius: 20px; background: rgba(0,200,212,0.18); }
    .c-op-l span { position: absolute; left: 0; top: 8px; width: 40px; text-align: center;
                   font-size: 22px; font-weight: 900; color: #7FE5EC; }
    .c-op-t { position: absolute; left: 72px; right: 18px; top: 18px; font-size: 24px;
              font-weight: 600; line-height: 1.3; color: #DCE4F2; }

    .c-principio { position: absolute; left: 128px; top: 690px; width: 1664px; height: 132px;
                   border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
                   opacity: 0; }
    .c-p-l { position: absolute; left: 28px; right: 26px; font-size: 26px; font-weight: 600;
             line-height: 1.3; color: #DCE4F2; opacity: 0; }
    .c-p-l b { color: #FFFFFF; font-weight: 800; }

    .c-aviso { position: absolute; left: 128px; top: 850px; width: 1240px; font-size: 27px;
               font-weight: 800; line-height: 1.24; color: #D4A62B; opacity: 0; }
"""

CASOS = [
    (352, "7 · Medicamento con advertencia de somnolencia; te sientes lento.",
     [("A", "Salir y evaluar en ruta."),
      ("B", "No iniciar, reportar y aplicar la alternativa."),
      ("C", "Tomar café y continuar.")]),
    (524, "8 · Camión detenido con la direccional derecha.",
     [("A", "Pasar entre el camión y el borde."),
      ("B", "Permanecer fuera del punto ciego y del giro."),
      ("C", "Tocar el timbre y pasar.")]),
]

BLOQUES = ""
for _b, (_top, _q, _ops) in enumerate(CASOS):
    _o = "".join(
        '        <div class="c-op" id="c-o%d%d" style="left: %dpx">\n'
        '          <div class="c-op-l" data-layout-ignore><span>%s</span></div>\n'
        '          <div class="c-op-t">%s</div>\n'
        '        </div>\n' % (_b + 1, j + 1, j * 570, l, t) for j, (l, t) in enumerate(_ops))
    BLOQUES += ('      <div class="c-bloque" id="c-b%d" style="top: %dpx">\n'
                '        <div class="c-preg">%s</div>\n%s      </div>\n' % (_b + 1, _top, _q, _o))

CUERPO = chrome("28", "EVALUACIÓN FINAL",
                "3/4 · <b style=\"color:#D4A62B\">Casos de toma de decisiones</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="c-lead" id="c-lead">En los dos, una opción parece inconveniente para la operación
        pero protege una barrera crítica.</div>
""" + BLOQUES + """
      <div class="c-principio" id="c-principio">
        <div class="c-p-l" id="c-p1" style="top: 22px">La urgencia de una entrega <b>no elimina el efecto sedante</b>
          de un medicamento.</div>
        <div class="c-p-l" id="c-p2" style="top: 74px">Tampoco <b>modifica la geometría del giro</b> de un vehículo pesado.</div>
      </div>

      <div class="c-aviso" id="c-aviso">Explica por qué una compensación improvisada no convierte una decisión
        insegura en aceptable.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 0.00 · «en la tercera parte analizo dos casos» */
      tl.fromTo("#c-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

      /* 2.95 · el medicamento / 9.37 · las tres salidas */
      tl.fromTo("#c-b1", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 3.05);
      tl.fromTo("#c-o11", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 9.47);
      tl.fromTo("#c-o12", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 12.30);
      tl.fromTo("#c-o13", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 15.10);

      /* 18.09 · el camión */
      tl.fromTo("#c-b2", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 18.19);
      tl.fromTo("#c-o21", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 20.40);
      tl.fromTo("#c-o22", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 21.90);
      tl.fromTo("#c-o23", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 23.40);

      /* 32.54 · lo que la urgencia no cambia */
      tl.fromTo("#c-principio", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 32.64);
      tl.fromTo("#c-p1", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.out" }, 33.10);
      tl.fromTo("#c-p2", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.out" }, 36.40);

      /* 40.52 · «explica por qué una compensación improvisada no basta» */
      tl.fromTo("#c-aviso", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 44.20);

""" + pausa_tl(40.62)


def escena():
    return envoltura("e28-evaluacion-3", DUR, CSS, CUERPO, TL, lamina=LAMINA)
