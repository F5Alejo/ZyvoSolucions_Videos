# En Vivo PESV · «Estudio virtual» — campaña de 3 videos (12 s, 9:16)

Video de **yezidricaurte.com** (no de FEGIR). Una sola composición; los textos, colores y tiempos viven en
`js/config.js`. Preview: `python -m http.server 5540` → <http://localhost:5540/?v=v1&fondo=escudo>

| | `?v=` | Titular | Botón |
| --- | --- | --- | --- |
| Video 1 · urgencia de tiempo | `v1` | Faltan pocos días… | Crea tu cuenta |
| Video 2 · recordatorio | `v2` | La oportunidad es mañana | Entrar al grupo de WhatsApp |
| Video 3 · clímax | `v3` | Llegó el día (+ sello EN VIVO) | Ir al grupo de WhatsApp |

## Decisiones frente a los prompts

| Punto | Prompt | Qué se hizo |
| --- | --- | --- |
| Fondo | uno prohíbe el plexus y pide un objeto 3D; el otro pide plexus sutil | **los dos**: `&fondo=escudo` (por defecto) y `&fondo=plexus` |
| Botón | verde FEGIR `#45a035` o cristal con borde dorado | **cristal con borde y resplandor dorado** por defecto: el cliente aclaró que el video es de yezidricaurte.com, no de FEGIR. El verde queda a un cambio: `BOTON = "verde"` en `config.js` |
| «Organizado por Fundación FEGIR» | lo menciona | no sale en pantalla: no está en los correos ni en la web y no hay logo oficial |
| Tipografía | Outfit o Montserrat | **Montserrat**, la de yezidricaurte.com (archivos reales en `assets/fonts/`) |
| Foto | `yezid-photo.png` en la raíz | está ahí: el recorte oficial publicado en yezidricaurte.com |

---

## Agente 1 · Guiones para ElevenLabs

Carlos (`4PN5DHmrfIgZksvIrawS`) · `eleven_multilingual_v2` · los mismos ajustes de la campaña aprobada.

```text
V1  Faltan pocos días… para dominar el P-E-S-V. Blinda tu empresa… en un solo día. ¡Regístrate ahora!
V2  La oportunidad es mañana… A las diez de la mañana, hora Colombia. ¡Entra al grupo de WhatsApp!
V3  Llegó el día… Estamos en vivo, ¡únete ahora mismo!
```

El prompt pide guiones largos y comillas; se aplicó lo que ya **se midió** en este repo
(`ENTREGABLES-VIDEO/prueba-puntuacion`):

| Recurso | Medido | Uso |
| --- | --- | --- |
| `…` | 0.64 s de silencio | todas las pausas dramáticas |
| `—` | 0.57 s (peor que `…`) | no se usa |
| comillas | no son un mecanismo del modelo; puede leerlas como cita | no se usan |
| `P-E-S-V` | la sigla pasa de 0.49 a 0.95 s y se entiende | V1 |
| «vivo» al cierre de frase | el modelo se come la «o» y suena «vip» (invitación del 18-sep) | V3: «Estamos en vivo, ¡únete…» — la coma obliga a articularla |
| cifras | «10» puede leerse «uno cero» | «diez de la mañana» en letras |

---

## [STORYBOARD TIMELINE]

`videoTimestamps` en `js/config.js`: v1 `{ hook: 0.5, valor: 4.0, cta: 8.5 }` · v2 `{ 0.4, 3.4, 8.0 }` · v3
`{ 0.4, 3.0, 7.6 }`. Con la voz real se reemplazan por los de `/with-timestamps` y todo se recoloca.

**Siempre (0–12 s):** fondo sólido verde profundo `#1A3B3B → #0F2A2A`; el escudo de cristal gira sin parar
sobre Y (0.24 rad/s) con su anillo dorado y tres nodos que orbitan; todo el contenido flota ±6 px; la foto
flota ±16 px; el punto pálido del rótulo late cada 1.2 s.

### Video 1 · Faltan pocos días

| s | Imagen | Voz |
| --- | --- | --- |
| 0.05 | Rótulo «EN VIVO PESV · Informe de Autogestión» se abre desde el centro (clip-path) | |
| 0.10 | La tarjeta de cristal de la foto se abre de abajo arriba; la foto entra con punch-in 1.25→1 (expo.out) | |
| 0.50 | **HOOK** «Faltan pocos días…» letra por letra desde su máscara (yPercent 115→0, expo.out, stagger 0.035), dorado; destello del fondo | «Faltan pocos días…» |
| 0.80 | Chip «Dr. Yezid Ricaurte · Abogado · Consultor · Conferencista» se revela de izquierda a derecha | «…para dominar el P-E-S-V» |
| 4.00 | **VALOR** subtítulo en cascada por palabras (power4.out); «dominar el reporte PESV» y «blinda tu empresa» en Bold, «un solo día.» en dorado | «Blinda tu empresa… en un solo día» |
| 4.80 | Tarjetas de cristal «Sábado · 03 de octubre» y «Hora · 10:00 a. m. (Col)» se revelan con clip-path | |
| 8.05 | El mensaje sube recortándose por su máscara | |
| 8.30 | La cámara 3D inicia un zoom-in hacia el escudo (1.4 s) | |
| 8.50 | **SPECTACLE BEAT**: botón «Crea tu cuenta» 1.5→1 con back.out(1.5); resplandor dorado que estalla a 60 px y respira; destello del fondo | «¡Regístrate ahora!» |
| 8.95–9.70 | «app.riskmann.com/registrarse» · firma oficial (revelado lateral) · yezidricaurte.com | |

### Video 2 · Es mañana

| s | Imagen | Voz |
| --- | --- | --- |
| 0.40 | «La oportunidad es mañana» letra por letra | «La oportunidad es mañana…» |
| 3.40 | «Los enlaces llegan por el grupo oficial de WhatsApp. Ten lista tu cuenta en app.riskmann.com.» | «A las diez de la mañana, hora Colombia» |
| 4.20 | Tarjetas «Mañana · 03 de octubre» y «Hora · 10:00 a. m. (Col)» | |
| 8.00 | Zoom-in + botón «Entrar al grupo de WhatsApp» (texto idéntico al del correo) + «Grupo oficial del En Vivo» | «¡Entra al grupo de WhatsApp!» |

### Video 3 · Es hoy

| s | Imagen | Voz |
| --- | --- | --- |
| 0–12 | Sello «EN VIVO» sobre la foto, latiendo en pálido (sin rojo) | |
| 0.40 | «Llegó el día» letra por letra | «Llegó el día…» |
| 3.00 | «Transmisión por Instagram, TikTok y YouTube. Los enlaces, en el grupo oficial.» | «Estamos en vivo…» |
| 3.80 | Tarjetas «Hoy · 10:00 a. m.» y «Estado · En vivo» | |
| 7.60 | Zoom-in + botón «Ir al grupo de WhatsApp» + «Ten abierta tu cuenta en app.riskmann.com» | «¡únete ahora mismo!» |

---

## Agente 3 · Código

| Archivo | Qué hace |
| --- | --- |
| `js/config.js` | textos de los 3 videos, `videoTimestamps`, guiones, paleta, estilo del botón |
| `js/estudio.js` | Three.js: fondo sólido con degradado radial mínimo + **escudo de cristal** (ExtrudeGeometry, MeshPhysicalMaterial con transmisión, aristas doradas, anillo de datos con nodos) o **red geométrica** lenta; zoom de cámara en el CTA |
| `js/escena.js` | arma el DOM y la coreografía GSAP (un timeline en pausa, seek-safe) |
| `js/main.js` | reproductor, voz de `assets/voz/v1.mp3…`, `window.seekTo(t)` para render |
| `tools/render.mjs` | `node tools/render.mjs --out <carpeta> --fondo escudo|plexus` |
| `tools/snap.mjs` | hoja de contactos: `node tools/snap.mjs v1 salida.png 1.0 5.0 9.0` |

Reglas: cero fades lineales (máscaras `clip-path` + `yPercent` con `expo.out` / `power4.out` / `back.out(1.5)`),
flotación con repeticiones contadas (nunca `repeat: -1`), sin rojo ni coral en pantalla.
