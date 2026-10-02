# Los agentes

Zyvo usa agentes para analizar, proponer y revisar. Regla de oro: **la IA elige, no ejecuta.**
Nunca escribe código, comandos ni rutas; solo devuelve datos que se validan contra un catálogo.

## Quién es quién

| # | Agente (prompt maestro) | En Zyvo | IA | Qué hace | Puede cambiar |
|---|---|---|---|---|---|
| 1 | Analyzer | Analizador (`motor/analisis.py`) | No | Láminas, notas, imágenes, tablas, gráficos, tema, dificultad, avisos | Nada (solo `analisis.json`) |
| 2 | Scriptwriter | Guionista y Redactor de pantalla (`motor/agentes/textos.py`) | Ollama, o reglas | Narración para láminas mudas; títulos y viñetas cortas | `ediciones` |
| 3 | Visual Director | Director de animación (`motor/agentes/director.py`) | Ollama, o reglas | Plantilla y efectos por lámina, del catálogo | `animacion` |
| 4 | Voice Director | La persona elige la voz; `taller.voz_inicial` y el respaldo ElevenLabs → Kokoro | No | Voz que funciona en el equipo | — |
| 5 | Music Director | `estilos.elegir_musica` | No | Pista por energía entre las subidas con licencia | — |
| 6 | SFX Director | `sfx.dirigir` | No | Como mucho un efecto suave por escena, antes de la voz | — |
| 7 | Timeline Director | `videospec.resolver` | No | La línea de tiempo en cuadros exactos | — |
| 8 | QA Agent | `motor/qa.py` + Revisor de voz (Whisper) | Whisper local | Chequeos técnicos y de contenido | Nada |
| 9 | Bug Detector | `motor/bugs.py` | No | Cada chequeo fallido → bug con código, severidad, escena y recuperación | Nada |
| — | — | Verificador normativo, Descriptor de imágenes, Evaluador, Publicador | Ollama, o reglas | Fuente de cifras y normas, texto alternativo, preguntas, metadatos | `verificadas`, `imagenes`, `banco`, `publicacion` |

Los directores de voz, música, efectos y línea de tiempo son **reglas deterministas**, no un modelo:
son decisiones con pocas opciones donde una regla clara es más estable que una IA.

## Cómo se controla un agente

Cada agente con IA (`motor/agentes/base.py`) tiene:

- **nombre, versión, tiempo máximo por pregunta**;
- **permisos** (`PERMISOS`): qué partes del curso lee y cuáles puede cambiar. Al aceptar una
  propuesta se compara el curso antes y después: si tocó algo que no le corresponde, se deshace y
  se rechaza;
- **validación** de cada respuesta: JSON → esquema → valores permitidos. En una lista, lo inválido se
  quita y se cuenta; si nada sirve, el agente usa sus reglas;
- **guardas** contra lo inventado (`guardas.py`): si una propuesta trae una cifra o norma que no
  está en la lámina, se descarta.

Todo lo que propone un agente queda **pendiente** hasta que una persona lo acepta o lo descarta.

## IA local

Ollama en `localhost:11434` con `qwen3:4b` (texto) y `qwen3.5:2b` (visión). Los agentes corren en la
misma cola que los videos (nunca a la vez: el equipo tiene 8 GB) y el modelo se descarga de la
memoria al terminar. Sin Ollama, todo sigue funcionando con reglas.
