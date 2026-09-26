# Paso a paso — del contexto a la materialización

> **Para qué sirve.** Es la ruta ordenada para llegar a construir el motor y la
> plataforma **con el contexto completo antes de escribir código nuevo**. Cada paso dice
> qué se busca, qué hace falta, qué se entrega y cuándo se da por terminado.
>
> **Cómo se usa.** Se avanza en orden; un paso puede empezar antes de que termine el
> anterior, pero **no se da por hecho** hasta cumplir su criterio. Al cerrar un paso se
> actualiza su estado y la fecha, y lo que se decidió va a `PLATAFORMA.md` §8.
>
> **Fuera de alcance por ahora (D-03):** modelo de negocio y a qué clientes nuevos se les
> venderá. El foco son las cuatro marcas actuales: **SOFU, RiskMann, FEGIR y Dr. Yezid Ricaurte**.
>
> Estados: `pendiente` · `en curso` · `hecho`.

---

## Etapa 1 — Contexto (qué es cada marca y qué hay)

### Paso 1.1 · Fichas de marca completas — `en curso`

- **Objetivo:** que cualquiera (persona o agente) pueda producir para una marca leyendo
  solo su ficha.
- **Hace falta:** manuales, webs, guiones, correos y logos de cada marca.
- **Entrega:** `docs/contexto/marcas/{sofu,riskmann,fegir,yezid-ricaurte}.md` con la
  plantilla `_PLANTILLA.md`.
- **Hecho cuando:** las cuatro fichas tienen todas sus secciones llenas y cada dato con
  fuente; los **⚠ por confirmar** tienen dueño y fecha.
- **Estado 2026-09-26:** las cuatro creadas con lo que había en el repo. SOFU y FEGIR son
  las más incompletas: no hay manual de marca de ninguna de las dos en el repositorio.

### Paso 1.2 · Ecosistema y glosario — `en curso`

- **Objetivo:** entender cómo se cruzan las marcas y hablar con las mismas palabras.
- **Entrega:** `docs/contexto/ECOSISTEMA.md` y `docs/contexto/GLOSARIO.md`.
- **Hecho cuando:** las cuatro preguntas de ECOSISTEMA §4 tienen respuesta.

### Paso 1.3 · Material de los clientes dentro del repo — `pendiente`

- **Objetivo:** que ninguna fuente viva solo en Drive, en un correo o en la cabeza de alguien.
- **Entrega:** carpeta `docs/fuentes/<marca>/` con manuales, guiones, briefs y capturas
  fechadas de las landings. Lo que tenga datos personales se queda fuera, con una nota
  que diga dónde está.
- **Hecho cuando:** cada fila de «Fuentes oficiales» de las fichas apunta a un archivo del
  repositorio o a una URL con fecha de lectura.
- **Hoy falta:** guion original y manual de SOFU; manual y brief de FEGIR; storyboard de
  inspecciones de RiskMann; videos del Drive del Dr. Yezid.

### Paso 1.4 · Inventario de lo producido con su estado — `pendiente`

- **Objetivo:** saber de cada una de las 61 carpetas de `videos/` qué es, de qué marca y
  en qué estado está.
- **Entrega:** `docs/contexto/INVENTARIO.md` (una fila por proyecto: marca, familia A/B,
  motor, estado, dónde está el final) y el campo `estado` en cada `meta.json`.
- **Hecho cuando:** ninguna carpeta queda sin estado, y la campaña de Yezid dice cuál de
  sus cinco variantes se aprobó.

---

## Etapa 2 — Estándares (cómo se hace, igual para todos)

### Paso 2.1 · Marca como datos — `pendiente`

- **Objetivo:** que la identidad de cada marca se lea de un archivo, no de copias.
- **Entrega:** `marcas/<marca>.json` (paleta, tipografías con su licencia, logos, voz, CTA,
  prohibiciones), generado desde la ficha.
- **Hecho cuando:** un proyecto nuevo toma su identidad de ahí sin copiar valores a mano.
- **Depende de:** 1.1 y 1.3.

### Paso 2.2 · La regla de la fuente, aplicable — `pendiente`

- **Objetivo:** que cada frase de un guion diga de dónde sale.
- **Entrega:** esquema del campo `fuente: {archivo, pagina|lamina|url, cita}` para
  `curso.json` y `narracion.json`, documentado con un ejemplo por marca.
- **Hecho cuando:** el esquema está escrito y probado en un proyecto de cada familia.

### Paso 2.3 · Licencias y datos — `pendiente`

- **Objetivo:** no entregar nada que el cliente no pueda usar, ni guardar lo que no se debe.
- **Entrega:** `docs/LICENCIAS-Y-DATOS.md` + ficha `*-LICENCIA.txt` junto a cada recurso
  de terceros.
- **Hecho cuando:** Segoe UI resuelta; toda la música, fotos y fuentes con ficha; política
  escrita sobre los correos con datos personales.

### Paso 2.4 · Estados y aprobaciones — `pendiente`

- **Objetivo:** que siempre se sepa qué está aprobado y por quién.
- **Entrega:** convención `estado` / `aprobado_por` / `aprobado_el` en `meta.json` y quién
  aprueba en cada marca (en su ficha).
- **Hecho cuando:** el inventario (1.4) se puede generar leyendo los `meta.json`.

---

## Etapa 3 — Consolidación técnica (la fase 0 de `PLATAFORMA.md`)

Se empieza cuando las etapas 1 y 2 están **en curso** con lo esencial resuelto
(las fichas completas y la regla de la fuente definida).

| Paso | Qué | Criterio |
| --- | --- | --- |
| 3.1 | Extractor PPTX → `curso.json` | Regenera el de csm idéntico |
| 3.2 | `moto.py` + `csm.py` → `tools/curso/` | Los dos cursos se construyen con el mismo código |
| 3.3 | Las variantes de `audio.py` → `tools/` | Las mezclas salen igual (< 1 dB) |
| 3.4 | Portar un lienzo propio a HyperFrames | Render equivalente, o una lista de lo que no se puede |
| 3.5 | Validación de la fuente en el constructor | Falla si una frase no la tiene |

---

## Etapa 4 — Materialización

Motor por CLI → uso interno medido → piloto con un tercero → API → interfaz
(`PLATAFORMA.md` §5, fases 1 a 5). Se detalla cuando se cierre la etapa 3.

---

## Registro de avance

| Fecha | Paso | Qué se hizo | Quién |
| --- | --- | --- | --- |
| 2026-09-26 | 1.1, 1.2 | Creadas las fichas de las cuatro marcas, la plantilla, el ecosistema y el glosario | Equipo `fegir` (con Claude) |
