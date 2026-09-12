# -*- coding: utf-8 -*-
"""Genera las sub-composiciones y el index.html de «Ruta Segura · Módulo 1».

Las duraciones salen de tools/tiempos-medidos.json: cada lámina dura lo que dura
su narración leída a ritmo de capacitación, más un respiro de cola. El video se
entrega SIN voz; el locutor colombiano graba encima siguiendo tools/GUION-VOZ.md.
"""
import io, os, sys, importlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)

MODULOS = ["e01", "e02", "e03", "e04", "e05", "e06",
           "e07", "e08", "e09", "e10", "e11", "e12"]

INDEX = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #101B33; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #101B33; }}
      .escena {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      .chrome {{ position: absolute; inset: 0; pointer-events: none; }}
      /* sello de marca: archivo oficial sobre pastilla blanca, legible sobre el azul noche */
      .sello {{ position: absolute; right: 118px; bottom: 24px; width: 186px; height: 62px;
                border-radius: 34px; background: #FFFFFF; }}
      .sello img {{ position: absolute; left: 20px; top: 9px; width: 120px; height: 45px; }}
      /* barra de avance del módulo: se llena a lo largo de los {mins} minutos */
      .barra {{ position: absolute; left: 120px; bottom: 44px; width: 1520px; height: 5px;
                border-radius: 3px; background: rgba(174,188,214,0.22); overflow: hidden; }}
      .barra-fill {{ position: absolute; inset: 0; background: #AC841D;
                     transform: scaleX(0); transform-origin: 0 50%; }}
      .marca {{ position: absolute; bottom: 38px; width: 2px; height: 17px;
                border-radius: 1px; background: rgba(174,188,214,0.45); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
         data-width="1920" data-height="1080">
{escenas}
      <div id="chrome" class="clip chrome" data-start="0" data-duration="{total}" data-track-index="6">
        <div class="barra"><div class="barra-fill" id="barra-fill"></div></div>
{marcas}
        <div class="sello" id="sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann by SOFU" /></div>
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      /* la barra avanza sin pausa: da al espectador la medida del módulo */
      tl.fromTo("#barra-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {total}, ease: "none" }}, 0);
      tl.to(".barra, .marca", {{ opacity: 0, duration: 0.8, ease: "power1.in" }}, {fin});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def main():
    dest = os.path.join(RAIZ, "compositions")
    if not os.path.isdir(dest):
        os.makedirs(dest)

    t, filas, marcas = 0.0, [], []
    for m in MODULOS:
        mod = importlib.import_module(m)
        html = mod.escena()
        cid = html.split('data-composition-id="', 1)[1].split('"', 1)[0]
        io.open(os.path.join(dest, cid + ".html"), "w", encoding="utf-8", newline="\n").write(html)
        filas.append(
            '      <div id="el-%s" class="escena" data-composition-id="%s"\n'
            '           data-composition-src="compositions/%s.html"\n'
            '           data-start="%g" data-duration="%g" data-track-index="1"></div>'
            % (cid[:3], cid, cid, t, mod.DUR))
        print("%-22s  inicia %7.2f   dura %6.2f" % (cid, t, mod.DUR))
        t += mod.DUR
        if m != MODULOS[-1]:
            marcas.append(t)

    total = round(t, 2)
    mrc = "\n".join('        <div class="marca" style="left: %.1fpx"></div>'
                    % (120 + 1520 * (x / total)) for x in marcas)
    io.open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8", newline="\n").write(
        INDEX.format(total=total, escenas="\n".join(filas), marcas=mrc,
                     fin=round(total - 0.9, 2), mins="%.1f" % (total / 60.0)))
    print("-" * 52)
    print("TOTAL %.2f s = %d:%02d" % (total, int(total // 60), int(round(total % 60))))


if __name__ == "__main__":
    main()
