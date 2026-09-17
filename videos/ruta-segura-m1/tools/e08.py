# -*- coding: utf-8 -*-
"""Lámina 08 · Caso práctico. Ruta inundada, sin iluminación y con retraso."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 8
DUR = cronometro.duracion(LAMINA)

CSS = """
    .k-foto { position: absolute; left: 1178px; top: 296px; width: 618px; height: 412px;
              border-radius: 10px; object-fit: cover; opacity: 0; }
    .k-foto-velo { position: absolute; left: 1178px; top: 296px; width: 618px; height: 412px;
                   border-radius: 10px; opacity: 0;
                   background: linear-gradient(0deg, rgba(16,27,51,0.88) 0%, rgba(16,27,51,0.08) 60%); }
    .k-reloj { position: absolute; left: 1210px; top: 596px; font-size: 62px; font-weight: 900;
               line-height: 1; color: #FFFFFF; opacity: 0; }
    .k-retraso { position: absolute; left: 1210px; top: 664px; font-size: 26px; font-weight: 700;
                 color: #D4A62B; opacity: 0; }

    .k-paso { position: absolute; left: 128px; width: 980px; height: 124px; border-radius: 10px;
              background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
              opacity: 0; will-change: transform, opacity; }
    .k-paso-n { position: absolute; left: 24px; top: 34px; font-size: 48px; font-weight: 900;
                color: #00C8D4; line-height: 1; }
    .k-paso-t { position: absolute; left: 96px; top: 22px; font-size: 36px; font-weight: 900;
                letter-spacing: 0.05em; color: #FFFFFF; }
    .k-paso-d { position: absolute; left: 96px; right: 22px; top: 70px; font-size: 25px;
                font-weight: 500; color: #AEBCD6; }

    .k-veto { position: absolute; left: 1178px; top: 760px; width: 618px; height: 152px;
              border-radius: 10px; background: rgba(172,132,29,0.14); border-left: 6px solid #AC841D;
              opacity: 0; }
    .k-veto-l { position: absolute; left: 24px; right: 20px; font-size: 24px; font-weight: 600;
                line-height: 1.32; color: #DCE4F2; opacity: 0; }

    .k-nota { position: absolute; left: 128px; width: 980px; font-size: 25px; font-weight: 500;
              line-height: 1.34; color: #AEBCD6; opacity: 0; }
    .k-final { position: absolute; left: 128px; top: 856px; width: 1040px; font-size: 28px;
               font-weight: 800; line-height: 1.22; color: #00C8D4; opacity: 0; }
"""

PASOS = [("1", "DETENERSE", "En un lugar seguro, fuera del flujo."),
         ("2", "AVISAR", "Por el canal definido, describiendo la condición."),
         ("3", "APLICAR", "Otra ruta, otro horario, otro plazo u otro medio.")]
PP = "".join(
    '      <div class="k-paso" id="k-p%d" style="top: %dpx">\n'
    '        <div class="k-paso-n">%s</div><div class="k-paso-t">%s</div>\n'
    '        <div class="k-paso-d">%s</div>\n'
    '      </div>\n' % (i + 1, 300 + i * 148, n, t, d) for i, (n, t, d) in enumerate(PASOS))

CUERPO = chrome("08", "CASO PRÁCTICO",
                "La ruta ordenada está <b style=\"color:#D4A62B\">inundada y sin iluminación</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <img class="k-foto" id="k-foto" src="assets/fotos/lluvia.jpg"
           alt="Intersección urbana bajo lluvia intensa" data-layout-ignore />
      <div class="k-foto-velo" id="k-foto-velo" data-layout-ignore></div>
      <div class="k-reloj" id="k-reloj">08:10</div>
      <div class="k-retraso" id="k-retraso">La entrega ya está retrasada.</div>

""" + PP + """
      <div class="k-veto" id="k-veto">
        <div class="k-veto-l" id="k-vt1" style="top: 22px">No continuar por presión de tiempo.</div>
        <div class="k-veto-l" id="k-vt2" style="top: 68px">No trasladar el riesgo al peatón usando el andén.</div>
      </div>

      <div class="k-nota" id="k-n1" style="top: 760px">Si el desplazamiento fue ordenado por la empresa, la exposición vial ocurre por causa u ocasión del trabajo y debe gestionarse.</div>
      <div class="k-nota" id="k-n2" style="top: 830px">Una misión segura necesita criterios claros de suspensión y respaldo organizacional para usarlos.</div>
      <div class="k-final" id="k-final">Si no existe una alternativa definida, esa ausencia también es un peligro que debe reportarse.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 1.59 · «La ruta ordenada está inundada, no tiene iluminación y la entrega ya está retrasada» */
      tl.fromTo(["#k-foto", "#k-foto-velo"], { opacity: 0, scale: 1.06, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.7, ease: "power3.out" }, 1.70);
      tl.fromTo("#k-reloj", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 3.40);
      tl.fromTo("#k-retraso", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 4.60);

      /* 7.71 · primera acción · 20.84 · segunda · 27.11 · tercera */
      tl.fromTo("#k-p1", { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 7.85);
      tl.fromTo("#k-p2", { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 21.00);
      tl.fromTo("#k-p3", { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 27.30);

      /* 11.40 · «No continúo para recuperar tiempo y tampoco uso el andén» */
      tl.fromTo("#k-veto", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 11.55);
      tl.fromTo("#k-vt1", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.out" }, 11.95);
      tl.fromTo("#k-vt2", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.out" }, 15.10);

      /* 34.86 y 44.77 · las dos notas de gestión */
      tl.fromTo("#k-n1", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 35.05);
      tl.fromTo("#k-n2", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 44.95);

""" + pausa_tl(52.30) + """
      /* 63.56 · «esa ausencia también es un peligro que debe reportarse» */
      tl.to(["#k-n1", "#k-n2"], { opacity: 0, duration: 0.45, ease: "power1.in" }, 63.10);
      /* entra cuando las notas ya salieron: el recorte de la invitación a pausar dejó las dos cosas juntas */
      tl.fromTo("#k-final", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 64.30);
"""


def escena():
    return envoltura("e08-caso", DUR, CSS, CUERPO, TL, lamina=LAMINA)
