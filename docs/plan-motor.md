# Del PPTX al MP4 listo para publicar: qué falta y con qué herramientas gratuitas

> **Estado (2026-09-29):** Fase 1 hecha en la rama `Alejodev`, salvo la música y la transcripción
> de control (ver [`bitacora.md`](bitacora.md)). La cola con progreso, prevista para la Fase 2,
> se adelantó porque sin ella no se puede producir desde la interfaz. Siguiente: Fase 2.

## Contexto
El estudio (`interfaz/`) ya cubre los pasos 1 a 4:
- Lee el PPTX (`app/extractor.py`).
- Traza el guion y estima duraciones.
- Deja elegir marca, voz y formato.
- Genera `curso.json` y la orden de producción (`taller.orden_produccion`, en `app/taller.py`).

Falta el **paso 5, el motor**, que convierte esa orden en MP4 terminados. También faltan las piezas que rodean cada publicación: subtítulos, miniaturas, metadatos, versiones verticales, control de calidad y aprobación.

Decisiones que ya tomó el usuario:
- **Visual:** plantillas de marca rearmadas en HTML a partir de `curso.json`, no capturas de la lámina.
- **Licencias:** uso comercial. Solo se usan herramientas con licencia MIT, Apache o BSD, o servicios de pago que ya se usan hoy, como ElevenLabs.
- **Destinos:** LMS, YouTube y redes, entrega al cliente, e historias y estados (Instagram y WhatsApp).

Equipo medido:
- Tarjeta gráfica GTX 1650 de 4 GB, 8 GB de RAM y un procesador i5-11400H.
- Ya instalados: ffmpeg 9.0.1 y Ollama, sin modelos descargados.
- Sin instalar: LibreOffice y Piper.

Estas cifras limitan qué modelos se pueden correr en local.

## 0. Flujo de trabajo en git (pedido por el usuario)
- **Todos los cambios van en la rama `Alejodev`.** Se crea desde `main`, que hoy está limpia en el remoto `origin` (`github.com/juanezzzzz/interfaz`).
- En esa rama también se hace la reorganización de la arquitectura: el paquete `motor/` y la separación de responsabilidades.
- Un commit por paso de la Fase 1: imágenes, normalización, voz, escenas, render, subtítulos y control de calidad. Así cada tema se puede revisar por separado.
- No se hace push ni pull request sin que el usuario lo pida. Tampoco se toca `main`.

---

## 1. Qué falta en la aplicación actual (antes del motor)
1. **Extraer las imágenes del PPTX.** Hoy `extractor.leer_pptx` solo guarda el *nombre* de la imagen en `foto` e `icono`, no el archivo. Hay que guardar las imágenes en `datos/trabajos/<id>/media/` para que las plantillas las usen.
2. **Editar el guion en el taller.** Hoy solo se pueden cambiar marca, voz y formatos (`taller.ajustar`). Falta poder:
   - editar la narración de cada lámina;
   - mover láminas entre videos;
   - excluir una lámina con su motivo;
   - escuchar una muestra de audio por lámina.

   Es un paso previo obligatorio: el motor no debe leer notas del orador sin revisar.
3. **Cola de render con progreso.** Un render tarda minutos. Se ejecuta en un proceso aparte, sin Redis. El estado se guarda en `trabajo.json` (`render: {estado, paso, progreso, log}`), y `app.js` consulta `GET /taller/{id}/render` cada pocos segundos.
4. **Aprobación conectada al panel.** Cuando un render termina, se crea o actualiza el registro en `datos/proyectos.json` con estado `revision`, reutilizando `datos.cambiar_estado` y su historial. Solo lo que queda `aprobado` se empaqueta para entregar.
5. **Revisar el motor que ya existe.** Hay que configurar `config.local.json` y leer `videos/csm-curso/tools/csm.py` en `riskmann2-marketing-videos`. Ese archivo ya produjo los 15 videos del curso csm: de ahí se reutilizan los tiempos (título 1,0 s y respiro 1,3 s), las plantillas y los ajustes de la voz.

## 2. El motor: nuevo paquete `motor/`
Entrada: `orden_produccion(t)` y `curso_json(t)`, que ya existen.
Salida: `datos/trabajos/<id>/salida/`.

| Paso | Módulo | Qué hace | Herramienta gratuita recomendada (uso comercial) |
|---|---|---|---|
| 1. Normalizar texto | `motor/normalizar.py` | Convierte cifras, leyes, siglas y porcentajes a texto que se pueda leer en voz alta («Ley 1503 de 2011», «SMMLV», «PESV», «30 %»). Usa un diccionario de pronunciación por marca guardado en `datos/marcas/*.json` | **num2words** (LGPL, se usa como librería) y reglas propias. Reutiliza el regex `extractor._NORMATIVO` |
| 2. Voz | `motor/voz.py` | Genera un audio por frase y mide su duración con ffprobe. Así cada frase queda sincronizada sin transcribir nada. Guarda el audio en caché por hash del texto y la voz, para no pagar dos veces | **Piper** (MIT, local, en CPU) para borradores y para la voz `piper-davefx`. **Kokoro-82M** (Apache 2.0) como segunda opción gratis por evaluar en español. **ElevenLabs/Carlos**, la voz de la casa ya pagada, para el final |
| 3. Escenas | `motor/escenas/` | Una plantilla HTML por tipo de lámina (título, lista de viñetas, imagen y texto, cifra destacada, cierre con CTA), con los colores, la tipografía y el logo de `datos/marcas/*.json`. Cada plantilla tiene una versión 16:9 y otra 9:16 | Jinja2 (ya está en el proyecto) y **GSAP** para las animaciones (hoy es gratuito, también para uso comercial) |
| 4. Render | `motor/render.py` | Convierte el HTML animado en video, frame a frame, de forma determinista | **HyperFrames** (HTML → MP4; confirmar que su licencia es Apache 2.0 antes de adoptarlo). Alternativa: **Playwright** (Apache 2.0) con ffmpeg. **Remotion no**: pide licencia pagada a empresas |
| 5. Mezcla | `motor/audio.py` | Une la voz con la música. La música baja sola cuando hay narración (`sidecompress`) y el volumen se normaliza a **-14 LUFS**, con picos de -1,5 dBTP | **ffmpeg** (ya instalado). Música de **Pixabay Music** o de la **YouTube Audio Library**, guardando la licencia de cada pista. **MusicGen no**: no permite uso comercial |
| 6. Subtítulos | `motor/subtitulos.py` | Genera `.vtt` y `.srt` a partir del guion y de los tiempos del paso 2, sin reconocimiento de voz. En redes e historias los subtítulos van quemados en la imagen | ffmpeg |
| 7. Control de calidad | `motor/qa.py` | Revisa con ffprobe resolución, fps, códec y duración real frente a la estimada. Detecta pantallas negras (`blackdetect`), silencios (`silencedetect`) y volumen (`ebur128`). Transcribe el audio final para confirmar que la voz dijo lo que dice el guion | ffmpeg y **faster-whisper** (MIT) con el modelo `small` en int8, que cabe en la GTX 1650 |
| 8. Empaquetar | `motor/empaquetar.py` | Prepara las salidas de cada destino (ver sección 3) | ffmpeg y Python |

## 3. «Todo lo necesario para subirse», por destino
- **Máster 16:9:** 1920×1080 a 30 fps, H.264 High, `yuv420p`, CRF 18, AAC a 48 kHz y 192 kbps, con `-movflags +faststart`.
- **LMS:**
  - el MP4 con su `.vtt`;
  - el banco de preguntas exportado a **Moodle XML o GIFT**, a partir del `banco` que ya existe;
  - un paquete SCORM, más adelante.
- **YouTube:**
  - miniatura de 1280×720 en JPG;
  - título, descripción y etiquetas;
  - **capítulos** (`0:00 …`) calculados con los tiempos de cada lámina;
  - `.srt`.
- **Redes, historias y estados:**
  - versión 9:16 de 1080×1920, con la composición rehecha en la plantilla vertical (no un recorte);
  - subtítulos quemados;
  - cortes de 60 s o menos, cada uno con su gancho y su CTA de la marca;
  - hay que verificar el límite actual de duración en WhatsApp e Instagram.
- **Entrega al cliente:** una carpeta con los MP4, los subtítulos, las miniaturas, `manifiesto.json` (qué video es, su versión, quién lo aprobó y los SHA-256) y el informe de control de calidad.

## 4. Agentes y modelos gratuitos (IA local con Ollama)
El material es del cliente, así que conviene correr la IA **en local**.

- **Modelos:** con 4 GB de VRAM y 8 GB de RAM caben modelos de 2 a 4 B cuantizados. Todo lo que genere la IA entra como borrador y alguien lo aprueba en la interfaz.
  - **`qwen3:4b`** (unos 2,5 GB, Apache 2.0): el principal para escribir guiones y preguntas; es el mejor en español dentro de ese tamaño.
  - **`qwen3.5:2b`** (unos 2,7 GB): el más rápido, para tareas cortas como títulos o etiquetas. También lee imágenes, así que puede describir las láminas.
  - **`gemma3:4b`**, **`phi4-mini`** o **`granite4.1:3b`**: como segunda opinión.
  - Un modelo de 7 u 8 B se desborda a la RAM y va lento. Con 16 GB de RAM y una tarjeta de 8 GB ya entraría `gemma4`, de más calidad.
- **Agentes propuestos:**
  1. **Guionista:**
     - propone la narración de las láminas sin notas, a partir de lo que muestra la lámina;
     - acorta los videos de más de 4 minutos;
     - reescribe para que suene hablado.
  2. **Verificador normativo:** toma las citas que detecta `_NORMATIVO` y arma una lista de revisión con la pregunta «¿cuál es la fuente?». No inventa fuentes.
  3. **Banco de preguntas:** genera 3 a 5 preguntas por video en el mismo formato de `_leer_banco`, con la lámina de la que sale cada una.
  4. **Publicador:** escribe títulos, descripción de YouTube, etiquetas, textos para historias y el gancho de los primeros 3 s.
- **Lo que NO conviene en este equipo:** generar imágenes con FLUX o SDXL (necesitan 12 GB o más de VRAM). Para imágenes de relleno se usan las APIs gratuitas de **Pexels o Pixabay**, que permiten uso comercial, guardando el crédito de cada imagen.
- **Descartados por licencia comercial:** XTTS-v2 y F5-TTS (voz), MusicGen (música) y edge-tts (usa un servicio de Microsoft sin licencia de uso).
- **Voz gratis de calidad con licencia comercial:**
  - **Kokoro-82M** (Apache 2.0): corre en CPU y es la mejor calidad para su tamaño. Hay que escuchar sus voces en español contra Carlos antes de decidir.
  - **Piper** (MIT): más robótica, pero instantánea. Sirve para borradores.
  - **Higgs Audio V2** (Apache 2.0): de más calidad, pero no cabe en 4 GB de VRAM.
  - La voz final sigue siendo Carlos en ElevenLabs, que es de pago.

## 4b. Herramientas de IA para programar el proyecto
- **OpenCode** (código abierto, se usa en la terminal): sí vale la pena instalarlo como agente gratuito de apoyo. Se conecta a:
  - **Ollama**, en local y sin costo, con `qwen2.5-coder:3b` o `qwen3:4b`, que caben en 4 GB;
  - proveedores con capa gratuita, como Google Gemini o Groq.
- **Limitación honesta:** en este equipo los modelos de código locales (3 a 4 B) sirven para tareas pequeñas (explicar un archivo, escribir una prueba, renombrar), pero no para cambios de arquitectura en varios archivos. Esos siguen con Claude Code.
- **Regla de privacidad:** los PPTX y guiones de clientes solo se procesan con modelos locales. Las capas gratuitas en la nube pueden usar lo que se les envía para entrenar sus modelos: sirven para el código del proyecto, no para el material del cliente.
- **Alternativas equivalentes a OpenCode**, si se prefiere trabajar dentro de VS Code: **Continue** o **Cline**, ambas con licencia Apache 2.0 y compatibles con Ollama. **Aider** también es Apache 2.0 y funciona en la terminal, bien integrado con git. Basta instalar una de ellas: **OpenCode** en la terminal o **Continue** en VS Code.

## 5. Instalación
- **Ya hecho (29-sep):** en `.venv` quedaron instalados `piper-tts 1.8.0`, `onnxruntime 1.30.0`, `playwright 1.63.0` y `num2words 0.5.14`. No se cambió ningún archivo del proyecto; `requirements.txt` sigue sin estas dependencias.
- Pendiente:
  - `playwright install chromium`;
  - descargar la voz de Piper `es_ES-davefx-medium` y revisar la licencia en su tarjeta del modelo;
  - `pip install faster-whisper`, que se usa en la Fase 1 para el control de calidad.
- **Decisión para la Fase 1:** el render se hace con **Playwright y ffmpeg**, no con HyperFrames. Todo queda en Python, sin Node y con licencia conocida. Para que sea rápido, solo se capturan cuadro a cuadro los ~1,2 s de animación de entrada de cada lámina; el resto de la lámina es el último cuadro fijo, que ffmpeg extiende hasta que termina el audio. HyperFrames queda para las fases 3 y 4, si hacen falta animaciones más ricas.
- Node.js, si se usa HyperFrames. Hay que verificar si está instalado.
- `ollama pull qwen3:4b` y `ollama pull qwen3.5:2b`. Opcional, para programar: `ollama pull qwen2.5-coder:3b`.
- Opcional: instalar OpenCode y conectarlo a Ollama.
- Kokoro: `pip install kokoro`, para compararlo con Piper y con Carlos.
- LibreOffice es opcional: solo sirve para ver una miniatura de la lámina original al lado de la plantilla.

## 6. Orden recomendado
1. **Fase 1, el primer MP4 que se puede subir** ✅ (sin música):
   - extraer las imágenes;
   - normalizar el texto;
   - generar la voz con Piper o ElevenLabs;
   - usar 3 plantillas de 16:9;
   - renderizar, mezclar y generar el `.vtt`;
   - pasar el control de calidad;
   - añadir el botón «Producir» y la descarga.
2. **Fase 2, el editor y la aprobación:**
   - editar el guion y reagrupar láminas;
   - la cola de render con progreso;
   - enlazar con `proyectos.json`.
3. **Fase 3, redes:**
   - plantillas 9:16 y cortes para historias;
   - subtítulos quemados;
   - miniaturas, capítulos y metadatos de YouTube.
4. **Fase 4, los agentes locales y las entregas:**
   - los agentes de Ollama;
   - la exportación a Moodle y GIFT;
   - el manifiesto de entrega.

## Archivos clave
- Se reutilizan:
  - `app/taller.py`: `orden_produccion`, `curso_json`, `resumen`, `guardar`;
  - `app/extractor.py`: `frases`, `segundos`, `_NORMATIVO`;
  - `app/datos.py`: `cambiar_estado`, `marcas`, `ruta_segura`.
- Se modifican:
  - `app/extractor.py`, para extraer las imágenes;
  - `app/main.py`, para las rutas de render, estado y descarga;
  - `app/templates/taller.html`, para el editor y el botón «Producir»;
  - `app/static/app.js`, para la consulta del progreso;
  - `requirements.txt`.
- Se crean: el paquete `motor/` y `tests/test_motor.py`.

## Verificación
- `tests/test_motor.py`:
  - arma un PPTX de 2 láminas con python-pptx y lo renderiza con Piper;
  - comprueba con ffprobe que sale 1920×1080, 30 fps, H.264 y AAC, que la duración queda a ±10 % de `extractor.segundos` y que el volumen está a -14 ±1 LUFS;
  - comprueba que el `.vtt` tiene tantas entradas como frases.
- Todas las pruebas de siempre (`python -m pytest`) deben seguir pasando.
- **De punta a punta:** con `config.local.json` configurado, se usa el ejemplo del curso csm en el taller y se produce el módulo `m01`. Se compara con el entregable real de `ENTREGABLES-VIDEO` y se sube un video de prueba como no listado a YouTube y a un curso de prueba del LMS.
