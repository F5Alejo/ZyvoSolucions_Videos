# Dirección — PESV Módulo 01 · «Ritmo» (60 s, sin voz)

## El pulso manda

**120 BPM → 1 pulso = 0.5 s, 1 compás = 2 s.** Toda entrada, marca y transición cae en
un múltiplo de 0.5 s. Cada escena empieza en frontera de compás. Constantes en cada
escena: `const P = 0.5; const B = n => n * P;` (tiempo local).

| Escena | Archivo | Inicio | Dura | Contenido (del documento) | Técnica principal |
|---|---|---|---|---|---|
| 01 | `s01-gancho` | 0 | 8 | «Tú no conduces. / Pero decides.» | Tipografía que golpea al compás (entradas distintas) + tachón y círculo a mano; el círculo se expande en iris |
| 02 | `s02-corresponsable` | 8 | 8 | «No manejar no significa ser un actor pasivo.» · «La seguridad también viaja en el asiento del pasajero.» | Cascada de entrada + subrayado marcador + tarjeta que se transforma de píldora a foto |
| 03 | `s03-roles` | 16 | 10 | «Todos los colaboradores, sin importar el cargo.» · peatón, ciclista, motociclista, conductor, pasajero | Palabras que llegan desde la profundidad 3D y se ordenan; PASAJERO crece en rojo; cinta de texto continua |
| 04 | `s04-deberes` | 26 | 12 | Exigir condiciones seguras, sin confrontar · Cumplir cinturón, postura y protocolos · Advertir, solicitar corrección y reportar | Tres tarjetas que giran en 3D por turno |
| 05 | `s05-principio` | 38 | 8 | «Cada decisión del pasajero puede aumentar o reducir la exposición al riesgo.» | Rodillo tipo tragamonedas AUMENTAR ⇄ REDUCIR |
| 06 | `s06-ruta` | 46 | 8 | Módulo 01 de 8 · los 8 nombres | Barra que se llena + nombres en rodillo |
| 07 | `s07-cierre` | 54 | 6 | «Pasajero seguro. Decidir bien también es conducir la seguridad.» + pie legal | El logo se revela; fundido final |

## Paleta (la de las diapositivas del documento)

`#F5F8FC` papel · `#0B2F6B` marino (texto y bloques) · `#1565C0` azul · `#5AA7E8` celeste ·
`#B7D3EF` regla · `#E6423C` rojo RiskMann (**un solo foco por escena**) · `#FFFFFF` sobre marino.
Montserrat variable: 900 para los golpes, 700 titulares, 500 apoyo.

## Cromo persistente (en `index.html`, sobre todas las escenas)

- **Firma**: píldora blanca abajo a la izquierda con `riskmann_logo_color.png` (archivo
  oficial, escala uniforme). Se lee sobre papel y sobre marino.
- **Barra de progreso rítmica** abajo: se llena de 0 a 100 % en 60 s con un tic en cada
  frontera de escena.

## Salidas (cada escena cierra tapando la pantalla con el fondo de la siguiente)

01 → iris desde el círculo · 02 → bloques verticales alternados · 03 → barrido diagonal ·
04 → barrido con estela + panel que empuja · 05 → la ventana del rodillo crece hasta llenar ·
06 → persianas horizontales · 07 → único fundido de la pieza.

## Reglas

- **Nada de estado en `onUpdate`**: el renderizador salta en el tiempo y ese callback no se
  ejecuta al retroceder. El rodillo mostró la palabra equivocada por eso. Cada paso es un
  `fromTo` explícito; los desenfoques se animan con `attr: { stdDeviation }`.
- Lo que no se ve se hace invisible de verdad (cara oculta de una tarjeta, palabras del
  rodillo fuera de la ventana): el verificador no entiende `backface-visibility` ni el recorte.
- Filas de elementos: que las ordene flexbox y animar desde su lugar natural; calcular
  posiciones a ojo hizo que dos píldoras se montaran.

- Nada rebota como entrada por defecto (`power4` / `expo` / `circ`); `back.out` solo en
  acentos (el círculo a mano).
- Transformaciones y pintura solamente; nunca `width`/`height`/`letterSpacing`.
- Nunca `visibility = "visible"` en hijos (usar `inherit`); nunca animar `visibility` de un `clip`.
- Todo el contenido por encima de y = 900 salvo el cromo.
