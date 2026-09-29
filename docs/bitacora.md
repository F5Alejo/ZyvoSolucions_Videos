# Bitácora del motor de video

Todo lo que se hace, se decide o falla en la rama `Alejodev`, en orden. Lo más nuevo va arriba.
El plan completo está en [`plan-motor.md`](plan-motor.md).

Cada entrada lleva: **Qué se hizo**, **Decisiones** (con su porqué), **Errores** (y cómo se
resolvieron) y **Pendiente**.

---

## 2026-09-29 · Arranque de la Fase 1

### Qué se hizo
- Se creó la rama `Alejodev` desde `main` (commit `7d591ae`).
- Entorno: `.venv` con Python 3.14.5; las 22 pruebas existentes pasan.
- Instalado en `.venv`: `piper-tts 1.8.0`, `onnxruntime 1.30.0`, `playwright 1.63.0` (+ Chromium),
  `num2words 0.5.14`, `kokoro-onnx 0.4.7`, `soundfile`.
- `scripts/descargar_modelos.py` baja los modelos de voz a `modelos/` (ignorada en git).
- Fuente Montserrat (SIL OFL 1.1) guardada en `motor/escenas/fuentes/` para que el render no
  dependa de internet.

### Decisiones
- **Render con Playwright + ffmpeg** (no HyperFrames ni Remotion): todo en Python, sin Node, con
  licencias conocidas. Remotion pide licencia pagada a empresas.
- **Kokoro-82M es la voz gratuita para entregar** (Apache 2.0). Voces en español: `ef_dora`
  (mujer), `em_alex` y `em_santa` (hombres). En este equipo genera ~6 s de audio en ~7 s de CPU.
- **Piper davefx solo para borradores internos.** Ver «Errores / hallazgos».
- **Fuente de los videos: Montserrat.** La ficha de RiskMann tiene abierta la contradicción
  «manual (Dubai) frente a web/app (Montserrat)»; Dubai no se puede empaquetar sin revisar su
  licencia. Si el cliente decide Dubai, se cambia en un solo lugar (`motor/escenas`).

### Errores / hallazgos
- **Licencia de Piper davefx (importante).** Su tarjeta dice que los datos en español son CC0,
  pero la voz se *afinó a partir de* `en_US-lessac`, y la licencia de Lessac (Blizzard 2013)
  prohíbe «cualquier propósito comercial», también el desarrollo de productos de voz. Fuentes:
  - https://huggingface.co/rhasspy/piper-voices/raw/main/es/es_ES/davefx/medium/MODEL_CARD
  - https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html

  El módulo PESV M01 ya se narró con esta voz: **conviene revisarlo con el cliente**.
- Probando voces desde Git Bash, `soundfile` no abre rutas `/c/...`: hay que pasarle rutas de
  Windows (`C:/...`). En el código se usa siempre `pathlib`, así que no afecta al motor.

### Pendiente
- Leer `videos/csm-curso/tools/csm.py` del repositorio de videos (hace falta `config.local.json`)
  para igualar los tiempos y las plantillas del curso csm.
- La clave de ElevenLabs caducó el 21-sep-2026 (pendiente en la ficha de RiskMann): sin ella la
  voz Carlos no se puede producir.
