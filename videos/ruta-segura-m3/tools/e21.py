# -*- coding: utf-8 -*-
"""Lámina 21 · La ruta y tu estado también se inspeccionan.

El semáforo de aptitud es el único sitio de la serie donde entran verde, ámbar y
rojo: no son colores de marca inventados, son el significado que el documento
fuente le da a cada estado. Van solo en el punto; la tipografía sigue en la
paleta del curso.
"""
import cronometro
from base import chrome, envoltura

LAMINA = 21
DUR = cronometro.duracion(LAMINA)

CSS = """
    .r-lead { position: absolute; left: 128px; top: 300px; width: 1664px; font-size: 28px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }

    /* --- columna izquierda: la matriz de ruta --- */
    .r-cap { position: absolute; left: 128px; top: 358px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .r-chip { position: absolute; height: 58px; padding: 0 22px; display: flex; align-items: center;
              border-radius: 8px; background: rgba(174,188,214,0.10); border-left: 5px solid #AC841D;
              font-size: 24px; font-weight: 700; color: #FFFFFF; opacity: 0; white-space: nowrap; }
    .r-corta { position: absolute; left: 128px; top: 678px; width: 840px; font-size: 30px;
               font-weight: 800; line-height: 1.26; color: #00C8D4; opacity: 0; }

    /* --- columna derecha: el semáforo de aptitud --- */
    .r-scap { position: absolute; left: 1060px; top: 358px; font-size: 24px; font-weight: 900;
              letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .r-estado { position: absolute; left: 1060px; width: 736px; height: 104px; border-radius: 10px;
                background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
                opacity: 0; will-change: transform, opacity; }
    .r-luz { position: absolute; left: 24px; top: 30px; width: 36px; height: 36px; border-radius: 18px; }
    .r-e-t { position: absolute; left: 78px; top: 16px; font-size: 26px; font-weight: 900;
             letter-spacing: 0.06em; color: #FFFFFF; }
    .r-e-d { position: absolute; left: 78px; right: 20px; top: 50px; font-size: 22px;
             font-weight: 500; line-height: 1.26; color: #AEBCD6; }

    .r-nota { position: absolute; left: 128px; top: 794px; width: 1664px; font-size: 26px;
              font-weight: 600; line-height: 1.3; color: #DCE4F2; opacity: 0; }
    .r-nota b { color: #7FE5EC; font-weight: 800; }
    .r-cierre { position: absolute; left: 128px; top: 872px; width: 1664px; font-size: 30px;
                font-weight: 800; color: #D4A62B; opacity: 0; }
"""

MATRIZ = [("Cruces", 128, 402), ("Tráfico pesado", 350, 402), ("Iluminación", 610, 402),
          ("Clima", 128, 470), ("Obras", 310, 470), ("Seguridad pública", 470, 470),
          ("Alternativa definida", 128, 538), ("Criterio de suspensión", 400, 538)]
MM = "".join('      <div class="r-chip" id="r-c%d" style="left: %dpx; top: %dpx">%s</div>\n'
             % (i + 1, x, y, t) for i, (t, x, y) in enumerate(MATRIZ))

# verde, ámbar y rojo de semáforo: es lo que el documento fuente significa
ESTADOS = [("#2FBF71", "VERDE", "Alerta, equipado y con condiciones controladas."),
           ("#E3A81B", "AMARILLO", "Detenerme, aplicar controles y volver a decidir."),
           ("#DE4D4D", "ROJO", "Somnolencia, mareo, alcohol o sustancias, efecto sedante, alteración visual o dolor incapacitante.")]
EE = "".join(
    '      <div class="r-estado" id="r-e%d" style="top: %dpx">\n'
    '        <div class="r-luz" style="background: %s" data-layout-ignore></div>\n'
    '        <div class="r-e-t">%s</div>\n'
    '        <div class="r-e-d">%s</div>\n'
    '      </div>\n' % (i + 1, 402 + i * 116, c, t, d) for i, (c, t, d) in enumerate(ESTADOS))

CUERPO = chrome("21", "MÓDULO 3", "La ruta y tu estado <b style=\"color:#D4A62B\">también se inspeccionan</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="r-lead" id="r-lead">No solo inspecciono la bicicleta: también la ruta y mi estado personal.</div>

      <div class="r-cap" id="r-cap">MATRIZ DE RUTA</div>
""" + MM + """      <div class="r-corta" id="r-corta">La ruta más segura no siempre es la más corta.</div>

      <div class="r-scap" id="r-scap">SEMÁFORO DE APTITUD</div>
""" + EE + """
      <div class="r-nota" id="r-nota">Mapa o teléfono: <b>solo antes de iniciar, o detenido en un lugar seguro</b>.</div>
      <div class="r-cierre" id="r-cierre">Ninguna urgencia operativa convierte una condición roja en aceptable.</div>
    </div>
"""

TL = """      /* 0.00 · «también inspecciono la ruta y mi estado» */
      tl.fromTo("#r-lead", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);

      /* 6.01 · la matriz de ruta, punto por punto */
      tl.fromTo("#r-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 6.10);
"""
for _i, _t in enumerate([7.00, 8.10, 9.20, 10.30, 11.40, 12.50, 13.80, 15.10]):
    TL += ('      tl.fromTo("#r-c%d", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 17.31 · «la ruta más segura no siempre es la más corta» */
      tl.fromTo("#r-corta", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 17.40);

      /* 20.80 · el semáforo de aptitud / 23.75 · 29.08 · 34.41 · los tres estados */
      tl.fromTo("#r-scap", { opacity: 0, x: 24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 20.90);
      tl.fromTo("#r-e1", { opacity: 0, x: 44 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 23.85);
      tl.fromTo("#r-e2", { opacity: 0, x: 44 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 29.18);
      tl.fromTo("#r-e3", { opacity: 0, x: 44 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 34.51);

      /* 44.79 · el mapa y el teléfono */
      tl.fromTo("#r-nota", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 44.90);

      /* 52.90 · «ninguna urgencia convierte una condición roja en aceptable» */
      tl.fromTo("#r-cierre", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 53.00);
"""


def escena():
    return envoltura("e21-ruta-estado", DUR, CSS, CUERPO, TL, lamina=LAMINA)
