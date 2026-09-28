# riskmann-pesv-publicitario

Video publicitario de RiskMann, 8 escenas, **~36 s**, animación por código.

Motor detectado en el repositorio, no asumido: **HyperFrames 0.8.42** sobre
**GSAP 3.14.2**, composiciones en **HTML** con sub-composiciones vía
`data-composition-src`. No hay React ni Remotion: la sintaxis de timeline es la
de GSAP y la de tiempos es la de los atributos `data-*` de HyperFrames.

Los filtros SVG (`feTurbulence`, `feDisplacementMap`, `feGaussianBlur`) **sí
funcionan**: la composición es HTML, así que se usan como `<filter>` en un
`<svg>` embebido o vía `filter:` en CSS.

---

## ⚠️ Conflictos entre el prompt y las reglas del repositorio

El prompt pide cosas que **`CLAUDE.md` y el manual de marca prohíben**. No las
resuelvo por mi cuenta: van aquí para que el cliente decida.

### 1. Figuras humanas — prohibidas

> **Sin figuras humanas dibujadas** (manual de marca §0.2) — `CLAUDE.md`

El prompt las pide dos veces:
- Escena 1: «ícono simple de figura humana (path SVG, línea blanca)»
- Escena 5: «siluetas de manos (paths SVG simples, blancas) revolviendo…»

**Alternativa propuesta:** en la 1, un icono de nodo único aislado frente a una
retícula de nodos conectados —dice «solo» sin dibujar a nadie—. En la 5,
los papeles se revuelven solos por *jitter*, sin manos: el caos se lee igual.

### 2. El logotipo — no se re-letra

> **El logo, solo con el archivo oficial**: nunca redibujado, **re-letrado**,
> recoloreado, deformado ni tapado (§0.1)

El prompt pide en la escena 8 «el logo "Riskmann" (texto wordmark)». Escribirlo
como texto **es re-letrarlo**.

**Alternativa:** se usa `assets/riskmann_logo_blanco.png`, el archivo oficial.
Esto choca con el punto del prompt de que «nada dependa de imágenes externas»,
pero la regla del logo pesa más que la preferencia por vectores.

### 3. Las cifras — tienen que ser rastreables

> **Nada entra al video si no puede rastrearse a un archivo que entregó
> RiskMann.** Ni cifras, ni afirmaciones de cumplimiento normativo… El primer
> video incumplió esto (afirma un «100%» inventado) y por eso la regla está
> escrita aquí.

El prompt pide exactamente eso en la escena 7: «usa valores de ejemplo como
**98%, 24/24, 100%**». Son inventados, y es literalmente el error que originó la
regla.

También hay que respaldar:
- **«24 frentes»** (escena 2) — ¿de dónde sale el 24?
- **«31 de enero»** (escena 3) — ¿qué norma fija esa fecha?

**Sin fuente, no entran.** La escena 7 puede funcionar con las etiquetas sin
número, o con cifras reales en cuanto RiskMann las entregue.

### 4. Paleta — no es la del manual

| Prompt | Manual oficial | |
| --- | --- | --- |
| `#0A4174` azul | `#26367D` institucional · `#333366` tecnológico | distinto |
| `#D93025` rojo | `#FF3333` énfasis y alertas | distinto |
| `#36a23a` verde | **no existe verde en la paleta** | sin equivalente |
| `#000000` negro | `#020202` fondo principal | casi igual |

El verde es el problema serio: RiskMann no tiene uno. El manual reserva
`#c8951a` (dorado, prestigio) y `#06c7fb` (cian, gráficos de acento).

**Propuesta:** el alivio se cuenta con el cian `#06c7fb`, que es el color que el
manual asigna a gráficos y acentos; el dorado marca el cierre de marca.

### 5. Tipografía — el manual fija Dubai

El prompt pide Archivo Black o Inter Black. El manual fija **Dubai** (Bold
títulos, Regular cuerpo), y los archivos ya están en `assets/fonts/`.

Dubai Bold sostiene bien un titular tipo escena 1. **Ojo:** su caja de línea
mide ~1.45em, así que `line-height` nunca por debajo de **1.5** o las líneas se
pisan.


---

## ✅ Fuente encontrada: `docs/marcas/riskmann/fuentes/manejo-pesv-24-pasos.pdf`

Captura de la landing «Manejo del PESV: los 24 pasos sin improvisar». **El guion
del prompt sale literalmente de ahí**, y con él las cifras que estaban sin
respaldo. Esto cierra tres de los cinco conflictos.

### Lo que la página dice, textual

> «Coordinas el PESV de tu empresa **solo**.» · «La norma no debería sentirse así.»
> **«24 pasos. 4 fases. Un reporte anual que vence el 31 de enero.»**
> «Un solo rol, **veinticuatro frentes**»
> «El PESV va a pasar de todas formas. ¿Lo reconstruyes bajo presión, o lo
> consultas en un clic?»
> «Todo en un solo lugar, en tiempo real»
> Respaldo: **Resolución 40595 de 2022**

### Queda resuelto

| Antes sin fuente | Ahora |
| --- | --- |
| «24 frentes» | ✅ «24 pasos. 4 fases.» y «veinticuatro frentes» |
| «31 de enero» | ✅ «Un reporte anual que vence el 31 de enero» |
| El guion entero | ✅ Es la copia de la propia landing, no inventada |

### Una corrección al prompt

Los cuatro frentes de la escena 2 **no son** los que dice el prompt. La página
lista: **Conductores** (en Recursos Humanos) · **Vehículos** (en Mantenimiento) ·
**Siniestros** (en Jurídico) · **Documentos** (en correos y Excel).

El prompt pone «itinerarios» donde la página pone **Siniestros**. Manda la
página.

### Y confirma la paleta

La landing es **negra con acentos dorados** (`#c8951a`), exactamente la del
manual. **No hay azul ni verde en ningún sitio.** Eso resuelve el conflicto 4 a
favor del manual, y ya no es una interpretación mía: es cómo se ve la página que
el video promociona.

El CTA real es **«Quiero registrarme»**, con «Sin tarjeta, sin compromiso.
Empiezas hoy.»

### Lo único que sigue sin fuente

Los números de la escena 7 —el prompt propone 98 %, 24/24, 100 %—. La página
muestra barras de progreso en su mockup (97 %, 65 %, 77 %, 86 %, 115
conductores), pero **son valores de una captura de interfaz, no afirmaciones de
resultado**. Usarlos como «lo que consigues con RiskMann» sería exactamente el
«100 % inventado» que originó la regla.

**Propuesta:** la escena 7 replica el mockup de la página —barras de indicadores
sin prometer nada— en vez de afirmar porcentajes de éxito.

---

## Lo que sí se implementa tal cual

Todo lo demás del prompt: las 8 escenas con su guion exacto, sus tiempos, sus
transiciones y los 7 efectos reutilizables. La voz en off queda como metadata en
cada escena para preparar el montaje con ElevenLabs.

## Estructura

```
compositions/
  components/   tokens.html · efectos reutilizables
  scenes/       scene01-hook.html … scene08-cierre.html
index.html      orquestador: monta las 8 en orden, offsets calculados
```

## Reglas técnicas que manda el repositorio

- Una sola timeline pausada por composición, registrada en `window.__timelines`.
- Determinismo: sin `Math.random()`, `Date.now()`, `repeat: -1` ni `yoyo`. El
  render busca por tiempo. **El «desfase aleatorio» y el «jitter» del prompt se
  implementan con una función hash determinista sobre el índice del elemento**,
  no con `Math.random()`.
- Sin tweens de `width`/`height`/`top`/`left`: solo transformaciones.
- `npm run check` con 0 errores antes de renderizar.
