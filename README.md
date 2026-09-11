# riskmann2-marketing-videos
Repositorio dedicado a la elaboración de videos para presentaciones, marketing y capacitación de la plataforma RiskMann, producidos con [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4).

## Documentación

| Documento | Para quién | Qué contiene |
| --- | --- | --- |
| [`docs/POC-SEGURIDAD-VIAL-PASAJEROS.md`](docs/POC-SEGURIDAD-VIAL-PASAJEROS.md) | Revisión del PoC | Entregable, checklist del issue, criterios de aceptación, viabilidad y pendientes |
| [`GUIA-PROMPTS.md`](GUIA-PROMPTS.md) | Quien pide los videos (marketing, gerencia) | «Con este prompt consigo esto»: instrucciones probadas, tiempos y lo que no funciona |
| [`PRODUCCION-VIDEOS.md`](PRODUCCION-VIDEOS.md) | Quien los produce (persona o agente) | El estándar: veracidad, marca, identidad visual, formatos, procedimiento, audio, trampas |
| `videos/<proyecto>/DIRECCION.md` | Quien construye un módulo | La dirección de arte normativa de ese video |

## Estructura

```
assets/                  material fuente compartido (marca, iconos, capturas, grabaciones)
  fotos-pixabay/         fotos candidatas ya revisadas para la serie PESV
docs/                    informes (PoC)
tools/                   voz.py · ritmo.py · mezcla.py · descargar-voz.py
video-presentacion/      pieza previa del equipo (12 s)
videos/
  pesv-m01-mando/        PoC «Seguridad Vial para Pasajeros» · Módulo 01, formato «Centro de mando» (con voz)
  pesv-m01-ritmo/        el mismo módulo en formato «Ritmo»: 60 s, al compás de una pista, sin voz
  riskmann-sala-de-control/  video de marketing de la plataforma (68 s)
```

## Videos

| Video | Proyecto | Enlace |
| --- | --- | --- |
| PESV · Módulo 01 «Actor vial» — Centro de mando (2:31, con voz) | `videos/pesv-m01-mando/` | _pendiente_ |
| PESV · Módulo 01 «Actor vial» — Ritmo (1:00, sin voz) | `videos/pesv-m01-ritmo/` | _pendiente_ |
| RiskMann · Sala de control (1:08) | `videos/riskmann-sala-de-control/` | _pendiente_ |

Los MP4 **no se versionan** (cada render pesa decenas de MB): se generan con el comando
de abajo y se comparten por enlace.

## Puesta en marcha

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
