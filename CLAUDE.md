# riskmann2-marketing-videos

Repositorio de videos de marketing y presentación de la plataforma RiskMann.
Los videos se producen con **HyperFrames** (HTML → MP4). Cada video vive en su
propio proyecto bajo `videos/`.

## Antes de tocar nada

**Lee [`PRODUCCION-VIDEOS.md`](PRODUCCION-VIDEOS.md) completo.** Es el estándar de
producción de la serie: identidad visual con valores exactos, estructura narrativa,
reglas técnicas duras, procedimiento y trampas ya documentadas. No es una guía
opcional — los nueve planos del primer video se ven como una sola pieza solo porque
comparten esas constantes.

## La regla que manda

**Nada entra al video si no puede rastrearse a un archivo que entregó RiskMann.**

Ni cifras, ni afirmaciones de cumplimiento normativo, ni nombres de módulo. Si el
material de entrada no lo trae, se pide por escrito o no se dice. El primer video
incumplió esto (afirma un «100%» inventado) y por eso la regla está escrita aquí.

«Sala de control» es un **concepto visual**, no un módulo de RiskMann. Los módulos
reales son los que tienen icono de portada: Espacios de trabajo, Control de personal,
Capacitaciones/Campus y Seguridad vial.

**El logo, solo con el archivo oficial** (manual de marca, §0.1): nunca redibujado,
re-letrado, recoloreado, deformado ni tapado. **Sin figuras humanas dibujadas** (§0.2).

## Módulo de capacitación nuevo (serie PESV)

La plantilla aprobada es `videos/pesv-m01-mando/` («Centro de mando»). Se copia y se
sigue el paso a paso de **§10.5** de `PRODUCCION-VIDEOS.md`. Voz y mezcla con las
herramientas compartidas de `tools/` (§11):

```bash
python ../../tools/voz.py tools/guion.json          # locución davefx, avisa si no cabe
python ../../tools/mezcla.py tools/mezcla-modulo.json   # cama + voz + efectos, verificada
```

Primero la apertura con sonido para aprobar; luego el resto.

Para la **pieza corta sin voz** del mismo módulo (60 s al compás de una pista), la
plantilla es `videos/pesv-m01-ritmo/` y el procedimiento es **§13**:

```bash
python ../../tools/ritmo.py tools/ritmo-video.json      # pista a 120 BPM
python ../../tools/mezcla.py tools/mezcla-video.json    # pista + efectos, verificada
```

## Curso a partir de un PPTX con notas de orador

La plantilla es `videos/ruta-segura-m1/` y el procedimiento es **§14** de
`PRODUCCION-VIDEOS.md`. Un video por módulo, montado sobre la duración **real** de
la narración: la locución se pide con timestamps por carácter y cada aparición cae
sobre la frase que la nombra. Las composiciones se generan:

```bash
set ELEVENLABS_API_KEY=...
python tools/voz-eleven.py <voice_id> eleven_v3   # locución + tiempos reales
python tools/construir.py                          # recoloca el video sobre esa voz
python tools/pista.py                              # máster de voz, verificado
python tools/guion.py                              # GUION-VOZ.md con ventanas absolutas
```

`tools/cronometro.py` traduce los tiempos de una locución a los de otra, así que
cambiar de voz —o grabarla con una persona— no obliga a tocar ninguna marca de
tiempo. Sin `tiempos-voz.json` el video se construye igual, mudo.

La voz del curso «Ruta Segura» es **«Carlos»** de ElevenLabs
(`4PN5DHmrfIgZksvIrawS`), colombiana, modelo `eleven_v3`. La clave con permiso
`voices_read` permite buscar en la biblioteca: hay ~30 voces colombianas.

En una máquina con poca RAM el render va por partes y **reanudable**:

```bash
python tools/render-partes.py videos/<proyecto> [...]   # salta las partes ya hechas
python tools/unir-curso.py <carpeta-de-entrega> <salida.mp4>
```

## Empezar un video de marketing nuevo

```bash
npx hyperframes init "videos/riskmann-<modulo>" --non-interactive --example=blank --skill=product-launch-video
node ~/.claude/skills/media-use/scripts/recipe.mjs use --hyperframes . --name riskmann-hud
```

La receta `riskmann-hud` trae la identidad completa ya congelada. Copia también
`assets/fonts/` desde `videos/riskmann-sala-de-control/` — Montserrat necesita sus
archivos reales o el render sale con otra tipografía.

## Estructura

- `assets/` — material fuente compartido de la plataforma (iconos de módulo, capturas,
  grabaciones de UI, logotipos). Para el cierre en fondo oscuro usa
  `public/riskmann_logo_blanco.png`; `riskmann_logo_central_blanco.svg` **no sirve**
  (es una ilustración a color).
- `videos/<proyecto>/` — un proyecto HyperFrames por video.
- `tools/` — herramientas compartidas: `voz.py` (Piper), `ritmo.py` (pista sintetizada), `mezcla.py` (ffmpeg) y
  `descargar-voz.py` (baja la voz aprobada a `tools/voces/`, que no va en git).
- `assets/fotos-pixabay/` — fotos candidatas ya revisadas para la serie PESV.
- **No van en git:** `renders/`, `snapshots/`, los MP4 y el modelo de voz (ver `.gitignore`).
  El video final se comparte por enlace.
- `GUIA-PROMPTS.md` — catálogo «con este prompt consigo esto», para quien pide los videos.
- `video-presentacion/` — pieza previa del equipo (12s), fuente de la copia aprobada:
  *«Automatiza y Controla el P.E.S.V.»*, *«Todo lo que necesitas en una sola plataforma»*.

## Validar siempre antes de renderizar

```bash
npx hyperframes lint    # 0 errores
npx hyperframes check   # debe decir "Check passed"
npx hyperframes snapshot --at <puntos medios y ±0.1s de cada corte>
```

Revisa la hoja de contactos. Un plano en negro no se nota hasta ver el MP4 terminado.
