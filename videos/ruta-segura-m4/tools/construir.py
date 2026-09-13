# -*- coding: utf-8 -*-
"""Genera las sub-composiciones y el index.html de «Ruta Segura · Módulo 4».

Cada lámina dura lo que dura su narración más un respiro de cola, y cada aparición
cae sobre la frase que la nombra: los tiempos salen del alineamiento por carácter
que devuelve ElevenLabs (ver tools/cronometro.py).
"""
import io, os, sys, importlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)

MODULOS = ["e26", "e27", "e28", "e29", "e30", "e31", "e32", "e33", "e34"]

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
{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      /* la barra avanza sin pausa: da al espectador la medida del módulo */
{barra}      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


PISTA = "assets/voz/modulo-4.mp3"


def audio(total):
    """La locución va como un único <audio> en la raíz, alineado al cero.

    Solo entra si la pista existe: sin ella el proyecto sigue construyéndose y
    el video queda mudo, que es como se entregó la primera versión.

    Con `--sin-audio` se deja fuera a propósito. Chrome decodifica el MP3 entero
    a PCM (~250 MB para once minutos) y en una máquina de 8 GB eso basta para que
    el sistema mate el render. La pista se pega después con `tools/montar.py`:
    las dos arrancan en cero y duran lo mismo, así que el resultado es idéntico.
    """
    if "--sin-audio" in sys.argv:
        return ""
    if not os.path.exists(os.path.join(RAIZ, PISTA.replace("/", os.sep))):
        return ""
    return ('      <audio id="voz" class="clip" src="%s"\n'
            '             data-start="0" data-duration="%s" data-track-index="10"></audio>\n'
            % (PISTA, total))


def plan():
    """Orden, inicio y duración de cada escena. Lo comparte con tools/pista.py."""
    t, out = 0.0, []
    for m in MODULOS:
        mod = importlib.import_module(m)
        out.append({"modulo": m, "lamina": getattr(mod, "LAMINA", None),
                    "inicio": round(t, 3), "dura": mod.DUR})
        t += mod.DUR
    return out, round(t, 3)


def escribir(ruta, escenas, total, desde, hasta, ultima, con_audio=True):
    """Escribe un index con las escenas dadas, rebasadas a su propio cero.

    `desde`/`hasta` son los segundos que ese trozo ocupa dentro del máster: con
    ellos la barra de avance sigue midiendo el módulo completo aunque el archivo
    solo contenga una parte.
    """
    dur = round(hasta - desde, 3)
    filas = []
    for e in escenas:
        cid = e["cid"]
        filas.append(
            '      <div id="el-%s" class="escena" data-composition-id="%s"\n'
            '           data-composition-src="compositions/%s.html"\n'
            '           data-start="%g" data-duration="%g" data-track-index="1"></div>'
            % (cid[:3], cid, cid, round(e["inicio"] - desde, 3), e["dura"]))

    marcas = [x["inicio"] for x in TODAS[1:]]
    mrc = "\n".join('        <div class="marca" style="left: %.1fpx"></div>'
                    % (120 + 1520 * (x / total)) for x in marcas)

    barra = ('      tl.fromTo("#barra-fill", { scaleX: %.5f }, { scaleX: %.5f, duration: %g, ease: "none" }, 0);\n'
             % (desde / total, hasta / total, dur))
    if ultima:
        barra += ('      tl.to(".barra, .marca", { opacity: 0, duration: 0.8, ease: "power1.in" }, %g);\n'
                  % round(dur - 0.9, 2))

    io.open(ruta, "w", encoding="utf-8", newline="\n").write(
        INDEX.format(total=dur, escenas="\n".join(filas), marcas=mrc,
                     audio=audio(dur) if con_audio else "", barra=barra,
                     mins="%.1f" % (total / 60.0)))


TODAS = []


def main():
    global TODAS
    dest = os.path.join(RAIZ, "compositions")
    if not os.path.isdir(dest):
        os.makedirs(dest)

    t = 0.0
    TODAS = []
    for m in MODULOS:
        mod = importlib.import_module(m)
        html = mod.escena()
        cid = html.split('data-composition-id="', 1)[1].split('"', 1)[0]
        io.open(os.path.join(dest, cid + ".html"), "w", encoding="utf-8", newline="\n").write(html)
        TODAS.append({"cid": cid, "inicio": round(t, 3), "dura": mod.DUR})
        print("%-22s  inicia %7.2f   dura %6.2f" % (cid, t, mod.DUR))
        t += mod.DUR
    total = round(t, 2)

    escribir(os.path.join(RAIZ, "index.html"), TODAS, total, 0.0, total, True)
    print("-" * 52)
    print("TOTAL %.2f s = %d:%02d" % (total, int(total // 60), int(round(total % 60))))

    # `--partes N` reparte las escenas en N archivos que se renderizan por
    # separado: ffmpeg bufferea el MP4 entero en memoria, y once minutos de una
    # sola vez no caben en una máquina de 8 GB.
    if "--partes" in sys.argv:
        n = int(sys.argv[sys.argv.index("--partes") + 1])
        grupos, tam = [], (len(TODAS) + n - 1) // n
        for i in range(0, len(TODAS), tam):
            grupos.append(TODAS[i:i + tam])
        print("")
        for k, g in enumerate(grupos, 1):
            desde = g[0]["inicio"]
            hasta = round(g[-1]["inicio"] + g[-1]["dura"], 3)
            ruta = os.path.join(RAIZ, "index-parte-%d.html" % k)
            escribir(ruta, g, total, desde, hasta, k == len(grupos), con_audio=False)
            print("parte %d/%d  %s  %6.2f -> %6.2f  (%5.2f s, %d escenas)"
                  % (k, len(grupos), os.path.basename(ruta), desde, hasta, hasta - desde, len(g)))


if __name__ == "__main__":
    main()
