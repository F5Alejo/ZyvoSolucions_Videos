# Estudio de video RiskMann

**Entra un PPTX. Sale el curso en video.** La interfaz del motor de `riskmann2-marketing-videos`:
el estudio donde entra la presentación del cliente y sale el curso, y el seguimiento de cada
video hasta su aprobación.

## Cómo está hecho

| Parte | Tecnología | Dónde |
| --- | --- | --- |
| Interfaz | **Vue 3** + TypeScript + **Tailwind CSS 4** + Vite, íconos Lucide | `frontend/` |
| API | FastAPI (Python), JSON en `/api/*`, documentación en `/api/docs` | `app/main.py` |
| Lógica | Extractor de PPTX, taller (guion, videos, revisión) y datos | `app/extractor.py`, `app/taller.py`, `app/datos.py` |
| Motor de video | Voz (Kokoro local o ElevenLabs), escenas HTML de marca dibujadas con Playwright, ffmpeg, subtítulos y control de calidad | `motor/` |

Vue porque es el framework de **app.riskmann.com** (Vue 3 + Vuex): el equipo de RiskMann ya lo conoce.

### Identidad

- **Colores: la guía del manual de identidad de RiskMann**, en sus dos modos (selector en la barra lateral,
  oscuro por defecto). Oscuro: `#020202` fondo, `#272725` separadores, `#C8951A` dorado, `#06C7FB` cian,
  `#999999` gris, `#FF3333` énfasis. Claro: `#26367D` institucional, `#333366` texto, `#336699`.
  Los que no llegan a 4,5:1 como texto sobre blanco se oscurecen solo para texto; cada token dice su
  origen y su contraste en `frontend/src/estilos.css`.
- **Imágenes: el banco de RiskMann.** El caballero del manual en la portada y en Crear curso; las
  ilustraciones de su app en los estados vacíos, el error de conexión y la página 404. El origen de cada
  una está en `frontend/public/marca/banco/FUENTES.md`.
- **Tipografía:** Dubai, la del manual, cuando está instalada (viene con Windows); si no, Montserrat.
  Dubai no se incluye en el proyecto: es de Microsoft y su licencia no permite redistribuirla en la web.

## Instalar en un equipo nuevo (Windows)

Con Python 3.12+ y Node 20+ instalados, después de clonar:

```powershell
git clone https://github.com/juanezzzzz/interfaz.git
cd interfaz
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

Requisitos: Python 3.12 y Node 20 o superior. Todos los comandos, desde la carpeta `estudio/`.

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
control de calidad. El plan y la bitácora de desarrollo están en `docs/`.

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

### El repositorio de videos y los entregables

El estudio vive en `estudio/` dentro del repositorio de videos y **lo encuentra solo** en la carpeta
de arriba: no hay que configurar nada para ver las marcas, los logos, los videos del catálogo y el
curso de ejemplo.

Lo único que no está en git son los MP4 entregados (`ENTREGABLES-VIDEO`, pesan cientos de MB). Para
verlos, copia `config.ejemplo.json` como `config.local.json` y pon su ruta en `entregables`.
`config.local.json` no se sube a git. También sirven las variables `REPO_VIDEOS` y `ENTREGABLES`.

El estudio **solo lee** esas carpetas; del repositorio de videos solo sirve imágenes, PDF y texto.

## Pruebas

```sh
python -m pytest                   # API, extractor, motor y seguridad de archivos
cd frontend
npm run typecheck                  # tipos de TypeScript
npm test                           # utilidades y componentes (Vitest)
```

## Pantallas

| Ruta | Qué hace |
| --- | --- |
| `/` | Inicio: qué hace el estudio, «continúa donde quedaste», cómo funciona y tus cursos; abajo, lo del equipo |
| `/cursos/nuevo` | Subir un PPTX (arrastrar y soltar, progreso de subida) |
| `/cursos/:id/asistente` | Después de subir: lo que encontramos → marca (con vista previa en vivo) → voz (con muestras) → formato → listo |
| `/empresas` | Las empresas: las cuatro marcas base y las que se registran desde el estudio |
| `/empresas/nueva` | Registrar una empresa en cuatro pasos: datos → logo (propone los colores del logo) → colores → voz y cierre, con vista previa en vivo |
| `/cursos/:id` | El curso en cinco pestañas: **Resumen** (estado, siguiente paso, vistas previas, agentes), **Guion**, **Marca y voz** (con los ajustes de producción del curso), **Animación** y **Producir** |
| `/configuracion` | Cómo se producen los videos, música, agentes y qué tiene este equipo |

Pensado para una persona que no es del equipo de producción:

- **Un paso a la vez.** El asistente guía después de subir; cada elección se guarda sola y «atrás» funciona.
- **Siempre un siguiente paso.** El Resumen dice qué hacer ahora y lleva al lugar exacto del guion.
- **Sus palabras.** «Diapositivas», no «láminas»; cada aviso dice qué pasa y qué hacer.
- **Ver antes de producir.** Cada video tiene una vista previa con la marca; el color del texto se elige por
  contraste medido, nunca por la paleta a ciegas.
- **Ayuda a mano.** Panel de ayuda con un dibujo de dónde están las notas del orador en PowerPoint.
- **Cualquier empresa entra sola.** «¿Tu empresa no está?» al elegir la marca lleva al registro y vuelve al curso.
- **Lo del equipo, aparte.** Videos y Pendientes van plegados en «Equipo de producción».

| Ruta del equipo | Qué hace |
| --- | --- |
| `/videos` | Todos los videos, con filtros que quedan en la dirección y columnas ordenables |
| `/videos/:id` | Un video: reproducción, siguiente paso (aprobar, entregar…) e historial |
| `/marcas/:id` | Ficha de la marca (las registradas se editan, se eliminan si no tienen cursos, o abren un curso nuevo con su marca y su voz); RiskMann con su paleta en cuatro capas y la fuente de cada color |
| `/pendientes` | Lo pendiente con cada marca y los videos sin estado |
| `/casos/:id` | Una pieza de marketing: qué entró, qué se hizo y qué salió |

## El curso, paso a paso

| Paso | Qué hace | Estado |
| --- | --- | --- |
| Entra | Lee el PPTX: formas con nombre, notas del orador, imágenes → `curso.json` (formato de csm/moto) | Funciona |
| Guion | Cada frase con la diapositiva de la que sale; cifras, normas y umbrales resaltados | Funciona |
| Videos | Un video por sección si el PPTX las marca (forma `section`); si no, por duración | Funciona |
| Marca y voz | Las marcas base, las empresas registradas y las voces con su muestra; se guarda solo | Funciona |
| Resultado | Plan de videos, preguntas, revisión, `curso.json` y **orden de producción** | Funciona |
| Animación | Estilo y entrada/salida de cada elemento, por curso o por lámina, con vista previa en vivo | Funciona |
| Render | «Producir video» por tarjeta o «Producir lo que falta y el completo»: MP4 por video, MP4 completo con capítulos, subtítulos y paquete ZIP | Funciona (16:9) |

La duración se estima con la velocidad medida en csm (2,394 palabras por segundo con Carlos,
más 2,3 s por lámina): para csm da 33:24 frente a los ~33 min reales.

Lo que se sube queda en `datos/trabajos/`, que no va a git: es material del cliente.

## Los datos

- `datos/marcas/<marca>.json`: una ficha por marca (SOFU, RiskMann, FEGIR, Dr. Yezid Ricaurte).
- `datos/empresas/<id>.json` y `datos/empresas/logos/<id>.png`: las empresas registradas desde el estudio. Son datos
  de clientes y no van a git. El logo se valida (PNG, JPG o WebP de hasta 5 MB) y se guarda re-codificado en PNG.
- `datos/proyectos.json`: un registro por video, con sus carpetas de `videos/`, sus entregables y su historial.
- `datos/voces.json` y `datos/casos.json`: voces para elegir y piezas de marketing de ejemplo.

Sembrados desde `MAESTRO.md` (26–29 sep 2026). Cada cambio de estado queda en el historial del video.

## Límites

- Las fichas de marca son una copia en JSON de `docs/marcas/*/ficha.md`: si la ficha cambia, se actualiza a mano.
- El estado se guarda en `datos/proyectos.json`, no en los `meta.json` del repositorio de videos.
- Los cursos que están en Drive (Ruta Segura, moto, csm, PESV M01, SOFU) no tienen vista previa.
- No hay usuarios ni inicio de sesión: «quién decide» se escribe a mano. Es para uso local del equipo.
