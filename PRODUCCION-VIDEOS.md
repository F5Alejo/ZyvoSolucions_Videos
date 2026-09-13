# Manual de producción — videos RiskMann

> Estándar de producción de los videos RiskMann. Cubre **dos formatos**, ambos
> verificados contra proyectos reales renderizados (septiembre 2026):
>
> | Formato | Para qué | Proyecto de referencia | Secciones |
> | --- | --- | --- | --- |
> | **Marketing** | Presentar la plataforma o un módulo a quien compra | `videos/riskmann-sala-de-control/` (68 s) | §1–§8 |
> | **Capacitación «Centro de mando»** | Módulos de formación (serie PESV «Pasajero seguro»), con voz | `videos/pesv-m01-mando/` (151 s) — **aprobado por el cliente** | §10–§12 |
> | **Capacitación «Ritmo»** | El mismo módulo como pieza corta de gancho, al compás de una pista, sin voz | `videos/pesv-m01-ritmo/` (60 s) — **aprobado por el cliente** | §13 |
>
> Los valores son los que realmente se usaron y renderizaron, no recomendaciones
> genéricas. Los prompts para pedir cada cosa están en [`GUIA-PROMPTS.md`](GUIA-PROMPTS.md).
>
> **Para quién:** cualquiera —persona o agente— que vaya a producir el siguiente video.
> Un agente que abra este repositorio debe leer este archivo antes de escribir una sola
> línea de composición.

---

## 0. La regla que manda sobre todas las demás

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**

En el primer video esta regla no existía y el resultado lo demostró: la pieza afirma
**«100% · TRAZABILIDAD DEL REGISTRO»**, una cifra que no sale de ningún dato de la
empresa. Se inventó porque el material de entrada no traía datos y el guion necesitaba
un número. Ese es exactamente el fallo que este manual existe para impedir.

Antes de aprobar un guion, aplica la prueba a **cada frase en pantalla**:

| Pregunta | Si la respuesta es no |
| --- | --- |
| ¿Esta frase está en un archivo que me dieron? | Bórrala o pide que te la aprueben por escrito. |
| ¿Esta cifra viene de un dato real de la empresa? | Bórrala. Sin excepción. |
| ¿Este nombre de módulo/submódulo aparece en la app o en los assets? | Usa el nombre que sí aparece. |
| ¿Esta afirmación de cumplimiento normativo la firmó alguien de RiskMann? | Bórrala. |

Un video puede ser espectacular sin afirmar nada falso. Lo que lo vuelve espectacular es
el montaje, el movimiento y el producto real en pantalla — no los adjetivos.

**Distingue concepto de funcionalidad.** «Sala de control» es un *concepto visual* (el
HUD azul con retícula y escuadras). No es un módulo de RiskMann y el video nunca debe
sugerir que lo sea. Los módulos reales son los que tienen icono en la portada de la
plataforma.

### 0.1 El manual de marca manda sobre el diseño

El logo de RiskMann tiene manual propio y no se negocia en ningún plano:

| Permitido | Prohibido |
| --- | --- |
| Usar **solo los archivos oficiales**: `riskmann_logo_blanco.png` (lockup *RiskMann by SOFU*, 840×280) y `riskmann_icono_blanco.png` (isotipo) | Redibujar, trazar o vectorizar el logo a mano |
| Escala **uniforme**, opacidad, traslación | Re-letrar el nombre con otra tipografía |
| Revelar el archivo completo con `clip-path` | Recolorear, deformar (escala no uniforme), rotar |
| Dejar libre su área de reserva (en el formato de capacitación: **44 px** alrededor de la tinta a 280 px de ancho) | Poner cualquier cosa encima o dentro de la reserva |

Dato útil: en `riskmann_logo_blanco.png` el isotipo ocupa x 35–215 y el nombre x 236–818.
`clip-path: inset(0 73.9% 0 0)` muestra **solo el isotipo** sin tocar el archivo.

> **Caso real:** los planos 03 y 09 de *Sala de control* redibujan el isotipo y re-letrean
> el nombre. Ese video incumple el manual y está pendiente de corrección (§9). El formato
> de capacitación nació ya cumpliéndolo.

### 0.2 Sin figuras humanas dibujadas

Monigotes y siluetas de línea fueron **rechazados por el cliente** («muy básicos y poco
profesionales»). Las personas aparecen solo en fotografía real — y sin caras
reconocibles, matrículas legibles ni logos de terceros (§10.4).

---

## 1. Qué hay que entregar antes de empezar

Ninguna producción arranca sin esto. La calidad del video está limitada por la calidad
de esta carpeta.

### 1.1 Ficha del módulo (obligatoria)

Un archivo de texto, `BRIEF-MODULO.txt`, con:

- **Módulo** y su nombre exacto tal como aparece en la plataforma.
- **A quién le habla el video**: al que compra (gerencia, HSEQ) o al que lo usa
  (conductor, coordinador). Cambia el vocabulario entero.
- **Los submódulos reales**, con su nombre exacto.
- **La copia aprobada**, si existe. Si la entregas, el video la usa *literal* — se
  reparte en planos, no se reescribe.
- **Cifras reales**, con su fuente. Si no hay, se dice: *no hay cifras* — y el video se
  construye sin ninguna.
- **La lista de lo prohibido**: normativas que no se pueden mencionar, promesas de
  cumplimiento que legal no aprueba, datos personales que no pueden salir en pantalla.

### 1.2 Grabaciones del módulo (lo que hace la diferencia)

Es el material más valioso y el más fácil de arruinar. **2 a 4 clips**, uno por paso del
flujo. Ejemplo para Inspecciones: crear inspección → llenar el formato → firmar →
informe generado.

| Regla | Por qué |
| --- | --- |
| 1920×1080, pantalla completa | El lienzo del video es 1920×1080; cualquier otra cosa se escala y pierde nitidez. |
| Sin barra del navegador, sin pestañas, sin notificaciones | El manual de composición prohíbe cromo de navegador en cuadro. |
| 10–20 segundos por clip | Más largo no cabe en un plano de 7–8s; hay que recortar y siempre se recorta mal. |
| Un solo paso por clip | Un clip largo con cuatro pasos no se puede repartir entre planos. |
| Cursor **lento**, con pausa antes de cada clic | Un movimiento apurado no se puede ralentizar sin que se vea a saltos. |
| Datos de demo, nunca reales | En el primer video salió una cédula legible en el carnet. No debe repetirse. |
| Sin zoom del navegador, al 100% | El zoom rompe la escala tipográfica del producto. |

Guárdalos en `assets/videos/` o en una carpeta que me indiques.

### 1.3 Capturas de pantalla

Para lo que no se mueve: pantallas de resultado, informes, certificados. PNG a resolución
nativa, sin recortar el cromo a mano.

### 1.4 Si el módulo tiene URL pública

Entonces no hace falta nada de lo anterior en su forma manual: el marco tiene captura
automática, que baja capturas reales, el texto del DOM y los colores de marca.

```bash
npx hyperframes capture "https://url-del-modulo" -o ./capture
```

Esto es lo que **no** se pudo hacer en el primer video (no había URL), y por eso el
inventario de assets se escribió a mano. Con captura real, la copia del video sale del
texto que ya está en el producto.

---

## 2. Identidad visual — valores verificados

Estos son los tokens reales de `frame.md` del primer video. **No los reinventes**: la
serie solo se ve como serie si todos los videos comparten exactamente estos valores.

### 2.1 Paleta

| Token | Valor | Uso |
| --- | --- | --- |
| `bg` | `#051427` | El suelo de todos los planos. Nunca negro puro. |
| `surface` | `#0C2B53` | Panel del centro de mando. |
| `surface-2` | `#0F396B` | Panel secundario, elevaciones. |
| `primary` | `#E6423C` | **El acento de foco. Uno por plano, nunca dos.** |
| `accent-2` | `#8E8FC4` | Lavanda. Solo cromo estructural: retícula, hairlines, escuadras, etiquetas de telemetría. Jamás compite con el rojo. |
| `text` | `#F2F7FF` | Titulares. |
| `text-muted` | `#A7BCCC` | Cuerpo y apoyo. |
| `text-light` | `#5D7793` | Terciario. |
| `border` | `rgba(142,143,196,0.28)` | Contorno de panel, 1.5px. |
| `card-bg` | `rgba(226,236,248,0.05)` | Relleno de tarjeta. |
| `grid` | `rgba(142,143,196,0.14)` | La retícula del HUD. Siempre bajo el 15%. |
| `glow` | `rgba(230,66,60,0.35)` | Halo rojo del elemento en foco. Uno por escena. |
| `positive` / `negative` | `#3DD68C` / `#E6423C` | Solo texto, sin relleno. |

**Elevación por contorno, nunca por sombra.** No hay una sola sombra difusa en la serie:
un panel se separa del fondo por su contorno de 1.5px y su relleno, no por un blur.

### 2.2 Las constantes del HUD (críticas para la continuidad)

Todos los planos que llevan HUD usan **exactamente** estos números. Nueve planos
construidos por nueve agentes distintos se ven como un solo centro de mando solo porque
estos valores se les entregaron como constantes:

```
Retícula:   paso 60 × 60 px, líneas de 1px, color rgba(142,143,196,0.14)
Escuadras:  4 marcas en L, brazos de 128px, trazo de 2px,
            color #8E8FC4 al 0.6 de opacidad, sangrado 56px desde cada borde
```

**El ciclo del HUD a lo largo de un video:**

1. El plano de apertura y el de dolor van **sin HUD** — es el mundo antes de la plataforma.
2. El plano de producto **enciende** el HUD: la retícula se dibuja de dentro hacia fuera,
   las escuadras entran una tras otra.
3. Los planos intermedios lo llevan **estático desde t=0**, sin animarlo.
4. El plano de cierre lo **retira** de fuera hacia dentro.

Ese arco es lo que convierte una lista de planos en una película.

### 2.3 Tipografía

**Montserrat**, la familia de la plataforma. Los `.woff2` están en
`videos/riskmann-sala-de-control/assets/fonts/` — cópialos a cada proyecto nuevo.

```css
font-family: "Montserrat", sans-serif;
```

**Regla dura:** toda fuente nombrada necesita su `@font-face` apuntando a un archivo real
dentro del proyecto. La máquina de render es un Chrome headless limpio, sin fuentes
instaladas: nombrar «Montserrat» sin el archivo hace que el MP4 salga con una genérica y
toda la tipografía cambia sin avisar. En el primer video esto se detectó tarde y hubo que
descargar la familia y parchear los nueve planos.

El peso y el tamaño hacen el trabajo de jerarquía: display 700–800, cuerpo 400,
etiquetas de cromo en mayúsculas con `letter-spacing` amplio.

### 2.4 Lista negativa

Nunca aparecen: barras de navegación, pies de página, scrollbars, cromo de navegador,
cursores del sistema, degradados morados de «IA», bokeh flotante, sombras difusas, ni
formas decorativas genéricas que sustituyan un asset real.

---

## 3. Estructura narrativa

### 3.1 El arco que funcionó

**BAB** — *antes → adelanto del después → puente/producto → recorrido → wow → cierre*.
Para un video de un solo módulo, la versión reducida es de **6 planos, ~45s**:

| # | Rol | Duración | Qué hace |
| --- | --- | --- | --- |
| 01 | `hook` | 7s | El dolor concreto de ese módulo, en el lenguaje del cliente. |
| 02 | `product_intro` | 7s | El HUD enciende, el módulo se nombra. |
| 03 | `feature_showcase` | 8s | El flujo real, con la grabación del módulo. |
| 04 | `feature_showcase` | 8s | El segundo paso del flujo, o los submódulos. |
| 05 | `benefit_highlight` | 7s | Lo que cambia — **solo con frases aprobadas**. |
| 06 | `branding` | 8s | Los paneles se van, el logo se arma, cierre *by SOFU*. |

Para un video general de plataforma, la versión completa es la de 9 planos y 68s del
primer video.

### 3.2 Duraciones

**7 u 8 segundos por plano.** No menos: un plano de 5s no alcanza a revelar y sostener.
No más: a partir de 9s hay que inventar movimiento para rellenar, y el movimiento
inventado es el que se ve barato.

### 3.3 Transiciones

Un juego corto, repetido:

- `crossfade` **0.5s** — el caso normal, entre planos del mismo mundo visual.
- `zoom-through` **0.4s** — solo en frontera de sección (dolor → producto, módulo → beneficio).
- `push-slide` — como mucho una vez por video, entre dos planos de función consecutivos.

Las inyecta el marco; no se escriben a mano.

### 3.4 El ritmo de revelado (lo que separa un video de una presentación)

**Ningún plano vuelca su contenido en el primer 25%.** El fallo clásico es dibujar todo
en la entrada y luego congelar: eso se lee como diapositiva.

- En t=0 entra **una sola pieza**.
- Cada pieza siguiente aparece **cuando su cue la nombra**, repartidas por todo el plano
  y sobre todo en la segunda mitad.
- El plano termina **sostenido y quieto**. Prefiere quietud a movimiento malo.
- Durante una sostenida solo se permite jitter de baja amplitud o internos de SVG vivos.
  **Nada de respirar** (escalar en bucle) ni de paneos lentos en la mitad final: molestan
  a la vista y son el tic más reconocible del video hecho por máquina.

Sin locución, el reloj del revelado son los **cues de texto en pantalla**. Con locución,
es la voz.

### 3.5 Curvas

`power3` por defecto — cola larga, asentamiento suave. **Nada rebota.** `back.out`,
`bounce.out` y `elastic.out` están prohibidos como entrada por defecto; el rebote es el
delator número uno de un video generado.

---

## 4. Catálogo de planos — qué forma para qué beat

El marco trae 22 formas probadas («blueprints»). Estas son las que se usaron y funcionaron:

| Beat | Forma | Cómo se usó en el primer video |
| --- | --- | --- |
| Gancho tipográfico | `kinetic-type-beats` | Línea fija con un hueco que cambia por corte seco; termina tachada en rojo. |
| Dolor por acumulación | `overwhelm-surround` | Fichas de trámite cerrando desde los cuatro bordes sobre una silueta quieta. |
| Producto / cierre de marca | `logo-assemble-lockup` | Las fichas se rompen en enjambre 3D y arman el isotipo. |
| Enumerar módulos | `grid-card-assemble` | Cuatro paneles en cascada, uno pasa al frente y el resto se desenfoca. |
| Producto real en pantalla | `device-surface-showcase` | El carnet QR como héroe, con barrido de escaneo y submódulos enganchados. |
| El dato en movimiento | `video-text-pivot` | Tres grabaciones reales, luego la pantalla central cede el hueco a una cifra. |
| Recorrer muchos submódulos | `spatial-pan-stations` | Paneo lateral por 7 estaciones sobre un lienzo de 9600px. |

**Varía las formas.** Repetir la misma en todos los planos recrea exactamente la monotonía
que el catálogo existe para evitar.

---

## 5. Reglas técnicas duras

Estas rompen el render o la validación. No son estilo.

### 5.1 Determinismo

El render avanza cuadro a cuadro haciendo *seeks*, no reproduce en tiempo real:

- Una sola línea de tiempo **pausada** por composición, registrada en `window.__timelines`.
- Entradas con `fromTo` y estado inicial explícito. Nunca tweens relativos (`+=`).
- **Prohibidos** `Math.random()` y `Date.now()`. Toda variación se deriva del índice del
  elemento.
- **Prohibidos** `repeat: -1` y `yoyo`. Cualquier "vida" es un tween finito.
- **Prohibidas** las animaciones CSS (`transition`, `@keyframes`): corren con el reloj del
  navegador, se desincronizan del seek y parpadean.

### 5.2 Solo transformaciones

Anima `x`, `y`, `scale`, `opacity`, `rotate` y propiedades de pintura. **Nunca** `width`,
`height`, `top`, `left` — ni `letterSpacing`.

> Caso real: el plano 08 animaba `letterSpacing` para el colapso de interletraje. El
> validador lo rechazó: esa propiedad refluye el texto y encaja los glifos en píxeles
> enteros, así que tiembla bajo el motor de captura. Se arregló partiendo la frase en
> glifos y animando la `x` de cada uno — mismo efecto, sin temblor.

### 5.3 Video: siempre en la raíz, nunca dentro de un plano

Los `<video>` van en `index.html` como clips de nivel raíz, con sus coordenadas absolutas.
El ensamblador **rechaza** un `<video>` dentro de una sub-composición.

Consecuencia de diseño: como el video queda clavado a coordenadas fijas del lienzo, **su
marco no puede moverse ni escalar mientras el clip está abierto**. Si el plano necesita
mover el panel, hazlo después de que la ventana del video cierre.

Patrón que funcionó: el plano dibuja el monitor (marco `surface` + contorno) y debajo una
**pantalla en reposo permanente** (gradiente oscuro + scanlines), para que cuando el clip
cierre el monitor nunca muestre un agujero.

```html
<video id="v-graficas" class="clip" src="assets/graficas.mp4"
       data-start="37.42" data-duration="3.2" data-track-index="7"
       style="position:absolute; left:528px; top:192px; width:864px; height:472px;
              object-fit:cover; border-radius:8px"
       preload="auto" muted playsinline></video>
```

`data-start` es global (tiempo del video completo), no local al plano.

### 5.4 Zona libre inferior

El **17% inferior** del cuadro (por debajo de y≈896) queda libre de contenido importante
en todos los planos, lleven subtítulos o no. Es consistencia de borde para toda la serie.

### 5.5 Densidad

El elemento principal ocupa **≥40%** del lienzo. Mínimo **3 capas** de profundidad (fondo
+ medio + frente). Nada de un grupo pequeño flotando en vacío. Prueba de entrecerrar los
ojos: tras el desenfoque todavía se distingue cuál es el elemento número uno.

---

## 6. El procedimiento

### 6.1 Crear el proyecto

Cada video es su propio proyecto dentro de `videos/`:

```bash
cd riskmann2-marketing-videos
npx hyperframes init "videos/riskmann-<modulo>" --non-interactive --example=blank \
    --skill=product-launch-video
```

### 6.2 Adoptar la identidad ya congelada

La estética del primer video está guardada como receta, disponible para cualquier
proyecto nuevo:

```bash
node ~/.claude/skills/media-use/scripts/recipe.mjs list --hyperframes . --json
node ~/.claude/skills/media-use/scripts/recipe.mjs use  --hyperframes . --name riskmann-hud
```

Esto trae el `frame.md` completo (paleta, tipografía, componentes) y los esqueletos de
guion. **Ahorra todo el paso de diseño** y garantiza que el video nuevo pertenezca a la
misma serie. Después copia `assets/fonts/` del primer proyecto.

### 6.3 Preparar los assets

Los archivos que va a nombrar el guion se ponen primero en `capture/assets/` (los videos
en `capture/assets/videos/`), y luego se montan:

```bash
node ~/.claude/skills/product-launch-video/scripts/stage-assets.mjs \
     --storyboard ./STORYBOARD.md --hyperframes .
```

Solo se monta lo que el guion nombra. Debe reportar `staged N/N` — cualquier faltante
significa que un plano va a pedir un archivo que no existe.

### 6.4 Construir, ensamblar, validar

```bash
node ~/.claude/skills/product-launch-video/scripts/frame-packets.mjs --project "$PWD" --storyboard "$PWD/STORYBOARD.md"
# … se construye un plano por agente, en paralelo …
node ~/.claude/skills/product-launch-video/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
node ~/.claude/skills/product-launch-video/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
npx hyperframes lint      # debe dar 0 errores
npx hyperframes check     # lint + runtime + layout + movimiento + contraste
npx hyperframes snapshot --at <puntos medios y ±0.1s de cada corte>
```

**Revisa la hoja de contactos antes de renderizar.** Ahí se detectan los planos vacíos y
los saltos entre cortes. En el primer video eso salvó la producción: el plano 06 aparecía
en negro y no se habría notado hasta ver el MP4 terminado.

### 6.5 Renderizar

```bash
npx hyperframes render --skill=product-launch-video --quality high --output renders/video.mp4
```

Referencia de tiempo: 68s a 1080p tardaron **4m 44s** y pesaron **15.9 MB**.

---

## 7. Trampas encontradas en la primera producción

Documentadas para que no cuesten tiempo dos veces.

| Trampa | Qué pasa | Cómo evitarla |
| --- | --- | --- |
| **Paquete de instrucciones muy grande** | El constructor de paquetes falla con «packet is 58762 bytes (limit 48000)» cuando un plano cita demasiadas recetas de movimiento. | Con una forma grande (`kinetic-type-beats`, `logo-assemble-lockup`, ~27–29 KB), cita como máximo **2 o 3 recetas**. Las demás se describen en prosa y el agente las abre desde `RULES_DIR`. |
| **Editar HTML con expresiones regulares** | Un patrón `<video ...>` coincidió primero dentro de un **comentario** y borró 4 KB de marcado. El plano salió en negro. | Nunca borres bloques HTML con regex sobre el archivo entero. Y **siempre** vuelve a sacar capturas después de editar a mano. |
| **Fuente sin archivo** | Nombrar una familia sin `@font-face` hace que el MP4 salga con otra tipografía, en silencio. | Copia `assets/fonts/` a cada proyecto y declara el `@font-face` en cada plano. |
| **Assets de marca inservibles** | `riskmann_logo_central_blanco.svg` resultó ser una ilustración a color de 250×300, no un logotipo blanco. | Para cierre en fondo oscuro usa **`riskmann_logo_blanco.png`** (el lockup real *RiskMann by SOFU*) y **`riskmann_icono_blanco.png`** (el isotipo). |
| **Iconos sobre fondo claro** | Los `.webp` de módulo son ilustraciones sobre fondo blanco; puestos directamente sobre el azul se ven sucios. | Siéntalos dentro de una tarjeta `surface` redondeada. |
| **Grabaciones con bandas negras** | Las tres grabaciones de UI traen sus propias bandas negras (son capturas verticales). | Grabar en 16:9 desde el principio, o aceptar el reencuadre. |
| **Tiempo de espera de navegación** | `check` falla intermitentemente con «Navigation timeout of 10000ms» cuando el proyecto carga muchos MB de video. | No es un error del proyecto: vuelve a correr `check`. |
| **Contraste bajo** | Etiquetas de cromo lavanda sobre azul quedan cerca de 3.9:1. | Para texto que se debe leer, sube a `text-muted` (`#A7BCCC`). El cromo decorativo puede quedarse abajo. |

Trampas añadidas en la serie PESV (formato de capacitación):

| Trampa | Qué pasa | Cómo evitarla |
| --- | --- | --- |
| **`visibility = "visible"` en un hijo** | Un `visible` explícito atraviesa el ocultamiento del plano: los glifos de la etiqueta del plano 01 seguían vivos debajo de los planos 02–07. Solo lo delató `check` («texto tapado» en el plano 04). | Revelar con `visibility = "inherit"`. Y **nunca** animar `visibility`/`display` de un elemento `clip` (se usa `opacity`). |
| **Máscara más estrecha que su frase** | Recorta palabras en silencio: desapareció «aumentar» del principio clave y cambió el sentido. Ni `lint` ni `check` lo ven. | Dimensionar cada máscara al texto real (`width: max-content`) y revisar **cada plano en reposo** con capturas. |
| **Mayúsculas acentuadas asomando** | La tilde de «Ó» o «Í» asoma por encima de la máscara antes del revelado. | Empezar el revelado en `yPercent: 150`, no 110. |
| **Falsos solapes con máscaras** | `check` da decenas de `content_overlap`: mide el texto oculto sin el recorte. | Mirar esos instantes, y declarar **solo** esos elementos con `data-layout-allow-overlap`. Luego revisar el reposo. |
| **Espacios en glifos `inline-block`** | Se colapsan: «CAPACITACIÓNPESV». | Espacio duro en cada celda de espacio: escribir `"\u00A0"` en el código (un espacio duro literal se ve igual que uno normal y se pierde al copiar). |
| **Foto sobregradada** | Brillo 0.5 + multiply 0.82 + velo global: la foto desaparece, queda azul plano. | Grado de §10.4 y un **scrim local** solo bajo el texto. |
| **Voz más corta que el plano** | 04 estaba pensado a 30 s y su voz duraba 9.6 s: 17 s de cola muerta. | Generar la voz **antes** de fijar duraciones (§11). |
| **Muchos constructores en paralelo** | Los límites de uso los cortan a medias y dejan archivos parciales. | Oleadas de 2; revisar el disco antes de relanzar. |
| **Estado guardado en `onUpdate`** | El renderizador salta en el tiempo y, al retroceder, ese callback no se ejecuta: el rodillo del formato «Ritmo» mostraba «REDUCIR» cuando tocaba «AUMENTAR». | Cada paso como `fromTo` explícito sobre la propiedad real; un desenfoque SVG se anima con `attr: { stdDeviation }`, no con un proxy. |
| **Lo invisible sigue contando** | `check` no entiende `backface-visibility` ni el recorte de `overflow: hidden`: la cara oculta de una tarjeta 3D y las palabras del rodillo fuera de la ventana dieron decenas de errores de solape y contraste. | Hacer invisible de verdad lo que no se ve: `opacity: 0` a la cara oculta en el medio giro, y a cada palabra del rodillo cuando sale de la ventana. |
| **Posiciones calculadas a ojo** | Anchos de palabras estimados → dos píldoras se montaron. | Que la fila la ordene flexbox y animar desde el lugar natural de cada elemento (`x: 0, y: 0` como destino). |
| **Texto decorativo auditado** | Números o cintas de fondo solo contorno (`color: transparent`) fallan «texto sin pintar» y contraste. | Marcarlos con `data-layout-ignore` (y `aria-hidden`). No forzarles contraste: son fondo. |
| **Graves que se comen la mezcla** | Con bombo e impactos, la subgrave se llevaba la normalización y los agudos quedaban 16 dB abajo. | `"pasa_altos": 90` en el JSON de mezcla; medir tres bandas (<120, 120–400, >400 Hz) y buscar que queden a pocos dB entre sí. |
| **Bloque del catálogo con su propia duración** | Cada bloque instalado lee su `data-duration` interno, no la del montaje: la foto del bloque de partículas se apagaba a mitad de escena aunque el hueco durara 8 s. | Editar `data-duration` y `data-composition-duration` dentro del archivo instalado. |
| **Variables de un bloque que chocan con los tokens de color** | La variable `accent` del bloque define `--accent`, así que elegir «blue» pintaba el azul puro de CSS en vez del de marca. | Fijar los colores de marca directamente en el archivo del bloque (es un archivo del proyecto desde que se instala). |
| **El bloque mide el texto con otro grosor** | El bloque calculaba el ancho con peso 600 mientras la hoja de estilos lo pintaba en 900: la frase se salía del cuadro. | Igualar el peso de la medición al que se ve. |
| **Amarillo (u otro color claro) como texto sobre fondo claro** | `#F9B410` sobre gris claro da 1.6:1; ilegible y `check` lo marca. | El color claro va en formas (pastillas, barras, subrayados) con tinta oscura encima; para texto, un tono oscuro de la marca. |
| **MP4 > 30 MB** | No se puede enviar por la sesión. | Copia de vista: `ffmpeg -crf 24` (el módulo 01 quedó en 11.4 MB). |
| **Escribir con `Set-Content`** | Corrompe los acentos. | Escribir archivos con Python o la herramienta de escritura. |

---

## 8. Lista de verificación antes de entregar

**Veracidad**

- [ ] Cada frase en pantalla se rastrea a un archivo entregado por RiskMann.
- [ ] No hay ninguna cifra sin fuente.
- [ ] No hay afirmación de cumplimiento normativo sin aprobación escrita.
- [ ] Los nombres de módulos y submódulos son los de la plataforma.
- [ ] Ningún dato personal real es legible en pantalla.
- [ ] Cada frase de la **locución** también se rastrea a la fuente (`tools/guion.json` la cita).
- [ ] El pie legal del cierre está presente y legible (formato de capacitación).

**Marca**

- [ ] El logo es el archivo oficial; ningún plano lo redibuja, re-letra, recolorea ni deforma.
- [ ] Nada invade su área de reserva.
- [ ] Ninguna figura humana dibujada; fotos sin caras reconocibles.

**Audio**

- [ ] `mezcla.py` terminó sin «FALLO» (banda de voz por encima de −40 dB).
- [ ] En el MP4 final: `highpass=f=400,volumedetect` da una media razonable (módulo 01: −22.9 dB).

**Técnica**

- [ ] `npx hyperframes lint` → 0 errores.
- [ ] `npx hyperframes check` → «Check passed».
- [ ] Hoja de contactos revisada: ningún plano vacío, ningún salto en los cortes.
- [ ] Los `.woff2` están en `assets/fonts/` y cada plano declara su `@font-face`.
- [ ] Los `<video>` están en `index.html`, no dentro de un plano.
- [ ] El 17% inferior está libre en todos los planos.

**Serie**

- [ ] Retícula a 60px y escuadras a 56px de sangrado, con los valores de §2.2.
- [ ] Un solo acento rojo por plano.
- [ ] El HUD enciende, persiste y se retira según §2.2.
- [ ] Las formas de plano varían; ninguna se repite en todos.

---

## 9. Estado actual de la serie

| Video | Estado | Ruta |
| --- | --- | --- |
| RiskMann · Sala de control (general, 68 s) | Renderizado, con y sin narración — **contiene copia inventada (§0) e incumple el manual de marca (§0.1)** | `videos/riskmann-sala-de-control/` |
| **PESV M01 «Centro de mando»** (151 s) | **Renderizado y aprobado. Es la plantilla de la serie.** | `videos/pesv-m01-mando/` → `renders/pesv-m01-mando.mp4` |
| PESV M01 base (réplica de diapositivas) | Referencia de contenido — fuera del repo | archivo local del equipo |
| PESV M01 «plus» | Rechazado (seguía siendo diapositiva; monigotes) — fuera del repo | archivo local del equipo |
| PESV M01 refactor fotográfico | Superado («muy básico») — fuera del repo | archivo local del equipo |
| **PESV M01 «Ritmo»** (60 s) | **Renderizado y aprobado.** Pieza corta sin voz. | `videos/pesv-m01-ritmo/` → `renders/pesv-m01-ritmo.mp4` |
| **PESV M01 «Ritmo» vertical** (60 s, 9:16) | **Renderizado.** Para TikTok / Reels / Shorts. | `videos/pesv-m01-ritmo-vertical/` |
| **SOFU BIC S.A.S. · comercial** (68 s) | **Renderizado.** Pieza de la casa matriz, desde su propio guion. Pendiente: datos de contacto y validación del portafolio. | `videos/sofu-comercial/` |
| PESV M01 «Profundidad» 16:9 y 9:16 | Exploración técnica: partículas por GPU y 3D con cámara. Apertura aprobada; escenas 3–7 sin construir. | `videos/pesv-m01-profundidad/` · `-vertical/` |
| PESV M02–M08 | Por hacer, con §10 (y §13 para su pieza corta) | — |
| Presentación anterior (12 s) | Del equipo, previo | `video-presentacion/` |

**Pendiente en el primer video:** sustituir «100% · TRAZABILIDAD DEL REGISTRO», revisar
las frases de §0, y rehacer los planos 03 y 09 con el archivo oficial del logo antes de
que la pieza se use comercialmente.

**Receta de identidad:** `riskmann-hud`, congelada en `~/.media/recipes/riskmann-hud`.

---

## 10. Formato de capacitación — «Centro de mando»

La dirección aprobada para la serie PESV después de tres intentos. Lo que el cliente
rechazó es tan útil como lo que aprobó:

| Intento | Veredicto del cliente | Lección |
| --- | --- | --- |
| Réplica de las diapositivas | Base aceptada | El documento es la fuente del **contenido**, no del formato |
| «Plus» animado | «No aplica… inspirada en las diapositivas» | Animar una diapositiva sigue siendo una diapositiva |
| Monigotes de línea | «Muy básicos y poco profesionales» | §0.2 |
| Refactor fotográfico | «Muy básico, no hay nada de destaque» | Fotos solas no dan identidad |
| **Centro de mando** | «Me gusta, sigámoslo ampliando» | Identidad RiskMann + fotos dentro de monitores + animación constante |

### 10.1 El documento que gobierna el módulo: `DIRECCION.md`

Cada módulo tiene un `DIRECCION.md` normativo **antes** de construir los planos. Es lo
que permite construir ocho planos por separado y que se vean como una sola sala. El de
`videos/pesv-m01-mando/DIRECCION.md` es el modelo: cópialo y cambia solo la tabla de
tiempos, la etiqueta y la descripción de cada plano.

### 10.2 El cromo persistente (idéntico en todos los planos intermedios)

```
Suelo       #051427 a sangre, como capa clip propia (nunca en #root)
Retícula    60×60 px, líneas rgba(142,143,196,0.14)
Escuadras   4 en L, 130×130, trazo 2 px #8E8FC4 al 0.6,
            en (56,56) · (1734,56) · (56,894) · (1734,894)
Reglas      laterales en x=84 y x=1820, de y=480 a y=840
Firma       riskmann_logo_blanco.png a 280 px de ancho, caja en left 92.33 / top 95
            (su tinta empieza en 104,104). Quieta. Reserva libre de 44 px.
Etiqueta    bajo la firma: regla roja + «CAPACITACIÓN PESV · MÓDULO NN · TEMA»,
            ~13 px lavanda, tracking 0.18em
Sección     arriba a la derecha, alineada a x=1816: «NN · NOMBRE DEL PLANO»
            — la única pieza de cromo que cambia de plano a plano
```

El plano de **apertura** construye este cromo en pantalla (el logo nace grande en el
centro y se va a la esquina); los intermedios lo llevan **quieto desde t=0**; el
**cierre** lo retira y devuelve el logo al centro. Es el mismo arco del §2.2.

### 10.3 Arquitectura de un módulo

| Plano | Rol | Qué lo hace funcionar |
| --- | --- | --- |
| 01 · Apertura | Gancho + identidad | El logo se arma, se hace firma, y una frase corta de la voz («Tú no conduces. / Pero decides.») |
| 02–05 · Contenido | Un concepto por plano | Una **forma distinta** en cada uno: monitor con detección, fotografía aérea con retículas, monitores en cascada, indicador analógico |
| 06 · Ruta | Dónde está el módulo en la serie | Paneo por las 8 estaciones, «ESTÁS AQUÍ» en rojo |
| 07 · Retroalimentación | Pausa activa | Preguntas del documento + anillo de pausa; **~6 s quietos** al final |
| 08 · Cierre | Firma + legal | Logo al centro, frase de cierre del documento, pie legal legible, fundido final |

**Duración del plano = voz + respiro.** Entre 12 y 28 s según la voz, nunca con cola muerta.
El módulo 01 quedó en 151 s: 16 · 20 · 20 · 21 · 16 · 18 · 28 · 12.

**Pie legal obligatorio en el cierre:** «Contenido basado en el documento suministrado.
Valide vigencia y aplicación normativa con el responsable PESV.» · «Marco base:
Resolución 20223040040595 de 2022.»

### 10.4 Fotografía

- **Fuente:** Pixabay (uso comercial sin atribución). Descargar en alta, armar hoja de
  contactos y **mirarlas** antes de elegir: los títulos mienten.
- **Descartar:** caras reconocibles (también reflejadas en espejos), matrículas legibles,
  logos de marcas.
- **Dónde van:** dentro de **monitores** (panel `#0C2B53`, contorno 1.5 px
  `rgba(142,143,196,0.28)`, marco interior 12–16 px); a sangre solo si el plano lo pide.
- **Grado:** `filter: brightness(0.78) contrast(1.14) saturate(0.45) hue-rotate(-6deg)` +
  capa `#0C2B53` en `multiply` a ~0.40. Scrim local bajo el texto, nunca un velo global.
- Fotos del módulo 01 en `videos/pesv-m01-mando/assets/fotos/` y biblioteca de
  candidatas ya revisadas (sin caras ni matrículas) en `assets/fotos-pixabay/`:
  reutilizables en otros módulos.

### 10.5 Producir el módulo NN (paso a paso)

```bash
# 1. Copiar la plantilla aprobada (sin renders ni capturas)
cp -r videos/pesv-m01-mando videos/pesv-mNN-<tema>
rm -rf videos/pesv-mNN-<tema>/renders videos/pesv-mNN-<tema>/snapshots

# 2. Guion: tools/guion.json con las frases del documento de ESE módulo (§0)
cd videos/pesv-mNN-<tema>
python ../../tools/descargar-voz.py             # solo la primera vez en cada equipo
python ../../tools/voz.py tools/guion.json      # WAV por línea + duración real

# 3. Con las duraciones reales: tabla de tiempos en DIRECCION.md e index.html
# 4. Planos: 01 y 08 casi no cambian (texto de etiqueta y cierre); 02-07 se rediseñan
#    contra DIRECCION.md. 06 solo mueve «ESTÁS AQUÍ» a la estación NN.
# 5. Sonido
python ../../tools/mezcla.py tools/mezcla-modulo.json
# 6. Validar (§6.4) y renderizar
npx hyperframes lint && npx hyperframes check
npx hyperframes snapshot --at <medios y reposos de cada plano>
npx hyperframes render --quality high --output renders/pesv-mNN-<tema>.mp4 --browser-timeout 180
```

**Primero la apertura con sonido, luego el resto.** Mostrar 16 s aprobables cuesta ~10 min;
construir el módulo entero en la dirección equivocada costó una hora cada vez.

Los ocho módulos de la serie (según el documento): 01 Actor vial · 02 Antes del viaje ·
03 Ascenso y descenso · 04 Durante el viaje · 05 Pasajeros vulnerables · 06 Acompañante
en moto · 07 Emergencias PAS · 08 Taller y evaluación.

---

## 11. Audio — voz, efectos y cama

Todo es gratuito, local y sin límite de uso. Las herramientas compartidas viven en
`tools/` en la raíz del repositorio:

| Pieza | Herramienta | Detalle |
| --- | --- | --- |
| **Voz** | Piper TTS, voz **`es_ES-davefx-medium`** (elegida por el cliente) | `pip install piper-tts` y, una vez, `python tools/descargar-voz.py` (baja el modelo de 60 MB a `tools/voces/` y verifica su huella; no va en git). `tools/voz.py` genera un WAV por línea y **avisa si una línea no cabe** en su plano (`"maximo"`). |
| **Efectos** | Biblioteca de `/media-use` (19 efectos) | Licencia Pixabay: uso comercial sin atribución. En `~/.claude/skills/media-use/audio/assets/sfx/`. |
| **Cama** | Síntesis propia con osciladores | Sin derechos de terceros. **Fundamentales ≥ 110 Hz**: un drone de 55–82 Hz mide bien y suena a silencio en un portátil. |
| **Pista rítmica** | `tools/ritmo.py` + un JSON por pieza | Bombo, platillos, palmas, bajo y acordes sintetizados a un BPM, por secciones, con subidas de ruido antes de cada cambio. Determinista, sin derechos de terceros. Para videos sin voz. |
| **Mezcla** | `tools/mezcla.py` + un JSON por pieza | Voz y `pistas` con `adelay`, cama opcional con ducking por cadena lateral, `pasa_altos` opcional, −16 LUFS, y **verificación del espectro**: falla si la banda alta está vacía. |

**Reglas:**

- La voz se genera **antes** de fijar la duración de los planos, y el plano se adapta a
  ella. Si una frase no cabe en un plano ya animado, se acorta la frase, no el plano.
- Cada efecto va en el instante visual que lo justifica (un clic cuando se fija una
  retícula, un impacto cuando entra el logo). Nada de relleno.
- MusicGen **no sirve**: su licencia no es comercial.
- La mezcla va en `index.html` como un único `<audio class="clip">` en la raíz.

La mezcla del módulo 01 (`videos/pesv-m01-mando/tools/mezcla-modulo.json`) es el modelo:
8 capas de cama, 9 líneas de voz, 54 efectos.

---

## 12. Tiempos y pesos medidos

| Pieza | Duración | Construcción | Render | Peso |
| --- | --- | --- | --- | --- |
| Marketing «Sala de control» | 68 s | ~1 día (inventar el sistema) | 4 min 44 s | 15.9 MB |
| PESV M01 «Centro de mando» | 151 s | muestra ~10 min + ~2 h | ~9 min 30 s | 39.1 MB (vista 11.4 MB) |
| PESV M01 «Ritmo» (sin voz) | 60 s | muestra ~30 min + ~1 h | 4 min 02 s | 15.3 MB |
| PESV M01 «Ritmo» vertical 9:16 | 60 s | ~1 h (recomposición de las 7 escenas) | 4 min 09 s | 14.5 MB |

Con la plantilla de §10 un módulo nuevo debería costar bastante menos que el primero: el
sistema ya existe y solo cambian el guion y los planos de contenido.

---

## 13. Formato de capacitación — «Ritmo» (pieza corta, sin voz)

La misma presentación del módulo, pero como pieza de **60 s que se sostiene sin voz**: la
música marca el tiempo y cada entrada cae sobre el pulso. Sirve de gancho (redes,
pantallas, apertura de una sesión) junto al módulo completo con voz de §10. El cliente pidió
«mejores animaciones, mejor ritmo, más movimiento, fluidez, que sea entretenido» y lo aprobó
sin cambios. Proyecto de referencia: `videos/pesv-m01-ritmo/` (lee su `DIRECCION.md`).

### 13.1 El pulso manda

**120 BPM → pulso de 0.5 s, compás de 2 s.** Cada escena empieza en frontera de compás y
todos sus tiempos son múltiplos del pulso (`const P = 0.5; const B = n => n * P;`). La pista
de `tools/ritmo.py` usa el mismo BPM, así que imagen y sonido coinciden sin ajustar a mano.

### 13.2 Diferencias con «Centro de mando»

| | Centro de mando (§10) | Ritmo |
| --- | --- | --- |
| Duración | ~2:30, dictada por la voz | 60 s, dictada por el pulso |
| Fondo | HUD oscuro persistente | Paleta de las diapositivas del documento: papel `#F5F8FC` y marino `#0B2F6B` alternados escena a escena |
| Logo | Firma blanca arriba a la izquierda | Logo a color en una píldora blanca abajo a la izquierda (se lee sobre papel y sobre marino) |
| Cromo | Retícula, escuadras, reglas | Barra de progreso del video completo con una marca en cada cambio de escena |
| Cortes | Fundidos entre planos | **Cada escena cierra tapando la pantalla con el fondo de la siguiente** (ver 13.3) |

### 13.3 El repertorio de movimiento

Cada técnica es una receta de `/hyperframes-animation` que la serie no había usado. Ninguna
se repite en dos escenas: esa variedad es lo que hace entretenida la pieza.

| Escena | Técnica | Receta |
| --- | --- | --- |
| Gancho | Cada palabra entra distinto (escala con desenfoque, golpe lateral, subida inclinada); estela de velocidad | `kinetic-beat-slam`, `motion-blur-streak` |
| Gancho | Tachón y círculo dibujados a mano | `css-marker-patterns` (sketchout, circle) |
| Corresponsable | Cascada de palabras, cada una antes de que termine la anterior; marcador detrás de una palabra | `waterfall-entry`, `css-marker-patterns` |
| Corresponsable | Un punto que se transforma en la tarjeta con la foto | `card-morph-anchor` |
| Roles | Palabras que llegan desde una nube 3D y se ordenan; barrido de color por dentro de las letras | `depth-scatter-assemble`, `gradient-text-sweep` |
| Deberes | Tarjetas que giran en 3D por turno | `transitions/css-3d` (card flip) |
| Principio | Rodillo tipo tragamonedas | `vertical-spring-ticker` |
| Ruta | Luz que recorre los 8 módulos, uno por pulso | pasos discretos sobre el pulso |

**Salidas:** iris desde el círculo · bloques verticales alternados · barrido diagonal ·
barrido con estela y panel que empuja · la ventana del rodillo crece hasta llenar ·
persianas · y el único fundido de la pieza al final.

### 13.4 Sonido

```bash
python ../../tools/ritmo.py tools/ritmo-video.json    # pista a 120 BPM por secciones
python ../../tools/mezcla.py tools/mezcla-video.json  # pista + efectos, pasa_altos 90, -16 LUFS
```

Un efecto en cada golpe y en cada transición (62 en el módulo 01). Balance medido del
módulo 01: −21 / −20 / −22.5 dB en graves, medios y agudos.

### 13.4b La variante vertical (9:16) para redes

`videos/pesv-m01-ritmo-vertical/` es el mismo minuto en **1080×1920**, para TikTok, Reels y
Shorts. **No es el horizontal recortado**: cada escena se recompone, y eso es todo el trabajo.

- **Lienzo**: `data-width="1080" data-height="1920"` en `index.html` y en cada escena, más el
  `width`/`height` del `#root` y del `body`.
- **Zona segura**: el contenido vive entre y≈300 y y≈1500. Arriba va el nombre de usuario y
  abajo los botones y los subtítulos de la app; la firma y la barra de progreso suben a
  y≈1560-1700.
- **Recomponer, no escalar**: lo que iba lado a lado se apila (la foto bajo el texto), las
  frases largas se parten en dos líneas, las filas de fichas se envuelven en dos renglones y
  la ruta de 8 módulos pasa de barra horizontal a **riel vertical**.
- **Tipografía proporcionalmente mayor**: un titular de 92 px en 16:9 se lee en 86 px sobre un
  cuadro que mide la mitad de ancho.
- **Mismo pulso, mismo audio**: los tiempos no cambian, así que las dos versiones comparten la
  mezcla (`assets/mezcla-video.wav`) y quedan sincronizadas.

Medido: render 4 min 09 s, 14.5 MB.

### 13.5 Producir la pieza «Ritmo» de otro módulo

1. Copiar `videos/pesv-m01-ritmo/` (sin `renders/` ni `snapshots/`).
2. Escoger del documento de ese módulo **una frase por escena**. Sin voz, lo que no cabe en
   pantalla no se dice: menos texto que en el módulo completo.
3. Reasignar las técnicas de 13.3 a las ideas nuevas, sin repetir ninguna, y mantener una
   salida distinta por escena.
4. Ajustar `tools/ritmo-video.json` (secciones y subidas en los cambios de escena) y los
   efectos de `tools/mezcla-video.json` a los nuevos tiempos.
5. **Primero una muestra de ~16 s con sonido**, luego el resto.
6. `check` → capturas en cada cambio de escena → render → revisar los cortes en el MP4.

---

## 14. Formato de curso — «lámina a lámina», con hueco para voz humana

Cuando el material de entrada es un **PPTX de capacitación con notas de orador**, el video ya
viene escrito: las notas son el guion y las láminas son la estructura. Lo que hay que resolver
es el **tiempo**. La plantilla es `videos/ruta-segura-m1/`.

### 14.1 La decisión de formato

- **Un video por módulo**, no uno por curso. Un PPTX de 33 láminas son ~29 min de narración;
  partido por módulos quedan piezas de 8 a 12 min, que es lo que una persona ve de una sentada
  y lo que se puede volver a grabar sin rehacer todo.
- **La voz se puede cambiar sin rehacer el video.** El montaje no guarda tiempos absolutos
  escritos a mano: los calcula a partir de la locución vigente (§14.3). Así se entrega una
  versión con voz sintética para aprobar la imagen, y el día que la grabe una persona se
  corre el mismo procedimiento sin tocar ninguna marca de tiempo.

### 14.2 Medir antes de animar

El paso que hace que el formato funcione. Con Piper, frase por frase:

```bash
python -m piper -m tools/voces/es_ES-davefx-medium.onnx -f frase.wav   # texto por stdin
```

Con ElevenLabs no hace falta trocear: el endpoint `/with-timestamps` devuelve el instante de
**cada carácter**, así que el inicio de cada frase se lee en vez de estimarse. Es la forma
preferida — más exacta y una sola llamada por lámina.

Se guarda la duración de cada frase (`tools/tiempos-medidos.json`). Con eso:

- la **duración de la lámina** = duración de su narración + ~1,2 s de aire;
- el **momento de cada aparición** = el segundo en que el narrador nombra esa cosa.

Sin esa medición, un video de doce minutos es una secuencia de láminas quietas. Con ella, cada
elemento entra cuando la voz lo menciona y el módulo se deja ver.

> **Piper falla con comillas angulares** (`«…»`): termina en código 1 sin escribir el WAV
> (`wave.Error: # channels not specified`). Medir frase por frase aísla el problema; si una
> frase falla, se estima por conteo de palabras (~0,46 s/palabra a 130 ppm).

> Las notas pueden traer rótulos del documento (`GUION DE VOZ — PRIMERA PERSONA`). No son
> narración: se descuentan del tiempo y no entran al libreto.

**Con ElevenLabs, tres decisiones probadas:**

- **`eleven_v3`, no `eleven_multilingual_v2`.** En español la entonación interrogativa sube
  al final sin palabra que la anuncie, y estos guiones están llenos de preguntas: v2 las lee
  como afirmaciones y delata el video como sintético. v3 las resuelve, habla más pausado y
  también devuelve timestamps. No acepta `previous_text` / `next_text` — el encadenado de
  entonación entre láminas solo sirve en los modelos v2.
- **Las cifras, escritas en palabras** antes de enviarlas. «Ley 2466 de 2025» leída como
  «veinticuatro sesenta y seis» arruina la única referencia jurídica de un módulo.
- **El máster de voz, en MP3.** En WAV, once minutos pesan 61 MB y el navegador no lo carga
  dentro de los 10 s que da `check`: el runtime se cae con `Navigation timeout of 10000 ms`.

### 14.3 Las composiciones se generan, no se escriben

Once láminas con el mismo encuadre no se mantienen a mano. En `tools/`:

- `base.py` — paleta, fuentes y **el encuadre común** (ceja, número, título, regla, pie).
- `eNN.py` — una lámina por archivo: CSS, cuerpo y línea de tiempo, con la marca de tiempo de
  la frase que dispara cada aparición escrita en el comentario.
- `cronometro.py` — **el mapa entre dos locuciones** (ver abajo).
- `voz-eleven.py` — pide la locución con timestamps y escribe `tiempos-voz.json`.
- `pista.py` — coloca cada lámina en su sitio del máster, normaliza a −16 LUFS y verifica.
- `construir.py` — encadena, calcula inicios y arma el `index.html` con barra, sello y voz.
- `guion.py` — escribe `GUION-VOZ.md`, el libreto con la **ventana absoluta** de cada lámina.

**Lo que hace sostenible el formato es `cronometro.py`.** Las apariciones se escriben una vez
contra una locución de referencia; cuando la voz definitiva dura otra cosa, el módulo traduce
cada marca de tiempo: exacto en cada frontera de frase, proporcional dentro de la frase,
desplazamiento fijo en la cola. Las ochenta y tantas marcas se recolocan solas y `DUR` deja de
escribirse (`DUR = cronometro.duracion(LAMINA)`).

Esto no es una comodidad: es lo que permite entregar una versión con voz sintética para
aprobar la imagen y luego reemplazarla por una grabación humana sin rehacer el montaje. Ojo,
la voz nueva no es uniformemente más rápida ni más lenta — en la primera prueba una lámina se
acortó 3 s y la siguiente se alargó 6 s.

### 14.4 Reglas de composición para láminas de ~60 s

- **Una sola línea de fuente documental** abajo (y=946). Nada puede invadirla: es el error que
  más veces apareció. Los cierres de lámina van en una sola línea, no en dos.
- **Título de máximo dos renglones** (50 px, ancho 1450) y la regla de acento **debajo** de esa
  caja, no dentro.
- **Sustituir en vez de acumular.** Cuando entra la idea de cierre, se apaga la anterior en el
  mismo sitio; si no, la lámina termina siendo un muro.
- **Una sola petición al espectador**: la pastilla «PAUSA EL VIDEO Y RESPONDE», y solo donde la
  narración lo pide.
- `check` toma **nueve muestras** en doce minutos: no basta. Hay que sacar `snapshot` en el
  momento más lleno de cada lámina (el final) y revisar la hoja de contactos.

### 14.4b Renderizar once minutos en una máquina de 8 GB

Un módulo entero de una sola vez **no cabe**: el sistema mata el proceso. Los tres
consumidores son el Chrome del usuario (~1,5 GB), el Chrome sin cabeza del render y un
`ffmpeg` que se asienta en ~650 MB y no baja. Dos medidas, en este orden:

1. **La voz fuera del `index.html`.** Con el `<audio>` dentro, Chrome decodifica el MP3
   entero a PCM —unos 250 MB para once minutos— y ese es justo el margen que falta. Se
   renderiza mudo y se pega después: las dos pistas arrancan en cero y miden lo mismo.
2. **El render por partes.** `construir.py --partes 4` escribe cuatro `index-parte-N.html`
   con las escenas rebasadas a su propio cero y la barra de avance ajustada para que siga
   midiendo el módulo completo. Cada parte se renderiza sola y se unen sin recodificar.

```bash
python tools/construir.py --sin-audio --partes 4
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
# ... una por una
python tools/montar.py     # une, pega la voz y verifica duraciones
```

Partir no baja el pico de memoria: **acorta la exposición y hace barato el fallo**. Si una
parte muere se repite esa parte (≈10 min), no cuarenta minutos de trabajo. Los cortes caen
en frontera de escena, donde la lámina saliente ya está apagada (§14.4), así que la unión no
se ve.

> Cuando un render muere por memoria **deja un `ffmpeg` huérfano de ~650 MB**. Hay que
> matarlo antes de reintentar o el siguiente intento arranca con menos margen que el anterior.

### 14.5 Producir el módulo siguiente

1. Extraer las láminas del módulo del PPTX (texto y notas) y medir frase por frase.
2. Copiar `videos/ruta-segura-m1/` sin `renders/`, `snapshots/` ni `compositions/`.
3. Reemplazar `tools/eNN.py` por las láminas nuevas, reutilizando `base.py` sin tocarlo.
4. `python tools/construir.py` → `npx hyperframes check` → capturas → render.
5. Locutar (`voz-eleven.py`), volver a construir, armar la pista (`pista.py`).
6. `python tools/guion.py` y entregar `GUION-VOZ.md` junto con el MP4.
