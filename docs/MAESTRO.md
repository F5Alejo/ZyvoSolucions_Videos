# Documento maestro — riskmann2-marketing-videos

> **Archivo generado. No se edita a mano.** Reúne en un solo lugar la documentación
> general del repositorio. Para cambiar algo, edita el documento fuente que aparece al
> inicio de cada capítulo y reconstruye con `python tools/maestro.py`.
> Los documentos propios de cada video (`videos/<proyecto>/*.md`) no están aquí.

## Índice

- [0. Cómo usar esta documentación](#cap-0)
- [1. Paso a paso](#cap-1)
- [2. Ecosistema de marcas](#cap-2)
- [3. Fichas de marca](#cap-3)
  - [3.1. SOFU BIC S.A.S.](#cap-3-1)
  - [3.2. RiskMann](#cap-3-2)
  - [3.3. FEGIR](#cap-3-3)
  - [3.4. Dr. Yezid Ricaurte](#cap-3-4)
- [4. Glosario](#cap-4)
- [5. Playbook](#cap-5)
- [6. Estándar de producción](#cap-6)
- [7. Guía de prompts](#cap-7)
- [8. Arranque en otro equipo](#cap-8)
- [9. Plataforma: ideas y decisiones](#cap-9)
- [10. Anexos](#cap-10)
  - [10.1. Bitácora del 17 y 18 de septiembre](#cap-10-1)
  - [10.2. PoC Seguridad Vial para Pasajeros](#cap-10-2)
  - [10.3. Lectura del manual de RiskMann](#cap-10-3)
  - [10.4. README del repositorio](#cap-10-4)
  - [10.5. Instrucciones para agentes (CLAUDE.md)](#cap-10-5)

---

<a id="cap-0"></a>

## 0. Cómo usar esta documentación

> Fuente: [`docs/README.md`](README.md) — se edita ahí, no aquí.

> Índice de todo lo escrito sobre el repositorio. Se lee en el orden de la tabla.
>
> **¿Lo quieres todo junto?** [`MAESTRO.md`](MAESTRO.md) reúne estos documentos en un solo
> archivo con índice. Es **generado**: no se edita; se editan los documentos de abajo y se
> reconstruye con `python tools/maestro.py`.

### Mapa de lectura

| # | Documento | Qué responde | Cuándo leerlo |
| --- | --- | --- | --- |
| 1 | [`PASO-A-PASO.md`](#cap-1) | ¿En qué punto estamos y qué sigue? | Siempre primero |
| 2 | [`marcas/ECOSISTEMA.md`](#cap-2) | ¿Quiénes son SOFU, RiskMann, FEGIR y el Dr. Yezid, y cómo se cruzan? | Antes de producir para cualquiera |
| 3 | [`marcas/<marca>/ficha.md`](marcas/) | Todo lo de una marca: fuentes, identidad, voz, CTA, lo producido, pendientes | Antes de producir para esa marca |
| 4 | [`marcas/GLOSARIO.md`](#cap-4) | ¿Qué significa PESV, lienzo propio, ducking…? | Cuando aparezca una palabra dudosa |
| 5 | [`PLAYBOOK.md`](#cap-5) | ¿Qué formato elijo, qué copio y en qué orden trabajo? | Al arrancar un proyecto |
| 6 | [`../PRODUCCION-VIDEOS.md`](#cap-6) | Valores y reglas exactas de cada formato | Al construir |
| 7 | [`../GUIA-PROMPTS.md`](#cap-7) | ¿Qué le pido al agente para conseguir cada cosa? | Al pedir un video |
| 8 | [`ARRANQUE-EN-OTRO-EQUIPO.md`](#cap-8) | Qué instalar y qué errores ya se pagaron | En un equipo nuevo o ante un error raro |
| 9 | [`PLATAFORMA.md`](#cap-9) | Hacia dónde evoluciona esto; registro de ideas y decisiones | Al proponer o decidir algo |
| 10 | [`BITACORA-2026-09-17-18.md`](#cap-10-1) | Qué se decidió en las piezas verticales de RiskMann y Yezid | Referencia |
| 11 | [`POC-SEGURIDAD-VIAL-PASAJEROS.md`](#cap-10-2) | Qué se entregó en el PoC | Referencia |

### Cómo están organizadas las carpetas

```
docs/
├── MAESTRO.md                 ← todo junto (generado)
├── README.md                  ← este índice
├── PASO-A-PASO.md · PLAYBOOK.md · PLATAFORMA.md · ARRANQUE-EN-OTRO-EQUIPO.md
├── BITACORA-2026-09-17-18.md · POC-SEGURIDAD-VIAL-PASAJEROS.md
└── marcas/                    ← todo lo de cada marca, en su carpeta
    ├── ECOSISTEMA.md · GLOSARIO.md · _PLANTILLA.md
    ├── sofu/            ficha.md
    ├── riskmann/        ficha.md · LEEME.md (lectura del manual) · manual-identidad*.pdf
    │                    fuentes/manejo-pesv-24-pasos.pdf
    ├── fegir/           ficha.md · manual-identidad-fegir.pdf · web-fegir-captura.pdf
    │                    logos-extraidos/
    └── yezid-ricaurte/  ficha.md · manual-yezid-ricaurte.pdf
```

### Cómo alimentar la documentación

| Llega… | Va a… |
| --- | --- |
| Un manual o material de identidad de una marca | `docs/marcas/<marca>/` + una fila en «Fuentes oficiales» de su ficha |
| Un guion, brief o PDF de contenido de un cliente | `docs/marcas/<marca>/fuentes/` + una fila en «Fuentes oficiales» de su ficha |
| Un dato de una marca (color, CTA, lema, contacto) | Su ficha, **con la fuente**; si no la tiene, a «⚠ por confirmar» |
| Una decisión del cliente | «Decisiones tomadas» de su ficha, con fecha |
| Un término nuevo | `marcas/GLOSARIO.md` |
| Una idea para el motor o la plataforma | `PLATAFORMA.md` §7 (registro de ideas) |
| Una decisión del equipo | `PLATAFORMA.md` §8 (registro de decisiones) |
| Un error que costó tiempo | `ARRANQUE-EN-OTRO-EQUIPO.md` §2 y, si es de los grandes, PLAYBOOK §8 |
| Un paso terminado | Su estado en `PASO-A-PASO.md` y una fila en su registro de avance |
| Una marca nueva | Crear `marcas/<marca>/` con `ficha.md` copiada de `marcas/_PLANTILLA.md`, añadirla a `ECOSISTEMA.md` y a `CAPITULOS` en `tools/maestro.py` |
| Un documento general nuevo | Añadirlo a esta tabla y a `CAPITULOS` en `tools/maestro.py` |

**Después de cualquier cambio:** `python tools/maestro.py` para que el maestro quede al día
(`python tools/maestro.py --verificar` dice si está desactualizado).

**Tres reglas:**

1. Todo dato lleva su fuente, o se marca **⚠ por confirmar**.
2. No se borra lo que cambió: se actualiza y se anota en el historial de la ficha.
3. Datos personales (correos, teléfonos de personas) **no** entran al repositorio.

---

<a id="cap-1"></a>

## 1. Paso a paso

> Fuente: [`docs/PASO-A-PASO.md`](PASO-A-PASO.md) — se edita ahí, no aquí.

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

### Etapa 1 — Contexto (qué es cada marca y qué hay)

#### Paso 1.1 · Fichas de marca completas — `en curso`

- **Objetivo:** que cualquiera (persona o agente) pueda producir para una marca leyendo
  solo su ficha.
- **Hace falta:** manuales, webs, guiones, correos y logos de cada marca.
- **Entrega:** `docs/marcas/<marca>/ficha.md` (sofu, riskmann, fegir, yezid-ricaurte) con la
  plantilla `_PLANTILLA.md`.
- **Hecho cuando:** las cuatro fichas tienen todas sus secciones llenas y cada dato con
  fuente; los **⚠ por confirmar** tienen dueño y fecha.
- **Estado 2026-09-26:** las cuatro creadas con lo que había en el repo. SOFU y FEGIR son
  las más incompletas: no hay manual de marca de ninguna de las dos en el repositorio.
  **Actualización 2026-09-26 (tarde):** llegó el manual de FEGIR con sus logos
  (`docs/marcas/fegir/`). SOFU sigue sin manual.

#### Paso 1.2 · Ecosistema y glosario — `en curso`

- **Objetivo:** entender cómo se cruzan las marcas y hablar con las mismas palabras.
- **Entrega:** `docs/marcas/ECOSISTEMA.md` y `docs/marcas/GLOSARIO.md`.
- **Hecho cuando:** las cuatro preguntas de ECOSISTEMA §4 tienen respuesta.

#### Paso 1.3 · Material de los clientes dentro del repo — `pendiente`

- **Objetivo:** que ninguna fuente viva solo en Drive, en un correo o en la cabeza de alguien.
- **Entrega:** carpeta `docs/marcas/<marca>/fuentes/` con manuales, guiones, briefs y capturas
  fechadas de las landings. Lo que tenga datos personales se queda fuera, con una nota
  que diga dónde está.
- **Hecho cuando:** cada fila de «Fuentes oficiales» de las fichas apunta a un archivo del
  repositorio o a una URL con fecha de lectura.
- **Hoy falta:** guion original y manual de SOFU; manual y brief de FEGIR; storyboard de
  inspecciones de RiskMann; videos del Drive del Dr. Yezid.

#### Paso 1.4 · Inventario de lo producido con su estado — `pendiente`

- **Objetivo:** saber de cada una de las 61 carpetas de `videos/` qué es, de qué marca y
  en qué estado está.
- **Entrega:** `docs/INVENTARIO.md` (una fila por proyecto: marca, familia A/B,
  motor, estado, dónde está el final) y el campo `estado` en cada `meta.json`.
- **Hecho cuando:** ninguna carpeta queda sin estado, y la campaña de Yezid dice cuál de
  sus cinco variantes se aprobó.

---

### Etapa 2 — Estándares (cómo se hace, igual para todos)

#### Paso 2.1 · Marca como datos — `pendiente`

- **Objetivo:** que la identidad de cada marca se lea de un archivo, no de copias.
- **Entrega:** `docs/marcas/<marca>/marca.json` (paleta, tipografías con su licencia, logos, voz, CTA,
  prohibiciones), generado desde la ficha.
- **Hecho cuando:** un proyecto nuevo toma su identidad de ahí sin copiar valores a mano.
- **Depende de:** 1.1 y 1.3.

#### Paso 2.2 · La regla de la fuente, aplicable — `pendiente`

- **Objetivo:** que cada frase de un guion diga de dónde sale.
- **Entrega:** esquema del campo `fuente: {archivo, pagina|lamina|url, cita}` para
  `curso.json` y `narracion.json`, documentado con un ejemplo por marca.
- **Hecho cuando:** el esquema está escrito y probado en un proyecto de cada familia.

#### Paso 2.3 · Licencias y datos — `pendiente`

- **Objetivo:** no entregar nada que el cliente no pueda usar, ni guardar lo que no se debe.
- **Entrega:** `docs/LICENCIAS-Y-DATOS.md` + ficha `*-LICENCIA.txt` junto a cada recurso
  de terceros.
- **Hecho cuando:** Segoe UI resuelta; toda la música, fotos y fuentes con ficha; política
  escrita sobre los correos con datos personales.

#### Paso 2.4 · Estados y aprobaciones — `pendiente`

- **Objetivo:** que siempre se sepa qué está aprobado y por quién.
- **Entrega:** convención `estado` / `aprobado_por` / `aprobado_el` en `meta.json` y quién
  aprueba en cada marca (en su ficha).
- **Hecho cuando:** el inventario (1.4) se puede generar leyendo los `meta.json`.

---

### Etapa 3 — Consolidación técnica (la fase 0 de `PLATAFORMA.md`)

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

### Etapa 4 — Materialización

Motor por CLI → uso interno medido → piloto con un tercero → API → interfaz
(`PLATAFORMA.md` §5, fases 1 a 5). Se detalla cuando se cierre la etapa 3.

---

### Registro de avance

| Fecha | Paso | Qué se hizo | Quién |
| --- | --- | --- | --- |
| 2026-09-26 | 1.1, 1.2 | Creadas las fichas de las cuatro marcas, la plantilla, el ecosistema y el glosario | Equipo `fegir` (con Claude) |
| 2026-09-28 | — | Carpetas reordenadas por marca (`docs/marcas/<marca>/`) y documento maestro generado (`docs/MAESTRO.md`, D-04) | Equipo `fegir` (con Claude) |

---

<a id="cap-2"></a>

## 2. Ecosistema de marcas

> Fuente: [`docs/marcas/ECOSISTEMA.md`](marcas/ECOSISTEMA.md) — se edita ahí, no aquí.

> Mapa de a quién le hacemos videos y cómo se relacionan entre sí. El detalle de cada
> una está en su ficha (`<marca>/ficha.md`). Lo marcado **⚠** no tiene fuente todavía.
>
> Última revisión: 2026-09-26.

### 1. El mapa

```
                    SOFU BIC S.A.S.  (Yopal, Casanare · empresa BIC)
                    riesgos y SST · seguridad vial · software · asesoría
                              │
                              │ producto propio («RiskMann by SOFU»)
                              ▼
                          RiskMann  ── riskmann.com · app.riskmann.com
                  Espacios de trabajo · Control de personal ·
                  Capacitaciones/Campus · Seguridad vial (PESV)
                              ┆
                              ┆ sus grabaciones aparecen en las piezas del En Vivo
                              ┆ ⚠ vínculo comercial sin documentar
                              ┆
          ┌───────────────────┴────────────────────┐
          ▼                                        ▼
   Dr. Yezid Ricaurte                        FEGIR
   yezidricaurte.com                         Fundación Especializada en
   abogado · consultor · conferencista       Gestión Integral del Riesgo · fegir.org
          │                                        │
          └──────── En Vivo «PESV · Informe de Autogestión» ────────┘
                    sábado 3 de octubre · 10:00 a. m. · gratuito
                    DOS versiones separadas: nunca se mezclan las marcas
```

### 2. Lo que las une: el PESV

El tema común es el **Plan Estratégico de Seguridad Vial** (ver `GLOSARIO.md`):

- **RiskMann** lo resuelve como software (módulo de Seguridad vial, landing consulta PESV).
- **El Dr. Yezid** lo enseña (En Vivo: cómo generar el informe de autogestión).
- **FEGIR** convoca al mismo En Vivo con su propia marca.
- **SOFU** lo ofrece como servicio de seguridad vial y asesoría.

### 3. Reglas de convivencia entre marcas

1. **Primero, de quién es el video.** La marca que firma decide paleta, tipografía, logo,
   voz y dominio del CTA (PLAYBOOK §3.9).
2. **Una marca por pieza.** Las piezas del Dr. Yezid no muestran FEGIR; las de FEGIR no
   llevan nada de la marca del Dr. Yezid. Del correo solo se toman los datos del evento.
3. **RiskMann puede aparecer como producto** (grabaciones de pantalla) dentro de otra marca
   sin que su logo firme la pieza. ⚠ Confirmar que está autorizado.
4. **La fuente es del dueño de la pieza.** Lo que se dice en un video de FEGIR tiene que
   salir de material de FEGIR o del evento, no de la landing de RiskMann.

### 4. Lo que no sabemos (y conviene preguntar)

- [ ] ¿Qué relación formal hay entre SOFU, FEGIR y el Dr. Yezid?
- [ ] ¿Quién organiza el En Vivo y quién es cada uno ahí (ponente, organizador, patrocinador)?
- [ ] ¿Quién aprueba las piezas en cada marca?
- [ ] ¿Pueden aparecer grabaciones de RiskMann en piezas de otras marcas?

---

<a id="cap-3"></a>

## 3. Fichas de marca

---

<a id="cap-3-1"></a>

### 3.1. SOFU BIC S.A.S.

> Fuente: [`docs/marcas/sofu/ficha.md`](marcas/sofu/ficha.md) — se edita ahí, no aquí.

| Campo | Valor |
| --- | --- |
| Nombre legal / nombre de uso | SOFU BIC S.A.S. / SOFU |
| Qué es (una línea) | Casa matriz de RiskMann: empresa BIC de gestión de riesgos, SST, seguridad vial, software y asesoría |
| Dominio principal | ⚠ por confirmar (no aparece en el repositorio) |
| Responsable del lado del cliente | ⚠ por confirmar |
| Última revisión de esta ficha | 2026-09-26 |

#### 1. Quién es

Según el guion comercial que entregó SOFU (`videos/sofu-comercial/DIRECCION.md`):

- Empresa **BIC** ubicada en **Yopal, Casanare**.
- Servicios: **gestión de riesgos y SST**, **seguridad vial**, **desarrollo de software** y **asesoría**.
- Producto propio: **RiskMann**, «plataforma de gestión de riesgos», para tener «menos tareas manuales».
- Diferenciales que declara: tecnología, experiencia, acompañamiento, innovación y compromiso.

#### 2. Relación con las otras marcas

- **RiskMann** es su producto: el logo oficial de RiskMann es el lockup «RiskMann **by SOFU**»
  (`PRODUCCION-VIDEOS.md` §0.1; `docs/marcas/riskmann/LEEME.md`).
- **FEGIR** y **Dr. Yezid Ricaurte:** ⚠ relación sin documentar. Las piezas del En Vivo PESV
  muestran grabaciones de RiskMann, pero ninguna fuente del repositorio dice qué vínculo
  hay entre SOFU y ellos.

#### 3. Fuentes oficiales

| Fuente | Tipo | Qué fija | Dónde está | Fecha |
| --- | --- | --- | --- | --- |
| Guion comercial de SOFU | guion | Contenido de los comerciales | Resumido en `videos/sofu-comercial/DIRECCION.md`; ⚠ el original no está en el repo | ≤ 2026-09-12 |
| Logo de SOFU | imagen | Marca | `videos/sofu-comercial/assets/marca/sofu-logo.png` (2217×1125) | ≤ 2026-09-12 |
| Piezas de marca de SOFU | varios | Paleta muestreada | ⚠ no identificadas en el repo | — |
| Manual de marca de SOFU | manual | — | ⚠ **no existe en el repo** | — |

#### 4. Identidad visual

- **Paleta** (muestreada de los archivos de SOFU, `DIRECCION.md`): `#19484D` petróleo ·
  `#F9B410` amarillo de acento · `#E8EAE9` gris claro · `#12383C` petróleo profundo ·
  `#0E7C8A` cian · `#FFFFFF` sobre oscuro.
- **Tipografía:** Montserrat con `@font-face` en cada escena (elección de producción; ⚠
  sin manual que la fije).
- **Logo:** solo `sofu-logo.png`. Escala uniforme, opacidad, traslación y recorte del
  archivo completo; nunca redibujar, re-letrar, recolorear ni deformar; área de reserva libre.
- **Contradicciones:** ninguna registrada, porque no hay manual con el que comparar.

#### 5. Voz y tono

- Los comerciales son **sin voz**, al pulso de una pista a 120 BPM (`DIRECCION.md`).
- ⚠ Tono y voz de locución de SOFU: sin definir.

#### 6. Dominio, CTA y datos de contacto

- ⚠ **Faltan los datos de contacto** para el cierre de los comerciales
  (`PRODUCCION-VIDEOS.md`, estado de SOFU).

#### 7. Lo producido

| Proyecto | Formato | Duración | Estado | Dónde |
| --- | --- | --- | --- | --- |
| `videos/sofu-comercial/` | 16:9, sin voz | 68 s | Renderizado; pendiente contacto y portafolio | Drive 05 |
| `videos/sofu-comercial-v2/` | 16:9, gancho + golpe + cierre | 52 s | Renderizado; mismos pendientes | Drive 06 |
| `videos/sofu-comercial-v2-vertical/` | 9:16 | 52 s | Renderizado; mismos pendientes | Drive 06b |

#### 8. Decisiones tomadas

| Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- |
| 2026-09-12 | Nada en pantalla que no esté en el guion o en piezas de marca de SOFU | Regla de la fuente | Juan |

#### 9. Pendientes y ⚠ por confirmar

- [ ] Validar con SOFU el **portafolio vigente** antes de publicar los comerciales.
- [ ] Dominio web y datos de contacto.
- [ ] Relación de SOFU con FEGIR y con el Dr. Yezid Ricaurte.

#### 10. Qué hay que pedirle al cliente

- [ ] El **guion original** (archivo) para guardarlo en el repositorio.
- [ ] **Manual de marca** de SOFU (o confirmar que no existe y aprobar la paleta muestreada).
- [ ] Logo en vector (SVG/PDF) además del PNG.
- [ ] Datos de contacto y CTA para los cierres.

#### 11. Historial de la ficha

| Fecha | Cambio | Quién |
| --- | --- | --- |
| 2026-09-26 | Ficha creada con lo que había en el repositorio | Equipo `fegir` (con Claude) |

---

<a id="cap-3-2"></a>

### 3.2. RiskMann

> Fuente: [`docs/marcas/riskmann/ficha.md`](marcas/riskmann/ficha.md) — se edita ahí, no aquí.

| Campo | Valor |
| --- | --- |
| Nombre legal / nombre de uso | RiskMann (producto de SOFU BIC S.A.S.; lockup «RiskMann by SOFU») |
| Qué es (una línea) | Plataforma digital de gestión de riesgos empresariales |
| Dominio principal | `riskmann.com` · aplicación en `app.riskmann.com` |
| Responsable del lado del cliente | ⚠ por confirmar |
| Última revisión de esta ficha | 2026-09-26 |

#### 1. Quién es

- «Solución digital para gestionar riesgos de forma simple, segura y conforme a la
  normativa» (manual oficial, `docs/marcas/riskmann/LEEME.md`).
- **Módulos reales** (los que tienen icono de portada, `CLAUDE.md`): Espacios de trabajo,
  Control de personal, Capacitaciones/Campus y Seguridad vial.
- «Sala de control» **no** es un módulo: es un concepto visual de un video (`CLAUDE.md`).

#### 2. Relación con las otras marcas

- Producto de **SOFU** (lockup «by SOFU»).
- Sus grabaciones de pantalla aparecen en las piezas del **En Vivo PESV** del Dr. Yezid
  Ricaurte («tu informe con un solo clic»). ⚠ El vínculo comercial no está documentado.

#### 3. Fuentes oficiales

| Fuente | Tipo | Qué fija | Dónde está | Fecha |
| --- | --- | --- | --- | --- |
| Manual de identidad (claro y oscuro) | PDF | Paleta, Dubai, caballero, anillos, reglas del isotipo | `docs/marcas/riskmann/manual-identidad*.pdf` + lectura en `docs/marcas/riskmann/LEEME.md` | 2026-09-17 (traído al repo) |
| Manejo del PESV en 24 pasos | PDF | Contenido del publicitario PESV | `docs/marcas/riskmann/fuentes/manejo-pesv-24-pasos.pdf` | 2026-09-18 |
| Landing consulta PESV | web | Copy y umbral de vehículos | `https://riskmann.com/consulta-pesv/` | leída ~2026-09-17 |
| Landing inspecciones gratis | web | Copy de 3 anuncios | `https://riskmann.com/inspecciones-gratis/` | leída 2026-09-23 |
| Landing capacitaciones | web | Copy del promo y la serie; identidad negro + dorado | `https://riskmann.com/capacitaciones` | 2026-09-26 |
| Logos oficiales | PNG | Cierre en fondo oscuro | `assets/public/riskmann_logo_blanco.png` (lockup), `riskmann_icono_blanco.png` (isotipo) | — |
| Iconos de módulo y grabaciones de UI | webp / mp4 | Material de producto | `assets/` | — |
| Drive «Manuales de Identidad» | Drive | Origen de los manuales | Enlace en el issue #3 | — |

#### 4. Identidad visual

- **Paleta del manual:** `#020202` fondo · `#c8951a` dorado (prestigio) · `#06c7fb` cian
  (acento) · `#272725` separadores. Isotipo: `#333366`, `#FF3333`, `#26367D`, `#FFFFFF`.
- **Tipografía del manual:** Dubai Bold (títulos) y Regular (cuerpo); `line-height` ≥ 1.5.
- **Estilo:** caballero medieval en fotografía real, dos anillos concéntricos cian + dorado,
  pesos mezclados dentro de una frase (Bold en lo que carga el mensaje, Light en conectores).
- **Logo:** solo los archivos oficiales; no deformar, recolorear, girar, tapar ni redibujar.
- **Prohibido:** cifras o afirmaciones normativas sin fuente; figuras humanas dibujadas;
  el «100 %» inventado de la sala de control.
- **Contradicciones abiertas:**
  - La receta **`riskmann-hud`** (que `CLAUDE.md` recomienda) **no corresponde al manual**.
  - La **landing de capacitaciones** usa negro + dorado **`#AC841D`** con Montserrat + Open
    Sans; el manual fija dorado `#c8951a` y Dubai. El promo y la serie de capacitaciones
    (26-sep) siguen la landing **por decisión del cliente para esas piezas**; sigue abierto
    cuál manda en general.

#### 5. Voz y tono

- **Carlos** (ElevenLabs, colombiana) `4PN5DHmrfIgZksvIrawS`.
  - Narrado (`eleven_multilingual_v2`): `stability 0.32 · style 0.45`, velocidad por plano.
  - Vendedor (`eleven_v3`): `stability 0.15 · style 0.78 · speed 1.03`.
- Cursos «Ruta Segura»: Carlos con `eleven_v3`. Módulo PESV M01: Piper `es_ES-davefx-medium`.
- ⚠ **La voz de RiskMann sigue sin decidir** entre siete muestras (`BITACORA-2026-09-17-18.md`).
- Tono: tú, directo («¿Inspeccionas TODOS tus vehículos?»).

#### 6. Dominio, CTA y datos de contacto

- CTAs literales de las landings: «Quiero mi inspección gratis», «Quiero activar
  Capacitaciones», «Quiero empezar ahora». Capacitaciones gratis **hasta el 1 de enero de 2027**.
- Entrada a la aplicación: `app.riskmann.com/entrada`. QR oficial en el promo de capacitaciones.

#### 7. Lo producido

| Proyecto | Formato | Duración | Estado | Dónde |
| --- | --- | --- | --- | --- |
| `riskmann-sala-de-control/` | 16:9, muda y narrada | 68 s | **No usar comercialmente** («100 %» sin fuente, logo redibujado en 03 y 09) | Drive 04/04b |
| `pesv-m01-mando/` | Módulo con voz | 2:31 | Entregable del PoC | Drive 01 |
| `pesv-m01-ritmo[-vertical]/` | Sin voz, 120 BPM | 60 s | Entregado | Drive 02/02b |
| `pesv-m01-profundidad[-vertical]/` | Exploración 3D | — | Apertura aprobada, resto sin construir | — |
| `ruta-segura-m1…m4/` | Curso lámina a lámina | 16 min | Entregado, cortado en piezas | Drive 07+ |
| `moto-*` (15 videos) | Curso generado | 40:47 | Entregado | `../videos-finales/` |
| `csm-*` (15 videos) | Curso generado + banco de preguntas | ~33 min | Entregado | `../videos-finales/` |
| `riskmann-consulta-pesv[-vertical]/` | 16:9 y 9:16, voz + música | 33.3 s | Variante A entregada | `ENTREGABLES-VIDEO\` (equipo de Alejandro) |
| `riskmann-pesv-v2/` | Lente como cámara continua | 34 s | Esqueleto verificado | — |
| `riskmann-pesv-publicitario/` | 8 escenas | ~36 s | Programado | — |
| `riskmann-inspecciones-ads/` | 3 anuncios, lienzo propio | 3 × 12 s | ⚠ estado por confirmar | — |
| `riskmann-capacitaciones-promo/` | HyperFrames 9:16, 7 escenas, QR oficial | 39,3 s | Entregado (V2, 26-sep) | `ENTREGABLES-VIDEO/riskmann-capacitaciones/` |
| `riskmann-capacitaciones-serie/` | 4 anuncios verticales gancho / valor / cta | 15,5–17,4 s | Entregados (26-sep) | `ENTREGABLES-VIDEO/riskmann-capacitaciones/serie/` |

#### 8. Decisiones tomadas

| Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- |
| ≤ 2026-09-12 | Nada entra al video sin rastrearse a un archivo de RiskMann | Se coló un «100 %» inventado | Juan |
| 2026-09-17 | La identidad se construye contra el manual en PDF, no contra `riskmann-hud` | La receta no coincide con el manual | Alejandro |
| 2026-09-17 | Música de catálogo con licencia sin restricción de plataforma (Mixkit, Pixabay) | Las piezas van a Reels y TikTok | Alejandro |
| 2026-09-18 | Rojo reservado para «peligro» | Entrega del 18-sep | Cliente |
| 2026-09-26 | El promo y la serie de Capacitaciones usan la identidad de **la landing** (negro + `#AC841D`, Montserrat + Open Sans) | Quien vea el video y entre a la página la reconoce | Cliente |
| 2026-09-26 | El QR `qr-app-riskmann-com` (→ `app.riskmann.com/entrada`) es el mismo del brochure; va en el cierre de las piezas de Capacitaciones | Vía secundaria al botón cuando el video se proyecta | Equipo `fegir` |

#### 9. Pendientes y ⚠ por confirmar

- [ ] **Umbral del PESV:** la landing dice «11 o más vehículos» y «diez (10) unidades».
- [ ] Rehacer o dejar de recomendar `riskmann-hud`.
- [ ] Manual frente a landing de capacitaciones: qué dorado y qué tipografía mandan.
- [ ] Elegir la voz oficial.
- [ ] Corregir o retirar «Sala de control».
- [x] Guardar en git el promo y la serie de capacitaciones (26-sep).
- [ ] Respuestas de las preguntas frecuentes de la landing de Capacitaciones (precio, validez del certificado).

#### 10. Qué hay que pedirle al cliente

- [ ] Confirmación escrita del umbral de vehículos y la norma de la que sale.
- [ ] El storyboard «LANDING INSPECCIONES GRATIS» (no está ni en el repo ni en el Drive).
- [ ] Decisión sobre la identidad de las landings frente al manual.
- [ ] Nueva clave de ElevenLabs (la del issue #3 caducó el 21-sep-2026).

#### 11. Historial de la ficha

| Fecha | Cambio | Quién |
| --- | --- | --- |
| 2026-09-26 | Ficha creada con lo que había en el repositorio | Equipo `fegir` (con Claude) |

---

<a id="cap-3-3"></a>

### 3.3. FEGIR

> Fuente: [`docs/marcas/fegir/ficha.md`](marcas/fegir/ficha.md) — se edita ahí, no aquí.

| Campo | Valor |
| --- | --- |
| Nombre legal / nombre de uso | Fundación Especializada en Gestión Integral del Riesgo / FEGIR |
| Qué es (una línea) | Fundación dedicada a la gestión integral del riesgo |
| Dominio principal | `fegir.org` |
| Responsable del lado del cliente | ⚠ por confirmar |
| Última revisión de esta ficha | 2026-09-26 |

#### 1. Quién es

- Nombre completo y dominio tomados de la escena de cierre de `videos/fegir-envivo/`
  («FEGIR - Fundación Especializada en Gestión Integral del Riesgo», «fegir.org»).
- Lema usado en la locución: «FEGIR… tu seguridad, nuestra prioridad.»
  ⚠ Confirmar que es un lema oficial.
- ⚠ Qué servicios ofrece, a quién y desde dónde: sin documentar.

#### 2. Relación con las otras marcas

- **Dr. Yezid Ricaurte:** el En Vivo PESV del 3 de octubre se comunica en **dos versiones
  separadas**: la de FEGIR («La Fundación FEGIR te invita a un en vivo, gratuito», CTA a
  `fegir.org`) y la de la página del Dr. Yezid (sin FEGIR en pantalla). Nunca se mezclan.
- Uno de los prompts de la campaña de Yezid decía «Organizado por Fundación FEGIR»; no se
  puso en pantalla porque ni los correos ni la web lo mencionaban.
- **SOFU / RiskMann:** ⚠ relación sin documentar.

#### 3. Fuentes oficiales

| Fuente | Tipo | Qué fija | Dónde está | Fecha |
| --- | --- | --- | --- | --- |
| **Manual de identidad FEGIR** | PDF (1 página) | Paleta, logo primario, favicon, espacio de respeto, usos incorrectos | `docs/marcas/fegir/manual-identidad-fegir.pdf` | entregado 2026-09-25 |
| Logos (color, blanco, escudo) | SVG + PNG 600 ppp | Marca | `docs/marcas/fegir/logos-extraidos/` (extraídos de los **vectores** del manual) | 2026-09-25 |
| Web de FEGIR (captura) | PDF | Servicios, titular «¡Tu seguridad, nuestra prioridad!», anuncio del En Vivo | `docs/marcas/fegir/web-fegir-captura.pdf` | 2026-09-25 |
| Portada del manual (vertical) | imagen | Foto de apertura | `videos/fegir-envivo/assets/fotos/portada-manual-vertical.jpg` (recorte de la foto del manual) | 2026-09-25 |
| Correos del En Vivo | correo | Datos del evento y pasos | `Documentos_contexto/correos-en-vivo-pesv/` (**fuera del repo**: datos personales) | — |

#### 4. Identidad visual

- **Paleta del manual (s.2):** verde `#45a035`, verde claro `#a8c875`, crema `#f1ecb0`.
  Banda verde del manual muestreada: `#50cd72 → #4ecd25`. Derivados de producción para
  contraste: `#3a8f2c` (fondo bajo texto blanco, 3,9:1), `#22621a` (texto verde sobre
  blanco), `#2e7a22`.
- **Tipografía:** Segoe UI (declarada como «FEGIR Sans»).
  ⚠ **Segoe UI es de Microsoft**: confirmar licencia o cambiar a una fuente libre.
- **Logo:** `fegir-logo-color` (primario, sobre claro), `fegir-logo-blanco` (sobre verde u
  oscuro), `fegir-escudo-color` (favicon). Reglas del manual: no aplastar, alargar, girar ni
  cambiar color; nada encima; sin fondos; respetar el kerning.
- **Contradicciones:** ninguna registrada.

#### 5. Voz y tono

- **Carlos** `4PN5DHmrfIgZksvIrawS`, `eleven_multilingual_v2`, semilla fija `20261003`,
  `stability 0.32 · similarity 0.85 · style 0.5 · speed 0.97` (`fegir-recordatorios/serie.py`).
- Siglas escritas para que se lean deletreadas: «pe e ese ve».
- Tono: tú, cercano, de invitación.
- Música: cama generada con ElevenLabs a 104 BPM (piano, guitarra, palmas suaves); prompt en
  `videos/fegir-envivo/assets/musica/ORIGEN.txt`.

#### 6. Dominio, CTA y datos de contacto

- CTA: «Reserva tu cupo gratis en fegir punto org.» → `fegir.org`.

#### 7. Lo producido

| Proyecto | Formato | Duración | Estado | Dónde |
| --- | --- | --- | --- | --- |
| `videos/fegir-envivo/` | 9:16, HyperFrames, editable en el Studio | 21,9 s | **Aprobado** (V4, 26-sep: con redes Instagram · TikTok · YouTube) | `ENTREGABLES-VIDEO/fegir-envivo/` |
| `videos/fegir-envivo-pesv/` | Versión combinada con Yezid (paleta y montaje de su invitación) | 18 s | **Descartada** (26-sep): «debe ser independiente» | `ENTREGABLES-VIDEO/fegir-envivo-pesv/` |
| `videos/fegir-recordatorios/` | 3 videos: pocos días / mañana / hoy | 18,9 / 16,6 / 15,5 s | Entregados (26-sep) | `ENTREGABLES-VIDEO/fegir-recordatorios/` |

#### 8. Decisiones tomadas

| Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- |
| ≤ 2026-09-26 | Las piezas de FEGIR no llevan nada de la marca de Yezid; del correo solo se toman datos del evento | Son dos entregas distintas del mismo evento | Equipo `fegir` |
| ≤ 2026-09-26 | Recordatorios heredan identidad y escenas de `fegir-envivo` | Es la pieza aprobada | Equipo `fegir` |
| 2026-09-26 | Identidad propia del manual de FEGIR (verde vivo, planos verde/blanco), no la paleta de Yezid | La V1 recoloreada «parecía dependiente» | Cliente |
| 2026-09-26 | Sigla escrita «pe e ese ve»; redes (Instagram · TikTok · YouTube) en todas las piezas | Sonaba distinta en cada frase; las redes solo salían en «Hoy» | Cliente |

#### 9. Pendientes y ⚠ por confirmar

- [ ] Licencia de Segoe UI (o cambio de fuente).
- [x] Origen oficial de los tres logos: extraídos del manual (26-sep).
- [ ] Que el cupo se reserve en `fegir.org` y cuál es el enlace del grupo de WhatsApp.
- [ ] Qué hace FEGIR, a quién le habla, y su relación con SOFU/RiskMann y con el Dr. Yezid.
- [ ] Guardar en git los cambios de `fegir-envivo` y la serie de recordatorios.

#### 10. Qué hay que pedirle al cliente

- [ ] **Manual de marca** de FEGIR completo (hay una portada, no el manual).
- [ ] El **brief** de la campaña como archivo.
- [ ] Logos en vector y reglas de uso.
- [ ] Confirmar lema, dominio y datos de contacto.

#### 11. Historial de la ficha

| Fecha | Cambio | Quién |
| --- | --- | --- |
| 2026-09-26 | Ficha creada con lo que había en el repositorio | Equipo `fegir` (con Claude) |

---

<a id="cap-3-4"></a>

### 3.4. Dr. Yezid Ricaurte

> Fuente: [`docs/marcas/yezid-ricaurte/ficha.md`](marcas/yezid-ricaurte/ficha.md) — se edita ahí, no aquí.

| Campo | Valor |
| --- | --- |
| Nombre legal / nombre de uso | Dr. Yezid Ricaurte |
| Qué es (una línea) | Abogado, consultor y conferencista; marca personal con página propia |
| Dominio principal | `yezidricaurte.com` |
| Responsable del lado del cliente | ⚠ por confirmar |
| Última revisión de esta ficha | 2026-09-26 |

#### 1. Quién es

- «Abogado · Consultor · Conferencista · 27 años de trayectoria» (texto usado en
  `videos/yezid-envivo-15s/GUION.md`; ⚠ confirmar que viene de su web).
- Dicta el **En Vivo «PESV · Informe de Autogestión»**: sábado **3 de octubre**,
  **10:00 a. m. (hora Colombia)**, gratuito. Página del evento:
  `yezidricaurte.com/en-vivos/pesv-informe-autogestion/`.
- **La firma quien dicta el evento, no una empresa** (`BITACORA-2026-09-17-18.md`).

#### 2. Relación con las otras marcas

- **FEGIR:** el mismo En Vivo tiene una versión FEGIR separada. En las piezas del Dr. Yezid
  **FEGIR no aparece**, porque no aparece ni en su página ni en sus correos.
- **RiskMann:** sus piezas muestran una grabación real de RiskMann (gráficas de
  conductores) para ilustrar «el informe con un solo clic». ⚠ Vínculo sin documentar.

#### 3. Fuentes oficiales

| Fuente | Tipo | Qué fija | Dónde está | Fecha |
| --- | --- | --- | --- | --- |
| Manual de marca Yezid Ricaurte | PDF | Dubai, verde `#336666`, oliva `#80804a`, tierra `#cdb5a2`, firma | `docs/marcas/yezid-ricaurte/manual-yezid-ricaurte.pdf` | 2026-09-18 |
| Página web | web | Cormorant Garamond + Montserrat, `#001217`, escala dorada | `yezidricaurte.com` | — |
| Página del En Vivo | web | Copy del evento | `yezidricaurte.com/en-vivos/pesv-informe-autogestion/` | — |
| Correos de la campaña (3) | correo | Petróleo `#001f26`, filete `#d2b96a`, botón coral `#f06e49`, asuntos | `Documentos_contexto/correos-en-vivo-pesv/` (**fuera del repo**: datos personales) | — |
| Foto oficial | imagen | Recorte publicado en su web | `yezidricaurte.com/images/yezid-portada-1.png` | — |
| Firma en negativo | imagen | Extraída del manual, sin redibujar | `assets/firma-yezid-blanca.png` en los proyectos | — |
| Videos del Drive del Dr. Ricaurte | video | Sus propias palabras | ⚠ **no accesibles** con la cuenta actual | — |

#### 4. Identidad visual

**Hay dos sistemas y el cliente eligió según la pieza:**

| | Manual de marca | Página web + correos |
| --- | --- | --- |
| Tipografía | Dubai (Bold, Medium, Regular) | Cormorant Garamond + Montserrat |
| Paleta | Verde `#336666`, oliva `#80804a`, tierra `#cdb5a2` | `#001217` / petróleo `#001f26`, dorado `#d2b96a`, pálido `#f1ecb0`, coral `#f06e49` (botón) |
| Usado en | `yezid-envivo-pesv-autogestion` (decisión: manda el manual) | `-estudio`, `-premium` (Montserrat de la web), `-campana` (mezcla manual + correo) |

- **Contraste:** oliva `#80804a` = 1.75:1 y tierra `#cdb5a2` = 2.99:1 sobre oscuro → variantes
  aclaradas **solo para texto**.
- **Firma:** la oficial en negativo; **nunca redibujarla** (el manual lo prohíbe).
- **Prohibido:** **rojo** (reservado para «peligro»; el coral del botón es el color de acción
  de los correos, no ese rojo); nada de FEGIR.
- **Contradicción abierta:** manual frente a web. En la promo principal se eligió el manual,
  aceptando que «el video no se parece a la página a la que manda la gente».
  ⚠ Definir una regla para las piezas siguientes.

#### 5. Voz y tono

- **Carlos** `4PN5DHmrfIgZksvIrawS`, `eleven_multilingual_v2`,
  `stability 0.35 · claridad 0.80 · style 0.45 · speed 1.0`; frases encadenadas
  (`previous_text` / `next_text`), 3 tomas y gana la más pausada que quepa.
- PESV deletreado (`P-E-S-V`); «vivo» nunca cierra frase.
- ⚠ Si comparten los videos del Drive, usar las palabras del propio Dr. Yezid.

#### 6. Dominio, CTA y datos de contacto

- «Cupo gratuito en yezidricaurte punto com.» · «Reservar cupo gratis →».
- Campaña por etapas: «Crea tu cuenta» / «Entrar al grupo de WhatsApp» / «Ir al grupo de WhatsApp».

#### 7. Lo producido

| Proyecto | Formato | Duración | Estado | Dónde |
| --- | --- | --- | --- | --- |
| `yezid-envivo-pesv-autogestion/` | 9:16 HyperFrames, voz + efectos + música | 15 s | Entregado (variante A) | `ENTREGABLES-VIDEO\` |
| `yezid-envivo-15s/` | Lienzo propio, Three.js | 15 s | ⚠ estado por confirmar | — |
| `yezid-envivo-campana/` | 3 videos de 12 s (18 días / mañana / hoy) | 12 s | ⚠ estado por confirmar | — |
| `yezid-envivo-campana-v2/` | Segunda versión de la campaña | 12 s | ⚠ estado por confirmar | — |
| `yezid-envivo-estudio/` | «Estudio virtual», 3 videos, fondo escudo o plexus | 12 s | ⚠ estado por confirmar | — |
| `yezid-envivo-premium/` | Una composición, 3 etapas en `config.js` | 12 s | ⚠ estado por confirmar | — |

**Hay cinco variantes de campaña y ningún documento dice cuál se aprobó.**

#### 8. Decisiones tomadas

| Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- |
| 2026-09-18 | En la promo principal manda el manual, no la web | Elección del cliente | Cliente |
| 2026-09-18 | El protagonista es el En Vivo, no la explicación del PESV | La primera versión explicaba la norma | Cliente |
| 2026-09-18 | Música Pixabay «elegant» (atlasaudio), sin restricción de plataforma | Licencia verificada | Alejandro |
| ≤ 2026-09-26 | Es un video de yezidricaurte.com, no de FEGIR | Aclaración del cliente | Cliente |

#### 9. Pendientes y ⚠ por confirmar

- [ ] **Cuál de las cinco variantes de campaña quedó aprobada**; archivar las demás.
- [ ] Regla de identidad para piezas nuevas: manual o web.
- [ ] Origen del texto «27 años de trayectoria».

#### 10. Qué hay que pedirle al cliente

- [ ] Acceso a los videos del Drive del Dr. Ricaurte.
- [ ] Confirmación de la variante aprobada de la campaña.
- [ ] Autorización para guardar una copia anonimizada de los correos en el repo (o dejarla fuera a propósito).

#### 11. Historial de la ficha

| Fecha | Cambio | Quién |
| --- | --- | --- |
| 2026-09-26 | Ficha creada con lo que había en el repositorio | Equipo `fegir` (con Claude) |

---

<a id="cap-4"></a>

## 4. Glosario

> Fuente: [`docs/marcas/GLOSARIO.md`](marcas/GLOSARIO.md) — se edita ahí, no aquí.

> Términos del negocio y de la producción que aparecen en el repositorio. Si una palabra
> se usa en dos sentidos, aquí se dice cuál es cuál. Añadir en orden alfabético.

### Del negocio

| Término | Significado | Fuente / nota |
| --- | --- | --- |
| **BIC** | Sociedad de Beneficio e Interés Colectivo (figura jurídica colombiana) | SOFU es «empresa BIC» (guion de SOFU) |
| **En Vivo** | Conversatorio en línea y gratuito del Dr. Yezid Ricaurte; el del PESV es el sábado 3 de octubre a las 10:00 a. m. | Página del evento en `yezidricaurte.com` |
| **Informe de autogestión** | Informe del PESV que se reporta; el En Vivo enseña a generarlo «con un solo clic» | Copy de la campaña del En Vivo |
| **PESV** | Plan Estratégico de Seguridad Vial | En locución se deletrea: `P-E-S-V` o «pe e ese ve» |
| **Resolución 20223040040595 de 2022** | Norma citada en la landing de inspecciones (paso 16) | `riskmann.com/inspecciones-gratis/` |
| **SMMLV** | Salario mínimo mensual legal vigente | Aparece en cifras de sanciones («500 SMMLV») |
| **SST** | Seguridad y Salud en el Trabajo | Servicio de SOFU |
| **Umbral de vehículos** | A partir de cuántos vehículos se exige el PESV. ⚠ La landing dice 11 y también 10 | PLAYBOOK §9 |

### De la producción

| Término | Significado |
| --- | --- |
| **Composición** | Un archivo HTML de HyperFrames con su timeline; `index.html` es la raíz y `compositions/` guarda las subcomposiciones |
| **Curso generado** | Curso producido por plantillas a partir de `curso.json` (moto, csm) |
| **Determinismo** | El render busca cada fotograma por tiempo y siempre da lo mismo: sin `Math.random`, `Date.now` ni `repeat:-1` |
| **Ducking** | Bajar la música automáticamente cuando habla la voz (`musica` en `mezcla.py`) |
| **Familia A / B** | A: cursos generados por plantillas. B: piezas de marketing a medida (`PLATAFORMA.md` §3.1) |
| **Ficha de marca** | Documento por marca en `docs/marcas/<marca>/ficha.md` |
| **Hoja de contactos** | Imagen con varios fotogramas del video para revisarlo sin verlo entero |
| **HyperFrames** | Framework de HeyGen que convierte HTML + GSAP en MP4; el motor principal del repo |
| **Lienzo propio** | Piezas hechas en HTML + GSAP + Three.js con su propio `render.mjs` (puppeteer), sin HyperFrames |
| **LUFS** | Medida de volumen percibido; −14 LUFS para redes, −16 en los módulos |
| **Muestra** | Los primeros ~15 s con sonido, para aprobar la dirección antes de producir todo |
| **Receta** (`riskmann-hud`) | Identidad visual congelada para reutilizar; ⚠ la de RiskMann no coincide con el manual |
| **Studio** | Editor visual de HyperFrames (`npx hyperframes preview`) |
| **Tiempo muerto** | Tramo en que la imagen casi no cambia; se mide con diferencia entre fotogramas (PLAYBOOK §6.4) |
| **Variante A/B/C** | Versiones de audio de una misma pieza (A: voz + efectos + música) |

---

<a id="cap-5"></a>

## 5. Playbook

> Fuente: [`docs/PLAYBOOK.md`](PLAYBOOK.md) — se edita ahí, no aquí.

> **Qué es esto.** La memoria destilada de todo lo que se produjo en este repositorio
> (2026): qué se hizo, **cómo** se hizo y qué parte se lleva tal cual a
> un proyecto nuevo — de RiskMann o de cualquier otro cliente.
>
> No sustituye a los otros documentos, los ordena:
>
> | Documento | Pregunta que responde |
> | --- | --- |
> | **Este** | ¿Qué formato elijo, qué copio y en qué orden trabajo? |
> | [`PRODUCCION-VIDEOS.md`](#cap-6) | ¿Cuáles son los valores y reglas exactos de cada formato? |
> | [`GUIA-PROMPTS.md`](#cap-7) | ¿Qué le digo al agente para conseguir cada cosa? |
> | [`POC-SEGURIDAD-VIAL-PASAJEROS.md`](#cap-10-2) | ¿Qué se entregó en el PoC y cómo responde al issue? |
> | [`ARRANQUE-EN-OTRO-EQUIPO.md`](#cap-8) | ¿Qué instalo en un equipo nuevo y qué errores de audio, GSAP y verificador ya se pagaron? |
> | [`BITACORA-2026-09-17-18.md`](#cap-10-1) | ¿Qué se decidió en las piezas verticales de RiskMann y Yezid, y qué quedó abierto? |
> | [`marcas/riskmann/LEEME.md`](#cap-10-3) | ¿Qué fija el manual oficial de RiskMann (y qué solo se ve mirando las páginas)? |
> | [`PLATAFORMA.md`](#cap-9) | ¿Hacia dónde evoluciona esto, qué ideas hay sobre la mesa y qué se decidió? |
>
> **Tres líneas de trabajo** alimentan este documento: la de cursos y PoC (Juan), la de
> piezas verticales con ElevenLabs y manual de marca (Alejandro) y la de campañas de En
> Vivo y anuncios de landing (equipo `fegir`). Las secciones §6 y §9 recogen las dos
> últimas.

---

### 1. Qué se produjo

| Serie | Entrada | Formato | Salida | Proyecto(s) |
| --- | --- | --- | --- | --- |
| RiskMann «Sala de control» | Logos, iconos, capturas y 3 grabaciones de UI | Marketing, 9 planos | 68 s, muda y narrada | `videos/riskmann-sala-de-control/` |
| PESV «Pasajero seguro» · M01 | PDF de diapositivas | «Centro de mando» (voz Piper) | 2:31 — **entregable del PoC** | `videos/pesv-m01-mando/` |
| PESV · M01 corto | El mismo PDF | «Ritmo» (sin voz, 120 BPM) | 60 s, 16:9 y 9:16 | `videos/pesv-m01-ritmo[-vertical]/` |
| PESV · exploración | El mismo PDF | Partículas GPU + 3D | Apertura aprobada, resto sin construir | `videos/pesv-m01-profundidad[-vertical]/` |
| SOFU BIC S.A.S. | Guion de la empresa | Comercial | 68 s; v2 dinámica 52 s (16:9 y 9:16) | `videos/sofu-comercial/`, `videos/sofu-comercial-v2[-vertical]/` |
| «Ruta Segura» (ciclistas) | PPTX de 33 láminas con notas | Curso lámina a lámina, láminas escritas a mano (`eNN.py`) | 4 módulos, 16 min, cortados en piezas de 1–2 min | `videos/ruta-segura-m1…m4/` |
| «Motociclista laboral seguro» | PPTX de 88 láminas con **formas con nombre** | Curso **generado** por plantillas | 15 videos, 40:47 | `videos/moto-curso/` → `moto-*` |
| «Conducción Segura y Manejo Defensivo» | PPTX de 55 láminas | Curso **generado** por plantillas | 15 videos, ~33 min + banco de preguntas | `videos/csm-curso/` → `csm-*` |
| RiskMann · consulta PESV | Landing del PESV + manual oficial (`docs/marcas/riskmann/`) | Vertical para redes, ElevenLabs + música con ducking | 33.3 s 9:16, variantes de audio A/B/C (se entregó la A); también 16:9 | `videos/riskmann-consulta-pesv[-vertical]/` |
| RiskMann · PESV v2 y publicitario | Manual oficial | «La lente del manual como cámara continua»; publicitario de 8 escenas | Esqueleto verificado; publicitario ~36 s programado | `videos/riskmann-pesv-v2/`, `videos/riskmann-pesv-publicitario/` |
| Yezid Ricaurte · En Vivo | Página del evento + manual de Yezid | Promo vertical, HyperFrames, rejilla de tempo | 15 s 9:16, voz + efectos + música | `videos/yezid-envivo-pesv-autogestion/` |
| Yezid Ricaurte · campañas del En Vivo | Correos de la campaña + web + manual | **Lienzo propio** (Three.js + GSAP + puppeteer), una composición y varias variantes | 15 s; campañas de 3 videos de 12 s (pocos días / mañana / hoy) | `videos/yezid-envivo-15s/`, `-campana[-v2]/`, `-estudio/`, `-premium/` |
| FEGIR · En Vivo | Mismo evento, firmado **solo** por la Fundación FEGIR + manual de FEGIR | HyperFrames, reorganizado para editar en el Studio | 21,9 s 9:16, 5 escenas, voz + efectos + música generada (V4 vigente). `fegir-envivo-pesv` fue la versión combinada con Yezid: **descartada** | `videos/fegir-envivo/` |
| FEGIR · recordatorios del En Vivo | Correos de la campaña (solo estructura y datos) | 3 proyectos HyperFrames generados por `serie.py` | 3 × 15–19 s (pocos días / mañana / hoy) | `videos/fegir-recordatorios/` |
| RiskMann · Capacitaciones, promo | Solo la landing `riskmann.com/capacitaciones` | HyperFrames generado (`tools/construir.py`), identidad de la landing | 39,3 s 9:16, 7 escenas, QR oficial | `videos/riskmann-capacitaciones-promo/` |
| RiskMann · Capacitaciones, serie | La misma landing | 4 anuncios `gancho / valor / cta` generados por `serie.py` (importa las plantillas del promo) | 4 × 15–17 s 9:16 | `videos/riskmann-capacitaciones-serie/` |
| RiskMann · «Inspecciones gratis» | Solo la landing `riskmann.com/inspecciones-gratis/` | Lienzo propio, 3 anuncios `hook / valor / cta` | 3 × 12 s 9:16, `eleven_v3` | `videos/riskmann-inspecciones-ads/` |

Todas las entregas finales están en `../videos-finales/` (con su `LEEME.txt`) y en la
carpeta de Drive enlazada en el [README](#cap-10-4).

#### La curva de aprendizaje, en una línea por paso

1. **Sala de control** — un día entero inventando el sistema (paleta, HUD, reglas). Nació
   la regla §0: se coló un «100 %» inventado.
2. **PESV M01** — tres direcciones rechazadas (réplica, «plus», monigotes, refactor
   fotográfico) antes de «Centro de mando». Nació la regla *muestra antes que módulo*.
3. **Ritmo** — aprobado sin cambios: el pulso musical como reloj de la animación.
4. **Ruta Segura** — la voz dicta el tiempo; `cronometro.py` separa el montaje de la
   locución; render por partes en 8 GB de RAM.
5. **Moto y CSM** — el salto de escala: de 12 láminas escritas a mano a 88 generadas. Un
   curso entero de 15 videos sale de `curso.json` + 6–7 plantillas + un comando por módulo.
6. **Consulta PESV vertical** — la música tapaba la voz 8–16 dB y 44 de 76 ventanas
   estaban congeladas. Nacieron la clave `musica` de `mezcla.py`, `nivelar-voz.py` y la
   medición de tiempos muertos; la identidad pasó a construirse contra el manual en PDF.
7. **En Vivo (Yezid / FEGIR)** — el mismo evento en dos marcas y varios estilos. Nació la
   pregunta que ahora va primero: **¿de quién es el video?** — y la puntuación medida
   para ElevenLabs (`…` como pausa, siglas deletreadas).
8. **Anuncios de landing** — una sola URL como fuente y tres ángulos (`hook / valor / cta`)
   sobre la misma composición: la campaña corta se vuelve configuración (`js/config.js`).
9. **FEGIR sola y Capacitaciones (26-sep)** — la pieza de FEGIR recoloreada sobre la de
   Yezid se rechazó por «dependiente»: una marca por video, también en el color y la
   estructura. Las series pasaron a ser **HyperFrames generado**: un script pide la voz con
   semilla fija, lee sus tiempos y escribe `index.html` + una sub-composición por escena,
   editables en el Studio (`serie.py`, `construir.py`).

**La lección de fondo:** el primer video de un formato cuesta un día; el segundo, una
hora; con el formato convertido en generador, un módulo cuesta lo que tarda su render.

---

### 2. Elegir el formato

```
¿Qué te entregan?
├─ Assets sueltos de un producto (logo, capturas, grabaciones) ─→ Marketing (PRODUCCION §1–§8)
├─ Un guion comercial de la empresa ────────────────────────────→ Comercial (modelo: sofu-comercial)
├─ Una landing o un evento para redes (9:16, 12–35 s, con voz) ─→ Pieza corta ElevenLabs (§6)
│    ├─ Una pieza que se editará después en el Studio ──────────→ HyperFrames (yezid-envivo-pesv-autogestion, fegir-envivo)
│    └─ Campaña de N variantes de la misma pieza ───────────────→ Lienzo propio + config.js (yezid-envivo-premium)
├─ Un PDF/diapositivas SIN notas de orador
│    ├─ Quieren el módulo completo con voz ─────────────────────→ «Centro de mando» (§10)
│    └─ Quieren gancho corto para redes ────────────────────────→ «Ritmo» 16:9 + 9:16 (§13)
└─ Un PPTX CON notas de orador (curso)
     ├─ ≤ 15 láminas, cada una distinta ────────────────────────→ Lámina a lámina a mano (§14, ruta-segura)
     └─ Muchas láminas con anatomía repetida ───────────────────→ Curso generado (§15, moto / csm)
```

Regla práctica para el último caso: si al hojear el PPTX ves **menos de ~8 anatomías
distintas de lámina**, escribe plantillas; si cada lámina es única, escríbelas a mano.

---

### 3. El método de trabajo (vale para cualquier formato)

Estas nueve prácticas son las que más tiempo ahorraron. Ninguna depende de RiskMann.

1. **La fuente manda.** Nada entra al video —texto, cifra, norma, nombre de módulo— si no
   se rastrea a un archivo entregado. Cada frase de locución cita su fuente en el JSON.
2. **Muestra antes que módulo.** Construir solo la apertura (~15 s) **con sonido** y
   pedir el sí. Una muestra cuesta ~10 min; un módulo en la dirección equivocada costó
   ~1 h + 9 min de render, tres veces.
3. **La voz antes que la animación.** La duración de cada plano sale de la locución real
   (o de su medición), nunca al revés. Si no cabe, se acorta la frase, no el plano.
4. **Un documento de dirección antes de construir en paralelo.** `DIRECCION.md` (o
   `base.py` en los cursos generados) fija las constantes: posición del logo, retícula,
   paleta, tipografía. Es lo que permite que planos hechos por separado parezcan uno.
5. **Configuración, no código.** Voz, mezcla, pista rítmica y cursos enteros se describen
   en JSON; los scripts de `tools/` no cambian entre proyectos.
6. **Verificar con medición, no con el ojo del agente.** El agente no oye ni ve el MP4:
   `lint` + `check` + hoja de contactos + espectro de audio por bandas.
7. **Entregar en piezas.** Un video por módulo; piezas de 1–2 min cortadas en frontera
   de lámina; máster continuo solo si lo piden (`unir-curso.py`).
8. **Commit y push antes de renderizar, y nunca dentro de OneDrive.** OneDrive borró el
   repo en caliente y luego lo revirtió seis commits; lo único que se salvó fue lo que
   estaba en GitHub.
9. **Primero, de quién es el video.** La marca que firma (RiskMann, Yezid, FEGIR) decide
   paleta, tipografía, logo y dominio del CTA. Si la página y el manual no coinciden,
   se le plantea al cliente; no se mezcla mitad y mitad.

---

### 4. Las piezas reutilizables

#### 4.1 Herramientas compartidas (`tools/`, no cambian entre proyectos)

| Script | Entrada | Cuándo |
| --- | --- | --- |
| `voz.py` | `guion.json` | Voz local gratuita (Piper `es_ES-davefx-medium`); avisa si una línea no cabe |
| `descargar-voz.py` | — | Una vez por equipo: baja y verifica el modelo Piper |
| `ritmo.py` | `ritmo.json` | Pista rítmica sintetizada a un BPM, sin derechos de terceros |
| `mezcla.py` | `mezcla-*.json` | Voz + pistas + cama + **`musica` (con ducking bajo la voz)** + efectos, −16 LUFS; falla si la banda >400 Hz queda vacía. Admite versión de solo música (bus frontal vacío, sin ducking) |
| `nivelar-voz.py` | carpeta de tomas | Lleva el TTS (ElevenLabs sale a ~−33 dB) a nivel de emisión, **a disco**, antes de mezclar |
| `probar-voces.py` | una frase | La misma frase con varias voces, para que el cliente elija a ciegas |
| `render-partes.py` | carpetas de proyecto | Render por partes, reanudable, mata huérfanos |
| `cortar-laminas.py` | proyecto + `--piezas N` | Parte un módulo en piezas parejas en frontera de lámina |
| `unir-curso.py` | carpeta de módulos | Máster continuo sin recodificar |

#### 4.2 Plantillas de proyecto (se copian)

| Para | Copiar | Cambiar |
| --- | --- | --- |
| Módulo de formación con voz | `videos/pesv-m01-mando/` | `tools/guion.json`, tabla de tiempos de `DIRECCION.md`, planos 02–07 |
| Pieza corta al pulso | `videos/pesv-m01-ritmo/` | una frase por escena, `ritmo-video.json`, `mezcla-video.json` |
| Versión vertical | `videos/pesv-m01-ritmo-vertical/` | recomponer escenas (no escalar) |
| Curso lámina a lámina | `videos/ruta-segura-m1/` | `tools/eNN.py`; `base.py` se deja |
| Curso generado | `videos/csm-curso/` (el más reciente) | `datos/`, `base.py` (paleta), `plantillas.py`, `LIMITES` |
| Marketing | `npx hyperframes init` + receta `riskmann-hud` | ver PRODUCCION §6 — **ojo:** la receta no coincide con el manual oficial (§9) |
| Vertical RiskMann con ElevenLabs | `videos/riskmann-consulta-pesv-vertical/` | `SCRIPT.md`, `tools/narracion.json`, `SFX-CUES.md`, `tools/final-A.json` |
| Promo de evento (HyperFrames) | `videos/yezid-envivo-pesv-autogestion/` | `tools/narracion.json`, `--brand` del fondo `aurora-drift`, rejilla de tempo |
| Promo editable en el Studio | `videos/fegir-envivo/` | `compositions/escena-*.html` (ver su `EDITAR.md`); **no** volver a correr `tools/estudio.py` |
| Promo de landing generado desde la voz | `videos/riskmann-capacitaciones-promo/` | `GUION` y `ESCENAS` de `tools/construir.py`; `voz` → `musica` → `construir` |
| Serie de N variantes, editable en el Studio | `videos/fegir-recordatorios/` o `videos/riskmann-capacitaciones-serie/` | la lista `SERIE` de `serie.py`; `python serie.py voz` + `construir` (reescribe las N carpetas) |
| Campaña de variantes (lienzo propio) | `videos/yezid-envivo-premium/` | `js/config.js` (textos, colores y tiempos por variante) |
| Anuncios de una landing | `videos/riskmann-inspecciones-ads/` | `js/ads.js → SCRIPTS`, la URL fuente en `GUIONES.md` |

#### 4.3 Recetas y fragmentos que ya están resueltos

- **`@font-face` de Montserrat** con los dos `.woff2` (latin + latin-ext): en cualquier
  `base.py`. Sin él, el render sale con otra fuente en silencio.
- **Números a palabras en español** para TTS (`en_palabras`, `normalizar` en
  `moto-curso/tools/moto.py`): «2466» → «dos mil cuatrocientos sesenta y seis»,
  «60 km/h», «%», siglas deletreadas («P E S V»).
- **Sincronía automática voz→aparición** (`sincronia.py`): empareja cada elemento con la
  frase que comparte más raíces de 5 letras; orden preservado, separación mínima 0,55 s,
  reparto si no hay coincidencia. Reutilizable en cualquier idioma cambiando `VACIAS`.
- **Reparto óptimo en piezas** (`tramos` en `moto.py`, `cortar-laminas.py`): programación
  dinámica que minimiza la desviación de cada pieza a la duración objetivo.
- **`cronometro.py`** (ruta-segura): traduce las marcas de tiempo de una locución a otra
  — la voz sintética de aprobación se cambia por una humana sin tocar el montaje.
- **Grado de fotografía a una paleta**: `brightness(0.78) contrast(1.14) saturate(0.45)
  hue-rotate(-6deg)` + capa de marca en `multiply` ~0.40 + scrim local bajo el texto.
- **Receta de identidad** `riskmann-hud` en `~/.media/recipes/` — el patrón de congelar
  una estética para reusarla vale para cualquier marca nueva.

---

### 5. Pipeline del curso generado (moto / csm)

Es el formato más escalable y el único que aún no estaba documentado en
`PRODUCCION-VIDEOS.md` (ver §15 allí).

```
PPTX ──extraer──▶ datos/curso.json ──voz──▶ assets/voz/sNN.mp3 + datos/tiempos-voz.json
                                    │
                                    └──construir──▶ videos/<curso>-<clave>/ (index + compositions + partes)
                                                     │
                            tools/render-partes.py ◀─┘ ──▶ renders/parte-N.mp4 (mudos)
                                                     │
                                          montar ────┴──▶ renders/<curso>-<clave>-N.mp4 (voz pegada, verificada)
```

```bash
set ELEVENLABS_API_KEY=...
python videos/csm-curso/tools/csm.py voz m01          # locuta lo que falte, guarda tiempos por frase
python videos/csm-curso/tools/csm.py construir m01    # genera videos/csm-m01/
cd videos/csm-m01 && npx hyperframes lint && npx hyperframes check && cd ../..
python videos/csm-curso/tools/csm.py construir m01 --tramos   # después de validar: index-parte-N.html
python tools/render-partes.py videos/csm-m01
python videos/csm-curso/tools/csm.py montar m01       # pista por tramo + mux + comprobación de duración
```

**Piezas del generador:**

| Archivo | Responsabilidad |
| --- | --- |
| `datos/curso.json` | Una entrada por lámina: `n`, `formas` (texto por nombre de forma del PPTX), `notas`/`texto`, `frases` |
| `datos/guion-partes.json` (csm) | Narración escrita cuando las notas del PPTX solo anuncian la parte — armada con lo que la lámina muestra, sin añadir |
| `base.py` | Paleta muestreada del PPTX, fuentes, encuadre común, `envoltura()` de cada composición |
| `plantillas.py` | 6–7 plantillas; `elegir(d)` decide por la firma de nombres de forma (moto) o por número de lámina (csm) |
| `sincronia.py` | Instante de cada aparición según la frase que la nombra |
| `<curso>.py` | `LIMITES` (láminas por módulo), `voz`, `construir`, `montar`; filtra evaluaciones y preguntas |

**Decisiones que funcionaron:**

- Duración de lámina = `ANTES` (1,0 s) + narración + `COLA` (1,3 s).
- Sin locución, se estima: `0,068 s × caracteres + 0,374 s` por frase — el video se puede
  construir y revisar mudo antes de pagar voz.
- Las preguntas, autochequeos y evaluaciones **no van en el video**: se cortan de la nota
  (`PAUSA` regex) y van a la plataforma. Para csm se generó además el banco A/B/C
  (`datos/banco_preguntas.py` + `tools/banco_html.py`), con la fuente de cada pregunta.
- La voz va **fuera** del `index.html` y se pega al final: el render mudo cabe en 8 GB.
- `montar` rechaza el resultado si el video y su pista difieren más de 0,6 s.
- Paleta del PPTX, pero **Montserrat** en vez de Aptos/Arial (empaquetable), y el color
  claro de marca nunca como texto pequeño (se usa una variante oscura con ≥ 4,5:1).

---

### 6. Piezas cortas para redes con ElevenLabs (verticales, En Vivo, landings)

El formato que produjeron Alejandro y el equipo `fegir`: 12–35 s, 9:16, con locución
de ElevenLabs, efectos y música. El detalle técnico está en
[`ARRANQUE-EN-OTRO-EQUIPO.md`](#cap-8); aquí va lo que se reutiliza.

#### 6.1 Dos maneras de construirla

| | HyperFrames | Lienzo propio |
| --- | --- | --- |
| Proyectos | `riskmann-consulta-pesv-vertical`, `yezid-envivo-pesv-autogestion`, `fegir-envivo`, `fegir-recordatorios/*`, `riskmann-capacitaciones-promo`, `riskmann-capacitaciones-serie/*` | `yezid-envivo-15s`, `-campana[-v2]`, `-estudio`, `-premium`, `riskmann-inspecciones-ads` |
| Motor | `data-*` + GSAP, `npm run check` / `render` | HTML + GSAP + Three.js; `window.seekTo(t)` y `tools/render.mjs` (puppeteer-core + Chrome del sistema → ffmpeg) |
| Preview | `npx hyperframes preview` | `python -m http.server <puerto>` + `?ad=` / `?v=` |
| Cuándo | Una pieza que alguien seguirá editando en el Studio | Varias variantes de la misma pieza, o 3D/shaders que no caben en una composición |
| Ojo | El Studio reescribe archivos con la vista previa abierta | No tiene `lint`/`check`: la verificación es la hoja de contactos (`tools/snap.mjs`) |

Las dos siguen las reglas de determinismo de §8 (timeline pausada, sin `Math.random`
ni `repeat:-1`): el render busca por tiempo.

#### 6.2 La voz

- **Voz «Carlos»** (colombiana) `4PN5DHmrfIgZksvIrawS`. Dos perfiles aprobados:
  - Narrado, `eleven_multilingual_v2`: `stability 0.32–0.35 · style 0.45 · claridad 0.80`,
    velocidad por plano. Con 0.5 lee plano y apresurado.
  - Vendedor, `eleven_v3`: `stability 0.15 · style 0.78 · speed 1.03`; admite
    `[etiquetas]` de tono (en `multilingual_v2` se leerían en voz alta: quitarlas).
- **Siempre con timestamps por carácter** (`/with-timestamps`) y cada aparición sobre la
  palabra que la nombra; encadenar frases con `previous_text` / `next_text`; 3 tomas por
  frase y gana la más pausada que quepa.
- **Puntuación medida:** `…` = 0.64 s, la mejor pausa; `—` = 0.57 s; siglas deletreadas
  (`P-E-S-V`, o «pe e ese ve» en el texto) pasan de 0.49 a 0.95 s y se entienden; una
  palabra en MAYÚSCULAS por anuncio con `eleven_v3`; «vivo» nunca cierra frase.
- **El acento es propiedad de la voz**, no un parámetro. Y la misma frase dura
  6.5–9.9 s según la voz: cambiarla obliga a recolocar las animaciones.
- **Una sigla que suena distinta en cada frase:** escribirla con el nombre de las letras.
  Medido con la misma semilla en dos frases: «pe e ese ve» dura 0,75 / 0,76 s (igual en las
  dos) frente a `P-E-S-V` 0,62 / 0,56, `P.E.S.V.` 0,51 / 0,61 y `pe-e-ese-ve` 0,84 / 0,71
  (`fegir-envivo/tools/prueba-sigla.py`). Igual «pe de efe» para PDF.
- **Semilla fija** (`"seed": 20261003` en el cuerpo): el mismo texto da la misma toma. Con
  ella se regenera **solo** la frase que cambia (`voz-eleven.py … 1,3`, `serie.py voz
  carpeta:2`) y las demás siguen siendo las aprobadas.
- El cuerpo de la petición en **UTF-8 desde Python**: con `curl` y tildes, `400 invalid_unicode`.
- La clave se lee de `ELEVENLABS_API_KEY`, nunca se escribe en el repo.

#### 6.3 La mezcla

```bash
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14   # a disco, antes de mezclar
python ../../tools/mezcla.py tools/final-A.json                         # musica con ducking bajo la voz
```

- La música va en **`musica`**, nunca en `pistas`: `pistas` comparte `amix` con la voz y
  nada la aparta.
- **Margen voz–música frase por frase**, con los buses por separado
  (`tools/margen-voz.py`): la voz entre +7 y +25 dB sobre la música. Las piezas de
  campaña apuntan a 12–18 dB y −14 LUFS finales para redes.
- Ningún efecto encima de una palabra clave (el golpe del gancho se adelantó para que
  sonara «¿Seguro?»).
- **Música con licencia verificada para Reels/TikTok:** Pixabay y Mixkit sí; la
  Biblioteca de Audio de YouTube no (solo licencia videos alojados en YouTube). Ficha
  en `assets/musica-LICENCIA.txt`. Alternativa sin terceros: música generada con
  ElevenLabs (`sound-generation`), con el prompt guardado en `assets/musica/ORIGEN.txt`.

#### 6.4 Tiempos muertos: medirlos, no adivinarlos

```bash
ffmpeg -i video.mp4 -vf "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -
```

Por debajo de ~0.35 se lee como parada. Lo que más los quita: recortar cada plano a su
locución + una respiración, salidas con `power2.in` (no `expo.in`) y deriva continua del
contenido con `ease: "none"`. En la consulta PESV: de 44 ventanas muertas de 76 a 19 de 67.

#### 6.5 Identidad por marca

| Marca | Fuente | Claves |
| --- | --- | --- |
| RiskMann | `docs/marcas/riskmann/` (PDF oficial) | `#020202`, dorado `#c8951a`, cian `#06c7fb`; Dubai; caballero y dos anillos cian + dorado; pesos mezclados en una frase |
| Yezid Ricaurte | Manual de Yezid + `yezidricaurte.com` + correos | Petróleo `#001f26`, verde `#336666`, dorado `#d2b96a`, pálido `#f1ecb0`, botón coral `#f06e49` de los correos; firma oficial en negativo, **sin redibujar**; **sin rojo** (reservado para «peligro») |
| FEGIR | `docs/marcas/fegir/manual-identidad-fegir.pdf` + web de FEGIR | Verde `#45a035`, verde claro `#a8c875`, crema `#f1ecb0`; banda del manual `#50cd72 → #4ecd25` (muestreada); Segoe UI (la del manual); logo **extraído de los vectores del manual** (`docs/marcas/fegir/logos-extraidos/`); planos alternos verde/blanco y la foto de portada del manual en duotono; **nada de Yezid** |
| RiskMann · landing de Capacitaciones | La landing (decisión del cliente, 26-sep, **solo para esa landing**) | Negro `#040404`, dorado `#AC841D` (el botón empieza en él, nunca más claro), Montserrat + Open Sans; logo oficial; QR oficial → `app.riskmann.com/entrada` |

La ficha completa de cada marca está en [`marcas/<marca>/ficha.md`](marcas/).

- Los colores de un manual pensado para papel pueden no pasar contraste en pantalla
  (oliva `#80804a` = 1.75:1): variantes aclaradas **solo para texto**, el color de marca
  intacto en acentos.
- Dubai necesita `line-height` ≥ 1.5.
- En las piezas de Yezid, FEGIR no aparece en pantalla, y en las de FEGIR no aparece Yezid
  (ni su nombre, ni su web, ni su paleta): son dos entregas distintas del mismo evento. La
  versión FEGIR recoloreada sobre la de Yezid se rechazó el 26-sep por verse «dependiente».

---

### 7. Arrancar un proyecto nuevo — lista corta

1. **Carpeta de entrada:** documento fuente, manual de marca, logo oficial (PNG/SVG real),
   fotos o permiso de usar Pixabay, lista de lo prohibido. Sin cifras reales → sin cifras.
   **Y de quién es el video** (qué marca firma y a qué dominio manda el CTA).
   Repo clonado **fuera de OneDrive**.
2. **Elegir formato** con el árbol de §2 y **copiar la plantilla** de §4.2.
3. **Identidad:** muestrear los colores del documento (no a ojo), escribir `frame.md` /
   `DIRECCION.md` / `base.py`, copiar los `.woff2`.
4. **Voz:** decidir Piper (gratis, local) o ElevenLabs (`eleven_v3`, con timestamps). Que
   el cliente escuche 2–3 voces (`tools/probar-voces.py`): el agente no puede elegir por
   oído. Perfiles y puntuación ya medidos en §6.2.
5. **Muestra de ~15 s con sonido** → aprobación.
6. **Construir el resto** contra el documento de dirección; oleadas de 2 agentes máximo.
7. **Validar:** `lint` (0 errores) → `check` («Check passed») → `snapshot` en medios,
   reposos y ±0,1 s de cada corte → mirar la hoja de contactos. En lienzo propio no hay
   `lint`/`check`: hoja de contactos con `tools/snap.mjs` y medición de tiempos muertos (§6.4).
8. **Audio:** `mezcla.py` sin «FALLO»; tres bandas a pocos dB entre sí; con música, margen
   voz–música frase por frase (§6.3).
9. **Commit y push**, y luego **render** (por partes si > ~3 min o poca RAM) → copia
   liviana `ffmpeg -crf 24–26`; para redes, `loudnorm` a −14 LUFS sobre el MP4 final.
10. **Entregar:** nombres `NN - Serie - Módulo - Título (XmYY).mp4`, `LEEME.txt` con qué
    es cada archivo y qué está pendiente, `GUION-VOZ` si habrá regrabación humana.

---

### 8. Trampas — las diez que más costaron

La lista completa está en PRODUCCION §7 y GUIA-PROMPTS §5. Si solo lees diez:

| # | Trampa | Remedio |
| --- | --- | --- |
| 1 | Cifra o afirmación inventada para «llenar» | Regla de la fuente; preguntar antes de escribir el guion |
| 2 | Construir todo antes de mostrar nada | Muestra de 15 s con sonido |
| 3 | Fuente nombrada sin `@font-face` | `.woff2` en el proyecto, siempre |
| 4 | `Math.random`, `Date.now`, CSS `transition`, `repeat:-1`, estado en `onUpdate` | Todo `fromTo` explícito en una timeline pausada |
| 5 | Máscara más estrecha que la frase: recorta palabras sin aviso | `width: max-content` y revisar cada reposo en captura |
| 6 | `visibility = "visible"` en un hijo | `"inherit"` |
| 7 | Editar HTML con regex sobre el archivo entero | Generar el HTML desde Python (`base.py`), no parchearlo |
| 8 | Render entero de 11 min en 8 GB | Voz fuera, partes, lote reanudable, matar `ffmpeg` huérfano |
| 9 | Mezcla con buen promedio y sin voz audible | Medir por bandas (>400 Hz), no el promedio |
| 10 | `Set-Content` de PowerShell | Escribir archivos con Python o la herramienta de escritura (UTF-8) |

#### Las de las piezas cortas (ninguna da error: solo se ven en los fotogramas o se oyen)

La lista completa está en [`ARRANQUE-EN-OTRO-EQUIPO.md`](#cap-8) §2.

| # | Trampa | Remedio |
| --- | --- | --- |
| 11 | Música en `pistas`: tapa la voz 8–16 dB | Clave `musica` de `mezcla.py` (ducking) |
| 12 | TTS a −33 dB contra música a −14 dB | `nivelar-voz.py` a disco antes de mezclar |
| 13 | `loudnorm` dentro del `filter_complex`: devuelve silencio | Nivelar a disco; `loudnorm` solo sobre el archivo final |
| 14 | Ramas de audio de distinta duración en un `asplit`: 37 s tardan 7 min | Rellenar cada rama hasta la duración final antes de mezclar |
| 15 | `expo.in` en las salidas: se lee como tiempo muerto | `power2.in` |
| 16 | Elemento elevado a la raíz con `data-start` global: no se mueve con su plano | Al recolocar planos, auditar **todos** los `data-start` del `index.html` |
| 17 | Studio abierto mientras se escribe: añade `data-hf-id` y los anclajes dejan de coincidir | `npx hyperframes preview --stop` antes de escribir; anclar por `id` |
| 18 | Suprimir avisos del verificador en bloque (40 `content_overlap` eran ciertos) | Quitar las supresiones y ver si el error vuelve |
| 19 | Re-correr un generador de un solo uso (`fegir-envivo/tools/estudio.py`) | Borra lo editado en el Studio: después del primer uso, la fuente es `index.html` + `compositions/` |
| 20 | OneDrive borra o revierte el repo en caliente | Clonar fuera de OneDrive; commit y push antes de renderizar |
| 21 | `data-volume` > 1 en un `<audio>`: no sube la toma | Nivelar la toma **a disco** midiendo su LUFS y aplicando la ganancia exacta que falta |
| 22 | Curva `data-automation` generada con `max()`/solapes: puntos fuera de orden en el tiempo | Ordenar y comprobar (`assert`) antes de escribir; en huecos < 0,6 s la cama se queda baja |
| 23 | Texto dentro de un elemento girado (certificado inclinado): decenas de `content_overlap` falsos | Girarlo solo en la entrada; en reposo, derecho |
| 24 | Botón dorado con degradado que empieza más claro que `#AC841D`: 2,97:1 con blanco | Empezar en `#AC841D` y oscurecer hacia el otro extremo |
| 25 | Aparecer con fundido lento: `check` mide el contraste a medio fundido y falla | Aparecer de golpe (0,01 s) mientras el elemento se desplaza |
| 26 | Parche con `assert` que falla a medias y luego se corre la herramienta sin el parche: regeneró las 6 tomas | Parchear con el editor; copiar antes las tomas aprobadas; la fuente de verdad son las niveladas (`assets/mezcla/`) |
| 27 | `.gitignore` con `videos/*/…` no cubre las series anidadas (`videos/<serie>/<N>/`) | Patrones `videos/*/*/…` (ya añadidos) |

---

### 9. Huecos conocidos (para cerrar antes del próximo proyecto)

- **El extractor PPTX → `curso.json` no está en el repositorio.** Los `curso.json` de
  moto y csm existen, pero el script que los produjo no. Es la primera pieza a recuperar o
  reescribir (con `python-pptx`: nombre de forma → texto, notas → frases, medios → fotos).
- **La evaluación del curso de moto** (`Evaluacion-por-modulo.html`,
  `Preguntas-plataforma-Motociclista.xlsx`) se entregó sin su generador en el repo; el de
  csm sí está (`banco_html.py`, que además depende de un CSS de referencia externo).
- `moto.py` y `csm.py` son casi idénticos (≈90 % del código): el siguiente curso debería
  sacar lo común (`voz`, `construir`, `montar`, `tramos`, números a palabras) a `tools/` y
  dejar en cada curso solo `LIMITES`, `base.py` y `plantillas.py`.
- **Sala de control** sigue con el «100 %» sin fuente y el logo redibujado en los planos
  03 y 09: no usar comercialmente hasta corregir.
- **SOFU** (05, 06, 06b): faltan datos de contacto y validar el portafolio.

**De las piezas cortas (Alejandro y `fegir`):**

- **La receta `riskmann-hud` no corresponde al manual oficial** (`docs/marcas/riskmann/`), y
  `CLAUDE.md` la sigue recomendando para marketing nuevo. O se rehace contra el manual o
  se deja de recomendar.
- **El umbral del PESV está sin confirmar:** la landing dice «11 o más vehículos» y
  también «diez (10) unidades». La consulta PESV usa once. Confirmar cuál, y de qué norma
  sale, antes de dar la locución por buena.
- **La clave de ElevenLabs del issue #3 caducaba el 21-sep-2026**, y las locuciones no
  van en git: sin clave nueva no se regeneran.
- **La misma herramienta copiada en cada proyecto:** `tools/render.mjs` (seis proyectos) y
  `tools/audio.py` (cinco) viven copiados en cada proyecto de lienzo propio. Igual que
  con `moto.py`/`csm.py`, el siguiente proyecto debería sacarlos a `tools/`.
- ~~Logos de FEGIR sin origen confirmado~~ **Resuelto (26-sep):** el manual de FEGIR está
  en `docs/marcas/fegir/` y los logos se extrajeron de sus vectores (sin redibujar). En la
  versión blanca, el centro del escudo va al 50 % de opacidad, como se ve en el manual
  sobre verde: es lo único interpretado.
- **FEGIR:** confirmar que el cupo se reserva en `fegir.org` (se dedujo del nombre de la
  carpeta que entregó el cliente) y cuál es el enlace del grupo de WhatsApp del evento (los
  correos y la web de Yezid usan dos distintos).
- **RiskMann Capacitaciones:** las respuestas de las preguntas frecuentes de la landing no
  se capturaron (estaban cerradas): por eso ninguna pieza habla de precio ni de la validez
  del certificado.
- **La clave de ElevenLabs actual** no tiene los permisos `music_generation` ni
  `user_read`: la música sale de `sound-generation` en bucle.
- **Varias variantes de la campaña de Yezid** (`-campana`, `-campana-v2`, `-estudio`,
  `-premium`, `-15s`) conviven sin un documento que diga cuál se aprobó. Anotarlo en un
  `LEEME` o retirar las descartadas.
- **El storyboard «LANDING INSPECCIONES GRATIS»** no está en el repo ni en el Drive: los
  anuncios siguen el texto de la landing. Si el storyboard trae frases literales, cambiar
  `js/ads.js → SCRIPTS`.
- **Fuentes Segoe UI** (`fegir-envivo*/assets/fonts/segoeui*.ttf`) son de Microsoft y
  están en el repo: confirmar licencia o cambiar a una libre (Montserrat ya está).
- **`Documentos_contexto/`** (correos de la campaña, con datos personales) vive fuera del
  repo a propósito: quien retome las campañas de Yezid lo necesita aparte.
- **La voz de RiskMann sigue sin decidir** entre siete muestras (`ENTREGABLES-VIDEO\pruebas-de-voz`).

---

<a id="cap-6"></a>

## 6. Estándar de producción

> Fuente: [`PRODUCCION-VIDEOS.md`](../PRODUCCION-VIDEOS.md) — se edita ahí, no aquí.

> Estándar de producción de los videos RiskMann. Cubre **dos formatos**, ambos
> verificados contra proyectos reales renderizados (septiembre 2026):
>
> | Formato | Para qué | Proyecto de referencia | Secciones |
> | --- | --- | --- | --- |
> | **Marketing** | Presentar la plataforma o un módulo a quien compra | `videos/riskmann-sala-de-control/` (68 s) | §1–§8 |
> | **Capacitación «Centro de mando»** | Módulos de formación (serie PESV «Pasajero seguro»), con voz | `videos/pesv-m01-mando/` (151 s) — **aprobado por el cliente** | §10–§12 |
> | **Capacitación «Ritmo»** | El mismo módulo como pieza corta de gancho, al compás de una pista, sin voz | `videos/pesv-m01-ritmo/` (60 s) — **aprobado por el cliente** | §13 |
>
> Los valores son los que realmente se usaron y renderizaron, no recomendaciones
> genéricas. Los prompts para pedir cada cosa están en [`GUIA-PROMPTS.md`](#cap-7).
>
> **Para quién:** cualquiera —persona o agente— que vaya a producir el siguiente video.
> Un agente que abra este repositorio debe leer este archivo antes de escribir una sola
> línea de composición.

---

### 0. La regla que manda sobre todas las demás

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**

En el primer video esta regla no existía y el resultado lo demostró: la pieza afirma
**«100% · TRAZABILIDAD DEL REGISTRO»**, una cifra que no sale de ningún dato de la
empresa. Se inventó porque el material de entrada no traía datos y el guion necesitaba
un número. Ese es exactamente el fallo que este manual existe para impedir.

Antes de aprobar un guion, aplica la prueba a **cada frase en pantalla**:

| Pregunta | Si la respuesta es no |
| --- | --- |
| ¿Esta frase está en un archivo que me dieron? | Bórrala o pide que te la aprueben por escrito. |
| ¿Esta cifra viene de un dato real de la empresa? | Bórrala. Sin excepción. |
| ¿Este nombre de módulo/submódulo aparece en la app o en los assets? | Usa el nombre que sí aparece. |
| ¿Esta afirmación de cumplimiento normativo la firmó alguien de RiskMann? | Bórrala. |

Un video puede ser espectacular sin afirmar nada falso. Lo que lo vuelve espectacular es
el montaje, el movimiento y el producto real en pantalla — no los adjetivos.

**Distingue concepto de funcionalidad.** «Sala de control» es un *concepto visual* (el
HUD azul con retícula y escuadras). No es un módulo de RiskMann y el video nunca debe
sugerir que lo sea. Los módulos reales son los que tienen icono en la portada de la
plataforma.

#### 0.1 El manual de marca manda sobre el diseño

El logo de RiskMann tiene manual propio y no se negocia en ningún plano:

| Permitido | Prohibido |
| --- | --- |
| Usar **solo los archivos oficiales**: `riskmann_logo_blanco.png` (lockup *RiskMann by SOFU*, 840×280) y `riskmann_icono_blanco.png` (isotipo) | Redibujar, trazar o vectorizar el logo a mano |
| Escala **uniforme**, opacidad, traslación | Re-letrar el nombre con otra tipografía |
| Revelar el archivo completo con `clip-path` | Recolorear, deformar (escala no uniforme), rotar |
| Dejar libre su área de reserva (en el formato de capacitación: **44 px** alrededor de la tinta a 280 px de ancho) | Poner cualquier cosa encima o dentro de la reserva |

Dato útil: en `riskmann_logo_blanco.png` el isotipo ocupa x 35–215 y el nombre x 236–818.
`clip-path: inset(0 73.9% 0 0)` muestra **solo el isotipo** sin tocar el archivo.

> **Caso real:** los planos 03 y 09 de *Sala de control* redibujan el isotipo y re-letrean
> el nombre. Ese video incumple el manual y está pendiente de corrección (§9). El formato
> de capacitación nació ya cumpliéndolo.

#### 0.2 Sin figuras humanas dibujadas

Monigotes y siluetas de línea fueron **rechazados por el cliente** («muy básicos y poco
profesionales»). Las personas aparecen solo en fotografía real — y sin caras
reconocibles, matrículas legibles ni logos de terceros (§10.4).

---

### 1. Qué hay que entregar antes de empezar

Ninguna producción arranca sin esto. La calidad del video está limitada por la calidad
de esta carpeta.

#### 1.1 Ficha del módulo (obligatoria)

Un archivo de texto, `BRIEF-MODULO.txt`, con:

- **Módulo** y su nombre exacto tal como aparece en la plataforma.
- **A quién le habla el video**: al que compra (gerencia, HSEQ) o al que lo usa
  (conductor, coordinador). Cambia el vocabulario entero.
- **Los submódulos reales**, con su nombre exacto.
- **La copia aprobada**, si existe. Si la entregas, el video la usa *literal* — se
  reparte en planos, no se reescribe.
- **Cifras reales**, con su fuente. Si no hay, se dice: *no hay cifras* — y el video se
  construye sin ninguna.
- **La lista de lo prohibido**: normativas que no se pueden mencionar, promesas de
  cumplimiento que legal no aprueba, datos personales que no pueden salir en pantalla.

#### 1.2 Grabaciones del módulo (lo que hace la diferencia)

Es el material más valioso y el más fácil de arruinar. **2 a 4 clips**, uno por paso del
flujo. Ejemplo para Inspecciones: crear inspección → llenar el formato → firmar →
informe generado.

| Regla | Por qué |
| --- | --- |
| 1920×1080, pantalla completa | El lienzo del video es 1920×1080; cualquier otra cosa se escala y pierde nitidez. |
| Sin barra del navegador, sin pestañas, sin notificaciones | El manual de composición prohíbe cromo de navegador en cuadro. |
| 10–20 segundos por clip | Más largo no cabe en un plano de 7–8s; hay que recortar y siempre se recorta mal. |
| Un solo paso por clip | Un clip largo con cuatro pasos no se puede repartir entre planos. |
| Cursor **lento**, con pausa antes de cada clic | Un movimiento apurado no se puede ralentizar sin que se vea a saltos. |
| Datos de demo, nunca reales | En el primer video salió una cédula legible en el carnet. No debe repetirse. |
| Sin zoom del navegador, al 100% | El zoom rompe la escala tipográfica del producto. |

Guárdalos en `assets/videos/` o en una carpeta que me indiques.

#### 1.3 Capturas de pantalla

Para lo que no se mueve: pantallas de resultado, informes, certificados. PNG a resolución
nativa, sin recortar el cromo a mano.

#### 1.4 Si el módulo tiene URL pública

Entonces no hace falta nada de lo anterior en su forma manual: el marco tiene captura
automática, que baja capturas reales, el texto del DOM y los colores de marca.

```bash
npx hyperframes capture "https://url-del-modulo" -o ./capture
```

Esto es lo que **no** se pudo hacer en el primer video (no había URL), y por eso el
inventario de assets se escribió a mano. Con captura real, la copia del video sale del
texto que ya está en el producto.

---

### 2. Identidad visual — valores verificados

Estos son los tokens reales de `frame.md` del primer video. **No los reinventes**: la
serie solo se ve como serie si todos los videos comparten exactamente estos valores.

#### 2.1 Paleta

| Token | Valor | Uso |
| --- | --- | --- |
| `bg` | `#051427` | El suelo de todos los planos. Nunca negro puro. |
| `surface` | `#0C2B53` | Panel del centro de mando. |
| `surface-2` | `#0F396B` | Panel secundario, elevaciones. |
| `primary` | `#E6423C` | **El acento de foco. Uno por plano, nunca dos.** |
| `accent-2` | `#8E8FC4` | Lavanda. Solo cromo estructural: retícula, hairlines, escuadras, etiquetas de telemetría. Jamás compite con el rojo. |
| `text` | `#F2F7FF` | Titulares. |
| `text-muted` | `#A7BCCC` | Cuerpo y apoyo. |
| `text-light` | `#5D7793` | Terciario. |
| `border` | `rgba(142,143,196,0.28)` | Contorno de panel, 1.5px. |
| `card-bg` | `rgba(226,236,248,0.05)` | Relleno de tarjeta. |
| `grid` | `rgba(142,143,196,0.14)` | La retícula del HUD. Siempre bajo el 15%. |
| `glow` | `rgba(230,66,60,0.35)` | Halo rojo del elemento en foco. Uno por escena. |
| `positive` / `negative` | `#3DD68C` / `#E6423C` | Solo texto, sin relleno. |

**Elevación por contorno, nunca por sombra.** No hay una sola sombra difusa en la serie:
un panel se separa del fondo por su contorno de 1.5px y su relleno, no por un blur.

#### 2.2 Las constantes del HUD (críticas para la continuidad)

Todos los planos que llevan HUD usan **exactamente** estos números. Nueve planos
construidos por nueve agentes distintos se ven como un solo centro de mando solo porque
estos valores se les entregaron como constantes:

```
Retícula:   paso 60 × 60 px, líneas de 1px, color rgba(142,143,196,0.14)
Escuadras:  4 marcas en L, brazos de 128px, trazo de 2px,
            color #8E8FC4 al 0.6 de opacidad, sangrado 56px desde cada borde
```

**El ciclo del HUD a lo largo de un video:**

1. El plano de apertura y el de dolor van **sin HUD** — es el mundo antes de la plataforma.
2. El plano de producto **enciende** el HUD: la retícula se dibuja de dentro hacia fuera,
   las escuadras entran una tras otra.
3. Los planos intermedios lo llevan **estático desde t=0**, sin animarlo.
4. El plano de cierre lo **retira** de fuera hacia dentro.

Ese arco es lo que convierte una lista de planos en una película.

#### 2.3 Tipografía

**Montserrat**, la familia de la plataforma. Los `.woff2` están en
`videos/riskmann-sala-de-control/assets/fonts/` — cópialos a cada proyecto nuevo.

```css
font-family: "Montserrat", sans-serif;
```

**Regla dura:** toda fuente nombrada necesita su `@font-face` apuntando a un archivo real
dentro del proyecto. La máquina de render es un Chrome headless limpio, sin fuentes
instaladas: nombrar «Montserrat» sin el archivo hace que el MP4 salga con una genérica y
toda la tipografía cambia sin avisar. En el primer video esto se detectó tarde y hubo que
descargar la familia y parchear los nueve planos.

El peso y el tamaño hacen el trabajo de jerarquía: display 700–800, cuerpo 400,
etiquetas de cromo en mayúsculas con `letter-spacing` amplio.

#### 2.4 Lista negativa

Nunca aparecen: barras de navegación, pies de página, scrollbars, cromo de navegador,
cursores del sistema, degradados morados de «IA», bokeh flotante, sombras difusas, ni
formas decorativas genéricas que sustituyan un asset real.

---

### 3. Estructura narrativa

#### 3.1 El arco que funcionó

**BAB** — *antes → adelanto del después → puente/producto → recorrido → wow → cierre*.
Para un video de un solo módulo, la versión reducida es de **6 planos, ~45s**:

| # | Rol | Duración | Qué hace |
| --- | --- | --- | --- |
| 01 | `hook` | 7s | El dolor concreto de ese módulo, en el lenguaje del cliente. |
| 02 | `product_intro` | 7s | El HUD enciende, el módulo se nombra. |
| 03 | `feature_showcase` | 8s | El flujo real, con la grabación del módulo. |
| 04 | `feature_showcase` | 8s | El segundo paso del flujo, o los submódulos. |
| 05 | `benefit_highlight` | 7s | Lo que cambia — **solo con frases aprobadas**. |
| 06 | `branding` | 8s | Los paneles se van, el logo se arma, cierre *by SOFU*. |

Para un video general de plataforma, la versión completa es la de 9 planos y 68s del
primer video.

#### 3.2 Duraciones

**7 u 8 segundos por plano.** No menos: un plano de 5s no alcanza a revelar y sostener.
No más: a partir de 9s hay que inventar movimiento para rellenar, y el movimiento
inventado es el que se ve barato.

#### 3.3 Transiciones

Un juego corto, repetido:

- `crossfade` **0.5s** — el caso normal, entre planos del mismo mundo visual.
- `zoom-through` **0.4s** — solo en frontera de sección (dolor → producto, módulo → beneficio).
- `push-slide` — como mucho una vez por video, entre dos planos de función consecutivos.

Las inyecta el marco; no se escriben a mano.

#### 3.4 El ritmo de revelado (lo que separa un video de una presentación)

**Ningún plano vuelca su contenido en el primer 25%.** El fallo clásico es dibujar todo
en la entrada y luego congelar: eso se lee como diapositiva.

- En t=0 entra **una sola pieza**.
- Cada pieza siguiente aparece **cuando su cue la nombra**, repartidas por todo el plano
  y sobre todo en la segunda mitad.
- El plano termina **sostenido y quieto**. Prefiere quietud a movimiento malo.
- Durante una sostenida solo se permite jitter de baja amplitud o internos de SVG vivos.
  **Nada de respirar** (escalar en bucle) ni de paneos lentos en la mitad final: molestan
  a la vista y son el tic más reconocible del video hecho por máquina.

Sin locución, el reloj del revelado son los **cues de texto en pantalla**. Con locución,
es la voz.

#### 3.5 Curvas

`power3` por defecto — cola larga, asentamiento suave. **Nada rebota.** `back.out`,
`bounce.out` y `elastic.out` están prohibidos como entrada por defecto; el rebote es el
delator número uno de un video generado.

---

### 4. Catálogo de planos — qué forma para qué beat

El marco trae 22 formas probadas («blueprints»). Estas son las que se usaron y funcionaron:

| Beat | Forma | Cómo se usó en el primer video |
| --- | --- | --- |
| Gancho tipográfico | `kinetic-type-beats` | Línea fija con un hueco que cambia por corte seco; termina tachada en rojo. |
| Dolor por acumulación | `overwhelm-surround` | Fichas de trámite cerrando desde los cuatro bordes sobre una silueta quieta. |
| Producto / cierre de marca | `logo-assemble-lockup` | Las fichas se rompen en enjambre 3D y arman el isotipo. |
| Enumerar módulos | `grid-card-assemble` | Cuatro paneles en cascada, uno pasa al frente y el resto se desenfoca. |
| Producto real en pantalla | `device-surface-showcase` | El carnet QR como héroe, con barrido de escaneo y submódulos enganchados. |
| El dato en movimiento | `video-text-pivot` | Tres grabaciones reales, luego la pantalla central cede el hueco a una cifra. |
| Recorrer muchos submódulos | `spatial-pan-stations` | Paneo lateral por 7 estaciones sobre un lienzo de 9600px. |

**Varía las formas.** Repetir la misma en todos los planos recrea exactamente la monotonía
que el catálogo existe para evitar.

---

### 5. Reglas técnicas duras

Estas rompen el render o la validación. No son estilo.

#### 5.1 Determinismo

El render avanza cuadro a cuadro haciendo *seeks*, no reproduce en tiempo real:

- Una sola línea de tiempo **pausada** por composición, registrada en `window.__timelines`.
- Entradas con `fromTo` y estado inicial explícito. Nunca tweens relativos (`+=`).
- **Prohibidos** `Math.random()` y `Date.now()`. Toda variación se deriva del índice del
  elemento.
- **Prohibidos** `repeat: -1` y `yoyo`. Cualquier "vida" es un tween finito.
- **Prohibidas** las animaciones CSS (`transition`, `@keyframes`): corren con el reloj del
  navegador, se desincronizan del seek y parpadean.

#### 5.2 Solo transformaciones

Anima `x`, `y`, `scale`, `opacity`, `rotate` y propiedades de pintura. **Nunca** `width`,
`height`, `top`, `left` — ni `letterSpacing`.

> Caso real: el plano 08 animaba `letterSpacing` para el colapso de interletraje. El
> validador lo rechazó: esa propiedad refluye el texto y encaja los glifos en píxeles
> enteros, así que tiembla bajo el motor de captura. Se arregló partiendo la frase en
> glifos y animando la `x` de cada uno — mismo efecto, sin temblor.

#### 5.3 Video: siempre en la raíz, nunca dentro de un plano

Los `<video>` van en `index.html` como clips de nivel raíz, con sus coordenadas absolutas.
El ensamblador **rechaza** un `<video>` dentro de una sub-composición.

Consecuencia de diseño: como el video queda clavado a coordenadas fijas del lienzo, **su
marco no puede moverse ni escalar mientras el clip está abierto**. Si el plano necesita
mover el panel, hazlo después de que la ventana del video cierre.

Patrón que funcionó: el plano dibuja el monitor (marco `surface` + contorno) y debajo una
**pantalla en reposo permanente** (gradiente oscuro + scanlines), para que cuando el clip
cierre el monitor nunca muestre un agujero.

```html
<video id="v-graficas" class="clip" src="assets/graficas.mp4"
       data-start="37.42" data-duration="3.2" data-track-index="7"
       style="position:absolute; left:528px; top:192px; width:864px; height:472px;
              object-fit:cover; border-radius:8px"
       preload="auto" muted playsinline></video>
```

`data-start` es global (tiempo del video completo), no local al plano.

#### 5.4 Zona libre inferior

El **17% inferior** del cuadro (por debajo de y≈896) queda libre de contenido importante
en todos los planos, lleven subtítulos o no. Es consistencia de borde para toda la serie.

#### 5.5 Densidad

El elemento principal ocupa **≥40%** del lienzo. Mínimo **3 capas** de profundidad (fondo
+ medio + frente). Nada de un grupo pequeño flotando en vacío. Prueba de entrecerrar los
ojos: tras el desenfoque todavía se distingue cuál es el elemento número uno.

---

### 6. El procedimiento

#### 6.1 Crear el proyecto

Cada video es su propio proyecto dentro de `videos/`:

```bash
cd riskmann2-marketing-videos
npx hyperframes init "videos/riskmann-<modulo>" --non-interactive --example=blank \
    --skill=product-launch-video
```

#### 6.2 Adoptar la identidad ya congelada

La estética del primer video está guardada como receta, disponible para cualquier
proyecto nuevo:

```bash
node ~/.claude/skills/media-use/scripts/recipe.mjs list --hyperframes . --json
node ~/.claude/skills/media-use/scripts/recipe.mjs use  --hyperframes . --name riskmann-hud
```

Esto trae el `frame.md` completo (paleta, tipografía, componentes) y los esqueletos de
guion. **Ahorra todo el paso de diseño** y garantiza que el video nuevo pertenezca a la
misma serie. Después copia `assets/fonts/` del primer proyecto.

#### 6.3 Preparar los assets

Los archivos que va a nombrar el guion se ponen primero en `capture/assets/` (los videos
en `capture/assets/videos/`), y luego se montan:

```bash
node ~/.claude/skills/product-launch-video/scripts/stage-assets.mjs \
     --storyboard ./STORYBOARD.md --hyperframes .
```

Solo se monta lo que el guion nombra. Debe reportar `staged N/N` — cualquier faltante
significa que un plano va a pedir un archivo que no existe.

#### 6.4 Construir, ensamblar, validar

```bash
node ~/.claude/skills/product-launch-video/scripts/frame-packets.mjs --project "$PWD" --storyboard "$PWD/STORYBOARD.md"
# … se construye un plano por agente, en paralelo …
node ~/.claude/skills/product-launch-video/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
node ~/.claude/skills/product-launch-video/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
npx hyperframes lint      # debe dar 0 errores
npx hyperframes check     # lint + runtime + layout + movimiento + contraste
npx hyperframes snapshot --at <puntos medios y ±0.1s de cada corte>
```

**Revisa la hoja de contactos antes de renderizar.** Ahí se detectan los planos vacíos y
los saltos entre cortes. En el primer video eso salvó la producción: el plano 06 aparecía
en negro y no se habría notado hasta ver el MP4 terminado.

#### 6.5 Renderizar

```bash
npx hyperframes render --skill=product-launch-video --quality high --output renders/video.mp4
```

Referencia de tiempo: 68s a 1080p tardaron **4m 44s** y pesaron **15.9 MB**.

---

### 7. Trampas encontradas en la primera producción

Documentadas para que no cuesten tiempo dos veces.

| Trampa | Qué pasa | Cómo evitarla |
| --- | --- | --- |
| **Paquete de instrucciones muy grande** | El constructor de paquetes falla con «packet is 58762 bytes (limit 48000)» cuando un plano cita demasiadas recetas de movimiento. | Con una forma grande (`kinetic-type-beats`, `logo-assemble-lockup`, ~27–29 KB), cita como máximo **2 o 3 recetas**. Las demás se describen en prosa y el agente las abre desde `RULES_DIR`. |
| **Editar HTML con expresiones regulares** | Un patrón `<video ...>` coincidió primero dentro de un **comentario** y borró 4 KB de marcado. El plano salió en negro. | Nunca borres bloques HTML con regex sobre el archivo entero. Y **siempre** vuelve a sacar capturas después de editar a mano. |
| **Fuente sin archivo** | Nombrar una familia sin `@font-face` hace que el MP4 salga con otra tipografía, en silencio. | Copia `assets/fonts/` a cada proyecto y declara el `@font-face` en cada plano. |
| **Assets de marca inservibles** | `riskmann_logo_central_blanco.svg` resultó ser una ilustración a color de 250×300, no un logotipo blanco. | Para cierre en fondo oscuro usa **`riskmann_logo_blanco.png`** (el lockup real *RiskMann by SOFU*) y **`riskmann_icono_blanco.png`** (el isotipo). |
| **Iconos sobre fondo claro** | Los `.webp` de módulo son ilustraciones sobre fondo blanco; puestos directamente sobre el azul se ven sucios. | Siéntalos dentro de una tarjeta `surface` redondeada. |
| **Grabaciones con bandas negras** | Las tres grabaciones de UI traen sus propias bandas negras (son capturas verticales). | Grabar en 16:9 desde el principio, o aceptar el reencuadre. |
| **Tiempo de espera de navegación** | `check` falla intermitentemente con «Navigation timeout of 10000ms» cuando el proyecto carga muchos MB de video. | No es un error del proyecto: vuelve a correr `check`. |
| **Contraste bajo** | Etiquetas de cromo lavanda sobre azul quedan cerca de 3.9:1. | Para texto que se debe leer, sube a `text-muted` (`#A7BCCC`). El cromo decorativo puede quedarse abajo. |

Trampas añadidas en la serie PESV (formato de capacitación):

| Trampa | Qué pasa | Cómo evitarla |
| --- | --- | --- |
| **`visibility = "visible"` en un hijo** | Un `visible` explícito atraviesa el ocultamiento del plano: los glifos de la etiqueta del plano 01 seguían vivos debajo de los planos 02–07. Solo lo delató `check` («texto tapado» en el plano 04). | Revelar con `visibility = "inherit"`. Y **nunca** animar `visibility`/`display` de un elemento `clip` (se usa `opacity`). |
| **Máscara más estrecha que su frase** | Recorta palabras en silencio: desapareció «aumentar» del principio clave y cambió el sentido. Ni `lint` ni `check` lo ven. | Dimensionar cada máscara al texto real (`width: max-content`) y revisar **cada plano en reposo** con capturas. |
| **Mayúsculas acentuadas asomando** | La tilde de «Ó» o «Í» asoma por encima de la máscara antes del revelado. | Empezar el revelado en `yPercent: 150`, no 110. |
| **Falsos solapes con máscaras** | `check` da decenas de `content_overlap`: mide el texto oculto sin el recorte. | Mirar esos instantes, y declarar **solo** esos elementos con `data-layout-allow-overlap`. Luego revisar el reposo. |
| **Espacios en glifos `inline-block`** | Se colapsan: «CAPACITACIÓNPESV». | Espacio duro en cada celda de espacio: escribir `"\u00A0"` en el código (un espacio duro literal se ve igual que uno normal y se pierde al copiar). |
| **Foto sobregradada** | Brillo 0.5 + multiply 0.82 + velo global: la foto desaparece, queda azul plano. | Grado de §10.4 y un **scrim local** solo bajo el texto. |
| **Voz más corta que el plano** | 04 estaba pensado a 30 s y su voz duraba 9.6 s: 17 s de cola muerta. | Generar la voz **antes** de fijar duraciones (§11). |
| **Muchos constructores en paralelo** | Los límites de uso los cortan a medias y dejan archivos parciales. | Oleadas de 2; revisar el disco antes de relanzar. |
| **Estado guardado en `onUpdate`** | El renderizador salta en el tiempo y, al retroceder, ese callback no se ejecuta: el rodillo del formato «Ritmo» mostraba «REDUCIR» cuando tocaba «AUMENTAR». | Cada paso como `fromTo` explícito sobre la propiedad real; un desenfoque SVG se anima con `attr: { stdDeviation }`, no con un proxy. |
| **Lo invisible sigue contando** | `check` no entiende `backface-visibility` ni el recorte de `overflow: hidden`: la cara oculta de una tarjeta 3D y las palabras del rodillo fuera de la ventana dieron decenas de errores de solape y contraste. | Hacer invisible de verdad lo que no se ve: `opacity: 0` a la cara oculta en el medio giro, y a cada palabra del rodillo cuando sale de la ventana. |
| **Posiciones calculadas a ojo** | Anchos de palabras estimados → dos píldoras se montaron. | Que la fila la ordene flexbox y animar desde el lugar natural de cada elemento (`x: 0, y: 0` como destino). |
| **Texto decorativo auditado** | Números o cintas de fondo solo contorno (`color: transparent`) fallan «texto sin pintar» y contraste. | Marcarlos con `data-layout-ignore` (y `aria-hidden`). No forzarles contraste: son fondo. |
| **Graves que se comen la mezcla** | Con bombo e impactos, la subgrave se llevaba la normalización y los agudos quedaban 16 dB abajo. | `"pasa_altos": 90` en el JSON de mezcla; medir tres bandas (<120, 120–400, >400 Hz) y buscar que queden a pocos dB entre sí. |
| **Bloque del catálogo con su propia duración** | Cada bloque instalado lee su `data-duration` interno, no la del montaje: la foto del bloque de partículas se apagaba a mitad de escena aunque el hueco durara 8 s. | Editar `data-duration` y `data-composition-duration` dentro del archivo instalado. |
| **Variables de un bloque que chocan con los tokens de color** | La variable `accent` del bloque define `--accent`, así que elegir «blue» pintaba el azul puro de CSS en vez del de marca. | Fijar los colores de marca directamente en el archivo del bloque (es un archivo del proyecto desde que se instala). |
| **El bloque mide el texto con otro grosor** | El bloque calculaba el ancho con peso 600 mientras la hoja de estilos lo pintaba en 900: la frase se salía del cuadro. | Igualar el peso de la medición al que se ve. |
| **Amarillo (u otro color claro) como texto sobre fondo claro** | `#F9B410` sobre gris claro da 1.6:1; ilegible y `check` lo marca. | El color claro va en formas (pastillas, barras, subrayados) con tinta oscura encima; para texto, un tono oscuro de la marca. |
| **MP4 > 30 MB** | No se puede enviar por la sesión. | Copia de vista: `ffmpeg -crf 24` (el módulo 01 quedó en 11.4 MB). |
| **Escribir con `Set-Content`** | Corrompe los acentos. | Escribir archivos con Python o la herramienta de escritura. |

---

### 8. Lista de verificación antes de entregar

**Veracidad**

- [ ] Cada frase en pantalla se rastrea a un archivo entregado por RiskMann.
- [ ] No hay ninguna cifra sin fuente.
- [ ] No hay afirmación de cumplimiento normativo sin aprobación escrita.
- [ ] Los nombres de módulos y submódulos son los de la plataforma.
- [ ] Ningún dato personal real es legible en pantalla.
- [ ] Cada frase de la **locución** también se rastrea a la fuente (`tools/guion.json` la cita).
- [ ] El pie legal del cierre está presente y legible (formato de capacitación).

**Marca**

- [ ] El logo es el archivo oficial; ningún plano lo redibuja, re-letra, recolorea ni deforma.
- [ ] Nada invade su área de reserva.
- [ ] Ninguna figura humana dibujada; fotos sin caras reconocibles.

**Audio**

- [ ] `mezcla.py` terminó sin «FALLO» (banda de voz por encima de −40 dB).
- [ ] En el MP4 final: `highpass=f=400,volumedetect` da una media razonable (módulo 01: −22.9 dB).

**Técnica**

- [ ] `npx hyperframes lint` → 0 errores.
- [ ] `npx hyperframes check` → «Check passed».
- [ ] Hoja de contactos revisada: ningún plano vacío, ningún salto en los cortes.
- [ ] Los `.woff2` están en `assets/fonts/` y cada plano declara su `@font-face`.
- [ ] Los `<video>` están en `index.html`, no dentro de un plano.
- [ ] El 17% inferior está libre en todos los planos.

**Serie**

- [ ] Retícula a 60px y escuadras a 56px de sangrado, con los valores de §2.2.
- [ ] Un solo acento rojo por plano.
- [ ] El HUD enciende, persiste y se retira según §2.2.
- [ ] Las formas de plano varían; ninguna se repite en todos.

---

### 9. Estado actual de la serie

| Video | Estado | Ruta |
| --- | --- | --- |
| RiskMann · Sala de control (general, 68 s) | Renderizado, con y sin narración — **contiene copia inventada (§0) e incumple el manual de marca (§0.1)** | `videos/riskmann-sala-de-control/` |
| **PESV M01 «Centro de mando»** (151 s) | **Renderizado y aprobado. Es la plantilla de la serie.** | `videos/pesv-m01-mando/` → `renders/pesv-m01-mando.mp4` |
| PESV M01 base (réplica de diapositivas) | Referencia de contenido — fuera del repo | archivo local del equipo |
| PESV M01 «plus» | Rechazado (seguía siendo diapositiva; monigotes) — fuera del repo | archivo local del equipo |
| PESV M01 refactor fotográfico | Superado («muy básico») — fuera del repo | archivo local del equipo |
| **PESV M01 «Ritmo»** (60 s) | **Renderizado y aprobado.** Pieza corta sin voz. | `videos/pesv-m01-ritmo/` → `renders/pesv-m01-ritmo.mp4` |
| **PESV M01 «Ritmo» vertical** (60 s, 9:16) | **Renderizado.** Para TikTok / Reels / Shorts. | `videos/pesv-m01-ritmo-vertical/` |
| **SOFU BIC S.A.S. · comercial** (68 s) | **Renderizado.** Pieza de la casa matriz, desde su propio guion. Pendiente: datos de contacto y validación del portafolio. | `videos/sofu-comercial/` |
| PESV M01 «Profundidad» 16:9 y 9:16 | Exploración técnica: partículas por GPU y 3D con cámara. Apertura aprobada; escenas 3–7 sin construir. | `videos/pesv-m01-profundidad/` · `-vertical/` |
| PESV M02–M08 | Por hacer, con §10 (y §13 para su pieza corta) | — |
| Presentación anterior (12 s) | Del equipo, previo | `video-presentacion/` |

**Pendiente en el primer video:** sustituir «100% · TRAZABILIDAD DEL REGISTRO», revisar
las frases de §0, y rehacer los planos 03 y 09 con el archivo oficial del logo antes de
que la pieza se use comercialmente.

**Receta de identidad:** `riskmann-hud`, congelada en `~/.media/recipes/riskmann-hud`.

---

### 10. Formato de capacitación — «Centro de mando»

La dirección aprobada para la serie PESV después de tres intentos. Lo que el cliente
rechazó es tan útil como lo que aprobó:

| Intento | Veredicto del cliente | Lección |
| --- | --- | --- |
| Réplica de las diapositivas | Base aceptada | El documento es la fuente del **contenido**, no del formato |
| «Plus» animado | «No aplica… inspirada en las diapositivas» | Animar una diapositiva sigue siendo una diapositiva |
| Monigotes de línea | «Muy básicos y poco profesionales» | §0.2 |
| Refactor fotográfico | «Muy básico, no hay nada de destaque» | Fotos solas no dan identidad |
| **Centro de mando** | «Me gusta, sigámoslo ampliando» | Identidad RiskMann + fotos dentro de monitores + animación constante |

#### 10.1 El documento que gobierna el módulo: `DIRECCION.md`

Cada módulo tiene un `DIRECCION.md` normativo **antes** de construir los planos. Es lo
que permite construir ocho planos por separado y que se vean como una sola sala. El de
`videos/pesv-m01-mando/DIRECCION.md` es el modelo: cópialo y cambia solo la tabla de
tiempos, la etiqueta y la descripción de cada plano.

#### 10.2 El cromo persistente (idéntico en todos los planos intermedios)

```
Suelo       #051427 a sangre, como capa clip propia (nunca en #root)
Retícula    60×60 px, líneas rgba(142,143,196,0.14)
Escuadras   4 en L, 130×130, trazo 2 px #8E8FC4 al 0.6,
            en (56,56) · (1734,56) · (56,894) · (1734,894)
Reglas      laterales en x=84 y x=1820, de y=480 a y=840
Firma       riskmann_logo_blanco.png a 280 px de ancho, caja en left 92.33 / top 95
            (su tinta empieza en 104,104). Quieta. Reserva libre de 44 px.
Etiqueta    bajo la firma: regla roja + «CAPACITACIÓN PESV · MÓDULO NN · TEMA»,
            ~13 px lavanda, tracking 0.18em
Sección     arriba a la derecha, alineada a x=1816: «NN · NOMBRE DEL PLANO»
            — la única pieza de cromo que cambia de plano a plano
```

El plano de **apertura** construye este cromo en pantalla (el logo nace grande en el
centro y se va a la esquina); los intermedios lo llevan **quieto desde t=0**; el
**cierre** lo retira y devuelve el logo al centro. Es el mismo arco del §2.2.

#### 10.3 Arquitectura de un módulo

| Plano | Rol | Qué lo hace funcionar |
| --- | --- | --- |
| 01 · Apertura | Gancho + identidad | El logo se arma, se hace firma, y una frase corta de la voz («Tú no conduces. / Pero decides.») |
| 02–05 · Contenido | Un concepto por plano | Una **forma distinta** en cada uno: monitor con detección, fotografía aérea con retículas, monitores en cascada, indicador analógico |
| 06 · Ruta | Dónde está el módulo en la serie | Paneo por las 8 estaciones, «ESTÁS AQUÍ» en rojo |
| 07 · Retroalimentación | Pausa activa | Preguntas del documento + anillo de pausa; **~6 s quietos** al final |
| 08 · Cierre | Firma + legal | Logo al centro, frase de cierre del documento, pie legal legible, fundido final |

**Duración del plano = voz + respiro.** Entre 12 y 28 s según la voz, nunca con cola muerta.
El módulo 01 quedó en 151 s: 16 · 20 · 20 · 21 · 16 · 18 · 28 · 12.

**Pie legal obligatorio en el cierre:** «Contenido basado en el documento suministrado.
Valide vigencia y aplicación normativa con el responsable PESV.» · «Marco base:
Resolución 20223040040595 de 2022.»

#### 10.4 Fotografía

- **Fuente:** Pixabay (uso comercial sin atribución). Descargar en alta, armar hoja de
  contactos y **mirarlas** antes de elegir: los títulos mienten.
- **Descartar:** caras reconocibles (también reflejadas en espejos), matrículas legibles,
  logos de marcas.
- **Dónde van:** dentro de **monitores** (panel `#0C2B53`, contorno 1.5 px
  `rgba(142,143,196,0.28)`, marco interior 12–16 px); a sangre solo si el plano lo pide.
- **Grado:** `filter: brightness(0.78) contrast(1.14) saturate(0.45) hue-rotate(-6deg)` +
  capa `#0C2B53` en `multiply` a ~0.40. Scrim local bajo el texto, nunca un velo global.
- Fotos del módulo 01 en `videos/pesv-m01-mando/assets/fotos/` y biblioteca de
  candidatas ya revisadas (sin caras ni matrículas) en `assets/fotos-pixabay/`:
  reutilizables en otros módulos.

#### 10.5 Producir el módulo NN (paso a paso)

```bash
# 1. Copiar la plantilla aprobada (sin renders ni capturas)
cp -r videos/pesv-m01-mando videos/pesv-mNN-<tema>
rm -rf videos/pesv-mNN-<tema>/renders videos/pesv-mNN-<tema>/snapshots

# 2. Guion: tools/guion.json con las frases del documento de ESE módulo (§0)
cd videos/pesv-mNN-<tema>
python ../../tools/descargar-voz.py             # solo la primera vez en cada equipo
python ../../tools/voz.py tools/guion.json      # WAV por línea + duración real

# 3. Con las duraciones reales: tabla de tiempos en DIRECCION.md e index.html
# 4. Planos: 01 y 08 casi no cambian (texto de etiqueta y cierre); 02-07 se rediseñan
#    contra DIRECCION.md. 06 solo mueve «ESTÁS AQUÍ» a la estación NN.
# 5. Sonido
python ../../tools/mezcla.py tools/mezcla-modulo.json
# 6. Validar (§6.4) y renderizar
npx hyperframes lint && npx hyperframes check
npx hyperframes snapshot --at <medios y reposos de cada plano>
npx hyperframes render --quality high --output renders/pesv-mNN-<tema>.mp4 --browser-timeout 180
```

**Primero la apertura con sonido, luego el resto.** Mostrar 16 s aprobables cuesta ~10 min;
construir el módulo entero en la dirección equivocada costó una hora cada vez.

Los ocho módulos de la serie (según el documento): 01 Actor vial · 02 Antes del viaje ·
03 Ascenso y descenso · 04 Durante el viaje · 05 Pasajeros vulnerables · 06 Acompañante
en moto · 07 Emergencias PAS · 08 Taller y evaluación.

---

### 11. Audio — voz, efectos y cama

Todo es gratuito, local y sin límite de uso. Las herramientas compartidas viven en
`tools/` en la raíz del repositorio:

| Pieza | Herramienta | Detalle |
| --- | --- | --- |
| **Voz** | Piper TTS, voz **`es_ES-davefx-medium`** (elegida por el cliente) | `pip install piper-tts` y, una vez, `python tools/descargar-voz.py` (baja el modelo de 60 MB a `tools/voces/` y verifica su huella; no va en git). `tools/voz.py` genera un WAV por línea y **avisa si una línea no cabe** en su plano (`"maximo"`). |
| **Efectos** | Biblioteca de `/media-use` (19 efectos) | Licencia Pixabay: uso comercial sin atribución. En `~/.claude/skills/media-use/audio/assets/sfx/`. |
| **Cama** | Síntesis propia con osciladores | Sin derechos de terceros. **Fundamentales ≥ 110 Hz**: un drone de 55–82 Hz mide bien y suena a silencio en un portátil. |
| **Pista rítmica** | `tools/ritmo.py` + un JSON por pieza | Bombo, platillos, palmas, bajo y acordes sintetizados a un BPM, por secciones, con subidas de ruido antes de cada cambio. Determinista, sin derechos de terceros. Para videos sin voz. |
| **Mezcla** | `tools/mezcla.py` + un JSON por pieza | Voz y `pistas` con `adelay`, cama opcional con ducking por cadena lateral, `pasa_altos` opcional, −16 LUFS, y **verificación del espectro**: falla si la banda alta está vacía. |

**Reglas:**

- La voz se genera **antes** de fijar la duración de los planos, y el plano se adapta a
  ella. Si una frase no cabe en un plano ya animado, se acorta la frase, no el plano.
- Cada efecto va en el instante visual que lo justifica (un clic cuando se fija una
  retícula, un impacto cuando entra el logo). Nada de relleno.
- MusicGen **no sirve**: su licencia no es comercial.
- La mezcla va en `index.html` como un único `<audio class="clip">` en la raíz.

La mezcla del módulo 01 (`videos/pesv-m01-mando/tools/mezcla-modulo.json`) es el modelo:
8 capas de cama, 9 líneas de voz, 54 efectos.

---

### 12. Tiempos y pesos medidos

| Pieza | Duración | Construcción | Render | Peso |
| --- | --- | --- | --- | --- |
| Marketing «Sala de control» | 68 s | ~1 día (inventar el sistema) | 4 min 44 s | 15.9 MB |
| PESV M01 «Centro de mando» | 151 s | muestra ~10 min + ~2 h | ~9 min 30 s | 39.1 MB (vista 11.4 MB) |
| PESV M01 «Ritmo» (sin voz) | 60 s | muestra ~30 min + ~1 h | 4 min 02 s | 15.3 MB |
| PESV M01 «Ritmo» vertical 9:16 | 60 s | ~1 h (recomposición de las 7 escenas) | 4 min 09 s | 14.5 MB |

Con la plantilla de §10 un módulo nuevo debería costar bastante menos que el primero: el
sistema ya existe y solo cambian el guion y los planos de contenido.

---

### 13. Formato de capacitación — «Ritmo» (pieza corta, sin voz)

La misma presentación del módulo, pero como pieza de **60 s que se sostiene sin voz**: la
música marca el tiempo y cada entrada cae sobre el pulso. Sirve de gancho (redes,
pantallas, apertura de una sesión) junto al módulo completo con voz de §10. El cliente pidió
«mejores animaciones, mejor ritmo, más movimiento, fluidez, que sea entretenido» y lo aprobó
sin cambios. Proyecto de referencia: `videos/pesv-m01-ritmo/` (lee su `DIRECCION.md`).

#### 13.1 El pulso manda

**120 BPM → pulso de 0.5 s, compás de 2 s.** Cada escena empieza en frontera de compás y
todos sus tiempos son múltiplos del pulso (`const P = 0.5; const B = n => n * P;`). La pista
de `tools/ritmo.py` usa el mismo BPM, así que imagen y sonido coinciden sin ajustar a mano.

#### 13.2 Diferencias con «Centro de mando»

| | Centro de mando (§10) | Ritmo |
| --- | --- | --- |
| Duración | ~2:30, dictada por la voz | 60 s, dictada por el pulso |
| Fondo | HUD oscuro persistente | Paleta de las diapositivas del documento: papel `#F5F8FC` y marino `#0B2F6B` alternados escena a escena |
| Logo | Firma blanca arriba a la izquierda | Logo a color en una píldora blanca abajo a la izquierda (se lee sobre papel y sobre marino) |
| Cromo | Retícula, escuadras, reglas | Barra de progreso del video completo con una marca en cada cambio de escena |
| Cortes | Fundidos entre planos | **Cada escena cierra tapando la pantalla con el fondo de la siguiente** (ver 13.3) |

#### 13.3 El repertorio de movimiento

Cada técnica es una receta de `/hyperframes-animation` que la serie no había usado. Ninguna
se repite en dos escenas: esa variedad es lo que hace entretenida la pieza.

| Escena | Técnica | Receta |
| --- | --- | --- |
| Gancho | Cada palabra entra distinto (escala con desenfoque, golpe lateral, subida inclinada); estela de velocidad | `kinetic-beat-slam`, `motion-blur-streak` |
| Gancho | Tachón y círculo dibujados a mano | `css-marker-patterns` (sketchout, circle) |
| Corresponsable | Cascada de palabras, cada una antes de que termine la anterior; marcador detrás de una palabra | `waterfall-entry`, `css-marker-patterns` |
| Corresponsable | Un punto que se transforma en la tarjeta con la foto | `card-morph-anchor` |
| Roles | Palabras que llegan desde una nube 3D y se ordenan; barrido de color por dentro de las letras | `depth-scatter-assemble`, `gradient-text-sweep` |
| Deberes | Tarjetas que giran en 3D por turno | `transitions/css-3d` (card flip) |
| Principio | Rodillo tipo tragamonedas | `vertical-spring-ticker` |
| Ruta | Luz que recorre los 8 módulos, uno por pulso | pasos discretos sobre el pulso |

**Salidas:** iris desde el círculo · bloques verticales alternados · barrido diagonal ·
barrido con estela y panel que empuja · la ventana del rodillo crece hasta llenar ·
persianas · y el único fundido de la pieza al final.

#### 13.4 Sonido

```bash
python ../../tools/ritmo.py tools/ritmo-video.json    # pista a 120 BPM por secciones
python ../../tools/mezcla.py tools/mezcla-video.json  # pista + efectos, pasa_altos 90, -16 LUFS
```

Un efecto en cada golpe y en cada transición (62 en el módulo 01). Balance medido del
módulo 01: −21 / −20 / −22.5 dB en graves, medios y agudos.

#### 13.4b La variante vertical (9:16) para redes

`videos/pesv-m01-ritmo-vertical/` es el mismo minuto en **1080×1920**, para TikTok, Reels y
Shorts. **No es el horizontal recortado**: cada escena se recompone, y eso es todo el trabajo.

- **Lienzo**: `data-width="1080" data-height="1920"` en `index.html` y en cada escena, más el
  `width`/`height` del `#root` y del `body`.
- **Zona segura**: el contenido vive entre y≈300 y y≈1500. Arriba va el nombre de usuario y
  abajo los botones y los subtítulos de la app; la firma y la barra de progreso suben a
  y≈1560-1700.
- **Recomponer, no escalar**: lo que iba lado a lado se apila (la foto bajo el texto), las
  frases largas se parten en dos líneas, las filas de fichas se envuelven en dos renglones y
  la ruta de 8 módulos pasa de barra horizontal a **riel vertical**.
- **Tipografía proporcionalmente mayor**: un titular de 92 px en 16:9 se lee en 86 px sobre un
  cuadro que mide la mitad de ancho.
- **Mismo pulso, mismo audio**: los tiempos no cambian, así que las dos versiones comparten la
  mezcla (`assets/mezcla-video.wav`) y quedan sincronizadas.

Medido: render 4 min 09 s, 14.5 MB.

#### 13.5 Producir la pieza «Ritmo» de otro módulo

1. Copiar `videos/pesv-m01-ritmo/` (sin `renders/` ni `snapshots/`).
2. Escoger del documento de ese módulo **una frase por escena**. Sin voz, lo que no cabe en
   pantalla no se dice: menos texto que en el módulo completo.
3. Reasignar las técnicas de 13.3 a las ideas nuevas, sin repetir ninguna, y mantener una
   salida distinta por escena.
4. Ajustar `tools/ritmo-video.json` (secciones y subidas en los cambios de escena) y los
   efectos de `tools/mezcla-video.json` a los nuevos tiempos.
5. **Primero una muestra de ~16 s con sonido**, luego el resto.
6. `check` → capturas en cada cambio de escena → render → revisar los cortes en el MP4.

---

### 14. Formato de curso — «lámina a lámina», con hueco para voz humana

Cuando el material de entrada es un **PPTX de capacitación con notas de orador**, el video ya
viene escrito: las notas son el guion y las láminas son la estructura. Lo que hay que resolver
es el **tiempo**. La plantilla es `videos/ruta-segura-m1/`.

#### 14.1 La decisión de formato

- **Un video por módulo**, no uno por curso. Un PPTX de 33 láminas son ~29 min de narración;
  partido por módulos quedan piezas de 8 a 12 min, que es lo que una persona ve de una sentada
  y lo que se puede volver a grabar sin rehacer todo.
- **La voz se puede cambiar sin rehacer el video.** El montaje no guarda tiempos absolutos
  escritos a mano: los calcula a partir de la locución vigente (§14.3). Así se entrega una
  versión con voz sintética para aprobar la imagen, y el día que la grabe una persona se
  corre el mismo procedimiento sin tocar ninguna marca de tiempo.

#### 14.2 Medir antes de animar

El paso que hace que el formato funcione. Con Piper, frase por frase:

```bash
python -m piper -m tools/voces/es_ES-davefx-medium.onnx -f frase.wav   # texto por stdin
```

Con ElevenLabs no hace falta trocear: el endpoint `/with-timestamps` devuelve el instante de
**cada carácter**, así que el inicio de cada frase se lee en vez de estimarse. Es la forma
preferida — más exacta y una sola llamada por lámina.

Se guarda la duración de cada frase (`tools/tiempos-medidos.json`). Con eso:

- la **duración de la lámina** = duración de su narración + ~1,2 s de aire;
- el **momento de cada aparición** = el segundo en que el narrador nombra esa cosa.

Sin esa medición, un video de doce minutos es una secuencia de láminas quietas. Con ella, cada
elemento entra cuando la voz lo menciona y el módulo se deja ver.

> **Piper falla con comillas angulares** (`«…»`): termina en código 1 sin escribir el WAV
> (`wave.Error: # channels not specified`). Medir frase por frase aísla el problema; si una
> frase falla, se estima por conteo de palabras (~0,46 s/palabra a 130 ppm).

> Las notas pueden traer rótulos del documento (`GUION DE VOZ — PRIMERA PERSONA`). No son
> narración: se descuentan del tiempo y no entran al libreto.

**Con ElevenLabs, tres decisiones probadas:**

- **`eleven_v3`, no `eleven_multilingual_v2`.** En español la entonación interrogativa sube
  al final sin palabra que la anuncie, y estos guiones están llenos de preguntas: v2 las lee
  como afirmaciones y delata el video como sintético. v3 las resuelve, habla más pausado y
  también devuelve timestamps. No acepta `previous_text` / `next_text` — el encadenado de
  entonación entre láminas solo sirve en los modelos v2.
- **Las cifras, escritas en palabras** antes de enviarlas. «Ley 2466 de 2025» leída como
  «veinticuatro sesenta y seis» arruina la única referencia jurídica de un módulo.
- **El máster de voz, en MP3.** En WAV, once minutos pesan 61 MB y el navegador no lo carga
  dentro de los 10 s que da `check`: el runtime se cae con `Navigation timeout of 10000 ms`.

#### 14.3 Las composiciones se generan, no se escriben

Once láminas con el mismo encuadre no se mantienen a mano. En `tools/`:

- `base.py` — paleta, fuentes y **el encuadre común** (ceja, número, título, regla, pie).
- `eNN.py` — una lámina por archivo: CSS, cuerpo y línea de tiempo, con la marca de tiempo de
  la frase que dispara cada aparición escrita en el comentario.
- `cronometro.py` — **el mapa entre dos locuciones** (ver abajo).
- `voz-eleven.py` — pide la locución con timestamps y escribe `tiempos-voz.json`.
- `pista.py` — coloca cada lámina en su sitio del máster, normaliza a −16 LUFS y verifica.
- `construir.py` — encadena, calcula inicios y arma el `index.html` con sello y voz.
- `guion.py` — escribe `GUION-VOZ.md`, el libreto con la **ventana absoluta** de cada lámina.

**Lo que hace sostenible el formato es `cronometro.py`.** Las apariciones se escriben una vez
contra una locución de referencia; cuando la voz definitiva dura otra cosa, el módulo traduce
cada marca de tiempo: exacto en cada frontera de frase, proporcional dentro de la frase,
desplazamiento fijo en la cola. Las ochenta y tantas marcas se recolocan solas y `DUR` deja de
escribirse (`DUR = cronometro.duracion(LAMINA)`).

Esto no es una comodidad: es lo que permite entregar una versión con voz sintética para
aprobar la imagen y luego reemplazarla por una grabación humana sin rehacer el montaje. Ojo,
la voz nueva no es uniformemente más rápida ni más lenta — en la primera prueba una lámina se
acortó 3 s y la siguiente se alargó 6 s.

#### 14.4 Reglas de composición para láminas de ~60 s

- **Nada por debajo de y=946** (donde iba la línea de fuente, que ya no se muestra). Invadir
  esa franja es el error que más veces apareció. Los cierres de lámina van en una sola línea, no en dos.
- **Título de máximo dos renglones** (50 px, ancho 1450) y la regla de acento **debajo** de esa
  caja, no dentro.
- **Sustituir en vez de acumular.** Cuando entra la idea de cierre, se apaga la anterior en el
  mismo sitio; si no, la lámina termina siendo un muro.
- **Sin quiz ni barra de avance en el video.** Las láminas de reto, retroalimentación, repaso
  y evaluación se implementan en la plataforma después de ver cada video, y el módulo se
  entrega solo, no unido a los demás.
- **El video es informativo, no un quiz.** Sin pastilla de pausa, sin escudos del Reto, sin
  preguntas para el espectador ni línea de fuente. Si la locución ya grabada invita a pausar o
  responder, esas frases se recortan con `CORTES` en `tools/cronometro.py`: `pista.py` las quita
  del audio y el montaje se corre solo, sin volver a locutar.
- `check` toma **nueve muestras** en doce minutos: no basta. Hay que sacar `snapshot` en el
  momento más lleno de cada lámina (el final) y revisar la hoja de contactos.

#### 14.4b Renderizar once minutos en una máquina de 8 GB

Un módulo entero de una sola vez **no cabe**: el sistema mata el proceso. Los tres
consumidores son el Chrome del usuario (~1,5 GB), el Chrome sin cabeza del render y un
`ffmpeg` que se asienta en ~650 MB y no baja. Dos medidas, en este orden:

1. **La voz fuera del `index.html`.** Con el `<audio>` dentro, Chrome decodifica el MP3
   entero a PCM —unos 250 MB para once minutos— y ese es justo el margen que falta. Se
   renderiza mudo y se pega después: las dos pistas arrancan en cero y miden lo mismo.
2. **El render por partes.** `construir.py --partes 4` escribe cuatro `index-parte-N.html`
   con las escenas rebasadas a su propio cero. Cada parte se renderiza sola y se unen sin recodificar.

```bash
python tools/construir.py --sin-audio --partes 4
npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode --workers 1
# ... una por una
python tools/montar.py     # une, pega la voz y verifica duraciones
```

Partir no baja el pico de memoria: **acorta la exposición y hace barato el fallo**. Si una
parte muere se repite esa parte (≈10 min), no cuarenta minutos de trabajo. Los cortes caen
en frontera de escena, donde la lámina saliente ya está apagada (§14.4), así que la unión no
se ve.

**El lote tiene que ser reanudable.** Un bucle corrido de diez partes pierde, con cada
muerte, todo lo que venía detrás. `tools/render-partes.py` comprueba qué partes ya existen
con la duración correcta, salta esas y renderiza solo las que faltan; se vuelve a invocar
hasta que termina. Además mata los huérfanos antes de cada parte:

```bash
python tools/render-partes.py videos/curso-m1 videos/curso-m2 videos/curso-m3 videos/curso-m4
```

> Cuando un render muere por memoria **deja un `ffmpeg` huérfano de ~650 MB**. Hay que
> matarlo antes de reintentar o el siguiente intento arranca con menos margen que el anterior.

> **Los `index-parte-N.html` rompen el `check`.** `lint` los ve como raíces alternativas y
> falla con `multiple_root_compositions`. Se valida con la raíz limpia y se generan las
> partes después; `montar.py` las borra al terminar.

**Partir un módulo en piezas cortas:** `tools/cortar-laminas.py videos/<proyecto> --piezas N`.
La plataforma muestra el curso en piezas cortas. Con `--piezas N` manda cuántas piezas
tiene el módulo —dos o tres, de uno a dos minutos— y el script prueba todos los cortes
posibles para que queden lo más parejas posible; sin él manda la duración y agrupa
láminas mientras la suma no pase de `--maximo`. En los dos casos corta
el MP4 aprobado **solo en frontera de lámina**, donde la lámina saliente ya está
apagada (§14.4). No se recompone ni se recorta contenido. Cortar obliga a recodificar
el video —el corte cae en un fotograma que no es clave— pero el audio se copia.

**Unir los módulos en un máster continuo:** `tools/unir-curso.py <carpeta> <salida.mp4>`.
Concatena sin recodificar y avisa si algún módulo va mudo.

#### 14.5 Producir el módulo siguiente

1. Extraer las láminas del módulo del PPTX (texto y notas) y medir frase por frase.
2. Copiar `videos/ruta-segura-m1/` sin `renders/`, `snapshots/` ni `compositions/`.
3. Reemplazar `tools/eNN.py` por las láminas nuevas, reutilizando `base.py` sin tocarlo.
4. `python tools/construir.py` → `npx hyperframes check` → capturas → render.
5. Locutar (`voz-eleven.py`), volver a construir, armar la pista (`pista.py`).
6. `python tools/guion.py` y entregar `GUION-VOZ.md` junto con el MP4.

---

### 15. Formato de curso generado — PPTX grande con anatomía repetida

Cuando un PPTX trae decenas de láminas que comparten pocas anatomías, escribir cada
lámina a mano (§14) no escala. Los cursos «Motociclista laboral seguro» (88 láminas → 15
videos, 40:47) y «Conducción Segura y Manejo Defensivo» (55 láminas → 15 videos, ~33 min)
se **generan**. Proyectos de referencia: `videos/moto-curso/` y `videos/csm-curso/`.

#### 15.1 Qué cambia respecto a §14

| | Lámina a lámina (§14) | Generado |
| --- | --- | --- |
| Composiciones | Un `eNN.py` escrito a mano por lámina | 6–7 plantillas en `plantillas.py`; `elegir(d)` asigna una por lámina |
| Fuente de datos | Notas copiadas a mano | `datos/curso.json`: texto por **nombre de forma** del PPTX, notas partidas en frases |
| Marcas de tiempo | Escritas en comentarios, traducidas por `cronometro.py` | Calculadas por `sincronia.py`: cada elemento entra con la frase que lo nombra |
| Carpetas | Un proyecto por módulo, con sus `tools/` | Un generador (`<curso>-curso/`) escribe los proyectos `<curso>-<clave>/` |
| Entrega | Módulo entero, cortado después con `cortar-laminas.py` | `--tramos` reparte las láminas en videos de ~1–2 min sin cortar ninguna |

#### 15.2 Reglas

- `LIMITES` fija qué láminas van en cada video. Evaluaciones, autochequeos y pausas **no
  entran**: se detectan por nombre de forma (`q-text-N`) o por la regex `PAUSA` sobre la
  nota, y van a la plataforma.
- Si la nota del orador solo anuncia la lámina («Parte 2 del módulo…»), la narración se
  arma en `datos/guion-partes.json` con lo que la lámina muestra, sin añadir nada.
- La paleta sale del PPTX; la tipografía es Montserrat empaquetada. El color claro de
  marca no se usa para texto pequeño (moto: `ORO_TEXTO #8C5E08`, 4,9:1 sobre crema).
- Cifras, porcentajes, `km/h` y siglas se pasan a palabras antes de locutar (`normalizar`).
- Sin `tiempos-voz.json` el proyecto se construye igual con tiempos estimados
  (0,068 s/carácter): se revisa mudo antes de pagar la voz.
- Los `index-parte-N.html` se escriben **después** de `lint`/`check` (rompen la validación
  con `multiple_root_compositions`); `montar` los borra al terminar.
- `montar` rechaza un render cuya duración difiere más de 0,6 s de su pista de voz.

#### 15.3 Producir un curso nuevo

1. Extraer el PPTX a `datos/curso.json` (el extractor no está en el repo: ver
   `docs/PLAYBOOK.md` §8).
2. Copiar `videos/csm-curso/` sin `assets/voz/`, `datos/tiempos-voz.json` ni `__pycache__/`.
3. `base.py`: paleta muestreada del nuevo PPTX. `plantillas.py`: una plantilla por
   anatomía. `<curso>.py`: `LIMITES` y el prefijo de las carpetas.
4. Construir la apertura mudo → `check` → capturas → **muestra al cliente**.
5. `voz` → `construir` → `construir --tramos` → `render-partes.py` → `montar`, módulo por módulo.

---

<a id="cap-7"></a>

## 7. Guía de prompts

> Fuente: [`GUIA-PROMPTS.md`](../GUIA-PROMPTS.md) — se edita ahí, no aquí.

> **Qué es esto.** Un catálogo de instrucciones probadas: *«con este prompt consigo esto»*.
> Cada entrada se escribió justo después de ejecutarse, con el resultado a la vista — no
> reconstruida de memoria al final. Lo que aquí aparece **funcionó de verdad** en este
> repositorio; lo que falló también está documentado, porque ahorra más tiempo que lo que
> salió bien.
>
> Se usa con Claude Code abierto en la carpeta `riskmann2-marketing-videos`.

---

### Cómo leer una entrada

Cada prompt trae: **qué consigue** · **el prompt literal** · **qué te devuelve** ·
**cuánto tarda** · **qué necesitas tener listo antes**.

Los prompts están escritos para pegarse tal cual, cambiando solo lo que va `<entre
ángulos>`.

---

## 1 · Arrancar

#### 1.1 — Un video nuevo desde un documento

**Consigues:** un video completo a partir de un PDF o unas diapositivas que ya existen.

```
Lee <ruta del documento>. Quiero un video que replique su sistema de
diapositivas con revelado progresivo: cada elemento aparece cuando la
narración lo nombra.

Antes de construir nada:
1. Extrae los colores reales del documento muestreando los píxeles, no los
   estimes a ojo.
2. Escribe un frame.md con esos valores y con las reglas de composición.
3. Enséñame el guion antes de animar.

Regla que manda sobre todo: nada entra al video si no puede rastrearse al
documento. Sin cifras inventadas, sin afirmaciones normativas que no estén
en el material.
```

**Te devuelve:** proyecto scaffolded, `frame.md` con la paleta real, `BRIEF.md`,
`STORYBOARD.md` y el guion para que lo apruebes.
**Tarda:** 10–15 min hasta el guion.
**Necesitas:** el documento en local, o capturas legibles de cada página.

> **Por qué el muestreo de píxeles importa.** En este repositorio dio
> `#0B2F6B` como navy dominante en el 93 % de las láminas. A ojo se habría puesto un azul
> «parecido» y las dos series no habrían encajado nunca.

#### 1.2 — Un video de marketing desde assets sueltos

**Consigues:** una pieza promocional a partir de logos, capturas y grabaciones de UI.

```
Con /hyperframes, haz un video de presentación de <producto> usando los
recursos de <carpeta de assets>. Que sea vistoso.

Antes de escribir el guion, dime qué afirmaciones vas a poner en pantalla y
de dónde sale cada una. Si algo no está en los archivos, no lo pongas.
```

**Te devuelve:** una ronda de conceptos para elegir, luego el video.
**Tarda:** 1–2 h con revisiones.

> **La segunda frase del prompt no es opcional.** Sin ella, el primer video de este
> repositorio acabó afirmando un «100 % de trazabilidad» que no salía de ningún dato de la
> empresa.

---

## 2 · Dirigir el resultado

#### 2.1 — Elegir el concepto antes de gastar tiempo

**Consigues:** cinco direcciones distintas para el mismo material, y eliges.

```
Antes de construir, proponme cinco conceptos visuales distintos para este
video. Que sean genuinamente diferentes entre sí, no variaciones del mismo.
Recomiéndame uno y dime por qué.
```

**Te devuelve:** cinco propuestas en texto, con recomendación.
**Tarda:** 2 min. **Ahorra:** horas de construir lo que no querías.

#### 2.2 — Subir el nivel de un video que ya existe

**Consigues:** una versión mejorada sin rehacer la identidad.

```
Haz una versión plus de <proyecto>. Hereda su frame.md entero — misma
paleta, misma retícula, mismo cromo — y añade dos capas:

1. Diagramas que expliquen, dibujados como SVG que se traza solo. No
   imágenes pegadas, no iconos de librería.
2. Una cámara que viaje entre láminas sobre un lienzo continuo, en vez de
   fundidos. La cámara nunca se mueve mientras hay texto entrando.
```

**Te devuelve:** un proyecto nuevo hermano del anterior, con la misma identidad.
**Tarda:** 40–60 min.

#### 2.3 — Refactor: salir del formato diapositiva

**Consigues:** una pieza de motion design real a partir de material que nació como
presentación. Es la dirección que el cliente aprobó para la serie PESV.

```
Haz un refactor de <proyecto>. El documento es la FUENTE DEL CONTENIDO, no el
formato visual: fuera la lámina blanca, los márgenes, la ambladura, el pie
repetido y las viñetas.

Lenguaje: fotografía real a sangre, gradada a la paleta de marca, con una capa
técnica fina encima (reglas de 1px, etiquetas pequeñas) y la tipografía grande
como suceso, entrando por máscara, nunca por fundido. Un empuje lento y
continuo sobre la foto por plano. Nada de figuras humanas dibujadas.

Antes de construir el video entero, construye SOLO el plano de apertura y
enséñame un fotograma a resolución completa.
```

**Te devuelve:** un plano de muestra para aprobar; con el sí, el resto del módulo.
**Tarda:** 5 min la muestra, ~45 min el resto.

> **La última frase es la que más ahorra.** Las dos versiones anteriores de este módulo se
> construyeron enteras (50 min + 9 min de render cada una) antes de que el cliente dijera
> que no era la dirección. La muestra de un solo plano cuesta cinco minutos.

#### 2.4 — Conseguir fotografía sin salir de la sesión

```
Busca en Pixabay fotos para <lista de tomas>. Descárgalas en alta, arma una
hoja de contactos numerada, y MÍRALAS antes de elegir. Descarta cualquiera
con caras reconocibles, matrículas legibles o logos de marca.
```

**Por qué «míralas»:** los títulos de las fotos mienten. En este repositorio, la foto
titulada «Rearview Mirror Windshield» mostraba los ojos del conductor reflejados — descartada.
La licencia de Pixabay permite uso comercial sin atribución.

#### 2.4b — Darle identidad de marca a una serie de formación

**Consigues:** que un módulo de capacitación se vea como una pieza RiskMann y no como una
presentación con fotos — logo vivo, animación constante, un universo visual propio. Es la
dirección **«Centro de mando»** que el cliente aprobó para la serie PESV después de llamar
«muy básico» al refactor fotográfico.

```
Toma como referencia de identidad <video de marca aprobado> (logo de RiskMann,
densidad de animación, recursos, HUD) y haz un prototipo nuevo de <módulo>
con ese concepto. El documento sigue siendo la única fuente del contenido.

Regla de marca: solo el archivo oficial del logo; nada de redibujarlo,
re-letrarlo, recolorearlo ni taparlo. Sin figuras humanas dibujadas.

Construye SOLO la apertura (~15 s) CON SONIDO (voz + efectos + cama) y
pásamela antes de seguir.
```

Con el sí:

```
Me gusta, amplíalo de esa misma manera. Escribe primero un DIRECCION.md con
el cromo persistente, la paleta y el tiempo de cada plano, y que todos los
planos se construyan contra ese documento.
```

**Te devuelve:** la muestra de apertura; luego el módulo completo con un `DIRECCION.md`
normativo, 8 planos, mezcla y render.
**Tarda:** ~10 min la muestra; ~2 h el módulo (construcción + verificación) + render.

> **Por qué «CON SONIDO» en la muestra:** la voz fija la duración real de cada plano. En
> este módulo, el plano de los tres deberes estaba pensado a 30 s y su voz duraba 9.6 s: 17 s
> de cola muerta. Se recortó a 21 s antes de construirlo, no después.
>
> **Por qué `DIRECCION.md`:** ocho planos construidos por separado solo se ven como una
> sola sala si comparten las mismas constantes escritas (posición exacta del logo, retícula,
> escuadras, etiqueta). Es el contrato que hace posible construir en paralelo.

#### 2.4c — Más ritmo y animaciones nuevas, sin voz

**Consigues:** una versión corta (60 s) del mismo módulo que se sostiene sola: cada
entrada cae sobre el pulso de una pista, cada escena se mueve con una técnica distinta y
los cambios de escena son fluidos. Es el formato **«Ritmo»**; el cliente lo aprobó sin
cambios («EXCELENTE»).

```
Sigue siendo una presentación del mismo módulo, pero quiero probar
animaciones mejores: más ritmo, más movimiento, fluidez, que sea
entretenido. Cosas nuevas, nada que ya hayamos usado. 60 segundos, sin voz.
```

**Te devuelve:** una muestra de ~16 s con sonido para aprobar; con el sí, los 60 s.
**Tarda:** ~30 min la muestra, ~1 h el resto, 4 min de render.

> **Lo que hizo funcionar este prompt:**
> - **«Nada que ya hayamos usado»** obliga a escoger técnicas nuevas del catálogo del
>   framework: tipografía que golpea al compás, trazos a mano, una forma que se transforma
>   entre escenas, tarjetas que giran en 3D, un rodillo tipo tragamonedas. Qué técnica va en
>   cada escena está en `PRODUCCION-VIDEOS.md` §13.3.
> - **Sin voz, la música manda:** todo cae en múltiplos de medio segundo (120 BPM) y la
>   pista se sintetiza con `tools/ritmo.py` al mismo tempo.
> - **Ojo con la pregunta de concepto.** Primero se propusieron cinco conceptos visuales
>   radicales y el cliente aclaró que no quería otro concepto, sino **mejor movimiento** en
>   el mismo formato. Si lo que falla es la animación, dilo así: ahorra una ronda.

#### 2.4d — Convertir un PPTX de capacitación en video, con hueco para voz humana

**Consigues:** el curso partido en videos por módulo (8 a 12 min cada uno), **sin voz**, con
cada aparición en pantalla montada sobre el segundo exacto en que la narración la menciona,
más el libreto con la ventana de tiempo de cada lámina para grabar la locución después.

```
Necesito animar esta presentación: <ruta al .pptx>
Hazlo por módulos, un video por módulo.
Dejo el hueco para voz humana: entrégalo sin locución, pero montado
sobre los tiempos reales de la narración, y dame el guion con los
tiempos para grabarla después.
```

**Te devuelve:** el MP4 del primer módulo y un `GUION-VOZ.md` con la ventana absoluta de
cada lámina y las frases en el orden en que el video las muestra.
**Tarda:** ~25 min medir la narración, ~2 h componer las láminas, ~40 min de render.

> **Lo que hizo funcionar este prompt:**
> - **Las notas del orador son el guion.** Antes de animar nada se sintetiza **frase por
>   frase** con Piper y se guardan las duraciones. La duración de cada lámina sale de ahí, no
>   de una estimación. Sin esa medición el resultado es una secuencia de láminas quietas.
> - **«Dejo el hueco para voz humana»** es lo que permite aprobar la imagen antes de pagar
>   estudio: una corrección de texto no obliga a re-renderizar doce minutos.
> - **Pedir «por módulos» acota el riesgo.** Un PPTX de 33 láminas son ~29 min de narración;
>   si algo no gusta, se rehace un módulo, no el curso.
> - Detalle del procedimiento en `PRODUCCION-VIDEOS.md` §14.

#### 2.5 — Corregir un plano concreto

**Consigues:** un cambio quirúrgico sin tocar el resto.

```
En <proyecto>, el plano <NN> tiene <problema>. Arréglalo sin tocar los
demás planos, y vuelve a sacar capturas de ese plano antes de renderizar.
```

**Tarda:** 5 min + render.

---

#### 2.6 — La misma pieza para otra marca, sin que dependa de la primera

**Consigues:** la versión de un evento para una segunda marca, con identidad propia. Nació de
FEGIR: la primera versión recoloreó la invitación de Yezid y el cliente la rechazó.

```
<ruta al manual de la marca> ahí está todo. La pieza debe ser solo de <marca>:
nada de <otra marca> (nombre, web, paleta ni estructura). Saca la identidad del
manual —colores muestreados, logo desde sus vectores— y dime qué datos del
evento vas a usar y de dónde sale cada uno.
```

**Te devuelve:** logos extraídos del PDF (SVG + PNG), la paleta real y una composición nueva.
**Tarda:** ~1 h con voz, música y render.

> **Lo que lo hizo funcionar:** pedir el manual antes de construir y decir «solo de
> <marca>» desde el principio. «Con los colores de X» no basta: la estructura heredada
> también se lee como dependencia.

#### 2.7 — Una serie de variantes a partir de una secuencia de correos o de una landing

```
Necesito ahora las versiones <recordatorio / es mañana / es hoy>: en <ruta> está
la estructura de los correos que se van a enviar esos días.
```

o, para una landing:

```
Ahora quiero la serie de videos cortos: uno por idea de la landing, cada uno
gancho → valor → CTA con un botón literal de la página.
```

**Te devuelve:** un `serie.py` que genera N proyectos HyperFrames editables en el Studio,
con la voz pedida con semilla fija y cada aparición sobre su palabra.
**Tarda:** ~40 min las voces y la construcción; ~30 s de render por pieza.

> **Cambiar una frase después** cuesta un comando: `python serie.py voz <carpeta>:<n>`
> regenera solo esa frase y `construir` recoloca las escenas. Ojo: `construir` reescribe
> lo editado a mano en el Studio.

#### 2.8 — Dejar un proyecto listo para editarlo en la interfaz de HyperFrames

```
Lo quiero editar localmente con la interfaz de HyperFrames.
```

**Te devuelve:** cada escena como sub-composición (una fila en la línea de tiempo), la voz,
los efectos y la música como pistas `<audio>` con la curva de volumen editable, y el Studio
abierto en `localhost:3002`.

## 3 · Audio

#### 3.1 — Narración gratuita e ilimitada en español

**Consigues:** locución local, sin cuenta y sin límite de uso.

```
Añade narración en español a <proyecto> con Piper, voz es_ES-davefx-medium.

El guion sale solo de: (a) texto que ya está en pantalla, (b) copia
aprobada de la empresa. Nada más.

Escribe cada línea para que quepa dentro de la duración que ya tiene su
plano — no re-cronometres la animación.
```

**Te devuelve:** un WAV por plano + la mezcla montada + `SCRIPT.md` con la procedencia de
cada frase.
**Tarda:** 10 min.
**Necesitas:** `pip install piper-tts` y los modelos de voz (~60 MB cada uno).

> **La última frase del prompt es la que salva el trabajo.** Si la narración no cabe en el
> plano, hay que re-cronometrar, y eso desincroniza todas las animaciones internas que ya
> estaban ajustadas al segundo.

#### 3.2 — Probar voces antes de decidir

```
Genera la misma frase con las voces españolas de Piper que no hemos
probado, y pásame los MP3 para escucharlos.
```

**Por qué:** el modelo no puede oír. La elección de voz es tuya, siempre.

#### 3.3 — Efectos y cama musical

```
Añade los efectos de la biblioteca incluida del framework, sincronizados a
los momentos visuales concretos (no de relleno). Y una cama musical con
ducking real por cadena lateral, para que baje cuando entra la voz.
```

**Nota de licencias:** los 19 efectos incluidos son licencia Pixabay — uso comercial, sin
atribución. **MusicGen no sirve para material comercial** (licencia no comercial). Para
música: elige una pista en Pixabay Music y pásala, o sintetiza una cama desde osciladores.

#### 3.4 — La mezcla como archivo de configuración

**Consigues:** que el sonido de un módulo nuevo sea editar un JSON, no programar.

```
Monta el sonido de <proyecto> con tools/mezcla.py: escribe
tools/mezcla-<nombre>.json con la cama, cada línea de voz en su segundo y
cada efecto en el instante visual que lo justifica.
```

**Te devuelve:** `assets/mezcla-<nombre>.wav` normalizado a −16 LUFS, con la voz
verificada por espectro (el script **falla** si la banda de voz está vacía).
**Tarda:** 2 min por módulo una vez escrito el JSON.
**Dónde está:** `tools/mezcla.py` en la raíz del repositorio — el script no cambia entre
módulos. Modelo de JSON: `videos/pesv-m01-mando/tools/mezcla-modulo.json`.

#### 3.5 — La locución como archivo de configuración

```
Genera la locución de <proyecto> con tools/voz.py a partir de
tools/guion.json. Cada línea con su "maximo" en segundos; si alguna no
cabe, acórtala sin cambiar el sentido y sin salirte del documento.
```

**Te devuelve:** un WAV por línea en `assets/vo/` y la duración de cada una; el script
**falla** si una línea no cabe en su plano.
**Tarda:** ~1 min por módulo. Modelo: `videos/pesv-m01-mando/tools/guion.json`.

#### 3.6 — Música propia a un tempo, para videos sin voz

```
Sintetiza una pista rítmica a 120 BPM con tools/ritmo.py para <proyecto>:
más ligera en el arranque, completa desde la segunda escena, una subida
antes de cada cambio de escena y un cierre suave. Mézclala con efectos en
cada golpe y cada transición, con pasa_altos 90, y mide tres bandas.
```

**Te devuelve:** `assets/ritmo-video.wav` y `assets/mezcla-video.wav`, más el balance
por bandas.
**Tarda:** ~2 min. Sin derechos de terceros: es síntesis propia.

> **Por qué «mide tres bandas»:** la primera mezcla tenía los agudos 16 dB por debajo de
> los graves; en un portátil habría sonado a puro bombo. El paso-altos a 90 Hz y bajar los
> impactos lo dejó en −21 / −20 / −22.5 dB. El modelo no puede oír: la medición es su oído.

---

#### 3.7 — Una sigla que suena rara o distinta cada vez

```
ElevenLabs no pronuncia bien "<SIGLA>" y en las dos frases la dice distinto.
```

**Qué hace el agente:** genera las dos frases con la misma semilla escribiendo la sigla de
4 maneras, **mide** cuánto dura la sigla en cada frase (alineamiento por carácter) y se queda
con la que dura igual en ambas. Para PESV ganó «pe e ese ve» (0,75 / 0,76 s). Deja los 4 MP3
para que tú elijas de oído y regenera **solo** las frases con la sigla.

## 4 · Verificar

#### 4.1 — La verificación de audio que evita un desastre

**Consigues:** saber si la voz está realmente en el archivo, sin escucharlo.

```
Antes de renderizar, verifica el audio partiendo el espectro: mide el nivel
por encima de 400 Hz (ahí vive la voz) y por debajo de 200 Hz. Si la banda
alta está por debajo de -40 dB, la voz no está.
```

> **Esto viene de un fallo real.** Una mezcla midió −11.9 dB de media —nivel perfectamente
> sano en un vúmetro— y sonaba a silencio absoluto: era energía casi toda por debajo de
> 200 Hz. El promedio no detecta ese fallo; el espectro sí, en un segundo.

#### 4.2 — Revisar antes de gastar el render

```
Saca capturas en los puntos medios de cada plano y a ±0.1s de cada corte, y
revisa la hoja de contactos antes de renderizar.
```

> **También viene de un fallo real.** Un plano salió completamente en negro y no se habría
> notado hasta ver el MP4 terminado, nueve minutos después.

---

## 5 · Lo que NO funciona

| Intento | Qué pasa | Qué hacer |
|---|---|---|
| Editar HTML con expresiones regulares | Un patrón `<video…>` coincidió dentro de un **comentario** y borró 4 KB de marcado. El plano salió en negro. | Editar con scripts que parseen, y **siempre** re-capturar después |
| Sustituir colores con `sed` sin `-I` | Los agentes escriben `#7a7a7a` en minúsculas; la sustitución en mayúsculas no coincide y el fallo de contraste persiste | `sed -i 's/…/…/gI'` |
| Escribir texto con `Set-Content` de PowerShell | Corrompe los acentos (doble codificación UTF-8) | Escribir con Python o con la herramienta de escritura, nunca con PowerShell |
| Nombrar una fuente sin `@font-face` | El MP4 sale con otra tipografía **en silencio** — el render es un Chrome limpio sin fuentes | Copiar los `.woff2` a `assets/fonts/` y declarar la fuente en cada plano |
| Poner un `<video>` dentro de una sub-composición | El ensamblador lo rechaza | Los `<video>` van en `index.html`, en la raíz |
| Animar `letterSpacing` | El validador lo rechaza: refluye el texto y tiembla bajo el motor de captura | Partir en glifos y animar la `x` de cada uno |
| Citar demasiadas recetas de movimiento en un plano | El paquete supera 48 KB y el constructor falla | Máximo 2–3 recetas por plano con formas grandes |
| Apilar capas de grado sobre una foto (brillo 0.5 + multiply navy 0.82 + velo global) | **La foto desaparece**: queda un campo azul plano, lo contrario de usar fotografía | Menos oscuridad, más desaturación, y un **scrim local** solo bajo el texto |
| Máscara de revelado con ancho fijo más estrecho que la frase | **Recorta palabras en silencio.** En el refactor desapareció «aumentar» del principio clave — cambiaba el sentido. Ni `lint` ni `check` lo detectan | Revisar **cada plano en reposo** con capturas. Ancho útil real: 1920 − margen izq. − margen der. |
| Fiarse de `check` con revelados por máscara | Da decenas de «solapamientos» que no existen: mide la caja del texto oculto sin el recorte | Verificar esos instantes a ojo, declarar **solo** los elementos afectados con `data-layout-allow-overlap`, y luego revisar el reposo |
| Dibujar personas en SVG (monigotes de línea) | El cliente los rechazó: básicos y poco profesionales | Sin figuras humanas: fotografía real o dibujo técnico de objetos |
| Poner `visibility = "visible"` en un hijo animado | Un `visible` explícito **atraviesa** el ocultamiento de su plano: los glifos de la etiqueta del plano 01 seguían vivos debajo de los planos siguientes. Solo lo delató `check` (texto «tapado» en el plano 04) | Revelar con `visibility = "inherit"`, nunca `"visible"`; y nunca animar `visibility`/`display` de un elemento `clip` |
| Espacios en glifos `inline-block` | Se colapsan: «CAPACITACIÓNPESV» | Espacio duro en cada celda de espacio, escrito como `"\u00A0"` en el código |
| Lanzar muchos constructores en paralelo | Los límites de uso los cortan a medias y dejan archivos parciales | Oleadas de 2, que cada uno escriba su archivo pronto, y revisar el disco antes de relanzar |
| Guardar el estado de una animación en un callback (`onUpdate`) | Al saltar hacia atrás el renderizador no lo ejecuta: el rodillo mostraba la palabra equivocada | Pedir que cada paso sea una animación explícita («seek-safe») |
| Calcular a ojo dónde queda cada palabra | Dos píldoras se montaron | Pedir que la fila se ordene sola (flexbox) y animar desde ahí |
| Fiarse del verificador con tarjetas 3D o rodillos | Lee como visible la cara oculta y lo que está fuera de la ventana: decenas de falsos errores | Hacer invisible de verdad lo que no se ve en cada instante |
| Enviar el MP4 master por la sesión | Límite de 30 MB; la fotografía lo supera (el refactor pesa 44.6 MB) | Copia de visualización con `ffmpeg -crf 26` (quedó en 6.9 MB) y el master aparte |

---

## 6 · Datos de producción medidos

| Pieza | Duración | Construcción | Render | Peso |
|---|---|---|---|---|
| Marketing «Sala de control» | 68 s | ~1 día con revisiones | 4 min 44 s | 15.9 MB |
| Marketing, con narración y audio | 68 s | +40 min | 5 min 34 s | 17.5 MB |
| PESV Módulo 01 (base) | 2 min 36 s | ~50 min | 9 min 32 s | 10.7 MB |
| PESV Módulo 01 «plus» — *rechazada* | 3 min 22 s | ~1 h | 9 min 04 s | 19.9 MB |
| PESV Módulo 01 refactor — *«muy básico»* | 2 min 28 s | ~1 h, con muestra previa | 10 min 08 s | 44.6 MB |
| PESV Módulo 01 «Centro de mando» — *dirección aprobada* | 2 min 31 s | muestra 16 s + ~2 h el resto, con voz/efectos/cama | ~9 min 30 s | 39.1 MB (11.4 MB copia de vista) |
| PESV Módulo 01 «Ritmo» — *aprobado sin cambios* | 1 min 00 s | muestra 16 s + ~1 h el resto, pista rítmica y efectos | 4 min 02 s | 15.3 MB |
| FEGIR En Vivo (identidad propia, editable en el Studio) | 21,9 s | ~1 h + ajustes | 36 s | 8,6 MB |
| FEGIR recordatorios (3 variantes generadas) | 3 × 15–19 s | ~40 min | ~30 s c/u | 7–8 MB c/u |
| RiskMann Capacitaciones, promo generado | 39,3 s | ~1,5 h con correcciones | 38 s | 15,3 MB |
| RiskMann Capacitaciones, serie de 4 (reutiliza el promo) | 4 × 15–17 s | ~40 min | ~30 s c/u | 7–8 MB c/u |

**La lectura útil:** el primer video de una serie cuesta un día porque hay que inventar el
sistema. El segundo cuesta una hora porque el sistema ya existe. Ahí está el retorno.

---

*Documento vivo. Cada entrada nueva se añade cuando el prompt se ejecuta, no después.*

---

<a id="cap-8"></a>

## 8. Arranque en otro equipo

> Fuente: [`docs/ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md) — se edita ahí, no aquí.

Todo lo que hace falta instalar y todo lo que ya costó caro aprender, para no
repetirlo. Verificado en el equipo donde se produjo `riskmann-consulta-pesv-vertical`
el 17 de septiembre de 2026.

---

### 1. Qué instalar

#### Software base

```bash
winget install --id Gyan.FFmpeg -e                 # 9.0.1
winget install --id oschwartz10612.Poppler -e      # 25.07.0  (leer PDF como imagen)
winget install --id GitHub.cli -e                  # 2.101.0
```

Ya presentes en el equipo original, por si el nuevo no los trae:

| Herramienta | Versión usada |
| --- | --- |
| Node | v24.16.0 (npx 11.13.0) |
| Python | 3.14.5 |
| Git | 2.53.0 |

```bash
python -m pip install numpy      # 2.5.3 — lo necesita tools/ritmo.py
```

> **`pip install` a secas instala en el Python equivocado.** En este equipo `pip`
> apuntaba al Python de la Store y el shell usaba `pythoncore-3.14-64`. Siempre
> `python -m pip`.

> **Poppler no queda en el PATH que winget anuncia.** El binario vive en
> `%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*\poppler-*\Library\bin`.
> Hay que invocarlo por ruta completa o añadirlo al PATH a mano.

#### Skills

Las 24 que estaban activas. **No hacen falta más**: en esta producción el
problema nunca fue falta de herramientas.

```
embedded-captions  faceless-explainer  ffmpeg  ffmpeg-media-finishing  figma
general-video  hyperframes  hyperframes-animation  hyperframes-audio
hyperframes-cli  hyperframes-core  hyperframes-creative  hyperframes-keyframes
hyperframes-registry  media-use  motion-graphics  music-to-video  pr-to-video
product-launch-video  remotion-to-hyperframes  slideshow  synced
talking-head-recut  ux-designer
```

```bash
npx hyperframes skills update      # refresca el set base y lo ya instalado
```

Reiniciar la sesión del agente después de instalar skills, o no se cargan.

**Tres que estaban instaladas y se desaprovecharon** — vale la pena usarlas:

- `hyperframes-registry` — ~400 bloques ya hechos y seek-safe. En la v1 se
  dibujó a mano cada barrido y cada destello.
- `hyperframes-keyframes` — cámara, punch-in, match cuts, profundidad 3D.
- `dataviz` — para cifras como el 500 SMMLV o el 70 %.

#### Claves y accesos

- `ELEVENLABS_API_KEY` — está en el issue #3. **Caducaba el 21 de septiembre de
  2026**; comprobar antes de contar con ella. Se lee del entorno y **nunca** se
  escribe en un archivo del repo.
- Voz «Carlos» (colombiana): `4PN5DHmrfIgZksvIrawS`, modelo `eleven_multilingual_v2`.
- El CLI de HyperFrames va **fijado por proyecto** (`hyperframes@0.8.42` en
  `package.json`), para que el render se reproduzca igual con el tiempo.

#### Dónde NO trabajar

**Fuera de OneDrive.** Durante esta producción OneDrive borró el repo de trabajo
en caliente: pasó de 1556 a 367 y luego a 53 archivos en menos de dos horas, y
se llevó `.git/HEAD`, `.git/config` y toda la base de objetos. Se perdieron los
MP4 entregados y los archivos sueltos de cada carpeta.

Lo que sobrevivió fue lo que estaba en GitHub. **Commit y push temprano y a
menudo** es la única red real.

---

### 2. Errores que ya se pagaron

#### Audio y mezcla

Están escritos como ocho lecciones en la cabecera de `tools/mezcla.py`. Las
cuatro que se descubrieron en esta producción:

**La música va en `musica`, nunca en `pistas`.** `pistas` desemboca en el mismo
`amix` que la locución y nada la aparta: en los picos se come la voz. Ese era el
motivo real de que la música tapara al locutor, y no era cuestión de volumen.

**Un TTS no entrega nivel de emisión.** ElevenLabs devuelve la voz a −33 dB de
media; una pista de catálogo viene a −14 dB. **19 dB de desventaja que ningún
ducking compensa.** Se nivela antes, a disco, con `tools/nivelar-voz.py`.

**`loudnorm` no puede ir dentro del `filter_complex`.** Entrega 192 kHz y
desplaza los timestamps, con lo que el `apad`/`atrim` posterior devuelve
**silencio sin dar ningún error ni código de fallo**. Por eso se nivela a disco.

**Rellenar toda rama hasta la duración final antes de mezclar.** Con ramas de 2 s
y de 37 s colgando del mismo `asplit`, ffmpeg acumula búfer hasta atascarse: una
mezcla de 37 s tardó **7 minutos** en vez de 2 segundos.

**El bus frontal puede quedar vacío.** Una versión de solo música no lleva voz ni
efectos, y `amix` con cero entradas **no da error**: deja el grafo colgado y
ffmpeg gira sin terminar nunca. Y sin voz no se aplica ducking, o la música se
agacharía bajo sus propios efectos.

**Una cama de senos suena a silencio en un celular.** Un acorde entre 146 y
440 Hz mide bien en el vúmetro y da −62.7 dB en agudos. Un parlante de teléfono
corta por debajo de 500 Hz.

#### Cómo se verifica el audio

Nunca por el nivel general. Siempre:

- **Margen voz–música frase por frase**, extrayendo los dos buses por separado.
  Objetivo: la voz entre **+7 y +25 dB** sobre la música en cada frase. Si se
  pasa de ahí la música se hunde y suena a bombeo.
- **Tres bandas** (graves <200, medios 200–2k, agudos >2k) dentro de ~12 dB:
  ```bash
  ffmpeg -i salida.mp4 -af "highpass=f=2000,volumedetect" -f null -
  ```

#### GSAP y HyperFrames

**`expo.in` en las salidas parece tiempo muerto.** Concentra casi todo el
recorrido en el tramo final: una salida de 0.75 s se pasa medio segundo sin que
se note nada y luego pega un tirón. **Usar `power2.in`.** Esta fue la causa de
fondo de la queja de «tiempos muertos», y afectaba a los seis planos.

**GSAP no interpola un `radial-gradient`.** Animar `background` entre dos
gradientes hace visible la caja rectangular del elemento. Se resuelve con capas
apiladas que se cruzan por opacidad.

**Dos `fromTo` sobre el mismo elemento.** El «from» del último se convierte en el
estado de reposo al buscar por tiempo. O se añade `immediateRender: false`, o se
usa `.to` cuando el CSS ya parte del valor correcto (p. ej. una rotación desde 0).

**Dubai necesita `line-height` ≥ 1.5.** Su caja de línea mide ~1.45em; por debajo
de eso las líneas se pisan y el verificador lo marca como texto ilegible.

**Determinismo, sin excepciones.** Nada de `repeat: -1`, `yoyo`, `Math.random()`,
`Date.now()` ni estado en `onUpdate`. El render busca por tiempo y tiene que dar
lo mismo siempre. Una sola timeline pausada por composición, registrada en
`window.__timelines["id"]`.

**Un `<video>` dentro de un comentario CSS** rompe la expresión regular del
ensamblador y se traga la etiqueta buena.

**El Studio anota los archivos** con `data-hf-id` al vuelo. Parar la vista previa
(`npx hyperframes preview --stop`) antes de escribir, o las escrituras fallan por
«archivo modificado».

#### El verificador

**No silenciar avisos en bloque.** En la v2 se marcaron 40 errores de
`content_overlap` como intencionales y eran ciertos: los textos quedaban
ilegibles en el render. La forma honesta de comprobar que algo está resuelto es
**retirar las supresiones y ver si el error vuelve**.

`data-layout-allow-overlap` **no se hereda**: hay que ponerlo en el bloque de
texto y también en los `<b>`/`<i>` de dentro.


#### Trampas que no dan ningún error (añadidas el 18 de septiembre)

Todas estas pasaron la validación, terminaron el render sin fallo y **solo se
detectaron mirando los fotogramas**. Son la familia más cara de bugs.

**Un elemento elevado a la raíz lleva tiempos GLOBALES y no se mueve con su
plano.** El video aprobado que el ensamblador saca a la raíz del `index.html`
tiene su propio `data-start` absoluto. Al recortar los planos se recolocaron
`el-<plano>` y `el-<plano>-voice` con una expresión regular, pero el elemento se
llamaba `el-s05-prueba-video-4` y no coincidía: quedó anclado al montaje viejo y
entraba 3.3 s tarde, con la tarjeta saliendo vacía en pantalla.
→ Al recolocar planos, **auditar TODOS los `data-start` del index**, no solo los
que siguen el patrón de nombres esperado.

**Ese mismo elemento hereda la escala de su tarjeta pero NO su opacidad.** Al
cerrar el plano todo se desvanecía menos la captura, que se cortaba de golpe a
brillo pleno. Se arregla dándole en la timeline raíz la misma curva de salida
que usa su contenedor.

**El Studio reescribe los archivos mientras la vista previa está abierta.**
Añade atributos `data-hf-id` y normaliza los que ya existen. Un anclaje de texto
que funcionaba deja de coincidir en silencio: el CSS y los tweens entraron, el
bloque HTML no, y **GSAP animando un elemento inexistente no da error**. El
verificador pasó con cero errores y el render salió sin el elemento.
→ Parar la vista previa antes de escribir, y anclar por `id` con expresión
regular, nunca por la línea completa.

**Nunca silenciar avisos del verificador en bloque.** Se marcaron 40 errores de
`content_overlap` como intencionales y eran ciertos: los textos salían
ilegibles. La forma honesta de comprobar que algo está resuelto es **retirar las
supresiones y ver si el error vuelve**.

#### Los colores de un manual no siempre pasan el contraste

El manual de Yezid Ricaurte está pensado para papel. Sobre cristal oscuro, su
oliva `#80804a` da **1.75:1** y su tierra `#cdb5a2` da **2.99:1**, contra el
mínimo de 3:1. La solución no es abandonar la paleta: se crean variantes
aclaradas **solo para texto** y el color de marca se conserva intacto en reglas,
acentos y elementos gráficos.

#### Página y manual pueden no coincidir

`yezidricaurte.com` usa Cormorant Garamond + Montserrat sobre `#001217` con
escala dorada. Su manual fija Dubai y la paleta verde/tierra. **Son dos sistemas
distintos.** No es un error de nadie: es una decisión que tiene que tomar el
cliente, y hay que planteársela en vez de mezclar mitad y mitad.

#### El acento de ElevenLabs es una propiedad de la voz

No hay un parámetro que lo module. Para cambiarlo hay que cambiar de voz:
`tools/probar-voces.py` genera la misma frase con varias para comparar a ciegas.
Ojo: la misma frase dura entre **6.5 y 9.9 s** según la voz, así que cambiarla
obliga a regenerar la locución y recolocar las animaciones.

Y el cuerpo de la petición va en **UTF-8 explícito**: con `curl` y acentos, la
API responde `400 invalid_unicode`. Por eso se manda desde Python.

#### OneDrive revirtió el repositorio entero

Además de borrar archivos, el 17 de septiembre **devolvió la carpeta a un estado
de horas antes**: el HEAD local retrocedió seis commits y se perdió un proyecto
completo que nunca se había confirmado. Lo único que salvó el trabajo fue
GitHub.
→ **Clonar fuera de OneDrive, y hacer commit ANTES de renderizar.** Un render
tarda dos minutos; reconstruir un proyecto entero, una hora.

---

### 3. Cómo se mide un «tiempo muerto»

No a ojo. Diferencia entre fotogramas consecutivos, promediada por ventanas:

```bash
ffmpeg -i video.mp4 -vf "tblend=all_mode=difference,signalstats,\
metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -
```

Por debajo de ~0.35 la imagen se lee como parada; 0.0 es un fotograma idéntico
al anterior.

**Dos avisos sobre esta medida**, aprendidos a base de equivocarse:

1. **Promedia todo el cuadro.** Un elemento pequeño moviéndose apenas la mueve.
   Hay que **mirar también los fotogramas**, no solo el número.
2. **Un texto que aparece solo por opacidad casi no cambia píxeles** aunque se
   vea perfectamente. Si hace falta movimiento, que además se desplace.

Lo que de verdad quita tiempos muertos, por orden de impacto:

1. **Recortar cada plano a su locución más una respiración.** En la v1 la voz
   ocupaba 25 de 37.5 s; sobraban 12 s de relleno.
2. **Repartir las salidas** (`power2.in`, no `expo.in`).
3. **Deriva continua del contenido**, con `ease: "none"` — cualquier otra curva
   deja tramos casi quietos. Mueve mucho más que la del fondo, porque el texto
   tiene bordes duros y un degradado suave casi no cambia píxel a píxel.

Resultado en esta pieza: de **44 ventanas muertas de 76** a **19 de 67**, y el
mínimo de 0.008 (fotograma congelado) a 0.120.

---

### 4. Método de producción

**Renderizar el esqueleto antes de montar contenido.** La v2 se construyó así y
destapó dos defectos de arquitectura con 30 líneas de GSAP y cuatro minutos de
render, en vez de con la pieza entera montada.

**La locución manda sobre el montaje.** Se pide con timestamps por carácter
(`/v1/text-to-speech/{id}/with-timestamps`) y cada aparición se coloca sobre la
palabra que la nombra. Nunca se estima.

`tools/voz-eleven.py` **falla si una línea no cabe en su plano**, en vez de que
se descubra en el MP4 final. El tope de cada plano es su corte, no el arranque
de la animación de salida: que la cola de una frase monte sobre la transición es
justo lo que evita que suene a trozos pegados.

**Para una voz más humana:** `stability` 0.32 (no 0.5), `style` 0.45, y la
velocidad afinada por plano. Con 0.5 el modelo lee plano y apresurado.

**Los efectos nunca caen encima de una palabra clave.** El golpe grave del gancho
se adelantó a 1.45 s para dejar sonar «¿Seguro?» a 1.53 s.

#### La identidad

**Contra `docs/marcas/riskmann/`, nunca contra lo que hizo la pieza anterior.** La receta
`riskmann-hud` que heredan los proyectos nuevos según `CLAUDE.md` **no
corresponde al manual oficial**. Sigue sin resolverse.

Los PDF están en el repo a propósito: antes vivían solo en Drive, se leían una
vez y sus valores se transcribían a mano a un `frame.md`. Cuando ese archivo se
perdió, la identidad se perdió con él.

`pdftotext` solo saca cadenas. El caballero, los dos anillos concéntricos
cian + dorado y la mezcla de pesos tipográficos dentro de una misma frase **solo
se ven mirando las páginas**, y son lo que define el aire de la marca.

#### La regla que manda

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**
Ni cifras, ni afirmaciones normativas, ni nombres de módulo.

> ⚠️ **Sin resolver:** la landing dice «11 o más vehículos» y también «diez (10)
> unidades». La pieza usa once. Hay que confirmar cuál es el umbral y de qué
> norma sale antes de dar la locución por buena.

---

### 5. Comandos del día a día

```bash
# validar SIEMPRE antes de renderizar — 0 errores y 0 avisos
npm run check

npm run render
npx hyperframes preview --background     # vista previa persistente
npx hyperframes preview --status
npx hyperframes preview --stop

# audio, desde la carpeta del proyecto
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14
python ../../tools/mezcla.py tools/etapa-sfx1.json
python ../../tools/mezcla.py tools/final-A.json

# pegar la mezcla al MP4
ffmpeg -i render.mp4 -i assets/mezcla-A.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -ac 2 -shortest salida-A.mp4
```

**Scripts largos a un archivo, no a un heredoc.** Los heredocs de bash se
atragantan pasados ~100 líneas y fallan con «unexpected EOF».

**Cuidado con `print()` y caracteres fuera de cp1252** (flechas, guiones largos):
revientan en la consola de Windows.

---

<a id="cap-9"></a>

## 9. Plataforma: ideas y decisiones

> Fuente: [`docs/PLATAFORMA.md`](PLATAFORMA.md) — se edita ahí, no aquí.

> **Qué es esto.** El documento vivo donde se discute en qué se puede convertir este
> repositorio: de «colección de proyectos que producen videos» a «motor que produce
> videos a partir de contenido y configuración». No describe lo que ya existe —eso es
> el [`PLAYBOOK.md`](#cap-5)—, sino hacia dónde ir, con qué pruebas y qué se decidió.
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

### 1. Punto de partida medido (26-sep-2026)

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

### 2. Lo que el análisis externo acierta

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

### 3. Dónde hay que matizarlo o corregirlo

#### 3.1 Son dos negocios, no uno

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

#### 3.2 No reconstruir la infraestructura de render

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

#### 3.3 Un formato intermedio por familia, no uno universal

El `video.json` universal es atractivo, pero diseñarlo antes de tiempo congela
decisiones que todavía no se entienden:

- **Familia A** ya tiene formato intermedio: `curso.json` (láminas → formas → notas →
  frases). Lo que falta es **formalizarlo** (esquema validable) y recuperar quien lo produce.
- **Familia B** tiene su especificación en el propio HTML compuesto, más `narracion.json`,
  `SFX-CUES.md` y `mezcla-*.json`. Lo que se puede estandarizar ya son **esos tres
  archivos de configuración**, no la composición.

Primero dos esquemas que funcionen; la unificación, si hace falta, después.

#### 3.4 La trazabilidad de fuentes es el P0 que falta, y el diferenciador

El análisis la menciona como una validación más. Para este repositorio es **la regla que
manda** (`CLAUDE.md`) y hoy casi no está implementada (§1). En contenido normativo (PESV,
Resolución 20223040040595, umbrales de vehículos) una cifra sin fuente es un riesgo
legal para el cliente, no un defecto estético. El caso del umbral «11 o 10 vehículos»
(PLAYBOOK §9) lo demuestra.

**Propuesta:** que cada frase de `curso.json` y `narracion.json` lleve
`fuente: {archivo, pagina|lamina|url, cita}` y que el motor **se niegue a construir**
si falta. Eso es algo que un editor de video genérico no ofrece.

#### 3.5 La «capa de IA» ya existe: es el agente

El análisis deja la IA para la fase 5. En la práctica, Claude Code con las skills de
HyperFrames ya es la capa que planifica y compone: produjo todas las piezas de la
familia B. La pregunta no es cómo añadir IA, sino **qué parte del trabajo del agente se
convierte en motor determinista**. Criterio: todo lo que se repite tres veces igual
(render, mezcla, nivelado de voz, medición de tiempos muertos) pasa al motor; lo que se
decide distinto cada vez se queda en el agente.

#### 3.6 La web app y el multiempresa van después, pero ya están en el plan

Somos 2–3 personas y ~4 marcas (RiskMann, SOFU, Yezid Ricaurte, FEGIR). Usuarios,
roles, organizaciones, PostgreSQL, colas y almacenamiento cuestan meses y no resuelven
ninguno de los problemas medidos en §1.

Desde **D-02** (se ofrece para uso interno **y** a terceros) ya no son opcionales: son el
destino. Lo que no cambia es el orden: motor por CLI → uso interno medido → piloto con
un tercero como servicio asistido → API → interfaz. Vender una interfaz sobre un motor
que todavía tiene seis `render.mjs` distintos multiplica los problemas por cliente.

#### 3.7 Riesgos que el análisis no menciona

| Riesgo | Hecho | Qué hacer |
| --- | --- | --- |
| Dependencia de ElevenLabs | La clave del issue #3 caducó el 21-sep; las locuciones no van en git | Guardar las locuciones aprobadas fuera de git con respaldo; abstracción de proveedor de voz (Piper como alternativa ya existe) |
| Licencias | Segoe UI (Microsoft) en el repo; música con licencias distintas por plataforma | Ficha de licencia obligatoria por cada recurso (`*-LICENCIA.txt` ya existe en 2 proyectos) y el motor que la exija |
| Datos personales | `Documentos_contexto/` con correos reales fuera del repo | Política escrita de qué entra al repo y qué no, antes de tener más clientes |
| Pérdida de trabajo | OneDrive borró y revirtió el repo; el trabajo de `fegir` estuvo días sin subir | Commit y push antes de renderizar (PLAYBOOK §3.8); rama por persona y unión frecuente |
| Costo de render | Máquinas de 8 GB; render por partes | Medir minutos de render por minuto de video antes de dimensionar la nube |
| Historias reescritas | La rama de Juan se reescribió y dejó copias viejas en otras ramas (70 conflictos el 26-sep) | No reescribir ramas compartidas; unir con `merge` |

#### 3.8 Una hipótesis de producto más concreta

El análisis habla de un «video factory» genérico. Los datos apuntan a algo más acotado:
los cursos (moto, csm, ruta-segura) se entregaron **junto con banco de preguntas para la
plataforma** («video informativo del quiz de la plataforma»). Eso sugiere:

> **PPTX de capacitación → videos por módulo + banco de preguntas trazado a la fuente,
> listos para cargar en RiskMann Campus.**

Es una hipótesis, no una decisión: hay que confirmar con RiskMann/SOFU si ese es el
flujo que compran y cuánto vale (ver §6).

#### 3.9 Qué cambia al ofrecerlo a terceros (D-02)

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

### 4. Arquitectura objetivo (revisada)

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

### 5. Hoja de ruta con criterios de salida

Cada fase termina cuando se cumple su criterio, no en una fecha.

#### Fase 0 — Consolidar (ahora)

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

#### Fase 1 — Motor por CLI

Un comando por familia: `video curso build <curso.json> --marca riskmann` y
`video pieza mezcla|render|verificar <proyecto>`.
**Criterio:** alguien que no escribió el código produce un curso nuevo de punta a punta
desde un PPTX sin editar Python.

#### Fase 2 — Uso interno medido

Producir 2–3 encargos reales con el motor y anotar horas, costo de voz y minutos de
render por minuto de video. Cuenta de voz del servicio, no personal.
**Criterio:** números que permitan poner precio a las dos ofertas.

#### Fase 3 — Piloto con un tercero (servicio asistido)

Un cliente externo entrega su PPTX o su brief; el equipo produce con el motor y entrega
videos + informe de verificación. Cliente en su propia carpeta o repositorio.
**Criterio:** entrega aprobada por el cliente, costo real dentro del precio, ningún
recurso sin licencia transferible y ningún archivo de otro cliente en la pieza.

#### Fase 4 — API y cola

Endpoints sobre el motor y render en la nube de HyperFrames antes que servidores propios.
**Criterio:** un encargo de la familia A corre de punta a punta sin que nadie ejecute
comandos a mano.

#### Fase 5 — Interfaz y multiempresa para la familia A

Organizaciones, usuarios y roles; asistente paso a paso: PPTX → marca → voz → muestra de
15 s → aprobar → curso completo en 16:9 y 9:16. La familia B se sigue ofreciendo como
servicio asistido. **Criterio:** un cliente externo lo usa sin ayuda.

---

### 6. Preguntas abiertas para el equipo

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

### 7. Registro de ideas

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

### 8. Registro de decisiones

| # | Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- | --- |
| D-01 | 2026-09-26 | Documentar la visión de plataforma en este archivo, separada del playbook | El playbook describe lo que existe; este documento, lo que se propone | — |
| D-02 | 2026-09-26 | Se mantienen **las dos ofertas**: uso interno y venta a terceros | Decisión del equipo `fegir`. Consecuencias en §3.9: licencias, datos, aislamiento por cliente y costo por video pasan a ser requisitos; se añade un piloto con un tercero (fase 3) antes de la API | Equipo `fegir` |
| D-03 | 2026-09-26 | **Modelo de negocio y clientes nuevos, aparcados.** Primero, documentación y contexto muy específicos de las cuatro marcas actuales (SOFU, RiskMann, FEGIR, Dr. Yezid) y una ruta paso a paso antes de materializar | Construir sobre contexto completo, no sobre supuestos. La ruta está en [`PASO-A-PASO.md`](#cap-1) y el contexto en [`marcas/`](marcas/) | Equipo `fegir` |
| D-04 | 2026-09-28 | **Un documento maestro generado** (`docs/MAESTRO.md`, con `python tools/maestro.py`) y el material de cada marca en `docs/marcas/<marca>/` | Leerlo todo en un solo archivo sin perder los documentos fuente: cada uno se sigue editando por separado, no se rompen enlaces ni las ramas de otros. El manual de FEGIR estaba dentro de la carpeta de RiskMann | Equipo `fegir` |

---

<a id="cap-10"></a>

## 10. Anexos

---

<a id="cap-10-1"></a>

### 10.1. Bitácora del 17 y 18 de septiembre

> Fuente: [`docs/BITACORA-2026-09-17-18.md`](BITACORA-2026-09-17-18.md) — se edita ahí, no aquí.

Qué se produjo, qué se decidió y por qué, y qué quedó abierto. Las trampas
técnicas están aparte, en [`ARRANQUE-EN-OTRO-EQUIPO.md`](#cap-8).

---

#### Lo que quedó entregado

Ambos en `Desktop\TRABAJO_SOFU\ENTREGABLES-VIDEO\`, con copia fuera de OneDrive
en `C:\RESPALDO-RISKMANN-2026-09-17\`.

| Pieza | Archivo | |
| --- | --- | --- |
| **RiskMann — PESV** | `riskmann-pesv-vertical\riskmann-pesv-vertical-A.mp4` | 33.3 s · 1080×1920 |
| **Yezid — En Vivo** | `yezid-envivo-pesv\yezid-envivo-A-voz-efectos-musica.mp4` | 15 s · 1080×1920 |

Los MP4 y las locuciones **no van en git** por convención del repositorio. Los
MP4 se rehacen con `npm run render`; las locuciones **no**, si caduca la clave
de ElevenLabs.

---

#### RiskMann — PESV (`videos/riskmann-consulta-pesv-vertical/`)

Pieza vertical para redes, tres variantes de audio para A/B testing. El equipo
recomendó la **A** (voz + efectos + música) y sobre ella se trabajó.

##### Lo que se corrigió, en orden

**La música tapaba la voz.** Medido bus contra bus, frase por frase, la música
estaba entre 8 y 16 dB **por encima** de la voz en las trece frases. Dos causas
y ninguna era de volumen: la pista entraba por `pistas`, que desemboca en el
mismo `amix` que la locución y donde nada la aparta; y ElevenLabs entrega la voz
a −33 dB mientras una pista de catálogo viene a −14 dB. Se añadió `musica` a
`mezcla.py` y `tools/nivelar-voz.py`.

**«¿Seguro?» no se oía.** Carlos sí lo decía, pero en un archivo de 1.76 s para
la frase entera: caía atropellado a 1.08 s mientras el rótulo aterrizaba a 1.80,
y el golpe grave le pasaba por encima. Ahora la frase lleva pausa, la palabra
cae a 1.53 s, el rótulo aterriza con ella y el golpe se adelantó.

**Tiempos muertos.** Medido con diferencia entre fotogramas, **44 de 76 ventanas
estaban congeladas**, con mínimos de 0.008 — imagen idéntica al fotograma
anterior. Dos causas: los planos duraban más que su locución (la voz ocupaba
25 s de 37.5) y nada se movía entre golpe y golpe. Quedó en **33.3 s** con
deriva continua de fondo y de contenido. Resultado: 19 ventanas de 67.

**El video del producto entraba tarde y la tarjeta salía vacía.** Ver la sección
de trampas silenciosas del documento de arranque: es el caso del elemento
elevado a la raíz con tiempos globales.

##### Decisiones

- **Música:** Mixkit «Hip Hop 02», licencia de uso comercial sin atribución y
  sin restricción de plataforma. Se descartó la Biblioteca de Audio de YouTube
  porque solo licencia videos alojados en YouTube y esto va a Reels y TikTok.
- **Voz más humana:** `stability` 0.5 → 0.32 y `style` 0.45, con velocidad por
  plano. Con 0.5 el modelo lee plano y apresurado.
- **Identidad:** construida contra el manual oficial en PDF, no contra la receta
  `riskmann-hud`.

---

#### Yezid Ricaurte — En Vivo (`videos/yezid-envivo-pesv-autogestion/`)

Promo de 15 s del conversatorio del 3 de octubre. **La firma quien dicta el
evento, no una empresa**: FEGIR no aparece porque tampoco aparece en la página.

##### Decisiones que tomó el cliente

**Identidad: manda el manual.** La página del evento usa Cormorant Garamond +
Montserrat sobre `#001217` con escala dorada; el manual fija Dubai y la paleta
verde/tierra. Son dos sistemas distintos y se eligió el manual.
**Consecuencia consciente: el video no se parece a la página a la que manda la
gente.**

**Foco: el en vivo, no el PESV.** La primera versión explicaba la norma. Se
reorientó para que el protagonista sea el evento.

**Música:** Pixabay, pista «elegant» de atlasaudio. Licencia verificada contra
el resumen oficial: uso comercial permitido, sin atribución, **sin restricción
de plataforma**. Ficha en `assets/musica-LICENCIA.txt`.

##### Cómo está hecho

- Fondo `aurora-drift` del registro de bloques, con `--brand` inyectado para que
  las auroras sean del verde del manual.
- Motion con la regla `kinetic-beat-slam`: una rejilla de tempo única a 0.62 s,
  entradas **distintas** por tema, y un cronómetro que lee esa misma rejilla.
- La firma manuscrita se extrajo del propio manual en versión negativo, **sin
  redibujarla** — el manual lo prohíbe expresamente.
- Marco de construcción con esquinas, guiño a la página «Logo Construcción».

---

#### Lo que quedó abierto

**El umbral de vehículos.** La landing del PESV dice «11 o más vehículos» y
también «diez (10) unidades». La pieza usa once y **nadie lo ha confirmado**.
Contradice la regla del repositorio: nada entra si no se rastrea a un archivo
que entregó RiskMann, y aquí el propio archivo se contradice.

**La receta `riskmann-hud`** que heredan los proyectos nuevos según `CLAUDE.md`
**no corresponde al manual oficial**. Sigue sin resolverse: o se corrige, o se
deja de recomendar en el arranque.

**La clave de ElevenLabs del issue #3 caducaba el 21 de septiembre de 2026.**
Las locuciones no van en git, así que sin clave nueva no se pueden regenerar.

**La voz está sin decidir.** Hay siete muestras comparables en
`ENTREGABLES-VIDEO\pruebas-de-voz`, generadas con `tools/probar-voces.py`.
Cambiar de voz obliga a regenerar la locución y recolocar las animaciones,
porque la misma frase dura entre 6.5 y 9.9 s según la voz.

**Los videos del Drive del Dr. Ricaurte** no son accesibles con esta cuenta. Si
los comparten, se puede transcribir lo que dice y usar sus propias palabras en
el guion — valdría más que cualquier texto redactado.

**Limpieza pendiente** en `ENTREGABLES-VIDEO\riskmann-pesv-vertical\`: sigue
`PESV_V1.mp4` de 37.5 s, que es una versión antigua, y las variantes B y C que
el cliente no pidió actualizar.

---

#### El incidente de OneDrive

El 17 de septiembre OneDrive **borró archivos en caliente** del repositorio de
trabajo: pasó de 1556 a 367 y luego a 53 archivos en menos de dos horas, y se
llevó `.git/HEAD`, `.git/config` y toda la base de objetos.

El 18 hizo algo peor: **revirtió la carpeta a un estado de horas antes**. El
HEAD local retrocedió seis commits y desapareció un proyecto entero que nunca se
había confirmado.

Lo único que salvó el trabajo fue **GitHub**. Desde entonces se trabaja en
`C:\dev\riskmann2-marketing-videos` y se hace commit **antes** de renderizar.

---

#### Herramientas que se añadieron

| Archivo | Para qué |
| --- | --- |
| `tools/nivelar-voz.py` | Lleva una locución de TTS a nivel de emisión, a disco |
| `tools/probar-voces.py` | Genera la misma frase con varias voces para comparar |
| `videos/*/tools/margen-voz.py` | Mide el margen voz–música frase por frase |
| `tools/mezcla.py` | Ampliado: clave `musica` con ducking, y ocho lecciones en su cabecera |

---

<a id="cap-10-2"></a>

### 10.2. PoC Seguridad Vial para Pasajeros

> Fuente: [`docs/POC-SEGURIDAD-VIAL-PASAJEROS.md`](POC-SEGURIDAD-VIAL-PASAJEROS.md) — se edita ahí, no aquí.

Informe de la prueba de concepto: qué se entregó, cómo responde a cada punto del
issue y qué queda pendiente antes de la revisión con el CEO.

| | |
| --- | --- |
| **Entregable** | Módulo 01 «Actor vial» de la capacitación *Seguridad Vial para Pasajeros* |
| **Proyecto** | [`videos/pesv-m01-mando/`](../videos/pesv-m01-mando/) — formato «Centro de mando» |
| **Video** | MP4 1920×1080, 30 fps, **2:31**, con locución, efectos y cama musical · 39 MB |
| **Enlace para el CEO** | [Videos HyperFrames — Google Drive](https://drive.google.com/drive/folders/1PKZKu0SMgxrLslJFHqhBHAsHuTa-K8ig?usp=sharing) · archivo `01 - … Capacitacion completa narrada (2m31)` |
| **Versión corta** | [`videos/pesv-m01-ritmo/`](../videos/pesv-m01-ritmo/) — formato «Ritmo»: 60 s al compás de una pista, sin voz · 15 MB |
| **Motor** | [HyperFrames](https://github.com/heygen-com/hyperframes) 0.8.31 (HTML → MP4) |

---

#### 1. Checklist del issue

##### Análisis de insumos

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Revisar el manual de identidad (paleta, tipografía, lineamientos) | ✅ | Reglas del logo en [`PRODUCCION-VIDEOS.md` §0.1](#cap-6); paleta y Montserrat en §2 y en [`DIRECCION.md`](../videos/pesv-m01-mando/DIRECCION.md) |
| Analizar el video de referencia (transiciones, ritmo, estilo) | ⚠️ parcial | Se trabajó sobre las **capturas y la transcripción** entregadas; el video en Drive no fue accesible directamente (llegó por correo corporativo). Conviene que alguien del equipo lo compare lado a lado |
| Desglosar el PDF en escenas renderizables | ✅ | 8 planos con su texto y su tiempo en [`DIRECCION.md`](../videos/pesv-m01-mando/DIRECCION.md); locución por plano en [`tools/guion.json`](../videos/pesv-m01-mando/tools/guion.json), con la fuente citada |

##### Desarrollo / Animación

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Configurar el entorno con HyperFrames | ✅ | Proyecto con la CLI fijada a 0.8.31 en `package.json`; herramientas compartidas en [`tools/`](../tools/) |
| Maquetar y animar las escenas según el guion | ✅ | [`compositions/frames/01…08`](../videos/pesv-m01-mando/compositions/frames/) |
| Integrar marca, iconografía y textos clave | ✅ | Logo oficial como firma persistente y cierre; fotografía real gradada a la paleta; textos solo del PDF |

##### Render y entrega

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Renderizar el video final en HD (MP4) | ✅ | `npx hyperframes render --quality high` → 1920×1080, 151 s |
| Control de calidad visual y de timing | ✅ | `hyperframes check` → **Check passed** (0 errores de layout, 208/208 textos con contraste WCAG AA); revisión de fotogramas de cada plano; voz verificada en el MP4 final (banda >400 Hz: −22.9 dB) |
| Subir la entrega y preparar demo para el CEO | ✅ | Videos en la [carpeta compartida de Drive](https://drive.google.com/drive/folders/1PKZKu0SMgxrLslJFHqhBHAsHuTa-K8ig?usp=sharing) |

---

#### 2. Criterios de aceptación

| Criterio | Estado |
| --- | --- |
| Video renderizado completo del módulo | ✅ Módulo 01 completo, 2:31 |
| Cumplimiento estricto del manual de identidad | ✅ Solo el archivo oficial del logo, sin redibujar, re-letrar, recolorear ni tapar; área de reserva libre; paleta y tipografía de marca |
| Consistencia visual y de ritmo con el video de referencia | ⚠️ Validada contra las capturas entregadas; falta la comparación directa con el video (§1) |
| Enlace compartido y listo para feedback del CEO | ✅ [Carpeta compartida de Drive](https://drive.google.com/drive/folders/1PKZKu0SMgxrLslJFHqhBHAsHuTa-K8ig?usp=sharing) |

---

#### 3. Cómo se llegó a este formato

La dirección final salió de cinco iteraciones con feedback. Los prototipos descartados
no están en el repositorio; se conservan como archivo local del equipo.

| Iteración | Resultado |
| --- | --- |
| Réplica fiel de las diapositivas | Aceptada como base de contenido |
| Versión «plus» animada | Rechazada: seguía leyéndose como diapositiva; figuras de línea poco profesionales |
| Refactor con fotografía real | Superada: «muy básico, no hay nada de destaque» |
| **«Centro de mando»** (identidad del video de marca RiskMann + fotos en monitores) | **Aprobada** sobre una muestra de 16 s con sonido y ampliada a los 8 planos |

Estructura del video: apertura (el logo se arma y pasa a firma) · corresponsabilidad ·
cada rol · tres deberes · principio clave · ruta de 8 módulos · retroalimentación con
pausa · cierre con pie legal.

**Regla de veracidad aplicada:** ninguna frase, en pantalla ni en la voz, sale de fuera
del PDF entregado. No hay cifras ni afirmaciones normativas añadidas; el cierre incluye el
pie legal del documento.

---

#### 4. Viabilidad técnica (lo que responde el PoC)

| Pregunta | Respuesta medida |
| --- | --- |
| ¿Se puede producir con herramientas sin licencia de pago? | Sí: HyperFrames (código abierto), locución local con Piper, efectos y fotos con licencia Pixabay (uso comercial sin atribución), cama musical sintetizada |
| ¿Cuánto cuesta el render? | ~9 min 30 s en un portátil para 151 s de video |
| ¿Cuánto cuesta un módulo? | El primero, varios días de iteración para definir el formato. Los siguientes reutilizan la plantilla, el cromo, la mezcla y la voz: solo cambian el guion y los planos de contenido (procedimiento en [`PRODUCCION-VIDEOS.md` §10.5](#cap-6)) |
| ¿Es reproducible por otra persona? | Sí: el render es determinista y todo el proceso está documentado. Prompts probados en [`GUIA-PROMPTS.md`](#cap-7) |

---

#### 4b. Segunda versión: «Ritmo»

Tras aprobar el «Centro de mando» se probó hasta dónde llega el movimiento del framework:
el mismo módulo como pieza de **60 s sin voz**, con animaciones que la serie no había
usado (tipografía al compás, trazos a mano, tarjetas 3D, rodillo tipo tragamonedas, forma
que se transforma entre escenas) y una pista rítmica sintetizada a 120 BPM. Aprobada sin
cambios. Render: 4 min 02 s. Sirve como gancho junto al módulo completo; el procedimiento
para repetirla en otros módulos está en [`PRODUCCION-VIDEOS.md` §13](#cap-6).

#### 5. Pendientes y siguientes pasos

1. ~~Subir los MP4 a Drive~~ — hecho: enlace arriba y en el README.
2. Comparar el video con la referencia en producción (alguien con acceso al Drive corporativo).
3. Revisión con el CEO → ajustes.
4. Escalar a los módulos 02–08 con la plantilla.
5. Fuera de este PoC: corregir el video de marketing *Sala de control* (incumple el manual
   de marca y contiene una cifra no respaldada) y evaluar una interfaz para que otras
   áreas generen videos.

---

#### 6. Reproducir el video

```bash
cd videos/pesv-m01-mando
npm run check            # validación completa
npm run render -- --quality high --output renders/pesv-m01-mando.mp4 --browser-timeout 180
```

Requisitos: Node.js y ffmpeg. La mezcla de audio ya va incluida
(`assets/mezcla-modulo.wav`); para regenerarla o narrar un módulo nuevo, ver
[`PRODUCCION-VIDEOS.md` §11](#cap-6).

---

<a id="cap-10-3"></a>

### 10.3. Lectura del manual de RiskMann

> Fuente: [`docs/marcas/riskmann/LEEME.md`](marcas/riskmann/LEEME.md) — se edita ahí, no aquí.

Los dos PDF de este directorio son **la fuente oficial** de la identidad
RiskMann. Vienen del Drive del equipo, enlazado en el issue #3:
`drive.google.com/drive/folders/1aVqnKAcIEWEn-Bvrcdb48Twe6yoSMip0`
→ carpeta «Manuales de Identidad».

Están **dentro del repo a propósito**. Antes vivían solo en Drive: se leían una
vez, sus valores se transcribían a mano al `frame.md` de un proyecto y a partir
de ahí nadie podía verificar nada sin volver a Drive. Cualquier pieza nueva se
contrasta contra estos archivos, no contra lo que hizo la pieza anterior.

#### Para leerlos como imagen (recomendado)

`pdftotext` extrae las cadenas pero **pierde el diseño**: los swatches de color,
las proporciones del isotipo y los ejemplos de uso incorrecto son imágenes. Para
verlos hace falta `pdftoppm`, que este equipo no tiene todavía:

```
winget install --id oschwartz10612.Poppler -e
```

Ya instalado (`oschwartz10612.Poppler`). El binario **no queda en el PATH** que
winget anuncia; vive en:
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*\poppler-*\Libraryin`

El PDF es **una sola pagina de 2200 x 10269 pt**, asi que hay que trocearla en
bandas para leerla:

```bash
pdftoppm -png -r 70 -x 0 -y <desplazamiento> -W 2139 -H 1660 manual.pdf banda
```

#### Lo que solo se ve mirando las paginas

Esto no lo da `pdftotext` y es justo lo que define el aire de la marca:

- **El caballero es fotografia real**, no ilustracion: cota de malla, yelmo,
  espada y escudo, en monocromo casi negro, iluminacion baja y dramatica.
- Alrededor del caballero hay **dos anillos concentricos**: uno grueso en cian
  `#06c7fb` y otro fino en dorado `#c8951a`. Es un motivo propio de la marca,
  una lente o portal que enmarca al sujeto.
- **La tipografia mezcla pesos dentro de una misma frase**: Bold en las palabras
  que cargan el mensaje y Light en los conectores.
  «RiskMann **es una** solucion digital **para gestionar** riesgos **de forma**
  simple, segura **y** conforme **a la** normativa.»
  Es un recurso de enfasis de la marca, no una licencia tipografica.
- El lockup del logo lleva **«by SOFU»** bajo el nombre.

#### Lo que fija el manual

**Paleta general**

| Hex | Uso que indica el manual |
| --- | --- |
| `#020202` | Fondo principal |
| `#c8951a` | Toques de prestigio y detalles |
| `#06c7fb` | Detalles decorativos, gráficos acento |
| `#272725` | Separadores, fondos secundarios |

**Paleta del isotipo**

| Hex | Uso que indica el manual |
| --- | --- |
| `#333366` | Círculos del isotipo, elementos tecnológicos |
| `#FF3333` | Énfasis, alertas, botones |
| `#26367D` | Color institucional secundario o de soporte |
| `#FFFFFF` | Contraste, espacios negativos |

**Tipografía:** Dubai Bold para títulos, Dubai Regular para cuerpo.

**Estilo visual declarado** — esto no es decoración, es la dirección creativa
que el manual pide y que la v1 no usó:

> «Inspirado en las figuras de los caballeros medievales, transmiten una imagen
> de defensa, integridad y compromiso frente a los riesgos empresariales.»

- El caballero = el rol protector de la marca: firme, preparado y ético.
- Azul oscuro = profesionalismo y confianza · Negro = elegancia y autoridad ·
  Gris claro = neutralidad · Dorado = prestigio y valor.
- Fotografía e ilustración: **escudos, armaduras, metáforas de protección y
  estrategia**.
- Diseño: limpio, ordenado, con énfasis en estructuras sólidas.

**Reglas duras del isotipo** (el manual las ilustra como usos incorrectos):
área de reserva libre alrededor, no deformar, no recolorear, no aplicar
opacidad, no girar, no ocultar, no poner nada encima, no reinterpretarlo.
Solo se usa el archivo oficial.

#### Advertencia sobre `riskmann-hud`

La receta congelada `riskmann-hud`, que heredan los proyectos nuevos según
`CLAUDE.md`, **no corresponde a este manual**. Se detectó al producir
`riskmann-consulta-pesv-vertical` y esa pieza se construyó contra el manual, no
contra la receta. Está sin resolver: o se corrige la receta, o se deja de
recomendar en el arranque de proyectos nuevos.

---

<a id="cap-10-4"></a>

### 10.4. README del repositorio

> Fuente: [`README.md`](../README.md) — se edita ahí, no aquí.

Repositorio dedicado a la elaboración de videos para presentaciones, marketing y capacitación de la plataforma RiskMann, producidos con [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4).

#### Documentación

| Documento | Para quién | Qué contiene |
| --- | --- | --- |
| [`docs/MAESTRO.md`](MAESTRO.md) | Quien quiere leerlo todo de corrido | Toda la documentación general en un solo archivo con índice (generado con `python tools/maestro.py`; no se edita) |
| [`docs/README.md`](#cap-0) | Todos, primero | Índice de la documentación, orden de lectura y cómo alimentarla |
| [`docs/marcas/`](marcas/) | Quien produce para una marca | Ecosistema, glosario y ficha de SOFU, RiskMann, FEGIR y Dr. Yezid Ricaurte |
| [`docs/PLAYBOOK.md`](#cap-5) | Quien arranca un proyecto nuevo | Qué se hizo, qué formato elegir, qué copiar, trampas principales y huecos conocidos |
| [`docs/POC-SEGURIDAD-VIAL-PASAJEROS.md`](#cap-10-2) | Revisión del PoC | Entregable, checklist del issue, criterios de aceptación, viabilidad y pendientes |
| [`GUIA-PROMPTS.md`](#cap-7) | Quien pide los videos (marketing, gerencia) | «Con este prompt consigo esto»: instrucciones probadas, tiempos y lo que no funciona |
| [`PRODUCCION-VIDEOS.md`](#cap-6) | Quien los produce (persona o agente) | El estándar: veracidad, marca, identidad visual, formatos, procedimiento, audio, trampas |
| `videos/<proyecto>/DIRECCION.md` | Quien construye un módulo | La dirección de arte normativa de ese video |
| [`videos/ruta-segura-m1/GUION-VOZ.md`](../videos/ruta-segura-m1/GUION-VOZ.md) | Quien graba la voz | El libreto del curso de ciclistas con la ventana de tiempo exacta de cada lámina |

#### Estructura

```
assets/                  material fuente compartido (marca, iconos, capturas, grabaciones)
  fotos-pixabay/         fotos candidatas ya revisadas para la serie PESV
docs/                    informes (PoC)
tools/                   voz.py · ritmo.py · mezcla.py · descargar-voz.py
video-presentacion/      pieza previa del equipo (12 s)
videos/
  pesv-m01-mando/        PoC «Seguridad Vial para Pasajeros» · Módulo 01, formato «Centro de mando» (con voz)
  pesv-m01-ritmo/        el mismo módulo en formato «Ritmo»: 60 s, al compás de una pista, sin voz
  pesv-m01-ritmo-vertical/  el «Ritmo» recompuesto en 9:16 para redes sociales
  pesv-m01-profundidad/  exploración: partículas por GPU y 3D con cámara (16:9)
  pesv-m01-profundidad-vertical/  la misma exploración en 9:16
  sofu-comercial/        comercial de SOFU BIC S.A.S. (68 s, 16:9)
  sofu-comercial-v2/     el comercial rehecho con gancho, golpe inicial y cierre (52 s, 16:9)
  sofu-comercial-v2-vertical/  la versión v2 en 9:16 para redes
  ruta-segura-m1/        curso «Ruta Segura» · apertura + módulo 1 (6:48)
  ruta-segura-m2/        curso «Ruta Segura» · módulo 2, bicicleta lista (3:43)
  ruta-segura-m3/        curso «Ruta Segura» · módulo 3, misión segura (3:43)
  ruta-segura-m4/        curso «Ruta Segura» · módulo 4, cierre y fuentes (2:08)
  riskmann-sala-de-control/  video de marketing de la plataforma (68 s)
  moto-curso/            generador del curso «Motociclista laboral seguro» (datos + plantillas)
  moto-apertura … moto-cierre/  los 15 videos generados de ese curso (40:47)
  csm-curso/             generador del curso «Conducción Segura y Manejo Defensivo»
  csm-apertura … csm-cierre/    los 15 videos generados de ese curso (~33 min)
```

#### Videos

Todos los videos terminados están en la carpeta compartida de Drive:
**[Videos HyperFrames — Google Drive](https://drive.google.com/drive/folders/1PKZKu0SMgxrLslJFHqhBHAsHuTa-K8ig?usp=sharing)**

| # | Archivo en Drive | Qué es | Proyecto |
| --- | --- | --- | --- |
| 01 | `Capacitacion completa narrada (2m31)` | Módulo 1 completo con voz — **entregable del PoC** | `videos/pesv-m01-mando/` |
| 01b | `Capacitacion completa (version liviana para compartir)` | El mismo 01, comprimido a 11 MB | `videos/pesv-m01-mando/` |
| 02 | `Resumen dinamico sin voz (1m00)` | Pieza corta de gancho, al compás de una pista | `videos/pesv-m01-ritmo/` |
| 02b | `Resumen dinamico vertical para redes (1m00)` | El mismo 02 en 9:16 para TikTok / Reels / Shorts | `videos/pesv-m01-ritmo-vertical/` |
| 03 | `Version presentacion fiel a las diapositivas (2m36)` | El módulo siguiendo el documento original | fuera del repo |
| 04 | `Presentacion de la plataforma - Video promocional (1m08)` | Marketing de RiskMann, sin sonido — *no usar comercialmente aún* | `videos/riskmann-sala-de-control/` |
| 04b | `Presentacion de la plataforma - Video promocional narrado (1m08)` | El mismo 04, con voz y música | `videos/riskmann-sala-de-control/` |
| 05 | `SOFU BIC SAS - Presentacion comercial de la empresa (1m08)` | Comercial de la casa matriz SOFU, a partir de su guion | `videos/sofu-comercial/` |
| 06 | `SOFU BIC SAS - Comercial dinamico (52s)` | El comercial rehecho: gancho, golpe inicial y cierre | `videos/sofu-comercial-v2/` |
| 06b | `SOFU BIC SAS - Comercial dinamico vertical para redes (52s)` | El mismo 06 en 9:16 | `videos/sofu-comercial-v2-vertical/` |
| 07 | `Ruta Segura - Modulo 1 Actor vial y Sistema Seguro - Narrado (6m48)` | Curso de ciclistas: apertura + módulo 1 | `videos/ruta-segura-m1/` |
| 08 | `Ruta Segura - Modulo 2 Bicicleta lista - Narrado (3m43)` | Inspección, clasificación, protección y visibilidad | `videos/ruta-segura-m2/` |
| 09 | `Ruta Segura - Modulo 3 Mision segura - Narrado (3m43)` | Anticipación, maniobra, ruta y estado, respuesta | `videos/ruta-segura-m3/` |
| 10 | `Ruta Segura - Modulo 4 Cierre - Narrado (2m08)` | Cierre y fuentes | `videos/ruta-segura-m4/` |
| — | `curso-motociclista/00 … 14` | Curso «Motociclista laboral seguro», 15 videos | `videos/moto-*` (generados por `videos/moto-curso/`) |
| — | `curso-conduccion-segura/00-1 … 13-1` | Curso «Conducción Segura y Manejo Defensivo», 15 videos | `videos/csm-*` (generados por `videos/csm-curso/`) |

El curso completo va con **locución sintética en voz colombiana** (ElevenLabs, «Carlos»,
`eleven_v3`). Cada módulo trae su copia liviana (`Nb`) y su `GUION-VOZ-modulo-N.md` con la
ventana de tiempo de cada lámina, por si se regraba con una persona.

Los archivos 01–03 empiezan por `NN - Seguridad Vial para Pasajeros - Modulo 1 Actor Vial - …` y
los 04 por `NN - RiskMann - …`; el número es el orden sugerido para verlos. Los nombres coinciden con los
de la carpeta de Drive.

Los MP4 **no se versionan** (cada render pesa decenas de MB): se generan con el comando
de abajo y se comparten por enlace. *Sala de control* está pendiente de corregir el logo
(manual de marca) y una cifra sin respaldo — ver `PRODUCCION-VIDEOS.md` §9.

#### Puesta en marcha

Requisitos: Node.js 18+, ffmpeg y Python 3.

```bash
cd videos/pesv-m01-mando
npm run check     # validación completa
npm run render -- --quality high --output renders/pesv-m01-mando.mp4 --browser-timeout 180
```

Solo para narrar o mezclar un módulo nuevo:

```bash
pip install piper-tts numpy
python tools/descargar-voz.py     # una vez: baja la voz aprobada (60 MB, fuera de git)
```

| Herramienta | Qué hace |
| --- | --- |
| `tools/voz.py` | Locución con la voz aprobada desde un guion JSON; avisa si una frase no cabe en su plano |
| `tools/ritmo.py` | Pista rítmica sintetizada (bombo, platillos, palmas, bajo, acordes) a un BPM dado, para videos sin voz |
| `tools/mezcla.py` | Mezcla voz, pistas, cama y efectos desde un JSON; normaliza a −16 LUFS y verifica que el audio llegó |
| `tools/cortar-laminas.py` | Parte el MP4 de un módulo en piezas de ~1 min, cortando solo en frontera de lámina |
| `tools/unir-curso.py` | Une los módulos de un curso en un máster continuo, sin recodificar; avisa de los que van mudos |
| `tools/render-partes.py` | Renderiza las partes que faltan y salta las hechas: hace el lote reanudable en máquinas con poca RAM |
| `videos/ruta-segura-m1/tools/voz-eleven.py` | Locución con ElevenLabs (`eleven_v3`) pidiendo timestamps por carácter |
| `videos/ruta-segura-m1/tools/cronometro.py` | Traduce los tiempos de una locución a los de otra y recoloca todo el montaje |

---

<a id="cap-10-5"></a>

### 10.5. Instrucciones para agentes (CLAUDE.md)

> Fuente: [`CLAUDE.md`](../CLAUDE.md) — se edita ahí, no aquí.

Repositorio de videos de marketing y presentación de la plataforma RiskMann.
Los videos se producen con **HyperFrames** (HTML → MP4). Cada video vive en su
propio proyecto bajo `videos/`.

#### Antes de tocar nada

Para orientarte (qué se ha hecho, qué formato elegir, qué copiar) empieza por
[`docs/PLAYBOOK.md`](#cap-5). Luego **lee [`PRODUCCION-VIDEOS.md`](#cap-6) completo.** Es el estándar de
producción de la serie: identidad visual con valores exactos, estructura narrativa,
reglas técnicas duras, procedimiento y trampas ya documentadas. No es una guía
opcional — los nueve planos del primer video se ven como una sola pieza solo porque
comparten esas constantes.

#### La regla que manda

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**

Ni cifras, ni afirmaciones de cumplimiento normativo, ni nombres de módulo. Si el
material de entrada no lo trae, se pide por escrito o no se dice. El primer video
incumplió esto (afirma un «100%» inventado) y por eso la regla está escrita aquí.

«Sala de control» es un **concepto visual**, no un módulo de RiskMann. Los módulos
reales son los que tienen icono de portada: Espacios de trabajo, Control de personal,
Capacitaciones/Campus y Seguridad vial.

**El logo, solo con el archivo oficial** (manual de marca, §0.1): nunca redibujado,
re-letrado, recoloreado, deformado ni tapado. **Sin figuras humanas dibujadas** (§0.2).

#### Módulo de capacitación nuevo (serie PESV)

La plantilla aprobada es `videos/pesv-m01-mando/` («Centro de mando»). Se copia y se
sigue el paso a paso de **§10.5** de `PRODUCCION-VIDEOS.md`. Voz y mezcla con las
herramientas compartidas de `tools/` (§11):

```bash
python ../../tools/voz.py tools/guion.json          # locución davefx, avisa si no cabe
python ../../tools/mezcla.py tools/mezcla-modulo.json   # cama + voz + efectos, verificada
```

Primero la apertura con sonido para aprobar; luego el resto.

Para la **pieza corta sin voz** del mismo módulo (60 s al compás de una pista), la
plantilla es `videos/pesv-m01-ritmo/` y el procedimiento es **§13**:

```bash
python ../../tools/ritmo.py tools/ritmo-video.json      # pista a 120 BPM
python ../../tools/mezcla.py tools/mezcla-video.json    # pista + efectos, verificada
```

#### Curso a partir de un PPTX con notas de orador

La plantilla es `videos/ruta-segura-m1/` y el procedimiento es **§14** de
`PRODUCCION-VIDEOS.md`. Un video por módulo, montado sobre la duración **real** de
la narración: la locución se pide con timestamps por carácter y cada aparición cae
sobre la frase que la nombra. Las composiciones se generan:

```bash
set ELEVENLABS_API_KEY=...
python tools/voz-eleven.py <voice_id> eleven_v3   # locución + tiempos reales
python tools/construir.py                          # recoloca el video sobre esa voz
python tools/pista.py                              # máster de voz, verificado
python tools/guion.py                              # GUION-VOZ.md con ventanas absolutas
```

`tools/cronometro.py` traduce los tiempos de una locución a los de otra, así que
cambiar de voz —o grabarla con una persona— no obliga a tocar ninguna marca de
tiempo. Sin `tiempos-voz.json` el video se construye igual, mudo.

La voz del curso «Ruta Segura» es **«Carlos»** de ElevenLabs
(`4PN5DHmrfIgZksvIrawS`), colombiana, modelo `eleven_v3`. La clave con permiso
`voices_read` permite buscar en la biblioteca: hay ~30 voces colombianas.

En una máquina con poca RAM el render va por partes y **reanudable**:

```bash
python tools/render-partes.py videos/<proyecto> [...]   # salta las partes ya hechas
python tools/unir-curso.py <carpeta-de-entrega> <salida.mp4>
```

#### Curso grande a partir de un PPTX (generado por plantillas)

Cuando el PPTX tiene muchas láminas con la misma anatomía, el curso se genera: la
plantilla es `videos/csm-curso/` (o `videos/moto-curso/`) y el procedimiento es **§15**
de `PRODUCCION-VIDEOS.md`.

```bash
python videos/csm-curso/tools/csm.py voz <clave>              # locución + tiempos por frase
python videos/csm-curso/tools/csm.py construir <clave>        # genera videos/csm-<clave>/; validar aquí
python videos/csm-curso/tools/csm.py construir <clave> --tramos
python tools/render-partes.py videos/csm-<clave>
python videos/csm-curso/tools/csm.py montar <clave>           # pega la voz y verifica duraciones
```

#### Empezar un video de marketing nuevo

```bash
npx hyperframes init "videos/riskmann-<modulo>" --non-interactive --example=blank --skill=product-launch-video
node ~/.claude/skills/media-use/scripts/recipe.mjs use --hyperframes . --name riskmann-hud
```

La receta `riskmann-hud` trae la identidad completa ya congelada. Copia también
`assets/fonts/` desde `videos/riskmann-sala-de-control/` — Montserrat necesita sus
archivos reales o el render sale con otra tipografía.

#### Estructura

- `assets/` — material fuente compartido de la plataforma (iconos de módulo, capturas,
  grabaciones de UI, logotipos). Para el cierre en fondo oscuro usa
  `public/riskmann_logo_blanco.png`; `riskmann_logo_central_blanco.svg` **no sirve**
  (es una ilustración a color).
- `videos/<proyecto>/` — un proyecto HyperFrames por video.
- `tools/` — herramientas compartidas: `voz.py` (Piper), `ritmo.py` (pista sintetizada), `mezcla.py` (ffmpeg) y
  `descargar-voz.py` (baja la voz aprobada a `tools/voces/`, que no va en git).
- `assets/fotos-pixabay/` — fotos candidatas ya revisadas para la serie PESV.
- **No van en git:** `renders/`, `snapshots/`, los MP4 y el modelo de voz (ver `.gitignore`).
  El video final se comparte por enlace.
- `GUIA-PROMPTS.md` — catálogo «con este prompt consigo esto», para quien pide los videos.
- `video-presentacion/` — pieza previa del equipo (12s), fuente de la copia aprobada:
  *«Automatiza y Controla el P.E.S.V.»*, *«Todo lo que necesitas en una sola plataforma»*.

#### Validar siempre antes de renderizar

```bash
npx hyperframes lint    # 0 errores
npx hyperframes check   # debe decir "Check passed"
npx hyperframes snapshot --at <puntos medios y ±0.1s de cada corte>
```

Revisa la hoja de contactos. Un plano en negro no se nota hasta ver el MP4 terminado.
