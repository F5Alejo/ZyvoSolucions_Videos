# -*- coding: utf-8 -*-
"""Lámina 15 · Actividad. Visible a 360°: proteger sin perder control."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 15
DUR = cronometro.duracion(LAMINA)

CSS = """
    .g-col { position: absolute; top: 316px; width: 540px; height: 470px; border-radius: 10px;
             background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
             opacity: 0; will-change: transform, opacity; }
    .g-t { position: absolute; left: 26px; top: 24px; font-size: 32px; font-weight: 900;
           letter-spacing: 0.05em; color: #D4A62B; }
    .g-raya { position: absolute; left: 26px; top: 72px; width: 60px; height: 4px; background: #00C8D4;
              transform: scaleX(0); transform-origin: 0 50%; }
    .g-item { position: absolute; left: 26px; right: 22px; font-size: 24px; font-weight: 500;
              line-height: 1.32; color: #DCE4F2; opacity: 0; }
    .g-item b { color: #FFFFFF; font-weight: 800; }

    .g-escudo { position: absolute; right: 128px; top: 150px; width: 208px; height: 96px;
                border-radius: 10px; background: #AC841D; opacity: 0; }
    .g-escudo-n { position: absolute; left: 0; top: 10px; width: 208px; text-align: center;
                  font-size: 46px; font-weight: 900; color: #101B33; line-height: 1; }
    .g-escudo-t { position: absolute; left: 0; top: 64px; width: 208px; text-align: center;
                  font-size: 17px; font-weight: 800; letter-spacing: 0.1em; color: #101B33; }

    .g-retiro { position: absolute; left: 120px; top: 812px; width: 1010px; height: 84px;
                border-radius: 10px; background: rgba(172,132,29,0.16); border-left: 6px solid #AC841D;
                opacity: 0; }
    .g-retiro span { position: absolute; left: 26px; right: 22px; top: 16px; font-size: 24px;
                     font-weight: 600; line-height: 1.3; color: #DCE4F2; }
    .g-retiro b { color: #D4A62B; font-weight: 800; }
    .g-tarea { position: absolute; left: 1158px; top: 812px; width: 642px; font-size: 25px;
               font-weight: 700; line-height: 1.3; color: #00C8D4; opacity: 0; }
"""

COLS = [(120, "CASCO", [("Talla adecuada, colocado <b>horizontal</b>.", 100),
                        ("Correas en <b>«V»</b> alrededor de las orejas.", 168),
                        ("Barboquejo ajustado y abrochado.", 236)]),
        (690, "SER VISTO", [("Luz <b>blanca</b> adelante.", 100),
                            ("Luz o elemento <b>rojo</b> atrás.", 168),
                            ("Reflectivos visibles: la carga no los cubre.", 236)]),
        (1260, "SIN BLOQUEAR", [("Ninguna prenda, capucha, audífono ni accesorio", 100),
                                ("puede bloquear <b>audición, visión, movilidad</b>", 168),
                                ("ni <b>control</b> de la bicicleta.", 236)])]

CC = ""
for _c, (_x, _t, _items) in enumerate(COLS):
    _it = "".join('        <div class="g-item" id="g-i%d%d" style="top: %dpx">%s</div>\n'
                  % (_c + 1, j + 1, y, tx) for j, (tx, y) in enumerate(_items))
    CC += ('      <div class="g-col" id="g-c%d" style="left: %dpx">\n'
           '        <div class="g-t">%s</div>\n'
           '        <div class="g-raya" id="g-r%d" data-layout-ignore></div>\n%s'
           '      </div>\n' % (_c + 1, _x, _t, _c + 1, _it))

CUERPO = chrome("15", "ACTIVIDAD", "Visible a 360°: <b style=\"color:#D4A62B\">proteger sin perder control</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="g-escudo" id="g-escudo">
        <div class="g-escudo-n">+300</div><div class="g-escudo-t">EN JUEGO</div>
      </div>
""" + CC + """
      <div class="g-retiro" id="g-retiro"><span>Tras un <b>impacto relevante</b>, daño o el límite del fabricante:
        retirar el casco y evaluarlo o reemplazarlo.</span></div>
      <div class="g-tarea" id="g-tarea">Pausa y revisa tu propio equipo frente a un espejo.</div>
    </div>

""" + PAUSA_HTML

TL = """      tl.fromTo("#g-escudo", { opacity: 0, scale: 0.8, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 0.60);

      /* 3.48 · el casco / 5.66 · cómo se ajusta */
      tl.fromTo("#g-c1", { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 3.55);
      tl.fromTo("#g-r1", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, 3.85);
      tl.fromTo("#g-i11", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 5.75);
      tl.fromTo("#g-i12", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 8.90);
      tl.fromTo("#g-i13", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 12.40);

      /* 15.65 · cuándo se retira el casco */
      tl.fromTo("#g-retiro", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 15.75);

      /* 25.18 · la visibilidad / 30.69 · los tres elementos */
      tl.fromTo("#g-c2", { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 25.25);
      tl.fromTo("#g-r2", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, 25.55);
      tl.fromTo("#g-i21", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 30.80);
      tl.fromTo("#g-i22", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 33.40);
      tl.fromTo("#g-i23", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 36.00);

      /* 39.85 · la compatibilidad / 43.09 · qué no puede bloquearse */
      tl.fromTo("#g-c3", { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 39.95);
      tl.fromTo("#g-r3", { scaleX: 0 }, { scaleX: 1, duration: 0.42, ease: "power2.out" }, 40.25);
      tl.fromTo("#g-i31", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 43.20);
      tl.fromTo("#g-i32", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 45.90);
      tl.fromTo("#g-i33", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 48.60);

      /* 52.29 · «pausa el video y revisa tu propio equipo» */
      tl.fromTo("#g-tarea", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 52.40);
""" + pausa_tl(52.90)


def escena():
    return envoltura("e15-visible", DUR, CSS, CUERPO, TL, lamina=LAMINA)
