# -*- coding: utf-8 -*-
"""Identidad y encuadre del curso «Motociclista laboral seguro».

Todo sale del propio PPTX (`diapositiva/2 conductor moto.pptx`): colores más
usados en las 88 láminas y la misma disposición — sección y número arriba,
título en azul, banda inferior con el contador «CLAVES PARA DECIDIR» y la
pausa autónoma sobre una regla dorada.

Dos desviaciones deliberadas del original:

- **Tipografía Montserrat, no Aptos.** Aptos viene con Office y no se puede
  empaquetar en el proyecto; Montserrat es la de toda la serie RiskMann y está
  en `assets/fonts/`.
- **El dorado no se usa para texto pequeño.** `#D79B27` sobre el crema del fondo
  da 2,1:1. En texto va `ORO_TEXTO` (#8C5E08, 4,9:1); el dorado original queda
  para reglas, discos y números grandes.
"""
import re

CREMA = "#F3F0E8"
PAPEL = "#FCFBF7"
TINTA = "#232323"
TINTA_2 = "#4A4A45"
AZUL = "#1F4E79"
OLIVA = "#4F6228"
ORO = "#D79B27"
ORO_TEXTO = "#8C5E08"
TINTE_OLIVA = "#DDE3D2"
TINTE_AZUL = "#DCE7F0"

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

# El encuadre común. Coordenadas sobre 1920×1080; la zona de contenido va de
# y=290 a y=780 y la banda inferior empieza en y=800.
COMUN_CSS = """
    #root { position: relative; width: 1920px; height: 1080px; overflow: hidden;
            font-family: "Montserrat", sans-serif; background: %(crema)s; color: %(tinta)s; }
    .capa { position: absolute; inset: 0; }
    .fondo { background: %(crema)s; }

    .k-seccion { position: absolute; left: 110px; top: 62px; font-size: 22px; font-weight: 800;
                 letter-spacing: 0.14em; color: %(oliva)s; opacity: 0; white-space: nowrap; }
    .k-pagina { position: absolute; right: 110px; top: 58px; font-size: 26px; font-weight: 800;
                color: %(azul)s; opacity: 0; }
    .k-regla { position: absolute; left: 110px; top: 104px; width: 1700px; height: 2px;
               background: %(tinte_oliva)s; transform: scaleX(0); transform-origin: 0 50%%; }
    .k-kicker { position: absolute; left: 110px; top: 138px; font-size: 24px; font-weight: 900;
                letter-spacing: 0.12em; color: %(oro_texto)s; opacity: 0; }
    .k-titulo { position: absolute; left: 110px; top: 150px; width: 1180px; font-size: 62px;
                font-weight: 800; line-height: 1.08; color: %(azul)s; }
    .k-titulo .p { display: inline-block; opacity: 0; will-change: transform, opacity; }
    .k-titulo.con-kicker { top: 180px; }

    /* banda inferior del mazo */
    .k-cuenta { position: absolute; left: 110px; top: 790px; display: flex; align-items: baseline;
                gap: 22px; opacity: 0; }
    .k-cuenta-n { font-size: 58px; font-weight: 900; color: #B48121; line-height: 1; }
    .k-cuenta-t { font-size: 21px; font-weight: 800; letter-spacing: 0.1em; color: %(oliva)s; }
    .k-oro { position: absolute; left: 110px; top: 868px; width: 1700px; height: 3px; background: %(oro)s;
             transform: scaleX(0); transform-origin: 0 50%%; }
    .k-pausa { position: absolute; left: 110px; top: 890px; width: 1480px; font-size: 25px;
               font-weight: 600; line-height: 1.3; color: %(tinta)s; opacity: 0; }
    .k-pausa b { color: %(oliva)s; font-weight: 900; letter-spacing: 0.06em; }
    .k-respuesta { position: absolute; left: 110px; top: 968px; width: 1480px; font-size: 24px;
                   font-weight: 700; line-height: 1.3; color: %(azul)s; opacity: 0; }
    .k-sello { position: absolute; right: 110px; top: 894px; height: 44px; opacity: 0; }

    /* viñetas de la columna izquierda */
    .v-lista { position: absolute; left: 110px; top: 330px; width: 820px; }
    .v-item { position: relative; display: flex; gap: 18px; align-items: flex-start;
              margin-bottom: 20px; opacity: 0; will-change: transform, opacity; }
    .v-dot { flex: none; width: 12px; height: 12px; margin-top: 15px; border-radius: 6px; background: %(oro)s; }
    .v-t { font-size: 32px; font-weight: 600; line-height: 1.24; color: %(tinta)s; }
""" % dict(crema=CREMA, tinta=TINTA, oliva=OLIVA, azul=AZUL, oro=ORO, oro_texto=ORO_TEXTO,
           tinte_oliva=TINTE_OLIVA)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def palabras_titulo(t):
    """El título entra palabra por palabra: cada una en su span."""
    return " ".join('<span class="p">%s</span>' % esc(w) for w in t.split())


def fromto(sel, desde, hasta, t):
    return '      tl.fromTo(%s, %s, %s, %.2f);\n' % (sel, desde, hasta, t)


def envoltura(cid, dur, css, cuerpo, tl):
    """Arma la sub-composición y le añade la salida común: el contenido se apaga
    en los últimos 0,6 s para que el corte ocurra sobre el fondo limpio."""
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
