# -*- coding: utf-8 -*-
"""Lámina 05 · Módulo 1. ¿Ser cuidadoso basta para estar seguro?

Dos columnas: a la izquierda la pregunta y la respuesta; a la derecha, primero
lo que la prudencia no controla y después la frase que el curso descarta.
"""
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

DUR = 65

CSS = """
    .s-foto { position: absolute; left: 50%; top: 50%; width: 2016px; height: 1344px;
              margin-left: -1008px; margin-top: -672px; opacity: 0.20; }
    .s-velo { position: absolute; inset: 0;
              background: radial-gradient(1500px 900px at 50% 42%, rgba(16,27,51,0.74) 0%, rgba(16,27,51,0.96) 78%); }

    /* --- columna izquierda --- */
    .s-preg { position: absolute; left: 128px; top: 318px; width: 860px; font-size: 60px;
              font-weight: 900; line-height: 1.1; color: #FFFFFF; opacity: 0; }
    .s-no { position: absolute; left: 128px; top: 486px; font-size: 92px; font-weight: 900;
            line-height: 1; color: #D4A62B; opacity: 0; }
    .s-no-r { position: absolute; left: 128px; top: 594px; width: 168px; height: 6px;
              background: #D4A62B; transform: scaleX(0); transform-origin: 0 50%; }
    .s-lead { position: absolute; left: 128px; top: 628px; width: 850px; font-size: 28px;
              font-weight: 600; line-height: 1.4; color: #AEBCD6; opacity: 0; }

    /* --- columna derecha, primer uso: lo que la prudencia no controla --- */
    .s-chip { position: absolute; left: 1060px; width: 736px; height: 62px; padding: 0 24px;
              display: flex; align-items: center; border-radius: 8px;
              background: rgba(174,188,214,0.10); border-left: 5px solid #AC841D;
              font-size: 27px; font-weight: 700; color: #FFFFFF; opacity: 0; }

    /* --- columna derecha, segundo uso: la frase descartada --- */
    .s-frase { position: absolute; left: 1060px; top: 372px; width: 736px; padding: 20px 26px;
               border-radius: 8px; background: rgba(174,188,214,0.10); font-size: 31px;
               font-weight: 700; font-style: italic; line-height: 1.26; color: #AEBCD6; opacity: 0; }
    .s-tacha { position: absolute; left: 1086px; top: 424px; width: 660px; height: 5px;
               background: #D4A62B; transform: scaleX(0); transform-origin: 0 50%; }
    .s-porque { position: absolute; left: 1060px; top: 520px; width: 736px; font-size: 27px;
                font-weight: 600; line-height: 1.36; color: #DCE4F2; opacity: 0; }
    .s-final { position: absolute; left: 1060px; top: 520px; width: 736px; font-size: 36px;
               font-weight: 800; line-height: 1.22; color: #00C8D4; opacity: 0; }

    /* --- banda inferior: las seis cosas que sí se observan --- */
    .s-cap { position: absolute; left: 128px; top: 782px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #7FE5EC; opacity: 0; }
    .s-fact { position: absolute; top: 824px; width: 258px; height: 96px; border-radius: 8px;
              background: rgba(0,200,212,0.10); border-bottom: 4px solid #00C8D4;
              opacity: 0; will-change: transform, opacity; }
    .s-fact span { position: absolute; left: 0; top: 32px; width: 258px; text-align: center;
                   font-size: 26px; font-weight: 800; color: #FFFFFF; }
"""

RIESGOS = ["Una bicicleta defectuosa", "Una intersección mal diseñada",
           "Una ruta inundada", "Una presión de tiempo inadecuada"]
CHIPS = "".join('      <div class="s-chip" id="s-r%d" style="top: %dpx">%s</div>\n'
                % (i + 1, 330 + i * 76, t) for i, t in enumerate(RIESGOS))

FACT = ["Persona", "Bicicleta", "Vía", "Velocidad", "Organización", "Respuesta"]
FACTS = "".join('      <div class="s-fact" id="s-f%d" style="left: %dpx"><span>%s</span></div>\n'
                % (i + 1, 128 + i * 278, t) for i, t in enumerate(FACT))

CUERPO = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <img class="s-foto" id="s-foto" src="assets/fotos/semaforo.jpg"
           alt="Ciclista y motociclista esperando en un semáforo" data-layout-ignore />
      <div class="s-velo" data-layout-ignore></div>
    </div>

""" + chrome("05", "MÓDULO 1", "Actor vial, reglas y <b style=\"color:#D4A62B\">Sistema Seguro</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="s-preg" id="s-preg">¿Ser cuidadoso basta para estar seguro?</div>
      <div class="s-no" id="s-no">NO.</div>
      <div class="s-no-r" id="s-no-r" data-layout-ignore></div>
      <div class="s-lead" id="s-lead">La prudencia individual es esencial, pero por sí sola no controla:</div>
""" + CHIPS + """
      <div class="s-cap" id="s-cap">LO QUE SÍ OBSERVO AL ANALIZAR EL RIESGO VIAL</div>
""" + FACTS + """
      <div class="s-frase" id="s-frase">«Si el ciclista se cuida, nada ocurre.»</div>
      <div class="s-tacha" id="s-tacha" data-layout-ignore></div>
      <div class="s-porque" id="s-porque">Esa idea deposita toda la responsabilidad en una sola persona y oculta las fallas del sistema.</div>
      <div class="s-final" id="s-final">Varias capas de protección deben trabajar juntas.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 3.23 · «¿ser cuidadoso basta para estar seguro?» */
      tl.fromTo("#s-preg", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 3.30);

      /* 5.84 · «Mi respuesta es no.» */
      tl.fromTo("#s-no", { opacity: 0, scale: 1.5, transformOrigin: "0% 50%" },
        { opacity: 1, scale: 1, duration: 0.45, ease: "power4.out" }, 5.90);
      tl.fromTo("#s-no-r", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, 6.20);

      /* 7.20 · «no controla por sí sola una bicicleta defectuosa, una intersección…» */
      tl.fromTo("#s-lead", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 7.40);
"""
for _i, _t in enumerate([10.40, 13.00, 15.60, 18.20]):
    TL += ('      tl.fromTo("#s-r%d", { opacity: 0, x: 46 }, { opacity: 1, x: 0, duration: 0.48, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 21.63 · «observo a la persona, la bicicleta, la vía, la velocidad, la organización…» */
      tl.fromTo("#s-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 21.80);
"""
for _i, _t in enumerate([23.40, 25.10, 26.80, 28.50, 30.20, 31.90]):
    TL += ('      tl.fromTo("#s-f%d", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 34.61 · la columna derecha cambia de contenido: entra la frase que se descarta */
      tl.to(".s-chip", { opacity: 0, x: 30, duration: 0.4, ease: "power2.in" }, 33.90);
      tl.to("#s-lead", { opacity: 0, duration: 0.4, ease: "power1.in" }, 33.90);
      tl.fromTo("#s-frase", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 34.75);
      tl.fromTo("#s-tacha", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, 38.10);

      /* 40.13 · «deposita toda la responsabilidad en una sola persona» */
      tl.fromTo("#s-porque", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 40.30);

""" + pausa_tl(45.90) + """
      /* 57.77 · «varias capas de protección deben trabajar juntas» */
      tl.to("#pausa", { opacity: 0, duration: 0.4, ease: "power1.in" }, 57.30);
      tl.to("#s-porque", { opacity: 0, duration: 0.4, ease: "power1.in" }, 57.30);
      tl.fromTo("#s-final", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 57.90);
"""


def escena():
    return envoltura("e05-cuidado", DUR, CSS, CUERPO, TL)
