# El esqueleto de la lente

Esto es solo la **estructura**: la lente, la cámara y seis bloques de relleno con
el nombre de cada tiempo. Sirve para una única pregunta, antes de invertir nada
en contenido:

> ¿La cámara continua funciona, o sigue pareciendo una sucesión de planos?

Si la respuesta es no, se tira este archivo y se pierde una hora, no la pieza
entera.

## Lo que hay que mirar al verlo

- En **5.5 · 11.0 · 17.0 · 23.0 · 28.5** están los relevos. **No deberías poder
  señalar el instante exacto en que cambia.** Si lo puedes señalar, la
  arquitectura no está funcionando.
- El aro no se apaga, no salta y no cambia de sitio en ningún momento.
- El color del aro cuenta el relato sin que nadie lo explique: cian en reposo,
  rojo en el costo, cian otra vez, dorado en la solución, rojo en el cierre.
- El texto mezcla pesos dentro de la misma frase, como hace el manual.

## Cómo está armado

Tres capas viven los 34 s completos y **nunca** se interrumpen:

| Capa | Qué hace |
| --- | --- |
| `#fondo` | El suelo. Un empuje lentísimo de 1.12 a 1.0 en 34 s. |
| `#ambiente` | El halo que vira de color con el relato. |
| `#lente` | Los tres aros: cian grueso, dorado fino, arco brillante que gira. |

Y `#camara` es un contenedor que se transforma. **Todo el contenido cuelga de
él**; los tiempos no se mueven por su cuenta.

### El mecanismo del relevo

Cada tiempo nace **dentro** del aro (escala 0.55) y sale **pasando por delante
de la cámara** (escala 2.3, desenfoque, opacidad 0). Entre uno y otro hay
**0.55 s de solape**: el siguiente ya está entrando cuando el anterior todavía
no ha terminado de salir. Ese solape es lo único que borra la frontera.

Encima, en cada relevo la lente hace un **iris**: se contrae a 0.74 y vuelve a
abrir con `expo.out`, y el aro engorda de 22 a 30 px. Es el gesto que lleva el
ojo de una idea a la siguiente.

### Decisiones que no son cosméticas

- **Una sola composición.** Nada de seis sub-composiciones con `data-start`
  consecutivos: eso es un corte, por mucho que se decore la salida. Era el
  error de arquitectura de la v1.
- **El solape está declarado, no corregido.** El verificador marcó 40 errores de
  `content_overlap` entre tiempos consecutivos. Son el mecanismo, así que van
  con `data-layout-allow-overlap` — y el atributo hay que ponerlo en el bloque
  de texto y en los `<b>`/`<i>`, no en el contenedor: no se hereda.
- **El giro va con `.to`, no con `fromTo`.** Dos `fromTo` sobre `#lente` dejan
  que el «from» del último se convierta en el estado de reposo del elemento al
  buscar por tiempo. El CSS ya parte de 0, así que `.to` basta. Misma trampa que
  mordió en la v1.
- **Sin `repeat: -1`, sin `yoyo`, sin estado en `onUpdate`.** El giro del arco
  es un único tween finito de 360° en 34 s. El render busca por tiempo y tiene
  que dar lo mismo siempre.

## Lo que falta

Todo el contenido. Cuando este esqueleto se apruebe, cada tiempo se rellena
según `STORYBOARD.md`, y se retira `#sello`.

Sigue pendiente, sin decidir: el umbral de vehículos (la landing dice once y
también diez), los derechos en video de la imagen del caballero, y la clave de
ElevenLabs, que caduca el 21 de septiembre.
