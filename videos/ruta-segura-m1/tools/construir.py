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

# Los quiz (reto, retroalimentación, repaso y evaluación) no van en el video:
# se implementan en la plataforma después de verlo.
MODULOS = ["e01", "e02", "e03", "e04", "e05", "e06", "e07", "e08", "e12"]

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
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
         data-width="1920" data-height="1080">
{escenas}
      <div id="chrome" class="clip chrome" data-start="0" data-duration="{total}" data-track-index="6">
        <div class="sello" id="sello"><img src="assets/marca/riskmann_logo_color.png" alt="RiskMann by SOFU" /></div>
      </div>
{audio}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


PISTA = "assets/voz/modulo-1.mp3"


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

    `desde`/`hasta` son los segundos que ese trozo ocupa dentro del máster.
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

    io.open(ruta, "w", encoding="utf-8", newline="\n").write(
        INDEX.format(total=dur, escenas="\n".join(filas),
                     audio=audio(dur) if con_audio else ""))


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
