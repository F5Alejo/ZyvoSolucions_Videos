# Ruta Segura · Módulo 4 — dirección

Cuarto y último video del curso. Cubre las láminas 26 a 33 del PPTX: evaluación
final en cuatro partes, compromiso individual, clave de respuestas, cierre y
fuentes.

- **Formato:** 1920×1080 · **7:54** (estimado) · locución **pendiente**.
- **Identidad, encuadre y reglas:** las del módulo 1
  ([`../ruta-segura-m1/DIRECCION.md`](../ruta-segura-m1/DIRECCION.md)).
- **Procedimiento:** §14 de `../../PRODUCCION-VIDEOS.md`.

## Estado: compuesto, sin locutar

Igual que el módulo 3: las láminas se compusieron contra la estimación de
`tools/estimar.py` porque la clave de ElevenLabs expiró. Con una clave nueva,
`voz-eleven.py` + `construir.py` recolocan todo. **No renderizar antes.**

## Las ocho láminas

| Lámina | Qué sostiene el minuto |
|---|---|
| 26 · Evaluación 1/4 | Tres preguntas de selección múltiple, tres opciones cada una |
| 27 · Evaluación 2/4 | Las tres siguientes, misma forma |
| 28 · Evaluación 3/4 | Dos casos de decisión, con lo que la urgencia no cambia |
| 29 · Evaluación 4/4 | Esquema en planta para identificar peligros |
| 30 · Compromiso | La frase a completar, sus cuatro condiciones y los tres niveles |
| 31 · Clave | Las respuestas agrupadas, y por qué todas son B |
| 32 · Cierre | Las cuatro acciones y el límite de lo que la capacitación puede |
| 33 · Fuentes | Dieciséis referencias en tres columnas, con el aviso de vigencia |

## Dos decisiones que conviene no deshacer

**Las dos láminas de selección múltiple comparten generador**
(`tools/evaluacion.py`). Tienen la misma forma y datos distintos; duplicar el CSS
en dos archivos garantiza que en la segunda corrección uno de los dos se quede
atrás. La corrección de altura de banda que hizo falta se aplicó una sola vez.

**La lámina 29 es un esquema, no una ilustración.** La propia narración dice que
la escena es esquemática y que no hay que buscar detalles que no aparecen. Los
vehículos son bloques rotulados, el cruce peatonal es su cebra y **no hay ninguna
figura humana dibujada** (regla de marca §0.2). Los cinco marcadores del esquema
comparten número con la lista de la derecha, para no obligar a buscar.

## Trampas nuevas

- **Tres bandas de 176 px no caben sobre el aviso de pie.** La suma de altos hay
  que hacerla contra la línea de fuente (y=946), no contra el alto del lienzo:
  con bandas de 154 px y paso de 160 px entran las tres.
- **Una lista con un ítem largo no se posiciona en absoluto.** Las referencias de
  la lámina 33 fluyen (`margin-bottom`), no van con `top` calculado: la
  Resolución 20223040040595 ocupa dos renglones y con posiciones fijas se comía
  la siguiente.
- **Un bloque a todo el ancho pisa la columna de al lado.** En la lámina 30 la
  frase sobre los niveles iba a 1664 px de ancho y cruzaba bajo las tarjetas de
  la derecha; se limitó a la columna izquierda.

## Construir

```bash
python tools/estimar.py            # solo mientras no haya locución
python tools/construir.py --sin-audio --partes 2
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
npx hyperframes render -c index-parte-2.html -o renders/parte-2.mp4 --quality high --low-memory-mode --workers 1
python tools/pista.py && python tools/montar.py && python tools/guion.py
```
