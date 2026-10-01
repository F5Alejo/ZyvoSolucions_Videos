# Estudio de video RiskMann

[![Pruebas](https://github.com/F5Alejo/ZyvoSolucions_Videos/actions/workflows/pruebas.yml/badge.svg?branch=main)](https://github.com/F5Alejo/ZyvoSolucions_Videos/actions/workflows/pruebas.yml)
[![Instalador en Windows](https://github.com/F5Alejo/ZyvoSolucions_Videos/actions/workflows/instalador-windows.yml/badge.svg)](https://github.com/F5Alejo/ZyvoSolucions_Videos/actions/workflows/instalador-windows.yml)

**Entra un PPTX. Sale el curso en video.** La interfaz del motor de `riskmann2-marketing-videos`:
el estudio donde entra la presentación del cliente y sale el curso, y el seguimiento de cada
video hasta su aprobación.

## Cómo está hecho

| Parte | Tecnología | Dónde |
| --- | --- | --- |
| Interfaz | **Vue 3** + TypeScript + **Tailwind CSS 4** + Vite, íconos Lucide, Montserrat incluida | `frontend/` |
| API | FastAPI (Python), JSON en `/api/*`, documentación en `/api/docs` | `app/main.py` |
| Lógica | Extractor de PPTX, taller (guion, videos, revisión) y datos | `app/extractor.py`, `app/taller.py`, `app/datos.py` |
| Motor de video | Voz (Kokoro local o ElevenLabs), escenas HTML de marca dibujadas con Playwright, ffmpeg, subtítulos y control de calidad | `motor/` |

Vue porque es el framework de **app.riskmann.com** (Vue 3 + Vuex): el equipo de RiskMann ya lo conoce.
Los colores son los de la app de RiskMann, con los contrastes medidos; los tokens están comentados en
`frontend/src/estilos.css`.

## Instalar en un equipo nuevo (Windows)

Con Python 3.12+ y Node 20+ instalados, después de clonar:

```powershell
git clone https://github.com/F5Alejo/ZyvoSolucions_Videos.git
cd ZyvoSolucions_Videos
powershell -ExecutionPolicy Bypass -File instalar.ps1
```

El script crea `.venv`, instala las librerías de Python, Chromium y las voces Kokoro y Piper,
compila la interfaz y pide la clave de ElevenLabs para guardarla en `.env` (Enter para dejarla
vacía). Se puede volver a correr: salta lo que ya está. Opciones: `-InstalarFfmpeg` (con winget),
`-SinModelos`, `-ConAgentes` (baja los modelos de Ollama, ~5 GB) y `-Probar` (corre las pruebas al
final). Al terminar dice qué quedó pendiente.

Lo que git no trae y el script resuelve: `.venv`, `frontend/node_modules` y `frontend/dist`,
Chromium, `modelos/` y `.env`. Lo que no resuelve: `config.local.json` (opcional, rutas de tu
equipo) y los cursos de `datos/trabajos/` (material de clientes, se quedan en cada equipo).

## Puesta en marcha

Requisitos: Python 3.12 y Node 20 o superior.

```sh
# API
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Interfaz
cd frontend
npm install
npm run build                      # compila en frontend/dist, que sirve la API
cd ..

uvicorn app.main:app --port 8765   # http://localhost:8765
```

### Para trabajar en la interfaz

Con la API encendida (`uvicorn app.main:app --port 8765`), en otra terminal:

```sh
cd frontend
npm run dev                        # http://localhost:5173, se recarga al guardar
```

Vite reenvía `/api` y `/media` al puerto 8765.

### El motor de video (Render)

Además de lo anterior, necesita **ffmpeg** en el PATH y, una sola vez:

```sh
python -m playwright install chromium   # el navegador que dibuja las escenas
python scripts/descargar_modelos.py     # voces Kokoro y Piper → modelos/ (no va a git)
```

| Voz | Proveedor | ¿Se puede entregar? |
| --- | --- | --- |
| Dora, Alex, Santa | Kokoro-82M, local (Apache 2.0) | Sí |
| Carlos y las demás de ElevenLabs | ElevenLabs, de pago | Sí. Necesita `ELEVENLABS_API_KEY` en `.env` (copia `.env.ejemplo`; `.env` no va a git) y, salvo Carlos, su `voice_id` en `datos/voces.json` |
| Piper · davefx | Piper, local | **No**: solo borradores (sale con sello «BORRADOR»). Ver `docs/bitacora.md` |

En **Resultado**, cada video tiene «Producir video». Sale en `datos/trabajos/<id>/salida/<clave>/`:
el `.mp4` (1920×1080, H.264 + AAC, -14 LUFS), sus subtítulos `.vtt` y `.srt`, y `qa.json` con el
control de calidad. La documentación (arquitectura, hallazgos, plan de nube y bitácora) está en [`docs/`](docs/README.md).

### Configuración (`/configuracion`)

Todo lo que antes estaba fijo en el código se elige aquí y se guarda en `datos/configuracion.json`:
resolución (1080p/720p), fps (25/30/60), calidad (final o borrador), subtítulos dentro de la imagen,
el ritmo de cada lámina, el volumen final (-14/-16/-23 LUFS), la música de fondo (se sube con su
licencia y baja sola cuando habla la voz), el MP4 completo del curso (tarjetas y capítulos) y los
agentes. Muestra también qué tiene el equipo (ffmpeg, navegador, voces, clave, Ollama, disco) y cómo
arreglar lo que falta. Cada curso puede cambiar estos ajustes para sí mismo en «Marca y voz».

### Animación

Cinco estilos de fábrica (Sobria, Dinámica, Cinética, Corporativa y Mínima) en `datos/animaciones/`.
En el paso **Animación** de cada curso se elige el estilo y se edita la **entrada y la salida** de
cada elemento (título, viñetas, imagen, línea, antetítulo, fondo, logo y barra de avance): efecto,
duración, espera, curva y separación. Se puede cambiar todo el curso o solo una lámina, guardar el
resultado como plantilla propia y verlo animándose en vivo antes de producir.

### Agentes con IA local

Proponen mejoras que una persona acepta o descarta; nada cambia solo. Usan Ollama (`qwen3:4b` y
`qwen3.5:2b`, gratuitos y locales: el material del cliente no sale del equipo) y, si no está, reglas
simples. Corren en la misma cola que los renders, uno a la vez.

| Agente | Paso | Qué propone |
| --- | --- | --- |
| Descriptor de imágenes | Presentación | Si cada imagen es contenido o adorno, y su texto alternativo |
| Redactor de pantalla | Guion | Títulos y viñetas cortas para leer mientras habla la voz |
| Guionista | Guion | Narración para láminas sin notas; acortar videos de más de 4 min |
| Verificador normativo | Guion | Cada cifra y norma con la pregunta por su fuente (sin IA) |
| Director de animación | Animación | Estilo y efectos por lámina, solo del catálogo |
| Evaluador | Resultado | Preguntas por video; se exportan a Moodle (GIFT y XML) |
| Publicador | Resultado | Título, descripción con capítulos, etiquetas e historias |
| Revisor de voz | Resultado | Escucha el video (Whisper local) y lo compara con el guion |

Ninguna propuesta puede traer cifras o normas que no estén en la lámina: si aparecen, se descarta.

### Conectar el repositorio de videos

Copia `config.ejemplo.json` como `config.local.json` y pon las rutas de tu equipo:

- `repo_videos`: la copia de `riskmann2-marketing-videos` (hoy, la rama `fegir/avance-local`).
- `entregables`: la carpeta `ENTREGABLES-VIDEO` con los MP4 entregados.

`config.local.json` no se sube a git. Sin él, el estudio funciona pero sin videos, logos ni el ejemplo.
El estudio **solo lee** esas carpetas; del repositorio de videos solo sirve imágenes, PDF y texto.

## Pruebas

```sh
python -m pytest                   # API, extractor, motor y seguridad de archivos
cd frontend
npm run typecheck                  # tipos de TypeScript
npm test                           # utilidades y componentes (Vitest)
```

### GitHub Actions y ramas

| Rama | Para qué | Cómo se actualiza |
| --- | --- | --- |
| `Alejodev` | Pruebas y mejoras: aquí se desarrolla | Push directo; Actions corre todo en cada push |
| `main` | La versión estable (protegida) | **Solo por pull request desde `Alejodev`**, con las pruebas en verde |

**Flujo «Pruebas»** (`.github/workflows/pruebas.yml`, Ubuntu 24.04, en cada push a las dos ramas y en
cada PR hacia `main`):

| Trabajo | Qué revisa |
| --- | --- |
| API y motor (pytest) | Python 3.12, ffmpeg y Chromium: 75 pruebas, que producen videos de verdad con una voz de prueba y Ollama simulado (no necesitan modelos ni claves). Sube el artefacto **`video-de-muestra`** (MP4, subtítulos y control de calidad, 14 días) |
| Interfaz | Node 22: `vue-tsc`, Vitest y la compilación |
| Estilo (ruff) | El código de Python, con las reglas de `pyproject.toml` |
| Secretos (gitleaks) | Que ninguna clave haya llegado a la historia de git |

**Flujo «Instalador en Windows»** (`.github/workflows/instalador-windows.yml`): `instalar.ps1
-SinModelos -Probar` en un Windows limpio, como en un equipo nuevo. Corre cada lunes, a mano
(pestaña Actions → «Run workflow») y cuando cambian el instalador o las dependencias.

**Dependabot** (`.github/dependabot.yml`): cada lunes propone PR agrupados hacia `Alejodev` con las
actualizaciones de pip, npm y las acciones.

**Para llevar `Alejodev` a `main`:**
```sh
gh pr create --base main --head Alejodev --fill   # abre el PR
gh pr checks --watch                              # espera las pruebas
gh pr merge --merge                               # fusiona cuando están en verde
git switch Alejodev && git pull origin main       # deja Alejodev igual que main
```

## Pantallas

| Ruta | Qué hace |
| --- | --- |
| `/` | Inicio: cifras, cómo funciona, tus cursos y piezas de marketing ya hechas |
| `/cursos/nuevo` | Subir un PPTX (arrastrar y soltar, progreso de subida) |
| `/cursos/:id` | El curso en cinco pasos: Presentación · Guion · Marca y voz · Animación · Resultado |
| `/configuracion` | Cómo se producen los videos, música, agentes y qué tiene este equipo |
| `/videos` | Todos los videos, con filtros que quedan en la dirección y columnas ordenables |
| `/videos/:id` | Un video: reproducción, siguiente paso (aprobar, entregar…) e historial |
| `/marcas/:id` | Ficha de la marca; RiskMann con su paleta en cuatro capas y la fuente de cada color |
| `/pendientes` | Lo pendiente con cada marca y los videos sin estado |
| `/casos/:id` | Una pieza de marketing: qué entró, qué se hizo y qué salió |

## El curso, paso a paso

| Paso | Qué hace | Estado |
| --- | --- | --- |
| Entra | Lee el PPTX: formas con nombre, notas del orador, imágenes → `curso.json` (formato de csm/moto) | Funciona |
| Guion | Cada frase con la lámina de la que sale; cifras, normas y umbrales resaltados | Funciona |
| Videos | Un video por sección si el PPTX las marca (forma `section`); si no, por duración | Funciona |
| Marca y voz | Las cuatro marcas y las voces con su muestra; se guarda solo | Funciona |
| Resultado | Plan de videos, preguntas, revisión, `curso.json` y **orden de producción** | Funciona |
| Animación | Estilo y entrada/salida de cada elemento, por curso o por lámina, con vista previa en vivo | Funciona |
| Render | «Producir video» por tarjeta o «Producir lo que falta y el completo»: MP4 por video, MP4 completo con capítulos, subtítulos y paquete ZIP | Funciona (16:9) |

La duración se estima con la velocidad medida en csm (2,394 palabras por segundo con Carlos,
más 2,3 s por lámina): para csm da 33:24 frente a los ~33 min reales.

Lo que se sube queda en `datos/trabajos/`, que no va a git: es material del cliente.

## Los datos

- `datos/marcas/<marca>.json`: una ficha por marca (SOFU, RiskMann, FEGIR, Dr. Yezid Ricaurte).
- `datos/proyectos.json`: un registro por video, con sus carpetas de `videos/`, sus entregables y su historial.
- `datos/voces.json` y `datos/casos.json`: voces para elegir y piezas de marketing de ejemplo.

Sembrados desde `MAESTRO.md` (26–29 sep 2026). Cada cambio de estado queda en el historial del video.

## Límites

- Las fichas de marca son una copia en JSON de `docs/marcas/*/ficha.md`: si la ficha cambia, se actualiza a mano.
- El estado se guarda en `datos/proyectos.json`, no en los `meta.json` del repositorio de videos.
- Los cursos que están en Drive (Ruta Segura, moto, csm, PESV M01, SOFU) no tienen vista previa.
- No hay usuarios ni inicio de sesión: «quién decide» se escribe a mano. Es para uso local del equipo.
