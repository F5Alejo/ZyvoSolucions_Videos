# Playbook — producir video con HyperFrames y un agente

> **Qué es esto.** La memoria destilada de todo lo que se produjo en este repositorio
> (2026): qué se hizo, **cómo** se hizo y qué parte se lleva tal cual a
> un proyecto nuevo — de RiskMann o de cualquier otro cliente.
>
> No sustituye a los otros documentos, los ordena:
>
> | Documento | Pregunta que responde |
> | --- | --- |
> | **Este** | ¿Qué formato elijo, qué copio y en qué orden trabajo? |
> | [`PRODUCCION-VIDEOS.md`](../PRODUCCION-VIDEOS.md) | ¿Cuáles son los valores y reglas exactos de cada formato? |
> | [`GUIA-PROMPTS.md`](../GUIA-PROMPTS.md) | ¿Qué le digo al agente para conseguir cada cosa? |
> | [`POC-SEGURIDAD-VIAL-PASAJEROS.md`](POC-SEGURIDAD-VIAL-PASAJEROS.md) | ¿Qué se entregó en el PoC y cómo responde al issue? |
> | [`ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md) | ¿Qué instalo en un equipo nuevo y qué errores de audio, GSAP y verificador ya se pagaron? |
> | [`BITACORA-2026-09-17-18.md`](BITACORA-2026-09-17-18.md) | ¿Qué se decidió en las piezas verticales de RiskMann y Yezid, y qué quedó abierto? |
> | [`marca/LEEME.md`](marca/LEEME.md) | ¿Qué fija el manual oficial de RiskMann (y qué solo se ve mirando las páginas)? |
>
> **Tres líneas de trabajo** alimentan este documento: la de cursos y PoC (Juan), la de
> piezas verticales con ElevenLabs y manual de marca (Alejandro) y la de campañas de En
> Vivo y anuncios de landing (equipo `fegir`). Las secciones §6 y §9 recogen las dos
> últimas.

---

## 1. Qué se produjo

| Serie | Entrada | Formato | Salida | Proyecto(s) |
| --- | --- | --- | --- | --- |
| RiskMann «Sala de control» | Logos, iconos, capturas y 3 grabaciones de UI | Marketing, 9 planos | 68 s, muda y narrada | `videos/riskmann-sala-de-control/` |
| PESV «Pasajero seguro» · M01 | PDF de diapositivas | «Centro de mando» (voz Piper) | 2:31 — **entregable del PoC** | `videos/pesv-m01-mando/` |
| PESV · M01 corto | El mismo PDF | «Ritmo» (sin voz, 120 BPM) | 60 s, 16:9 y 9:16 | `videos/pesv-m01-ritmo[-vertical]/` |
| PESV · exploración | El mismo PDF | Partículas GPU + 3D | Apertura aprobada, resto sin construir | `videos/pesv-m01-profundidad[-vertical]/` |
| SOFU BIC S.A.S. | Guion de la empresa | Comercial | 68 s; v2 dinámica 52 s (16:9 y 9:16) | `videos/sofu-comercial/`, `videos/sofu-comercial-v2[-vertical]/` |
| «Ruta Segura» (ciclistas) | PPTX de 33 láminas con notas | Curso lámina a lámina, láminas escritas a mano (`eNN.py`) | 4 módulos, 16 min, cortados en piezas de 1–2 min | `videos/ruta-segura-m1…m4/` |
| «Motociclista laboral seguro» | PPTX de 88 láminas con **formas con nombre** | Curso **generado** por plantillas | 15 videos, 40:47 | `videos/moto-curso/` → `moto-*` |
| «Conducción Segura y Manejo Defensivo» | PPTX de 55 láminas | Curso **generado** por plantillas | 15 videos, ~33 min + banco de preguntas | `videos/csm-curso/` → `csm-*` |
| RiskMann · consulta PESV | Landing del PESV + manual oficial (`docs/marca/`) | Vertical para redes, ElevenLabs + música con ducking | 33.3 s 9:16, variantes de audio A/B/C (se entregó la A); también 16:9 | `videos/riskmann-consulta-pesv[-vertical]/` |
| RiskMann · PESV v2 y publicitario | Manual oficial | «La lente del manual como cámara continua»; publicitario de 8 escenas | Esqueleto verificado; publicitario ~36 s programado | `videos/riskmann-pesv-v2/`, `videos/riskmann-pesv-publicitario/` |
| Yezid Ricaurte · En Vivo | Página del evento + manual de Yezid | Promo vertical, HyperFrames, rejilla de tempo | 15 s 9:16, voz + efectos + música | `videos/yezid-envivo-pesv-autogestion/` |
| Yezid Ricaurte · campañas del En Vivo | Correos de la campaña + web + manual | **Lienzo propio** (Three.js + GSAP + puppeteer), una composición y varias variantes | 15 s; campañas de 3 videos de 12 s (pocos días / mañana / hoy) | `videos/yezid-envivo-15s/`, `-campana[-v2]/`, `-estudio/`, `-premium/` |
| FEGIR · En Vivo | Mismo evento, firmado por la Fundación FEGIR | HyperFrames, reorganizado para editar en el Studio | 5 escenas con voz, efectos y música generada; `fegir-envivo-pesv` es una variante en curso (fondo `aurora-drift` y narración) | `videos/fegir-envivo/`, `videos/fegir-envivo-pesv/` |
| RiskMann · «Inspecciones gratis» | Solo la landing `riskmann.com/inspecciones-gratis/` | Lienzo propio, 3 anuncios `hook / valor / cta` | 3 × 12 s 9:16, `eleven_v3` | `videos/riskmann-inspecciones-ads/` |

Todas las entregas finales están en `../videos-finales/` (con su `LEEME.txt`) y en la
carpeta de Drive enlazada en el [README](../README.md).

### La curva de aprendizaje, en una línea por paso

1. **Sala de control** — un día entero inventando el sistema (paleta, HUD, reglas). Nació
   la regla §0: se coló un «100 %» inventado.
2. **PESV M01** — tres direcciones rechazadas (réplica, «plus», monigotes, refactor
   fotográfico) antes de «Centro de mando». Nació la regla *muestra antes que módulo*.
3. **Ritmo** — aprobado sin cambios: el pulso musical como reloj de la animación.
4. **Ruta Segura** — la voz dicta el tiempo; `cronometro.py` separa el montaje de la
   locución; render por partes en 8 GB de RAM.
5. **Moto y CSM** — el salto de escala: de 12 láminas escritas a mano a 88 generadas. Un
   curso entero de 15 videos sale de `curso.json` + 6–7 plantillas + un comando por módulo.
6. **Consulta PESV vertical** — la música tapaba la voz 8–16 dB y 44 de 76 ventanas
   estaban congeladas. Nacieron la clave `musica` de `mezcla.py`, `nivelar-voz.py` y la
   medición de tiempos muertos; la identidad pasó a construirse contra el manual en PDF.
7. **En Vivo (Yezid / FEGIR)** — el mismo evento en dos marcas y varios estilos. Nació la
   pregunta que ahora va primero: **¿de quién es el video?** — y la puntuación medida
   para ElevenLabs (`…` como pausa, siglas deletreadas).
8. **Anuncios de landing** — una sola URL como fuente y tres ángulos (`hook / valor / cta`)
   sobre la misma composición: la campaña corta se vuelve configuración (`js/config.js`).

**La lección de fondo:** el primer video de un formato cuesta un día; el segundo, una
hora; con el formato convertido en generador, un módulo cuesta lo que tarda su render.

---

## 2. Elegir el formato

```
¿Qué te entregan?
├─ Assets sueltos de un producto (logo, capturas, grabaciones) ─→ Marketing (PRODUCCION §1–§8)
├─ Un guion comercial de la empresa ────────────────────────────→ Comercial (modelo: sofu-comercial)
├─ Una landing o un evento para redes (9:16, 12–35 s, con voz) ─→ Pieza corta ElevenLabs (§6)
│    ├─ Una pieza que se editará después en el Studio ──────────→ HyperFrames (yezid-envivo-pesv-autogestion, fegir-envivo)
│    └─ Campaña de N variantes de la misma pieza ───────────────→ Lienzo propio + config.js (yezid-envivo-premium)
├─ Un PDF/diapositivas SIN notas de orador
│    ├─ Quieren el módulo completo con voz ─────────────────────→ «Centro de mando» (§10)
│    └─ Quieren gancho corto para redes ────────────────────────→ «Ritmo» 16:9 + 9:16 (§13)
└─ Un PPTX CON notas de orador (curso)
     ├─ ≤ 15 láminas, cada una distinta ────────────────────────→ Lámina a lámina a mano (§14, ruta-segura)
     └─ Muchas láminas con anatomía repetida ───────────────────→ Curso generado (§15, moto / csm)
```

Regla práctica para el último caso: si al hojear el PPTX ves **menos de ~8 anatomías
distintas de lámina**, escribe plantillas; si cada lámina es única, escríbelas a mano.

---

## 3. El método de trabajo (vale para cualquier formato)

Estas nueve prácticas son las que más tiempo ahorraron. Ninguna depende de RiskMann.

1. **La fuente manda.** Nada entra al video —texto, cifra, norma, nombre de módulo— si no
   se rastrea a un archivo entregado. Cada frase de locución cita su fuente en el JSON.
2. **Muestra antes que módulo.** Construir solo la apertura (~15 s) **con sonido** y
   pedir el sí. Una muestra cuesta ~10 min; un módulo en la dirección equivocada costó
   ~1 h + 9 min de render, tres veces.
3. **La voz antes que la animación.** La duración de cada plano sale de la locución real
   (o de su medición), nunca al revés. Si no cabe, se acorta la frase, no el plano.
4. **Un documento de dirección antes de construir en paralelo.** `DIRECCION.md` (o
   `base.py` en los cursos generados) fija las constantes: posición del logo, retícula,
   paleta, tipografía. Es lo que permite que planos hechos por separado parezcan uno.
5. **Configuración, no código.** Voz, mezcla, pista rítmica y cursos enteros se describen
   en JSON; los scripts de `tools/` no cambian entre proyectos.
6. **Verificar con medición, no con el ojo del agente.** El agente no oye ni ve el MP4:
   `lint` + `check` + hoja de contactos + espectro de audio por bandas.
7. **Entregar en piezas.** Un video por módulo; piezas de 1–2 min cortadas en frontera
   de lámina; máster continuo solo si lo piden (`unir-curso.py`).
8. **Commit y push antes de renderizar, y nunca dentro de OneDrive.** OneDrive borró el
   repo en caliente y luego lo revirtió seis commits; lo único que se salvó fue lo que
   estaba en GitHub.
9. **Primero, de quién es el video.** La marca que firma (RiskMann, Yezid, FEGIR) decide
   paleta, tipografía, logo y dominio del CTA. Si la página y el manual no coinciden,
   se le plantea al cliente; no se mezcla mitad y mitad.

---

## 4. Las piezas reutilizables

### 4.1 Herramientas compartidas (`tools/`, no cambian entre proyectos)

| Script | Entrada | Cuándo |
| --- | --- | --- |
| `voz.py` | `guion.json` | Voz local gratuita (Piper `es_ES-davefx-medium`); avisa si una línea no cabe |
| `descargar-voz.py` | — | Una vez por equipo: baja y verifica el modelo Piper |
| `ritmo.py` | `ritmo.json` | Pista rítmica sintetizada a un BPM, sin derechos de terceros |
| `mezcla.py` | `mezcla-*.json` | Voz + pistas + cama + **`musica` (con ducking bajo la voz)** + efectos, −16 LUFS; falla si la banda >400 Hz queda vacía. Admite versión de solo música (bus frontal vacío, sin ducking) |
| `nivelar-voz.py` | carpeta de tomas | Lleva el TTS (ElevenLabs sale a ~−33 dB) a nivel de emisión, **a disco**, antes de mezclar |
| `probar-voces.py` | una frase | La misma frase con varias voces, para que el cliente elija a ciegas |
| `render-partes.py` | carpetas de proyecto | Render por partes, reanudable, mata huérfanos |
| `cortar-laminas.py` | proyecto + `--piezas N` | Parte un módulo en piezas parejas en frontera de lámina |
| `unir-curso.py` | carpeta de módulos | Máster continuo sin recodificar |

### 4.2 Plantillas de proyecto (se copian)

| Para | Copiar | Cambiar |
| --- | --- | --- |
| Módulo de formación con voz | `videos/pesv-m01-mando/` | `tools/guion.json`, tabla de tiempos de `DIRECCION.md`, planos 02–07 |
| Pieza corta al pulso | `videos/pesv-m01-ritmo/` | una frase por escena, `ritmo-video.json`, `mezcla-video.json` |
| Versión vertical | `videos/pesv-m01-ritmo-vertical/` | recomponer escenas (no escalar) |
| Curso lámina a lámina | `videos/ruta-segura-m1/` | `tools/eNN.py`; `base.py` se deja |
| Curso generado | `videos/csm-curso/` (el más reciente) | `datos/`, `base.py` (paleta), `plantillas.py`, `LIMITES` |
| Marketing | `npx hyperframes init` + receta `riskmann-hud` | ver PRODUCCION §6 — **ojo:** la receta no coincide con el manual oficial (§9) |
| Vertical RiskMann con ElevenLabs | `videos/riskmann-consulta-pesv-vertical/` | `SCRIPT.md`, `tools/narracion.json`, `SFX-CUES.md`, `tools/final-A.json` |
| Promo de evento (HyperFrames) | `videos/yezid-envivo-pesv-autogestion/` | `tools/narracion.json`, `--brand` del fondo `aurora-drift`, rejilla de tempo |
| Promo editable en el Studio | `videos/fegir-envivo/` | `compositions/escena-*.html` (ver su `EDITAR.md`); **no** volver a correr `tools/estudio.py` |
| Campaña de variantes (lienzo propio) | `videos/yezid-envivo-premium/` | `js/config.js` (textos, colores y tiempos por variante) |
| Anuncios de una landing | `videos/riskmann-inspecciones-ads/` | `js/ads.js → SCRIPTS`, la URL fuente en `GUIONES.md` |

### 4.3 Recetas y fragmentos que ya están resueltos

- **`@font-face` de Montserrat** con los dos `.woff2` (latin + latin-ext): en cualquier
  `base.py`. Sin él, el render sale con otra fuente en silencio.
- **Números a palabras en español** para TTS (`en_palabras`, `normalizar` en
  `moto-curso/tools/moto.py`): «2466» → «dos mil cuatrocientos sesenta y seis»,
  «60 km/h», «%», siglas deletreadas («P E S V»).
- **Sincronía automática voz→aparición** (`sincronia.py`): empareja cada elemento con la
  frase que comparte más raíces de 5 letras; orden preservado, separación mínima 0,55 s,
  reparto si no hay coincidencia. Reutilizable en cualquier idioma cambiando `VACIAS`.
- **Reparto óptimo en piezas** (`tramos` en `moto.py`, `cortar-laminas.py`): programación
  dinámica que minimiza la desviación de cada pieza a la duración objetivo.
- **`cronometro.py`** (ruta-segura): traduce las marcas de tiempo de una locución a otra
  — la voz sintética de aprobación se cambia por una humana sin tocar el montaje.
- **Grado de fotografía a una paleta**: `brightness(0.78) contrast(1.14) saturate(0.45)
  hue-rotate(-6deg)` + capa de marca en `multiply` ~0.40 + scrim local bajo el texto.
- **Receta de identidad** `riskmann-hud` en `~/.media/recipes/` — el patrón de congelar
  una estética para reusarla vale para cualquier marca nueva.

---

## 5. Pipeline del curso generado (moto / csm)

Es el formato más escalable y el único que aún no estaba documentado en
`PRODUCCION-VIDEOS.md` (ver §15 allí).

```
PPTX ──extraer──▶ datos/curso.json ──voz──▶ assets/voz/sNN.mp3 + datos/tiempos-voz.json
                                    │
                                    └──construir──▶ videos/<curso>-<clave>/ (index + compositions + partes)
                                                     │
                            tools/render-partes.py ◀─┘ ──▶ renders/parte-N.mp4 (mudos)
                                                     │
                                          montar ────┴──▶ renders/<curso>-<clave>-N.mp4 (voz pegada, verificada)
```

```bash
set ELEVENLABS_API_KEY=...
python videos/csm-curso/tools/csm.py voz m01          # locuta lo que falte, guarda tiempos por frase
python videos/csm-curso/tools/csm.py construir m01    # genera videos/csm-m01/
cd videos/csm-m01 && npx hyperframes lint && npx hyperframes check && cd ../..
python videos/csm-curso/tools/csm.py construir m01 --tramos   # después de validar: index-parte-N.html
python tools/render-partes.py videos/csm-m01
python videos/csm-curso/tools/csm.py montar m01       # pista por tramo + mux + comprobación de duración
```

**Piezas del generador:**

| Archivo | Responsabilidad |
| --- | --- |
| `datos/curso.json` | Una entrada por lámina: `n`, `formas` (texto por nombre de forma del PPTX), `notas`/`texto`, `frases` |
| `datos/guion-partes.json` (csm) | Narración escrita cuando las notas del PPTX solo anuncian la parte — armada con lo que la lámina muestra, sin añadir |
| `base.py` | Paleta muestreada del PPTX, fuentes, encuadre común, `envoltura()` de cada composición |
| `plantillas.py` | 6–7 plantillas; `elegir(d)` decide por la firma de nombres de forma (moto) o por número de lámina (csm) |
| `sincronia.py` | Instante de cada aparición según la frase que la nombra |
| `<curso>.py` | `LIMITES` (láminas por módulo), `voz`, `construir`, `montar`; filtra evaluaciones y preguntas |

**Decisiones que funcionaron:**

- Duración de lámina = `ANTES` (1,0 s) + narración + `COLA` (1,3 s).
- Sin locución, se estima: `0,068 s × caracteres + 0,374 s` por frase — el video se puede
  construir y revisar mudo antes de pagar voz.
- Las preguntas, autochequeos y evaluaciones **no van en el video**: se cortan de la nota
  (`PAUSA` regex) y van a la plataforma. Para csm se generó además el banco A/B/C
  (`datos/banco_preguntas.py` + `tools/banco_html.py`), con la fuente de cada pregunta.
- La voz va **fuera** del `index.html` y se pega al final: el render mudo cabe en 8 GB.
- `montar` rechaza el resultado si el video y su pista difieren más de 0,6 s.
- Paleta del PPTX, pero **Montserrat** en vez de Aptos/Arial (empaquetable), y el color
  claro de marca nunca como texto pequeño (se usa una variante oscura con ≥ 4,5:1).

---

## 6. Piezas cortas para redes con ElevenLabs (verticales, En Vivo, landings)

El formato que produjeron Alejandro y el equipo `fegir`: 12–35 s, 9:16, con locución
de ElevenLabs, efectos y música. El detalle técnico está en
[`ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md); aquí va lo que se reutiliza.

### 6.1 Dos maneras de construirla

| | HyperFrames | Lienzo propio |
| --- | --- | --- |
| Proyectos | `riskmann-consulta-pesv-vertical`, `yezid-envivo-pesv-autogestion`, `fegir-envivo` | `yezid-envivo-15s`, `-campana[-v2]`, `-estudio`, `-premium`, `riskmann-inspecciones-ads` |
| Motor | `data-*` + GSAP, `npm run check` / `render` | HTML + GSAP + Three.js; `window.seekTo(t)` y `tools/render.mjs` (puppeteer-core + Chrome del sistema → ffmpeg) |
| Preview | `npx hyperframes preview` | `python -m http.server <puerto>` + `?ad=` / `?v=` |
| Cuándo | Una pieza que alguien seguirá editando en el Studio | Varias variantes de la misma pieza, o 3D/shaders que no caben en una composición |
| Ojo | El Studio reescribe archivos con la vista previa abierta | No tiene `lint`/`check`: la verificación es la hoja de contactos (`tools/snap.mjs`) |

Las dos siguen las reglas de determinismo de §8 (timeline pausada, sin `Math.random`
ni `repeat:-1`): el render busca por tiempo.

### 6.2 La voz

- **Voz «Carlos»** (colombiana) `4PN5DHmrfIgZksvIrawS`. Dos perfiles aprobados:
  - Narrado, `eleven_multilingual_v2`: `stability 0.32–0.35 · style 0.45 · claridad 0.80`,
    velocidad por plano. Con 0.5 lee plano y apresurado.
  - Vendedor, `eleven_v3`: `stability 0.15 · style 0.78 · speed 1.03`; admite
    `[etiquetas]` de tono (en `multilingual_v2` se leerían en voz alta: quitarlas).
- **Siempre con timestamps por carácter** (`/with-timestamps`) y cada aparición sobre la
  palabra que la nombra; encadenar frases con `previous_text` / `next_text`; 3 tomas por
  frase y gana la más pausada que quepa.
- **Puntuación medida:** `…` = 0.64 s, la mejor pausa; `—` = 0.57 s; siglas deletreadas
  (`P-E-S-V`, o «pe e ese ve» en el texto) pasan de 0.49 a 0.95 s y se entienden; una
  palabra en MAYÚSCULAS por anuncio con `eleven_v3`; «vivo» nunca cierra frase.
- **El acento es propiedad de la voz**, no un parámetro. Y la misma frase dura
  6.5–9.9 s según la voz: cambiarla obliga a recolocar las animaciones.
- El cuerpo de la petición en **UTF-8 desde Python**: con `curl` y tildes, `400 invalid_unicode`.
- La clave se lee de `ELEVENLABS_API_KEY`, nunca se escribe en el repo.

### 6.3 La mezcla

```bash
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14   # a disco, antes de mezclar
python ../../tools/mezcla.py tools/final-A.json                         # musica con ducking bajo la voz
```

- La música va en **`musica`**, nunca en `pistas`: `pistas` comparte `amix` con la voz y
  nada la aparta.
- **Margen voz–música frase por frase**, con los buses por separado
  (`tools/margen-voz.py`): la voz entre +7 y +25 dB sobre la música. Las piezas de
  campaña apuntan a 12–18 dB y −14 LUFS finales para redes.
- Ningún efecto encima de una palabra clave (el golpe del gancho se adelantó para que
  sonara «¿Seguro?»).
- **Música con licencia verificada para Reels/TikTok:** Pixabay y Mixkit sí; la
  Biblioteca de Audio de YouTube no (solo licencia videos alojados en YouTube). Ficha
  en `assets/musica-LICENCIA.txt`. Alternativa sin terceros: música generada con
  ElevenLabs (`sound-generation`), con el prompt guardado en `assets/musica/ORIGEN.txt`.

### 6.4 Tiempos muertos: medirlos, no adivinarlos

```bash
ffmpeg -i video.mp4 -vf "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -
```

Por debajo de ~0.35 se lee como parada. Lo que más los quita: recortar cada plano a su
locución + una respiración, salidas con `power2.in` (no `expo.in`) y deriva continua del
contenido con `ease: "none"`. En la consulta PESV: de 44 ventanas muertas de 76 a 19 de 67.

### 6.5 Identidad por marca

| Marca | Fuente | Claves |
| --- | --- | --- |
| RiskMann | `docs/marca/` (PDF oficial) | `#020202`, dorado `#c8951a`, cian `#06c7fb`; Dubai; caballero y dos anillos cian + dorado; pesos mezclados en una frase |
| Yezid Ricaurte | Manual de Yezid + `yezidricaurte.com` + correos | Petróleo `#001f26`, verde `#336666`, dorado `#d2b96a`, pálido `#f1ecb0`, botón coral `#f06e49` de los correos; firma oficial en negativo, **sin redibujar**; **sin rojo** (reservado para «peligro») |
| FEGIR | Brief | Verde `#45a035`; CTA a `fegir.org`. **No hay logo oficial en el repo** |

- Los colores de un manual pensado para papel pueden no pasar contraste en pantalla
  (oliva `#80804a` = 1.75:1): variantes aclaradas **solo para texto**, el color de marca
  intacto en acentos.
- Dubai necesita `line-height` ≥ 1.5.
- En las piezas de Yezid, FEGIR no aparece en pantalla, y en las de FEGIR el CTA es
  `fegir.org`: son dos entregas distintas del mismo evento.

---

## 7. Arrancar un proyecto nuevo — lista corta

1. **Carpeta de entrada:** documento fuente, manual de marca, logo oficial (PNG/SVG real),
   fotos o permiso de usar Pixabay, lista de lo prohibido. Sin cifras reales → sin cifras.
   **Y de quién es el video** (qué marca firma y a qué dominio manda el CTA).
   Repo clonado **fuera de OneDrive**.
2. **Elegir formato** con el árbol de §2 y **copiar la plantilla** de §4.2.
3. **Identidad:** muestrear los colores del documento (no a ojo), escribir `frame.md` /
   `DIRECCION.md` / `base.py`, copiar los `.woff2`.
4. **Voz:** decidir Piper (gratis, local) o ElevenLabs (`eleven_v3`, con timestamps). Que
   el cliente escuche 2–3 voces (`tools/probar-voces.py`): el agente no puede elegir por
   oído. Perfiles y puntuación ya medidos en §6.2.
5. **Muestra de ~15 s con sonido** → aprobación.
6. **Construir el resto** contra el documento de dirección; oleadas de 2 agentes máximo.
7. **Validar:** `lint` (0 errores) → `check` («Check passed») → `snapshot` en medios,
   reposos y ±0,1 s de cada corte → mirar la hoja de contactos. En lienzo propio no hay
   `lint`/`check`: hoja de contactos con `tools/snap.mjs` y medición de tiempos muertos (§6.4).
8. **Audio:** `mezcla.py` sin «FALLO»; tres bandas a pocos dB entre sí; con música, margen
   voz–música frase por frase (§6.3).
9. **Commit y push**, y luego **render** (por partes si > ~3 min o poca RAM) → copia
   liviana `ffmpeg -crf 24–26`; para redes, `loudnorm` a −14 LUFS sobre el MP4 final.
10. **Entregar:** nombres `NN - Serie - Módulo - Título (XmYY).mp4`, `LEEME.txt` con qué
    es cada archivo y qué está pendiente, `GUION-VOZ` si habrá regrabación humana.

---

## 8. Trampas — las diez que más costaron

La lista completa está en PRODUCCION §7 y GUIA-PROMPTS §5. Si solo lees diez:

| # | Trampa | Remedio |
| --- | --- | --- |
| 1 | Cifra o afirmación inventada para «llenar» | Regla de la fuente; preguntar antes de escribir el guion |
| 2 | Construir todo antes de mostrar nada | Muestra de 15 s con sonido |
| 3 | Fuente nombrada sin `@font-face` | `.woff2` en el proyecto, siempre |
| 4 | `Math.random`, `Date.now`, CSS `transition`, `repeat:-1`, estado en `onUpdate` | Todo `fromTo` explícito en una timeline pausada |
| 5 | Máscara más estrecha que la frase: recorta palabras sin aviso | `width: max-content` y revisar cada reposo en captura |
| 6 | `visibility = "visible"` en un hijo | `"inherit"` |
| 7 | Editar HTML con regex sobre el archivo entero | Generar el HTML desde Python (`base.py`), no parchearlo |
| 8 | Render entero de 11 min en 8 GB | Voz fuera, partes, lote reanudable, matar `ffmpeg` huérfano |
| 9 | Mezcla con buen promedio y sin voz audible | Medir por bandas (>400 Hz), no el promedio |
| 10 | `Set-Content` de PowerShell | Escribir archivos con Python o la herramienta de escritura (UTF-8) |

### Las de las piezas cortas (ninguna da error: solo se ven en los fotogramas o se oyen)

La lista completa está en [`ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md) §2.

| # | Trampa | Remedio |
| --- | --- | --- |
| 11 | Música en `pistas`: tapa la voz 8–16 dB | Clave `musica` de `mezcla.py` (ducking) |
| 12 | TTS a −33 dB contra música a −14 dB | `nivelar-voz.py` a disco antes de mezclar |
| 13 | `loudnorm` dentro del `filter_complex`: devuelve silencio | Nivelar a disco; `loudnorm` solo sobre el archivo final |
| 14 | Ramas de audio de distinta duración en un `asplit`: 37 s tardan 7 min | Rellenar cada rama hasta la duración final antes de mezclar |
| 15 | `expo.in` en las salidas: se lee como tiempo muerto | `power2.in` |
| 16 | Elemento elevado a la raíz con `data-start` global: no se mueve con su plano | Al recolocar planos, auditar **todos** los `data-start` del `index.html` |
| 17 | Studio abierto mientras se escribe: añade `data-hf-id` y los anclajes dejan de coincidir | `npx hyperframes preview --stop` antes de escribir; anclar por `id` |
| 18 | Suprimir avisos del verificador en bloque (40 `content_overlap` eran ciertos) | Quitar las supresiones y ver si el error vuelve |
| 19 | Re-correr un generador de un solo uso (`fegir-envivo/tools/estudio.py`) | Borra lo editado en el Studio: después del primer uso, la fuente es `index.html` + `compositions/` |
| 20 | OneDrive borra o revierte el repo en caliente | Clonar fuera de OneDrive; commit y push antes de renderizar |

---

## 9. Huecos conocidos (para cerrar antes del próximo proyecto)

- **El extractor PPTX → `curso.json` no está en el repositorio.** Los `curso.json` de
  moto y csm existen, pero el script que los produjo no. Es la primera pieza a recuperar o
  reescribir (con `python-pptx`: nombre de forma → texto, notas → frases, medios → fotos).
- **La evaluación del curso de moto** (`Evaluacion-por-modulo.html`,
  `Preguntas-plataforma-Motociclista.xlsx`) se entregó sin su generador en el repo; el de
  csm sí está (`banco_html.py`, que además depende de un CSS de referencia externo).
- `moto.py` y `csm.py` son casi idénticos (≈90 % del código): el siguiente curso debería
  sacar lo común (`voz`, `construir`, `montar`, `tramos`, números a palabras) a `tools/` y
  dejar en cada curso solo `LIMITES`, `base.py` y `plantillas.py`.
- **Sala de control** sigue con el «100 %» sin fuente y el logo redibujado en los planos
  03 y 09: no usar comercialmente hasta corregir.
- **SOFU** (05, 06, 06b): faltan datos de contacto y validar el portafolio.

**De las piezas cortas (Alejandro y `fegir`):**

- **La receta `riskmann-hud` no corresponde al manual oficial** (`docs/marca/`), y
  `CLAUDE.md` la sigue recomendando para marketing nuevo. O se rehace contra el manual o
  se deja de recomendar.
- **El umbral del PESV está sin confirmar:** la landing dice «11 o más vehículos» y
  también «diez (10) unidades». La consulta PESV usa once. Confirmar cuál, y de qué norma
  sale, antes de dar la locución por buena.
- **La clave de ElevenLabs del issue #3 caducaba el 21-sep-2026**, y las locuciones no
  van en git: sin clave nueva no se regeneran.
- **La misma herramienta copiada en cada proyecto:** `tools/render.mjs` (seis proyectos) y
  `tools/audio.py` (cinco) viven copiados en cada proyecto de lienzo propio. Igual que
  con `moto.py`/`csm.py`, el siguiente proyecto debería sacarlos a `tools/`.
- **FEGIR no tiene logo oficial en el repo.** Si una pieza debe firmarla la Fundación,
  hace falta su archivo.
- **Varias variantes de la campaña de Yezid** (`-campana`, `-campana-v2`, `-estudio`,
  `-premium`, `-15s`) conviven sin un documento que diga cuál se aprobó. Anotarlo en un
  `LEEME` o retirar las descartadas.
- **El storyboard «LANDING INSPECCIONES GRATIS»** no está en el repo ni en el Drive: los
  anuncios siguen el texto de la landing. Si el storyboard trae frases literales, cambiar
  `js/ads.js → SCRIPTS`.
- **Fuentes Segoe UI** (`fegir-envivo*/assets/fonts/segoeui*.ttf`) son de Microsoft y
  están en el repo: confirmar licencia o cambiar a una libre (Montserrat ya está).
- **`Documentos_contexto/`** (correos de la campaña, con datos personales) vive fuera del
  repo a propósito: quien retome las campañas de Yezid lo necesita aparte.
- **La voz de RiskMann sigue sin decidir** entre siete muestras (`ENTREGABLES-VIDEO\pruebas-de-voz`).
