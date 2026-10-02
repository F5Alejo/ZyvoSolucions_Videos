# Audio: voz, música y efectos

La voz siempre manda: la música baja cuando alguien habla y los efectos suenan antes de que entre la voz.

```
VOZ (frase por frase) + EFECTOS (-26 dB) ─▶ pista ─▶ + MÚSICA (ducking) ─▶ normalizar a -14 LUFS ─▶ MP4
```

## Voz (`motor/voz.py`)

| Voz | Proveedor | ¿Se puede entregar? |
|---|---|---|
| Dora, Alex, Santa | Kokoro-82M, local (Apache 2.0) | Sí |
| Carlos y las de ElevenLabs | ElevenLabs, de pago (clave en `.env`) | Sí |
| Piper · davefx | Piper, local | **No**: solo borradores, con sello «BORRADOR» |

- Antes de leer, `motor/normalizar.py` pasa leyes, cifras, pesos, porcentajes y siglas a palabras
  («Ley 1503 de 2011» → «Ley mil quinientos tres de dos mil once»). Los subtítulos conservan el texto original.
- Cada frase se genera aparte y se guarda en caché por voz + texto: con ElevenLabs no se paga dos veces la misma frase.
- Un curso nuevo toma una voz que funcione en el equipo (Kokoro si no hay clave de ElevenLabs).
- Si ElevenLabs falla a mitad de camino, todo el video se rehace con Kokoro y el informe lo dice
  (se apaga con `audio.respaldo_voz`).

## Música

- Las pistas se suben en Configuración **con su licencia**, y opcionalmente su energía (calmada, media, enérgica).
- Si el curso no eligió pista y su estilo pide música, el director de música toma la primera con esa
  energía. Nunca baja música de internet. Se apaga con «Música» en Opciones (`audio.musica_estilo`).
- La música va en bucle con fundido de entrada y de salida y *sidechain*: baja unos 10 dB cuando habla la voz.

## Efectos de sonido (`motor/sfx.py`)

Whoosh, barrido suave, pop, clic, éxito, notificación, impacto y tecleo, **sintetizados con código**:
originales, idénticos en cada render y sin licencias que revisar. El director es sobrio: como mucho
uno por escena, nunca en la primera, a -26 dB (nunca más de -12 dB).

## Volumen final

Ganancia lineal más limitador a -2 dBFS, repetido hasta quedar a ±0,3 LUFS del objetivo (-14 para
YouTube y redes, -16 web, -23 TV), siempre medido en estéreo. El control de calidad revisa el volumen,
que el pico no pase de -0,1 dBFS (saturación) y que no haya silencios de más de 4 s.
