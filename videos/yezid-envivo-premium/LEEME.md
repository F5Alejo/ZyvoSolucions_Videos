# En Vivo PESV · versión premium (yezidricaurte.com)

Una composición 1080×1920 de 12 s que sirve para las tres etapas de la campaña. **Los textos se editan en
`js/config.js`**: `pocos` («Faltan pocos días…»), `manana` («Es mañana») y `hoy` («Es hoy»).

```bash
python -m http.server 5530          # preview: http://localhost:5530/?v=pocos | manana | hoy
node tools/render.mjs --out <carpeta> [--variantes pocos,manana,hoy]
node tools/snap.mjs pocos salida.png 1.2 4.5 8.25   # hoja de contactos
```

| Archivo | Qué hace |
| --- | --- |
| `js/config.js` | textos, colores y tiempos de cada etapa (`*negrita*`, `_acento pálido_`) |
| `js/red.js` | Three.js: red de puntos conectados en 3D + gradiente líquido sutil; lee `fondoEstado` |
| `js/escena.js` | arma el DOM desde la configuración y el timeline GSAP (en pausa, seek-safe) |
| `js/main.js` | reproductor, `window.seekTo(t)` para render y voz de `assets/voz/<variante>.mp3` |

**Paleta** (yezidricaurte.com + manual de marca): petróleo `#001f26`, verde Yezid `#336666` (botón),
dorado `#d2b96a` (borde y filetes), amarillo pálido `#f1ecb0` (acentos y brillos). Sin rojo ni coral.
Es un video de la página del Dr. Yezid: nada de FEGIR.

**Voz:** cuando exista la locución, su MP3 va en `assets/voz/<variante>.mp3` y los segundos de
`tiempos` en `config.js` se reemplazan por los de ElevenLabs (`/with-timestamps`); la animación se
recoloca sola.
