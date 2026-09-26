# En Vivo PESV · Informe de Autogestión — campaña de 3 videos (12 s, 9:16)

Un video por correo de la secuencia que envía `notificaciones@yezidricaurte.com`. La copia fiel de los
tres correos, junto al video que acompaña a cada uno, está en
`Documentos_contexto/correos-en-vivo-pesv/index.html` (fuera del repo: llevan datos personales).

| Video | Correo | Asunto |
| --- | --- | --- |
| 1 · Faltan 18 días | reserva de cupo | Tu cupo en En Vivo PESV - Informe de Autogestión: cómo prepararte |
| 2 · Mañana | recordatorio 24 h | Mañana: En Vivo PESV - Informe de Autogestión a las 10:00 a. m. (Hora Colombia) |
| 3 · Hoy | transmisión | Hoy: En Vivo PESV - Informe de Autogestión |

Preview: `python -m http.server 5520` en esta carpeta → <http://localhost:5520/?ad=1>

## Identidad

| Fuente | Qué aporta |
| --- | --- |
| Correo de la campaña | petróleo `#001f26`, filete dorado `#d2b96a` bajo el encabezado, **botón coral `#f06e49`** con el mismo texto del correo |
| Manual de marca Yezid Ricaurte | Dubai (Bold títulos, Medium subtítulos, Regular texto), verde profundo `#336666`, firma oficial en negativo |
| Brief | verde FEGIR `#45a035` y destellos amarillo pálido `#f1ecb0` en el mesh gradient |

**Sin rojo:** en esta serie el cliente reserva el rojo para «peligro» (entrega del 18-sep). El indicador
«EN VIVO» del video 3 late en el pálido de marca, como en la invitación aprobada. El coral del botón no es
ese rojo: es el color de acción de los propios correos.

«Fundación FEGIR» no aparece en pantalla: ni los correos ni la web lo mencionan y no hay logo oficial en el
material. Si debe ir, se necesita su logo.

---

## Agente 1 · Guiones para ElevenLabs

**Voz:** Carlos (`4PN5DHmrfIgZksvIrawS`, la misma de la invitación aprobada), `eleven_multilingual_v2`
(el modelo para el que ElevenLabs optimiza esta voz), **estabilidad 0.35 · claridad 0.80** (lo que sugiere
el brief) · estilo 0.45 · velocidad 1.0. Cada frase se pide con marcas de tiempo por carácter y encadenada
a las vecinas (`previous_text`/`next_text`); 3 tomas por frase y gana la más pausada que quepa.

**Ingeniería de puntuación, con lo que ya se midió en este repo:**

| Recurso del brief | Qué se hizo | Por qué |
| --- | --- | --- |
| Guiones largos para pausas | **puntos suspensivos** `…` | medido: `…` deja 0.64 s de silencio y `—` 0.57 s (`ENTREGABLES-VIDEO/prueba-puntuacion`) |
| Comillas para énfasis | no se usan | no es un mecanismo del modelo: puede leerlas como cita |
| — | **PESV deletreado: `P-E-S-V`** | la sigla pasa de 0.49 a 0.95 s y se entiende a la primera |
| — | **cifras en palabras** | «dieciocho», «tres de octubre», «diez de la mañana» |
| — | **«vivo» nunca cierra frase** | cerrando frase el modelo se come la «o» y suena a «vip» (invitación del 18-sep) |

### Textos locutados (los que cupieron; entre corchetes, lo que se recortó del borrador)

**Video 1 · Anticipación**
```text
Faltan dieciocho días… para En Vivo P-E-S-V.            [: Informe de Autogestión — no cabía]
Sábado tres de octubre… a las diez de la mañana, hora Colombia.
Crea hoy tu cuenta en app punto riskmann punto com.
```

**Video 2 · Urgencia**
```text
¡Mañana es En Vivo P-E-S-V!, a las diez de la mañana.    [hora Colombia — va en pantalla]
Los enlaces, por el grupo de WhatsApp. Ten lista tu cuenta en RiskMann.
Entra ya al grupo de WhatsApp.
```

**Video 3 · Acción inmediata**
```text
¡Hoy es En Vivo P-E-S-V!… a las diez de la mañana.
Por Instagram, TikTok y YouTube. Ten abierta tu cuenta en RiskMann.
Ve ya al grupo de WhatsApp.
```

---

## [STORYBOARD TIMELINE]

Los números salen de la voz real: `audioTimestampsV1/V2/V3` al inicio de `js/ads.js`. Si se regraba la
voz, se cambian esos números y la animación se recoloca sola.

### Video 1 — `audioTimestampsV1 = { hook: 0.0, dieciocho: 0.49, fecha: 4.5, hora: 6.25, cta: 8.0 }`

| s | Visual | Voz |
| --- | --- | --- |
| 0.05 | Rótulo «EN VIVO PESV · Informe de Autogestión» + filete dorado (el encabezado del correo) | |
| 0.10 | Reloj de arena SVG: marco y vidrio se dibujan con stroke-dashoffset; la arena cae de 0.8 a 4.0 s | «Faltan…» |
| 0.20–0.45 | «Faltan / **18** / días» palabra por palabra; el 18 entra 1.5→1 (back.out) con destello **en 0.45**, con la palabra «dieciocho» | «…dieciocho días» (0.49) |
| 1.60 | «para En Vivo PESV»; el reloj flota | «…para En Vivo P-E-S-V» |
| 4.50 | Tarjeta glass de calendario: anillas trazadas, «OCTUBRE 2026», **03**, «Sábado» | «Sábado tres de octubre…» |
| 6.17 | «10:00 a. m. (Hora Colombia)»; el calendario flota y respira a 1.02 | «…a las diez de la mañana» (6.25) |
| 8.00 | «Nos vemos en vivo.» (el cierre del correo) + **SPECTACLE**: botón coral «Crea tu cuenta» 1.6→1 con `back.out(4)`, resplandor coral que estalla y respira, sacudida, destello | «Crea hoy tu cuenta…» |
| 8.50–9.35 | app.riskmann.com/registrarse · «y entra al grupo oficial de WhatsApp» · firma · yezidricaurte.com | |

### Video 2 — `audioTimestampsV2 = { hook: 0.0, hora: 3.05, info: 4.0, grupo: 5.2, cuenta: 6.16, cta: 8.0 }`

| s | Visual | Voz |
| --- | --- | --- |
| 0.10 | **«Mañana»** 1.5→1 + «es En Vivo PESV» en cascada; el líquido corre más (energía ↑) | «¡Mañana es En Vivo P-E-S-V!» |
| 2.93 | Chip «10:00 a. m. · Hora Colombia», el reloj se traza | «…a las diez de la mañana» (3.05) |
| 4.00 | Tarjeta glass con los dos pasos del correo; paso 1 entra | «Los enlaces…» |
| 5.20 | Se traza el ícono de chat del paso 1 | «…por el grupo de WhatsApp» |
| 6.01–6.16 | Paso 2 entra y se traza el check; la tarjeta flota | «Ten lista tu cuenta en RiskMann» |
| 8.00 | «¡Te esperamos!» + **SPECTACLE**: botón coral «Entrar al grupo de WhatsApp» (texto idéntico al del correo) | «Entra ya al grupo de WhatsApp» |
| 8.50–9.35 | «Mañana · 10:00 a. m. (Hora Colombia)» · firma · yezidricaurte.com | |

### Video 3 — `audioTimestampsV3 = { hook: 0.0, hora: 2.41, redes: 3.6, instagram: 3.93, tiktok: 4.51, youtube: 5.33, cuenta: 6.07, cta: 8.0 }`

| s | Visual | Voz |
| --- | --- | --- |
| 0.05–12 | Indicador **EN VIVO**: aro trazado, núcleo pálido que late y dos ondas que se expanden los 12 s | |
| 0.20 | «Hoy es / En Vivo / PESV» palabra por palabra | «¡Hoy es En Vivo P-E-S-V!» |
| 2.31 | «10:00 a. m. · Hora Colombia» | «…a las diez de la mañana» (2.41) |
| 3.60 | «La transmisión va por» | «Por…» |
| 3.88 · 4.46 · 5.28 | Tarjetas glass **Instagram · TikTok · YouTube**, cada una entra cuando la voz la nombra | «Instagram, TikTok y YouTube» |
| 6.02 | «Ten abierta tu cuenta en app.riskmann.com» | «Ten abierta tu cuenta en RiskMann» (6.07) |
| 8.00 | «Los enlaces, en el grupo oficial» + **SPECTACLE**: botón coral «Ir al grupo de WhatsApp» | «Ve ya al grupo de WhatsApp» |

---

## Agente 2 · Código

| Archivo | Qué hace |
| --- | --- |
| `index.html` | Lienzo 1080×1920 con las 3 composiciones + panel de preview |
| `js/bg.js` | Three.js: **mesh gradient** de 6 puntos de color que derivan (Lissajous) sobre un campo deformado con ruido, mezclados por distancia inversa. Reacciona a `energia`, `pulso`, `coral`, `warp`, `zoom` |
| `js/ads.js` | `audioTimestampsV1/V2/V3` + un timeline GSAP en pausa por video, registrado en `window.__timelines` |
| `tools/audio.py` | voz (ElevenLabs) · efectos · música · mezcla con ducking y verificación voz/música por frase |
| `tools/render.mjs` | render fotograma a fotograma con el Chrome del sistema + ffmpeg |

Reglas físicas: entradas solo con `power4.out` o `back.out(1.5)`; textos palabra por palabra
(`stagger`); flotación en Y + escala 1.02 con repeticiones contadas (seek-safe); spectacle beat del botón
con overshoot `back.out(4)` desde 1.6 y `drop-shadow` dinámico.

## Audio

- **Música:** «Elegant» (atlasaudio, Pixabay Content License: uso comercial sin atribución), la pista que
  el cliente ya aprobó para este evento, desde el segundo 9.90 como en la versión aprobada.
- **Efectos:** Pixabay (/media-use) + tres generados con ElevenLabs: arena del reloj, tic-tac, hoja del
  calendario.
- **Mezcla:** −14 LUFS; la voz queda **≥ 11 dB** sobre la música en todas las frases.

```bash
set ELEVENLABS_API_KEY=sk_...        # nunca se guarda en el repo
python tools/audio.py voz            # tomas + marcas de tiempo
python tools/audio.py sfx
python tools/audio.py musica
python tools/audio.py mezcla
node tools/render.mjs --out <carpeta> --base http://localhost:5520
```
