# riskmann2-marketing-videos
Repositorio dedicado a la elaboración de videos para presentaciones, marketing y capacitación de la plataforma RiskMann, producidos con [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4).

## Documentación

| Documento | Para quién | Qué contiene |
| --- | --- | --- |
| [`docs/POC-SEGURIDAD-VIAL-PASAJEROS.md`](docs/POC-SEGURIDAD-VIAL-PASAJEROS.md) | Revisión del PoC | Entregable, checklist del issue, criterios de aceptación, viabilidad y pendientes |
| [`GUIA-PROMPTS.md`](GUIA-PROMPTS.md) | Quien pide los videos (marketing, gerencia) | «Con este prompt consigo esto»: instrucciones probadas, tiempos y lo que no funciona |
| [`PRODUCCION-VIDEOS.md`](PRODUCCION-VIDEOS.md) | Quien los produce (persona o agente) | El estándar: veracidad, marca, identidad visual, formatos, procedimiento, audio, trampas |
| `videos/<proyecto>/DIRECCION.md` | Quien construye un módulo | La dirección de arte normativa de ese video |
| [`videos/ruta-segura-m1/GUION-VOZ.md`](videos/ruta-segura-m1/GUION-VOZ.md) | Quien graba la voz | El libreto del curso de ciclistas con la ventana de tiempo exacta de cada lámina |

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
  pesv-m01-ritmo-vertical/  el «Ritmo» recompuesto en 9:16 para redes sociales
  pesv-m01-profundidad/  exploración: partículas por GPU y 3D con cámara (16:9)
  pesv-m01-profundidad-vertical/  la misma exploración en 9:16
  sofu-comercial/        comercial de SOFU BIC S.A.S. (68 s, 16:9)
  ruta-segura-m1/        curso «Ruta Segura» · apertura + módulo 1 (11:35, con locución)
  ruta-segura-m2/        curso «Ruta Segura» · módulo 2, bicicleta lista (7:20)
  ruta-segura-m3/        curso «Ruta Segura» · módulo 3, misión segura (7:08, sin voz)
  ruta-segura-m4/        curso «Ruta Segura» · módulo 4, evaluación y cierre (7:54, sin voz)
  riskmann-sala-de-control/  video de marketing de la plataforma (68 s)
```

## Videos

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
| 07 | `Ruta Segura - Modulo 1 Actor vial y Sistema Seguro - Narrado (11m35)` | Curso de ciclistas: apertura + módulo 1, con locución sintética — el libreto para regrabarla con una persona es [`GUION-VOZ.md`](videos/ruta-segura-m1/GUION-VOZ.md) | `videos/ruta-segura-m1/` |
| 07b | `Ruta Segura - Modulo 1 - Narrado (version liviana para compartir)` | El mismo 07, comprimido a 19 MB | `videos/ruta-segura-m1/` |
| 08 | `Ruta Segura - Modulo 2 Bicicleta lista - Narrado (7m20)` | Inspección preoperacional, clasificación de la bicicleta, protección y visibilidad | `videos/ruta-segura-m2/` |
| 08b | `Ruta Segura - Modulo 2 - Narrado (version liviana para compartir)` | El mismo 08, comprimido a 12 MB | `videos/ruta-segura-m2/` |
| 09 | `Ruta Segura - Modulo 3 Mision segura - SIN VOZ (7m08)` | Anticipación, maniobra en cinco pasos, inspección de ruta y estado, respuesta ante siniestro | `videos/ruta-segura-m3/` |
| 09b | `Ruta Segura - Modulo 3 - SIN VOZ (version liviana para compartir)` | El mismo 09, comprimido a 6 MB | `videos/ruta-segura-m3/` |
| 10 | `Ruta Segura - Modulo 4 Evaluacion final y cierre - SIN VOZ (7m54)` | Evaluación en cuatro partes, compromiso, clave, cierre y fuentes | `videos/ruta-segura-m4/` |
| 10b | `Ruta Segura - Modulo 4 - SIN VOZ (version liviana para compartir)` | El mismo 10, comprimido a 7 MB | `videos/ruta-segura-m4/` |

Los módulos **3** y **4** se entregan **sin locución**: la clave de ElevenLabs caducó a mitad del
trabajo y su montaje está hecho sobre una estimación de tiempos (`tools/estimar.py`, ajustada sobre
las 187 frases ya locutadas de los módulos 1 y 2). Cuando se locuten hay que **reconstruir y volver
a renderizar** — `cronometro.py` recoloca las marcas solo, pero el MP4 actual quedaría desfasado.

Los archivos 01–03 empiezan por `NN - Seguridad Vial para Pasajeros - Modulo 1 Actor Vial - …` y
los 04 por `NN - RiskMann - …`; el número es el orden sugerido para verlos. Los nombres coinciden con los
de la carpeta de Drive.

Los MP4 **no se versionan** (cada render pesa decenas de MB): se generan con el comando
de abajo y se comparten por enlace. *Sala de control* está pendiente de corregir el logo
(manual de marca) y una cifra sin respaldo — ver `PRODUCCION-VIDEOS.md` §9.

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
| `videos/ruta-segura-m1/tools/voz-eleven.py` | Locución con ElevenLabs (`eleven_v3`) pidiendo timestamps por carácter |
| `videos/ruta-segura-m1/tools/cronometro.py` | Traduce los tiempos de una locución a los de otra y recoloca todo el montaje |
