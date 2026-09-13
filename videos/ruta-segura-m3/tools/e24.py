# -*- coding: utf-8 -*-
"""Lámina 24 · Retroalimentación. La anticipación crea tiempo y espacio.

La segunda mitad de la lámina enlaza prevención con respuesta: la cadena
Proteger → Alertar → Socorrer → Reportar entra eslabón a eslabón, uno por frase.
"""
import cronometro
from base import chrome, envoltura

LAMINA = 24
DUR = cronometro.duracion(LAMINA)

CSS = """
    .f-card { position: absolute; top: 300px; width: 812px; height: 250px; border-radius: 10px;
              background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
              opacity: 0; will-change: transform, opacity; }
    .f-n { position: absolute; left: 26px; top: 22px; width: 44px; height: 44px;
           border-radius: 22px; background: rgba(0,200,212,0.20); }
    .f-n span { position: absolute; left: 0; top: 9px; width: 44px; text-align: center;
                font-size: 24px; font-weight: 900; color: #7FE5EC; }
    .f-resp { position: absolute; left: 88px; top: 24px; font-size: 36px; font-weight: 900;
              color: #FFFFFF; }
    .f-txt { position: absolute; left: 26px; right: 24px; top: 88px; font-size: 25px;
             font-weight: 500; line-height: 1.34; color: #DCE4F2; opacity: 0; }
    .f-mas { position: absolute; left: 26px; right: 24px; top: 168px; font-size: 23px;
             font-weight: 500; line-height: 1.3; color: #AEBCD6; opacity: 0; }

    /* --- la cadena de respuesta --- */
    .f-cap { position: absolute; left: 128px; top: 592px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .f-paso { position: absolute; top: 634px; width: 396px; height: 172px; border-radius: 10px;
              background: rgba(172,132,29,0.14); border-left: 5px solid #AC841D;
              opacity: 0; will-change: transform, opacity; }
    .f-p-t { position: absolute; left: 24px; top: 18px; font-size: 28px; font-weight: 900;
             letter-spacing: 0.05em; color: #D4A62B; }
    .f-p-d { position: absolute; left: 24px; right: 20px; top: 60px; font-size: 22px;
             font-weight: 500; line-height: 1.3; color: #DCE4F2; }
    .f-flecha { position: absolute; top: 716px; width: 22px; height: 3px; background: #AC841D;
                transform: scaleX(0); transform-origin: 0 50%; }

    .f-veto { position: absolute; left: 128px; top: 830px; width: 1664px; font-size: 26px;
              font-weight: 600; line-height: 1.3; color: #DCE4F2; opacity: 0; }
    .f-veto b { color: #FFFFFF; font-weight: 800; }
    .f-cierre { position: absolute; left: 128px; top: 886px; width: 1664px; font-size: 27px;
                font-weight: 800; color: #00C8D4; opacity: 0; }
"""

PASOS = [("PROTEGER", "Verificar peligros y protegerme: no crear una segunda víctima."),
         ("ALERTAR", "Al 123 y al canal interno."),
         ("SOCORRER", "Únicamente dentro de mi competencia."),
         ("REPORTAR", "El evento, siempre.")]
PP = "".join(
    '      <div class="f-paso" id="f-s%d" style="left: %dpx">\n'
    '        <div class="f-p-t">%s</div>\n'
    '        <div class="f-p-d">%s</div>\n'
    '      </div>\n' % (i + 1, 128 + i * 428, t, d) for i, (t, d) in enumerate(PASOS))
FL = "".join('      <div class="f-flecha" id="f-fl%d" style="left: %dpx" data-layout-ignore></div>\n'
             % (i + 1, 534 + i * 428) for i in range(3))

CUERPO = chrome("24", "RETROALIMENTACIÓN",
                "La anticipación crea <b style=\"color:#D4A62B\">tiempo y espacio para corregir</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="f-card" id="f-c1" style="left: 128px">
        <div class="f-n" data-layout-ignore><span>1</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t1">Observar, señalizar, volver a verificar y ejecutar de forma estable.</div>
        <div class="f-mas" id="f-m1">Girar primero elimina el tiempo de reacción de los demás; el timbre no
          reemplaza la verificación.</div>
      </div>

      <div class="f-card" id="f-c2" style="left: 980px">
        <div class="f-n" data-layout-ignore><span>2</span></div>
        <div class="f-resp">Respuesta B</div>
        <div class="f-txt" id="f-t2">Permanecer fuera del punto ciego y de la trayectoria de giro.</div>
        <div class="f-mas" id="f-m2">Pasar entre el vehículo y el borde puede dejarme sin espacio cuando el
          remolque cierra la curva.</div>
      </div>

      <div class="f-cap" id="f-cap">Y SI YA OCURRIÓ: LA CADENA DE RESPUESTA</div>
""" + PP + FL + """
      <div class="f-veto" id="f-veto">No muevo a una persona lesionada, salvo <b>peligro mayor inmediato</b>
        o indicación competente.</div>
      <div class="f-cierre" id="f-cierre">Tras un golpe en la cabeza: retirar a la persona de la conducción y aplicar el protocolo de valoración.</div>
    </div>
"""

TL = """      /* 0.00 · «las dos respuestas correctas son B» */
      tl.fromTo("#f-c1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.45);
      tl.fromTo("#f-c2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.80);

      /* 2.75 · la secuencia / 9.71 · por qué no las otras */
      tl.fromTo("#f-t1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 2.85);
      tl.fromTo("#f-m1", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 9.80);

      /* 17.07 · el camión / 22.74 · el remolque que cierra la curva */
      tl.fromTo("#f-t2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 17.18);
      tl.fromTo("#f-m2", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 22.84);

      /* 29.62 · «enlazo la prevención con la respuesta» */
      tl.fromTo("#f-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 29.72);

      /* 34.82 · proteger / 42.32 · alertar y socorrer / reportar */
      tl.fromTo("#f-s1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 34.92);
      tl.fromTo("#f-s2", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 42.42);
      tl.fromTo("#f-s3", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 44.60);
      tl.fromTo("#f-s4", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 46.80);
      tl.fromTo("#f-fl1", { scaleX: 0 }, { scaleX: 1, duration: 0.32, ease: "power2.out" }, 42.20);
      tl.fromTo("#f-fl2", { scaleX: 0 }, { scaleX: 1, duration: 0.32, ease: "power2.out" }, 44.40);
      tl.fromTo("#f-fl3", { scaleX: 0 }, { scaleX: 1, duration: 0.32, ease: "power2.out" }, 46.60);

      /* 49.20 · «no muevo a una persona lesionada» */
      tl.fromTo("#f-veto", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 49.30);

      /* 55.48 · el golpe en la cabeza */
      tl.fromTo("#f-cierre", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 55.58);
"""


def escena():
    return envoltura("e24-retro", DUR, CSS, CUERPO, TL, lamina=LAMINA)
