# Editar fegir-envivo en el Studio

```bash
npx hyperframes preview          # abre http://localhost:3002/#project/fegir-envivo
npx hyperframes preview --stop   # lo cierra
```

## Qué hay en la línea de tiempo

| Fila | Contenido |
|---|---|
| 1 y 2 | Las 5 escenas, alternadas (una fila por escena en `compositions/`) |
| 3 | Sello «EN VIVO · 3 OCT», todo el video |
| 10 | Voz de Carlos, una toma por frase |
| 11 y 12 | Efectos (cortina, visto, pop, golpe, hoja, brillo) |
| 13 | Música; su curva de volumen la baja bajo cada frase |

## Lo que conviene saber antes de tocar

- **Textos, colores y tamaños** de cada escena: en `compositions/escena-*.html`.
- **Mover una escena**: cambia su `data-start` y, dentro de su archivo, la
  variable `S` al mismo valor. Las animaciones van en tiempo global (`V`), así
  que siguen cayendo sobre la voz.
- **El orden de apilado** lo da el `z-index` de cada escena en `index.html`,
  no el número de fila.
- **Cambiar una frase** de la voz: `tools/narracion.json` →
  `python tools/voz-eleven.py 4PN5DHmrfIgZksvIrawS eleven_multilingual_v2` →
  `python tools/audio.py mezcla` (regenera las tomas niveladas).
- **No volver a correr** `tools/estudio.py`: reescribe `index.html` y
  `compositions/` y borraría lo editado.
- **Exportar** para redes: `npx hyperframes render -o renders/final.mp4` y
  luego normalizar a −14 LUFS:
  `ffmpeg -i renders/final.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5 -c:a aac -b:a 192k final-redes.mp4`
