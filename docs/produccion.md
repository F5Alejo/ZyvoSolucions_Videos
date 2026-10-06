# El pipeline: del PPTX al MP4

Cómo trabaja Zyvo por dentro cuando alguien pulsa «✨ Crear mi video». Todo es local: archivos y
carpetas, ffmpeg y Chromium. Código: [`motor/produccion.py`](../motor/produccion.py).

## Las etapas

```
PPTX ─▶ Analizar ─▶ Plan ─▶ Voz ─▶ Escenas ─▶ Audio ─▶ Unir ─▶ Subtítulos ─▶ Control de calidad ─▶ MP4
         analisis   videospec  videospec  escenas/    (mezcla)   tmp/       .vtt .srt      qa.json     versiones/
         .json      .plan.json .json      <huella>.mp4
```

| Etapa | Qué hace | Lo que deja |
|---|---|---|
| Analizar (al subir) | Cuenta láminas, notas, imágenes, tablas y gráficos; tema, dificultad y avisos (`motor/analisis.py`) | `analisis.json` |
| Plan | Arma el [VideoSpec](videospec.md): escenas, narración, animación, cámara, transición, efectos y música | `videospec.plan.json` |
| Voz | Una frase a la vez, con caché por voz + texto; fija la línea de tiempo en cuadros exactos | `videospec.json`, `cache/voz/` |
| Escenas | Chromium dibuja la entrada y la salida de cada escena; ffmpeg sostiene lo del medio y aplica cámara y fundidos | `escenas/<huella>.mp4` |
| Audio | Voz + efectos de sonido + música con *ducking*, normalizado a -14 LUFS | (temporal) |
| Unir y subtítulos | Video + audio en el MP4; VTT y SRT; subtítulos dentro de la imagen si se pide | `<clave>.mp4`, `.vtt`, `.srt` |
| Control de calidad | Resolución, formato, sincronía, volumen, saturación, negros, silencios, textos y contenido; cada falla es un bug con código | `qa.json` |
| Versión | Guarda esta producción como `v001`, `v002`… (las últimas 5) | `versiones/` |

Todo queda en `datos/trabajos/<id>/` (no va a git: es material del cliente):

```
datos/trabajos/<id>/
├── entrada.pptx · trabajo.json · analisis.json
├── media/            imágenes del PPTX
├── cache/voz/ · cache/sfx/
├── logs/<clave>.jsonl   registro técnico
└── salida/<clave>/
    ├── videospec.plan.json · videospec.json · qa.json · estado.json
    ├── escenas/<huella>.mp4
    ├── <clave>.mp4 · <clave>.vtt · <clave>.srt
    └── versiones/v001/ …
```

## Estados

La cola (`motor/cola.py`) atiende un trabajo a la vez. Cada video tiene un `estado` (`en_cola`,
`produciendo`, `listo`, `error`) y una `fase`:

`QUEUED → SCRIPTING → SCRIPT_READY → GENERATING_AUDIO → AUDIO_READY → BUILDING_SCENES → SCENES_READY → RENDERING → RENDERED → QA_RUNNING → QA_PASSED | QA_FAILED → COMPLETED` (o `FAILED`).

La interfaz las traduce a pasos humanos («Generando narración…») en `frontend/src/generacion.ts`.

## Cuando algo falla

- Cada falla se clasifica (`motor/errores.py`): código (`TTS_001`, `RENDER_001`…), severidad y qué hacer.
- **Reintentos:** la voz hasta 3 veces y las escenas hasta 2, **solo** si la falla es pasajera (red, servicio caído, navegador que se cerró).
- **Respaldo de voz:** si ElevenLabs falla, todo el video se rehace con Kokoro y el informe lo dice. Nunca con Piper.
- **Nada se pierde:** lo que ya estaba hecho (voz y escenas) queda en caché; volver a producir solo rehace lo que falta.
- El detalle técnico va a `logs/<clave>.jsonl`; la interfaz lo muestra en «Modo diagnóstico».

## Regenerar por partes

- Si se cambia una lámina, **solo esa escena** se vuelve a dibujar (su huella cambió).
- «Regenerar esta escena» borra su caché aunque no haya cambiado.
- «Regenerar voz» borra el audio de las frases del video; las escenas no se tocan si la duración no cambia.
