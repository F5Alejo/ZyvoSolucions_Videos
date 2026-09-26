# -*- coding: utf-8 -*-
"""Constantes compartidas por las once escenas de «Ruta Segura · Módulo 1».

La paleta sale del propio PPTX (colores más usados en las láminas 1-11):
#FFFFFF, #AC841D (oro), #040404 (negro), #00C8D4 (cian), #87733D, #1A2744.
Sobre fondo oscuro el oro #AC841D queda en 5:1 contra el azul noche; para texto
pequeño se usa la versión clara #D4A62B.
"""
import re

import cronometro

W, H = 1920, 1080

NOCHE = "#101B33"      # base del lienzo (derivada de #1A2744, un punto más oscura)
NOCHE_ALTA = "#1E2C4E"  # centro del degradado radial
TINTA = "#FFFFFF"
TINTA_2 = "#AEBCD6"     # texto secundario, 7.2:1 sobre #101B33
ORO = "#AC841D"
ORO_CLARO = "#D4A62B"   # oro para texto pequeño, 7.6:1
CIAN = "#00C8D4"
PIZARRA = "#87733D"

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

# Cabecera y pie comunes: el mismo encuadre en las once láminas para que la
# serie se lea como una sola pieza y el ojo solo siga lo que cambia.
CHROME_CSS = """
    #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden;
             font-family: "Montserrat", sans-serif; background: {noche};
             color: {tinta}; }}
    .capa {{ position: absolute; inset: 0; }}
    .fondo {{ background: radial-gradient(1400px 900px at 50% 34%, {alta} 0%, {noche} 72%); }}
    .marco {{ position: absolute; left: 96px; top: 78px; width: 1728px; height: 924px;
              border: 1.5px solid rgba(174,188,214,0.16); border-radius: 4px; }}
    .ceja {{ position: absolute; left: 128px; top: 112px; font-size: 24px; font-weight: 800;
             letter-spacing: 0.22em; color: {oroc}; }}
    .lamina {{ position: absolute; right: 128px; top: 106px; font-size: 30px; font-weight: 800;
               letter-spacing: 0.1em; color: rgba(174,188,214,0.55); }}
    .titulo {{ position: absolute; left: 128px; top: 150px; width: 1450px; font-size: 50px;
               font-weight: 800; line-height: 1.12; color: {tinta}; }}
    .regla {{ position: absolute; left: 128px; top: 272px; width: 220px; height: 5px;
              background: {oro}; transform-origin: 0 50%; }}
    .fuente {{ position: absolute; left: 128px; top: 946px; font-size: 21px; font-weight: 600;
               letter-spacing: 0.04em; color: rgba(174,188,214,0.80); }}
    /* aviso de pausa: el único elemento que pide al espectador hacer algo */
    .pausa {{ position: absolute; right: 128px; bottom: 108px; height: 58px; padding: 0 30px;
              display: flex; align-items: center; gap: 16px; border-radius: 29px;
              background: rgba(0,200,212,0.12); border: 1.5px solid {cian};
              font-size: 24px; font-weight: 700; letter-spacing: 0.04em; color: {cian}; opacity: 0; }}
    .pausa-icono {{ width: 16px; height: 20px; border-left: 5px solid {cian}; border-right: 5px solid {cian}; }}
""".format(noche=NOCHE, alta=NOCHE_ALTA, tinta=TINTA, oro=ORO, oroc=ORO_CLARO, cian=CIAN)


def chrome(numero, ceja, titulo, fuente="Documento fuente: Ruta Segura, sep. 2026"):
    """Cabecera común de escena. `titulo` admite <br> y <b>.

    `fuente` ya no se muestra: el video es informativo y va sin línea de fuente.
    Se conserva el parámetro para no tocar las láminas que lo pasan.
    """
    return """    <div id="ch" class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">
      <div class="marco" id="ch-marco" data-layout-ignore></div>
      <div class="ceja" id="ch-ceja">{ceja}</div>
      <div class="lamina" id="ch-lamina">{num}</div>
      <div class="titulo" id="ch-titulo">{tit}</div>
      <div class="regla" id="ch-regla" data-layout-ignore></div>
    </div>""".replace("{ceja}", ceja).replace("{num}", numero).replace("{tit}", titulo)


CHROME_TL = """      /* cabecera: entra siempre igual, en los primeros 1.2 s */
      tl.fromTo("#ch-ceja", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 0);
      tl.fromTo("#ch-lamina", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.out" }, 0.1);
      tl.fromTo("#ch-titulo", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.62, ease: "power3.out" }, 0.18);
      tl.fromTo("#ch-regla", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.42);
      tl.fromTo("#ch-marco", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "power1.out" }, 0);
"""


POSICION = re.compile(r",(\s*)(-?\d+(?:\.\d+)?)(\s*)\);")


def recronometrar(tl, lamina):
    """Lleva las marcas de tiempo de la línea de tiempo a la locución vigente.

    Toda sentencia generada aquí termina en `, <posición>);`, así que la
    posición es lo último antes del cierre; las duraciones y los valores de
    animación van dentro de las llaves y no se tocan — el movimiento debe durar
    lo mismo aunque la voz hable más rápido.
    """
    f = cronometro.mapa(lamina)

    def cambia(m):
        return ",%s%s%s);" % (m.group(1), ("%.2f" % f(float(m.group(2)))).rstrip("0").rstrip("."), m.group(3))
    return POSICION.sub(cambia, tl)


def envoltura(cid, dur, css, cuerpo, tl, con_chrome=True, con_cola=True, lamina=None):
    """Arma el archivo de sub-composición completo.

    `con_chrome=False` para las láminas que no usan la cabecera común (portada,
    cierre): sin ella los selectores #ch-* no existen y GSAP avisa del objetivo
    vacío en cada muestra del check.

    `con_cola=True` apaga el contenido en los últimos 0,65 s. Sin eso el corte
    entre láminas salta de una pantalla llena a una vacía que se vuelve a
    construir; con la cola, las dos caras del corte son el fondo limpio.

    `lamina` es el número de lámina del PPTX: con él las marcas de tiempo se
    reconvierten a la locución vigente (ver `tools/cronometro.py`).
    """
    if lamina is not None:
        tl = recronometrar(tl, lamina)
    cola = ""
    if con_cola:
        salida = (
            '      /* salida: el corte a la lámina siguiente ocurre sobre el fondo limpio */',
            '      tl.to(".capa:not(.fondo)", { opacity: 0, duration: 0.55, ease: "power1.in" }, %.2f);' % (dur - 0.65),
            "")
        cola = "\n".join(salida)

    return """<template>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>{fuentes}
{chrome_css}
{css}
  </style>

  <div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
    <div class="clip capa fondo" data-start="0" data-duration="{dur}" data-track-index="0"></div>
{cuerpo}
  </div>

  <script>
    (function () {{
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
{chrome_tl}{tl}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
""".format(fuentes=FUENTES, chrome_css=CHROME_CSS, css=css, cid=cid, dur=dur,
           cuerpo=cuerpo.replace("{d}", str(dur)),
           chrome_tl=CHROME_TL if con_chrome else "", tl=tl + cola)


# La pastilla «PAUSA EL VIDEO Y RESPONDE» ya no va en el video: la actividad
# se hace en la plataforma. Quedan vacías para no tocar las láminas que las usan.
PAUSA_HTML = ""


def pausa_tl(t):
    return ""
