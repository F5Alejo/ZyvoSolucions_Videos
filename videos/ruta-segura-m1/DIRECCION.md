# Ruta Segura · Módulo 1 — dirección

Primer video del curso **«Ruta Segura · cada pedaleo cuenta»** (trabajadores
ciclistas). Cubre la **apertura + el módulo 1** del PPTX de origen
(`diapositiva/actor ciclista ..pptx`, láminas 1 a 11).

- **Formato:** 1920×1080 · **11:35** · con locución.
- **Voz:** sintética (ElevenLabs, `eleven_v3`). El libreto con la ventana de cada
  lámina está en [`GUION-VOZ.md`](GUION-VOZ.md): sirve para volver a grabarla con
  una persona sin tocar el montaje.
- **Resto del curso:** láminas 12-33 en tres videos más (módulos 2 y 3 y cierre).

## Por qué dura lo que dura

Las notas del PPTX son el guion, y **la duración de cada lámina es la duración de
su narración más ~1,2 s de aire**. Nada se estima: la locución se pide con
timestamps por carácter, así que el instante en que empieza cada frase se lee de
la respuesta.

`tools/cronometro.py` es la pieza que hace esto sostenible. Guarda dos mediciones
—la de referencia (Piper, con la que se compuso) y la de la locución vigente— y
construye un mapa entre ellas: exacto en cada frontera de frase, proporcional
dentro de la frase, desplazamiento fijo en la cola. Con eso **las ochenta y tantas
marcas de tiempo de `tools/eNN.py` se recolocan solas** cuando cambia la voz. No
hay que reescribir ninguna a mano, y el día que la grabe una persona el
procedimiento es el mismo.

El resultado es que **cada aparición en pantalla cae sobre la frase que la
nombra**: los cinco chips de la lámina 2 entran mientras el narrador enumera las
cinco condiciones; las cinco capas de la lámina 6 entran una por capa. Ese es el
único motivo por el que un video de doce minutos se deja ver.

Dos notas del PPTX (láminas 7 y 11) empiezan con el rótulo
`GUION DE VOZ — PRIMERA PERSONA`. No es narración: sus tiempos van corridos
**−2,3 s** y el rótulo no aparece en `GUION-VOZ.md`.

## Identidad

Sale del propio PPTX (colores más usados en las láminas 1-11):

| Uso | Valor |
|---|---|
| Fondo | `#101B33` con radial a `#1E2C4E` |
| Tinta | `#FFFFFF` · secundaria `#AEBCD6` |
| Oro (títulos, escudos, avisos) | `#AC841D` · texto pequeño `#D4A62B` |
| Cian (lo que se aprende, lo que se pide hacer) | `#00C8D4` · texto pequeño `#7FE5EC` |

Tipografía **Montserrat** (archivos reales en `assets/fonts/`). Fotografías:
las tres del propio PPTX (`assets/fotos/`), nunca ilustraciones de personas.
Logo RiskMann: archivo oficial, sin redibujar.

**Encuadre común** (`tools/base.py` → `CHROME_CSS`), idéntico en las once láminas:
ceja a 112, número de lámina arriba a la derecha, título a 150 (máx. dos
renglones, 50 px), regla dorada a 272, contenido desde 296 y línea de fuente
documental a 946. Nada puede invadir esa línea: es el error que más veces
apareció al componer.

El único elemento que le pide algo al espectador es la pastilla cian
**PAUSA EL VIDEO Y RESPONDE**, y solo en las láminas donde la narración lo pide
(1, 2, 5, 8, 9 y 11).

## Cómo se construye

Las composiciones **no se editan a mano**: se generan.

```bash
set ELEVENLABS_API_KEY=...
python tools/voz-eleven.py <voice_id> eleven_v3   # locución + tiempos reales
python tools/construir.py                          # recoloca el video sobre esa voz
python tools/pista.py                              # arma assets/voz/modulo-1.mp3
python tools/guion.py                              # escribe GUION-VOZ.md
npx hyperframes check                              # debe decir "Check passed"
```

**El render va por partes** (§14.4b de `PRODUCCION-VIDEOS.md`): once minutos de una vez no
caben en esta máquina de 8 GB.

```bash
python tools/construir.py --sin-audio --partes 4
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
# ... las cuatro, una por una (~10 min cada una)
python tools/montar.py     # une sin recodificar, pega la voz y verifica duraciones
```

Sin `tools/tiempos-voz.json` todo sigue funcionando: el video se construye con
los tiempos de referencia y sale mudo, que es como se entregó la primera versión.

- `tools/base.py` — paleta, fuentes, encuadre común, envoltura de sub-composición.
- `tools/eNN.py` — una lámina por archivo: su CSS, su cuerpo y su línea de tiempo,
  con la marca de tiempo de la frase que dispara cada aparición en el comentario.
- `tools/construir.py` — encadena las láminas, calcula los inicios y arma el
  `index.html` con la barra de avance, el sello de marca y la pista de voz.
- `tools/cronometro.py` — el mapa entre la locución de referencia y la vigente.
- `tools/voz-eleven.py` — pide la locución con timestamps y escribe `tiempos-voz.json`.
- `tools/pista.py` — coloca cada lámina en su sitio del máster y normaliza a −16 LUFS.
- `tools/narracion.json` — el texto de las once notas, ya sin los rótulos del PPTX.

Las duraciones ya no se escriben: `DUR = cronometro.duracion(LAMINA)`. Cambiar de
voz, o volver a grabar con una persona, es correr `voz-eleven.py` y `construir.py`
otra vez — el resto se recalcula, `GUION-VOZ.md` incluido.

## Trampas que aparecieron aquí

- **Piper falla con comillas angulares.** La frase con `«…»` de la lámina 5 hacía
  que `piper` terminara en código 1 sin escribir el WAV (`wave.Error: # channels
  not specified`). Medir frase por frase, en vez de la nota entera, aísla el
  problema y además da los tiempos que necesita el montaje.
- **`eleven_multilingual_v2` lee las preguntas como afirmaciones.** En español la
  entonación sube al final sin palabra interrogativa y este guion está lleno de
  preguntas. `eleven_v3` las resuelve, habla más pausado y también devuelve
  timestamps — que es lo que hacía falta comprobar antes de cambiar.
- **v3 no acepta `previous_text` / `next_text`** («not yet supported with the
  eleven_v3 model»): el encadenado de entonación entre láminas solo sirve en v2.
- **Las cifras, en palabras.** En estas once láminas solo hay una («Ley 2466 de
  2025»), pero leída como «veinticuatro sesenta y seis» arruina la única
  referencia jurídica del módulo. `voz-eleven.py` la convierte antes de enviarla.
- **El máster de voz, en MP3.** En WAV pesa 61 MB y el navegador no lo carga
  dentro de los 10 s que da `check` antes de la primera muestra: el runtime se
  cae con `Navigation timeout of 10000 ms`.
- **`volumedetect` no imprime nada con `ffmpeg -v error`.** La verificación de que
  la pista no salió muda se quedaba en «?» hasta subir el nivel a `-v info`.
- **El render entero no cabe en 8 GB** y el sistema lo mata. Va por partes, y la
  voz se pega después. Cada render abortado deja además un `ffmpeg` huérfano de
  ~650 MB: hay que matarlo antes de reintentar.
- **Título de dos renglones sobre la regla dorada.** Con 58 px varios títulos
  pasaban a dos renglones y se comían la regla a 246. Se bajó a 50 px, ancho
  1450 y la regla a 272.
- **El pie a 62 % de alfa no pasa AA.** `#ch-fuente` daba 4,24:1 sobre el azul
  noche. Con 80 % pasa.
- **`GSAP target not found` por la cabecera.** Portada y cierre no usan el
  encuadre común: hay que construirlas con `envoltura(..., con_chrome=False)` o
  el check avisa en cada muestra.
- **Etiqueta larga contra su descripción.** «RESPUESTA POSTERIOR» necesitaba
  mover la columna de descripción de 430 a 524 px.
- **`check` solo toma nueve muestras** en doce minutos: no basta. Hay que sacar
  `snapshot` en el momento más lleno de cada lámina (al final, cuando ya entró
  todo) y revisar la hoja de contactos.
