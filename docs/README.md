# Documentación — por dónde empezar

> Índice de todo lo escrito sobre el repositorio. Se lee en el orden de la tabla.

## Mapa de lectura

| # | Documento | Qué responde | Cuándo leerlo |
| --- | --- | --- | --- |
| 1 | [`PASO-A-PASO.md`](PASO-A-PASO.md) | ¿En qué punto estamos y qué sigue? | Siempre primero |
| 2 | [`contexto/ECOSISTEMA.md`](contexto/ECOSISTEMA.md) | ¿Quiénes son SOFU, RiskMann, FEGIR y el Dr. Yezid, y cómo se cruzan? | Antes de producir para cualquiera |
| 3 | [`contexto/marcas/`](contexto/marcas/) | Todo lo de una marca: fuentes, identidad, voz, CTA, lo producido, pendientes | Antes de producir para esa marca |
| 4 | [`contexto/GLOSARIO.md`](contexto/GLOSARIO.md) | ¿Qué significa PESV, lienzo propio, ducking…? | Cuando aparezca una palabra dudosa |
| 5 | [`PLAYBOOK.md`](PLAYBOOK.md) | ¿Qué formato elijo, qué copio y en qué orden trabajo? | Al arrancar un proyecto |
| 6 | [`../PRODUCCION-VIDEOS.md`](../PRODUCCION-VIDEOS.md) | Valores y reglas exactas de cada formato | Al construir |
| 7 | [`ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md) | Qué instalar y qué errores ya se pagaron | En un equipo nuevo o ante un error raro |
| 8 | [`PLATAFORMA.md`](PLATAFORMA.md) | Hacia dónde evoluciona esto; registro de ideas y decisiones | Al proponer o decidir algo |
| 9 | [`BITACORA-2026-09-17-18.md`](BITACORA-2026-09-17-18.md) | Qué se decidió en las piezas verticales de RiskMann y Yezid | Referencia |
| 10 | [`POC-SEGURIDAD-VIAL-PASAJEROS.md`](POC-SEGURIDAD-VIAL-PASAJEROS.md) | Qué se entregó en el PoC | Referencia |

Material de origen: [`marca/`](marca/) (manual de RiskMann), `marca-yezid/` (manual del
Dr. Yezid), `fuentes/` (documentos fuente de contenido).

## Cómo alimentar la documentación

| Llega… | Va a… |
| --- | --- |
| Un manual, guion, brief o PDF de un cliente | `docs/fuentes/<marca>/` (o `docs/marca*/` si es identidad) + una fila en «Fuentes oficiales» de su ficha |
| Un dato de una marca (color, CTA, lema, contacto) | Su ficha, **con la fuente**; si no la tiene, a «⚠ por confirmar» |
| Una decisión del cliente | «Decisiones tomadas» de su ficha, con fecha |
| Un término nuevo | `contexto/GLOSARIO.md` |
| Una idea para el motor o la plataforma | `PLATAFORMA.md` §7 (registro de ideas) |
| Una decisión del equipo | `PLATAFORMA.md` §8 (registro de decisiones) |
| Un error que costó tiempo | `ARRANQUE-EN-OTRO-EQUIPO.md` §2 y, si es de los grandes, PLAYBOOK §8 |
| Un paso terminado | Su estado en `PASO-A-PASO.md` y una fila en su registro de avance |
| Una marca nueva | Copiar `contexto/marcas/_PLANTILLA.md` y añadirla a `ECOSISTEMA.md` |

**Tres reglas:**

1. Todo dato lleva su fuente, o se marca **⚠ por confirmar**.
2. No se borra lo que cambió: se actualiza y se anota en el historial de la ficha.
3. Datos personales (correos, teléfonos de personas) **no** entran al repositorio.
