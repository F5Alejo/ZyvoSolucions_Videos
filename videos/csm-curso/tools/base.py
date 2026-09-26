# -*- coding: utf-8 -*-
"""Identidad del curso «Conducción Segura y Manejo Defensivo».

Sale del propio PPTX: azul noche #14193F y #1E2761, amarillo #FFC300, azul
hielo #CADCFC. Cada lámina de módulo tiene la misma anatomía —banda superior
con el código del módulo, dos columnas de viñetas con foto, franja amarilla con
la idea fuerza y dos tarjetas abajo— y la animación la respeta.

Desviación deliberada: Montserrat en vez de Arial / Arial Black (Montserrat es
la de toda la serie RiskMann y viene empaquetada en `assets/fonts/`).
"""
import re

NOCHE = "#14193F"
AZUL = "#1E2761"
AMARILLO = "#FFC300"
HIELO = "#CADCFC"
PAPEL = "#FFFFFF"
FONDO = "#F4F6FB"
TINTA = "#14193F"
TINTA_2 = "#4A5070"

FUENTES = """
    @font-face {
      font-family: "Montserrat"; font-style: normal; font-weight: 100 900; font-display: block;
      src: url("assets/fonts/montserrat-latin-ext.woff2") format("woff2");
      unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
    }
    @font-face {
      font-family: "Montserrat"; font-style: normal; font-weight: 100 900; font-display: block;
      src: url("assets/fonts/montserrat-latin.woff2") format("woff2");
      unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }"""

COMUN_CSS = """
    #root { position: relative; width: 1920px; height: 1080px; overflow: hidden;
            font-family: "Montserrat", sans-serif; background: %(fondo)s; color: %(tinta)s; }
    .capa { position: absolute; inset: 0; }
    .fondo { background: %(fondo)s; }
    .sello { position: absolute; right: 60px; bottom: 36px; width: 170px; height: 56px; border-radius: 28px;
             background: #FFFFFF; opacity: 0; box-shadow: 0 4px 14px rgba(20, 25, 63, 0.12); }
    .sello img { position: absolute; left: 20px; top: 8px; height: 40px; }
""" % dict(fondo=FONDO, tinta=TINTA)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def palabras(t):
    """Cada palabra en su span, para que el título entre palabra por palabra."""
    return " ".join('<span class="p">%s</span>' % esc(w) for w in t.split())


def fromto(sel, desde, hasta, t):
    return '      tl.fromTo(%s, %s, %s, %.2f);\n' % (sel, desde, hasta, t)


def envoltura(cid, dur, css, cuerpo, tl):
    """Sub-composición con la salida común: el contenido se apaga en los
    últimos 0,6 s para que el corte ocurra sobre el fondo limpio."""
    k = [0]

    def con_id(m):
        k[0] += 1
        return '<div id="capa-%d" class="clip capa' % k[0]
    cuerpo = re.sub(r'<div class="clip capa', con_id, cuerpo)
    salida = ('      tl.to(".capa:not(.fondo)", { opacity: 0, duration: 0.5, ease: "power1.in" }, %.2f);\n'
              % (dur - 0.6))
    return """<template>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>%s
%s
%s
  </style>

  <div id="root" data-composition-id="%s" data-start="0" data-duration="%s" data-width="1920" data-height="1080">
    <div id="capa-fondo" class="clip capa fondo" data-start="0" data-duration="%s" data-track-index="0"></div>
%s
  </div>

  <script>
    (function () {
      window.__timelines = window.__timelines || {};
      var tl = gsap.timeline({ paused: true });
%s%s
      window.__timelines["%s"] = tl;
    })();
  </script>
</template>
""" % (FUENTES, COMUN_CSS, css, cid, dur, dur, cuerpo, tl, salida, cid)
