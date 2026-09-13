# -*- coding: utf-8 -*-
"""Lámina 17 · Retroalimentación. La falla crítica no se negocia con el recorrido."""
import cronometro
from base import chrome, envoltura

LAMINA = 17
DUR = cronometro.duracion(LAMINA)

CSS = """
    .f-card { position: absolute; top: 316px; width: 812px; height: 322px; border-radius: 10px;
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

    .f-principio { position: absolute; left: 128px; top: 680px; width: 1664px; height: 160px;
                   border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
                   opacity: 0; }
    .f-p-t { position: absolute; left: 28px; top: 20px; font-size: 23px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; }
    .f-p-l { position: absolute; left: 28px; right: 26px; top: 58px; font-size: 27px;
             font-weight: 600; line-height: 1.34; color: #DCE4F2; }
    .f-p-l b { color: #FFFFFF; font-weight: 800; }

    .f-cierre { position: absolute; left: 128px; top: 878px; width: 1664px; font-size: 29px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

CUERPO = chrome("17", "RETROALIMENTACIÓN",
                "La falla crítica <b style=\"color:#D4A62B\">no se negocia con el recorrido</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="f-card" id="f-c1" style="left: 128px">
        <div class="f-n" data-layout-ignore><span>1</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t1">Un freno inoperante exige declarar la bicicleta no apta, inmovilizarla y reportarla.</div>
        <div class="f-mas" id="f-m1" style="top: 210px">Circular lentamente o cambiar de infraestructura no sustituye
          la capacidad de frenar.</div>
      </div>

      <div class="f-card" id="f-c2" style="left: 980px">
        <div class="f-n" data-layout-ignore><span>2</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t2">Tras un impacto relevante, retiro el casco y aplico las indicaciones del fabricante
          para evaluarlo o reemplazarlo.</div>
        <div class="f-mas" id="f-m2" style="top: 210px">El material interno puede haber absorbido energía sin mostrar
          grieta externa: prestarlo deja a otra persona sin protección efectiva.</div>
      </div>

      <div class="f-principio" id="f-principio">
        <div class="f-p-t">EL MISMO PRINCIPIO, EN DIRECCIÓN, RUEDA O LLANTA</div>
        <div class="f-p-l">No se normaliza la falla con <b>«es solo un trayecto corto»</b> ni con
          <b>«yo ya conozco la bicicleta»</b>.</div>
      </div>

      <div class="f-cierre" id="f-cierre">La autorización se recupera con mantenimiento o evaluación competente, no con confianza.</div>
    </div>
"""

TL = """      /* 0.00 · «en las dos preguntas, la respuesta correcta es la B» */
      tl.fromTo("#f-c1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.50);
      tl.fromTo("#f-c2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.85);

      /* 3.63 · por qué la primera */
      tl.fromTo("#f-t1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 3.70);
      /* 10.20 · «circular lentamente no sustituye la capacidad de frenar» */
      tl.fromTo("#f-m1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 10.30);

      /* 15.89 · por qué la segunda */
      tl.fromTo("#f-t2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 16.00);
      /* 23.57 · la energía absorbida sin grieta visible */
      tl.fromTo("#f-m2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 23.65);

      /* 34.86 · el principio general / 42.32 · las dos frases que lo rompen */
      tl.fromTo("#f-principio", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 34.95);

      /* 49.49 · «la autorización se recupera después del mantenimiento» */
      tl.fromTo("#f-cierre", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 49.60);
"""


def escena():
    return envoltura("e17-retro", DUR, CSS, CUERPO, TL, lamina=LAMINA)
