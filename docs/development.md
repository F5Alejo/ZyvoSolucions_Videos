# Desarrollo

## Dónde está cada cosa

| Carpeta | Qué hay |
|---|---|
| `app/` | API (FastAPI): `main.py` (rutas), `taller.py` (cursos), `extractor.py` (PPTX), `configuracion.py`, `datos.py` |
| `motor/` | El pipeline: `produccion.py` (etapas), `videospec.py`, `analisis.py`, `voz.py`, `renderers.py`, `render.py`, `camara.py`, `audio.py`, `sfx.py`, `estilos.py`, `qa.py`, `bugs.py`, `errores.py`, `logs.py`, `versiones.py`, `cola.py`, `catalogo.py`, `proveedores.py`, `escenas/`, `agentes/` |
| `frontend/` | Vue 3 + TypeScript + Tailwind 4. El flujo de Zyvo en `views/CrearVideoView.vue` y `views/EditorVideoView.vue`, sus piezas en `components/zyvo/`, el estado en `composables/proyecto.ts` y los textos en `mensajes.ts` |
| `datos/` | Catálogos que van a git: marcas, voces, animaciones, estilos, configuración. Lo de cada equipo (`trabajos/`, `musica/`, `cache/`) no va a git |
| `tests/` | pytest y `fixtures/` (ver `testing.md`) |
| `scripts/` | Descargar modelos de voz y generar los PPTX de prueba |

## Correr en modo desarrollo

```sh
uvicorn app.main:app --port 8765 --reload   # la API
cd frontend && npm run dev                  # http://localhost:5173, se recarga al guardar
```

## Reglas del proyecto

- **Local primero:** archivos y JSON. Nada de bases de datos, Redis ni nube obligatoria.
- **Licencias:** solo MIT, Apache, BSD o servicios ya pagados (por eso no Remotion, y Piper solo para borradores).
- **La IA propone, no ejecuta:** todo valor sale de un catálogo y se valida (ver `agents.md` y `videospec.md`).
- **Nombres:** el código está en español (`trabajo`, `lamina`, `producir`); los conceptos nuevos usan
  los nombres del objetivo (`VideoSpec`, `TTSProvider`, `VideoRenderer`).
- **Estable antes que mucho:** pocos efectos que funcionan bien antes que muchos inestables.
- **Una opción nueva no debe desactualizar videos:** si no cambia el resultado, o vale lo de siempre,
  queda fuera de `produccion.firma`.

## Cómo agregar…

- **Una voz:** una entrada en `datos/voces.json`; un proveedor nuevo es una clase con `extension` y
  `generar(texto, destino)` en `voz.PROVEEDORES` (interfaz `TTSProvider`).
- **Un movimiento de cámara o una transición:** su filtro en `motor/camara.py` y su nombre en `motor/catalogo.py`.
- **Un estilo:** un JSON en `datos/estilos/` que solo use valores de los catálogos (se valida al cargar).
- **Un efecto de sonido:** su síntesis en `motor/sfx.py` y su nombre en `CATALOGO`.
- **Un agente:** su módulo en `motor/agentes/`, con `registrar(Agente(...))` y su entrada en `PERMISOS`.

## Git

Se trabaja en `Alejodev`; `main` solo cambia por pull request con las pruebas en verde. Los commits
van en español y **sin coautoría**. Cada cambio importante lleva su entrada en `bitacora.md`.
