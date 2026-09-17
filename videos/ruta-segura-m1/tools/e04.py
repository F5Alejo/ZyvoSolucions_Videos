# -*- coding: utf-8 -*-
"""Lámina 04 · Ruta de aprendizaje. Tres módulos y las reglas del Reto RiskMann."""
import cronometro
from base import chrome, envoltura

LAMINA = 4
DUR = cronometro.duracion(LAMINA)

CSS = """
    .m-riel { position: absolute; left: 128px; top: 372px; width: 1664px; height: 4px;
              background: rgba(174,188,214,0.26); transform: scaleX(0); transform-origin: 0 50%; }
    .m-card { position: absolute; top: 296px; width: 520px; height: 230px; border-radius: 10px;
              background: rgba(174,188,214,0.09); border: 1.5px solid rgba(174,188,214,0.26);
              opacity: 0; will-change: transform, opacity; }
    .m-num { position: absolute; left: -1px; top: -1px; width: 88px; height: 62px;
             border-radius: 10px 0 10px 0; background: #AC841D; }
    .m-num span { position: absolute; left: 0; top: 12px; width: 88px; text-align: center;
                  font-size: 32px; font-weight: 900; color: #101B33; }
    .m-tit { position: absolute; left: 108px; top: 14px; font-size: 38px; font-weight: 900;
             color: #FFFFFF; }
    .m-sub { position: absolute; left: 30px; right: 26px; top: 92px; font-size: 27px;
             font-weight: 600; color: #00C8D4; }
    .m-des { position: absolute; left: 30px; right: 26px; top: 136px; font-size: 24px;
             font-weight: 500; line-height: 1.36; color: #AEBCD6; }

    .m-reto { position: absolute; left: 128px; top: 574px; font-size: 26px; font-weight: 900;
              letter-spacing: 0.18em; color: #D4A62B; opacity: 0; }
    .m-esc { position: absolute; top: 622px; width: 340px; height: 148px; border-radius: 10px;
             background: rgba(172,132,29,0.14); border: 1.5px solid #AC841D;
             opacity: 0; will-change: transform, opacity; }
    .m-esc-n { position: absolute; left: 0; top: 18px; width: 340px; text-align: center;
               font-size: 54px; font-weight: 900; color: #D4A62B; line-height: 1; }
    .m-esc-t { position: absolute; left: 0; top: 88px; width: 340px; text-align: center;
               font-size: 24px; font-weight: 700; color: #DCE4F2; }

    .m-veto { position: absolute; left: 1210px; top: 614px; width: 582px; height: 164px;
              border-radius: 10px; background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
              opacity: 0; }
    .m-veto-l { position: absolute; left: 26px; right: 22px; font-size: 24px; font-weight: 600;
                line-height: 1.34; color: #DCE4F2; opacity: 0; }

    .m-nota { position: absolute; left: 128px; top: 802px; width: 1664px; font-size: 27px;
              font-weight: 500; color: #AEBCD6; opacity: 0; }
    .m-cierre { position: absolute; left: 128px; top: 862px; width: 1664px; font-size: 36px;
                font-weight: 800; line-height: 1.2; color: #FFFFFF; opacity: 0; }
    .m-cierre b { color: #00C8D4; font-weight: 800; }
"""

MODS = [("01", "Actor vial y reglas", "Responsabilidad compartida",
         "El ciclista como conductor, las reglas básicas y el Sistema Seguro."),
        ("02", "Bicicleta lista", "Inspección y visibilidad",
         "Fallas críticas, retiro de servicio, protección y visibilidad."),
        ("03", "Misión segura", "Ruta, maniobra y respuesta",
         "Planeación de ruta, maniobras, factor humano y respuesta ante incidentes.")]
CARDS = "".join(
    '      <div class="m-card" id="m-c%d" style="left: %dpx">\n'
    '        <div class="m-num" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="m-tit">%s</div>\n'
    '        <div class="m-sub">%s</div>\n'
    '        <div class="m-des">%s</div>\n'
    '      </div>\n' % (i + 1, 128 + i * 572, n, t, s, d) for i, (n, t, s, d) in enumerate(MODS))

ESC = [("100", "Decisión correcta"), ("80", "Peligro nuevo"), ("40", "Apoyo respetuoso")]
ESCUDOS = "".join(
    '      <div class="m-esc" id="m-e%d" style="left: %dpx">\n'
    '        <div class="m-esc-n">%s</div><div class="m-esc-t">%s</div>\n'
    '      </div>\n' % (i + 1, 128 + i * 358, n, t) for i, (n, t) in enumerate(ESC))

CUERPO = chrome("04", "RUTA DE APRENDIZAJE",
                "Tres módulos. Un criterio: <b style=\"color:#D4A62B\">calidad de la decisión.</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="m-riel" id="m-riel" data-layout-ignore></div>
""" + CARDS + """
    </div>
"""

TL = """      tl.fromTo("#m-riel", { scaleX: 0 }, { scaleX: 1, duration: 1.6, ease: "power2.out" }, 1.10);
"""
for _i, _t in enumerate([2.60, 11.10, 22.45]):
    TL += ('      tl.fromTo("#m-c%d", { opacity: 0, y: 46, scale: 0.95 },'
           ' { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power3.out" }, %.2f);\n' % (_i + 1, _t))



def escena():
    return envoltura("e04-ruta", DUR, CSS, CUERPO, TL, lamina=LAMINA)
