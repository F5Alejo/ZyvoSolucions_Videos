---
version: alpha
name: RiskMann — Manual Oficial (frame layer)
description: >
  Frame layer construido DESDE CERO a partir del manual de identidad oficial de RiskMann
  (PDF "Manual-de-identidad.pdf" y "Manual-de-identidad - Modo Oscuro.pdf", Google Drive,
  carpeta RiskMann-by-SOFU/Manuales de Identidad). NO hereda del recipe `riskmann-hud`
  usado en el resto de la serie de videos (Montserrat + azul marino #051427 + rojo #E6423C
  + lavanda #8E8FC4) — ese recipe no corresponde al manual real, ver "Nota de origen"
  abajo. Este proyecto usa exclusivamente los valores que el PDF documenta.
unit: the frame — 1920×1080 primary
principle: solo los valores del manual · nada inventado · estructuras sólidas, no adornos

colors:
  bg: "#020202"
  surface: "#272725"
  surface-2: "#26367D"
  primary: "#FF3333"
  accent-tech: "#333366"
  accent-blue: "#336699"
  accent-gold: "#c8951a"
  accent-cyan: "#06c7fb"
  text: "#FFFFFF"
  text-muted: "#999999"
  border: "rgba(51, 102, 153, 0.35)"
  card-bg: "rgba(255, 255, 255, 0.04)"
  grid: "rgba(51, 51, 102, 0.16)"
  glow: "rgba(255, 51, 51, 0.35)"
  positive: "#06c7fb"
  negative: "#FF3333"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  body:      { fontFamily: "Dubai", fontWeight: "Regular", cqw: 0.85, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Dubai", fontWeight: "Medium", cqw: 0.8, tracking: "0.08em", upper: true, color: "accent-cyan" }
  tag:       { fontFamily: "Dubai", fontWeight: "Medium", px: 12, color: "primary" }
  counter:   { fontFamily: "Dubai", fontWeight: "Regular", px: 13, tracking: "0.05em", color: "text-muted" }
  h3:        { fontFamily: "Dubai", fontWeight: "Bold", cqw: 1.25, lineHeight: 1.3, tracking: "-0.01em", color: "text" }
  stat-num:  { fontFamily: "Dubai", fontWeight: "Bold", cqw: 1.9, lineHeight: 1.0, color: "primary" }
  h2:        { fontFamily: "Dubai", fontWeight: "Bold", cqw: 2.6, lineHeight: 1.1, tracking: "-0.01em", color: "text" }
  metric-value:{ fontFamily: "Dubai", fontWeight: "Bold", cqw: 3.0, lineHeight: 1.0, color: "accent-cyan" }
  h1:        { fontFamily: "Dubai", fontWeight: "Bold", cqw: 4.2, lineHeight: 1.08, tracking: "-0.01em", color: "text" }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "Panel universal de contenido. Nunca color sólido, nunca sombra — la estructura sólida del manual se lee por contorno, no por profundidad."
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.accent-cyan}) + label en {typography.tag}"
    description: "Cifra hero. El cian es el color de 'gráficos acento' del manual — ahí es donde vive un dato."
  tag-pill:
    backgroundColor: "rgba(255, 51, 51, 0.12)"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "Chrome secundario, arriba a la derecha del header de un plano."
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    rounded: "{radii.pill}"
    typography: "Dubai Bold"
    shadow: "none"
    description: "El único elemento sólido — 'énfasis, alertas, botones' es literalmente el uso sugerido del rojo #FF3333 en el manual."
  accent-line:
    backgroundColor: "{colors.accent-gold}"
    size: "60×4, 2px radius"
    description: "Sobre eyebrows / separadores de sección. El dorado es 'toques de prestigio y detalles' — se usa con moderación, nunca como acento principal."
  panel-frame:
    border: "1.5px solid {colors.border}"
    cornerMarks: "4 marcas en L, 2px, color {colors.accent-tech} al 0.5 de opacidad, 48px de brazo"
    description: "Motivo estructural del plano — 'estructuras sólidas' y metáforas de protección del manual, sin dibujar literalmente un escudo o caballero. Reemplaza la retícula HUD heredada del recipe anterior."
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    rounded: "50%"
    size: "56px"
    description: "Pasos secuenciales (p.ej. los 24 pasos del PESV), opacidad 1.0→0.85→0.7→0.55."
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px, borde inferior, ancho crece con el índice"
    description: "Franja de progreso persistente."
---

# RiskMann — Manual Oficial (frame layer)

## Nota de origen (léela antes de tocar nada)

Este `frame.md` reemplaza al recipe `riskmann-hud` que usa el resto de la serie
(`videos/riskmann-sala-de-control/`, `pesv-m01-mando/`, `ruta-segura-*/`, etc.):
Montserrat + `bg #051427` (azul marino) + `primary #E6423C` (rojo) + `accent-2 #8E8FC4`
(lavanda). Al cruzar esos valores contra el manual real (`RiskMann Manual-de-identidad.pdf`
y su versión Modo Oscuro, Google Drive → RiskMann-by-SOFU → Manuales de Identidad),
**ninguno de esos cuatro valores aparece en el manual**, y la tipografía del manual es
**Dubai** (Bold en títulos, Regular en cuerpo), no Montserrat. Por instrucción explícita
del cliente (2026-09-16), este proyecto usa el manual real en vez del recipe heredado. La
discrepancia en la serie anterior queda reportada aparte, sin corregir retroactivamente
aquí.

Valores tomados literalmente de las tablas "Colores Generales" / "Paleta de Colores de
Isotipo" de ambos PDF:

| Hex | Uso sugerido en el manual | Rol en este frame.md |
| --- | --- | --- |
| `#020202` | Fondo principal | `bg` |
| `#272725` | Separadores, fondos secundarios | `surface` |
| `#26367D` | Color institucional secundario o de soporte | `surface-2` |
| `#FF3333` | Énfasis, alertas, botones | `primary` |
| `#333366` | Círculos del isotipo, elementos tecnológicos | `accent-tech` |
| `#336699` | (paleta del manual, modo claro) | `accent-blue` / base de `border` |
| `#c8951a` | Toques de prestigio y detalles | `accent-gold` |
| `#06c7fb` | Detalles decorativos, gráficos acento | `accent-cyan` |
| `#999999` | Contraste, espacios negativos | `text-muted` |

Ningún hex en este archivo está inventado o aproximado — cada uno viene de una de esas dos
tablas. `border`, `card-bg`, `grid` y `glow` son las únicas derivadas (transparencias sobre
los hex de arriba), como exige `hyperframes-core` para chrome estructural no sólido.

## Identidad visual (manual, resumen para diseño de plano)

El manual describe el estilo como "seguridad, prestigio y liderazgo", inspirado en
caballeros medievales: protección, integridad, compromiso. Traducido a un frame sin dibujar
literalmente un escudo o un caballero:

- **Estructura antes que adorno.** Paneles con contorno de 1.5px (`border`), nunca sombra.
  El motivo `panel-frame` (marcas de esquina en L) es la única cita visual a "estructuras
  sólidas" — deliberadamente discreto.
- **Un solo acento fuerte por plano: el rojo `#FF3333`.** Es literalmente "énfasis, alertas,
  botones" en el manual — resérvalo para el CTA, una cifra crítica o un solo elemento en
  foco. Nunca dos rojos compitiendo en el mismo plano.
- **El dorado (`#c8951a`) es prestigio, no decoración de fondo.** Úsalo en una línea de
  acento o un detalle puntual — nunca como relleno ni como segundo acento compitiendo con
  el rojo.
- **El cian (`#06c7fb`) es donde vive un dato.** El manual lo define como "gráficos
  acento" — es el color de las cifras hero (`metric-value`) y de elementos de
  visualización de datos, no de texto de cuerpo.
- **Tipografía: Dubai, sin excepción.** Bold para todo titular/cifra, Regular para cuerpo,
  Medium para chrome (eyebrows, tags). Los `.ttf` están en `assets/fonts/` (copiados del
  sistema — Dubai es la fuente que Microsoft distribuye con Windows/Office; se usa aquí
  solo para renderizar el video, nunca se redistribuye el archivo de fuente).

## Zona libre inferior y densidad

Se mantienen las reglas técnicas duras del repo (`PRODUCCION-VIDEOS.md` §5), independientes
de qué manual de marca se use: 17% inferior libre de contenido importante, elemento
principal ≥40% del lienzo, mínimo 3 capas de profundidad, curvas `power3` sin rebote.
