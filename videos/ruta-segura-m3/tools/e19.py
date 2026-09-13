# -*- coding: utf-8 -*-
"""Lámina 19 · Apertura del módulo 3. Ver, ser visto y confirmar."""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 19
DUR = cronometro.duracion(LAMINA)

CSS = """
    /* el camión del propio PPTX: es literalmente el tema del módulo */
    .v-foto { position: absolute; left: 50%; top: 50%; width: 2016px; height: 1344px;
              margin-left: -1008px; margin-top: -672px; opacity: 0.20; }
    .v-velo { position: absolute; inset: 0;
              background: radial-gradient(1500px 900px at 50% 42%, rgba(16,27,51,0.74) 0%, rgba(16,27,51,0.96) 78%); }

    .v-cap { position: absolute; left: 128px; top: 300px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .v-idea { position: absolute; top: 340px; height: 64px; padding: 0 28px; display: flex;
              align-items: center; border-radius: 32px; background: rgba(0,200,212,0.12);
              border: 1.5px solid #00C8D4; font-size: 27px; font-weight: 800; color: #7FE5EC;
              opacity: 0; white-space: nowrap; }

    .v-preg { position: absolute; left: 128px; top: 444px; width: 940px; font-size: 52px;
              font-weight: 900; line-height: 1.12; color: #FFFFFF; opacity: 0; }
    .v-no { position: absolute; left: 128px; top: 572px; font-size: 76px; font-weight: 900;
            line-height: 1; color: #D4A62B; opacity: 0; }
    .v-regla { position: absolute; left: 128px; top: 676px; width: 940px; padding: 18px 24px;
               border-radius: 8px; background: rgba(172,132,29,0.16); border-left: 6px solid #AC841D;
               font-size: 27px; font-weight: 700; line-height: 1.3; color: #FFFFFF; opacity: 0; }
    .v-obs { position: absolute; left: 128px; top: 806px; width: 940px; font-size: 25px;
             font-weight: 600; line-height: 1.32; color: #AEBCD6; opacity: 0; }
    .v-obs b { color: #7FE5EC; font-weight: 800; }

    .v-pcap { position: absolute; left: 1120px; top: 444px; font-size: 24px; font-weight: 900;
              letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .v-pesado { position: absolute; left: 1120px; width: 330px; height: 58px; padding: 0 20px;
                display: flex; align-items: center; border-radius: 8px;
                background: rgba(174,188,214,0.10); border-left: 5px solid #AEBCD6;
                font-size: 25px; font-weight: 700; color: #FFFFFF; opacity: 0; }
    .v-barre { position: absolute; left: 1120px; top: 680px; width: 676px; padding: 20px 24px;
               border-radius: 8px; background: rgba(0,200,212,0.10); border-left: 6px solid #00C8D4;
               font-size: 25px; font-weight: 600; line-height: 1.32; color: #DCE4F2; opacity: 0; }
    .v-barre b { color: #FFFFFF; font-weight: 800; }

    .v-escudo { position: absolute; right: 128px; top: 150px; width: 208px; height: 96px;
                border-radius: 10px; background: #AC841D; opacity: 0; }
    .v-escudo-n { position: absolute; left: 0; top: 10px; width: 208px; text-align: center;
                  font-size: 46px; font-weight: 900; color: #101B33; line-height: 1; }
    .v-escudo-t { position: absolute; left: 0; top: 64px; width: 208px; text-align: center;
                  font-size: 17px; font-weight: 800; letter-spacing: 0.1em; color: #101B33; }
"""

IDEAS = [("Ver", 128), ("Ser visto", 300), ("Confirmar que reaccionó", 540)]
II = "".join('      <div class="v-idea" id="v-i%d" style="left: %dpx">%s</div>\n'
             % (i + 1, x, t) for i, (t, x) in enumerate(IDEAS))

PESADOS = [("Buses", 0, 0), ("Camiones", 346, 0), ("Tractocamiones", 0, 66), ("Maquinaria", 346, 66)]
PZ = "".join('      <div class="v-pesado" id="v-v%d" style="left: %dpx; top: %dpx">%s</div>\n'
             % (i + 1, 1120 + dx, 486 + dy, t) for i, (t, dx, dy) in enumerate(PESADOS))

CUERPO = """    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="1">
      <img class="v-foto" id="v-foto" src="assets/fotos/camion.jpg"
           alt="Ciclista junto a un camión detenido en una intersección" data-layout-ignore />
      <div class="v-velo" data-layout-ignore></div>
    </div>

""" + chrome("19", "MÓDULO 3", "Misión segura: <b style=\"color:#D4A62B\">ruta, maniobra y respuesta</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="v-escudo" id="v-escudo">
        <div class="v-escudo-n">+80</div><div class="v-escudo-t">RETO RISKMANN</div>
      </div>

      <div class="v-cap" id="v-cap">TRES IDEAS QUE NO SON LA MISMA</div>
""" + II + """
      <div class="v-preg" id="v-preg">Si no ves al conductor, ¿puedes asumir que te ve?</div>
      <div class="v-no" id="v-no">NO.</div>
      <div class="v-regla" id="v-regla">No me ubico entre el vehículo y el borde en una intersección,
        aunque exista espacio disponible.</div>
      <div class="v-obs" id="v-obs">Mantengo distancia y observo <b>direccionales, ruedas, espejos y trayectoria</b>,
        conservando una ruta de escape.</div>

      <div class="v-pcap" id="v-pcap">SOBRE TODO CERCA DE</div>
""" + PZ + """      <div class="v-barre" id="v-barre">Al girar a la derecha, un vehículo pesado <b>barre un área mayor
        de la que parece</b> y cierra el espacio lateral.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 0.00 · «distingo tres ideas» / 3.70 · las tres */
      tl.fromTo("#v-cap", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.55);
      tl.fromTo("#v-i1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 3.80);
      tl.fromTo("#v-i2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 4.80);
      tl.fromTo("#v-i3", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 5.80);

      /* 7.94 · «si no veo al conductor, no asumo que me ve» */
      tl.fromTo("#v-preg", { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 8.05);
      tl.fromTo("#v-no", { opacity: 0, scale: 1.4, transformOrigin: "0% 50%" },
        { opacity: 1, scale: 1, duration: 0.45, ease: "power4.out" }, 10.60);

      /* 13.06 · los vehículos pesados */
      tl.fromTo("#v-pcap", { opacity: 0, x: 24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 13.15);
"""
for _i, _t in enumerate([14.30, 15.20, 16.10, 17.00]):
    TL += ('      tl.fromTo("#v-v%d", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, %.2f);\n'
           % (_i + 1, _t))

TL += """
      /* 19.34 · «barre un área mayor de la que parece» */
      tl.fromTo("#v-barre", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 19.45);

      /* 27.93 · «no me ubico entre el vehículo y el borde» */
      tl.fromTo("#v-regla", { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.55, ease: "power2.out" }, 28.05);

      /* 35.49 · lo que sí observo */
      tl.fromTo("#v-obs", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 35.60);

""" + pausa_tl(43.05)


def escena():
    return envoltura("e19-apertura", DUR, CSS, CUERPO, TL, lamina=LAMINA)
