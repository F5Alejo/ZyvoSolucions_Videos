# -*- coding: utf-8 -*-
"""Lámina 10 · Retroalimentación del reto."""
import cronometro
from base import chrome, envoltura

LAMINA = 10
DUR = cronometro.duracion(LAMINA)

CSS = """
    .f-card { position: absolute; width: 812px; height: 300px; border-radius: 10px;
              background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
              opacity: 0; will-change: transform, opacity; }
    .f-n { position: absolute; left: 26px; top: 22px; width: 44px; height: 44px;
           border-radius: 22px; background: rgba(0,200,212,0.20); }
    .f-n span { position: absolute; left: 0; top: 9px; width: 44px; text-align: center;
                font-size: 24px; font-weight: 900; color: #7FE5EC; }
    .f-resp { position: absolute; left: 88px; top: 24px; font-size: 38px; font-weight: 900;
              color: #FFFFFF; }
    .f-txt { position: absolute; left: 26px; right: 24px; top: 92px; font-size: 26px;
             font-weight: 500; line-height: 1.38; color: #DCE4F2; opacity: 0; }
    .f-mas { position: absolute; left: 26px; right: 24px; font-size: 24px; font-weight: 500;
             line-height: 1.34; color: #AEBCD6; opacity: 0; }

    .f-cons { position: absolute; left: 128px; top: 664px; width: 1664px; height: 168px;
              border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
              opacity: 0; }
    .f-cons-t { position: absolute; left: 28px; top: 20px; font-size: 23px; font-weight: 900;
                letter-spacing: 0.16em; color: #D4A62B; }
    .f-cons-l { position: absolute; left: 28px; right: 26px; top: 58px; font-size: 26px;
                font-weight: 500; line-height: 1.36; color: #DCE4F2; }

    .f-regla { position: absolute; left: 128px; top: 878px; width: 1664px; font-size: 28px;
               font-weight: 800; line-height: 1.2; color: #00C8D4; opacity: 0; }
"""

CUERPO = chrome("10", "RETROALIMENTACIÓN",
                "Una regla segura conserva <b style=\"color:#D4A62B\">sus condiciones y límites</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="f-card" id="f-c1" style="left: 128px; top: 316px">
        <div class="f-n" data-layout-ignore><span>1</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t1">El error humano es posible; varias capas deben impedir que ese error produzca muerte o lesión grave.</div>
        <div class="f-mas" id="f-m1" style="top: 210px">A culpa solo al ciclista. C es incorrecta: ninguna prioridad es absoluta.</div>
      </div>

      <div class="f-card" id="f-c2" style="left: 980px; top: 316px">
        <div class="f-n" data-layout-ignore><span>2</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t2">Trabajador y empleador pueden acordar un día de descanso remunerado por cada seis meses en que se certifique el uso de la bicicleta para ir y volver del trabajo.</div>
        <div class="f-mas" id="f-m2" style="top: 236px">No es automático y no reemplaza las vacaciones.</div>
      </div>

      <div class="f-cons" id="f-cons">
        <div class="f-cons-t">CONSECUENCIA DE ELEGIR A O C</div>
        <div class="f-cons-l">Culpar solo al ciclista oculta fallas del sistema. Convertir condiciones jurídicas en promesas
          automáticas crea interpretaciones erróneas.</div>
      </div>

      <div class="f-regla" id="f-regla">Conserva siempre las condiciones y advertencias que cambian el significado técnico o jurídico de un mensaje.</div>
    </div>
"""

TL = """      /* 1.87 · «la opción correcta es la B» (pregunta 1) */
      tl.fromTo("#f-c1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 2.00);
      /* 5.84 · por qué */
      tl.fromTo("#f-t1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 6.00);
      /* 15.09 · por qué A y C no */
      tl.fromTo("#f-m1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 15.25);

      /* 27.11 · «la respuesta también es la B» (pregunta 2) */
      tl.fromTo("#f-c2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 27.25);
      /* 31.19 · la Ley 2466 de 2025 */
      tl.fromTo("#f-t2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 31.35);
      /* 44.45 · «no es automático y no reemplaza las vacaciones» */
      tl.fromTo("#f-m2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 44.60);

      /* la consecuencia de A o C acompaña a la explicación de la primera pregunta */
      tl.fromTo("#f-cons", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 20.60);

      /* 48.21 · la regla de comunicación con la que cierra la lámina */
      tl.fromTo("#f-regla", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 48.40);
"""


def escena():
    return envoltura("e10-retro", DUR, CSS, CUERPO, TL, lamina=LAMINA)
