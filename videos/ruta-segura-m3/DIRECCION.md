# Ruta Segura · Módulo 3 — dirección

Tercer video del curso **«Ruta Segura · cada pedaleo cuenta»**. Cubre el **módulo
3** del PPTX de origen (láminas 19 a 25): anticipación, maniobra, inspección de
ruta y estado personal, y respuesta ante un siniestro.

- **Formato:** 1920×1080 · **7:08** · con locución.
- **Identidad, encuadre y reglas:** las del módulo 1
  ([`../ruta-segura-m1/DIRECCION.md`](../ruta-segura-m1/DIRECCION.md)).
- **Procedimiento:** §14 de `../../PRODUCCION-VIDEOS.md`.

## La locución

Voz colombiana de ElevenLabs: «Carlos» (`4PN5DHmrfIgZksvIrawS`), modelo
`eleven_v3`. Las láminas se compusieron primero contra una estimación
(`tools/estimar.py`, ajustada sobre las frases ya locutadas de los módulos 1 y 2)
y después `tools/cronometro.py` recolocó todas las marcas sobre los tiempos
reales, exacto en cada frontera de frase. No hubo que tocar ningún `eNN.py`.

Para regrabar con una persona: `GUION-VOZ.md` trae la ventana de cada lámina. Se
vuelve a renderizar, pero no se toca ninguna animación.

## Las siete láminas

| Lámina | Qué sostiene el minuto |
|---|---|
| 19 · Apertura | Ver, ser visto y confirmar son tres cosas distintas; el barrido del vehículo pesado al girar |
| 20 · Cinco pasos | Observar → anticipar → señalizar → verificar → ejecutar, encadenados con flecha, uno por frase |
| 21 · Ruta y estado | Matriz de ruta a la izquierda, semáforo de aptitud a la derecha |
| 22 · Caso integrador | Cuatro señales de alerta que por separado no parecen motivo para detenerse |
| 23 · Reto | Dos decisiones de anticipación |
| 24 · Retroalimentación | Las dos respuestas B y la cadena Proteger → Alertar → Socorrer → Reportar |
| 25 · Repaso | Tres preguntas con su clave |

## El semáforo de aptitud es la excepción de color

Es el único punto de la serie donde entran verde, ámbar y rojo. **No son colores
de marca inventados**: el documento fuente define el estado *por* su color, así
que el color es el contenido. Van solo en el punto luminoso
(`#2FBF71` / `#E3A81B` / `#DE4D4D`); los rótulos y las descripciones siguen en la
paleta del curso. En el módulo 2 la clasificación apto / con observación / no
apta **no** lleva semáforo, porque allí el documento nombra estados, no colores.

## Trampas nuevas

- **El recuadro del estado rojo se desborda por abajo.** Su descripción es la más
  larga de la lámina (seis condiciones) y a 96 px de alto el texto se salía 9,7 px.
  Con 104 px y 116 px de paso entre tarjetas, cabe.
- **La lámina 22 tiene cinco acciones en una fila**: hay que medir los anchos de
  texto antes de repartir los `left`, no repartirlos a intervalos iguales.

## Construir

```bash
python tools/estimar.py            # solo mientras no haya locución
python tools/construir.py --sin-audio --partes 2
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
npx hyperframes render -c index-parte-2.html -o renders/parte-2.mp4 --quality high --low-memory-mode --workers 1
python tools/pista.py
python tools/montar.py
python tools/guion.py
```
