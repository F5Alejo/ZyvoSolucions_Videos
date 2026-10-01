# Bitácora del motor de video

Todo lo que se hace, se decide o falla en la rama `Alejodev`, en orden. Lo más nuevo va arriba.
El plan completo está en [`plan-motor.md`](plan-motor.md).

Cada entrada lleva: **Qué se hizo**, **Decisiones** (con su porqué), **Errores** (y cómo se
resolvieron) y **Pendiente**.

---

## 2026-10-01 · Fases 6 y 7: errores con código, reintentos, voz de respaldo, registro técnico y detector de bugs

### Qué se hizo
- **`motor/errores.py`:** cada falla se clasifica con un código estable (`PPTX_001`, `TTS_001`, `TTS_002`, `RENDER_001`, `AUDIO_001`, `VIDEO_001`, `SPEC_001`, `QA_001`, `MOTOR_001`…), una severidad (CRITICAL a INFO), un mensaje para la persona y una recuperación sugerida.
- **Reintentos (`produccion.correr`):** la voz se reintenta hasta 3 veces y las escenas hasta 2, **solo** si la falla es pasajera (red, ElevenLabs 5xx o 429, el navegador que se cayó). Un ffmpeg con datos malos o una clave que falta no se reintentan.
- **Voz de respaldo:** si ElevenLabs falla, el video entero se rehace con la primera voz Kokoro lista (nunca Piper) y el informe lo dice (`respaldo_voz` y un aviso). Se apaga con `audio.respaldo_voz`.
- **Registro técnico (`motor/logs.py`):** una línea JSON por evento en `datos/trabajos/<id>/logs/<clave>.jsonl`, con etapa, intento, código, severidad y *traceback*. `GET /api/trabajos/{id}/diagnostico/{clave}` lo entrega para el modo diagnóstico. La interfaz nunca recibe el *traceback*.
- **Fases del pipeline** en `estado.json` y en la API: QUEUED, SCRIPTING, SCRIPT_READY, GENERATING_AUDIO, AUDIO_READY, BUILDING_SCENES, SCENES_READY, RENDERING, RENDERED, QA_RUNNING, QA_PASSED / QA_FAILED, COMPLETED y FAILED.
- **Control de calidad:** cada chequeo lleva un `id` estable. Nuevos: «El audio no se satura» (pico por debajo de -0,1 dBFS), «Textos sin caracteres extraños» y «Todas las láminas e imágenes están en el video».
- **Detector de bugs (`motor/bugs.py`):** cada chequeo fallido se vuelve un bug con código, severidad, escena y recuperación, ordenados de más a menos grave, en `qa.json["bugs"]`. No corrige nada solo.
- Pruebas: 86 (`tests/test_robustez.py`).

### Errores y cómo se resolvieron
- **El commit `e3eea68` dejó Actions en rojo:** al pasar `datos_copia` a `conftest.py` se quitó `ORIGEN` de `test_motor.py`, que importan otras tres pruebas. Después de ese cambio solo se había corrido un subconjunto. Se arregló en `1d2071e`. Lección: correr **todas** las pruebas después del último cambio, no antes.

### Decisiones
- **No se detectan «cuadros congelados»:** una lámina quieta mientras habla la voz es a propósito, así que `freezedetect` marcaría casi todo el video. Las pantallas negras y los silencios largos sí se detectan.

---

## 2026-10-01 · Fases 2, 3 y 6: VideoSpec, producción por etapas y caché de escenas

### Qué se hizo
- **`motor/videospec.py`:** el contrato de un video en Pydantic (versión 1). `construir()` arma el plan con duraciones estimadas (`videospec.plan.json`); `resolver()` le pone el audio a cada frase y fija cada escena en cuadros exactos (`videospec.json`). Se valida esquema, catálogo y coherencia; `sanear()` cambia lo desconocido por el valor por defecto con el aviso `INVALID_EFFECT`. Ver `docs/videospec.md`.
- **`motor/catalogo.py`:** catálogos cerrados de cámara y transición (por ahora `estatica` y `corte`, lo que el render ya sabe hacer).
- **`motor/produccion.py` por etapas:** plan → voz → escenas → audio → subtítulos → QA, todas sobre el VideoSpec. Los tiempos son los mismos de antes.
- **Caché de escenas (`salida/<clave>/escenas/<huella>.mp4`):** cada escena dibujada se guarda con un hash de su HTML y sus ajustes. Si se edita una lámina, solo esa escena se vuelve a dibujar; las que ya no se usan se borran.
- **`motor/recursos.py`:** `logo()` y `media()` dejaron de ser funciones privadas de `produccion` que importaban `main.py` y `empaquetar.py`. `escenas` usa `extractor.seccion_lamina` en vez de `_forma` y `_SECCION`.
- `qa.json` trae además cámara y transición por lámina, los avisos del VideoSpec y su nombre de archivo.
- `tests/conftest.py` con el fixture `datos_copia` compartido. Pruebas: 80 (4 nuevas en `tests/test_videospec.py`).

### Decisiones
- **Las escenas se cachean por su HTML, no por el número de lámina:** el HTML ya incluye texto, imagen, colores, animación y duración, así que cualquier cambio que se vea invalida solo esa escena.

---

## 2026-10-01 · Línea base, voz inicial que funciona e instalador sin preguntas colgadas

### Qué se hizo
- **Línea base en este equipo:** Python 3.12.10 y ffmpeg 9.0.2 instalados para el usuario, luego `instalar.ps1 -Probar`: pytest 75/75, Vitest 10/10, `vue-tsc` y ruff sin avisos.
- **Voz inicial (`taller.voz_inicial`):** un curso nuevo toma la voz de la configuración solo si el equipo la puede usar; si no, la primera que se pueda entregar (Kokoro sin clave de ElevenLabs). Nunca Piper. Si ninguna está lista, queda la de la configuración y el taller dice qué falta.
- **Instalador:** no pregunta la clave de ElevenLabs cuando nadie puede responder.
- Pruebas: 76 (una nueva para la voz inicial).

### Errores y cómo se resolvieron
- **`instalar.ps1` se quedaba esperando para siempre** en «Pega la clave de ElevenLabs» al correr sin ventana: `Read-Host` no lanza error, espera. Ahora solo pregunta si la sesión es interactiva, la entrada no está redirigida y no se pasó `-NonInteractive`.
- Dos pruebas daban por hecho que la voz de un curso nuevo es Carlos: ahora la eligen de forma explícita.

---

## 2026-10-01 · Fase 1 del prompt maestro: análisis y plan de arquitectura

### Qué se hizo
- `ARCHITECTURE.md` en la raíz: la arquitectura actual frente al objetivo (VideoSpec, pipeline por etapas, agentes, proveedores), los problemas encontrados, las decisiones y el plan de migración por fases. No se cambió código.

### Decisiones (aceptadas por el usuario)
- **Remotion no entra** salvo que se compre su licencia: se crea `VideoRenderer` con el renderer actual (Playwright + ffmpeg) como principal.
- **Respaldo de voz: ElevenLabs → Kokoro.** Piper davefx sigue solo para borradores, nunca como respaldo de un video final.
- **Nombres nuevos (`VideoSpec`, `TTSProvider`, `VideoRenderer`) dentro de `motor/` y `app/`**; la reorganización de carpetas se deja para cuando el pipeline ya esté en etapas.
- **SFX:** solo con archivos de licencia comercial clara, guardada al lado.

### Pendiente
- Línea base de pruebas en este equipo (no tenía Python ni ffmpeg).
- Fase 0b: voz por defecto que funcione en un equipo nuevo (Carlos depende de una clave caducada).

---

## 2026-10-01 · `main` protegida, primer PR y ajustes de Dependabot

### Qué se hizo
- **Regla «Proteger main»** (ruleset 24305825, creada con `gh api`):
  - exige pull request (0 aprobaciones: hay un solo desarrollador y GitHub no deja aprobar el PR propio);
  - exige que pasen «API y motor (pytest)», «Interfaz (tipos, Vitest y compilación)», «Estilo (ruff)» y «Secretos (gitleaks)»;
  - solo fusión con *merge*, y bloquea el *force push* y el borrado.
- **Comprobado:** un `git push origin Alejodev:main` directo es rechazado («push declined due to repository rule violations») y `main` no cambia.
- **Primer PR** (#1, «GitHub Actions completo y documentación»): los 4 trabajos en verde, fusionado con *merge* (`ae394ed`). Después `Alejodev` se adelantó a `main` para quedar iguales. «Pruebas» también pasó en `main` después de la fusión.
- **Dependabot** arrancó al llegar su configuración a `main` y abrió PR hacia `Alejodev`: 5 de pip y uno de npm (TypeScript 7).

### Errores y cómo se resolvieron
- **Los PR de Dependabot no se probaban:** «Pruebas» solo se activaba con PR hacia `main`. Ahora también con PR hacia `Alejodev`.
- **Ruido de pip:** abrió un PR por paquete solo para subir el mínimo de `requirements.txt` (p. ej. `fastapi>=0.115` a `>=0.141.1`), aunque los `>=` ya admitían esas versiones. Con `versioning-strategy: increase-if-necessary` solo propone algo cuando una versión queda fuera del rango. Los PR #3 a #7 se cerraron por eso.

- **TypeScript 7 (PR #2):** las pruebas lo atraparon. «Interfaz» falla porque `vue-tsc` todavía no funciona con TypeScript 7 (`ERR_PACKAGE_PATH_NOT_EXPORTED`: no encuentra `./lib/tsc`). Se cerró el PR y Dependabot ya no propone versiones mayores de TypeScript. Hay que quitar esa excepción de `dependabot.yml` cuando `vue-tsc` lo soporte.

---

## 2026-10-01 · GitHub Actions completo y documentación de lo encontrado

El usuario decidió terminar GitHub Actions antes de pasar a la nube. El plan de nube quedó
documentado en [`plan-nube.md`](plan-nube.md) como siguiente etapa.

### Qué se hizo
- **Avisos corregidos:**
  - el runner queda fijo en `ubuntu-24.04` (`ubuntu-latest` pasa a Ubuntu 26 el 19-oct);
  - `lucide-vue-next` (obsoleto) pasa a `@lucide/vue`, sin cambiar los nombres de los íconos;
  - se suma `httpx2`, el cliente que Starlette usa en sus pruebas si está instalado (`import httpx2 as httpx`); es de Tom Christie, el autor de httpx, con licencia BSD-3;
  - Chromium queda en caché.
- **Estilo con ruff:**
  - `pyproject.toml` con las reglas E, F e I y líneas hasta 140 (el estilo que ya tiene el código);
  - E741 se ignora porque `l` es «lámina» en todo el proyecto;
  - se corrigieron 13 problemas automáticamente (imports ordenados y uno sin usar) y 11 líneas largas a mano.
- **Secretos:** gitleaks revisa toda la historia en cada push y PR. Es gratis en cuentas personales y no pide licencia.
- **Dependabot:** cada lunes, PR agrupados hacia `Alejodev` para pip, npm y las acciones.
- **Video de muestra:** la prueba de punta a punta guarda su MP4, VTT, SRT y `qa.json` cuando existe `GUARDAR_MUESTRA`. El flujo los sube como artefacto `video-de-muestra` (14 días). Comprobado: H.264 1920×1080 con AAC, 14 s.
- **Instalador en Windows** (`instalador-windows.yml`, `windows-2025`):
  - Python 3.12, Node 22 y ffmpeg estático de gyan.dev;
  - corre `instalar.ps1 -SinModelos -Probar` con Windows PowerShell 5.1;
  - corre cada lunes, a mano y cuando cambian el instalador o las dependencias;
  - **primera ejecución en verde en 3 min**: instaló todo y pasaron 75 pruebas de pytest y 10 de Vitest.
- **«Pruebas»** quedó con 4 trabajos en verde: API y motor (75 pruebas en 50 s, sin avisos), Interfaz, Estilo y Secretos.
- **Documentación nueva:**
  - [`arquitectura-actual.md`](arquitectura-actual.md): cómo funciona hoy;
  - [`hallazgos.md`](hallazgos.md): cada problema con su causa y su solución;
  - [`plan-nube.md`](plan-nube.md): arquitectura en cuatro piezas, herramientas, prueba 100 % gratuita en Oracle Cloud Always Free, y SaaS y escala;
  - [`README.md`](README.md): índice;
  - el README principal suma las insignias de Actions y la sección «GitHub Actions y ramas».

### Decisiones
- `main` se protege con una regla (*ruleset*): solo por PR desde `Alejodev`, con los 4 trabajos de «Pruebas» en verde, sin *force push* y sin borrado. Ver la siguiente entrada.
- En el flujo de Windows se copia `.env.ejemplo` a `.env` antes de instalar: en Actions nadie escribe la clave y el instalador no debe quedarse preguntando.

---

## 2026-09-30 · GitHub Actions: pruebas en cada cambio

### Qué se hizo
- `.github/workflows/pruebas.yml` con dos trabajos en Ubuntu:
  - **API y motor:** Python 3.12, ffmpeg por apt, Chromium de Playwright (`--with-deps`) y `pytest`;
  - **Interfaz:** Node 22, `npm ci`, `vue-tsc`, Vitest y la compilación.
- **Se activa:**
  - en cada push a `Alejodev`, la rama de pruebas y mejoras;
  - en cada push a `main` y en cada pull request hacia `main`;
  - a mano, desde la pestaña Actions (`workflow_dispatch`).

  Si llega un push nuevo a la misma rama, se cancela la ejecución anterior.
- README: sección «GitHub Actions y ramas».

- **Primera ejecución en verde:** 75 pruebas de pytest (con ffmpeg 7.0.2 estático y Chromium, sin saltarse ninguna) y 10 de Vitest, en unos 2 minutos. Actions ya estaba activado en el repositorio (Settings → Actions → General: «Allow all actions»); no hizo falta cambiar nada ahí.

### Errores y cómo se resolvieron
- **`apt-get` se colgó más de 20 min instalando ffmpeg** en la primera ejecución. Se canceló, y ahora se descarga la versión estática de johnvansickle.com (un archivo), con `apt` de respaldo y un tiempo límite de 5 min. Chromium se instala sin `--with-deps`, que también usa `apt`: las imágenes de Ubuntu de GitHub ya traen sus librerías.
- **GitHub avisó que las acciones en v4 usan Node 20, que está obsoleto.** Se pasaron a `actions/checkout@v7`, `actions/setup-python@v7` y `actions/setup-node@v7`.

### Pendiente
- `ubuntu-latest` pasa a Ubuntu 26 el 19-oct-2026. Si algo falla ese día, fijar `runs-on: ubuntu-24.04`.

### Decisiones
- **Las pruebas no necesitan secretos en GitHub:** usan una voz de prueba y Ollama simulado, así que no hace falta subir la clave de ElevenLabs a los *secrets* del repositorio.
- **Flujo de ramas:** se trabaja en `Alejodev` y `main` se actualiza desde `Alejodev` solo con las pruebas en verde.

---

## 2026-09-30 · Rama `Alejodev` en ZyvoSolucions_Videos

- El desarrollo sigue en este repositorio. Se creó la rama `Alejodev` desde `main` (`59cf9da`) y se subió.
  Como antes: se trabaja en `Alejodev`, con un commit por tema y sin coautoría, y `main` solo se
  actualiza cuando se pide, con las pruebas en verde y con un avance directo.
- El servidor local se deja en su propia ventana de PowerShell («Estudio de video - localhost:8765»),
  para que no lo corte el tiempo máximo de las tareas en segundo plano del asistente.

---

## 2026-09-30 · El proyecto pasa a `F5Alejo/ZyvoSolucions_Videos`

### Qué se hizo
- Se copió el contenido de `main` del repositorio `interfaz` (commit `2c42a15`: 112 archivos) con
  `git archive`, que solo lleva lo que está en git. No pasaron `.env`, `.venv`, `node_modules`,
  `dist`, `modelos/` ni el material de clientes (`datos/trabajos/`).
- Por decisión del usuario el repositorio nuevo empieza con **commits nuevos por tema**, sin la
  historia de `interfaz`. Esa historia sigue en `github.com/juanezzzzz/interfaz`.
- El README apunta al repositorio nuevo para clonar.
- **Probado como un equipo recién clonado:** `instalar.ps1 -ConAgentes -Probar` creó un `.venv`
  propio, instaló todo, compiló la interfaz y pasaron 75 pruebas de pytest y 10 de Vitest (salida
  con código 0). Con el servidor encendido respondieron las pantallas, la API y el diagnóstico
  (ffmpeg, Chromium, voces, clave y Ollama).
- En este equipo se copiaron a mano `modelos/` y `.env`, para no volver a bajar las voces ni pedir la clave.
  Los dos siguen fuera de git.

---

## 2026-09-30 · `main` actualizada con todo lo de `Alejodev`

### Qué se hizo
- A pedido del usuario se revisaron todas las ramas del remoto: solo existen `main` y `Alejodev`.
  `Alejodev` contenía todo lo de `origin/main` (la interfaz en Vue, `51aad05`) más 19 commits.
- Antes de tocar `main` pasaron 75 pruebas de pytest, `vue-tsc`, 10 pruebas de Vitest y la compilación.
- `main` se actualizó con un avance directo (`git push origin Alejodev:main`): sin forzar, sin
  reescribir historia y sin conflictos. El `main` local, que seguía en la historia anterior al
  *force push* (`7d591ae`), se puso al día con `origin/main`.

### Decisiones
- Se sigue trabajando en `Alejodev`. `main` se actualiza solo cuando el usuario lo pide y
  siempre con un avance directo, después de pasar las pruebas.

---

## 2026-09-30 · Frente C (y B4): agentes locales que proponen mejoras

### Qué se hizo
- **Base (`motor/agentes/`):**
  - `ollama.py` es el cliente: salida JSON con esquema, `think: false`, `temperature` 0,2, y el modelo se descarga al terminar cada agente;
  - `guardas.py` descarta cualquier propuesta que traiga una cifra o una norma que no esté en la lámina;
  - `base.py` tiene el registro, la ejecución en la cola y las propuestas (pendiente, aceptada o descartada), y guarda con qué se hizo cada una (el modelo, «reglas» o «whisper small»).
- **Ediciones del curso** (`trabajo["ediciones"]`): título, viñetas y narración corregidos, sin tocar el original del PPTX. Las usan el resumen, las escenas y `curso.json`. En el paso Guion cada lámina tiene «Editar» y «Original».
- **Los 8 agentes:**

  | Agente | Con IA | Sin IA |
  | --- | --- | --- |
  | Redactor de pantalla | `qwen3:4b` | Recorta a 8 y 10 palabras |
  | Guionista | `qwen3:4b` | Arma la narración con título y viñetas |
  | Verificador normativo | — | Clasifica cada cita, la cruza con los pendientes de la marca y, al aceptarla, queda como «fuente revisada» en el chequeo |
  | Director de animación (B4) | `qwen3:4b`, en lotes de 10 láminas y solo con listas cerradas del catálogo | Cifra → escalar; portada → palabra por palabra; muchas viñetas → más seguidas; imagen → revelar |
  | Evaluador | `qwen3:4b` (sin IA no corre) | — |
  | Publicador | `qwen3:4b` | Plantilla de texto; los capítulos son los reales |
  | Descriptor de imágenes | `qwen3.5:2b` con visión | Imágenes pequeñas o muy alargadas = adorno; si no es contenido, la escena no la usa como foto |
  | Revisor de voz | faster-whisper `small` en int8 | — |

  El Revisor de voz transcribe el MP4 y lo compara con el guion; los dos textos se normalizan igual.
- **Exportes:** el banco de preguntas sale en GIFT y Moodle XML (`/banco.gift` y `/banco.xml`), y el ZIP incluye `publicacion.md` y el banco en los dos formatos.
- **Interfaz:**
  - `PanelAgentes.vue` en Presentación, Guion, Animación y Resultado: proponer, ver el avance y cada propuesta con su «ahora» y su «propuesta», aceptar, descartar o aceptar todas;
  - Configuración muestra qué agentes tienen IA hoy.
- `instalar.ps1 -ConAgentes` baja los modelos de Ollama.
- **Pruebas:** `tests/test_agentes.py` (13) con Ollama simulado.
- **Probado con los modelos reales** en el curso demo:
  - Redactor, 22 s; Director, 25 s; Publicador, 32 s; Evaluador, 32 s; Descriptor (visión), 59 s;
  - Revisor de voz, 5 s (más la descarga única del modelo), con 100 % de coincidencia.

### Decisiones
- **Nada se aplica solo.** Aceptar una propuesta es lo que cambia el curso, y el cambio queda como edición: siempre se puede volver al original.
- **Los agentes van en la cola de los renders.** El equipo tiene 8 GB y un modelo de 4 B más Chromium no caben juntos con holgura.
- **El Director no puede inventar efectos:** el esquema JSON solo admite los del catálogo, y lo que no valida cae a las reglas.

### Errores y cómo se resolvieron
- **Con `keep_alive: 0` Ollama recargaba el modelo en cada pregunta** (Redactor: 79 s para 2 láminas). Ahora el modelo queda cargado 2 min mientras trabaja el agente y se descarga al terminar (`ollama.descargar`): 22 s. `ollama ps` confirma que no queda en memoria.
- **faster-whisper 1.2.1 falla al leer audio con la versión de PyAV instalada** («unexpected keyword argument 'metadata_errors'»). El audio se decodifica con ffmpeg y se pasa como muestras.
- **El Revisor de voz daba un falso 73 %:** Whisper escribe «1503» y el guion «mil quinientos tres». Ahora la transcripción pasa por la misma normalización.
- **La guarda contaba dos veces la misma cifra** (como cifra y como norma). Una norma solo se marca si sus números ya estaban pero el texto cambió («Decreto 1503» donde decía «Ley 1503»). Además compara sin espacios («30%» = «30 %»).
- **`instalar.ps1` estaba en git con `\r\r\n`** (una conversión de saltos de línea anterior); PowerShell lo toleraba. Se corrigió, y `.gitattributes` fija `*.ps1` en CRLF.
- **Bash no aceptó un script largo en línea** («unexpected EOF»). Los scripts largos se guardan en la carpeta temporal y se ejecutan desde ahí.

---

## 2026-09-30 · Frente B3: editor de animación con vista previa en vivo

### Qué se hizo
- **API:**
  - `GET /api/animaciones`: plantillas y catálogo (efectos por elemento, curvas y límites);
  - `POST /api/animaciones` para guardar una plantilla propia, y `DELETE` solo para las propias;
  - `GET` y `PUT /api/trabajos/{id}/animacion`, validado contra el catálogo.
- **Vista previa:** `POST /api/trabajos/{id}/escena/{n}` devuelve el HTML de la lámina con **lo que se está editando, sin guardar**, en bucle (entrada, 1,6 s quieta y salida). La fuente, el logo y las imágenes se sirven por la API (`/api/escenas/fuente.ttf`, `/api/escenas/logo/{marca}` y `/api/trabajos/{id}/media/{nombre}`, solo imágenes de esa carpeta).
- **Paso nuevo «Animación»** (5 pasos en el curso), en `PasoAnimacion.vue`:
  - estilos para elegir y alcance («Todo el curso» o «Solo la lámina N», marcando las láminas con animación propia);
  - editor por elemento con pestañas Entrada y Salida: efecto, curva, duración, espera o adelanto y separación entre viñetas o palabras;
  - botón de restaurar, «Guardar como plantilla nueva» y vista previa escalada con `ResizeObserver`.
- `utils.ts`: `resolverAnimacion` y `fijarAjuste` (la misma lógica por capas que el servidor), con pruebas de Vitest.

### Errores y cómo se resolvieron
- **`structuredClone` falla con los objetos reactivos de Vue** («#<Object> could not be cloned»). Afectaba también a «Ajustes de este curso» del paso Marca y voz, sin que se hubiera notado. Se cambió por `clonar()` (copia por JSON) en todo el frontend.
- **La vista previa corre en un iframe aislado** (`sandbox`, origen «null»), así que el navegador bloqueaba la fuente por CORS. La ruta de la fuente, que es pública (OFL), responde `Access-Control-Allow-Origin: *`.
- Al probar con Playwright desde la terminal, la tilde de «Cinética» llegaba dañada. Se busca por el valor (`cinetica`).

---

## 2026-09-30 · Frente B1/B2: plantillas de animación con entradas y salidas

### Qué se hizo
- **Catálogo de efectos** (`motor/escenas/efectos.py`), todos en CSS y deterministas:
  - `aparecer`, `subir`, `bajar`, `deslizar-izquierda`, `deslizar-derecha`, `escalar`, `desenfoque`, `revelar`, `rebote`, `girar`, `crecer`;
  - `palabra-por-palabra` y `maquina` (letra por letra), solo para el título y el antetítulo.

  Cuatro curvas: suave, enérgica, con rebote y lineal. Cada elemento (fondo, logo, antetítulo, título, línea, viñetas, imagen, barra de avance) dice qué efectos admite.
- **Cinco plantillas de fábrica** en `datos/animaciones/`: Sobria, Dinámica (la de antes, mejorada), Cinética, Corporativa y Mínima. Cada elemento tiene su entrada y su salida (efecto, duración, retardo, curva y escalonado).
- **`motor/escenas/animacion.py`:**
  - carga y valida las plantillas (las de fábrica y las de `propias/`);
  - mezcla por capas: plantilla del curso → ajustes del curso → ajustes de la lámina (que puede cambiar de plantilla);
  - calcula cuánto duran la entrada y la salida de cada escena y genera el CSS.
- **Render con salidas:** se dibuja cuadro a cuadro la entrada y la salida; ffmpeg sostiene lo del medio (`tpad` + `concat`). El respiro final dura al menos la salida más 0,3 s, para que la salida no pise la voz.
- **Revisor de encuadre** (sin IA): al terminar la entrada, Playwright mide si algún texto se sale de la pantalla o de su caja. Aparece en el control de calidad como «Todo el texto cabe», con la lámina.
- **Pruebas** (`tests/test_animaciones.py`, 12):
  - las plantillas son válidas y se rechazan los ajustes inválidos;
  - la mezcla por capas funciona;
  - el fondo y el logo solo se animan al abrir y al cerrar el video;
  - el título se parte palabra por palabra;
  - al final de la escena el título tiene opacidad 0 con salida y 1 sin salida;
  - el revisor detecta la lámina que no cabe.

### Decisiones
- **El fondo y el logo** solo entran en la primera escena del video y solo salen en la última. Entre láminas quedan fijos; si no, parpadean en cada cambio.
- **La salida usa `fill-mode: forwards`** (la entrada, `both`): así la salida no actúa antes de su momento y no pisa a la entrada.
- **Las viñetas salen en orden**, y la última termina justo al final de la escena.

### Errores y cómo se resolvieron
- Al generar `render.py` con un script, un `
` dentro de un f-string se escribió como salto de línea real (`SyntaxError`). Se corrigió a mano.
- El chequeo de comandos del asistente falló varias veces seguidas. Las plantillas se escribieron con la herramienta de archivos y se validaron después.

---

## 2026-09-30 · Frente A2: curso completo en un MP4 y paquete ZIP

### Qué se hizo
- **`motor/empaquetar.py`:**
  - `armar_completo` une los MP4 de todos los videos **sin recodificar** (`concat -c copy`, todos salen con los mismos parámetros);
  - entre video y video pone una tarjeta con el título del video (se dibuja con la misma plantilla de marca, con audio en silencio y el mismo formato);
  - incrusta los capítulos en el MP4 (FFMETADATA) y escribe `capitulos.txt` en formato YouTube;
  - une el VTT y el SRT corriendo los tiempos de cada video.
- `pendientes(t)`: lista los videos sin producir o desactualizados. Si hay alguno, no se arma el completo y se dice cuáles.
- `paquete(t)`: un ZIP con cada video, sus subtítulos y su informe de calidad, más el completo, los capítulos, el banco de preguntas y un `manifiesto.json` con el SHA-256 de cada archivo. Los MP4 van sin comprimir de nuevo (`ZIP_STORED`), lo que es igual de liviano y mucho más rápido.
- La cola de `motor/cola.py` atiende también `completo`: los videos y el completo van en la misma fila, así que «Producir todo» arma el completo al final.
- **API:**
  - `POST /api/trabajos/{id}/producir-todo`: solo lo que falta o quedó desactualizado, y al final el completo;
  - `POST /api/trabajos/{id}/completo`;
  - `GET /api/trabajos/{id}/paquete.zip`;
  - `/produccion` ahora dice cuántos videos están listos, cuáles faltan y el estado del completo.
- **Interfaz (Resultado):** tarjeta «Todo el curso» con el avance, «Producir lo que falta y el completo», el estado del MP4 completo con sus descargas (MP4, SRT, VTT y capítulos) y «Descargar ZIP».
- **Prueba nueva:** un curso de dos videos. Se comprueban los capítulos dentro del MP4, `capitulos.txt`, los subtítulos corridos, el manifiesto con SHA-256 correctos y que un cambio de ajuste deja todo desactualizado.
- **Probado en vivo** con el curso demo: completo de 0:15 (tarjeta de 3 s más el video de 12 s) y ZIP.

---

## 2026-09-30 · Frente A1/A3: configuración del estudio

Plan de esta ronda (configuración, plantillas de animación y agentes): ver `docs/plan-motor.md`.

### Qué se hizo
- **`app/configuracion.py` + `datos/configuracion.json`** (va a git, sin secretos). Grupos:
  - cursos nuevos: marca, voz, formatos y animación;
  - video: resolución 1080p/720p, 25/30/60 fps, calidad final/borrador y subtítulos quemados;
  - tiempos: entrada, pausa y respiro;
  - audio: -14/-16/-23 LUFS, música de fondo y su volumen;
  - curso completo: tarjetas entre videos y capítulos;
  - agentes: URL de Ollama, modelos y cuáles están activos.

  Lo que falta en el archivo toma el valor por defecto, y todo se valida con mensajes claros.
- **Ajustes por curso** (`trabajo["ajustes_video"]`): solo lo que cambia respecto a lo global.
  `PUT /api/trabajos/{id}/ajustes-video` (null vuelve a lo global).
- **El motor usa la configuración:**
  - fps, resolución (Chromium dibuja con `device_scale_factor` 2/3 para 720p, sin cambiar la composición), CRF y preset;
  - tiempos y volumen objetivo;
  - música con `sidechaincompress`: baja ~10 dB cuando habla la voz, con fundido de entrada y de salida;
  - subtítulos quemados con Montserrat.
- **«Desactualizado»** ya no compara solo marca y voz: `produccion.firma(t)` resume marca, voz, ajustes, animación y ediciones, y el informe la guarda.
- **Música:** `POST /api/musica` exige la licencia (se guarda en un `.json` al lado). `datos/musica/` no va a git.
- **Diagnóstico** `GET /api/sistema`: ffmpeg, Chromium, voces, clave de ElevenLabs (solo si está), Ollama y sus modelos, y el disco. Nunca devuelve la clave.
- **Interfaz:**
  - vista `/configuracion` con el diagnóstico y los comandos para arreglar lo que falta, cursos nuevos, producción, música con subida y licencia, y agentes; barra de «cambios sin guardar»;
  - en «Marca y voz», el bloque «Ajustes de producción de este curso», que marca lo que cambia y deja volver a lo general.
- **Pruebas:** 48 de pytest (14 nuevas), entre ellas una producción real a 720p, 25 fps, -16 LUFS, con música y subtítulos quemados; 8 de Vitest.

### Decisiones
- La configuración va a git y la música no. Por eso, si otro equipo no tiene la pista, el curso se produce **sin música** en vez de fallar (`_validar(estricto=False)`).
- Cliente de Ollama con `keep_alive: 0` y `think: false`: libera la RAM al terminar y no gasta tiempo «pensando».

### Errores y cómo se resolvieron
- Con un campo de formulario vacío FastAPI respondía 422 antes de llegar a nuestro mensaje. La licencia pasó a `Form("")` para responder «escribe la licencia».
- Al reiniciar el servidor, PowerShell estaba en `frontend/` y no encontró `.venv`. Se lanza con la ruta de la carpeta del proyecto.

---

## 2026-09-30 · Script de instalación para equipos nuevos

### Qué se hizo
- **`instalar.ps1`** (PowerShell 5.1+). En orden:
  1. revisa Python ≥ 3.12, Node ≥ 20 y ffmpeg;
  2. crea `.venv` e instala `requirements.txt`;
  3. instala Chromium (Playwright);
  4. baja los modelos de voz;
  5. crea `.env` desde `.env.ejemplo` pidiendo la clave de ElevenLabs de forma oculta;
  6. corre `npm ci` y `npm run build`.

  Al final lista lo pendiente. Opciones: `-InstalarFfmpeg`, `-SinModelos` y `-Probar`.
- README: sección nueva «Instalar en un equipo nuevo».
- **Probado** en este equipo con `-Probar`: sale con código 0, pasan 34 pruebas de pytest y 7 de Vitest, y respeta el `.env` existente.

### Decisiones
- El archivo se guarda en UTF-8 **con BOM**: sin él, Windows PowerShell 5.1 lo lee como ANSI y
  las tildes de los mensajes salen dañadas.
- Se llama `npm.cmd` en vez de `npm`, para no depender de que PowerShell permita correr `npm.ps1`.
- `.env` existente nunca se toca. La clave se pide con `-AsSecureString`, para que no quede en
  pantalla ni en el historial.
- ffmpeg no se instala sin permiso: solo con `-InstalarFfmpeg`, porque instala un programa en
  todo el equipo.

### Pendiente
- No se probó en un equipo limpio de verdad (aquí ya estaba todo instalado). La primera vez
  baja unos 600 MB entre librerías, Chromium y voces.

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
