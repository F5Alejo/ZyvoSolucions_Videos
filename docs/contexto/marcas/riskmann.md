# Ficha de marca — RiskMann

| Campo | Valor |
| --- | --- |
| Nombre legal / nombre de uso | RiskMann (producto de SOFU BIC S.A.S.; lockup «RiskMann by SOFU») |
| Qué es (una línea) | Plataforma digital de gestión de riesgos empresariales |
| Dominio principal | `riskmann.com` · aplicación en `app.riskmann.com` |
| Responsable del lado del cliente | ⚠ por confirmar |
| Última revisión de esta ficha | 2026-09-26 |

## 1. Quién es

- «Solución digital para gestionar riesgos de forma simple, segura y conforme a la
  normativa» (manual oficial, `docs/marca/LEEME.md`).
- **Módulos reales** (los que tienen icono de portada, `CLAUDE.md`): Espacios de trabajo,
  Control de personal, Capacitaciones/Campus y Seguridad vial.
- «Sala de control» **no** es un módulo: es un concepto visual de un video (`CLAUDE.md`).

## 2. Relación con las otras marcas

- Producto de **SOFU** (lockup «by SOFU»).
- Sus grabaciones de pantalla aparecen en las piezas del **En Vivo PESV** del Dr. Yezid
  Ricaurte («tu informe con un solo clic»). ⚠ El vínculo comercial no está documentado.

## 3. Fuentes oficiales

| Fuente | Tipo | Qué fija | Dónde está | Fecha |
| --- | --- | --- | --- | --- |
| Manual de identidad (claro y oscuro) | PDF | Paleta, Dubai, caballero, anillos, reglas del isotipo | `docs/marca/manual-identidad*.pdf` + lectura en `docs/marca/LEEME.md` | 2026-09-17 (traído al repo) |
| Manejo del PESV en 24 pasos | PDF | Contenido del publicitario PESV | `docs/fuentes/manejo-pesv-24-pasos.pdf` | 2026-09-18 |
| Landing consulta PESV | web | Copy y umbral de vehículos | `https://riskmann.com/consulta-pesv/` | leída ~2026-09-17 |
| Landing inspecciones gratis | web | Copy de 3 anuncios | `https://riskmann.com/inspecciones-gratis/` | leída 2026-09-23 |
| Landing capacitaciones | web | Copy del promo y la serie; identidad negro + dorado | `https://riskmann.com/capacitaciones` | 2026-09-26 |
| Logos oficiales | PNG | Cierre en fondo oscuro | `assets/public/riskmann_logo_blanco.png` (lockup), `riskmann_icono_blanco.png` (isotipo) | — |
| Iconos de módulo y grabaciones de UI | webp / mp4 | Material de producto | `assets/` | — |
| Drive «Manuales de Identidad» | Drive | Origen de los manuales | Enlace en el issue #3 | — |

## 4. Identidad visual

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

## 5. Voz y tono

- **Carlos** (ElevenLabs, colombiana) `4PN5DHmrfIgZksvIrawS`.
  - Narrado (`eleven_multilingual_v2`): `stability 0.32 · style 0.45`, velocidad por plano.
  - Vendedor (`eleven_v3`): `stability 0.15 · style 0.78 · speed 1.03`.
- Cursos «Ruta Segura»: Carlos con `eleven_v3`. Módulo PESV M01: Piper `es_ES-davefx-medium`.
- ⚠ **La voz de RiskMann sigue sin decidir** entre siete muestras (`BITACORA-2026-09-17-18.md`).
- Tono: tú, directo («¿Inspeccionas TODOS tus vehículos?»).

## 6. Dominio, CTA y datos de contacto

- CTAs literales de las landings: «Quiero mi inspección gratis», «Quiero activar
  Capacitaciones», «Quiero empezar ahora». Capacitaciones gratis **hasta el 1 de enero de 2027**.
- Entrada a la aplicación: `app.riskmann.com/entrada`. QR oficial en el promo de capacitaciones.

## 7. Lo producido

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

## 8. Decisiones tomadas

| Fecha | Decisión | Por qué | Quién |
| --- | --- | --- | --- |
| ≤ 2026-09-12 | Nada entra al video sin rastrearse a un archivo de RiskMann | Se coló un «100 %» inventado | Juan |
| 2026-09-17 | La identidad se construye contra el manual en PDF, no contra `riskmann-hud` | La receta no coincide con el manual | Alejandro |
| 2026-09-17 | Música de catálogo con licencia sin restricción de plataforma (Mixkit, Pixabay) | Las piezas van a Reels y TikTok | Alejandro |
| 2026-09-18 | Rojo reservado para «peligro» | Entrega del 18-sep | Cliente |
| 2026-09-26 | El promo y la serie de Capacitaciones usan la identidad de **la landing** (negro + `#AC841D`, Montserrat + Open Sans) | Quien vea el video y entre a la página la reconoce | Cliente |
| 2026-09-26 | El QR `qr-app-riskmann-com` (→ `app.riskmann.com/entrada`) es el mismo del brochure; va en el cierre de las piezas de Capacitaciones | Vía secundaria al botón cuando el video se proyecta | Equipo `fegir` |

## 9. Pendientes y ⚠ por confirmar

- [ ] **Umbral del PESV:** la landing dice «11 o más vehículos» y «diez (10) unidades».
- [ ] Rehacer o dejar de recomendar `riskmann-hud`.
- [ ] Manual frente a landing de capacitaciones: qué dorado y qué tipografía mandan.
- [ ] Elegir la voz oficial.
- [ ] Corregir o retirar «Sala de control».
- [x] Guardar en git el promo y la serie de capacitaciones (26-sep).
- [ ] Respuestas de las preguntas frecuentes de la landing de Capacitaciones (precio, validez del certificado).

## 10. Qué hay que pedirle al cliente

- [ ] Confirmación escrita del umbral de vehículos y la norma de la que sale.
- [ ] El storyboard «LANDING INSPECCIONES GRATIS» (no está ni en el repo ni en el Drive).
- [ ] Decisión sobre la identidad de las landings frente al manual.
- [ ] Nueva clave de ElevenLabs (la del issue #3 caducó el 21-sep-2026).

## 11. Historial de la ficha

| Fecha | Cambio | Quién |
| --- | --- | --- |
| 2026-09-26 | Ficha creada con lo que había en el repositorio | Equipo `fegir` (con Claude) |
