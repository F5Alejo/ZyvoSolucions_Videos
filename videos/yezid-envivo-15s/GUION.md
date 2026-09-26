# «En Vivo: PESV · Autogestión» — promocional de 15 s (9:16)

Anuncia el En Vivo del Dr. Yezid Ricaurte (sábado 3 de octubre, 10:00 a. m., hora Colombia).
Copy tomado de `yezidricaurte.com/en-vivos/pesv-informe-autogestion/` y de los correos de la campaña
(`Documentos_contexto/correos-en-vivo-pesv/`). Preview: `python -m http.server 5530` → <http://localhost:5530>

## Recursos reales usados

| Recurso | Origen |
| --- | --- |
| Foto del Dr. Yezid (recorte con fondo transparente) | `yezidricaurte.com/images/yezid-portada-1.png`, publicada en su web |
| Firma oficial en negativo | manual de marca (`assets/firma-yezid-blanca.png`) |
| Grabación real de RiskMann: gráficas de conductores | `graficas-limpio.mp4` (ya limpia de marca y de datos de cliente) |
| Iconos oficiales: inspecciones, vehículos, conductores, mantenimientos | `assets/img/seguridad_vial_icono_*.webp` de RiskMann |
| Fotos de conducción (cockpit, autopista, cinturón, tablero) | `assets/fotos-pixabay/` (licencia Pixabay) |
| Tipografía Dubai · #336666 · #80804a | manual de marca Yezid Ricaurte |
| Petróleo, filete dorado, botón coral | correos de la campaña |
| #45a035 · #f1ecb0 | brief |

## Locución

Carlos (ElevenLabs, `eleven_multilingual_v2`, estabilidad 0.35 · claridad 0.80), una frase por bloque con
marcas de tiempo por carácter. PESV deletreado; «vivo» nunca cierra frase.

```text
1.00  Tu P-E-S-V ya está en marcha… pero falta el informe.
4.50  Inspecciones, flota, conductores… ¿a mano?                         [«¿y todo a mano?» no cabía]
7.03  El doctor Yezid Ricaurte te enseña a generarlo… con un solo clic.
11.50 Tres de octubre, ¡en vivo y gratis! Reserva tu cupo.
```

`js/ads.js` → `elevenLabsTimestamps` (los cuatro del brief + las palabras clave medidas):
`hook 1.0 · falta 3.40 · informe 3.82 · dolor 4.5 · flota 5.30 · conductores 5.69 · mano 6.62 ·
presentacionYezid 7.0 · yezid 7.62 · generarlo 9.28 · clic 10.95 · fechaEvento 11.5 · vivo 12.79 · gratis 13.43`.

## [STORYBOARD TIMELINE]

| s | Imagen | Cámara 3D | Sonido |
| --- | --- | --- | --- |
| 0.00–0.25 | «EN VIVO» con separación cromática verde/pálido/blanco, entra 2.4→1 (`expo.out`), desenfoque 18→0 px; destello | ráfaga a 140 u/s, lente abierto +16°, giro | ráfaga ElevenLabs + impacto grave |
| 0.60–1.0 | Rótulo «EN VIVO · PESV · Autogestión» + filete dorado (el encabezado del correo) | frena a 16 u/s | whoosh |
| 0.78 | La apertura sale (escala 1.18, desenfoque, `power4.in`) | | |
| 1.00 | «Tu PESV ya está en marcha.» letra por letra; se acerca lento | crucero 10 u/s, paralaje | voz |
| 3.32 | **«FALTA EL»**: cada letra cae desde escala 3, giro ±35° y desenfoque (`back.out(1.7)`, cascada de 0.04 s) | | «…falta…» 3.40 |
| 3.72 | **«INFORME»** en pálido: cada letra sube desde escala 0.2 (`expo.out`); sacudida y destello | golpe de lente +9° | impacto · «informe» 3.82 |
| 3.94 | Sello dorado «el que exige el Ministerio de Trabajo» | | |
| 4.38 | Corte 1: foto de cockpit en duotono verde se abre con máscara; icono **Inspecciones** 1.8→1 | acelera a 52 u/s | obturador + glitch |
| 5.18 | Corte 2 (máscara lateral): autopista; icono **Flota** | | obturador · «flota» 5.30 |
| 5.57 | Corte 3 (máscara desde abajo): cinturón; icono **Conductores** | | obturador · «conductores» 5.69 |
| 5.87 | Corte 4: tablero; icono **Mantenimiento**. Los cuatro quedan en rejilla 2×2 | | obturador |
| 6.24 | La rejilla sale; **«¿TODO A MANO?»** letra por letra | | glitch |
| 6.62 | Tacha pálida atraviesa la frase; sacudida | | impacto · «¿a mano?» |
| 6.80 | El bloque del dolor se barre hacia arriba (máscara `expo.inOut`) | frena a 7 u/s | whoosh cinematográfico |
| 6.90 | **Foto del Dr. Yezid**: la máscara de cristal esmerilado (blur 15 px) se abre de abajo arriba; la foto hace punch-in 1.35→1; luz pálida barre el fondo del marco | golpe de lente +6° | brillo · «doctor» 7.22 |
| 7.35 | «Dr. Yezid Ricaurte» letra por letra | | «Yezid» 7.62 |
| 7.95 | «Abogado · Consultor · Conferencista · 27 años de trayectoria» | | |
| 8.20 | La firma se escribe de izquierda a derecha (máscara de trazo) | | |
| 7.9–11.2 | **Ambient idle**: el marco flota en Y y escala 1.02→1.05; la foto crece 1→1.04 | crucero lento | |
| 9.18 | Tarjeta de cristal con la **grabación real de RiskMann** (gráficas) entra girando en Y (`back.out(1.7)`) y el video corre | | whoosh · «generarlo» 9.28 |
| 10.95 | «con un solo clic» salta 1.8→1 en pálido; destello | | pop · «clic» 10.95 |
| 9.9–11.5 | | | riser |
| 11.24 | La presentación sale | frena a 6 u/s | |
| **11.50** | **SPECTACLE BEAT: «3»** 2x→1x con `back.out(3.2)`, resplandor #f1ecb0 que estalla a 110 px y respira; sacudida fuerte; destello | **máximo: 110 u/s**, lente +18°, giro | golpe cinematográfico ElevenLabs · «Tres de octubre» |
| 11.62 | «DE OCTUBRE» entra desde escala 2 | | |
| 12.20 | «Sábado · 10:00 a. m. (Hora Colombia)» | vuelve a 16 u/s | |
| 12.59 | Píldora «● EN VIVO» + letras; el punto late | | ping · «vivo» 12.79 |
| 13.38 | Botón coral **«Reservar cupo gratis →»** 1.7→1 (`back.out(3)`), resplandor coral que respira; sacudida | | pop · «gratis» 13.43 |
| 13.78–13.93 | yezidricaurte.com · la firma se escribe | | brillo |
| 12.6–15 | El «3» flota y respira | crucero | «Reserva tu cupo» |

Reglas cumplidas: sin fades lineales (entradas `back.out(1.7)`, `expo.out`, `expo.inOut`,
`power4.out`), textos letra por letra en cascada, ambient idle en foto y tarjetas, destellos con tope de
0.5 (sin lavar la imagen ni pasar de uno por segundo), sin rojo (regla del cliente).

## Técnica

- `js/bg.js`: escena Three.js real con 6 500 partículas en túnel (shader propio), 420 rayos de datos que se
  estiran con la velocidad, 12 anillos hexagonales wireframe y 4 icosaedros wireframe, niebla exponencial y
  cámara con paralaje continuo. La distancia recorrida integra una curva de velocidad fija (`VELOCIDAD` en
  `ads.js`): el render es determinista.
- El video de RiskMann se sincroniza fotograma a fotograma: `window.seekTo(t)` espera el `seeked`.
- `tools/audio.py`: voz, efectos (4 hechos con ElevenLabs: ráfaga, golpe, glitch, obturador; el resto de
  Pixabay), música enérgica generada con ElevenLabs (energía pareja −13/−15 LUFS los 15 s) y mezcla a −14
  LUFS con la voz 12–18 dB sobre la música.
- `tools/render.mjs`: 1080×1920, 30 fps, H.264 CRF 18, 15 s.
