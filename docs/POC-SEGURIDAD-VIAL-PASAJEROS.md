# PoC · Renderizado de video animado con HyperFrames — «Seguridad Vial para Pasajeros»

Informe de la prueba de concepto: qué se entregó, cómo responde a cada punto del
issue y qué queda pendiente antes de la revisión con el CEO.

| | |
| --- | --- |
| **Entregable** | Módulo 01 «Actor vial» de la capacitación *Seguridad Vial para Pasajeros* |
| **Proyecto** | [`videos/pesv-m01-mando/`](../videos/pesv-m01-mando/) — formato «Centro de mando» |
| **Video** | MP4 1920×1080, 30 fps, **2:31**, con locución, efectos y cama musical · 39 MB |
| **Enlace para el CEO** | _pendiente: subir el MP4 a Drive y pegar aquí el enlace_ |
| **Motor** | [HyperFrames](https://github.com/heygen-com/hyperframes) 0.8.31 (HTML → MP4) |

---

## 1. Checklist del issue

### Análisis de insumos

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Revisar el manual de identidad (paleta, tipografía, lineamientos) | ✅ | Reglas del logo en [`PRODUCCION-VIDEOS.md` §0.1](../PRODUCCION-VIDEOS.md); paleta y Montserrat en §2 y en [`DIRECCION.md`](../videos/pesv-m01-mando/DIRECCION.md) |
| Analizar el video de referencia (transiciones, ritmo, estilo) | ⚠️ parcial | Se trabajó sobre las **capturas y la transcripción** entregadas; el video en Drive no fue accesible directamente (llegó por correo corporativo). Conviene que alguien del equipo lo compare lado a lado |
| Desglosar el PDF en escenas renderizables | ✅ | 8 planos con su texto y su tiempo en [`DIRECCION.md`](../videos/pesv-m01-mando/DIRECCION.md); locución por plano en [`tools/guion.json`](../videos/pesv-m01-mando/tools/guion.json), con la fuente citada |

### Desarrollo / Animación

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Configurar el entorno con HyperFrames | ✅ | Proyecto con la CLI fijada a 0.8.31 en `package.json`; herramientas compartidas en [`tools/`](../tools/) |
| Maquetar y animar las escenas según el guion | ✅ | [`compositions/frames/01…08`](../videos/pesv-m01-mando/compositions/frames/) |
| Integrar marca, iconografía y textos clave | ✅ | Logo oficial como firma persistente y cierre; fotografía real gradada a la paleta; textos solo del PDF |

### Render y entrega

| Tarea | Estado | Evidencia |
| --- | --- | --- |
| Renderizar el video final en HD (MP4) | ✅ | `npx hyperframes render --quality high` → 1920×1080, 151 s |
| Control de calidad visual y de timing | ✅ | `hyperframes check` → **Check passed** (0 errores de layout, 208/208 textos con contraste WCAG AA); revisión de fotogramas de cada plano; voz verificada en el MP4 final (banda >400 Hz: −22.9 dB) |
| Subir la entrega y preparar demo para el CEO | ⏳ | Falta subir el MP4 y compartir el enlace (§4) |

---

## 2. Criterios de aceptación

| Criterio | Estado |
| --- | --- |
| Video renderizado completo del módulo | ✅ Módulo 01 completo, 2:31 |
| Cumplimiento estricto del manual de identidad | ✅ Solo el archivo oficial del logo, sin redibujar, re-letrar, recolorear ni tapar; área de reserva libre; paleta y tipografía de marca |
| Consistencia visual y de ritmo con el video de referencia | ⚠️ Validada contra las capturas entregadas; falta la comparación directa con el video (§1) |
| Enlace compartido y listo para feedback del CEO | ⏳ Pendiente de subir |

---

## 3. Cómo se llegó a este formato

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

## 4. Viabilidad técnica (lo que responde el PoC)

| Pregunta | Respuesta medida |
| --- | --- |
| ¿Se puede producir con herramientas sin licencia de pago? | Sí: HyperFrames (código abierto), locución local con Piper, efectos y fotos con licencia Pixabay (uso comercial sin atribución), cama musical sintetizada |
| ¿Cuánto cuesta el render? | ~9 min 30 s en un portátil para 151 s de video |
| ¿Cuánto cuesta un módulo? | El primero, varios días de iteración para definir el formato. Los siguientes reutilizan la plantilla, el cromo, la mezcla y la voz: solo cambian el guion y los planos de contenido (procedimiento en [`PRODUCCION-VIDEOS.md` §10.5](../PRODUCCION-VIDEOS.md)) |
| ¿Es reproducible por otra persona? | Sí: el render es determinista y todo el proceso está documentado. Prompts probados en [`GUIA-PROMPTS.md`](../GUIA-PROMPTS.md) |

---

## 5. Pendientes y siguientes pasos

1. **Subir el MP4 a Drive** y pegar el enlace arriba y en el PR.
2. Comparar el video con la referencia en producción (alguien con acceso al Drive corporativo).
3. Revisión con el CEO → ajustes.
4. Escalar a los módulos 02–08 con la plantilla.
5. Fuera de este PoC: corregir el video de marketing *Sala de control* (incumple el manual
   de marca y contiene una cifra no respaldada) y evaluar una interfaz para que otras
   áreas generen videos.

---

## 6. Reproducir el video

```bash
cd videos/pesv-m01-mando
npm run check            # validación completa
npm run render -- --quality high --output renders/pesv-m01-mando.mp4 --browser-timeout 180
```

Requisitos: Node.js y ffmpeg. La mezcla de audio ya va incluida
(`assets/mezcla-modulo.wav`); para regenerarla o narrar un módulo nuevo, ver
[`PRODUCCION-VIDEOS.md` §11](../PRODUCCION-VIDEOS.md).
