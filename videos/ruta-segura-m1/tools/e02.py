# -*- coding: utf-8 -*-
"""Lámina 02 · Pregunta inicial. Cinco fallas encadenadas."""
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

DUR = 58.5

CSS = """
    /* la lluvia del PPTX queda al fondo, muy baja: ambienta sin competir con el texto */
    .q-foto { position: absolute; left: 50%; top: 50%; width: 2016px; height: 1344px;
              margin-left: -1008px; margin-top: -672px; opacity: 0.22; }
    .q-velo { position: absolute; inset: 0;
              background: radial-gradient(1500px 900px at 50% 40%, rgba(16,27,51,0.72) 0%, rgba(16,27,51,0.95) 78%); }

    .q-fila { position: absolute; left: 128px; top: 322px; width: 1668px; height: 156px; }
    .q-falla { position: absolute; top: 0; width: 300px; height: 156px; border-radius: 10px;
               background: rgba(174,188,214,0.10); border: 1.5px solid rgba(174,188,214,0.30);
               opacity: 0; will-change: transform, opacity; }
    .q-falla-n { position: absolute; left: 20px; top: 14px; font-size: 22px; font-weight: 900;
                 color: #D4A62B; letter-spacing: 0.1em; }
    .q-falla-t { position: absolute; left: 20px; right: 18px; top: 54px; font-size: 32px;
                 font-weight: 800; line-height: 1.14; color: #FFFFFF; }
    .q-eslabon { position: absolute; top: 76px; width: 42px; height: 3px; background: #AC841D;
                 transform: scaleX(0); transform-origin: 0 50%; }

    .q-cadena { position: absolute; left: 128px; top: 504px; font-size: 26px; font-weight: 800;
                letter-spacing: 0.18em; color: #D4A62B; opacity: 0; }
    .q-tags { position: absolute; left: 128px; top: 548px; display: flex; gap: 14px; }
    .q-tag { height: 46px; padding: 0 22px; display: flex; align-items: center; border-radius: 23px;
             border: 1.5px solid rgba(0,200,212,0.55); background: rgba(0,200,212,0.10);
             font-size: 22px; font-weight: 700; letter-spacing: 0.05em; color: #7FE5EC;
             opacity: 0; white-space: nowrap; }

    .q-preg { position: absolute; left: 128px; top: 640px; width: 1240px; font-size: 64px;
              font-weight: 900; line-height: 1.1; color: #FFFFFF; opacity: 0; }
    .q-escudo { position: absolute; left: 1470px; top: 632px; width: 226px; height: 132px;
                border-radius: 12px; background: #AC841D; opacity: 0; }
    .q-escudo-n { position: absolute; left: 0; top: 18px; width: 226px; text-align: center;
                  font-size: 60px; font-weight: 900; color: #101B33; line-height: 1; }
    .q-escudo-t { position: absolute; left: 0; top: 88px; width: 226px; text-align: center;
                  font-size: 19px; font-weight: 800; letter-spacing: 0.1em; color: #101B33; }

    .q-ctrl { position: absolute; top: 790px; height: 66px; padding: 0 26px; display: flex;
              align-items: center; border-radius: 8px; background: rgba(0,200,212,0.12);
              border-left: 5px solid #00C8D4; font-size: 27px; font-weight: 700; color: #DCE4F2;
              opacity: 0; white-space: nowrap; }
    .q-final { position: absolute; left: 128px; top: 872px; width: 1660px; font-size: 36px;
               font-weight: 800; line-height: 1.25; color: #00C8D4; opacity: 0; }
"""

FALLAS = [("01", "Lluvia"), ("02", "Presión<br />de tiempo"), ("03", "Poca luz"),
          ("04", "Freno<br />deficiente"), ("05", "Ruta alterada")]
CAJAS = "".join(
    '      <div class="q-falla" id="q-f%d" style="left: %dpx">\n'
    '        <div class="q-falla-n">%s</div><div class="q-falla-t">%s</div>\n'
    '      </div>\n' % (i + 1, i * 342, n, t) for i, (n, t) in enumerate(FALLAS))
ESLABONES = "".join('      <div class="q-eslabon" id="q-e%d" style="left: %dpx" data-layout-ignore></div>\n'
                    % (i + 1, 300 + i * 342) for i in range(4))

TAGS = ["Personales", "Técnicos", "Ambientales", "Organizacionales"]
TG = "".join('        <div class="q-tag" id="q-t%d">%s</div>\n' % (i + 1, t) for i, t in enumerate(TAGS))

CTRL = [("Un control sobre la bicicleta", 128), ("Uno sobre la operación", 690),
        ("Uno sobre la ruta", 1190)]
CT = "".join('      <div class="q-ctrl" id="q-c%d" style="left: %dpx">%s</div>\n'
             % (i + 1, x, t) for i, (t, x) in enumerate(CTRL))

CUERPO = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <img class="q-foto" id="q-foto" src="assets/fotos/lluvia.jpg"
           alt="Ciclista detenido en una intersección bajo lluvia" data-layout-ignore />
      <div class="q-velo" data-layout-ignore></div>
    </div>

""" + chrome("02", "PREGUNTA INICIAL", "Cinco fallas. <b style=\"color:#D4A62B\">Una sola salida.</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="q-fila">
""" + CAJAS + ESLABONES + """      </div>
      <div class="q-cadena" id="q-cadena">NO SON PROBLEMAS AISLADOS: FORMAN UNA CADENA</div>
      <div class="q-tags" id="q-tags">
""" + TG + """      </div>
      <div class="q-preg" id="q-preg">¿Pedaleas, corriges o detienes la misión?</div>
      <div class="q-escudo" id="q-escudo">
        <div class="q-escudo-n">+80</div><div class="q-escudo-t">RETO RISKMANN</div>
      </div>
""" + CT + """      <div class="q-final" id="q-final">No busques culpables: busca barreras que rompan la cadena antes de la salida.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 3.29 · «Imagina que debes realizar una entrega, pero está lloviendo…» */
"""
for _i, _t in enumerate([4.10, 5.90, 7.70, 9.50, 11.30]):
    TL += ('      tl.fromTo("#q-f%d", { opacity: 0, y: 34, scale: 0.94 }, '
           '{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, %.2f);\n' % (_i + 1, _t))

TL += """
      /* 16.83 · «Estas condiciones no son problemas aislados» — se ven los eslabones */
"""
for _i, _t in enumerate([16.95, 17.45, 17.95, 18.45]):
    TL += ('      tl.fromTo("#q-e%d", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 19.66 · «juntas forman una cadena que puede terminar en un siniestro» */
      tl.fromTo("#q-cadena", { opacity: 0, x: -26 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 19.80);

      /* 22.86 · «factores personales, técnicos, ambientales y organizacionales» */
"""
for _i, _t in enumerate([23.20, 24.20, 25.20, 26.20]):
    TL += ('      tl.fromTo("#q-t%d", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 29.92 · «¿existen condiciones suficientes para hacerlo sin trasladar el riesgo?» */
      tl.fromTo("#q-preg", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.62, ease: "power3.out" }, 30.10);
      tl.fromTo("#q-escudo", { opacity: 0, scale: 0.8, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 31.20);

""" + pausa_tl(39.60) + """
      /* 43.40 · «propone por lo menos tres controles» */
      tl.fromTo("#q-c1", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 44.00);
      tl.fromTo("#q-c2", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 48.30);
      tl.fromTo("#q-c3", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 50.30);

      /* 52.72 · «No busques culpables. Busca barreras…» */
      tl.to("#pausa", { opacity: 0, duration: 0.4, ease: "power1.in" }, 52.40);
      tl.fromTo("#q-final", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 52.90);
"""


def escena():
    return envoltura("e02-pregunta", DUR, CSS, CUERPO, TL)
