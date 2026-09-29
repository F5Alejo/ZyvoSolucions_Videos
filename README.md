# Panel de producción

**Entra un PPTX. Sale el curso en video.** La interfaz del motor de `riskmann2-marketing-videos`:
el taller donde entra el contenido del cliente y sale el curso, y el panel donde se sigue
cada pieza hasta su aprobación.

## Identidad

La interfaz usa la identidad de **app.riskmann.com**, el producto de RiskMann: fondo `#F3F3F3`,
texto `#3C3C44`, principal `#073D7A` y Montserrat, con el logo oficial «RiskMann by SOFU» en
la cabecera. El modo oscuro toma el negro, el dorado y el cian de riskmann.com y del manual.
Los contrastes están medidos (todo texto ≥ 4,5:1); los valores y su fuente están comentados en
`app/static/estilo.css`.

La paleta completa de RiskMann, en cuatro capas con su fuente (manual, logo medido, web y app),
está en `datos/marcas/riskmann.json` y se ve en `/marcas/riskmann`.

## El taller (`/`)

| Paso | Qué hace | Estado |
| --- | --- | --- |
| 1. Entra | Lee el PPTX: formas con nombre, notas del orador, imágenes → `curso.json` en el formato de csm/moto (tarea 0.1 de PLATAFORMA.md) | Funciona |
| 2. Guion trazado | Cada frase con la lámina de la que sale; cifras, normas y umbrales resaltados | Funciona |
| 3. Marca, voz, formato | Las cuatro marcas con su logo y paleta; las voces con su muestra grabada | Funciona |
| 4. Sale | Plan de videos con su duración, banco de preguntas, informe de verificación, `curso.json` y **orden de producción** | Funciona |
| 5. Render | «Producir video» en cada tarjeta: voz, escenas de marca, subtítulos VTT/SRT y control de calidad → MP4 listo para subir | Funciona (Fase 1: 16:9) |

La duración se estima con la velocidad medida en csm (2,394 palabras por segundo con Carlos,
más 2,3 s por lámina). Para csm da 33:24 frente a los ~33 min que salieron de verdad.

**Recorrer el caso real (curso csm)** carga el curso ya producido: su `curso.json`, sus 15
videos, las láminas excluidas con su motivo y sus 146 preguntas. `banco_preguntas.py` se lee
con `ast.literal_eval`: nunca se ejecuta.

Los **casos de marketing** (`/casos/<id>`, en `datos/casos.json`) muestran qué entró, qué se
hizo y los videos que salieron.

Lo que se sube queda en `datos/trabajos/`, que no va a git: es material del cliente.

## El panel

| Ruta | Qué muestra |
| --- | --- |
| `/proyectos` | Todos los proyectos, con resumen por estado y filtros por marca, estado y familia (A/B) |
| `/proyectos/<id>` | Datos del proyecto, cambio de estado (con quién y por qué) e historial |
| `/marcas/<id>` | La ficha de la marca: paleta, tipografía, voz, CTA, fuentes, contradicciones y pendientes |
| `/pendientes` | Todos los pendientes de las fichas y los proyectos sin estado |

## Puesta en marcha

```sh
python -m venv .venv
.venv\Scripts\activate          # Windows  (en macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego se abre http://localhost:8000.

### El motor de video (paso 5)

Además de lo anterior, necesita **ffmpeg** en el PATH y, una sola vez:

```sh
python -m playwright install chromium   # el navegador que dibuja las escenas
python scripts/descargar_modelos.py     # voces Kokoro y Piper → modelos/ (no va a git)
```

| Voz | Proveedor | ¿Se puede entregar? |
| --- | --- | --- |
| Dora, Alex, Santa | Kokoro-82M, local (Apache 2.0) | Sí |
| Carlos y las demás de ElevenLabs | ElevenLabs, de pago | Sí. Necesita `ELEVENLABS_API_KEY` y, salvo Carlos, su `voice_id` en `datos/voces.json` |
| Piper · davefx | Piper, local | **No**: solo borradores (sale con sello «BORRADOR»). Ver `docs/bitacora.md` |

Cada video sale en `datos/trabajos/<id>/salida/<clave>/`: el `.mp4` (1920×1080, H.264 + AAC,
-14 LUFS), sus subtítulos `.vtt` y `.srt`, y `qa.json` con el control de calidad. El código
está en `motor/` (un módulo por paso); el plan y la bitácora de desarrollo, en `docs/`.

### Conectar el repositorio de videos y los entregables

Copia `config.ejemplo.json` como `config.local.json` y pon las rutas de tu equipo:

- `repo_videos`: la copia de `riskmann2-marketing-videos` (hoy, la de la rama `fegir/avance-local`).
- `entregables`: la carpeta `ENTREGABLES-VIDEO` con los MP4 entregados.

`config.local.json` no se sube a git. Las rutas también se pueden dar con las variables
`REPO_VIDEOS` y `ENTREGABLES`. Sin configuración el panel funciona igual, pero sin
carpetas, logos ni videos.

El panel **solo lee** esas carpetas: no escribe nada en ellas. Del repositorio de videos solo
sirve imágenes, PDF y texto; nunca código ni archivos fuera de la carpeta configurada.

Para las pruebas: `python -m pytest`.

## Los datos

- `datos/marcas/<marca>.json`: una ficha por marca (SOFU, RiskMann, FEGIR, Dr. Yezid Ricaurte).
- `datos/proyectos.json`: un registro por proyecto de video.

Se sembraron a mano desde `MAESTRO.md` (26–28 sep 2026). `estado_original` guarda el texto
literal del maestro para no perder matices. Los proyectos que el maestro marca con
«⚠ estado por confirmar» quedan como `sin_estado`.

**Estados:** `sin_estado` · `borrador` · `revision` · `aprobado` · `final` · `archivado`.
Cada cambio se anota en el `historial` del proyecto con la fecha, quién y la nota. Nada se borra.

Cada proyecto declara sus `carpetas` de `videos/` (un curso agrupa sus módulos) y sus
`entregables` (rutas dentro de `ENTREGABLES-VIDEO`). Si aparece una carpeta nueva en el
repositorio que ningún proyecto reclama, se ve en **Pendientes → Carpetas sin registrar**.

## Límites de esta versión

- Las fichas de marca son una copia en JSON de `docs/marcas/*/ficha.md`; si la ficha
  cambia, hay que actualizar el JSON a mano.
- El estado se guarda en `datos/proyectos.json`, no en los `meta.json` del repositorio de videos.
- Los cursos de Drive (Ruta Segura, moto, csm, PESV M01, SOFU) no tienen vista previa: sus
  finales no están en `ENTREGABLES-VIDEO`.
- No hay usuarios ni inicio de sesión: «quién» se escribe a mano. Es para uso local del equipo.
