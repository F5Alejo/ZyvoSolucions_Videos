# Guía de prompts — producción de video con HyperFrames

> **Qué es esto.** Un catálogo de instrucciones probadas: *«con este prompt consigo esto»*.
> Cada entrada se escribió justo después de ejecutarse, con el resultado a la vista — no
> reconstruida de memoria al final. Lo que aquí aparece **funcionó de verdad** en este
> repositorio; lo que falló también está documentado, porque ahorra más tiempo que lo que
> salió bien.
>
> Se usa con Claude Code abierto en la carpeta `riskmann2-marketing-videos`.

---

## Cómo leer una entrada

Cada prompt trae: **qué consigue** · **el prompt literal** · **qué te devuelve** ·
**cuánto tarda** · **qué necesitas tener listo antes**.

Los prompts están escritos para pegarse tal cual, cambiando solo lo que va `<entre
ángulos>`.

---

# 1 · Arrancar

### 1.1 — Un video nuevo desde un documento

**Consigues:** un video completo a partir de un PDF o unas diapositivas que ya existen.

```
Lee <ruta del documento>. Quiero un video que replique su sistema de
diapositivas con revelado progresivo: cada elemento aparece cuando la
narración lo nombra.

Antes de construir nada:
1. Extrae los colores reales del documento muestreando los píxeles, no los
   estimes a ojo.
2. Escribe un frame.md con esos valores y con las reglas de composición.
3. Enséñame el guion antes de animar.

Regla que manda sobre todo: nada entra al video si no puede rastrearse al
documento. Sin cifras inventadas, sin afirmaciones normativas que no estén
en el material.
```

**Te devuelve:** proyecto scaffolded, `frame.md` con la paleta real, `BRIEF.md`,
`STORYBOARD.md` y el guion para que lo apruebes.
**Tarda:** 10–15 min hasta el guion.
**Necesitas:** el documento en local, o capturas legibles de cada página.

> **Por qué el muestreo de píxeles importa.** En este repositorio dio
> `#0B2F6B` como navy dominante en el 93 % de las láminas. A ojo se habría puesto un azul
> «parecido» y las dos series no habrían encajado nunca.

### 1.2 — Un video de marketing desde assets sueltos

**Consigues:** una pieza promocional a partir de logos, capturas y grabaciones de UI.

```
Con /hyperframes, haz un video de presentación de <producto> usando los
recursos de <carpeta de assets>. Que sea vistoso.

Antes de escribir el guion, dime qué afirmaciones vas a poner en pantalla y
de dónde sale cada una. Si algo no está en los archivos, no lo pongas.
```

**Te devuelve:** una ronda de conceptos para elegir, luego el video.
**Tarda:** 1–2 h con revisiones.

> **La segunda frase del prompt no es opcional.** Sin ella, el primer video de este
> repositorio acabó afirmando un «100 % de trazabilidad» que no salía de ningún dato de la
> empresa.

---

# 2 · Dirigir el resultado

### 2.1 — Elegir el concepto antes de gastar tiempo

**Consigues:** cinco direcciones distintas para el mismo material, y eliges.

```
Antes de construir, proponme cinco conceptos visuales distintos para este
video. Que sean genuinamente diferentes entre sí, no variaciones del mismo.
Recomiéndame uno y dime por qué.
```

**Te devuelve:** cinco propuestas en texto, con recomendación.
**Tarda:** 2 min. **Ahorra:** horas de construir lo que no querías.

### 2.2 — Subir el nivel de un video que ya existe

**Consigues:** una versión mejorada sin rehacer la identidad.

```
Haz una versión plus de <proyecto>. Hereda su frame.md entero — misma
paleta, misma retícula, mismo cromo — y añade dos capas:

1. Diagramas que expliquen, dibujados como SVG que se traza solo. No
   imágenes pegadas, no iconos de librería.
2. Una cámara que viaje entre láminas sobre un lienzo continuo, en vez de
   fundidos. La cámara nunca se mueve mientras hay texto entrando.
```

**Te devuelve:** un proyecto nuevo hermano del anterior, con la misma identidad.
**Tarda:** 40–60 min.

### 2.3 — Refactor: salir del formato diapositiva

**Consigues:** una pieza de motion design real a partir de material que nació como
presentación. Es la dirección que el cliente aprobó para la serie PESV.

```
Haz un refactor de <proyecto>. El documento es la FUENTE DEL CONTENIDO, no el
formato visual: fuera la lámina blanca, los márgenes, la ambladura, el pie
repetido y las viñetas.

Lenguaje: fotografía real a sangre, gradada a la paleta de marca, con una capa
técnica fina encima (reglas de 1px, etiquetas pequeñas) y la tipografía grande
como suceso, entrando por máscara, nunca por fundido. Un empuje lento y
continuo sobre la foto por plano. Nada de figuras humanas dibujadas.

Antes de construir el video entero, construye SOLO el plano de apertura y
enséñame un fotograma a resolución completa.
```

**Te devuelve:** un plano de muestra para aprobar; con el sí, el resto del módulo.
**Tarda:** 5 min la muestra, ~45 min el resto.

> **La última frase es la que más ahorra.** Las dos versiones anteriores de este módulo se
> construyeron enteras (50 min + 9 min de render cada una) antes de que el cliente dijera
> que no era la dirección. La muestra de un solo plano cuesta cinco minutos.

### 2.4 — Conseguir fotografía sin salir de la sesión

```
Busca en Pixabay fotos para <lista de tomas>. Descárgalas en alta, arma una
hoja de contactos numerada, y MÍRALAS antes de elegir. Descarta cualquiera
con caras reconocibles, matrículas legibles o logos de marca.
```

**Por qué «míralas»:** los títulos de las fotos mienten. En este repositorio, la foto
titulada «Rearview Mirror Windshield» mostraba los ojos del conductor reflejados — descartada.
La licencia de Pixabay permite uso comercial sin atribución.

### 2.4b — Darle identidad de marca a una serie de formación

**Consigues:** que un módulo de capacitación se vea como una pieza RiskMann y no como una
presentación con fotos — logo vivo, animación constante, un universo visual propio. Es la
dirección **«Centro de mando»** que el cliente aprobó para la serie PESV después de llamar
«muy básico» al refactor fotográfico.

```
Toma como referencia de identidad <video de marca aprobado> (logo de RiskMann,
densidad de animación, recursos, HUD) y haz un prototipo nuevo de <módulo>
con ese concepto. El documento sigue siendo la única fuente del contenido.

Regla de marca: solo el archivo oficial del logo; nada de redibujarlo,
re-letrarlo, recolorearlo ni taparlo. Sin figuras humanas dibujadas.

Construye SOLO la apertura (~15 s) CON SONIDO (voz + efectos + cama) y
pásamela antes de seguir.
```

Con el sí:

```
Me gusta, amplíalo de esa misma manera. Escribe primero un DIRECCION.md con
el cromo persistente, la paleta y el tiempo de cada plano, y que todos los
planos se construyan contra ese documento.
```

**Te devuelve:** la muestra de apertura; luego el módulo completo con un `DIRECCION.md`
normativo, 8 planos, mezcla y render.
**Tarda:** ~10 min la muestra; ~2 h el módulo (construcción + verificación) + render.

> **Por qué «CON SONIDO» en la muestra:** la voz fija la duración real de cada plano. En
> este módulo, el plano de los tres deberes estaba pensado a 30 s y su voz duraba 9.6 s: 17 s
> de cola muerta. Se recortó a 21 s antes de construirlo, no después.
>
> **Por qué `DIRECCION.md`:** ocho planos construidos por separado solo se ven como una
> sola sala si comparten las mismas constantes escritas (posición exacta del logo, retícula,
> escuadras, etiqueta). Es el contrato que hace posible construir en paralelo.

### 2.4c — Más ritmo y animaciones nuevas, sin voz

**Consigues:** una versión corta (60 s) del mismo módulo que se sostiene sola: cada
entrada cae sobre el pulso de una pista, cada escena se mueve con una técnica distinta y
los cambios de escena son fluidos. Es el formato **«Ritmo»**; el cliente lo aprobó sin
cambios («EXCELENTE»).

```
Sigue siendo una presentación del mismo módulo, pero quiero probar
animaciones mejores: más ritmo, más movimiento, fluidez, que sea
entretenido. Cosas nuevas, nada que ya hayamos usado. 60 segundos, sin voz.
```

**Te devuelve:** una muestra de ~16 s con sonido para aprobar; con el sí, los 60 s.
**Tarda:** ~30 min la muestra, ~1 h el resto, 4 min de render.

> **Lo que hizo funcionar este prompt:**
> - **«Nada que ya hayamos usado»** obliga a escoger técnicas nuevas del catálogo del
>   framework: tipografía que golpea al compás, trazos a mano, una forma que se transforma
>   entre escenas, tarjetas que giran en 3D, un rodillo tipo tragamonedas. Qué técnica va en
>   cada escena está en `PRODUCCION-VIDEOS.md` §13.3.
> - **Sin voz, la música manda:** todo cae en múltiplos de medio segundo (120 BPM) y la
>   pista se sintetiza con `tools/ritmo.py` al mismo tempo.
> - **Ojo con la pregunta de concepto.** Primero se propusieron cinco conceptos visuales
>   radicales y el cliente aclaró que no quería otro concepto, sino **mejor movimiento** en
>   el mismo formato. Si lo que falla es la animación, dilo así: ahorra una ronda.

### 2.4d — Convertir un PPTX de capacitación en video, con hueco para voz humana

**Consigues:** el curso partido en videos por módulo (8 a 12 min cada uno), **sin voz**, con
cada aparición en pantalla montada sobre el segundo exacto en que la narración la menciona,
más el libreto con la ventana de tiempo de cada lámina para grabar la locución después.

```
Necesito animar esta presentación: <ruta al .pptx>
Hazlo por módulos, un video por módulo.
Dejo el hueco para voz humana: entrégalo sin locución, pero montado
sobre los tiempos reales de la narración, y dame el guion con los
tiempos para grabarla después.
```

**Te devuelve:** el MP4 del primer módulo y un `GUION-VOZ.md` con la ventana absoluta de
cada lámina y las frases en el orden en que el video las muestra.
**Tarda:** ~25 min medir la narración, ~2 h componer las láminas, ~40 min de render.

> **Lo que hizo funcionar este prompt:**
> - **Las notas del orador son el guion.** Antes de animar nada se sintetiza **frase por
>   frase** con Piper y se guardan las duraciones. La duración de cada lámina sale de ahí, no
>   de una estimación. Sin esa medición el resultado es una secuencia de láminas quietas.
> - **«Dejo el hueco para voz humana»** es lo que permite aprobar la imagen antes de pagar
>   estudio: una corrección de texto no obliga a re-renderizar doce minutos.
> - **Pedir «por módulos» acota el riesgo.** Un PPTX de 33 láminas son ~29 min de narración;
>   si algo no gusta, se rehace un módulo, no el curso.
> - Detalle del procedimiento en `PRODUCCION-VIDEOS.md` §14.

### 2.5 — Corregir un plano concreto

**Consigues:** un cambio quirúrgico sin tocar el resto.

```
En <proyecto>, el plano <NN> tiene <problema>. Arréglalo sin tocar los
demás planos, y vuelve a sacar capturas de ese plano antes de renderizar.
```

**Tarda:** 5 min + render.

---

### 2.6 — La misma pieza para otra marca, sin que dependa de la primera

**Consigues:** la versión de un evento para una segunda marca, con identidad propia. Nació de
FEGIR: la primera versión recoloreó la invitación de Yezid y el cliente la rechazó.

```
<ruta al manual de la marca> ahí está todo. La pieza debe ser solo de <marca>:
nada de <otra marca> (nombre, web, paleta ni estructura). Saca la identidad del
manual —colores muestreados, logo desde sus vectores— y dime qué datos del
evento vas a usar y de dónde sale cada uno.
```

**Te devuelve:** logos extraídos del PDF (SVG + PNG), la paleta real y una composición nueva.
**Tarda:** ~1 h con voz, música y render.

> **Lo que lo hizo funcionar:** pedir el manual antes de construir y decir «solo de
> <marca>» desde el principio. «Con los colores de X» no basta: la estructura heredada
> también se lee como dependencia.

### 2.7 — Una serie de variantes a partir de una secuencia de correos o de una landing

```
Necesito ahora las versiones <recordatorio / es mañana / es hoy>: en <ruta> está
la estructura de los correos que se van a enviar esos días.
```

o, para una landing:

```
Ahora quiero la serie de videos cortos: uno por idea de la landing, cada uno
gancho → valor → CTA con un botón literal de la página.
```

**Te devuelve:** un `serie.py` que genera N proyectos HyperFrames editables en el Studio,
con la voz pedida con semilla fija y cada aparición sobre su palabra.
**Tarda:** ~40 min las voces y la construcción; ~30 s de render por pieza.

> **Cambiar una frase después** cuesta un comando: `python serie.py voz <carpeta>:<n>`
> regenera solo esa frase y `construir` recoloca las escenas. Ojo: `construir` reescribe
> lo editado a mano en el Studio.

### 2.8 — Dejar un proyecto listo para editarlo en la interfaz de HyperFrames

```
Lo quiero editar localmente con la interfaz de HyperFrames.
```

**Te devuelve:** cada escena como sub-composición (una fila en la línea de tiempo), la voz,
los efectos y la música como pistas `<audio>` con la curva de volumen editable, y el Studio
abierto en `localhost:3002`.

# 3 · Audio

### 3.1 — Narración gratuita e ilimitada en español

**Consigues:** locución local, sin cuenta y sin límite de uso.

```
Añade narración en español a <proyecto> con Piper, voz es_ES-davefx-medium.

El guion sale solo de: (a) texto que ya está en pantalla, (b) copia
aprobada de la empresa. Nada más.

Escribe cada línea para que quepa dentro de la duración que ya tiene su
plano — no re-cronometres la animación.
```

**Te devuelve:** un WAV por plano + la mezcla montada + `SCRIPT.md` con la procedencia de
cada frase.
**Tarda:** 10 min.
**Necesitas:** `pip install piper-tts` y los modelos de voz (~60 MB cada uno).

> **La última frase del prompt es la que salva el trabajo.** Si la narración no cabe en el
> plano, hay que re-cronometrar, y eso desincroniza todas las animaciones internas que ya
> estaban ajustadas al segundo.

### 3.2 — Probar voces antes de decidir

```
Genera la misma frase con las voces españolas de Piper que no hemos
probado, y pásame los MP3 para escucharlos.
```

**Por qué:** el modelo no puede oír. La elección de voz es tuya, siempre.

### 3.3 — Efectos y cama musical

```
Añade los efectos de la biblioteca incluida del framework, sincronizados a
los momentos visuales concretos (no de relleno). Y una cama musical con
ducking real por cadena lateral, para que baje cuando entra la voz.
```

**Nota de licencias:** los 19 efectos incluidos son licencia Pixabay — uso comercial, sin
atribución. **MusicGen no sirve para material comercial** (licencia no comercial). Para
música: elige una pista en Pixabay Music y pásala, o sintetiza una cama desde osciladores.

### 3.4 — La mezcla como archivo de configuración

**Consigues:** que el sonido de un módulo nuevo sea editar un JSON, no programar.

```
Monta el sonido de <proyecto> con tools/mezcla.py: escribe
tools/mezcla-<nombre>.json con la cama, cada línea de voz en su segundo y
cada efecto en el instante visual que lo justifica.
```

**Te devuelve:** `assets/mezcla-<nombre>.wav` normalizado a −16 LUFS, con la voz
verificada por espectro (el script **falla** si la banda de voz está vacía).
**Tarda:** 2 min por módulo una vez escrito el JSON.
**Dónde está:** `tools/mezcla.py` en la raíz del repositorio — el script no cambia entre
módulos. Modelo de JSON: `videos/pesv-m01-mando/tools/mezcla-modulo.json`.

### 3.5 — La locución como archivo de configuración

```
Genera la locución de <proyecto> con tools/voz.py a partir de
tools/guion.json. Cada línea con su "maximo" en segundos; si alguna no
cabe, acórtala sin cambiar el sentido y sin salirte del documento.
```

**Te devuelve:** un WAV por línea en `assets/vo/` y la duración de cada una; el script
**falla** si una línea no cabe en su plano.
**Tarda:** ~1 min por módulo. Modelo: `videos/pesv-m01-mando/tools/guion.json`.

### 3.6 — Música propia a un tempo, para videos sin voz

```
Sintetiza una pista rítmica a 120 BPM con tools/ritmo.py para <proyecto>:
más ligera en el arranque, completa desde la segunda escena, una subida
antes de cada cambio de escena y un cierre suave. Mézclala con efectos en
cada golpe y cada transición, con pasa_altos 90, y mide tres bandas.
```

**Te devuelve:** `assets/ritmo-video.wav` y `assets/mezcla-video.wav`, más el balance
por bandas.
**Tarda:** ~2 min. Sin derechos de terceros: es síntesis propia.

> **Por qué «mide tres bandas»:** la primera mezcla tenía los agudos 16 dB por debajo de
> los graves; en un portátil habría sonado a puro bombo. El paso-altos a 90 Hz y bajar los
> impactos lo dejó en −21 / −20 / −22.5 dB. El modelo no puede oír: la medición es su oído.

---

### 3.7 — Una sigla que suena rara o distinta cada vez

```
ElevenLabs no pronuncia bien "<SIGLA>" y en las dos frases la dice distinto.
```

**Qué hace el agente:** genera las dos frases con la misma semilla escribiendo la sigla de
4 maneras, **mide** cuánto dura la sigla en cada frase (alineamiento por carácter) y se queda
con la que dura igual en ambas. Para PESV ganó «pe e ese ve» (0,75 / 0,76 s). Deja los 4 MP3
para que tú elijas de oído y regenera **solo** las frases con la sigla.

# 4 · Verificar

### 4.1 — La verificación de audio que evita un desastre

**Consigues:** saber si la voz está realmente en el archivo, sin escucharlo.

```
Antes de renderizar, verifica el audio partiendo el espectro: mide el nivel
por encima de 400 Hz (ahí vive la voz) y por debajo de 200 Hz. Si la banda
alta está por debajo de -40 dB, la voz no está.
```

> **Esto viene de un fallo real.** Una mezcla midió −11.9 dB de media —nivel perfectamente
> sano en un vúmetro— y sonaba a silencio absoluto: era energía casi toda por debajo de
> 200 Hz. El promedio no detecta ese fallo; el espectro sí, en un segundo.

### 4.2 — Revisar antes de gastar el render

```
Saca capturas en los puntos medios de cada plano y a ±0.1s de cada corte, y
revisa la hoja de contactos antes de renderizar.
```

> **También viene de un fallo real.** Un plano salió completamente en negro y no se habría
> notado hasta ver el MP4 terminado, nueve minutos después.

---

# 5 · Lo que NO funciona

| Intento | Qué pasa | Qué hacer |
|---|---|---|
| Editar HTML con expresiones regulares | Un patrón `<video…>` coincidió dentro de un **comentario** y borró 4 KB de marcado. El plano salió en negro. | Editar con scripts que parseen, y **siempre** re-capturar después |
| Sustituir colores con `sed` sin `-I` | Los agentes escriben `#7a7a7a` en minúsculas; la sustitución en mayúsculas no coincide y el fallo de contraste persiste | `sed -i 's/…/…/gI'` |
| Escribir texto con `Set-Content` de PowerShell | Corrompe los acentos (doble codificación UTF-8) | Escribir con Python o con la herramienta de escritura, nunca con PowerShell |
| Nombrar una fuente sin `@font-face` | El MP4 sale con otra tipografía **en silencio** — el render es un Chrome limpio sin fuentes | Copiar los `.woff2` a `assets/fonts/` y declarar la fuente en cada plano |
| Poner un `<video>` dentro de una sub-composición | El ensamblador lo rechaza | Los `<video>` van en `index.html`, en la raíz |
| Animar `letterSpacing` | El validador lo rechaza: refluye el texto y tiembla bajo el motor de captura | Partir en glifos y animar la `x` de cada uno |
| Citar demasiadas recetas de movimiento en un plano | El paquete supera 48 KB y el constructor falla | Máximo 2–3 recetas por plano con formas grandes |
| Apilar capas de grado sobre una foto (brillo 0.5 + multiply navy 0.82 + velo global) | **La foto desaparece**: queda un campo azul plano, lo contrario de usar fotografía | Menos oscuridad, más desaturación, y un **scrim local** solo bajo el texto |
| Máscara de revelado con ancho fijo más estrecho que la frase | **Recorta palabras en silencio.** En el refactor desapareció «aumentar» del principio clave — cambiaba el sentido. Ni `lint` ni `check` lo detectan | Revisar **cada plano en reposo** con capturas. Ancho útil real: 1920 − margen izq. − margen der. |
| Fiarse de `check` con revelados por máscara | Da decenas de «solapamientos» que no existen: mide la caja del texto oculto sin el recorte | Verificar esos instantes a ojo, declarar **solo** los elementos afectados con `data-layout-allow-overlap`, y luego revisar el reposo |
| Dibujar personas en SVG (monigotes de línea) | El cliente los rechazó: básicos y poco profesionales | Sin figuras humanas: fotografía real o dibujo técnico de objetos |
| Poner `visibility = "visible"` en un hijo animado | Un `visible` explícito **atraviesa** el ocultamiento de su plano: los glifos de la etiqueta del plano 01 seguían vivos debajo de los planos siguientes. Solo lo delató `check` (texto «tapado» en el plano 04) | Revelar con `visibility = "inherit"`, nunca `"visible"`; y nunca animar `visibility`/`display` de un elemento `clip` |
| Espacios en glifos `inline-block` | Se colapsan: «CAPACITACIÓNPESV» | Espacio duro en cada celda de espacio, escrito como `"\u00A0"` en el código |
| Lanzar muchos constructores en paralelo | Los límites de uso los cortan a medias y dejan archivos parciales | Oleadas de 2, que cada uno escriba su archivo pronto, y revisar el disco antes de relanzar |
| Guardar el estado de una animación en un callback (`onUpdate`) | Al saltar hacia atrás el renderizador no lo ejecuta: el rodillo mostraba la palabra equivocada | Pedir que cada paso sea una animación explícita («seek-safe») |
| Calcular a ojo dónde queda cada palabra | Dos píldoras se montaron | Pedir que la fila se ordene sola (flexbox) y animar desde ahí |
| Fiarse del verificador con tarjetas 3D o rodillos | Lee como visible la cara oculta y lo que está fuera de la ventana: decenas de falsos errores | Hacer invisible de verdad lo que no se ve en cada instante |
| Enviar el MP4 master por la sesión | Límite de 30 MB; la fotografía lo supera (el refactor pesa 44.6 MB) | Copia de visualización con `ffmpeg -crf 26` (quedó en 6.9 MB) y el master aparte |

---

# 6 · Datos de producción medidos

| Pieza | Duración | Construcción | Render | Peso |
|---|---|---|---|---|
| Marketing «Sala de control» | 68 s | ~1 día con revisiones | 4 min 44 s | 15.9 MB |
| Marketing, con narración y audio | 68 s | +40 min | 5 min 34 s | 17.5 MB |
| PESV Módulo 01 (base) | 2 min 36 s | ~50 min | 9 min 32 s | 10.7 MB |
| PESV Módulo 01 «plus» — *rechazada* | 3 min 22 s | ~1 h | 9 min 04 s | 19.9 MB |
| PESV Módulo 01 refactor — *«muy básico»* | 2 min 28 s | ~1 h, con muestra previa | 10 min 08 s | 44.6 MB |
| PESV Módulo 01 «Centro de mando» — *dirección aprobada* | 2 min 31 s | muestra 16 s + ~2 h el resto, con voz/efectos/cama | ~9 min 30 s | 39.1 MB (11.4 MB copia de vista) |
| PESV Módulo 01 «Ritmo» — *aprobado sin cambios* | 1 min 00 s | muestra 16 s + ~1 h el resto, pista rítmica y efectos | 4 min 02 s | 15.3 MB |
| FEGIR En Vivo (identidad propia, editable en el Studio) | 21,9 s | ~1 h + ajustes | 36 s | 8,6 MB |
| FEGIR recordatorios (3 variantes generadas) | 3 × 15–19 s | ~40 min | ~30 s c/u | 7–8 MB c/u |
| RiskMann Capacitaciones, promo generado | 39,3 s | ~1,5 h con correcciones | 38 s | 15,3 MB |
| RiskMann Capacitaciones, serie de 4 (reutiliza el promo) | 4 × 15–17 s | ~40 min | ~30 s c/u | 7–8 MB c/u |

**La lectura útil:** el primer video de una serie cuesta un día porque hay que inventar el
sistema. El segundo cuesta una hora porque el sistema ya existe. Ahí está el retorno.

---

*Documento vivo. Cada entrada nueva se añade cuando el prompt se ejecuta, no después.*
