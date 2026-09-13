# -*- coding: utf-8 -*-
"""Lámina 18 · Repaso del módulo 2."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 18
DUR = cronometro.duracion(LAMINA)

CSS = """
    .z-preg { position: absolute; left: 128px; width: 1664px; height: 106px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border-left: 6px solid #AC841D;
              opacity: 0; will-change: transform, opacity; }
    .z-n { position: absolute; left: 24px; top: 27px; width: 52px; height: 52px;
           border-radius: 26px; background: rgba(172,132,29,0.28); }
    .z-n span { position: absolute; left: 0; top: 11px; width: 52px; text-align: center;
                font-size: 27px; font-weight: 900; color: #D4A62B; }
    .z-t { position: absolute; left: 100px; right: 24px; top: 22px; font-size: 29px;
           font-weight: 700; line-height: 1.3; color: #FFFFFF; }

    .z-clave { position: absolute; left: 228px; width: 1580px; font-size: 23px; font-weight: 500;
               line-height: 1.34; color: #AEBCD6; opacity: 0; }
    .z-clave b { color: #7FE5EC; font-weight: 700; }

    .z-final { position: absolute; left: 128px; top: 900px; width: 1240px; font-size: 24px;
               font-weight: 700; line-height: 1.26; color: #00C8D4; opacity: 0; }
"""

PREGS = [
    (296, "1", "Menciona cinco puntos de inspección y una falla crítica que obligue a declarar «no apta»."),
    (524, "2", "¿Qué cuatro acciones siguen cuando una bicicleta queda clasificada como «no apta»?"),
    (716, "3", "¿Cómo ajustas el casco y confirmas que luces y reflectivos sean visibles a 360°?"),
]
PP = "".join(
    '      <div class="z-preg" id="z-p%d" style="top: %dpx">\n'
    '        <div class="z-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="z-t">%s</div>\n'
    '      </div>\n' % (i + 1, top, n, t) for i, (top, n, t) in enumerate(PREGS))

CUERPO = chrome("18", "REPASO · MÓDULO 2", "Tres preguntas para <b style=\"color:#D4A62B\">cerrar el módulo</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
""" + PP + """
      <div class="z-clave" id="z-k1" style="top: 412px">Marco y horquilla · dirección · ruedas y llantas · frenos ·
        transmisión · pedales y sillín · luces y reflectivos · carga.<br />
        <b>Falla crítica:</b> freno inoperante, rueda o dirección floja, fisura estructural, llanta insegura
        o falta de luz obligatoria de noche.</div>
      <div class="z-clave" id="z-k2" style="top: 640px">Etiquetar · <b>inmovilizar</b> · reportar · solicitar evaluación
        o mantenimiento competente. No se improvisa una reparación crítica.</div>
      <div class="z-clave" id="z-k3" style="top: 832px">Casco horizontal, talla correcta, correas en <b>«V»</b> y
        barboquejo abrochado. Después: visibilidad de frente, atrás y lados, y que la carga no cubra luces ni reflectivos.</div>

      <div class="z-final" id="z-final">Responde usando tu bicicleta y tu equipo como referencia.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 0.00 · «compruebo que la inspección se convierta en una decisión» */
      tl.fromTo("#z-p1", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 0.60);
      /* 4.77 · los ocho puntos / 19.10 · la falla crítica */
      tl.fromTo("#z-k1", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 4.85);

      /* 33.73 · segunda pregunta / 37.19 · las cuatro acciones */
      tl.fromTo("#z-p2", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 33.80);
      tl.fromTo("#z-k2", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 37.30);

      /* 46.21 · tercera pregunta / 56.92 · la visibilidad */
      tl.fromTo("#z-p3", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 46.30);
      tl.fromTo("#z-k3", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 50.40);

""" + pausa_tl(66.25) + """
      tl.fromTo("#z-final", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 66.30);
"""


def escena():
    return envoltura("e18-repaso", DUR, CSS, CUERPO, TL, lamina=LAMINA)
