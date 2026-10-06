# Solución de problemas

Primero: **Configuración → Este equipo** dice qué falta (ffmpeg, navegador, voces, clave, Ollama, disco).
Si un video falló, en la pantalla del error abre **«Modo diagnóstico»**: muestra cada etapa, los
intentos y el código. El mismo registro está en `datos/trabajos/<id>/logs/<clave>.jsonl`.

## Por código de error

| Código | Qué pasó | Qué hacer |
|---|---|---|
| `PPTX_001` | No se pudo leer la presentación | Ábrela en PowerPoint y guárdala de nuevo como .pptx |
| `SPEC_001` | El plan del video no es válido | Revisa la presentación; un valor raro en un archivo editado a mano se cambia solo por el de por defecto |
| `TTS_001` | La voz no se puede usar en este equipo | Elige otra voz, o pon la clave de ElevenLabs en `.env`, o corre `python scripts/descargar_modelos.py` |
| `TTS_002` | El servicio de voz no respondió (ya se reintentó 3 veces) | Revisa la conexión e inténtalo de nuevo; con ElevenLabs, el video sale con Kokoro si el respaldo está activo |
| `RENDER_001` | No se pudo dibujar una escena | Inténtalo de nuevo; si se repite: `python -m playwright install chromium` |
| `AUDIO_001` / `VIDEO_001` | ffmpeg no pudo mezclar o unir | Revisa que `ffmpeg -version` funcione y que haya espacio en disco |
| `MOTOR_001` | Algo inesperado | Abre el modo diagnóstico y comparte el registro |

## Por bug del control de calidad (`qa.json["bugs"]`)

| Bug | Qué significa | Qué hacer |
|---|---|---|
| `AUDIO_003` | Silencio de más de 4 s | Casi siempre es una lámina sin notas del orador: escríbele narración |
| `TEXT_001` | Un texto no cabe | Acorta el título o las viñetas de esa escena |
| `CONTENT_001` | Falta una lámina o una imagen | Revisa que la imagen esté en el PPTX y no esté marcada como decorativa |
| `SYNC_001` / `AUDIO_002` / `AUDIO_004` | Imagen y voz desfasadas, volumen o saturación | Regenera la voz del video |
| `VIDEO_002` – `VIDEO_004` | Resolución, formato o pantalla negra | Regenera el video o la escena |

## Problemas conocidos del equipo

- **`instalar.ps1` se queda esperando:** en versiones viejas preguntaba la clave sin ventana; actualiza el repositorio.
- **Tildes dañadas en la terminal de Windows:** es la codificación de la consola, no el archivo.
- **El servidor se apaga solo** cuando lo lanza un asistente en segundo plano: ábrelo en su propia ventana.

Más casos, con su causa: [`hallazgos.md`](hallazgos.md).
