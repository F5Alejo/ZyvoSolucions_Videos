---
format: 1920x1080
duration: 68s
arc: BAB — antes (papel) → adelanto del después → puente/producto → módulo a módulo → wow → cierre de marca
music: none
---

## Video direction

**Paleta (de `frame.md`, nada inventado).** Suelo `bg #051427` en todos los planos, siempre con la
retícula `grid` por debajo del 15%. Los paneles del centro de mando son `surface` / `surface-2` con
contorno `border` de 1.5px y **cero sombra**. El rojo `primary` es el único acento de foco: una cifra,
una palabra o un elemento por plano, nunca dos. El lavanda `accent-2` es exclusivo del cromo
estructural — retícula, hairlines, marcas de esquina, etiquetas de telemetría — y jamás compite con el
rojo. Texto en la escalera `text` → `text-muted` → `text-light`. Tipografía por rol: display para
titulares y cifras, body para apoyo, chrome en mayúsculas con tracking para las etiquetas del HUD.

**Gramática de movimiento y modelo de revelado.** Curvas de cola larga, `power3` por defecto; nada
rebota. **Este video no tiene locución**, así que el reloj del revelado son los *cues de texto en
pantalla*: cada plano entra con una sola pieza y las demás llegan cuando su cue aparece, repartidas
sobre todo el plano y sobre todo en su segunda mitad. Ningún plano vuelca su lienzo en el primer 25%.
Cámara: un solo empuje o recorrido motivado por plano, nunca un segundo empuje en la mitad final.
Durante una sostenida sólo se permite jitter de baja amplitud (`sine-wave-loop` en registro bajo) o
internos de SVG vivos; nada de respirar.

**Ritmo y sostenidas.** El video alterna densidad y calma a propósito: los planos 02, 06 y 07 son los
densos; el **plano 03 sostiene** tras el clímax de partículas, el **plano 05 sostiene** sobre el carnet
ya revelado, y el **plano 09 sostiene** el lockup hasta el final. Esa alternancia es lo que impide que
la pieza lea como un desfile uniforme.

**Continuidad del HUD.** La retícula y las cuatro marcas de esquina lavanda nacen en el plano 03 y
persisten hasta el 08; en el 09 se retiran con los paneles. Es el hilo que convierte nueve planos en
un solo centro de mando.

**Lista negativa.** Nunca: barras de navegación, pies de página, scrollbars, cromo de navegador,
cursores reales, degradados morados de "IA", bokeh flotante, formas decorativas genéricas sustituyendo
un asset real, sombras difusas (aquí se eleva con contorno y contraste, no con sombra). Nunca los dos
modos de fallo de movimiento: **diapositiva** (volcar todo y congelar) y **salvapantallas** (todo
flotando por su cuenta). Nunca rebote (`back.out` / `elastic.out`) como entrada por defecto. El 17%
inferior del cuadro queda libre en todos los planos.

## Frame 1 — El papel manda

- duration: 7s
- transition_in: cut
- status: outline
- src: compositions/frames/01-el-papel-manda.html
- type: hook
- persuasion: Pain validation
- beat: frustración
- blueprint: kinetic-type-beats
- blueprint: kinetic-type-beats (Adapt)
- focal: (tipografía pura — sin asset)
- roles: —
- sfx: impact-soft

<fill in: this video's content for the "El papel manda" beat — keep the layout role, replace the words.>

## Frame 2 — Sepultado en formatos

- duration: 8s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-sepultado-en-formatos.html
- type: pain_point
- persuasion: Pain agitation
- beat: agobio
- blueprint: overwhelm-surround
- blueprint: overwhelm-surround (Adapt)
- focal: assets/seguridad_vial_icono_formatos.webp
- roles: seguridad_vial_icono_formatos = cutout · seguridad_vial_icono_inspecciones = supporting · control_personal_icono_registro_manual = supporting · capacitaciones_icono_evaluacion_final = supporting
- sfx: riser, paper-rustle

<fill in: this video's content for the "Sepultado en formatos" beat — keep the layout role, replace the words.>

## Frame 3 — Se enciende el centro de mando

- duration: 7s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/03-centro-de-mando.html
- type: product_intro
- persuasion: Negative contrast
- beat: alivio + control
- blueprint: logo-assemble-lockup
- blueprint: logo-assemble-lockup (Adapt)
- focal: assets/riskmann_icono_blanco.png
- roles: riskmann_icono_blanco = cutout · riskmann_logo_central_blanco.svg = supporting
- sfx: whoosh-impact, power-up

<fill in: this video's content for the "Se enciende el centro de mando" beat — keep the layout role, replace the words.>

## Frame 4 — Cuatro tableros, un mando

- duration: 8s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-cuatro-tableros.html
- type: feature_showcase
- persuasion: Value stacking
- beat: claridad
- blueprint: grid-card-assemble
- blueprint: grid-card-assemble (Reproduce)
- focal: assets/inicio_icono_seguridad_vial.webp
- roles: inicio_icono_empresas = supporting · inicio_icono_control_personal = supporting · inicio_icono_capacitaciones = supporting · inicio_icono_seguridad_vial = cutout
- sfx: click-soft

<fill in: this video's content for the "Cuatro tableros, un mando" beat — keep the layout role, replace the words.>

## Frame 5 — La gente entra con su cara

- duration: 7s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/05-control-de-personal.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: confianza
- blueprint: device-surface-showcase
- blueprint: device-surface-showcase (Adapt)
- focal: assets/screenshot1.png
- roles: screenshot1 = cutout · control_personal_icono_lector_qr = supporting · control_personal_icono_historial_diario = supporting · control_personal_icono_ausentismo_laboral = supporting
- sfx: scan-beep, click-soft

<fill in: this video's content for the "La gente entra con su cara" beat — keep the layout role, replace the words.>

## Frame 6 — El dato ya está vivo

- duration: 8s
- transition_in: crossfade
- status: outline
- src: compositions/frames/06-dato-vivo.html
- type: benefit_highlight
- persuasion: Show-don't-tell proof
- beat: asombro
- blueprint: video-text-pivot
- blueprint: video-text-pivot (Adapt)
- focal: assets/graficas.mp4
- roles: graficas.mp4 = cutout · estadisticas.mp4 = supporting · lista.mp4 = supporting
- sfx: riser, impact-soft

<fill in: this video's content for the "El dato ya está vivo" beat — keep the layout role, replace the words.>

## Frame 7 — PESV, estación por estación

- duration: 8s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/07-pesv-estaciones.html
- type: feature_showcase
- persuasion: Rule of three (extendida a siete)
- beat: control
- blueprint: spatial-pan-stations
- blueprint: spatial-pan-stations (Reproduce)
- focal: assets/seguridad_vial_icono_siniestralidad_vial.webp
- roles: seguridad_vial_icono_conductores = supporting · seguridad_vial_icono_vehiculos = supporting · seguridad_vial_icono_inspecciones = supporting · seguridad_vial_icono_mantenimientos = supporting · seguridad_vial_icono_siniestralidad_vial = cutout · seguridad_vial_icono_formatos = supporting · seguridad_vial_icono_infografias = supporting
- sfx: whoosh

<fill in: this video's content for the "PESV, estación por estación" beat — keep the layout role, replace the words.>

## Frame 8 — Lo que cambia

- duration: 7s
- transition_in: crossfade
- status: outline
- src: compositions/frames/08-lo-que-cambia.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: inevitabilidad
- blueprint: kinetic-type-beats
- blueprint: kinetic-type-beats (Reproduce)
- focal: (tipografía pura — sin asset)
- roles: —
- sfx: beat-tick

<fill in: this video's content for the "Lo que cambia" beat — keep the layout role, replace the words.>

## Frame 9 — RiskMann

- duration: 8s
- transition_in: crossfade
- status: outline
- src: compositions/frames/09-cierre-riskmann.html
- type: branding
- persuasion: Authority by association
- beat: confianza
- blueprint: logo-assemble-lockup
- blueprint: logo-assemble-lockup (Reproduce)
- focal: assets/riskmann_logo_central_blanco.svg
- roles: riskmann_logo_central_blanco.svg = cutout · riskmann_icono_blanco = supporting
- sfx: whoosh-out, chime-soft

<fill in: this video's content for the "RiskMann" beat — keep the layout role, replace the words.>
