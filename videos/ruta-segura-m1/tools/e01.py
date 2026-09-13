# -*- coding: utf-8 -*-
"""Lámina 01 · Portada. 60 s, atada a la narración medida de la lámina 1."""
import cronometro
from base import envoltura, PAUSA_HTML, pausa_tl

LAMINA = 1
DUR = cronometro.duracion(LAMINA)

CSS = """
    /* --- fotografía del propio PPTX, con empuje lento: la única animación continua --- */
    .p-foto { position: absolute; left: 50%; top: 50%; width: 2112px; height: 1188px;
              margin-left: -1056px; margin-top: -594px; }
    .p-velo { position: absolute; inset: 0;
              background:
                linear-gradient(90deg, rgba(16,27,51,0.97) 0%, rgba(16,27,51,0.93) 40%,
                                       rgba(16,27,51,0.55) 68%, rgba(16,27,51,0.18) 100%),
                linear-gradient(0deg, rgba(16,27,51,0.92) 0%, rgba(16,27,51,0) 38%); }

    /* --- fase A: portada --- */
    .p-ceja { position: absolute; left: 128px; top: 300px; font-size: 26px; font-weight: 800;
              letter-spacing: 0.26em; color: #D4A62B; opacity: 0; }
    .p-tit { position: absolute; left: 122px; top: 346px; font-size: 148px; font-weight: 900;
             letter-spacing: -0.02em; line-height: 1; color: #FFFFFF; white-space: nowrap; }
    .p-tit span { display: inline-block; opacity: 0; will-change: transform, opacity; }
    .p-sub { position: absolute; left: 128px; top: 520px; font-size: 58px; font-weight: 700;
             color: #00C8D4; opacity: 0; white-space: nowrap; }
    .p-raya { position: absolute; left: 128px; top: 604px; width: 520px; height: 4px;
              background: #00C8D4; transform: scaleX(0); transform-origin: 0 50%; }
    .p-chips { position: absolute; left: 128px; top: 656px; display: flex; gap: 16px; }
    .p-chip { height: 54px; padding: 0 26px; display: flex; align-items: center; border-radius: 27px;
              background: rgba(174,188,214,0.12); border: 1.5px solid rgba(174,188,214,0.34);
              font-size: 24px; font-weight: 700; letter-spacing: 0.05em; color: #DCE4F2;
              opacity: 0; white-space: nowrap; }

    /* --- fase B: promesa del curso --- */
    .p-lock { position: absolute; left: 128px; top: 112px; font-size: 26px; font-weight: 800;
              letter-spacing: 0.22em; color: #D4A62B; opacity: 0; white-space: nowrap; }
    .p-badge { position: absolute; left: 128px; top: 170px; height: 58px; padding: 0 28px;
               display: flex; align-items: center; border-radius: 8px; background: #AC841D;
               font-size: 25px; font-weight: 800; letter-spacing: 0.06em; color: #101B33;
               opacity: 0; white-space: nowrap; }
    .p-head { position: absolute; left: 128px; top: 268px; font-size: 40px; font-weight: 600;
              color: #AEBCD6; opacity: 0; white-space: nowrap; }
    .p-fila { position: absolute; left: 128px; width: 1180px; height: 96px; opacity: 0;
              will-change: transform, opacity; }
    .p-num { position: absolute; left: 0; top: 16px; font-size: 34px; font-weight: 900;
             color: #D4A62B; letter-spacing: 0.08em; }
    .p-txt { position: absolute; left: 92px; top: 2px; font-size: 50px; font-weight: 800;
             color: #FFFFFF; white-space: nowrap; }
    .p-nota { position: absolute; left: 128px; top: 862px; width: 1180px; font-size: 26px;
              font-weight: 500; line-height: 1.42; color: #AEBCD6; opacity: 0; }

    /* --- fase C: cierre --- */
    .p-oscuro { position: absolute; inset: 0; background: rgba(16,27,51,0.78); opacity: 0; }
    .p-cierre { position: absolute; left: 0; top: 452px; width: 1920px; text-align: center;
                font-size: 62px; font-weight: 800; line-height: 1.2; color: #FFFFFF; opacity: 0; }
    .p-cierre b { color: #00C8D4; font-weight: 800; }
"""

VERBOS = [("01", "Reconocer los peligros de la ruta"),
          ("02", "Revisar la bicicleta antes de salir"),
          ("03", "Circular visible y predecible"),
          ("04", "Responder ante lo inesperado")]

FILAS = "".join(
    '      <div class="p-fila" id="p-f%d" style="top: %dpx">\n'
    '        <div class="p-num">%s</div><div class="p-txt">%s</div>\n'
    '      </div>\n' % (i + 1, 350 + i * 120, n, t) for i, (n, t) in enumerate(VERBOS))

CHIPS = ["Capacitación condensada", "Trabajadores ciclistas", "Colombia", "120 min"]
CH = "".join('        <div class="p-chip" id="p-c%d">%s</div>\n' % (i + 1, c) for i, c in enumerate(CHIPS))

CUERPO = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <img class="p-foto" id="p-foto" src="assets/fotos/amanecer.jpg"
           alt="Ciclista urbano al amanecer" data-layout-ignore />
      <div class="p-velo" data-layout-ignore></div>
    </div>

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="2">
      <div class="p-ceja" id="p-ceja">RISKMANN · CAPACITACIÓN VIRTUAL</div>
      <div class="p-tit" id="p-tit"><span id="p-t1">RUTA</span> <span id="p-t2">SEGURA</span></div>
      <div class="p-sub" id="p-sub">Cada pedaleo cuenta</div>
      <div class="p-raya" id="p-raya" data-layout-ignore></div>
      <div class="p-chips" id="p-chips">
""" + CH + """      </div>
    </div>

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="p-lock" id="p-lock">RUTA SEGURA · CADA PEDALEO CUENTA</div>
      <div class="p-badge" id="p-badge">EXPERIENCIA VIRTUAL CONDENSADA · 120 MIN</div>
      <div class="p-head" id="p-head">Al terminar vas a poder:</div>
""" + FILAS + """      <div class="p-nota" id="p-nota">Se basa en un programa integral de doce horas: no sustituye la práctica
        controlada ni la demostración presencial de competencias.</div>
    </div>

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="4">
      <div class="p-oscuro" id="p-oscuro" data-layout-ignore></div>
      <div class="p-cierre" id="p-cierre">Cada decisión segura<br /><b>comienza antes de pedalear.</b></div>
    </div>

""" + PAUSA_HTML

TL = ("""      /* empuje continuo de la fotografía durante toda la lámina */
      tl.fromTo("#p-foto", { scale: 1, x: 0 }, { scale: 1.075, x: -40, duration: %.1f, ease: "none" }, 0);

      /* 0.00 · «Te doy la bienvenida a Ruta Segura:» */
"""  % DUR) + """      tl.fromTo("#p-ceja", { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 0.15);
      tl.set("#p-t1", { opacity: 1 }, 0.45);
      tl.fromTo("#p-t1", { y: 120, rotationX: -48, transformOrigin: "50% 100%" },
        { y: 0, rotationX: 0, duration: 0.7, ease: "power4.out" }, 0.45);
      tl.set("#p-t2", { opacity: 1 }, 0.62);
      tl.fromTo("#p-t2", { y: 120, rotationX: -48, transformOrigin: "50% 100%" },
        { y: 0, rotationX: 0, duration: 0.7, ease: "power4.out" }, 0.62);

      /* 2.11 · «cada pedaleo cuenta.» */
      tl.fromTo("#p-sub", { opacity: 0, x: -44 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, 2.11);
      tl.fromTo("#p-raya", { scaleX: 0 }, { scaleX: 1, duration: 0.55, ease: "power2.out" }, 2.35);

      /* 3.39 · «voy a acompañarte a tomar decisiones más seguras…» */
      tl.fromTo("#p-c1", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 3.60);
      tl.fromTo("#p-c2", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 3.85);
      tl.fromTo("#p-c3", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 4.10);
      tl.fromTo("#p-c4", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.42, ease: "power2.out" }, 4.35);

      /* 15.80 · la portada se retira antes de «Mi propósito no es que memorices…» */
      tl.to(["#p-ceja", "#p-sub", "#p-raya", "#p-chips"], { opacity: 0, y: -26, duration: 0.5, ease: "power2.in" }, 15.80);
      tl.to("#p-tit", { opacity: 0, y: -40, scale: 0.82, transformOrigin: "0% 50%", duration: 0.6, ease: "power2.inOut" }, 15.95);
      tl.fromTo("#p-lock", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 16.45);

      /* 17.09 · «reconocer peligros, revisar tu bicicleta, circular…, responder…» */
      tl.fromTo("#p-head", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 16.90);
"""

for _i, _t in enumerate([17.60, 20.90, 24.10, 27.30]):
    TL += ('      tl.fromTo("#p-f%d", { opacity: 0, x: -70 }, { opacity: 1, x: 0, duration: 0.55, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 30.77 · «experiencia virtual condensada de ciento veinte minutos» */
      tl.fromTo("#p-badge", { opacity: 0, scale: 0.86, transformOrigin: "0% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 30.90);

      /* 38.11 · «programa integral de doce horas… no sustituye la práctica» */
      tl.fromTo("#p-nota", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 38.30);

""" + pausa_tl(48.00) + """
      /* 54.98 · «cada decisión segura comienza antes de pedalear.» */
      tl.to("#pausa", { opacity: 0, duration: 0.4, ease: "power1.in" }, 54.40);
      tl.fromTo("#p-oscuro", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.inOut" }, 54.40);
      tl.to(["#p-lock", "#p-badge", "#p-head", ".p-fila", "#p-nota"], { opacity: 0, duration: 0.6, ease: "power1.in" }, 54.40);
      tl.fromTo("#p-cierre", { opacity: 0, y: 34, scale: 0.94 },
        { opacity: 1, y: 0, scale: 1, duration: 0.85, ease: "power3.out" }, 55.05);
      tl.to(["#p-cierre", "#p-oscuro"], { opacity: 0, duration: 0.7, ease: "power1.in" }, 59.20);
"""


def escena():
    return envoltura("e01-portada", DUR, CSS, CUERPO, TL, lamina=LAMINA, con_chrome=False)
