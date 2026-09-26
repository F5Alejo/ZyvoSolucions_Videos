# RiskMann · Landing «Inspecciones gratis» — 3 anuncios de 12 s

**Fuente única:** <https://riskmann.com/inspecciones-gratis/> (leída el 2026-09-23). Cada frase del guion
y del lienzo sale de esa página: «Inspección preoperacional · 100% gratis», «desde el celular», «en
minutos», «papel, WhatsApp y hojas de cálculo», «novedades pendientes», «quién inspeccionó y cuándo»,
Apto / Con control específico / No apto, «revisión técnico‑mecánica», «Paso 16 · Resolución
20223040040595 de 2022», «Sin tarjeta de crédito», «Aplica para todos los niveles», «Quiero mi
inspección gratis». No hay cifras inventadas.

> El documento del storyboard «LANDING INSPECCIONES GRATIS» no está ni en el repo ni en el Drive
> conectado. Los guiones siguen el ángulo que pide cada anuncio y el texto de la landing. Si el
> storyboard trae frases literales distintas, se cambian en `js/ads.js → SCRIPTS` y en el HTML.

Formato: **1080×1920 (9:16) · 12 s · estructura `{ hook: 0.0, valor: 2.0, cta: 8.0 }`**.
Preview: `python -m http.server 5510 --directory videos/riskmann-inspecciones-ads` → <http://localhost:5510/?ad=1>

---

## Agente 1 · Ingeniería de puntuación para ElevenLabs

**Voz:** «Carlos» `4PN5DHmrfIgZksvIrawS` · **modelo** `eleven_v3` · ajustes «vendedor máximo», ya
aprobados en `ENTREGABLES-VIDEO/prueba-voz-carlos`: `stability 0.15 · style 0.78 · speed 1.03`.

Lo que ya midió el equipo (`ENTREGABLES-VIDEO/prueba-puntuacion/LEEME.txt`) y cómo se aplica aquí:

| Recurso | Medido | Uso en estos guiones |
| --- | --- | --- |
| `…` puntos suspensivos | 0.64 s de silencio: **la mejor pausa** | Todas las pausas dramáticas |
| `—` guion largo | 0.57 s: peor pausa que `…` | Solo en el AD 1, porque el brief lo pide antes de «¿Cuándo…?» |
| `P-E-S-V` deletreado | la sigla pasa de 0.49 a 0.95 s y se entiende | AD 3 |
| MAYÚSCULAS | `eleven_v3` las acentúa | Una palabra por anuncio: TODOS · PENDIENTE · EXPUESTA · HOY |
| `[etiqueta]` | etiquetas de audio de `eleven_v3` | Tono de cada tramo; `multilingual_v2` las leería en voz alta: quítalas |

### AD 1 · Autodiagnóstico

```text
[decidido] ¿Inspeccionas TODOS tus vehículos?
— ¿Cuándo fue la última vez… que revisaste una a tiempo? — Con RiskMann… la haces desde el celular. ¡En MINUTOS!
Gratis, sin tarjeta. ¡Regístrate HOY!
```

### AD 2 · Consecuencia (problema hasta el segundo 8, alivio en el CTA)

```text
[frustrado] Papel. Excel. WhatsApp.
Y el vehículo… sigue rodando. Con una novedad PENDIENTE. ¿Quién lo inspeccionó? ¿Cuándo?… Nadie lo sabe.
[aliviado] Tranquilo… RiskMann lo centraliza todo. Gratis. ¡Regístrate hoy!
```

Para que el cambio de tono sea limpio, genera el CTA como **segunda llamada** con
`stability 0.35` (más cálido) y únelo en el 8.0 s.

### AD 3 · Urgencia (pausas antes de revelar la exposición)

```text
[serio] ¿Tu técnico-mecánica… al día?
¿Y la inspección diaria que exige el P-E-S-V? … … Sin ese registro… tu empresa queda… EXPUESTA.
[firme] RiskMann la registra gratis. ¡Regístrate HOY!
```

**Presupuesto de tiempo** (Carlos a speed 1.03 ≈ 3 palabras/s): hook ≤ 5 palabras, valor ≤ 18,
CTA ≤ 8. Si una toma se pasa de 12.0 s, recorta en el valor, no en el CTA.

---

## [STORYBOARD TIMELINE]

### AD 1 · Autodiagnóstico

| s | Evento visual | Voz |
| --- | --- | --- |
| **0–2 HOOK** | Eyebrow entra (power4.out). Cascada «¿Inspeccionas / **TODOS** / tus vehículos?», TODOS a 280 px en rojo con pop 1.6→1. Fondo: tensión roja leve. | ¿Inspeccionas TODOS…? |
| 1.78 | El hook sale hacia arriba (power4.in). | — |
| **2–8 VALOR** 2.00 | Destello del fondo. **El reloj SVG se dibuja** (stroke‑dashoffset 1→0): aro, aro interior, 12 marcas en cascada. | — ¿Cuándo fue la última vez…? |
| 2.60 | Agujas con back.out(1.5), giran 720°; el líquido se retuerce (warp ↑). | |
| 4.40 | El reloj se encoge a la izquierda; sube la tarjeta Glassmorphism del celular; el fondo pasa de rojo a cian. | Con RiskMann… desde el celular |
| 4.85–6.8 | Los 3 pasos de la landing en cascada; checks trazados en 5.6 / 6.2 / 6.8; barrido de brillo; flotación en Y. | |
| 7.10 | Sello «EN MINUTOS» (back.out). | ¡En MINUTOS! |
| **8–12 CTA** 8.00 | **Spectacle beat:** «REGÍSTRATE HOY» 1.5→1.0 con `back.out(4)` (baja a ~0.86 y rebota), drop‑shadow rojo 0→80 px→26 px que respira, sacudida del lienzo, destello y zoom del fondo. | Gratis, sin tarjeta. |
| 8.55–9.35 | Botón «Quiero mi inspección gratis» (late), «Gratis · Sin tarjeta de crédito», logo, URL. | ¡Regístrate HOY! |

### AD 2 · Consecuencia

| s | Evento visual | Voz |
| --- | --- | --- |
| **0–2 HOOK** | Tarjetas Papel (0.05) / Excel (0.45) / WhatsApp (0.85), una por palabra, back.out. Fondo rojo. | Papel. Excel. WhatsApp. |
| **2–8 VALOR** 2.00 | «El vehículo sigue rodando…» en cascada. | Y el vehículo… sigue rodando. |
| 3.10 | «con una novedad pendiente.» en rojo; tensión al máximo; las tarjetas tiemblan. | Con una novedad PENDIENTE. |
| 3.40 | Grietas rojas trazadas sobre cada tarjeta. | |
| 4.40 | «¿Quién lo inspeccionó? ¿Cuándo?» | ¿Quién…? ¿Cuándo?… |
| 5.50 | **Quiebre:** cada tarjeta estalla en 8 esquirlas (clip‑path); destello. | Nadie lo sabe. |
| 6.00–7.4 | «Todo en un solo lugar.» + interfaz móvil Glassmorphism con barrido de brillo; Apto / Con control específico / No apto en cascada; el fondo vira a cian; flotación. | *(silencio de la voz → la imagen adelanta el alivio)* |
| **8–12 CTA** | Spectacle beat idéntico + «Todo en un solo lugar · Gratis». | [aliviado] Tranquilo… ¡Regístrate hoy! |

### AD 3 · Urgencia

| s | Evento visual | Voz |
| --- | --- | --- |
| **0–2 HOOK** | «¿Tu técnico‑mecánica… **al día?**» (rojo, pop). Tarjeta glass «Hoja de vida del vehículo»: SOAT / Revisión técnico‑mecánica / Inspección de hoy con «?» dorados que laten. | ¿Tu técnico‑mecánica… al día? |
| **2–8 VALOR** 2.00 | «El PESV exige registrar la inspección…» | ¿Y la inspección diaria que exige el P‑E‑S‑V? |
| 3.00–3.7 | «todos los días.» + línea dorada + píldora «Resolución 20223040040595 de 2022 · Paso 16». | |
| 4.60 | **Pausa:** el texto sale; el fondo se tensa en silencio. | … … |
| 4.90 | «Sin registro… tu empresa queda» | Sin ese registro… tu empresa queda… |
| 5.70 | **«EXPUESTA»** golpea 2.2→1 con sacudida y destello rojo. | EXPUESTA. |
| 6.20–7.4 | El texto sube; **el escudo se ensambla** en 6 piezas (back.out, stagger 0.1); contorno cian y check trazados; «PESV · Paso 16». Fondo a cian. | |
| **8–12 CTA** | Spectacle beat + «Aplica para todos los niveles del PESV». | RiskMann la registra gratis. ¡Regístrate HOY! |

---

## Agente 2 · Código

| Archivo | Qué hace |
| --- | --- |
| `index.html` | Lienzo 1080×1920 con las 3 composiciones (`data-composition-id`) + panel de control |
| `js/bg.js` | Three.js: mesh gradient líquido (fbm con domain warping) con la paleta del manual. Reacciona a `bgState` (`heat`, `calm`, `pulse`, `warp`, `zoom`), que animan los timelines |
| `js/ads.js` | `videoTimelines`, los guiones, y un timeline GSAP **en pausa** por anuncio, registrado en `window.__timelines` |
| `js/main.js` | Reproductor: un solo reloj (el MP3 si existe, si no el de pared) que mueve el timeline y el shader |
| `css/stage.css` | Identidad: Dubai, `#020202`, `#FF3333`, `#06c7fb`, `#c8951a`; glassmorphism |

**Reglas físicas implementadas:** entradas solo con `power4.out` o `back.out(1.5)` (el único `none` es
la barra de progreso); textos de hook y valor en cascada (`stagger`); flotación en Y con repeticiones
contadas (seek‑safe); spectacle beat en 8.0 s.

### Dónde inyectar el audio final

1. Deja los MP3 en `assets/voz/ad1.mp3`, `ad2.mp3`, `ad3.mp3` (y opcionalmente `assets/musica.mp3`).
   El reproductor los detecta solo y usa la voz como reloj maestro. `assets/voz/` no va en git.
2. Para HyperFrames, cada anuncio lleva
   `<audio src="assets/voz/adN.mp3" data-start="0" data-duration="12" data-track-index="10" data-volume="1">`
   (comentado en `index.html`). Mezcla voz + música + SFX con `tools/mezcla.py` como en la pieza PESV
   (verifica por bandas: agudos por encima de −45 dB o en el celular no se oye).
3. La clave de ElevenLabs del issue #3 caducó el 21 de septiembre: se necesita una nueva.

### Dónde van los assets de marca

- Logo oficial: `assets/riskmann_logo_blanco.png` (copiado de `assets/public/`). Solo se escala.
- Icono del módulo: `assets/icono_inspecciones.webp` (de `assets/img/seguridad_vial_icono_inspecciones.webp`).
- Tipografía: `assets/fonts/DUBAI-*.TTF`.
- Iconos de papel, Excel y chat: pictogramas genéricos dibujados en SVG, **no** los logos de Microsoft
  ni de WhatsApp.

## V2 · el rojo solo significa peligro

| Elemento | V1 | V2 | Por qué |
| --- | --- | --- | --- |
| «TODOS» (AD 1), «al día?» (AD 3) | rojo | **dorado** `#c8951a` | Llaman la atención, no son peligro |
| «REGÍSTRATE **HOY**», su resplandor, destello del fondo en el CTA | rojo | **dorado** | Llamado a la acción |
| Botón «Quiero mi inspección gratis» | píldora roja | **dorado de la landing**: `#c49a22 → #ac841d`, radio 14 px (28 px a escala del video), sombra `rgba(172,132,29,.45)` — calcado de `.btn-cta` de riskmann.com | Es el mismo botón de la página |
| Barra de progreso, marcas mayores del reloj | rojo | dorado | Decorativos |
| «con una novedad pendiente.», grietas, «No apto», «EXPUESTA», aguja del reloj, tensión roja del fondo | rojo | **rojo** | Son peligro o riesgo |

### Fondos (parámetro `?bg=`)

| Fondo | Idea | Cómo reacciona |
| --- | --- | --- |
| `liquido` | Mesh gradient líquido (el de la V1) | se retuerce, rojo → cian |
| `aurora` | Cortinas de luz verticales, más sobrias y «premium» | las bandas se tiñen de rojo en el problema y de cian en la solución |
| `topografico` | Curvas de nivel (mapa del terreno / rutas), cada 5.ª línea en dorado | las líneas se agitan; rojo → cian |
| `carretera` | Piso en perspectiva con carriles que avanzan hacia la cámara | la velocidad sube con la tensión; el horizonte se enciende rojo y luego cian |
| `bokeh` | Luces de tráfico desenfocadas: faros dorados, stops rojos | los stops rojos se encienden con el problema; el tráfico acelera |

`?ad=1&v=2&bg=carretera` en el preview; los selectores «Versión» y «Fondo» del panel hacen lo mismo.

### Renderizar

```bash
npm install            # una vez: puppeteer-core (usa el Chrome instalado)
npm run dev            # servidor en :5510
node tools/render.mjs --out <carpeta> --v 2 --bg carretera --ads 1,2,3 --prefix V2-carretera
```

~45 s por anuncio: 1080×1920, 30 fps, H.264 CRF 18, `+faststart`, pista de audio muda AAC
(algunas redes rechazan videos sin audio). Al llegar la locución se reemplaza esa pista.

`?ad=N&render=1` deja solo el lienzo 1080×1920 sin escalar, y `window.seekTo(t)` pinta cualquier
instante de forma determinista (GSAP y shader leen el mismo `t`). Para el MP4 hay dos caminos:
capturar fotograma a fotograma con esos ganchos, o partir cada anuncio en una composición
HyperFrames (el timeline ya está en pausa y registrado en `window.__timelines`) y seguir
`npx hyperframes lint / check / render` (§6 de `PRODUCCION-VIDEOS.md`).

---

## Audio producido (V1, V2 y V3)

Generado con `tools/audio.py` (la clave de ElevenLabs se pasa por `ELEVENLABS_API_KEY`, nunca al repo).

**Voz:** Carlos (`4PN5DHmrfIgZksvIrawS`, voz profesional PVC) con `eleven_multilingual_v2`, que es el
modelo para el que ElevenLabs la declara optimizada. Ajustes «vendedor máximo», los aprobados en
`ENTREGABLES-VIDEO/prueba-voz-carlos`: stability 0.15 · style 0.78 · speed 1.03 · seed 20260918. Cada frase
se pide **con marcas de tiempo por carácter** y encadenada a las vecinas (`previous_text`/`next_text`);
3 tomas por frase y gana la más pausada que quepa. Las [etiquetas] de v3 no se usan: v2 las leería.

| Anuncio | Tramo | Suena | Texto final |
| --- | --- | --- | --- |
| AD1 | hook | 0.08 → 1.94 s | «¿Inspeccionas TODOS tus vehículos?» |
| AD1 | valor-a | 2.05 → 4.33 s | «¿Cuándo fue la última vez que revisaste una?» |
| AD1 | valor-b | 4.55 → 7.89 s | «Con RiskMann… la haces desde el celular. ¡En MINUTOS!» |
| AD1 | cta | 8.00 → 10.45 s | «¡Regístrate HOY! Gratis… y sin tarjeta.» |
| AD2 | hook | 0.08 → 1.96 s | «Papel. Excel. WhatsApp.» |
| AD2 | valor-a | 2.04 → 3.59 s | «Y el vehículo… sigue rodando.» |
| AD2 | valor-b | 3.67 → 4.95 s | «Con una novedad pendiente.» |
| AD2 | valor-c | 5.03 → 6.55 s | «¿Quién lo inspeccionó? ¿Cuándo?» |
| AD2 | cta | 8.00 → 11.66 s | «Tranquilo… RiskMann lo centraliza todo. ¡Regístrate hoy!» |
| AD3 | hook | 0.08 → 1.82 s | «¿Tu técnico-mecánica al día?» |
| AD3 | valor-a | 2.00 → 4.17 s | «¿Y la inspección diaria del P-E-S-V?» |
| AD3 | valor-b | 4.25 → 6.62 s | «Sin registro, tu empresa queda… EXPUESTA.» |
| AD3 | cta | 8.00 → 10.96 s | «¡Regístrate HOY! RiskMann la registra gratis.» |

Recortes frente al guion original (no cabían sin acelerar la voz): AD 1 pierde «…a tiempo», AD 2 pierde
«Nadie lo sabe» (el quiebre de las tarjetas lo dice sin palabras), AD 3 usa «¿…diaria del P-E-S-V?» y
«Sin registro, tu empresa queda… EXPUESTA». La animación se movió para seguir a la voz real: en el AD 3
«EXPUESTA» golpea en 6.05 s y en el AD 2 el quiebre pasa a 6.0 s.

**Efectos:** librería Pixabay de /media-use (whooshes, impactos, riser, pings, pops, chime, sparkle — uso
comercial sin atribución) + cuatro a medida con ElevenLabs Sound Effects: tic-tac del reloj (AD 1), vidrio
que se agrieta y se rompe (AD 2), placas metálicas del escudo (AD 3).

**Música** — el cliente eligió la B (2026-09-24); se evaluaron tres candidatas por anuncio, niveladas a −18 LUFS para compararlas en igualdad:

| Opción | Fuente | Licencia | Dónde |
| --- | --- | --- | --- |
| A | «Hip Hop 02», Mixkit — tema producido, el mismo de la pieza PESV ya aprobada; se toma el tramo que sube hacia el segundo 8 | Mixkit Free License: uso comercial, sin atribución, cualquier plataforma | — |
| **B (elegida)** | Cama generada con ElevenLabs Sound Effects (la clave no trae `music_generation`) | Generado en plan pago: uso comercial | V1, V2 y V3 |
| C | Síntesis propia, `tools/ritmo.py` | Sin derechos de nadie | — |

**Mezcla:** la música baja ~5 dB cuando habla Carlos y tiene un hueco de −4 dB en 2 kHz; el cierre lleva
+2.5 dB de voz. Verificado frase por frase: la voz queda **≥ 8.5 dB sobre la música** en todas.
Máster a −14 LUFS / ≤ −1 dBTP (Reels, TikTok, Shorts), AAC 192 kbps en el MP4.
