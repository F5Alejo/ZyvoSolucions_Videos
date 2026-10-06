# Arquitectura anterior a la migración (octubre 2026)

Cómo funcionaba el estudio **antes** de la migración, tal como estaba en la rama `Alejodev` el
1 de octubre de 2026. Se conserva como registro: para la arquitectura de hoy ver
[`arquitectura.md`](arquitectura.md), y para el análisis y el plan que llevaron a cambiarla,
[`plan-migracion.md`](plan-migracion.md). El plan de llevarla a la nube sigue en
[`plan-nube.md`](plan-nube.md); lo aprendido por el camino, en [`hallazgos.md`](hallazgos.md).

## Piezas

```
Navegador ── http://localhost:8765 ──> FastAPI (app/main.py)
                                         ├─ sirve la interfaz compilada (frontend/dist)
                                         ├─ API JSON /api/*  ──> app/taller.py, app/datos.py, app/configuracion.py
                                         └─ cola en memoria (motor/cola.py, un hilo)
                                                └─ motor/produccion.py · motor/empaquetar.py · motor/agentes/*
Disco local: datos/ (JSON y cursos) · modelos/ (voces) · .env (clave)
Externos opcionales: ElevenLabs (voz de pago) · Ollama en localhost:11434 (agentes)
```

Todo es **un solo proceso** de Python en una sola máquina. La API, la cola y el render comparten
CPU y memoria.

| Parte | Dónde | Qué hace |
|---|---|---|
| Interfaz | `frontend/` (Vue 3, TypeScript, Tailwind 4, Vite) | Inicio, cursos en 5 pasos (Presentación, Guion, Marca y voz, Animación, Resultado), Videos, Marcas, Pendientes y Configuración |
| API | `app/main.py` | JSON en `/api/*`, archivos en `/media/*` y la aplicación Vue en el resto de rutas |
| Extractor | `app/extractor.py` | PPTX → láminas (formas, notas, frases, imágenes). Las imágenes se guardan en `media/` |
| Taller | `app/taller.py` | Crear cursos, agrupar en videos, resumen y chequeos, ediciones por lámina y orden de producción |
| Datos | `app/datos.py` | Lee los JSON de `datos/`, carga `.env` y las rutas de `config.local.json` |
| Configuración | `app/configuracion.py` | `datos/configuracion.json` más los ajustes de cada curso (`ajustes_video`) |
| Motor | `motor/` | Ver «Del PPTX al MP4» |
| Agentes | `motor/agentes/` | Proponen mejoras; una persona las acepta o las descarta |

## Del PPTX al MP4

1. **Subir** (`POST /api/trabajos`): el PPTX se guarda en `datos/trabajos/<id>/entrada.pptx`; las láminas y los videos propuestos van a `trabajo.json`.
2. **Normalizar** (`motor/normalizar.py`): leyes, cifras, pesos, porcentajes y siglas a palabras para la voz. Los subtítulos conservan el texto original.
3. **Voz** (`motor/voz.py`): un audio por frase, con caché por voz y texto (`cache/voz/`). Proveedores: Kokoro (local, Apache 2.0), Piper (solo borradores) y ElevenLabs (de pago, con la clave de `.env`).
4. **Escenas** (`motor/escenas/`): una plantilla HTML de marca por lámina (portada, lista o imagen). Las entradas y salidas salen de la plantilla de animación: plantilla del curso, luego ajustes del curso, luego ajustes de la lámina (`animacion.py`, `efectos.py`).
5. **Render** (`motor/render.py`): Chromium (Playwright) dibuja cuadro a cuadro solo la entrada y la salida, y ffmpeg sostiene lo del medio. También revisa el encuadre («Todo el texto cabe»).
6. **Audio** (`motor/audio.py`): la pista de narración, la música con *sidechain* si la hay, y el volumen a -14, -16 o -23 LUFS en estéreo.
7. **Subtítulos** (`motor/subtitulos.py`): VTT y SRT con los tiempos reales; pueden ir quemados en la imagen.
8. **Control de calidad** (`motor/qa.py`): resolución, fps, códecs, sincronía, LUFS, pantallas negras y silencios.
9. **Curso completo y ZIP** (`motor/empaquetar.py`): une los videos sin recodificar, con tarjetas, capítulos y subtítulos unidos, y arma un ZIP con manifiesto SHA-256.

## Dónde se guarda cada cosa

| Qué | Dónde | ¿En git? |
|---|---|---|
| Fichas de marca, proyectos, voces, casos | `datos/*.json`, `datos/marcas/` | Sí |
| Configuración del estudio | `datos/configuracion.json` | Sí |
| Plantillas de animación | `datos/animaciones/` (las propias en `propias/`) | Las de fábrica sí |
| Cursos: PPTX, imágenes, `trabajo.json`, salida, caché de voz | `datos/trabajos/<id>/` | **No** (material de clientes) |
| Música de fondo con su licencia | `datos/musica/` | No |
| Modelos de voz Kokoro y Piper | `modelos/` | No (`scripts/descargar_modelos.py`) |
| Clave de ElevenLabs | `.env` | **No** (plantilla: `.env.ejemplo`) |
| Rutas del repositorio de videos | `config.local.json` | No |

## La cola

`motor/cola.py` atiende **un trabajo a la vez** en un hilo del mismo proceso: videos, el curso
completo y agentes. El estado de cada trabajo vive en `salida/<clave>/estado.json` y la interfaz lo
consulta cada 2 o 3 s. Si el servidor se reinicia, lo que estaba en la cola se pierde y la tarjeta
lo marca como interrumpido.

## Agentes

Viven en `motor/agentes/`: el cliente de Ollama, las guardas contra cifras inventadas, la base de
propuestas y los 8 agentes. Corren en la misma cola que los renders. El modelo queda cargado 2 min
mientras el agente trabaja y se descarga al terminar. Sin Ollama usan reglas sin IA, salvo el Evaluador.

## Dependencias del sistema

Python 3.12 o superior, Node 20 o superior, ffmpeg, Chromium de Playwright, modelos de voz y,
de forma opcional, Ollama (`qwen3:4b` y `qwen3.5:2b`) y faster-whisper. `instalar.ps1` deja todo
listo en Windows. En Linux (GitHub Actions) se usa ffmpeg estático y `playwright install chromium`.

## Rendimiento medido (PC con i5-11400H, 8 GB y GTX 1650)

| Qué | Tiempo |
|---|---|
| Render con Kokoro en CPU | ~1,5 a 2 veces la duración del video (2 min de video ≈ 3 a 4 min) |
| Video de 12 s con ElevenLabs | ~22 s |
| Unir el curso completo | segundos (no recodifica) |
| Redactor (2 láminas, `qwen3:4b`) | 22 s |
| Descriptor de imágenes (`qwen3.5:2b`, visión) | ~60 s por imagen la primera vez |
| Revisor de voz (Whisper `small` int8) | ~5 s por video corto |
| Pruebas: pytest (75) / Vitest (10) | ~85 s / ~20 s |

## Límites conocidos

- Sin usuarios ni inicio de sesión: es para uso local.
- Los datos son JSON escritos sin bloqueo: hay riesgo si dos personas guardan a la vez.
- Una sola cola en memoria y un solo worker.
- Solo formato 16:9: el 9:16 está en el plan.
- En 8 GB no conviene un render junto con un modelo de 4 B: por eso comparten la cola.
