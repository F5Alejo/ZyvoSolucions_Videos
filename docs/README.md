# Documentación — por dónde empezar

> Índice de todo lo escrito sobre el repositorio. Se lee en el orden de la tabla.
>
> **¿Lo quieres todo junto?** [`MAESTRO.md`](MAESTRO.md) reúne estos documentos en un solo
> archivo con índice. Es **generado**: no se edita; se editan los documentos de abajo y se
> reconstruye con `python tools/maestro.py`.

## Mapa de lectura

| # | Documento | Qué responde | Cuándo leerlo |
| --- | --- | --- | --- |
| 1 | [`PASO-A-PASO.md`](PASO-A-PASO.md) | ¿En qué punto estamos y qué sigue? | Siempre primero |
| 2 | [`marcas/ECOSISTEMA.md`](marcas/ECOSISTEMA.md) | ¿Quiénes son SOFU, RiskMann, FEGIR y el Dr. Yezid, y cómo se cruzan? | Antes de producir para cualquiera |
| 3 | [`marcas/<marca>/ficha.md`](marcas/) | Todo lo de una marca: fuentes, identidad, voz, CTA, lo producido, pendientes | Antes de producir para esa marca |
| 4 | [`marcas/GLOSARIO.md`](marcas/GLOSARIO.md) | ¿Qué significa PESV, lienzo propio, ducking…? | Cuando aparezca una palabra dudosa |
| 5 | [`PLAYBOOK.md`](PLAYBOOK.md) | ¿Qué formato elijo, qué copio y en qué orden trabajo? | Al arrancar un proyecto |
| 6 | [`../PRODUCCION-VIDEOS.md`](../PRODUCCION-VIDEOS.md) | Valores y reglas exactas de cada formato | Al construir |
| 7 | [`../GUIA-PROMPTS.md`](../GUIA-PROMPTS.md) | ¿Qué le pido al agente para conseguir cada cosa? | Al pedir un video |
| 8 | [`ARRANQUE-EN-OTRO-EQUIPO.md`](ARRANQUE-EN-OTRO-EQUIPO.md) | Qué instalar y qué errores ya se pagaron | En un equipo nuevo o ante un error raro |
| 9 | [`PLATAFORMA.md`](PLATAFORMA.md) | Hacia dónde evoluciona esto; registro de ideas y decisiones | Al proponer o decidir algo |
| 10 | [`BITACORA-2026-09-17-18.md`](BITACORA-2026-09-17-18.md) | Qué se decidió en las piezas verticales de RiskMann y Yezid | Referencia |
| 11 | [`POC-SEGURIDAD-VIAL-PASAJEROS.md`](POC-SEGURIDAD-VIAL-PASAJEROS.md) | Qué se entregó en el PoC | Referencia |

## Cómo están organizadas las carpetas

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

## Cómo alimentar la documentación

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
