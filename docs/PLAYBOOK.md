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

---

## 1. Qué se produjo

| Serie | Entrada | Formato | Salida | Proyecto(s) |
| --- | --- | --- | --- | --- |
| RiskMann «Sala de control» | Logos, iconos, capturas y 3 grabaciones de UI | Marketing, 9 planos | 68 s, muda y narrada | `videos/riskmann-sala-de-control/` |
| PESV «Pasajero seguro» · M01 | PDF de diapositivas | «Centro de mando» (voz Piper) | 2:31 — **entregable del PoC** | `videos/pesv-m01-mando/` |
| PESV · M01 corto | El mismo PDF | «Ritmo» (sin voz, 120 BPM) | 60 s, 16:9 y 9:16 | `videos/pesv-m01-ritmo[-vertical]/` |
| PESV · exploración | El mismo PDF | Partículas GPU + 3D | Apertura aprobada, resto sin construir | `videos/pesv-m01-profundidad[-vertical]/` |
| SOFU BIC S.A.S. | Guion de la empresa | Comercial | 68 s; v2 dinámica 52 s (16:9 y 9:16) | `videos/sofu-comercial/`; v2 en la rama `juan/sofu-comercial-v2` |
| «Ruta Segura» (ciclistas) | PPTX de 33 láminas con notas | Curso lámina a lámina, láminas escritas a mano (`eNN.py`) | 4 módulos, 16 min, cortados en piezas de 1–2 min | `videos/ruta-segura-m1…m4/` |
| «Motociclista laboral seguro» | PPTX de 88 láminas con **formas con nombre** | Curso **generado** por plantillas | 15 videos, 40:47 | `videos/moto-curso/` → `moto-*` |
| «Conducción Segura y Manejo Defensivo» | PPTX de 55 láminas | Curso **generado** por plantillas | 15 videos, ~33 min + banco de preguntas | `videos/csm-curso/` → `csm-*` |

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

**La lección de fondo:** el primer video de un formato cuesta un día; el segundo, una
hora; con el formato convertido en generador, un módulo cuesta lo que tarda su render.

---

## 2. Elegir el formato

```
¿Qué te entregan?
├─ Assets sueltos de un producto (logo, capturas, grabaciones) ─→ Marketing (PRODUCCION §1–§8)
├─ Un guion comercial de la empresa ────────────────────────────→ Comercial (modelo: sofu-comercial)
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

Estas siete prácticas son las que más tiempo ahorraron. Ninguna depende de RiskMann.

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

---

## 4. Las piezas reutilizables

### 4.1 Herramientas compartidas (`tools/`, no cambian entre proyectos)

| Script | Entrada | Cuándo |
| --- | --- | --- |
| `voz.py` | `guion.json` | Voz local gratuita (Piper `es_ES-davefx-medium`); avisa si una línea no cabe |
| `descargar-voz.py` | — | Una vez por equipo: baja y verifica el modelo Piper |
| `ritmo.py` | `ritmo.json` | Pista rítmica sintetizada a un BPM, sin derechos de terceros |
| `mezcla.py` | `mezcla-*.json` | Voz + pistas + cama + efectos, −16 LUFS, **falla si la voz no está** |
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
| Marketing | `npx hyperframes init` + receta `riskmann-hud` | ver PRODUCCION §6 |

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

## 6. Arrancar un proyecto nuevo — lista corta

1. **Carpeta de entrada:** documento fuente, manual de marca, logo oficial (PNG/SVG real),
   fotos o permiso de usar Pixabay, lista de lo prohibido. Sin cifras reales → sin cifras.
2. **Elegir formato** con el árbol de §2 y **copiar la plantilla** de §4.2.
3. **Identidad:** muestrear los colores del documento (no a ojo), escribir `frame.md` /
   `DIRECCION.md` / `base.py`, copiar los `.woff2`.
4. **Voz:** decidir Piper (gratis, local) o ElevenLabs (`eleven_v3`, con timestamps). Que
   el cliente escuche 2–3 voces: el agente no puede elegir por oído.
5. **Muestra de ~15 s con sonido** → aprobación.
6. **Construir el resto** contra el documento de dirección; oleadas de 2 agentes máximo.
7. **Validar:** `lint` (0 errores) → `check` («Check passed») → `snapshot` en medios,
   reposos y ±0,1 s de cada corte → mirar la hoja de contactos.
8. **Audio:** `mezcla.py` sin «FALLO»; tres bandas a pocos dB entre sí.
9. **Render** (por partes si > ~3 min o poca RAM) → copia liviana `ffmpeg -crf 24–26`.
10. **Entregar:** nombres `NN - Serie - Módulo - Título (XmYY).mp4`, `LEEME.txt` con qué
    es cada archivo y qué está pendiente, `GUION-VOZ` si habrá regrabación humana.

---

## 7. Trampas — las diez que más costaron

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

---

## 8. Huecos conocidos (para cerrar antes del próximo proyecto)

- **El extractor PPTX → `curso.json` no está en el repositorio.** Los `curso.json` de
  moto y csm existen, pero el script que los produjo no. Es la primera pieza a recuperar o
  reescribir (con `python-pptx`: nombre de forma → texto, notas → frases, medios → fotos).
- **«SOFU comercial v2» vive en otra rama** (`juan/sofu-comercial-v2`, sin fusionar): en
  esta rama `videos/sofu-comercial-v2*/` solo tiene renders.
- **La evaluación del curso de moto** (`Evaluacion-por-modulo.html`,
  `Preguntas-plataforma-Motociclista.xlsx`) se entregó sin su generador en el repo; el de
  csm sí está (`banco_html.py`, que además depende de un CSS de referencia externo).
- `moto.py` y `csm.py` son casi idénticos (≈90 % del código): el siguiente curso debería
  sacar lo común (`voz`, `construir`, `montar`, `tramos`, números a palabras) a `tools/` y
  dejar en cada curso solo `LIMITES`, `base.py` y `plantillas.py`.
- **Sala de control** sigue con el «100 %» sin fuente y el logo redibujado en los planos
  03 y 09: no usar comercialmente hasta corregir.
- **SOFU** (05, 06, 06b): faltan datos de contacto y validar el portafolio.
