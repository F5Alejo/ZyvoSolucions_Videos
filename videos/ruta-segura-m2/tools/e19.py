# -*- coding: utf-8 -*-
"""Cierre del módulo 2. Siete segundos sin narración: sirve de respiro y de enlace."""
from base import envoltura

DUR = 7

CSS = """
    .x-fondo { position: absolute; inset: 0;
               background: radial-gradient(1200px 800px at 50% 46%, #1E2C4E 0%, #101B33 74%); }
    .x-ceja { position: absolute; left: 0; top: 392px; width: 1920px; text-align: center;
              font-size: 26px; font-weight: 800; letter-spacing: 0.26em; color: #D4A62B; opacity: 0; }
    .x-tit { position: absolute; left: 0; top: 440px; width: 1920px; text-align: center;
             font-size: 96px; font-weight: 900; line-height: 1; color: #FFFFFF; opacity: 0; }
    .x-raya { position: absolute; left: 860px; top: 566px; width: 200px; height: 5px;
              background: #00C8D4; transform: scaleX(0); transform-origin: 50% 50%; }
    .x-sig { position: absolute; left: 0; top: 606px; width: 1920px; text-align: center;
             font-size: 38px; font-weight: 700; color: #AEBCD6; opacity: 0; }
    .x-sig b { color: #00C8D4; font-weight: 800; }
"""

CUERPO = """    <div class="clip capa x-fondo" data-start="0" data-duration="{d}" data-track-index="1"></div>

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">
      <div class="x-ceja" id="x-ceja">RUTA SEGURA · CADA PEDALEO CUENTA</div>
      <div class="x-tit" id="x-tit">Fin del módulo 2</div>
      <div class="x-raya" id="x-raya" data-layout-ignore></div>
      <div class="x-sig" id="x-sig">Sigue el <b>Módulo 3 · Misión segura</b></div>
    </div>
"""

TL = """      tl.fromTo("#x-ceja", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 0.20);
      tl.fromTo("#x-tit", { opacity: 0, y: 34, scale: 0.94 },
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }, 0.40);
      tl.fromTo("#x-raya", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 0.95);
      tl.fromTo("#x-sig", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 1.30);
      tl.to(["#x-ceja", "#x-tit", "#x-raya", "#x-sig"], { opacity: 0, duration: 0.7, ease: "power1.in" }, 6.10);
"""


def escena():
    return envoltura("e19-cierre", DUR, CSS, CUERPO, TL, con_chrome=False, con_cola=False)
