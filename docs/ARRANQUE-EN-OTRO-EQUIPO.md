# Arranque en otro equipo

Todo lo que hace falta instalar y todo lo que ya costó caro aprender, para no
repetirlo. Verificado en el equipo donde se produjo `riskmann-consulta-pesv-vertical`
el 17 de septiembre de 2026.

---

## 1. Qué instalar

### Software base

```bash
winget install --id Gyan.FFmpeg -e                 # 9.0.1
winget install --id oschwartz10612.Poppler -e      # 25.07.0  (leer PDF como imagen)
winget install --id GitHub.cli -e                  # 2.101.0
```

Ya presentes en el equipo original, por si el nuevo no los trae:

| Herramienta | Versión usada |
| --- | --- |
| Node | v24.16.0 (npx 11.13.0) |
| Python | 3.14.5 |
| Git | 2.53.0 |

```bash
python -m pip install numpy      # 2.5.3 — lo necesita tools/ritmo.py
```

> **`pip install` a secas instala en el Python equivocado.** En este equipo `pip`
> apuntaba al Python de la Store y el shell usaba `pythoncore-3.14-64`. Siempre
> `python -m pip`.

> **Poppler no queda en el PATH que winget anuncia.** El binario vive en
> `%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*\poppler-*\Library\bin`.
> Hay que invocarlo por ruta completa o añadirlo al PATH a mano.

### Skills

Las 24 que estaban activas. **No hacen falta más**: en esta producción el
problema nunca fue falta de herramientas.

```
embedded-captions  faceless-explainer  ffmpeg  ffmpeg-media-finishing  figma
general-video  hyperframes  hyperframes-animation  hyperframes-audio
hyperframes-cli  hyperframes-core  hyperframes-creative  hyperframes-keyframes
hyperframes-registry  media-use  motion-graphics  music-to-video  pr-to-video
product-launch-video  remotion-to-hyperframes  slideshow  synced
talking-head-recut  ux-designer
```

```bash
npx hyperframes skills update      # refresca el set base y lo ya instalado
```

Reiniciar la sesión del agente después de instalar skills, o no se cargan.

**Tres que estaban instaladas y se desaprovecharon** — vale la pena usarlas:

- `hyperframes-registry` — ~400 bloques ya hechos y seek-safe. En la v1 se
  dibujó a mano cada barrido y cada destello.
- `hyperframes-keyframes` — cámara, punch-in, match cuts, profundidad 3D.
- `dataviz` — para cifras como el 500 SMMLV o el 70 %.

### Claves y accesos

- `ELEVENLABS_API_KEY` — está en el issue #3. **Caducaba el 21 de septiembre de
  2026**; comprobar antes de contar con ella. Se lee del entorno y **nunca** se
  escribe en un archivo del repo.
- Voz «Carlos» (colombiana): `4PN5DHmrfIgZksvIrawS`, modelo `eleven_multilingual_v2`.
- El CLI de HyperFrames va **fijado por proyecto** (`hyperframes@0.8.42` en
  `package.json`), para que el render se reproduzca igual con el tiempo.

### Dónde NO trabajar

**Fuera de OneDrive.** Durante esta producción OneDrive borró el repo de trabajo
en caliente: pasó de 1556 a 367 y luego a 53 archivos en menos de dos horas, y
se llevó `.git/HEAD`, `.git/config` y toda la base de objetos. Se perdieron los
MP4 entregados y los archivos sueltos de cada carpeta.

Lo que sobrevivió fue lo que estaba en GitHub. **Commit y push temprano y a
menudo** es la única red real.

---

## 2. Errores que ya se pagaron

### Audio y mezcla

Están escritos como ocho lecciones en la cabecera de `tools/mezcla.py`. Las
cuatro que se descubrieron en esta producción:

**La música va en `musica`, nunca en `pistas`.** `pistas` desemboca en el mismo
`amix` que la locución y nada la aparta: en los picos se come la voz. Ese era el
motivo real de que la música tapara al locutor, y no era cuestión de volumen.

**Un TTS no entrega nivel de emisión.** ElevenLabs devuelve la voz a −33 dB de
media; una pista de catálogo viene a −14 dB. **19 dB de desventaja que ningún
ducking compensa.** Se nivela antes, a disco, con `tools/nivelar-voz.py`.

**`loudnorm` no puede ir dentro del `filter_complex`.** Entrega 192 kHz y
desplaza los timestamps, con lo que el `apad`/`atrim` posterior devuelve
**silencio sin dar ningún error ni código de fallo**. Por eso se nivela a disco.

**Rellenar toda rama hasta la duración final antes de mezclar.** Con ramas de 2 s
y de 37 s colgando del mismo `asplit`, ffmpeg acumula búfer hasta atascarse: una
mezcla de 37 s tardó **7 minutos** en vez de 2 segundos.

**El bus frontal puede quedar vacío.** Una versión de solo música no lleva voz ni
efectos, y `amix` con cero entradas **no da error**: deja el grafo colgado y
ffmpeg gira sin terminar nunca. Y sin voz no se aplica ducking, o la música se
agacharía bajo sus propios efectos.

**Una cama de senos suena a silencio en un celular.** Un acorde entre 146 y
440 Hz mide bien en el vúmetro y da −62.7 dB en agudos. Un parlante de teléfono
corta por debajo de 500 Hz.

### Cómo se verifica el audio

Nunca por el nivel general. Siempre:

- **Margen voz–música frase por frase**, extrayendo los dos buses por separado.
  Objetivo: la voz entre **+7 y +25 dB** sobre la música en cada frase. Si se
  pasa de ahí la música se hunde y suena a bombeo.
- **Tres bandas** (graves <200, medios 200–2k, agudos >2k) dentro de ~12 dB:
  ```bash
  ffmpeg -i salida.mp4 -af "highpass=f=2000,volumedetect" -f null -
  ```

### GSAP y HyperFrames

**`expo.in` en las salidas parece tiempo muerto.** Concentra casi todo el
recorrido en el tramo final: una salida de 0.75 s se pasa medio segundo sin que
se note nada y luego pega un tirón. **Usar `power2.in`.** Esta fue la causa de
fondo de la queja de «tiempos muertos», y afectaba a los seis planos.

**GSAP no interpola un `radial-gradient`.** Animar `background` entre dos
gradientes hace visible la caja rectangular del elemento. Se resuelve con capas
apiladas que se cruzan por opacidad.

**Dos `fromTo` sobre el mismo elemento.** El «from» del último se convierte en el
estado de reposo al buscar por tiempo. O se añade `immediateRender: false`, o se
usa `.to` cuando el CSS ya parte del valor correcto (p. ej. una rotación desde 0).

**Dubai necesita `line-height` ≥ 1.5.** Su caja de línea mide ~1.45em; por debajo
de eso las líneas se pisan y el verificador lo marca como texto ilegible.

**Determinismo, sin excepciones.** Nada de `repeat: -1`, `yoyo`, `Math.random()`,
`Date.now()` ni estado en `onUpdate`. El render busca por tiempo y tiene que dar
lo mismo siempre. Una sola timeline pausada por composición, registrada en
`window.__timelines["id"]`.

**Un `<video>` dentro de un comentario CSS** rompe la expresión regular del
ensamblador y se traga la etiqueta buena.

**El Studio anota los archivos** con `data-hf-id` al vuelo. Parar la vista previa
(`npx hyperframes preview --stop`) antes de escribir, o las escrituras fallan por
«archivo modificado».

### El verificador

**No silenciar avisos en bloque.** En la v2 se marcaron 40 errores de
`content_overlap` como intencionales y eran ciertos: los textos quedaban
ilegibles en el render. La forma honesta de comprobar que algo está resuelto es
**retirar las supresiones y ver si el error vuelve**.

`data-layout-allow-overlap` **no se hereda**: hay que ponerlo en el bloque de
texto y también en los `<b>`/`<i>` de dentro.


### Trampas que no dan ningún error (añadidas el 18 de septiembre)

Todas estas pasaron la validación, terminaron el render sin fallo y **solo se
detectaron mirando los fotogramas**. Son la familia más cara de bugs.

**Un elemento elevado a la raíz lleva tiempos GLOBALES y no se mueve con su
plano.** El video aprobado que el ensamblador saca a la raíz del `index.html`
tiene su propio `data-start` absoluto. Al recortar los planos se recolocaron
`el-<plano>` y `el-<plano>-voice` con una expresión regular, pero el elemento se
llamaba `el-s05-prueba-video-4` y no coincidía: quedó anclado al montaje viejo y
entraba 3.3 s tarde, con la tarjeta saliendo vacía en pantalla.
→ Al recolocar planos, **auditar TODOS los `data-start` del index**, no solo los
que siguen el patrón de nombres esperado.

**Ese mismo elemento hereda la escala de su tarjeta pero NO su opacidad.** Al
cerrar el plano todo se desvanecía menos la captura, que se cortaba de golpe a
brillo pleno. Se arregla dándole en la timeline raíz la misma curva de salida
que usa su contenedor.

**El Studio reescribe los archivos mientras la vista previa está abierta.**
Añade atributos `data-hf-id` y normaliza los que ya existen. Un anclaje de texto
que funcionaba deja de coincidir en silencio: el CSS y los tweens entraron, el
bloque HTML no, y **GSAP animando un elemento inexistente no da error**. El
verificador pasó con cero errores y el render salió sin el elemento.
→ Parar la vista previa antes de escribir, y anclar por `id` con expresión
regular, nunca por la línea completa.

**Nunca silenciar avisos del verificador en bloque.** Se marcaron 40 errores de
`content_overlap` como intencionales y eran ciertos: los textos salían
ilegibles. La forma honesta de comprobar que algo está resuelto es **retirar las
supresiones y ver si el error vuelve**.

### Los colores de un manual no siempre pasan el contraste

El manual de Yezid Ricaurte está pensado para papel. Sobre cristal oscuro, su
oliva `#80804a` da **1.75:1** y su tierra `#cdb5a2` da **2.99:1**, contra el
mínimo de 3:1. La solución no es abandonar la paleta: se crean variantes
aclaradas **solo para texto** y el color de marca se conserva intacto en reglas,
acentos y elementos gráficos.

### Página y manual pueden no coincidir

`yezidricaurte.com` usa Cormorant Garamond + Montserrat sobre `#001217` con
escala dorada. Su manual fija Dubai y la paleta verde/tierra. **Son dos sistemas
distintos.** No es un error de nadie: es una decisión que tiene que tomar el
cliente, y hay que planteársela en vez de mezclar mitad y mitad.

### El acento de ElevenLabs es una propiedad de la voz

No hay un parámetro que lo module. Para cambiarlo hay que cambiar de voz:
`tools/probar-voces.py` genera la misma frase con varias para comparar a ciegas.
Ojo: la misma frase dura entre **6.5 y 9.9 s** según la voz, así que cambiarla
obliga a regenerar la locución y recolocar las animaciones.

Y el cuerpo de la petición va en **UTF-8 explícito**: con `curl` y acentos, la
API responde `400 invalid_unicode`. Por eso se manda desde Python.

### OneDrive revirtió el repositorio entero

Además de borrar archivos, el 17 de septiembre **devolvió la carpeta a un estado
de horas antes**: el HEAD local retrocedió seis commits y se perdió un proyecto
completo que nunca se había confirmado. Lo único que salvó el trabajo fue
GitHub.
→ **Clonar fuera de OneDrive, y hacer commit ANTES de renderizar.** Un render
tarda dos minutos; reconstruir un proyecto entero, una hora.

---

## 3. Cómo se mide un «tiempo muerto»

No a ojo. Diferencia entre fotogramas consecutivos, promediada por ventanas:

```bash
ffmpeg -i video.mp4 -vf "tblend=all_mode=difference,signalstats,\
metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -
```

Por debajo de ~0.35 la imagen se lee como parada; 0.0 es un fotograma idéntico
al anterior.

**Dos avisos sobre esta medida**, aprendidos a base de equivocarse:

1. **Promedia todo el cuadro.** Un elemento pequeño moviéndose apenas la mueve.
   Hay que **mirar también los fotogramas**, no solo el número.
2. **Un texto que aparece solo por opacidad casi no cambia píxeles** aunque se
   vea perfectamente. Si hace falta movimiento, que además se desplace.

Lo que de verdad quita tiempos muertos, por orden de impacto:

1. **Recortar cada plano a su locución más una respiración.** En la v1 la voz
   ocupaba 25 de 37.5 s; sobraban 12 s de relleno.
2. **Repartir las salidas** (`power2.in`, no `expo.in`).
3. **Deriva continua del contenido**, con `ease: "none"` — cualquier otra curva
   deja tramos casi quietos. Mueve mucho más que la del fondo, porque el texto
   tiene bordes duros y un degradado suave casi no cambia píxel a píxel.

Resultado en esta pieza: de **44 ventanas muertas de 76** a **19 de 67**, y el
mínimo de 0.008 (fotograma congelado) a 0.120.

---

## 4. Método de producción

**Renderizar el esqueleto antes de montar contenido.** La v2 se construyó así y
destapó dos defectos de arquitectura con 30 líneas de GSAP y cuatro minutos de
render, en vez de con la pieza entera montada.

**La locución manda sobre el montaje.** Se pide con timestamps por carácter
(`/v1/text-to-speech/{id}/with-timestamps`) y cada aparición se coloca sobre la
palabra que la nombra. Nunca se estima.

`tools/voz-eleven.py` **falla si una línea no cabe en su plano**, en vez de que
se descubra en el MP4 final. El tope de cada plano es su corte, no el arranque
de la animación de salida: que la cola de una frase monte sobre la transición es
justo lo que evita que suene a trozos pegados.

**Para una voz más humana:** `stability` 0.32 (no 0.5), `style` 0.45, y la
velocidad afinada por plano. Con 0.5 el modelo lee plano y apresurado.

**Los efectos nunca caen encima de una palabra clave.** El golpe grave del gancho
se adelantó a 1.45 s para dejar sonar «¿Seguro?» a 1.53 s.

### La identidad

**Contra `docs/marca/`, nunca contra lo que hizo la pieza anterior.** La receta
`riskmann-hud` que heredan los proyectos nuevos según `CLAUDE.md` **no
corresponde al manual oficial**. Sigue sin resolverse.

Los PDF están en el repo a propósito: antes vivían solo en Drive, se leían una
vez y sus valores se transcribían a mano a un `frame.md`. Cuando ese archivo se
perdió, la identidad se perdió con él.

`pdftotext` solo saca cadenas. El caballero, los dos anillos concéntricos
cian + dorado y la mezcla de pesos tipográficos dentro de una misma frase **solo
se ven mirando las páginas**, y son lo que define el aire de la marca.

### La regla que manda

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**
Ni cifras, ni afirmaciones normativas, ni nombres de módulo.

> ⚠️ **Sin resolver:** la landing dice «11 o más vehículos» y también «diez (10)
> unidades». La pieza usa once. Hay que confirmar cuál es el umbral y de qué
> norma sale antes de dar la locución por buena.

---

## 5. Comandos del día a día

```bash
# validar SIEMPRE antes de renderizar — 0 errores y 0 avisos
npm run check

npm run render
npx hyperframes preview --background     # vista previa persistente
npx hyperframes preview --status
npx hyperframes preview --stop

# audio, desde la carpeta del proyecto
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14
python ../../tools/mezcla.py tools/etapa-sfx1.json
python ../../tools/mezcla.py tools/final-A.json

# pegar la mezcla al MP4
ffmpeg -i render.mp4 -i assets/mezcla-A.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -ac 2 -shortest salida-A.mp4
```

**Scripts largos a un archivo, no a un heredoc.** Los heredocs de bash se
atragantan pasados ~100 líneas y fallan con «unexpected EOF».

**Cuidado con `print()` y caracteres fuera de cp1252** (flechas, guiones largos):
revientan en la consola de Windows.
