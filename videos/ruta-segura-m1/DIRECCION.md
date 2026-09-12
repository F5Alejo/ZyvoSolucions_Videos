# Ruta Segura · Módulo 1 — dirección

Primer video del curso **«Ruta Segura · cada pedaleo cuenta»** (trabajadores
ciclistas). Cubre la **apertura + el módulo 1** del PPTX de origen
(`diapositiva/actor ciclista ..pptx`, láminas 1 a 11).

- **Formato:** 1920×1080 · **11:47** · **sin voz**.
- **Voz:** se graba después, en Colombia, siguiendo [`GUION-VOZ.md`](GUION-VOZ.md).
- **Resto del curso:** láminas 12-33 en tres videos más (módulos 2 y 3 y cierre).

## Por qué dura lo que dura

Las notas del PPTX son el guion. Cada nota se sintetizó frase por frase con
Piper (`es_ES-davefx-medium`, ~130 palabras/minuto) y **la duración de cada
lámina es la duración de su narración más ~1,2 s de aire**. Las mediciones están
en `tools/tiempos-medidos.json`; el guion con ventanas absolutas se genera con
`python tools/guion.py`.

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
python tools/construir.py    # escribe compositions/*.html y index.html
python tools/guion.py        # escribe GUION-VOZ.md
npx hyperframes check        # debe decir "Check passed"
npx hyperframes render --quality high --browser-timeout 240
```

- `tools/base.py` — paleta, fuentes, encuadre común, envoltura de sub-composición.
- `tools/eNN.py` — una lámina por archivo: su CSS, su cuerpo y su línea de tiempo,
  con la marca de tiempo de la frase que dispara cada aparición en el comentario.
- `tools/construir.py` — encadena las láminas, calcula los inicios y arma el
  `index.html` con la barra de avance y el sello de marca.

Para mover una lámina basta cambiar `DUR` en su archivo: `construir.py` recalcula
todos los inicios y las marcas de la barra. Después hay que regenerar
`GUION-VOZ.md` (y actualizar `LAMINAS` en `tools/guion.py` si cambió una duración).

## Trampas que aparecieron aquí

- **Piper falla con comillas angulares.** La frase con `«…»` de la lámina 5 hacía
  que `piper` terminara en código 1 sin escribir el WAV (`wave.Error: # channels
  not specified`). Medir frase por frase, en vez de la nota entera, aísla el
  problema y además da los tiempos que necesita el montaje.
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
