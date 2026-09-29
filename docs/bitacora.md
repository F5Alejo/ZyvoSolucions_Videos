# Bitácora del motor de video

Todo lo que se hace, se decide o falla en la rama `Alejodev`, en orden. Lo más nuevo va arriba.
El plan completo está en [`plan-motor.md`](plan-motor.md).

Cada entrada lleva: **Qué se hizo**, **Decisiones** (con su porqué), **Errores** (y cómo se
resolvieron) y **Pendiente**.

---

## 2026-09-29 · Unión con `main` (interfaz nueva en Vue 3)

### Qué se hizo
- `origin/main` recibió un *force push*: el commit inicial se reescribió (`7d591ae` → `7b04806`,
  con los mismos archivos) y encima llegó «Rehacer la interfaz con Vue 3, TypeScript y
  Tailwind» (`51aad05`). El servidor pasó a ser una API JSON y se borraron las plantillas Jinja.
- `Alejodev` se movió encima de `7b04806` (`git rebase --onto`, sin conflictos) y luego se unió
  con `origin/main`.
- **Conflictos resueltos:**
  - `app/templates/taller.html`, `app/static/app.js` y `app/static/estilo.css`: se aceptó el
    borrado; lo que hacían ahora está en Vue.
  - `app/main.py`: se tomó la API nueva y se le añadieron las rutas del motor:
    `GET /api/trabajos/{id}/produccion`, `POST /api/trabajos/{id}/producir/{clave}` (202) y
    `GET /api/trabajos/{id}/salida/{clave}/{archivo}`. `/api/catalogo` dice por cada voz qué le
    falta para producir (`falta`).
  - `app/extractor.py`: se conservaron `guardar_imagenes` y las nuevas reglas de título y sección.
  - `README.md`: el de `main` más la fila del motor y su instalación.
- **Ajustes por la reorganización:**
  - el logo de RiskMann se movió a `frontend/public/marca/` y se actualizó `logo_local` en su ficha;
  - las escenas usan `extractor.titulo_lamina` (forma «title») y no repiten el título ni la sección en las viñetas;
  - `main` quitó `jinja2` de `requirements.txt`, pero el motor lo usa, así que se volvió a añadir en la sección del motor.
- **Vue:**
  - `PasoResultado.vue` tiene el botón «Producir video», el progreso cada 3 s, el reproductor con subtítulos, la calidad y las descargas, y avisa si la voz falta, es de borrador o si el video quedó desactualizado;
  - `PasoMarcaVoz.vue` avisa qué le falta a cada voz;
  - se añadieron los tipos en `tipos.ts`.
- **Verificado:**
  - 34 pruebas de Python, `vue-tsc`, 7 pruebas de Vitest y `npm run build`;
  - en vivo: el curso demo se produjo con Carlos (ElevenLabs), con todos los chequeos en verde.

### Errores y cómo se resolvieron
- Unir directamente fallaba porque las historias no tenían ancestro común (el commit inicial fue
  reescrito). Se resolvió con `git rebase --onto 7b04806 7d591ae` antes de unir.

---

## 2026-09-29 · Commits sin coautoría y subida de la rama

### Qué se hizo
- A pedido del usuario, se quitó la línea `Co-Authored-By` de los 10 commits de `Alejodev`
  (`git filter-branch --msg-filter`). Aún no se habían subido. Los archivos no cambiaron: el
  árbol es el mismo (`de8e346`). Desde ahora los commits van sin esa línea.
- Revisado antes de subir: ningún commit trae `.env`, la clave, `modelos/` ni `datos/trabajos/`.

### Pendiente
- Subir la rama: `git push -u origin Alejodev`. El asistente no tiene permiso para hacer push;
  lo corre el usuario.

---

## 2026-09-29 · Clave de ElevenLabs y manejo de secretos

### Qué se hizo
- La clave nueva de ElevenLabs quedó en `interfaz/.env`, que **no va a git**. `.gitignore` ignora
  `.env` y `.env.*`, salvo la plantilla `.env.ejemplo`, que sí va y no trae ninguna clave.
- `app/datos.py` lee `.env` al arrancar (`_cargar_env`), sin dependencias nuevas. Una variable
  de entorno del sistema manda sobre el archivo.

### Decisiones
- **Las claves nunca se escriben en el código, en `docs/` ni en los mensajes de commit.** Si
  hay que citar una, se dice «la clave de ElevenLabs de `.env`».
- La clave se compartió por chat: conviene **rotarla** en el panel de ElevenLabs cuando se pueda
  y actualizar solo `.env`.

---

## 2026-09-29 · Fase 1: el primer MP4 que se puede subir

### Qué se hizo
- **Paquete `motor/`**, un módulo por paso:
  - `normalizar.py`: leyes, cifras, pesos, porcentajes, ordinales, radicados y siglas en palabras.
  - `voz.py`: audio por frase con caché por (voz + texto); proveedores Kokoro, Piper y ElevenLabs; `disponible()` dice qué falta.
  - `escenas/`: plantilla HTML de marca (portada, lista, imagen) y el color de la marca con contraste medido.
  - `render.py`: Playwright dibuja 1,2 s de entrada por lámina y ffmpeg sostiene el último cuadro.
  - `audio.py`: pista de narración y volumen a -14 LUFS.
  - `subtitulos.py`: VTT y SRT a partir del guion y de los tiempos reales.
  - `qa.py`: resolución, formato, sincronía, volumen, pantallas negras y silencios.
  - `produccion.py`: encadena los pasos.
  - `cola.py`: un video a la vez, en segundo plano.
- **Taller:**
  - las imágenes del PPTX se guardan en `media/` al crear el trabajo;
  - la sección «Resultado» tiene el botón «Producir video», el progreso en vivo, el reproductor con subtítulos, el control de calidad y las descargas (MP4, VTT y SRT);
  - avisa si la voz elegida no se puede usar o si es solo para borradores;
  - avisa si el video se produjo con otra marca o voz.
- **Rutas nuevas:**
  - `POST /taller/{id}/producir/{clave}`;
  - `GET /taller/{id}/render`;
  - `GET /taller/{id}/salida/{clave}/{archivo}`, que solo entrega el mp4, el vtt, el srt y `qa.json` de ese video.
- **Voces:** Dora, Alex y Santa (Kokoro) en `datos/voces.json`. Piper davefx queda marcada con `solo_borrador` y sus videos salen con el sello «BORRADOR».
- **RiskMann:** su ficha trae un bloque `video` (capa manual: negro, dorado y cian). Las demás marcas deducen sus colores de la paleta, con contraste de al menos 4,5:1 para el texto.
- **Pruebas:** 32 en total (10 del motor), en unos 27 s.
- **Prueba real:** un PPTX de 3 láminas con la voz Kokoro produce un video de 25 s en 43 s, con todos los chequeos en verde. Por la interfaz, uno de 11 s tarda 22 s.

### Decisiones
- **El estado de producción va en `salida/<clave>/estado.json` y no en `trabajo.json`**, para que el hilo del motor no pise lo que la persona guarda mientras tanto. Si el servidor se reinicia a mitad de una producción, la tarjeta lo dice y ofrece volver a producir.
- **Tiempos de csm.py:** el título entra 1,0 s antes de la voz; 0,35 s entre frases; 1,3 s de respiro al final. La línea de tiempo se redondea a cuadros exactos (30 fps) para que la imagen y la voz no se separen.
- **Los subtítulos usan el guion tal cual** («Ley 1503 de 2011»), no el texto normalizado para la voz.
- **Formato de entrega:**
  - video: 1920×1080 a 30 fps, H.264 High, `yuv420p`, CRF 18;
  - audio: AAC estéreo a 48 kHz y 192 kbps;
  - `+faststart` para la web.
- La portada lleva como antetítulo el nombre del curso. Antes repetía el título, porque el video toma su nombre de la primera lámina.

### Errores y cómo se resolvieron
- **El volumen quedaba en -15,2 LUFS en vez de -14.** Había dos causas:
  1. `loudnorm` en modo `linear` pasa a modo dinámico cuando la ganancia choca con el límite de picos, y se queda corto.
  2. Pasar de mono a estéreo al final sube unos 3 dB la sonoridad medida.

  **Solución:** convertir a estéreo antes de medir, aplicar ganancia lineal con `alimiter` a -2 dBFS y repetir hasta quedar a ±0,3 LUFS. Resultado: -14,09 LUFS con pico de -1,92 dBTP.
- En la tarjeta del video, la regla `.videos-plan` (170 px) pisaba la nueva, que venía antes en el CSS. Se subió la especificidad (`.videos-plan.salida-videos`).

### Pendiente (siguientes fases, ver plan)
- No hay música: falta elegir pistas con licencia comercial (Pixabay o YouTube Audio Library) y guardar su licencia.
- La transcripción de control con faster-whisper no está: se deja para cuando haga falta (pesa y es opcional).
- Mientras habla la voz, la lámina queda quieta: falta movimiento suave (Fase 3, con más plantillas).
- Los logos de FEGIR, SOFU y Yezid están en el repositorio de videos. Sin `config.local.json` se escribe el nombre de la marca en su lugar.
- El curso csm de ejemplo no tiene imágenes (su PPTX no está en el repositorio).
- El chequeo informativo «Duración frente a la estimada» se ve con «!» como si hubiera que revisarlo; convendría un estilo «informativo».
- Fase 2: editar el guion en la interfaz y conectar la aprobación con `proyectos.json`.

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
