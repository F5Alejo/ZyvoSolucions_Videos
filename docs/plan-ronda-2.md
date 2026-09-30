> **Estado (2026-09-30):** frentes A, B y C hechos en `Alejodev` (ver `bitacora.md`). Las recomendaciones del final siguen abiertas.

# Configuración, plantillas de animación y agentes locales

## Contexto
La Fase 1 del motor ya está en la rama `Alejodev`: cada video se produce por separado y sale como MP4 de 16:9 con voz, subtítulos y control de calidad. La interfaz es Vue 3 y el servidor una API JSON.

El usuario pide tres frentes:
1. **Configuración decente**: faltan opciones básicas, como descargar el curso completo en un solo MP4 y no video por video.
2. **Animaciones como plantillas**: cada plantilla con su estilo, con entradas **y salidas** editables, y un agente gratuito de Ollama que proponga mejoras.
3. **Más agentes** que mejoren lo que produce el estudio.

También pide recomendaciones de lo que falta.

Decisiones del usuario:
- Animación por **plantilla más ajustes por lámina**, con vista previa.
- Desarrollo **en secuencia por frentes**, cada uno con su commit, sus pruebas, su entrada en la bitácora y push a `Alejodev` sin coautoría.

Restricciones que siguen vigentes:
- Solo licencias comerciales (MIT, Apache o BSD).
- El equipo tiene 8 GB de RAM y una GTX 1650 de 4 GB. Por eso los modelos de Ollama van de 2 a 4 B, se descargan de memoria al terminar (`keep_alive: 0`) y **nunca corren al mismo tiempo que un render**: usan la misma cola de `motor/cola.py`.
- Todo lo que propone un agente queda como propuesta que una persona acepta o descarta. Nunca se aplica solo.
- Si Ollama no está, todo sigue funcionando con reglas sin IA.

---

## Frente A — Configuración y descargas

### A1. Configuración global
Nuevo archivo `datos/configuracion.json`, que sí va a git porque no tiene secretos. Lo lee y escribe `app/configuracion.py` con valores por defecto. Opciones:

| Grupo | Opciones |
|---|---|
| Por defecto en cursos nuevos | marca, voz, formatos, plantilla de animación |
| Video | resolución (1080p o 720p), fps (25, 30 o 60), calidad (Borrador rápido: CRF 23 `veryfast` · Final: CRF 18 `medium`), subtítulos quemados (sí o no) |
| Tiempos | entrada antes de la voz (1,0 s), pausa entre frases (0,35 s), respiro final (1,3 s): los que hoy están fijos en `motor/produccion.py` |
| Audio | volumen objetivo (-14 LUFS para YouTube y redes, -16 para podcast, -23 para TV y broadcast), música de fondo (archivo en `datos/musica/` con su licencia y volumen; baja sola cuando habla la voz) |
| Curso completo | tarjeta de título entre videos (sí o no, y su duración), capítulos |
| Agentes | URL de Ollama, modelo de texto y modelo de visión, y activar o desactivar cada agente |

**Diagnóstico** (solo lectura, `GET /api/sistema`):
- ffmpeg, Chromium y las voces instaladas;
- la clave de ElevenLabs (solo si está o no, nunca su valor);
- Ollama y sus modelos;
- espacio en disco.

**Ajustes por curso:** `trabajo["ajustes_video"]` pisa la configuración global solo en lo que cambie. `motor/produccion.py` lee la configuración mezclada en vez de sus constantes.

### A2. Descargar el curso completo
- **«Producir todos»:** `POST /api/trabajos/{id}/producir-todo` pone en la cola los videos que faltan o quedaron desactualizados.
- **MP4 del curso completo:** nuevo módulo `motor/empaquetar.py`.
  - Une los MP4 listos con el *concat* de ffmpeg sin recodificar; todos comparten formato, así que no pierde calidad y tarda segundos.
  - Si la configuración lo pide, agrega una tarjeta de título entre videos.
  - Incrusta capítulos en el MP4 (FFMETADATA) y escribe `capitulos.txt` en formato YouTube (`0:00 Título`).
  - Une también los subtítulos VTT y SRT, corriendo los tiempos de cada video.
  - Si falta algún video o está desactualizado, no arma y dice cuáles.
- **Paquete ZIP del curso:** todos los MP4 (sueltos y el completo), los subtítulos, los informes de calidad, `capitulos.txt`, el banco de preguntas y `manifiesto.json` con el SHA-256 de cada archivo, la marca, la voz y la fecha.
- **Rutas:**
  - `POST /api/trabajos/{id}/completo`: lo arma en la cola.
  - `GET /api/trabajos/{id}/salida/completo/{archivo}`.
  - `GET /api/trabajos/{id}/paquete.zip`: el ZIP se arma sobre la marcha.

### A3. Interfaz
- Vista nueva **`/configuracion`**, con entrada en `BarraLateral.vue`: los grupos de A1 más el diagnóstico con su estado (bien, falta o cómo arreglarlo).
- En **Resultado:**
  - botones «Producir todos», «Descargar curso completo (MP4)» y «Descargar paquete (ZIP)»;
  - resumen del avance: «3 de 5 listos».
- En **Marca y voz**, un bloque «Ajustes de este curso» con los ajustes de A1 que se pueden cambiar por curso.

---

## Frente B — Plantillas de animación

### B1. Modelo de datos
- Cada plantilla es un archivo JSON:
  - `datos/animaciones/<id>.json` para las de fábrica (van a git);
  - `datos/animaciones/propias/` para las que duplica la persona.
- Estructura de una plantilla:
  ```json
  { "id": "dinamica", "nombre": "Dinámica", "descripcion": "…",
    "elementos": {
      "fondo":   {"entrada": {"efecto": "girar", "duracion": 1.2, "retardo": 0, "curva": "suave"},
                  "salida": {"efecto": "aparecer", "duracion": 0.4, "retardo": 0, "curva": "suave"}},
      "titulo":  {...}, "antetitulo": {...}, "linea": {...},
      "vinetas": {"entrada": {..., "escalonado": 0.12}, "salida": {...}},
      "imagen": {...}, "avance": {...}, "logo": {...}
    } }
  ```
- **Efectos** (catálogo fijo en `motor/escenas/efectos.py`, en CSS y deterministas): `ninguno`, `aparecer`, `subir`, `bajar`, `deslizar-izquierda`, `deslizar-derecha`, `escalar`, `desenfoque`, `revelar` (con máscara), `palabra-por-palabra`, `rebote`, `girar`, `maquina` (letra por letra, solo para títulos cortos).
- **Curvas:** `suave`, `energica`, `rebote`, `lineal`.
- **Las 5 plantillas de fábrica:**

  | Plantilla | Estilo | Entrada | Salida |
  |---|---|---|---|
  | **Sobria** | Formación normativa | Aparece con desvanecimiento | Desvanecimiento |
  | **Dinámica** | La actual, mejorada | Sube, con viñetas escalonadas | Baja, con desvanecimiento |
  | **Cinética** | Promocional | Palabra por palabra y escala | Desenfoque |
  | **Corporativa** | Presentación formal | Revelar con máscara | Deslizar |
  | **Mínima** | La más ligera | Solo aparecer | Sin salida |
- **Mezcla de ajustes:** plantilla → ajustes del curso (`trabajo["animacion"]["ajustes"]`) → ajustes de la lámina (`trabajo["animacion"]["laminas"]["5"]`). Cada una puede cambiar solo un efecto, una duración, etc. La mezcla está en `motor/escenas/animacion.py`, con validación de que el efecto existe y de que las duraciones van de 0 a 3 s.

### B2. Render con salidas
- `escena.html` genera los `@keyframes` y las reglas CSS desde la plantilla ya mezclada. Las salidas llevan un retardo igual a la duración de la escena menos la duración de la salida; con `fill-mode: both` el elemento queda visible hasta que empieza a salir.
- `motor/render.py` dibuja cuadro a cuadro **la entrada** (de 0 a E) y **la salida** (de T−S a T), y ffmpeg sostiene el cuadro del medio. El costo sigue siendo bajo: unos 2 s de cuadros por lámina. Se reutiliza `_IR_A`, que ya lleva cada animación a su instante exacto.
- `motor/produccion.py` se asegura de que el respiro final dure al menos lo que dura la salida más 0,3 s, y de que la voz no empiece antes de que el título haya entrado.
- **Revisor de encuadre**, un chequeo sin IA: Playwright mide si algún texto se sale de la pantalla o de su caja, o si quedó con letra menor a 28 px. Se agrega al control de calidad como «Todo el texto cabe», con la lámina donde falla.

### B3. Vista previa y editor (paso nuevo en el curso)
- `GET /api/trabajos/{id}/escena/{n}?formato=16:9` devuelve el HTML de la escena con las animaciones **corriendo en el navegador**, en bucle: entrada, pausa de 1,5 s y salida. Se muestra en un `<iframe>` escalado.
- `CursoView.vue` pasa de 4 a 5 pasos: Presentación · Guion · Marca y voz · **Animación** · Resultado.
- Nuevo componente `PasoAnimacion.vue`:
  - tarjetas de las plantillas, cada una con su vista previa en miniatura;
  - editor por elemento (título, viñetas, imagen, fondo, línea, logo), con pestañas **Entrada** y **Salida** y controles de efecto, duración, retardo, curva y escalonado;
  - selector de lámina: «Todo el curso» o «Solo la lámina 5», que marca las láminas con cambios propios y deja restaurarlas;
  - botones «Guardar como plantilla nueva» (va a `propias/`) y «Sugerir con IA» (agente B4).
- `PATCH /api/trabajos/{id}/animacion`, `GET /api/animaciones` y `POST /api/animaciones` (duplicar o guardar una propia).
- En **Configuración**, la plantilla por defecto y la gestión de las plantillas propias.

### B4. Agente «Director de animación» (Ollama)
- Recibe un resumen de cada lámina (tipo de escena, cuántas viñetas, largo del título, si tiene cifras o imagen) y **elige solo del catálogo**: plantilla y efectos por lámina, con una razón corta.
- Usa `format` con esquema JSON en Ollama; lo que no esté en el catálogo se descarta.
- Sin Ollama usa reglas fijas:
  - cifra → escalar;
  - muchas viñetas → escalonado corto;
  - portada → la entrada más vistosa de la plantilla.
- La propuesta aparece en el editor como cambios por lámina que se aceptan todos juntos o de a uno.

---

## Frente C — Agentes locales

### C1. Base común (`motor/agentes/`)
- **`ollama.py`:** cliente de `/api/chat` con httpx.
  - salida JSON con esquema;
  - `temperature` 0,2;
  - `keep_alive: 0`, para liberar la RAM al terminar;
  - tiempo límite de espera;
  - `disponible()`, que informa si Ollama está encendido y si tiene el modelo.
- **`guardas.py`:** verifica que toda cifra, norma o porcentaje de una propuesta exista en el texto de origen. Reutiliza `extractor.afirmaciones_normativas` y compara también los números sueltos. Si aparece algo inventado, la propuesta se descarta.
- **Registro de agentes y propuestas:**
  - las propuestas se guardan en `trabajo["propuestas"][agente]`, con fecha, modelo y estado (pendiente, aceptada o descartada);
  - los agentes se ejecutan **en la cola de `motor/cola.py`**, uno a la vez y nunca junto a un render.
- **Rutas:**
  - `GET /api/agentes`: estado y modelo de cada agente;
  - `POST /api/trabajos/{id}/agentes/{agente}`: lo ejecuta;
  - `POST /api/trabajos/{id}/propuestas/{agente}/{i}/aceptar` y `/descartar`.
- **Ediciones del curso**, necesarias para poder aceptar propuestas:
  - `trabajo["ediciones"][n] = {"titulo", "vinetas", "notas"}`, sin tocar el original extraído del PPTX;
  - `taller.resumen`, `curso_json` y las escenas usan el texto editado si existe;
  - en el paso **Guion**, un botón «Editar» por lámina con «Volver al original». Así se adelanta lo mínimo de la Fase 2.

### C2. Los agentes

| Agente | Qué hace | Modelo | Dónde aparece |
|---|---|---|---|
| **Redactor de pantalla** | Convierte los párrafos en un título de hasta 8 palabras y 2 a 4 viñetas de hasta 10 palabras. Señala la cifra que conviene destacar | `qwen3:4b` | Guion |
| **Director de animación** | Ver B4 | `qwen3:4b` | Animación |
| **Guionista** | Propone la narración de las láminas sin notas a partir de lo que muestran, y acorta los videos de más de 4 minutos | `qwen3:4b` | Guion |
| **Verificador normativo** | Clasifica cada cita (ley, porcentaje, umbral, dinero), pregunta «¿cuál es la fuente?» y cruza con los pendientes de la marca (p. ej. el umbral del PESV). Nunca inventa fuentes | `qwen3:4b` + reglas | Guion (Revisión) |
| **Evaluador** | 3 a 5 preguntas por video, con la lámina de la que sale cada una, en el formato de `_leer_banco`. Exporta a Moodle XML y GIFT sin IA | `qwen3:4b` | Resultado |
| **Publicador** | Título, descripción de YouTube con capítulos reales, etiquetas y textos para historias. Va dentro del ZIP | `qwen3.5:2b` | Resultado |
| **Descriptor de imágenes** | Distingue contenido de decoración (así no se usa un logo como foto) y escribe el texto alternativo para el LMS | `qwen3.5:2b` (visión) | Presentación |
| **Revisor de voz** | Transcribe el MP4 y lo compara con el guion: palabras omitidas o mal dichas | faster-whisper `small` en int8 (MIT), sin Ollama | Control de calidad |

- `instalar.ps1` suma la opción `-ConAgentes`: `ollama pull qwen3:4b qwen3.5:2b` (unos 5 GB) y `pip install faster-whisper`.
- La página **Configuración** muestra cada agente con su estado y un botón para activarlo o desactivarlo.

---

## Orden de ejecución (en secuencia, un commit por paso)
1. **A1 y A3:** configuración y diagnóstico. Los tiempos y la calidad salen de la configuración.
2. **A2:** producir todos, MP4 completo con capítulos, subtítulos unidos y ZIP con manifiesto.
3. **B1 y B2:** plantillas, mezcla, salidas en el render y revisor de encuadre.
4. **B3:** paso Animación con vista previa y editor.
5. **C1:** base de agentes, guardas, propuestas y ediciones del curso.
6. **B4 y C2:** Director de animación, Redactor, Guionista, Verificador, Evaluador, Publicador, Descriptor y Revisor de voz, cada uno con su commit.
7. Documentación: README, bitácora en cada paso, `docs/plan-motor.md` al día y push.

## Archivos clave
- **Se reutilizan:**
  - `motor/cola.py`, para renders, armado y agentes en la misma cola;
  - `motor/render.py` (`_IR_A` y `cuadros`);
  - `motor/produccion.py`;
  - `motor/escenas/` (`vista`, `estilo`, `html`);
  - `motor/qa.py`;
  - `app/extractor.py` (`afirmaciones_normativas`, `titulo_lamina`);
  - `app/taller.py` (`resumen`, `guardar`, `ajustar`);
  - `app/datos.py`;
  - en el frontend: `api.ts`, `useCarga`, `avisar` y los tipos de `tipos.ts`.
- **Se crean:**
  - `app/configuracion.py` y `datos/configuracion.json`;
  - `motor/empaquetar.py`;
  - `motor/escenas/efectos.py` y `motor/escenas/animacion.py`;
  - `datos/animaciones/*.json`;
  - `motor/agentes/` (`ollama.py`, `guardas.py` y un archivo por agente);
  - `frontend/src/views/ConfiguracionView.vue`;
  - `frontend/src/components/curso/PasoAnimacion.vue`;
  - un editor de lámina en `PasoGuion.vue`;
  - `tests/test_configuracion.py`, `tests/test_animaciones.py` y `tests/test_agentes.py`.

## Verificación
- **pytest:**
  - la configuración se mezcla bien y los tiempos se aplican;
  - el MP4 completo dura la suma de sus partes, con los capítulos correctos y los subtítulos corridos;
  - el ZIP trae el manifiesto con los SHA-256 correctos;
  - las plantillas son válidas y su mezcla funciona;
  - en el render, la salida se ve: el último cuadro está vacío con desvanecimiento y lleno con «ninguno»;
  - el revisor de encuadre detecta un título que no cabe;
  - agentes con Ollama simulado: el esquema se respeta, una cifra inventada se descarta y sin Ollama se usan las reglas;
  - aceptar una propuesta cambia la escena.
- **Vitest:** la mezcla de ajustes en el editor y el formato de capítulos.
- **`npm run typecheck` y `npm run build`.**
- **En vivo** (`uvicorn` en el puerto 8765): con el curso demo, cambiar a la plantilla Cinética, editar la salida de la lámina 2, ver la vista previa, producir todos, descargar el MP4 completo y el ZIP. Con `qwen3:4b` descargado, correr Redactor y Director y aceptar sus propuestas.
- `instalar.ps1 -Probar` sigue pasando.

---

## Recomendaciones de lo que falta después (sin implementar en esta ronda)
1. **Formato 9:16 y cortes para historias** (Fase 3): las plantillas ya lo contemplan; falta el render vertical, los subtítulos quemados y los cortes de 60 s.
2. **Aprobación conectada al panel de Videos:** cuando un video queda listo, crear su registro en `proyectos.json` en «En revisión», y que el paquete de entrega salga solo de lo aprobado.
3. **Miniaturas** de 1280×720 por video.
4. **Exportar al LMS:** SCORM 1.2 con video, subtítulos y preguntas.
5. **Rendimiento:**
   - generar la voz de la siguiente lámina mientras se dibuja la actual;
   - reutilizar escenas que no cambiaron;
   - NVENC de la GTX 1650 para borradores.
6. **Calidad del código:**
   - GitHub Actions que corra pytest, Vitest y la compilación en cada push;
   - pruebas de la interfaz con Playwright;
   - migrar `lucide-vue-next` (obsoleto) a `@lucide/vue`;
   - quitar el aviso de `httpx` en las pruebas.
7. **Operación:**
   - usuarios e inicio de sesión si el estudio se comparte fuera del equipo;
   - copia de seguridad de `datos/`;
   - registro de errores en archivo.
8. **Pendientes de negocio:**
   - rotar la clave de ElevenLabs;
   - confirmar cómo se dice PESV;
   - decidir entre Dubai y Montserrat;
   - revisar con el cliente el módulo PESV M01, narrado con Piper, cuya base no permite uso comercial.
