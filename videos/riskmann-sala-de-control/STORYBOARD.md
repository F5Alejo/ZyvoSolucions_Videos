---
format: 1920x1080
duration: 68s
message: "RiskMann convierte el papeleo del SG-SST y del PESV en un centro de control automatizado"
arc: BAB — antes (papel) → adelanto del después → puente/producto → módulo a módulo → wow → cierre de marca
audience: "Empresas colombianas con obligación PESV y SG-SST; gerencia y responsables de HSEQ"
mode: autonomous
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

- scene: Palabras de papeleo se apilan en el centro y una sola línea las tacha
- voiceover: ""
- duration: 7s
- transition_in: cut
- status: animated
- src: compositions/frames/01-el-papel-manda.html
- type: hook
- persuasion: Pain validation
- beat: frustración
- blueprint: kinetic-type-beats
- asset_candidates:
- blueprint: kinetic-type-beats (Adapt)
- focal: (tipografía pura — sin asset)
- roles: —
- sfx: impact-soft

Adapt: se conserva el motor de la sub-forma A (la línea fija con un hueco que cambia por corte seco);
lo que cambia es que el hueco no lleva la broma sino el trámite, y la resolución no es un signo de
puntuación sino una línea roja que tacha la frase entera.
Scene 1 (0.0–1.6s): campo `bg` sólido, retícula aún apagada. La línea fija «Este mes toca **actualizar
la matriz**.» entra con **revelado escalonado por palabra** (`revelado secuenciado por guion — receta en RULES_DIR`) y asiento de
cola larga; el hueco variable va en `primary`. Centrado, la línea ocupa ~62% del ancho, tres capas de
profundidad (retícula tenue · línea · viñeta de borde). Cámara quieta.
Scene 2 (1.6–4.4s): sólo el hueco cambia, por **corte duro en el sitio** (`discrete-text-sequence`),
un trámite por beat, ~0.7s cada uno: «actualizar la matriz» → «pasar la lista» → «firmar la inspección»
→ «archivar el certificado». El resto de la línea no se mueve ni un píxel: la inmovilidad es el chiste.
Scene 3 (4.4–5.8s): el hueco se detiene en «**volver a empezar**» y una **línea de tachado se dibuja de
izquierda a derecha** (`css-marker-patterns`, modo strike) sobre toda la frase, en `primary`.
Scene 4 (5.8–7.0s): sostiene quieto sobre la frase tachada; sólo un **jitter de baja amplitud**
(`jitter senoidal de baja amplitud — receta en RULES_DIR`, registro bajo) mantiene el cuadro vivo. Sin cámara.

narrativeRole: Valida en 3 segundos el dolor real del cliente antes de nombrar nada. La palabra que
gira en el mismo hueco es la broma: cambia el trámite, nunca cambia el método.
keyMessage: Cumplir hoy significa perseguir papeles.

## Frame 2 — Sepultado en formatos

- scene: Formatos, planillas y carpetas se acumulan desde los bordes hasta cerrar sobre el centro
- voiceover: ""
- duration: 8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-sepultado-en-formatos.html
- type: pain_point
- persuasion: Pain agitation
- beat: agobio
- blueprint: overwhelm-surround
- asset_candidates: assets/seguridad_vial_icono_formatos.webp — icono de formatos; assets/seguridad_vial_icono_inspecciones.webp — icono de inspecciones; assets/control_personal_icono_registro_manual.webp — icono de registro manual; assets/capacitaciones_icono_evaluacion_final.webp — icono de evaluación
- blueprint: overwhelm-surround (Adapt)
- focal: assets/seguridad_vial_icono_formatos.webp
- roles: seguridad_vial_icono_formatos = cutout · seguridad_vial_icono_inspecciones = supporting · control_personal_icono_registro_manual = supporting · capacitaciones_icono_evaluacion_final = supporting
- sfx: riser, paper-rustle

Adapt: se conserva el movimiento firma — el **cierre radial desde los cuatro lados con el centro
quieto** — y también la morfosis del centro, pero el centro no se convierte en un avatar sino en la
**silueta de una persona hecha de las mismas fichas de papel**: el sujeto sepultado es el responsable
de HSEQ. Se cambia el inventario de apps por fichas de trámite reales de la plataforma.
Scene 1 (0.0–1.8s): el icono de formatos entra grande y solo, centrado, ~40% del cuadro
(`spring-pop-entrance` en su registro suave, asiento de cola larga). Tres capas: viñeta · icono · una
etiqueta chrome «FORMATOS» que aparece bajo él.
Scene 2 (1.8–3.6s): los otros tres iconos llegan **escalonados desde fuera de cuadro**
(`center-outward-expansion` en su forma inversa: entran hacia el centro) y se colocan a media
distancia; cada uno arrastra su etiqueta. La composición pasa de héroe centrado a racimo asimétrico
60/40. El foco `primary` sigue en el icono central; los que llegan quedan en `desenfoque selectivo — receta en RULES_DIR` suave.
Scene 3 (3.6–5.4s): **el centro se transforma** (movimiento firma) — el icono de formatos se disuelve y
debajo aparece la silueta de una persona compuesta por fichas de papel apiladas (`card-morph-anchor`
para el cambio de contenedor + `depth-scatter-assemble` para las fichas).
Scene 4 (5.4–8.0s): decenas de fichas de trámite **cierran desde los cuatro bordes**
(`center-outward-expansion`, entrada radial escalonada, stagger tope ~0.5s) hasta rodear a la silueta,
que **no se mueve**: la claustrofobia viene de estar rodeado, nunca de un empuje de cámara. Densidad
alta, cinco capas. Sostiene el estado agobiado sin más movimiento.

narrativeRole: Sube la presión hasta lo claustrofóbico: no es un trámite, son decenas a la vez, y
todos caen sobre la misma persona. Es el "antes" del arco BAB.
keyMessage: No es un formato, es un sistema entero disperso.

## Frame 3 — Se enciende el centro de mando

- scene: El montón colapsa en partículas que se reordenan y arman el isotipo de RiskMann; la retícula del HUD enciende
- voiceover: ""
- duration: 7s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-centro-de-mando.html
- type: product_intro
- persuasion: Negative contrast
- beat: alivio + control
- blueprint: logo-assemble-lockup
- asset_candidates: assets/riskmann_icono_blanco.png — isotipo RiskMann en blanco; assets/riskmann_logo_central_blanco.svg — logotipo vectorial blanco
- blueprint: logo-assemble-lockup (Adapt)
- focal: assets/riskmann_icono_blanco.png
- roles: riskmann_icono_blanco = cutout · riskmann_logo_central_blanco.svg = supporting
- sfx: whoosh-impact, power-up

Adapt: se conserva el movimiento firma — la marca **llega a existir** ensamblándose de partes en un
escenario despejado. Lo que cambia es la materia prima: las partes no son formas abstractas, son las
mismas fichas de papel del plano anterior, así que el giro del video ocurre sin corte de material.
Scene 1 (0.0–1.4s): las fichas que rodeaban la silueta **se rompen en un enjambre 3D**
(`depth-scatter-assemble`) y giran hacia el centro; **estela de desenfoque de movimiento**
(`estela de velocidad — receta en RULES_DIR`) en el pico de velocidad. Composición centrada, cuatro capas de profundidad.
Scene 2 (1.4–2.8s): el enjambre **se aplana y se resuelve** en el isotipo de RiskMann en el centro
(`depth-scatter-assemble` en su fase de reensamblaje), y el trazo del isotipo **se dibuja solo**
(`svg-path-draw`) en el último tercio del movimiento. Aquí aterriza el foco `primary` del plano.
Scene 3 (2.8–4.4s): **enciende el HUD** — la retícula `grid` se dibuja de dentro hacia fuera y las
cuatro marcas de esquina lavanda entran una tras otra (`svg-path-draw` + `expansión desde el centro — receta en RULES_DIR`).
El fondo pasa de plano a campo con halo (`halo ambiental — receta en RULES_DIR`, pico ≤0.45) detrás del isotipo.
Scene 4 (4.4–5.8s): el logotipo completo se despliega a la derecha del isotipo con **cascada por
letra** (`waterfall-entry`) y bajo él entra la etiqueta chrome «CENTRO DE CONTROL · SG-SST · PESV»
con barrido de máscara.
Scene 5 (5.8–7.0s): **sostenida** deliberada. Todo quieto, sólo jitter de baja amplitud
(`jitter senoidal de baja amplitud — receta en RULES_DIR`) sobre el lockup. Es el respiro antes del recorrido de módulos.

narrativeRole: El giro del video. El mismo material del problema se convierte, sin corte, en la
marca. Aquí aterriza la promesa completa (beat 2 del arco de valor).
keyMessage: RiskMann es el centro de control de todo eso.

## Frame 4 — Cuatro tableros, un mando

- scene: Cuatro paneles del centro de mando entran escalonados con los iconos de los módulos
- voiceover: ""
- duration: 8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-cuatro-tableros.html
- type: feature_showcase
- persuasion: Value stacking
- beat: claridad
- blueprint: grid-card-assemble
- asset_candidates: assets/inicio_icono_empresas.webp — icono de espacios de trabajo; assets/inicio_icono_control_personal.webp — icono de control de personal; assets/inicio_icono_capacitaciones.webp — icono de campus; assets/inicio_icono_seguridad_vial.webp — icono de seguridad vial
- blueprint: grid-card-assemble (Reproduce)
- focal: assets/inicio_icono_seguridad_vial.webp
- roles: inicio_icono_empresas = supporting · inicio_icono_control_personal = supporting · inicio_icono_capacitaciones = supporting · inicio_icono_seguridad_vial = cutout
- sfx: click-soft

Scene 1 (0.0–1.4s): sobre el HUD ya encendido, el titular «Cuatro tableros. Un solo mando.» se **rellena
línea a línea** (`revelado secuenciado por guion — receta en RULES_DIR`) en el tercio superior — la zona dorada. Debajo queda
establecida, vacía, la región de cuadrícula 2×2 con sus contornos lavanda apenas visibles. Cámara fija.
Scene 2 (1.4–4.6s): los cuatro paneles **se ensamblan en cascada escalonada** (`center-outward-expansion`
en su forma de deslizamiento corto directo al hueco, ~0.8s por panel, sin rebote): Espacios de trabajo,
Control de personal, Campus, Seguridad vial. Cada panel llega con su icono ya dentro y su etiqueta se
revela con **barrido de máscara** un beat después del panel. Cuadrícula 2×2, densidad media, cuatro capas.
Scene 3 (4.6–6.4s): bajo cada etiqueta aparecen dos o tres píldoras de submódulo, **escalonadas por
índice** (`center-outward-expansion`), y un **barrido de brillo lavanda recorre la cuadrícula**
(`ambient-glow-bloom`, forma de destello viajero) de arriba-izquierda a abajo-derecha.
Scene 4 (6.4–8.0s): el panel de Seguridad vial **sube al frente** — escala ligera y **halo rojo**
(`ambient-glow-bloom`) mientras los otros tres se **desenfocan** (`depth-of-field-blur`). Ese foco es
el gancho que engancha con los planos siguientes. Sostiene.

narrativeRole: Muestra la amplitud de un golpe: cuatro módulos, un solo tablero. Es el mapa que el
resto del video recorre.
keyMessage: Empresas, personal, campus y seguridad vial en un mismo mando.

## Frame 5 — La gente entra con su cara

- scene: El móvil con el carnet digital QR se sostiene como héroe mientras las funciones de control de personal se enganchan a su alrededor
- voiceover: ""
- duration: 7s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-control-de-personal.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: confianza
- blueprint: device-surface-showcase
- asset_candidates: assets/screenshot1.png — móvil con carnet digital, foto, cargo y QR; assets/control_personal_icono_lector_qr.webp — lector QR; assets/control_personal_icono_historial_diario.webp — historial diario; assets/control_personal_icono_ausentismo_laboral.webp — ausentismo laboral
- blueprint: device-surface-showcase (Adapt)
- focal: assets/screenshot1.png
- roles: screenshot1 = cutout · control_personal_icono_lector_qr = supporting · control_personal_icono_historial_diario = supporting · control_personal_icono_ausentismo_laboral = supporting
- sfx: scan-beep, click-soft

Adapt: se conserva el movimiento firma — la **superficie real sostenida como héroe mientras su flujo
avanza** — pero sin cursor y sin ciclo de pantallas: la captura del carnet es única, así que el flujo lo
llevan los enganches que se acoplan a su alrededor y el destello de escaneo sobre el QR.
Scene 1 (0.0–1.5s): el móvil con el carnet entra desde el borde derecho y **se asienta** en el tercio
derecho del cuadro, ocupando ~55% de la altura (`nudge-curve`, lento-rápido-lento). Composición
asimétrica 60/40, tres capas: retícula · panel `surface` de fondo · dispositivo.
Scene 2 (1.5–3.2s): a la izquierda, el titular «La gente entra con su cara, no con una firma.» se
revela **por palabra** (`revelado secuenciado por guion — receta en RULES_DIR`). Nada más aparece todavía.
Scene 3 (3.2–5.0s): un **destello de escaneo recorre el QR** de arriba abajo (`halo ambiental — receta en RULES_DIR`,
forma de barrido) y sobre él se dibuja un **marco de detección de esquinas** (`ai-tracking-box`,
recoloreado a `primary`, sin porcentaje inventado: la etiqueta dice «REGISTRO OK»). Es el foco rojo
del plano.
Scene 4 (5.0–6.2s): tres píldoras de submódulo — lector QR, historial diario, ausentismo — **se enganchan
al dispositivo** una por una con una línea fina lavanda que las ata al borde del móvil
(`center-outward-expansion` + `svg-path-draw` para las líneas).
Scene 5 (6.2–7.0s): **sostenida**. Todo quieto; sólo los internos del icono del lector QR siguen vivos
(`svg-icon-enrichment`).

narrativeRole: Primer módulo con producto real en pantalla. La captura auténtica del carnet hace la
prueba que ningún texto haría.
keyMessage: Cada ingreso queda registrado con un escaneo.

## Frame 6 — El dato ya está vivo

- scene: Las pantallas del HUD se llenan con el video real de la plataforma y luego ceden el cuadro a una línea de impacto
- voiceover: ""
- duration: 8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-dato-vivo.html
- type: benefit_highlight
- persuasion: Show-don't-tell proof
- beat: asombro
- blueprint: video-text-pivot
- asset_candidates: assets/estadisticas.mp4 — [video] pantalla de estadísticas en movimiento; assets/graficas.mp4 — [video] gráficas animándose; assets/lista.mp4 — [video] listado de registros desplazándose
- blueprint: video-text-pivot (Adapt)
- focal: assets/graficas.mp4
- roles: graficas.mp4 = cutout · estadisticas.mp4 = supporting · lista.mp4 = supporting
- sfx: riser, impact-soft

Adapt: se conserva el movimiento firma — **el video cede su peso a la cifra en el mismo anclaje, como un
solo suceso** — pero se abre a tres superficies en vez de una, porque el argumento aquí es que la
plataforma opera en varios frentes a la vez. El pivote lo hace la pantalla central; las laterales se
atenúan un beat antes para que la transferencia de peso se lea limpia.
Scene 1 (0.0–1.8s): la pantalla central del HUD entra y `graficas.mp4` **arranca dentro de ella**;
marco `surface` con contorno, ~48% del cuadro, centrado. Empuje lento de cámara por debajo
(`multi-phase-camera`, una sola fase). Las dos pantallas laterales existen apagadas, en oscuro.
Scene 2 (1.8–3.6s): **se encienden las laterales** con un beat de diferencia — `estadisticas.mp4` a la
izquierda, `lista.mp4` a la derecha, ambas inclinadas hacia el centro (`split-tilt-cards`, sin flotación
continua) y ligeramente desenfocadas (`depth-of-field-blur`) para que la central mande. Triple panel,
cinco capas. Aquí está el pico de densidad del video.
Scene 3 (3.6–5.4s): las laterales se **atenúan** y la central **se desliza y encoge hacia la izquierda,
entregando el hueco** (movimiento firma) a la cifra que aparece ocupando el centro: un contador
**cuya escala crece con el valor** (`counting-dynamic-scale`) que sube hasta «100%» sobre la etiqueta
chrome «TRAZABILIDAD DEL REGISTRO». Una transferencia de peso, no dos sucesos.
Scene 4 (5.4–8.0s): la línea «El informe no se arma. Ya se está armando.» **entra por palabra**
(`revelado secuenciado por guion — receta en RULES_DIR`) bajo la cifra, con «**se está armando**» en `primary` y un
**resplandor de palabra clave** (`resplandor de palabra clave — receta en RULES_DIR`, disparado por tiempo, no por audio) que aterriza
sobre ella. Sostiene quieto.

narrativeRole: El pico visual del video. Tres superficies reales moviéndose a la vez prueban que la
plataforma existe y opera, no que se promete.
keyMessage: El informe no se arma: ya se está armando solo.

## Frame 7 — PESV, estación por estación

- scene: Una cámara recorre lateralmente siete estaciones del módulo de seguridad vial
- voiceover: ""
- duration: 8s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/07-pesv-estaciones.html
- type: feature_showcase
- persuasion: Rule of three (extendida a siete)
- beat: control
- blueprint: spatial-pan-stations
- asset_candidates: assets/seguridad_vial_icono_conductores.webp — conductores; assets/seguridad_vial_icono_vehiculos.webp — vehículos; assets/seguridad_vial_icono_inspecciones.webp — inspecciones; assets/seguridad_vial_icono_mantenimientos.webp — mantenimientos; assets/seguridad_vial_icono_siniestralidad_vial.webp — siniestralidad vial; assets/seguridad_vial_icono_formatos.webp — formatos; assets/seguridad_vial_icono_infografias.webp — infografías
- blueprint: spatial-pan-stations (Reproduce)
- focal: assets/seguridad_vial_icono_siniestralidad_vial.webp
- roles: seguridad_vial_icono_conductores = supporting · seguridad_vial_icono_vehiculos = supporting · seguridad_vial_icono_inspecciones = supporting · seguridad_vial_icono_mantenimientos = supporting · seguridad_vial_icono_siniestralidad_vial = cutout · seguridad_vial_icono_formatos = supporting · seguridad_vial_icono_infografias = supporting
- sfx: whoosh

Scene 1 (0.0–1.6s): la cámara abre encuadrando la primera estación de un lienzo sobredimensionado
(`viewport-change`, modo PAN sobre un único envoltorio `.world`): «CONDUCTORES», icono a la izquierda y
su llamada a la derecha, que **aparece con pop de resorte suave** un beat después de que la estación
se centra. Franja de ancho completo, tres capas con paralaje.
Scene 2 (1.6–3.4s): **paneo lateral** a «VEHÍCULOS» y luego a «INSPECCIONES» — dos estaciones en un solo
movimiento continuo con desaceleración en cada una; cada llamada se revela sólo al quedar centrada.
Scene 3 (3.4–5.4s): sigue el paneo por «MANTENIMIENTOS», «FORMATOS» e «INFOGRAFÍAS», más rápido y con
**estela de desenfoque** (`motion-blur-streak`) entre estaciones; las llamadas ahora son de una palabra.
La aceleración es el argumento: son muchas, y todas están.
Scene 4 (5.4–8.0s): la cámara **frena en seco sobre «SINIESTRALIDAD VIAL»**, la estación final, que queda
centrada y ocupando ~45% del cuadro con **halo rojo** (`halo ambiental — receta en RULES_DIR`). Debajo se dibuja la línea
«El PESV completo. No una parte.» (`css-marker-patterns`, subrayado dibujado). Sostiene sin cámara.

narrativeRole: El módulo diferenciador. El recorrido lateral convierte una lista de siete en un
territorio que se atraviesa, y aterriza en el que más pesa: siniestralidad.
keyMessage: El PESV completo, no una parte.

## Frame 8 — Lo que cambia

- scene: Cuatro frases de valor entran y se limpian a alta cadencia sobre el fondo del HUD
- voiceover: ""
- duration: 7s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-lo-que-cambia.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: inevitabilidad
- blueprint: kinetic-type-beats
- asset_candidates:
- blueprint: kinetic-type-beats (Reproduce)
- focal: (tipografía pura — sin asset)
- roles: —
- sfx: beat-tick

Scene 1 (0.0–1.4s): sobre el HUD, la primera frase de valor **entra con corte duro**, sola y enorme,
centrada, ocupando ~70% del ancho: «**UN SOLO LUGAR**». Sub-forma B: cada beat es una pantalla completa
con su propia entrada. Tres capas: retícula · frase · viñeta.
Scene 2 (1.4–2.6s): corte a «**TODO TRAZABLE**» — entrada por **colapso de interletraje**
(`kinetic-beat-slam`), nada del beat anterior permanece.
Scene 3 (2.6–3.8s): corte a «**AUDITABLE EN MINUTOS**» — entrada por **deslizamiento enmascarado desde
abajo**; la palabra «MINUTOS» en `primary`.
Scene 4 (3.8–5.0s): corte a «**EN TIEMPO REAL**» — entrada con **estela de desenfoque** que resuelve
nítida en el centro (`estela de velocidad — receta en RULES_DIR`).
Scene 5 (5.0–7.0s): los cuatro fragmentos **regresan a la vez, pequeños, a las cuatro esquinas del HUD**
(`center-outward-expansion`) y en el centro queda la línea «Eso es un centro de control.» revelada por
palabra. Sostiene quieto hasta el final.

narrativeRole: Traduce todo lo mostrado a lo que el gerente compra: trazabilidad, tiempo y
tranquilidad frente a una auditoría.
keyMessage: Un solo lugar, auditable y en tiempo real.

## Frame 9 — RiskMann

- scene: Los paneles se retiran por los cuatro bordes y el logotipo se dibuja solo en el centro
- voiceover: ""
- duration: 8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-cierre-riskmann.html
- type: branding
- persuasion: Authority by association
- beat: confianza
- blueprint: logo-assemble-lockup
- asset_candidates: assets/riskmann_logo_central_blanco.svg — logotipo vectorial blanco; assets/riskmann_icono_blanco.png — isotipo blanco
- blueprint: logo-assemble-lockup (Reproduce)
- focal: assets/riskmann_logo_central_blanco.svg
- roles: riskmann_logo_central_blanco.svg = cutout · riskmann_icono_blanco = supporting
- sfx: whoosh-out, chime-soft

Scene 1 (0.0–1.6s): los paneles y las píldoras que quedaban en cuadro **se dispersan por los cuatro
bordes** (`expansión desde el centro — receta en RULES_DIR`, salida escalonada por índice) y la retícula se apaga de fuera
hacia dentro. El escenario queda limpio: es el movimiento de despeje que pide el blueprint.
Scene 2 (1.6–3.4s): el isotipo **florece desde cero** en el centro (`spring-pop-entrance`, asiento de
cola larga sin sobreimpulso) y su contorno **se dibuja solo** (`svg-path-draw`); halo rojo contenido
detrás (`halo ambiental — receta en RULES_DIR`).
Scene 3 (3.4–5.0s): el logotipo se completa a su derecha con **cascada por letra** (`waterfall-entry`)
hasta cerrar el lockup «RiskMann». Composición centrada, ~40% del ancho, tres capas.
Scene 4 (5.0–6.4s): bajo el lockup entra la firma «by SOFU» con **barrido de izquierda a derecha**
(`marcador dibujado en CSS — receta en RULES_DIR`) y, un beat después, la línea de cierre «Gestión de riesgo laboral y seguridad
vial» en `text-muted`.
Scene 5 (6.4–8.0s): **sostenida final**, la más larga del video. Todo quieto; sólo un jitter de baja
amplitud (`jitter senoidal de baja amplitud — receta en RULES_DIR`) sobre el lockup. Éste es el único plano con salida propia: al final el halo
se cierra y el cuadro descansa.

narrativeRole: Cierra el arco: el centro de mando se despeja y queda solo la marca. La firma
"by SOFU" da respaldo institucional.
keyMessage: RiskMann by SOFU.
