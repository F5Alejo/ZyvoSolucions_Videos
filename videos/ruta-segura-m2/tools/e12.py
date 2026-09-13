# -*- coding: utf-8 -*-
"""Lámina 12 · Apertura del módulo 2. ¿Qué defecto obliga a no salir?"""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 12
DUR = cronometro.duracion(LAMINA)

CSS = """
    /* el taller del propio PPTX, al fondo: sitúa el módulo sin competir con el texto */
    .b-foto { position: absolute; left: 50%; top: 50%; width: 2016px; height: 1344px;
              margin-left: -1008px; margin-top: -672px; opacity: 0.20; }
    .b-velo { position: absolute; inset: 0;
              background: radial-gradient(1500px 900px at 50% 42%, rgba(16,27,51,0.74) 0%, rgba(16,27,51,0.96) 78%); }

    .b-preg { position: absolute; left: 128px; top: 316px; width: 940px; font-size: 62px;
              font-weight: 900; line-height: 1.1; color: #FFFFFF; opacity: 0; }

    /* la definición que el módulo descarta, y la que pone en su lugar */
    .b-no { position: absolute; left: 128px; top: 470px; width: 940px; padding: 18px 24px;
            border-radius: 8px; background: rgba(174,188,214,0.10); font-size: 29px;
            font-weight: 600; font-style: italic; line-height: 1.28; color: #AEBCD6; opacity: 0; }
    .b-tacha { position: absolute; left: 152px; top: 516px; width: 830px; height: 5px;
               background: #D4A62B; transform: scaleX(0); transform-origin: 0 50%; }
    .b-si { position: absolute; left: 128px; top: 592px; font-size: 54px; font-weight: 900;
            line-height: 1; color: #00C8D4; opacity: 0; }

    .b-cap { position: absolute; left: 1120px; top: 300px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .b-falla { position: absolute; left: 1120px; width: 676px; height: 64px; padding: 0 22px;
               display: flex; align-items: center; border-radius: 8px;
               background: rgba(172,132,29,0.14); border-left: 5px solid #AC841D;
               font-size: 25px; font-weight: 700; color: #FFFFFF; opacity: 0; }
    .b-veredicto { position: absolute; left: 1120px; top: 706px; width: 676px; font-size: 32px;
                   font-weight: 900; line-height: 1.2; color: #D4A62B; opacity: 0; }

    /* las tres excusas que no eliminan la falla */
    .b-excusas { position: absolute; left: 128px; top: 680px; display: flex; gap: 16px; }
    .b-ex { height: 58px; padding: 0 24px; display: flex; align-items: center; border-radius: 29px;
            border: 1.5px solid rgba(174,188,214,0.34); background: rgba(174,188,214,0.10);
            font-size: 24px; font-weight: 700; color: #DCE4F2; opacity: 0; white-space: nowrap; }
    .b-ex-tacha { position: absolute; left: 140px; top: 708px; width: 776px; height: 4px;
                  background: #D4A62B; transform: scaleX(0); transform-origin: 0 50%; }

    .b-control { position: absolute; left: 128px; top: 790px; width: 940px; font-size: 30px;
                 font-weight: 700; line-height: 1.3; color: #FFFFFF; opacity: 0; }
    .b-control b { color: #00C8D4; font-weight: 800; }
    .b-escudo { position: absolute; left: 1470px; top: 790px; width: 226px; height: 124px;
                border-radius: 12px; background: #AC841D; opacity: 0; }
    .b-escudo-n { position: absolute; left: 0; top: 16px; width: 226px; text-align: center;
                  font-size: 56px; font-weight: 900; color: #101B33; line-height: 1; }
    .b-escudo-t { position: absolute; left: 0; top: 82px; width: 226px; text-align: center;
                  font-size: 18px; font-weight: 800; letter-spacing: 0.1em; color: #101B33; }
    .b-final { position: absolute; left: 128px; top: 878px; width: 1240px; font-size: 34px;
               font-weight: 800; line-height: 1.22; color: #00C8D4; opacity: 0; }
"""

FALLAS = ["Freno inoperante", "Rueda o dirección floja", "Fisura estructural",
          "Llanta sin condición segura", "Sin luz obligatoria de noche"]
FF = "".join('      <div class="b-falla" id="b-f%d" style="top: %dpx">%s</div>\n'
             % (i + 1, 348 + i * 72, t) for i, t in enumerate(FALLAS))

EXCUSAS = ["La distancia es corta", "Conozco la ruta", "Voy despacio"]
EX = "".join('        <div class="b-ex" id="b-x%d">%s</div>\n' % (i + 1, t) for i, t in enumerate(EXCUSAS))

CUERPO = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <img class="b-foto" id="b-foto" src="assets/fotos/taller.jpg"
           alt="Inspección de frenos en un taller de bicicletas" data-layout-ignore />
      <div class="b-velo" data-layout-ignore></div>
    </div>

""" + chrome("12", "MÓDULO 2", "Bicicleta lista, <b style=\"color:#D4A62B\">protección y visibilidad</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="b-preg" id="b-preg">¿Qué defecto obliga a no salir?</div>
      <div class="b-no" id="b-no" data-layout-allow-occlusion>«Una lista para marcar rápidamente.»</div>
      <div class="b-tacha" id="b-tacha" data-layout-ignore></div>
      <div class="b-si" id="b-si">Es un proceso de decisión.</div>

      <div class="b-cap" id="b-cap">SI ENCUENTRO CUALQUIERA DE ESTO</div>
""" + FF + """      <div class="b-veredicto" id="b-veredicto">Declaro la bicicleta NO APTA.</div>

      <div class="b-excusas" id="b-excusas">
""" + EX + """      </div>
      <div class="b-ex-tacha" id="b-ex-tacha" data-layout-ignore></div>

      <div class="b-control" id="b-control">Retirarla no es incumplir la misión: es <b>aplicar un control preventivo</b>.</div>
      <div class="b-escudo" id="b-escudo">
        <div class="b-escudo-n">+80</div><div class="b-escudo-t">RETO RISKMANN</div>
      </div>
      <div class="b-final" id="b-final">Una secuencia que puedes repetir antes de cada uso.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 3.28 · «¿qué defecto me obliga a no salir?» */
      tl.fromTo("#b-preg", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 3.35);

      /* 6.11 · «no es una formalidad ni una lista para marcar rápidamente» */
      tl.fromTo("#b-no", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 6.20);
      tl.fromTo("#b-tacha", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.out" }, 9.60);

      /* 12.51 · «Es un proceso de decisión.» */
      tl.fromTo("#b-si", { opacity: 0, scale: 1.28, transformOrigin: "0% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "power4.out" }, 12.60);

      /* 14.72 · la enumeración de fallas críticas, una por una */
      tl.fromTo("#b-cap", { opacity: 0, x: 26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 14.80);
"""
for _i, _t in enumerate([16.40, 18.90, 21.40, 23.60, 26.10]):
    TL += ('      tl.fromTo("#b-f%d", { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 0.48, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """      tl.fromTo("#b-veredicto", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 28.60);

      /* 30.45 · «la distancia corta, una ruta conocida o ir despacio no eliminan la falla» */
      tl.fromTo("#b-x1", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 30.60);
      tl.fromTo("#b-x2", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 31.80);
      tl.fromTo("#b-x3", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 33.00);
      tl.fromTo("#b-ex-tacha", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, 34.60);

      /* 38.00 · «retirarla no significa incumplir la misión» */
      tl.fromTo("#b-control", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 38.10);
      tl.fromTo("#b-escudo", { opacity: 0, scale: 0.82, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 39.20);

""" + pausa_tl(45.45) + """
      /* 53.55 · «una secuencia que puedes repetir antes de cada uso» */
      tl.to("#pausa", { opacity: 0, duration: 0.4, ease: "power1.in" }, 53.10);
      tl.fromTo("#b-final", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 53.65);
"""


def escena():
    return envoltura("e12-apertura", DUR, CSS, CUERPO, TL, lamina=LAMINA)
