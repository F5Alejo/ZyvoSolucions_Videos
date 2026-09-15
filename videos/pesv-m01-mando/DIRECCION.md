# Dirección de arte — PESV Módulo 01 · «Centro de mando»

> Aprobada por el cliente sobre la muestra `renders/muestra-apertura.mp4` (plano 01).
> Todo plano nuevo es hermano de `compositions/frames/01-apertura.html`: léelo antes de
> escribir una línea.

## Duraciones del módulo (151 s)

| Plano | Archivo | Inicio | Dura |
|---|---|---|---|
| 01 | `01-apertura` | 0 | 16 s — **hecho y aprobado** |
| 02 | `02-corresponsabilidad` | 16 | 20 s |
| 03 | `03-roles` | 36 | 20 s |
| 04 | `04-deberes` | 56 | 21 s — *recortado de 30 s: su voz dura 9.6 s y la cola quieta de 17 s se leía muerta* |
| 05 | `05-principio` | 77 | 16 s |
| 06 | `06-ruta` | 93 | 18 s |
| 07 | `07-retroalimentacion` | 111 | 28 s |
| 08 | `08-cierre` | 139 | 12 s |

## El cromo persistente — idéntico en los planos 02 a 07

Es el estado final del plano 01 (t = 16 s). Va en **una capa estática** presente desde t = 0,
sin animar. Es la continuidad del centro de mando: el espectador nunca sale de la sala.

- Suelo `#051427` a sangre, como capa `clip` propia (nunca en `#root`).
- Retícula: 60×60 px, líneas `rgba(142,143,196,0.14)`.
- Cuatro escuadras en L: 130×130, trazo 2 px `#8E8FC4`, opacidad **0.6**, en
  (56,56) · (1734,56) · (56,894) · (1734,894).
- Reglas laterales: x = 84 y x = 1820, de y 480 a y 840 (cópialas del plano 01).
- **Firma de marca**: `assets/marca/riskmann_logo_blanco.png` a **280 px de ancho**
  (escala 1/3), caja de imagen en **left 92.33 px, top 95 px** — así su tinta empieza en
  (104, 104). Quieta. Nada a menos de 44 px de ella.
- Bajo la firma: la regla roja y la etiqueta `CAPACITACIÓN PESV · MÓDULO 01 · ACTOR VIAL`
  exactamente como quedan en el plano 01 a t = 16 s (≈13 px, lavanda, tracking 0.18em).
- **Etiqueta de sección** arriba a la derecha, alineada con la firma: `NN · NOMBRE` en
  `#8E8FC4`, ~13 px, tracking 0.18em, alineada a la derecha en x = 1816, y ≈ 104. Es la
  única pieza de cromo que cambia de plano a plano.

El plano 08 es la excepción: es el cierre y la firma vuelve al centro.

## Paleta

`#051427` suelo · `#0C2B53` / `#0F396B` paneles · `#E6423C` rojo (**un solo foco por
plano**) · `#8E8FC4` lavanda (solo cromo estructural) · `#F2F7FF` texto · `#A7BCCC`
texto secundario. Tipografía Montserrat 700 con `@font-face` hacia
`assets/fonts/montserrat-latin.woff2` y `assets/fonts/montserrat-latin-ext.woff2`.

## Fotografía dentro del centro de mando

Las fotos de `assets/fotos/` no van a sangre como en el refactor: van **dentro de
monitores** — paneles `#0C2B53` con contorno 1.5 px `rgba(142,143,196,0.28)` y un marco
interior de 12–16 px — o a sangre **solo** cuando el plano lo pide explícitamente. Grado:
`filter: brightness(0.78) contrast(1.14) saturate(0.45) hue-rotate(-6deg)` más una capa
`#0C2B53` en `multiply` a ~0.40. La foto tiene que **leerse**: el primer intento de grado
del refactor la borró entera.

## Reglas de marca (manual RiskMann — no negociables)

Solo el archivo oficial. Nunca redibujar, trazar, re-letrar, recolorear, deformar, rotar ni
tapar el logo. Nada encima de él. Área de reserva libre alrededor. Movimiento permitido:
escala uniforme, opacidad, traslación y el recorte `clip-path` del archivo completo.

## Movimiento

Una línea de tiempo pausada por plano en `window.__timelines`. Entradas con `fromTo`.
Cero `Math.random`, `Date.now`, `repeat`, `yoyo`, transiciones o `@keyframes` CSS. Solo
transformaciones y pintura — **nunca** `letterSpacing`, `width`, `height`. Texto por
**máscara** (`overflow:hidden` + `yPercent`), no por fundido. Curvas `power3`, sin rebote.
Nada de figuras humanas. Todo el contenido por encima de y = 900.

**Las máscaras tienen que ser más anchas que su texto.** En el refactor, una máscara de
ancho fijo recortó la palabra «aumentar» del principio clave en silencio — cambió el sentido
de la frase y ni el `lint` ni el `check` lo vieron. Dimensiona cada máscara al texto real.

El sonido (cama, efectos y voz) se monta aparte en `index.html`: **no incluyas `<audio>`**.

---

## Los planos

### 02 · CORRESPONSABILIDAD (20 s)

Voz desde ~1.5 s: *«No manejar no significa ser un actor pasivo. La seguridad también viaja
en el asiento del pasajero.»*

Un **monitor grande** (~1180×660) a la derecha con `02-asiento-pasajero.jpg` — vista desde
el asiento del pasajero. Sobre el asiento vacío, un **recuadro de detección** (esquinas en L,
rojo `#E6423C`) que busca y se fija, con la etiqueta `ASIENTO DEL PASAJERO` y un pequeño
`ACTOR ACTIVO` que se descifra. A la izquierda, por máscara: «No manejar / no significa ser /
un actor pasivo.» a ~84 px; luego, más pequeño en `#A7BCCC`, «La seguridad también viaja en
el asiento del pasajero.»

### 03 · CADA ROL (20 s)

Voz desde ~1.5 s: *«Esto aplica a todos los colaboradores, sin importar su cargo. Y a cada
rol: peatón, ciclista, motociclista, conductor o pasajero.»*

`05-aerea-carriles.jpg` **a sangre** detrás del cromo, gradada. Encima, un sistema de
**seguimiento**: cinco retículas de detección (recuadros en L lavanda) que se fijan una a una
sobre puntos de la vía cuando la voz nombra cada rol, cada una con su etiqueta y un pequeño
identificador técnico (`ROL 01`…`ROL 05`). La de **PASAJERO** se vuelve roja al final y es la
única en rojo. Titular abajo a la izquierda: «Todos los colaboradores. / Sin importar el
cargo.» Las etiquetas no pueden tocarse entre sí: en el refactor CONDUCTOR y PASAJERO se
montaron.

### 04 · TRES DEBERES (21 s)

Voz desde ~1.5 s: *«Tres deberes. Exigir condiciones seguras, sin confrontar. Cumplir
cinturón, postura y protocolos. Advertir, solicitar corrección y reportar.»*

**Tres monitores** que se ensamblan en cascada (`06-camiones.jpg`, `03-cinturon.jpg`,
`04-cuadro-mandos.jpg` — este último, más claro: es casi negro). Luego cada uno **pasa al
frente por turno** —escala y el único halo rojo del plano— mientras los otros dos se
desenfocan, y su deber entra por máscara: `DEBER 01` «Exigir condiciones seguras» + «sin
confrontar» · `DEBER 02` «Cinturón, postura y protocolos» · `DEBER 03` «Advertir, solicitar
corrección y reportar». Al final, los tres monitores juntos, en calma.

### 05 · PRINCIPIO CLAVE (16 s)

Voz desde ~1.5 s: *«Cada decisión del pasajero puede aumentar o reducir la exposición al
riesgo.»*

Un **indicador analógico** grande, dibujado en SVG que se traza: un arco con el extremo
izquierdo marcado `REDUCE` y el derecho `AUMENTA`, y una aguja que oscila entre ambos al
ritmo de la frase y se asienta en el centro. **Sin cifras, sin porcentajes**: no hay dato que
lo respalde. La frase completa por máscara bajo el indicador — **completa, con «aumentar»**.

### 06 · LA RUTA (18 s)

Voz desde ~1.5 s: *«Es el primero de una ruta de ocho módulos para convertir intención en
conducta.»*

Recorrido lateral de cámara (un único envoltorio `.world`) por **ocho estaciones**: 01 Actor
vial · 02 Antes del viaje · 03 Ascenso y descenso · 04 Durante el viaje · 05 Pasajeros
vulnerables · 06 Acompañante en moto · 07 Emergencias PAS · 08 Taller y evaluación. La
estación 01 lleva `ESTÁS AQUÍ` y se enciende en rojo. El cromo persistente queda **fuera** del
envoltorio, fijo a cámara. Al final la cámara retrocede y se ven las ocho.

### 07 · RETROALIMENTACIÓN (28 s)

Voz desde ~2 s: *«Piense, converse y responda. ¿Por qué el pasajero es corresponsable de la
seguridad vial? Mencione un derecho y un deber del pasajero. ¿Cómo puede intervenir sin
aumentar el riesgo? Pause el video y responda con sus propias palabras.»*

Un panel de consola a la izquierda con las tres preguntas entrando una a una (numeral lavanda,
pregunta blanca, regla de respuesta que se dibuja). A la derecha, un **anillo de cuenta
atrás** con `3:00` en el centro y `TIEMPO DE PAUSA` debajo, que se traza sin marcar segundos.
Últimos ~6 s completamente quietos: es la pausa de lectura.

### 08 · CIERRE (12 s)

Voz desde ~1.5 s: *«Pasajero seguro. Decidir bien también es conducir la seguridad.»*

La firma **vuelve de la esquina al centro** y crece hasta el lockup grande (mismo archivo,
escala uniforme), mientras la retícula y las escuadras se retiran de fuera hacia dentro y el
área de reserva queda limpia. Bajo el logo, fuera de la reserva: «Pasajero seguro» y «Decidir
bien también es conducir la seguridad.» Y el pie legal, legible:
«Contenido basado en el documento suministrado. Valide vigencia y aplicación normativa con el
responsable PESV.» · «Marco base: Resolución 20223040040595 de 2022.»
Es el único plano con salida propia: fundido final en el último ~0.8 s.
