# -*- coding: utf-8 -*-
"""Cierre de la capacitación completa. Diez segundos sin narración."""
import cronometro
from base import envoltura

DUR = 10

CSS = """
    .z-fondo { position: absolute; inset: 0;
               background: radial-gradient(1200px 800px at 50% 46%, #1E2C4E 0%, #101B33 74%); }
    .z-ceja { position: absolute; left: 0; top: 372px; width: 1920px; text-align: center;
              font-size: 26px; font-weight: 800; letter-spacing: 0.26em; color: #D4A62B; opacity: 0; }
    .z-tit { position: absolute; left: 0; top: 420px; width: 1920px; text-align: center;
             font-size: 104px; font-weight: 900; line-height: 1; color: #FFFFFF; opacity: 0; }
    .z-raya { position: absolute; left: 850px; top: 556px; width: 220px; height: 5px;
              background: #00C8D4; transform: scaleX(0); transform-origin: 50% 50%; }
    .z-sub { position: absolute; left: 0; top: 596px; width: 1920px; text-align: center;
             font-size: 40px; font-weight: 700; color: #AEBCD6; opacity: 0; }
    .z-sub b { color: #00C8D4; font-weight: 800; }
    .z-nota { position: absolute; left: 0; top: 680px; width: 1920px; text-align: center;
              font-size: 25px; font-weight: 600; color: #AEBCD6; opacity: 0; }
"""

CUERPO = """    <div class="clip capa z-fondo" data-start="0" data-duration="{d}" data-track-index="1"></div>

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">
      <div class="z-ceja" id="z-ceja">RUTA SEGURA</div>
      <div class="z-tit" id="z-tit">Cada pedaleo cuenta</div>
      <div class="z-raya" id="z-raya" data-layout-ignore></div>
      <div class="z-sub" id="z-sub">Fin de la capacitación · <b>cuatro módulos</b></div>
      <div class="z-nota" id="z-nota">Capacitar no reemplaza la gestión material del riesgo.</div>
    </div>
"""

TL = """      tl.fromTo("#z-ceja", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 0.20);
      tl.fromTo("#z-tit", { opacity: 0, y: 36, scale: 0.94 },
        { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: "power3.out" }, 0.40);
      tl.fromTo("#z-raya", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 1.05);
      tl.fromTo("#z-sub", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 1.40);
      tl.fromTo("#z-nota", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 2.30);
      tl.to(["#z-ceja", "#z-tit", "#z-raya", "#z-sub", "#z-nota"],
        { opacity: 0, duration: 0.8, ease: "power1.in" }, 8.90);
"""


def escena():
    return envoltura("e34-fin", DUR, CSS, CUERPO, TL, con_chrome=False, con_cola=False)
