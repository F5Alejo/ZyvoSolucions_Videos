# Arquitectura de Zyvo (después de la migración)

El análisis completo, con lo que había, los problemas y las decisiones, está en
[`plan-migracion.md`](plan-migracion.md). Aquí, cómo quedó.

```
Navegador ── http://localhost:8765 ─▶ FastAPI (app/main.py)
   │  /crear  (flujo de Zyvo)                ├─ app/: taller, extractor, configuración, datos
   │  /cursos (modo experto)                 └─ motor/cola.py ── un trabajo a la vez
   │                                                │
   ▼                                                ▼
frontend/ (Vue 3)                     motor/produccion.py  — etapas con registro, reintentos y respaldo
  composables/proyecto.ts (estado)      plan ─▶ voz ─▶ escenas ─▶ audio ─▶ unir ─▶ subtítulos ─▶ QA ─▶ versión
  generacion.ts · mensajes.ts             │       │        │         │                          │
                                     videospec.py  voz.py  renderers.py  audio.py · sfx.py      qa.py · bugs.py
                                     (contrato)   (TTS)    render.py     estilos.py (música)
                                                           camara.py
Agentes: motor/analisis.py (Analizador) y motor/agentes/* (con permisos y respuestas validadas)
Proveedores: motor/proveedores.py — TTSProvider · LLMProvider · VideoRenderer
Datos locales: datos/ (catálogos en git) · datos/trabajos/<id>/ (cada proyecto, fuera de git)
```

## Correspondencia con la estructura objetivo del prompt

| Objetivo | En Zyvo |
|---|---|
| `apps/api` | `app/main.py` |
| `apps/web` | `frontend/` |
| `core/domain` (presentation, slide, scene, timeline, video) | `motor/videospec.py` (Escena, Frase, Efecto, Video, Audio) y `motor/analisis.py` |
| `core/pipeline` (stages, jobs) | `motor/produccion.py` (etapas), `motor/cola.py` (trabajos) |
| `core/providers` (tts, llm, render, music, sfx) | `motor/proveedores.py`, `voz.py`, `agentes/ollama.py`, `renderers.py`, `estilos.py`, `sfx.py` |
| `presentation/pptx` | `app/extractor.py` |
| `video/` (scenes, templates, transitions, effects, subtitles) | `motor/escenas/`, `camara.py`, `catalogo.py`, `subtitulos.py` |
| `audio/` (narration, music, sfx, mixing, mastering) | `voz.py`, `normalizar.py`, `sfx.py`, `audio.py` |
| `ai/` (analysis, scripting, animation, quality) | `analisis.py`, `agentes/`, `qa.py`, `bugs.py` |
| `storage/projects/{id}` | `datos/trabajos/<id>/` |
| `config/` (voices, styles, animations…) | `datos/voces.json`, `datos/estilos/`, `datos/animaciones/`, `datos/configuracion.json` |

Se decidió **no mover las carpetas**: el código ya está separado por responsabilidad y moverlo solo
rompería imports y la historia de git sin mejorar el video (ver `plan-migracion.md`, sección 5.3).
