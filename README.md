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
tools/                   voz.py · mezcla.py · descargar-voz.py
video-presentacion/      pieza previa del equipo (12 s)
videos/
  pesv-m01-mando/        PoC «Seguridad Vial para Pasajeros» · Módulo 01 — plantilla de la serie
  riskmann-sala-de-control/  video de marketing de la plataforma (68 s)
```

## Videos

| Video | Proyecto | Enlace |
| --- | --- | --- |
| PESV · Módulo 01 «Actor vial» (2:31) | `videos/pesv-m01-mando/` | _pendiente_ |
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
pip install piper-tts
python tools/descargar-voz.py     # una vez: baja la voz aprobada (60 MB, fuera de git)
```
