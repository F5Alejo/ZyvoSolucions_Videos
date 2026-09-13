# -*- coding: utf-8 -*-
"""Lámina 29 · Evaluación final 4/4. Identificar al menos cuatro peligros.

La escena es un **esquema en planta**, no una ilustración: la narración dice
explícitamente «la escena es esquemática, así que no busco una respuesta basada
en detalles que no aparecen». Vehículos y zonas son bloques rotulados y el cruce
peatonal es su cebra — ninguna figura humana dibujada (regla de marca §0.2).

Los cinco marcadores del esquema y la lista de la derecha comparten número: el
espectador no tiene que buscar a qué se refiere cada punto.
"""
import cronometro
from base import chrome, envoltura, PAUSA_HTML, pausa_tl

LAMINA = 29
DUR = cronometro.duracion(LAMINA)

CSS = """
    .p-escena { position: absolute; left: 120px; top: 312px; width: 1020px; height: 580px;
                border-radius: 10px; overflow: hidden; background: #0C1428;
                border: 1.5px solid rgba(174,188,214,0.22); opacity: 0; }
    .p-svg { position: absolute; inset: 0; }
    .p-marca { opacity: 0; }

    .p-cap { position: absolute; left: 1180px; top: 312px; font-size: 24px; font-weight: 900;
             letter-spacing: 0.16em; color: #D4A62B; opacity: 0; }
    .p-item { position: absolute; left: 1180px; width: 624px; height: 82px; border-radius: 8px;
              background: rgba(174,188,214,0.09); border-left: 5px solid #AC841D;
              opacity: 0; will-change: transform, opacity; }
    .p-i-n { position: absolute; left: 18px; top: 21px; width: 40px; height: 40px;
             border-radius: 20px; background: rgba(172,132,29,0.30); }
    .p-i-n span { position: absolute; left: 0; top: 8px; width: 40px; text-align: center;
                  font-size: 21px; font-weight: 900; color: #D4A62B; }
    .p-i-t { position: absolute; left: 72px; top: 14px; font-size: 25px; font-weight: 800;
             color: #FFFFFF; }
    .p-i-d { position: absolute; left: 72px; right: 18px; top: 46px; font-size: 21px;
             font-weight: 500; color: #AEBCD6; }

    .p-tarea { position: absolute; left: 1180px; top: 812px; width: 624px; font-size: 25px;
               font-weight: 700; line-height: 1.3; color: #00C8D4; opacity: 0; }
    .p-nota { position: absolute; left: 120px; top: 908px; width: 1240px; font-size: 23px;
              font-weight: 600; color: #AEBCD6; opacity: 0; }
"""

# El esquema: calzadas, dos vehículos pesados, la trayectoria de giro, la zona de
# baja visibilidad, el ciclista, la superficie mojada y la cebra.
ESCENA = """      <svg class="p-svg" viewBox="0 0 1020 580" aria-hidden="true">
        <rect x="380" y="0" width="300" height="580" fill="#1A2744" />
        <rect x="0" y="200" width="1020" height="250" fill="#1A2744" />
        <path d="M 530 0 V 190 M 530 460 V 580" stroke="#5E6E8C" stroke-width="4" stroke-dasharray="26 22" />
        <path d="M 0 325 H 370 M 690 325 H 1020" stroke="#5E6E8C" stroke-width="4" stroke-dasharray="26 22" />

        <!-- zona de baja visibilidad del camión -->
        <path id="p-ciego" class="p-marca" d="M 660 60 L 900 150 L 900 330 L 660 190 Z"
              fill="rgba(172,132,29,0.22)" stroke="#AC841D" stroke-width="2" stroke-dasharray="8 6" />
        <!-- trayectoria de giro -->
        <path id="p-giro" class="p-marca" d="M 600 190 C 600 300 720 325 900 325"
              fill="none" stroke="#D4A62B" stroke-width="5" stroke-dasharray="14 10" />
        <path id="p-punta" class="p-marca" d="M 880 310 L 912 325 L 880 340 Z" fill="#D4A62B" />

        <!-- camión -->
        <g id="p-camion" class="p-marca">
          <rect x="400" y="20" width="260" height="160" rx="8" fill="#33415F" stroke="#AEBCD6" stroke-width="2" />
          <text x="530" y="112" text-anchor="middle" font-family="Montserrat, sans-serif"
                font-size="30" font-weight="800" fill="#FFFFFF">CAMIÓN</text>
        </g>
        <!-- bus -->
        <g id="p-bus" class="p-marca">
          <rect x="40" y="236" width="250" height="130" rx="8" fill="#33415F" stroke="#AEBCD6" stroke-width="2" />
          <text x="165" y="312" text-anchor="middle" font-family="Montserrat, sans-serif"
                font-size="30" font-weight="800" fill="#FFFFFF">BUS</text>
        </g>
        <!-- ciclista, junto al borde y dentro de la zona ciega -->
        <g id="p-ciclista" class="p-marca">
          <circle cx="706" cy="212" r="30" fill="rgba(0,200,212,0.20)" stroke="#00C8D4" stroke-width="3" />
          <text x="706" y="223" text-anchor="middle" font-family="Montserrat, sans-serif"
                font-size="26" font-weight="900" fill="#7FE5EC">C</text>
        </g>
        <!-- superficie mojada -->
        <g id="p-mojado" class="p-marca">
          <rect x="740" y="352" width="220" height="86" rx="6" fill="rgba(0,200,212,0.14)"
                stroke="#00C8D4" stroke-width="2" stroke-dasharray="10 8" />
          <text x="850" y="403" text-anchor="middle" font-family="Montserrat, sans-serif"
                font-size="21" font-weight="800" fill="#7FE5EC">PINTURA MOJADA</text>
        </g>
        <!-- cruce peatonal -->
        <g id="p-cebra" class="p-marca">
          <rect x="396" y="486" width="26" height="70" fill="#DCE4F2" />
          <rect x="440" y="486" width="26" height="70" fill="#DCE4F2" />
          <rect x="484" y="486" width="26" height="70" fill="#DCE4F2" />
          <rect x="528" y="486" width="26" height="70" fill="#DCE4F2" />
          <rect x="572" y="486" width="26" height="70" fill="#DCE4F2" />
          <rect x="616" y="486" width="26" height="70" fill="#DCE4F2" />
        </g>
      </svg>
"""

PELIGROS = [("1", "Camión y su trayectoria de giro", "El remolque barre más de lo que parece."),
            ("2", "Ciclista en zona de baja visibilidad", "Sin ruta de escape hacia el borde."),
            ("3", "Bus en la vía transversal", "Segundo vehículo pesado en el cruce."),
            ("4", "Superficie con pintura mojada", "Menos adherencia justo en la curva."),
            ("5", "Cruce peatonal activo", "El andén no es la salida.")]
PP = "".join(
    '      <div class="p-item" id="p-l%d" style="top: %dpx">\n'
    '        <div class="p-i-n" data-layout-ignore><span>%s</span></div>\n'
    '        <div class="p-i-t">%s</div>\n'
    '        <div class="p-i-d">%s</div>\n'
    '      </div>\n' % (i + 1, 352 + i * 88, n, t, d) for i, (n, t, d) in enumerate(PELIGROS))

CUERPO = chrome("29", "EVALUACIÓN FINAL",
                "4/4 · Pregunta 9: <b style=\"color:#D4A62B\">identifica al menos cuatro peligros</b>") + """

    <div class="clip capa" data-start="0" data-duration="{d}" data-track-index="3">
      <div class="p-escena" id="p-escena" data-layout-ignore>
""" + ESCENA + """      </div>

      <div class="p-cap" id="p-cap">LO QUE LA ESCENA SÍ MUESTRA</div>
""" + PP + """
      <div class="p-tarea" id="p-tarea">Escribe un control aplicable para cada peligro, y cuándo suspenderías el recorrido.</div>
      <div class="p-nota" id="p-nota">Se aceptan otros peligros si son coherentes con la escena y no dependen de suposiciones inventadas.</div>
    </div>

""" + PAUSA_HTML

TL = """      /* 3.83 · «la escena es esquemática»: primero el plano vacío */
      tl.fromTo("#p-escena", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, 3.93);
      tl.fromTo("#p-cap", { opacity: 0, x: 24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 9.60);

      /* 10.45 · los elementos, cada uno con su punto en la lista */
      tl.fromTo("#p-camion", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 10.55);
      tl.fromTo("#p-giro", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 11.60);
      tl.fromTo("#p-punta", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 12.10);
      tl.fromTo("#p-l1", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 10.75);

      tl.fromTo("#p-ciclista", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 14.60);
      tl.fromTo("#p-ciego", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 15.60);
      tl.fromTo("#p-l2", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 14.80);

      tl.fromTo("#p-bus", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 18.40);
      tl.fromTo("#p-l3", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 18.60);

      tl.fromTo("#p-mojado", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 20.80);
      tl.fromTo("#p-l4", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 21.00);

      /* 23.72 · la intersección activa y la ruta de escape */
      tl.fromTo("#p-cebra", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 23.82);
      tl.fromTo("#p-l5", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 24.02);

      /* 36.34 · «identifica al menos cuatro peligros y un control para cada uno» */
      tl.fromTo("#p-tarea", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 36.44);

      /* 46.25 · «acepto otros peligros si son coherentes con la escena» */
      tl.fromTo("#p-nota", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 46.35);

""" + pausa_tl(35.05)


def escena():
    return envoltura("e29-peligros", DUR, CSS, CUERPO, TL, lamina=LAMINA)
