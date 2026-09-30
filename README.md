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

### Conectar el repositorio de videos

Copia `config.ejemplo.json` como `config.local.json` y pon las rutas de tu equipo:

- `repo_videos`: la copia de `riskmann2-marketing-videos` (hoy, la rama `fegir/avance-local`).
- `entregables`: la carpeta `ENTREGABLES-VIDEO` con los MP4 entregados.

`config.local.json` no se sube a git. Sin él, el estudio funciona pero sin videos, logos ni el ejemplo.
El estudio **solo lee** esas carpetas; del repositorio de videos solo sirve imágenes, PDF y texto.

## Pruebas

```sh
python -m pytest                   # API, extractor y seguridad de archivos
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
| `/cursos/:id` | El curso en tres pestañas: **Resumen** (estado, siguiente paso, vistas previas), **Guion** y **Marca y voz** |

Pensado para una persona que no es del equipo de producción:

- **Un paso a la vez.** El asistente guía después de subir; cada elección se guarda sola y «atrás» funciona.
- **Siempre un siguiente paso.** El Resumen dice qué hacer ahora y lleva al lugar exacto del guion.
- **Sus palabras.** «Diapositivas», no «láminas»; cada aviso dice qué pasa y qué hacer.
- **Ver antes de producir.** Cada video tiene una vista previa con la marca; el color del texto se elige por
  contraste medido, nunca por la paleta a ciegas.
- **Ayuda a mano.** Panel de ayuda con un dibujo de dónde están las notas del orador en PowerPoint.
- **Lo del equipo, aparte.** Videos, Pendientes y Marcas van plegados en «Equipo de producción».

| Ruta del equipo | Qué hace |
| --- | --- |
| `/videos` | Todos los videos, con filtros que quedan en la dirección y columnas ordenables |
| `/videos/:id` | Un video: reproducción, siguiente paso (aprobar, entregar…) e historial |
| `/marcas/:id` | Ficha de la marca; RiskMann con su paleta en cuatro capas y la fuente de cada color |
| `/pendientes` | Lo pendiente con cada marca y los videos sin estado |
| `/casos/:id` | Una pieza de marketing: qué entró, qué se hizo y qué salió |

## El curso, paso a paso

| Paso | Qué hace | Estado |
| --- | --- | --- |
| Entra | Lee el PPTX: formas con nombre, notas del orador, imágenes → `curso.json` (formato de csm/moto) | Funciona |
| Guion | Cada frase con la diapositiva de la que sale; cifras, normas y umbrales resaltados | Funciona |
| Videos | Un video por sección si el PPTX las marca (forma `section`); si no, por duración | Funciona |
| Marca y voz | Las cuatro marcas y las voces con su muestra; se guarda solo | Funciona |
| Resultado | Plan de videos, preguntas, revisión, `curso.json` y **orden de producción** | Funciona |
| Render | El motor por CLI recibe la orden de producción y produce los MP4 | **Falta el motor** |

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
