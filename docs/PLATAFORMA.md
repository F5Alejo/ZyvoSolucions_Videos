# Hacia la plataforma — ideas, contraste y decisiones

> **Qué es esto.** El documento vivo donde se discute en qué se puede convertir este
> repositorio: de «colección de proyectos que producen videos» a «motor que produce
> videos a partir de contenido y configuración». No describe lo que ya existe —eso es
> el [`PLAYBOOK.md`](PLAYBOOK.md)—, sino hacia dónde ir, con qué pruebas y qué se decidió.
>
> **Cómo se usa.** Cada idea nueva entra en el [registro de ideas](#7-registro-de-ideas)
> con su origen y su estado (`propuesta` → `en prueba` → `aceptada` / `descartada`).
> Cuando el equipo decide algo, va al [registro de decisiones](#8-registro-de-decisiones)
> con la fecha y el porqué. Nada se borra: una idea descartada con su motivo evita
> volver a discutirla.
>
> **Primera versión:** 26-sep-2026. Parte de un análisis externo (una conversación con
> otro asistente sobre el playbook) contrastado con mediciones del repositorio ese día.

---

## 1. Punto de partida medido (26-sep-2026)

Datos del repositorio, no impresiones:

| Hecho | Valor | Dónde se ve |
| --- | --- | --- |
| Proyectos de video | 58 carpetas en `videos/` | `ls videos` |
| Personas que hacen commit | 2 principales (Juan, Alejandro, ~40 commits cada uno) + trabajo local de `fegir` que no se había subido hasta el 26-sep | `git log` |
| Motores de render en uso | 2: HyperFrames y «lienzo propio» (HTML + GSAP + Three.js + puppeteer) | PLAYBOOK §6.1 |
| `render.mjs` copiado | **6 copias, las 6 distintas entre sí** (405 líneas en total) | `videos/*/tools/render.mjs` |
| `audio.py` copiado | **5 copias, 4 variantes** (~2 000 líneas en total) | `videos/*/tools/audio.py` |
| `moto.py` frente a `csm.py` | 358 y 356 líneas; solo ~66 líneas difieren (≈ 90 % común). `sincronia.py`, idéntico | `videos/{moto,csm}-curso/tools/` |
| Extractor PPTX → `curso.json` | **No está en ninguna rama** (ni local ni en GitHub) | búsqueda de `pptx` en todas las ramas |
| Regla «cada frase cita su fuente» | Escrita en PLAYBOOK §3.1, pero **solo 1 proyecto** (`pesv-m01-mando/tools/guion.json`) tiene campo `fuente`; `csm-curso/datos/curso.json` no lo tiene | `grep '"fuente"'` |
| Estado de aprobación de una pieza | No existe: los `meta.json` solo tienen `id` y `name` | `videos/*/meta.json` |
| Formatos productivos | Cursos generados (moto, csm), curso lámina a lámina, módulos PESV, comerciales, verticales para redes, campañas de variantes | PLAYBOOK §1 |

**Lectura:** la capacidad existe y está probada; la fragmentación también, y es medible.
Las copias de `render.mjs` y `audio.py` ya **divergieron**: no son duplicados que se
puedan borrar, son bifurcaciones que hay que reconciliar.

---

## 2. Lo que el análisis externo acierta

Se conserva, porque los datos lo respaldan:

1. **El diagnóstico de fondo.** El repositorio está en la transición entre «scripts que
   funcionan» y «motor parametrizable». El salto moto/csm (88 láminas → 15 videos con
   un comando por módulo) prueba que el concepto funciona.
2. **Separar motor y contenido.** La práctica «configuración, no código» (PLAYBOOK §3.5)
   ya apunta ahí; falta llevarla a todo el repositorio.
3. **Consolidar antes de construir encima.** Unificar moto/csm, sacar `render.mjs` y
   `audio.py` a `tools/`, recuperar el extractor PPTX. Coincide con PLAYBOOK §9.
4. **Versionado y aprobación desde el principio.** La campaña de Yezid tiene cinco
   variantes y nadie puede decir hoy cuál se aprobó.
5. **La marca como entidad.** «¿De quién es el video?» (PLAYBOOK §3.9) merece un archivo
   formal por marca, no valores repartidos en `frame.md`, `base.py` y `config.js`.
6. **IA para planificar, motor determinista para ejecutar.** Es lo que ya se hace en los
   cursos generados y es lo que hace confiable el resultado.
7. **Primero la muestra, después la producción** como paso obligatorio del flujo.

---

## 3. Dónde hay que matizarlo o corregirlo

### 3.1 Son dos negocios, no uno

El análisis trata todo como una sola «fábrica de video». Los datos muestran dos familias
con economías opuestas:

| | **A. Cursos generados** | **B. Piezas de marketing a medida** |
| --- | --- | --- |
| Ejemplos | moto, csm, ruta-segura, PESV M01 | consulta PESV, En Vivo, campañas, landings, SOFU |
| Entrada | PPTX/PDF con estructura repetida | Brief, landing, manual de marca |
| Valor | Volumen: 15 videos por curso | Diseño: cada pieza es distinta |
| ¿Se puede plantillar? | **Sí** (6–7 plantillas cubren 88 láminas) | **Poco:** cada pieza inventa movimiento y composición |
| Quién compone hoy | Un generador en Python | Un agente escribiendo HTML/GSAP con skills |
| Forma de escalar | Plataforma: subir PPTX → elegir marca → generar | Kit por marca + bloques del registro + recetas + agente |

**Consecuencia:** el asistente paso a paso con «subir PPTX, elegir marca, generar» tiene
sentido para **A**. Para **B**, un asistente web no sustituye la dirección creativa; lo
que escala es darle al agente mejores piezas de partida (kit de marca, bloques, recetas,
trampas conocidas). Construir una sola plataforma para las dos cosas es el error caro.

### 3.2 No reconstruir la infraestructura de render

El análisis propone un servicio de render propio con renderizador HTML, cola y
servidores de trabajo. HyperFrames ya trae buena parte de eso:

- CLI con `lint`, `check`, `snapshot` y `render`, que ya se usa aquí.
- **Render en la nube:** hospedado por HeyGen, AWS Lambda o Google Cloud Run
  (skill `hyperframes-cli`).
- **Adaptador de Three.js** y otros seis motores de animación (skill `hyperframes-animation`).
- **Registro de ~400 bloques** que no dependen de la búsqueda por tiempo (skill `hyperframes-registry`).

**Consecuencia:** antes de escribir un «HTML renderer» propio, hay que medir si las
piezas de lienzo propio se pueden portar a HyperFrames con su adaptador de Three.js.
Si se puede, desaparecen las 6 copias de `render.mjs` y queda **un solo motor**
con verificador. Si no se puede, hay que escribir qué es lo que no cabe.

### 3.3 Un formato intermedio por familia, no uno universal

El `video.json` universal es atractivo, pero diseñarlo antes de tiempo congela
decisiones que todavía no se entienden:

- **Familia A** ya tiene formato intermedio: `curso.json` (láminas → formas → notas →
  frases). Lo que falta es **formalizarlo** (esquema validable) y recuperar quien lo produce.
- **Familia B** tiene su especificación en el propio HTML compuesto, más `narracion.json`,
  `SFX-CUES.md` y `mezcla-*.json`. Lo que se puede estandarizar ya son **esos tres
  archivos de configuración**, no la composición.

Primero dos esquemas que funcionen; la unificación, si hace falta, después.

### 3.4 La trazabilidad de fuentes es el P0 que falta, y el diferenciador

El análisis la menciona como una validación más. Para este repositorio es **la regla que
manda** (`CLAUDE.md`) y hoy casi no está implementada (§1). En contenido normativo (PESV,
Resolución 20223040040595, umbrales de vehículos) una cifra sin fuente es un riesgo
legal para el cliente, no un defecto estético. El caso del umbral «11 o 10 vehículos»
(PLAYBOOK §9) lo demuestra.

**Propuesta:** que cada frase de `curso.json` y `narracion.json` lleve
`fuente: {archivo, pagina|lamina|url, cita}` y que el motor **se niegue a construir**
si falta. Eso es algo que un editor de video genérico no ofrece.

### 3.5 La «capa de IA» ya existe: es el agente

El análisis deja la IA para la fase 5. En la práctica, Claude Code con las skills de
HyperFrames ya es la capa que planifica y compone: produjo todas las piezas de la
familia B. La pregunta no es cómo añadir IA, sino **qué parte del trabajo del agente se
convierte en motor determinista**. Criterio: todo lo que se repite tres veces igual
(render, mezcla, nivelado de voz, medición de tiempos muertos) pasa al motor; lo que se
decide distinto cada vez se queda en el agente.

### 3.6 La web app y el multiempresa van después, pero ya están en el plan

Somos 2–3 personas y ~4 marcas (RiskMann, SOFU, Yezid Ricaurte, FEGIR). Usuarios,
roles, organizaciones, PostgreSQL, colas y almacenamiento cuestan meses y no resuelven
ninguno de los problemas medidos en §1.

Desde **D-02** (se ofrece para uso interno **y** a terceros) ya no son opcionales: son el
destino. Lo que no cambia es el orden: motor por CLI → uso interno medido → piloto con
un tercero como servicio asistido → API → interfaz. Vender una interfaz sobre un motor
que todavía tiene seis `render.mjs` distintos multiplica los problemas por cliente.

### 3.7 Riesgos que el análisis no menciona

| Riesgo | Hecho | Qué hacer |
| --- | --- | --- |
| Dependencia de ElevenLabs | La clave del issue #3 caducó el 21-sep; las locuciones no van en git | Guardar las locuciones aprobadas fuera de git con respaldo; abstracción de proveedor de voz (Piper como alternativa ya existe) |
| Licencias | Segoe UI (Microsoft) en el repo; música con licencias distintas por plataforma | Ficha de licencia obligatoria por cada recurso (`*-LICENCIA.txt` ya existe en 2 proyectos) y el motor que la exija |
| Datos personales | `Documentos_contexto/` con correos reales fuera del repo | Política escrita de qué entra al repo y qué no, antes de tener más clientes |
| Pérdida de trabajo | OneDrive borró y revirtió el repo; el trabajo de `fegir` estuvo días sin subir | Commit y push antes de renderizar (PLAYBOOK §3.8); rama por persona y unión frecuente |
| Costo de render | Máquinas de 8 GB; render por partes | Medir minutos de render por minuto de video antes de dimensionar la nube |
| Historias reescritas | La rama de Juan se reescribió y dejó copias viejas en otras ramas (70 conflictos el 26-sep) | No reescribir ramas compartidas; unir con `merge` |

### 3.8 Una hipótesis de producto más concreta

El análisis habla de un «video factory» genérico. Los datos apuntan a algo más acotado:
los cursos (moto, csm, ruta-segura) se entregaron **junto con banco de preguntas para la
plataforma** («video informativo del quiz de la plataforma»). Eso sugiere:

> **PPTX de capacitación → videos por módulo + banco de preguntas trazado a la fuente,
> listos para cargar en RiskMann Campus.**

Es una hipótesis, no una decisión: hay que confirmar con RiskMann/SOFU si ese es el
flujo que compran y cuánto vale (ver §6).

### 3.9 Qué cambia al ofrecerlo a terceros (D-02)

Para uso interno basta con que el motor funcione en nuestras máquinas. Para vendérselo a
otros hace falta además:

| Requisito | Por qué | Desde |
| --- | --- | --- |
| **La regla de la fuente, generalizada** | Hoy dice «un archivo que entregó RiskMann»; con terceros es «un archivo que entregó **el cliente**», y hay que guardar qué entregó y cuándo | Fase 0 (tarea 0.5) |
| **Licencias transferibles** | Lo que se entrega (música, fuentes, fotos, voz) tiene que poder usarlo el cliente en sus canales. Segoe UI o la Biblioteca de Audio de YouTube no sirven | Fase 0 (tarea 0.8) |
| **Aislamiento por cliente** | Marcas, archivos fuente y locuciones de un cliente no pueden aparecer en la pieza de otro. Hoy todo convive en un repositorio y en `assets/` compartido | Fase 3 (piloto): carpeta o repositorio por cliente; fase 5: organizaciones |
| **Datos personales** | Los correos de campaña ya traen datos reales (`Documentos_contexto/`). Con terceros hace falta una política escrita y acuerdos de tratamiento | Fase 0 (tarea 0.8) |
| **Propiedad del resultado** | Quién es dueño de las composiciones, las plantillas y las locuciones. Las plantillas son el activo: se licencian, no se ceden | Antes del primer contrato externo |
| **Costo por video conocido** | Sin horas, costo de voz y minutos de render por minuto de video no hay precio | Fase 2 |
| **Voz con cuenta propia del servicio** | Una clave personal que caduca (issue #3) no sostiene un servicio para terceros | Fase 2 |
| **Verificación como garantía** | Lo que hoy es control interno (fuentes, contraste, audio por bandas) se convierte en lo que se le promete al cliente: un informe de verificación con cada entrega | Fase 1 |

**Las dos ofertas usan el mismo motor.** Lo que cambia es quién lo opera: dentro, el
equipo con el agente; fuera, primero el equipo **para** el cliente (servicio asistido) y
solo después el cliente directamente (autoservicio, familia A).

---

## 4. Arquitectura objetivo (revisada)

```
                   ┌──────────────── marcas/ ────────────────┐
                   │ riskmann.json · yezid.json · fegir.json │  (paleta, fuentes, logo,
                   └────────────────────┬────────────────────┘   CTA, voz, reglas)
                                        │
 Familia A (cursos)                     │                 Familia B (marketing)
 PPTX/PDF ──extractor──▶ curso.json ────┤                 brief + landing + manual
            (con fuentes)   │           │                        │
                            ▼           ▼                        ▼
                     plantillas del curso               agente + skills + bloques
                            │                                    │
                            └────────────┬───────────────────────┘
                                         ▼
                           composición HyperFrames (un solo motor)
                                         │
      motor común (tools/): voz · nivelar · mezcla · sincronía · render · verificación
                                         │
                 verificación: lint/check · fuentes · licencias · audio por bandas
                                · tiempos muertos · contraste
                                         │
                      estado en meta.json: borrador → revisión → aprobado → final
```

---

## 5. Hoja de ruta con criterios de salida

Cada fase termina cuando se cumple su criterio, no en una fecha.

### Fase 0 — Consolidar (ahora)

| # | Tarea | Criterio de salida |
| --- | --- | --- |
| 0.1 | Recuperar o reescribir el extractor PPTX → `curso.json` (`python-pptx`) | Regenera el `curso.json` de csm **idéntico** al actual desde su PPTX |
| 0.2 | Sacar lo común de `moto.py`/`csm.py` a `tools/curso/` | moto y csm se construyen con el mismo código; cada curso solo aporta `LIMITES`, `base.py`, `plantillas.py` |
| 0.3 | Reconciliar las 4 variantes de `audio.py` en `tools/` | Las 5 piezas vuelven a producir su mezcla con el script común; diferencias medidas < 1 dB |
| 0.4 | Probar un lienzo propio en HyperFrames (p. ej. `yezid-envivo-premium`) | Render equivalente sin `render.mjs`, o una lista escrita de lo que no se puede |
| 0.5 | Campo `fuente` obligatorio en `curso.json` y `narracion.json` | El constructor falla si una frase no tiene fuente |
| 0.6 | `estado` en `meta.json` (`borrador/revision/aprobado/final/archivado`) + quién y cuándo | Cada carpeta de `videos/` tiene estado; la campaña de Yezid dice cuál se aprobó |
| 0.7 | `marcas/<marca>.json` para RiskMann, Yezid y FEGIR | Un proyecto nuevo toma paleta, fuentes y logo de ahí, no de copias |
| 0.8 | Política de licencias y datos: qué recursos se pueden entregar a un tercero y qué datos entran al repositorio | Documento escrito; ficha de licencia en cada recurso de `assets/`; Segoe UI reemplazada o con licencia confirmada |

### Fase 1 — Motor por CLI

Un comando por familia: `video curso build <curso.json> --marca riskmann` y
`video pieza mezcla|render|verificar <proyecto>`.
**Criterio:** alguien que no escribió el código produce un curso nuevo de punta a punta
desde un PPTX sin editar Python.

### Fase 2 — Uso interno medido

Producir 2–3 encargos reales con el motor y anotar horas, costo de voz y minutos de
render por minuto de video. Cuenta de voz del servicio, no personal.
**Criterio:** números que permitan poner precio a las dos ofertas.

### Fase 3 — Piloto con un tercero (servicio asistido)

Un cliente externo entrega su PPTX o su brief; el equipo produce con el motor y entrega
videos + informe de verificación. Cliente en su propia carpeta o repositorio.
**Criterio:** entrega aprobada por el cliente, costo real dentro del precio, ningún
recurso sin licencia transferible y ningún archivo de otro cliente en la pieza.

### Fase 4 — API y cola

Endpoints sobre el motor y render en la nube de HyperFrames antes que servidores propios.
**Criterio:** un encargo de la familia A corre de punta a punta sin que nadie ejecute
comandos a mano.

### Fase 5 — Interfaz y multiempresa para la familia A

Organizaciones, usuarios y roles; asistente paso a paso: PPTX → marca → voz → muestra de
15 s → aprobar → curso completo en 16:9 y 9:16. La familia B se sigue ofreciendo como
servicio asistido. **Criterio:** un cliente externo lo usa sin ayuda.

---

## 6. Preguntas abiertas para el equipo

1. ~~¿El producto es para **uso interno** o para **vender a terceros**?~~ **Resuelta en
   D-02: las dos.** Se abren estas otras:
   - *Aparcadas por D-03:* ¿quién será el primer tercero del piloto?, ¿se vende por
     video, curso, suscripción o minuto?, ¿bajo qué nombre se ofrece?
2. ¿RiskMann Campus es el destino principal de los cursos? ¿Qué formato de preguntas acepta?
3. ¿Quién aprueba una pieza en cada marca, y cómo se registra hoy esa aprobación?
4. ¿Se acepta depender de ElevenLabs, o la voz local (Piper) debe ser una alternativa
   de producción real?
5. ¿Las piezas de lienzo propio se pueden portar a HyperFrames? Lo responde la tarea 0.4.
6. ¿Dónde viven los renders finales y las locuciones aprobadas (Drive, almacenamiento en
   la nube)? Hoy dependen de carpetas locales.

---

## 7. Registro de ideas

| # | Idea | Origen | Estado | Fecha | Nota |
| --- | --- | --- | --- | --- | --- |
| I-01 | Separar motor (agnóstico de cliente) y plataforma (usuarios, proyectos) | Análisis externo | aceptada | 2026-09-26 | Aceptada con D-02; la plataforma llega en las fases 4–5 (§3.6) |
| I-02 | Formato intermedio universal `video.json` | Análisis externo | propuesta | 2026-09-26 | Se sustituye por un esquema por familia (§3.3) |
| I-03 | Arquitectura en 4 capas: core / plantillas / proyectos / orquestador | Análisis externo | propuesta | 2026-09-26 | Coincide con la fase 0–1 |
| I-04 | Estados de aprobación y versionado por pieza | Análisis externo | propuesta | 2026-09-26 | Se empieza ya con `meta.json` (tarea 0.6) |
| I-05 | Marca como entidad (`brand.json`) | Análisis externo | propuesta | 2026-09-26 | Tarea 0.7 |
| I-06 | Servicio de render propio con cola y servidores de trabajo | Análisis externo | propuesta | 2026-09-26 | Antes, evaluar el render en la nube de HyperFrames (§3.2) |
| I-07 | Asistente web: PPTX → marca → voz → muestra → curso | Análisis externo | aceptada | 2026-09-26 | Con D-02; solo para la familia A, fase 5 (§3.1) |
| I-08 | IA que estructura, motor determinista que ejecuta | Análisis externo | aceptada | 2026-09-26 | Ya es la práctica de los cursos generados |
| I-09 | Dos familias de producto con estrategias distintas | Contraste con el repo | propuesta | 2026-09-26 | §3.1 |
| I-10 | Un solo motor: portar el lienzo propio a HyperFrames | Contraste con el repo | propuesta | 2026-09-26 | Tarea 0.4 |
| I-11 | Fuente obligatoria por frase, validada por el motor | Contraste con el repo | propuesta | 2026-09-26 | Tarea 0.5; diferenciador en contenido normativo |
| I-12 | Producto: PPTX → cursos + banco de preguntas para RiskMann Campus | Contraste con el repo | propuesta | 2026-09-26 | Hipótesis a validar (§3.8, pregunta 2) |
| I-13 | Ficha de licencia obligatoria por recurso | Contraste con el repo | aceptada | 2026-09-26 | Con D-02 pasa a obligatoria: tarea 0.8 |
| I-14 | Servicio asistido con un tercero antes que autoservicio | Consecuencia de D-02 | propuesta | 2026-09-26 | Fase 3 (§3.9) |
| I-15 | Aislamiento por cliente (carpeta o repositorio, luego organizaciones) | Consecuencia de D-02 | propuesta | 2026-09-26 | §3.9 |
| I-16 | Informe de verificación entregado con cada video | Consecuencia de D-02 | propuesta | 2026-09-26 | La verificación interna se convierte en garantía para el cliente |

---

## 8. Registro de decisiones

| # | Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- | --- |
| D-01 | 2026-09-26 | Documentar la visión de plataforma en este archivo, separada del playbook | El playbook describe lo que existe; este documento, lo que se propone | — |
| D-02 | 2026-09-26 | Se mantienen **las dos ofertas**: uso interno y venta a terceros | Decisión del equipo `fegir`. Consecuencias en §3.9: licencias, datos, aislamiento por cliente y costo por video pasan a ser requisitos; se añade un piloto con un tercero (fase 3) antes de la API | Equipo `fegir` |
| D-03 | 2026-09-26 | **Modelo de negocio y clientes nuevos, aparcados.** Primero, documentación y contexto muy específicos de las cuatro marcas actuales (SOFU, RiskMann, FEGIR, Dr. Yezid) y una ruta paso a paso antes de materializar | Construir sobre contexto completo, no sobre supuestos. La ruta está en [`PASO-A-PASO.md`](PASO-A-PASO.md) y el contexto en [`marcas/`](marcas/) | Equipo `fegir` |
| D-04 | 2026-09-28 | **Un documento maestro generado** (`docs/MAESTRO.md`, con `python tools/maestro.py`) y el material de cada marca en `docs/marcas/<marca>/` | Leerlo todo en un solo archivo sin perder los documentos fuente: cada uno se sigue editando por separado, no se rompen enlaces ni las ramas de otros. El manual de FEGIR estaba dentro de la carpeta de RiskMann | Equipo `fegir` |
