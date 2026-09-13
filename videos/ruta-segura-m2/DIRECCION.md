# Ruta Segura · Módulo 2 — dirección

Segundo video del curso **«Ruta Segura · cada pedaleo cuenta»**. Cubre el
**módulo 2** del PPTX de origen (`diapositiva/actor ciclista ..pptx`, láminas 12
a 18): inspección preoperacional, clasificación de la bicicleta, protección y
visibilidad.

- **Formato:** 1920×1080 · **7:20** · con locución.
- **Identidad, encuadre y reglas de composición:** las mismas del módulo 1. La
  referencia es [`../ruta-segura-m1/DIRECCION.md`](../ruta-segura-m1/DIRECCION.md);
  aquí solo se anota lo propio de este módulo.
- **Procedimiento completo:** §14 de `../../PRODUCCION-VIDEOS.md`.

## Lo que cambió respecto del módulo 1

**La locución se genera antes de componer.** En el módulo 1 las láminas se
escribieron contra una medición con Piper y después se recolocaron sobre la voz
real. Aquí el orden es el correcto desde el principio:

```bash
set ELEVENLABS_API_KEY=...
python tools/voz-eleven.py <voice_id> eleven_v3   # locuta y devuelve los tiempos
copy tools\tiempos-voz.json tools\tiempos-referencia.json
```

Esos tiempos quedan congelados en `tiempos-referencia.json` y son contra los que
se escribieron las marcas de `tools/eNN.py`. Cualquier locución posterior solo
reescribe `tiempos-voz.json`; `tools/cronometro.py` traduce el resto. Por eso ya
no hace falta la medición con Piper: la referencia **es** la voz que se oye.

## Las siete láminas

| Lámina | Qué sostiene el minuto |
|---|---|
| 12 · Apertura | La pregunta, la definición que el módulo descarta («una lista para marcar») y las cinco fallas que obligan a declarar no apta |
| 13 · Ocho puntos | Los ocho puntos entran uno por frase, en el orden exacto en que el narrador los enumera |
| 14 · Decisión | Tres estados —apto, con observación, no apto— y las cuatro acciones que siguen al tercero |
| 15 · Visible a 360° | Tres columnas (casco, ser visto, sin bloquear) que se llenan renglón a renglón |
| 16 · Reto | Dos decisiones con tres salidas cada una |
| 17 · Retroalimentación | Las dos respuestas B y el principio que las une |
| 18 · Repaso | Tres preguntas con su clave debajo |

**Los estados de la lámina 14 no usan verde ni rojo.** La paleta del PPTX no los
tiene, y inventarlos rompería la serie: apto va en cian, con observación en gris
y no apto en oro, que es el color de alerta del curso.

## Trampas nuevas

- **Nunca animar `width`.** La tachadura de las tres excusas de la lámina 12 se
  escribió primero como un `width` que crecía; va con `scaleX` sobre un ancho
  fijo, como el resto de las reglas del proyecto.
- **La tachadura tapa su texto a propósito**, así que el elemento tachado lleva
  `data-layout-allow-occlusion` o el check lo reporta en cada muestra.
- **Bloque de clave debajo de una pregunta:** en la lámina 18 la respuesta a la
  primera pregunta creció a cuatro renglones y se metió bajo el recuadro de la
  segunda. `check` no lo vio —solo toma nueve muestras—; apareció en la captura
  del momento más lleno. Hay que sacar esa captura siempre.
- **`Navigation timeout of 10000 ms`** en `check` cuando la máquina está cargada:
  `PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=120000` delante del comando. `check` no
  tiene bandera `--browser-timeout`; `render` sí.

## Construir

```bash
python tools/construir.py --sin-audio --partes 2
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
npx hyperframes render -c index-parte-2.html -o renders/parte-2.mp4 --quality high --low-memory-mode --workers 1
python tools/pista.py       # assets/voz/modulo-2.mp3, verificada
python tools/montar.py      # une, pega la voz y comprueba duraciones
python tools/guion.py       # GUION-VOZ.md con las ventanas absolutas
```
