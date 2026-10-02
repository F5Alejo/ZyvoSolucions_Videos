# Arquitectura de Zyvo: lo que hay, lo que falla y cómo llegar al objetivo

> **Fase 1 del «prompt maestro»** (2026-10-01). Este documento solo analiza: no cambia código.
> Está escrito sobre la rama `Alejodev` (igual a `main`, commit `0201136`). Lo que ya está
> documentado se enlaza en lugar de repetirse: [`docs/arquitectura-actual.md`](docs/arquitectura-actual.md),
> [`docs/hallazgos.md`](docs/hallazgos.md) y [`docs/bitacora.md`](docs/bitacora.md).

## Estado de la migración (2026-10-02)

Las secciones 1 a 6 son el análisis de partida y siguen como registro. Así quedó cada fase (detalle
en [`docs/bitacora.md`](docs/bitacora.md); cómo quedó la arquitectura en [`docs/architecture.md`](docs/architecture.md)):

| Fase | Estado | Dónde |
|---|---|---|
| 0 · Línea base y voz que funciona | Hecha | `instalar.ps1`, `taller.voz_inicial` |
| 1 · Este análisis | Hecha | este archivo |
| 2–3 · VideoSpec y separar etapas | Hecha | `motor/videospec.py`, `motor/produccion.py`, `motor/recursos.py` |
| 4 · Agentes con permisos y respuestas validadas; Analizador | Hecha | `motor/agentes/base.py`, `motor/analisis.py` |
| 5 · Proveedores | Hecha | `motor/proveedores.py`, `motor/renderers.py` |
| 6 · Checkpoints, caché de escenas y reintentos | Hecha | `salida/<clave>/escenas/`, `produccion.correr` |
| 7 · QA, errores con código y detector de bugs | Hecha | `motor/qa.py`, `motor/errores.py`, `motor/bugs.py`, `motor/logs.py` |
| 8–10 · Renderer, cámara, transiciones y formatos | Hecha (sin Remotion, por licencia) | `motor/camara.py`, `motor/catalogo.py` |
| 11 · Línea de tiempo | Hecha | `videospec.linea_de_tiempo`, `GET /api/trabajos/{id}/linea/{clave}` |
| 12 · Audio: efectos y director de música | Hecha | `motor/sfx.py`, `motor/estilos.py` |
| 13 · Estilos | Hecha | `datos/estilos/` |
| 14–15 · Interfaz y editor | Hecha | `frontend/src/views/CrearVideoView.vue`, `EditorVideoView.vue`, `components/zyvo/` |
| 16 · Fixtures y prueba de punta a punta | Hecha | `tests/fixtures/`, `tests/test_e2e.py` |
| Versiones del video y regeneración selectiva | Hecha | `motor/versiones.py` |

Lo que queda fuera a propósito: Remotion (licencia), Piper como respaldo (licencia), mover el código
a la estructura de carpetas del objetivo (sección 5.3), paralaje, paneos verticales y fundido cruzado
(ver `motor/catalogo.py`).

## 1. En una frase

Zyvo **ya convierte un PPTX en MP4** con voz, animaciones de catálogo, música con *ducking*,
subtítulos, control de calidad, curso completo con capítulos y ZIP. Lo que le falta no es
funcionalidad básica sino **estructura**: el paso del PPTX al MP4 es una sola función larga, no hay
un contrato intermedio (VideoSpec) que se pueda guardar, revisar y repetir por partes, y no hay
reintentos ni respaldos cuando algo falla.

Por eso la recomendación es **evolucionar, no reconstruir**: casi todas las piezas que pide el
objetivo existen con otro nombre y funcionan (sección 3).

## 2. Arquitectura actual

### 2.1 Piezas

```
Navegador ── http://localhost:8765 ──> FastAPI  app/main.py  (672 líneas, 52 rutas)
                                         │
              ┌──────────────────────────┼──────────────────────────────┐
              ▼                          ▼                              ▼
   app/  (lógica del estudio)     motor/cola.py (1 hilo, en memoria)   frontend/dist (Vue 3)
   ├─ extractor.py  PPTX → láminas       │
   ├─ taller.py     curso, videos,       ├─ motor/produccion.py   un video, de punta a punta
   │                ediciones, resumen   ├─ motor/empaquetar.py   curso completo y ZIP
   ├─ configuracion.py  ajustes          └─ motor/agentes/*       8 agentes (proponen)
   └─ datos.py      JSON de datos/, .env, config.local.json
                                         motor/ (pasos del video)
                                         ├─ normalizar.py  cifras y leyes → palabras
                                         ├─ voz.py         Kokoro · Piper · ElevenLabs + caché
                                         ├─ escenas/       HTML de marca + catálogo de efectos
                                         ├─ render.py      Playwright cuadro a cuadro + ffmpeg
                                         ├─ audio.py       pista, música, LUFS
                                         ├─ subtitulos.py  VTT / SRT
                                         └─ qa.py          ffprobe + filtros de ffmpeg
```

Todo es local: archivos JSON y carpetas, ffmpeg, Chromium, modelos de voz en `modelos/`, Ollama
opcional en `localhost:11434`. No hay base de datos ni servicios en la nube obligatorios (ElevenLabs
es opcional). **Esto ya cumple las reglas 5–14 y 57 del objetivo y hay que conservarlo.**

### 2.2 Del PPTX al MP4 hoy

`motor/produccion.py:62` (`producir`) hace, en una sola llamada:

1. resumen del curso (`taller.resumen`) → láminas efectivas con sus ediciones;
2. voz frase por frase (con caché por SHA-256 de voz + texto);
3. **línea de tiempo** en cuadros exactos (aquí se decide cuánto dura cada lámina);
4. HTML de cada escena con su plan de animación (`animacion.plan`) → render con Playwright;
5. pista de narración → música con *sidechain* → normalización a LUFS → `render.unir`;
6. subtítulos (y quemado opcional);
7. QA y `qa.json` (que ya trae la línea de tiempo por lámina y una **firma** de lo que lo produjo).

### 2.3 Dependencias entre módulos

```
app/main.py ──> app/*  y  motor/*
motor/*     ──> app/taller, app/configuracion, app/datos, app/extractor   ← el motor depende de la API
app/taller  ──> app/configuracion (import tardío: «para evitar un import circular»)
app/main.py ──> motor.produccion._logo / _media                         ← funciones privadas
motor/escenas ──> app.extractor._forma / _SECCION                        ← funciones privadas
```

### 2.4 Pruebas e integración continua

- 63 funciones de prueba en `tests/` (6 archivos; el README cuenta 75 por las parametrizadas).
  Producen MP4 reales con una voz de prueba (un tono) y Ollama simulado: no necesitan claves.
- Los PPTX de prueba se generan en código con `python-pptx` (`tests/test_motor.py:18`); no hay
  carpeta `tests/fixtures/`.
- GitHub Actions: pytest + ffmpeg + Chromium, Vitest + `vue-tsc`, ruff, gitleaks y el instalador en
  Windows. Sube un video de muestra como artefacto.
- **En este equipo no se pudo correr la línea base**: no hay Python ni ffmpeg instalados (solo Node
  24). Antes de la Fase 2 hay que correr `instalar.ps1 -Probar` o confiar en el último verde de
  Actions (ver sección 7).

## 3. Lo que ya existe frente a lo que pide el objetivo

| Objetivo (prompt maestro) | Qué hay hoy | Dónde | Estado |
|---|---|---|---|
| Extracción del PPTX | Formas con nombre, notas, frases, foto e ícono, imágenes a `media/` | `app/extractor.py` | ✅ Funciona; no lee tablas ni gráficos |
| Modelo de presentación | Diccionarios sueltos (`lamina`, `trabajo`) sin esquema | `app/taller.py` | ⚠️ Sin tipos |
| **VideoSpec** | Parcial y repartido: `orden_produccion` (v1, nadie la consume), `animacion.plan`, la línea de tiempo dentro de `producir` y `qa.json` | `taller.py`, `produccion.py` | ❌ No hay contrato único |
| Catálogos cerrados | Efectos de entrada/salida por elemento, curvas y límites | `motor/escenas/efectos.py:51-88` | ✅ Y se validan (`AnimacionInvalida`) |
| Estilos | 5 plantillas de animación + 4 fichas de marca (colores, logo, pronunciación) | `datos/animaciones/`, `datos/marcas/` | ✅ Falta unir marca + animación + música en un «estilo» |
| Agentes con permisos limitados | 8 agentes que **proponen**; una persona acepta. Esquema JSON en Ollama, listas `enum`, guarda contra cifras inventadas | `motor/agentes/` | ✅ El principio de la regla 6 ya se cumple |
| Analyzer / Scriptwriter / Visual Director | Descriptor de imágenes, Redactor, Guionista, Verificador, Director de animación | `motor/agentes/textos.py`, `director.py`, `revision.py` | ✅ Con otros nombres |
| Voice / Music / SFX / Timeline Director | No hay agentes; la voz y la música se eligen a mano; el timeline lo calcula `producir` | — | ❌ |
| QA Agent | 8 chequeos técnicos + «el texto cabe» + Revisor de voz (Whisper) | `motor/qa.py`, `render.py` | ✅ Faltan cuadros congelados, *clipping*, caracteres raros |
| Bug Detector con severidad y código | Errores como texto; *traceback* guardado en `estado.json` | `motor/cola.py:105` | ❌ |
| `TTSProvider` común | Tres clases con el mismo método `generar(texto, destino)` | `motor/voz.py` | ⚠️ Interfaz implícita, sin respaldo entre proveedores |
| Caché por hash | Voz por SHA-256 (voz + ajustes + texto) | `motor/voz.py` | ✅ Solo la voz |
| Checkpoints y reanudar | El render borra `tmp/` al empezar y al terminar; solo sobrevive la caché de voz | `produccion.py:81,167` | ❌ |
| Estados del pipeline | `en_cola → produciendo → listo / error` con paso y porcentaje | `motor/cola.py` | ⚠️ Pocos estados, sin reintentos |
| Versiones del video | Se sobrescribe `<clave>.mp4`; la firma dice si quedó desactualizado | `produccion.py:firma` | ❌ |
| Formatos 16:9 / 9:16 / 1:1 / 4:5 | Lienzo 9:16 definido en escenas, pero el motor fija 16:9 | `produccion.py:75` | ❌ |
| Cámara (zoom, pan) | Mientras habla la voz la lámina queda quieta (ffmpeg repite el último cuadro) | `render.py` | ❌ Es el mayor salto de calidad pendiente |
| Música / *ducking* / LUFS | Pista en bucle, fundidos, *sidechain*, LUFS de 2 pasadas | `motor/audio.py` | ✅ |
| SFX | — | — | ❌ No hay efectos ni catálogo con licencia |
| Renderer intercambiable | Playwright + ffmpeg, cableado dentro de `producir` | `motor/render.py` | ⚠️ |
| Remotion | Descartado a propósito (ver 5.1) | `docs/bitacora.md` 2026-09-29 | — |
| Logs estructurados | No hay; solo `estado.json` | — | ❌ |
| Interfaz para no técnicos | 5 pasos completos, pero pensada para el equipo de producción (LUFS, CRF, fps a la vista en Configuración) | `frontend/` | ⚠️ |

## 4. Problemas encontrados

Ordenados por cuánto bloquean el objetivo.

1. **No hay contrato intermedio.** `producir` calcula, decide y ejecuta a la vez. No se puede
   guardar «qué se va a hacer», mostrarlo en un timeline, editar una escena ni volver a dibujar solo
   una. Es el cuello de botella de las fases 2, 6, 11, 15 y de la regeneración selectiva (regla 68).
2. **Todo o nada.** Si falla el render de la lámina 9, se repite todo salvo la voz. No hay
   reintentos (regla 19) ni respaldos (regla 20).
3. **La voz por defecto no se puede usar en un equipo nuevo.** `configuracion.py:16` y
   `datos/configuracion.json:4` eligen «Carlos» (ElevenLabs) y la clave caducó el 21-sep-2026. Un
   usuario no técnico choca con un error en su primer video. Arreglo pequeño y de alto impacto.
4. **El motor depende de la API** (`motor/* → app/*`) y hay imports de funciones privadas en ambos
   sentidos (`main.py:382,433`, `escenas/__init__.py:76`). Mover carpetas hoy rompería cosas en
   cadena; primero hay que cortar esas dependencias.
5. **`app/main.py` hace demasiado**: rutas, armado de respuestas, la vista previa de escenas
   (reescribe rutas `file://` dentro del HTML) y la subida de música.
6. **Cola en memoria**: si el servidor se reinicia, lo encolado se pierde (se marca «interrumpido»).
   Aceptable para uso local, pero con checkpoints se podría reanudar.
7. **JSON sin bloqueo**: `taller.guardar` es atómico, pero leer-modificar-guardar desde la persona y
   desde un agente a la vez puede perder un cambio (los agentes ya releen para mitigarlo).
8. **Marca del producto**: el título de la API, el README, los logos y `package.json` dicen
   «Estudio de video RiskMann». Zyvo es el producto; RiskMann es una de sus marcas cliente.
9. **Errores técnicos al usuario**: el mensaje genérico está bien, pero hay rutas donde el texto de
   una excepción llega tal cual a la interfaz (el manejador de `ValueError` en `main.py`).

Lo que **funciona bien y no se debe tocar sin motivo**: el render determinista por cuadros, la
normalización de audio, `normalizar.py`, las guardas contra cifras inventadas, la caché de voz, la
validación de animaciones y las rutas que solo sirven archivos permitidos.

## 5. Decisiones

> **Tomadas el 2026-10-01:** el usuario aceptó las cuatro recomendaciones de esta sección.

### 5.1 Remotion y la licencia (choca con una decisión ya tomada)

La bitácora del 2026-09-29 descartó Remotion porque **pide licencia de pago a empresas** (más de 3
personas), y el proyecto se fijó la regla de usar solo MIT, Apache, BSD o servicios ya pagados.
Además, lo que Remotion aporta (llevar cada animación a un cuadro exacto) es justo lo que ya hace
`render.py` con Chromium.

**Recomendación:** hacer la fase 8 como una interfaz `VideoRenderer` con el renderer actual como
implementación principal, e invertir el esfuerzo en lo que de verdad falta (cámara, componentes de
escena, formatos). Remotion se agrega como segundo renderer **solo si** se compra la licencia.

### 5.2 Cadena de respaldo de voces

El objetivo propone `ElevenLabs → Kokoro → Piper`. Piper davefx **no se puede entregar** (licencia
de su base, ver `docs/hallazgos.md`). **Recomendación:** `ElevenLabs → Kokoro`, y Piper solo para
borradores con su sello, nunca como respaldo silencioso de un video final. El respaldo cambia la voz,
así que el resultado debe decir «se usó la voz X porque Y falló».

### 5.3 Nombres y carpetas

El código está en español (`trabajo`, `lamina`, `producir`) y el objetivo usa una estructura en
inglés (`core/domain`, `core/pipeline/stages`). Mover y renombrar todo de una vez es el cambio más
riesgoso posible y no mejora el video.

**Recomendación:** los conceptos nuevos usan los nombres del objetivo (`VideoSpec`, `TTSProvider`,
`VideoRenderer`, etapas), pero viven al principio dentro de `motor/` y `app/`. La estructura de
carpetas final se alcanza en la fase 10, cuando el pipeline ya esté en etapas y las dependencias
privadas cortadas, y se hace con módulos puente para no romper imports.

### 5.4 SFX y música

No hay ningún efecto de sonido en el repositorio. Un catálogo de SFX necesita archivos con licencia
comercial clara (y su licencia guardada al lado, como ya se hace con la música).

## 6. Propuesta

### 6.1 VideoSpec en dos momentos

La duración de cada escena **depende de la voz**: no se conoce hasta generar el audio. Por eso el
VideoSpec tiene dos estados del mismo documento:

| Momento | Qué tiene | Quién lo escribe |
|---|---|---|
| `videospec.plan.json` | escenas, texto de narración, voz, estilo, animación, transición, cámara, música, subtítulos; duraciones **estimadas** | etapa *plan* (sin costo: segundos) |
| `videospec.json` | lo mismo con duraciones **reales** en cuadros, y la ruta y el hash de cada audio | etapa *voz* |

El renderer solo lee `videospec.json`. Se arma con lo que ya existe: `taller.resumen` (escenas y
narración), `animacion.plan` (animación ya resuelta y validada), la línea de tiempo de
`producir` (duraciones) y `configuracion.para_trabajo` (video y audio). Lleva `version: 1` y se
valida con Pydantic (ya viene con FastAPI): esquema → valores del catálogo → coherencia
(lámina existe, duración > 0, fps y resolución permitidos). Un valor fuera del catálogo se cambia
por el valor por defecto y queda anotado como aviso `INVALID_EFFECT`; nunca se ejecuta.

### 6.2 Pipeline en etapas con checkpoints

Cada etapa lee archivos, escribe archivos y se puede repetir sola:

```
plan ──> voz ──> escenas (HTML) ──> render (por escena) ──> audio ──> unir ──> subtítulos ──> QA
 │        │         │                    │                     │                              │
 ▼        ▼         ▼                    ▼                     ▼                              ▼
videospec videospec escenas/NNN.html  escenas/NNN.mp4     narracion.wav                    qa.json
.plan     .json     (hash)            (hash)              (hash)
```

- Cada escena se dibuja a su propio `escenas/NNN.mp4` con un hash de su HTML + ajustes de video:
  si no cambió, no se vuelve a dibujar. **Esto ya da la regeneración selectiva por escena** sin un
  editor nuevo.
- Hoy el render ya produce partes por escena (`parte-NNN.mp4`) y luego las borra; el cambio es
  guardarlas con su hash en lugar de borrar `tmp/`.
- Un `estado.json` por video con la etapa actual, intentos y el último error con código.

Carpetas: el objetivo pide `storage/projects/{id}/…`; hoy existe `datos/trabajos/<id>/` con
`entrada.pptx`, `media/`, `cache/` y `salida/`. **Se mantiene** `datos/trabajos/<id>/` (no rompe
cursos existentes ni el `.gitignore`) y se agregan dentro las carpetas que faltan.

### 6.3 Errores, reintentos y respaldo

- Una excepción con `codigo` (`PPTX_001`, `TTS_001`, `RENDER_001`…), `severidad` y `recuperacion`.
  La interfaz muestra el texto humano; el *traceback* va a `logs/` del curso (JSON por línea).
- Reintentos por etapa con límite (3) solo para errores transitorios (red, ElevenLabs 5xx, Chromium
  que se cae). Un error de la persona (falta la clave) no se reintenta.
- Respaldo de voz según 5.2, anotado en el informe.

### 6.4 Interfaces de proveedores

`TTSProvider` (formaliza lo que ya hacen las tres clases de `voz.py`), `LLMProvider` (envuelve
`ollama.py`; las reglas sin IA son su respaldo), `VideoRenderer` (envuelve `render.py`). Música y SFX
como catálogos JSON en `datos/` con licencia por archivo; no hacen falta clases hasta que haya un
segundo proveedor.

## 7. Plan de migración

Cada fase termina con: pytest, Vitest y `vue-tsc` en verde, un video real producido, una entrada en
la bitácora y un commit en `Alejodev`. Si algo existente se rompe, se arregla antes de seguir.

| # | Fase | Primer entregable concreto | Riesgo |
|---|---|---|---|
| 0 | **Línea base** | Instalar Python 3.12 + ffmpeg en este equipo (`instalar.ps1 -InstalarFfmpeg -Probar`), registrar el número de pruebas y un video de referencia | — |
| 0b | Arreglo rápido | Voz por defecto Kokoro en cursos nuevos (o la primera voz disponible) | Bajo |
| 2 | VideoSpec | `motor/videospec.py` (Pydantic) + `construir_plan(t, clave)` + pruebas; `producir` lo escribe pero aún no lo usa | Bajo: solo agrega |
| 3 | Separar | `producir` renderiza **desde** `videospec.json`; cortar imports privados (`_logo`, `_media`, `_forma` pasan a ser públicos y van a su módulo) | Medio: el test de producción real lo cubre |
| 4–5 | Agentes y proveedores | `TTSProvider`, `VideoRenderer`, `LLMProvider` como interfaces sobre lo que ya existe; respaldo de voz | Bajo |
| 6 | Checkpoints | Escenas con hash, `estado.json` por etapa, reintentos | Medio |
| 7 | QA y errores | Códigos de error, logs JSON, chequeos nuevos (cuadros congelados, *clipping*) | Bajo |
| 8–10 | Renderer y cámara | Movimiento de cámara del catálogo (zoom lento, paneo) como CSS animado durante toda la escena; formatos 9:16 / 1:1 / 4:5 | **Alto en tiempo de render**: dejar de sostener el cuadro obliga a dibujar más cuadros; medir antes |
| 11–13 | Timeline, audio, estilos | Timeline visual de solo lectura sobre `videospec.json`; SFX con catálogo; «estilo» = marca + animación + música | Medio |
| 14–15 | Interfaz y editor | Flujo simple «Subir → Estilo → Voz → Crear» encima del actual; el flujo de 5 pasos queda como modo avanzado | Medio |
| 16 | E2E y fixtures | `tests/fixtures/` con los 7 PPTX (generados por un script, para que sean reproducibles) | Bajo |

Lo primero que da valor visible al usuario es la fase 0b; lo primero que desbloquea todo lo demás
es la fase 2.

## 8. Riesgos

- **Tiempo de render con cámara**: hoy una lámina de 40 s cuesta lo mismo que una de 5 s porque se
  sostiene el cuadro. Un zoom continuo rompe ese atajo. Alternativa a medir: aplicar el zoom/paneo
  con el filtro `zoompan` o `scale+crop` de ffmpeg sobre el cuadro sostenido, sin Chromium.
- **8 GB de RAM**: cualquier agente nuevo (Voice, Music, Timeline Director) debe seguir en la misma
  cola que el render.
- **Cursos existentes**: `trabajo.json` no tiene versión; el VideoSpec debe poder construirse desde
  cualquier `trabajo.json` actual sin migrarlo.
