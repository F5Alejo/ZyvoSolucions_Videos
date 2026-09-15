# Narración — RiskMann · Sala de control

Voz: **es_ES-davefx-medium** (Piper, local, sin cuenta ni límite).
Pista mezclada: `assets/narracion.wav` (68s, −16 LUFS). Líneas sueltas en `assets/vo/`.

**Procedencia de cada línea.** Nada aquí es invención: cada frase es o bien texto que
ya aparece en pantalla en el propio video, o bien copia aprobada del video anterior del
equipo (`video-presentacion/index.html`), o bien nombres reales de módulo y submódulo
tomados de los archivos de `assets/`.

| Plano | Entra | Dura | Línea | Fuente |
| --- | --- | --- | --- | --- |
| 01 | 0.5s | 6.2s | «Actualizar la matriz. Pasar la lista. Firmar la inspección. Y volver a empezar.» | Texto en pantalla del plano 01 |
| 02 | 7.8s | 2.8s | «No es un formato. Es un sistema entero, disperso.» | Texto en pantalla del plano 02 |
| 03 | 16.0s | 3.8s | «RiskMann. Automatiza y controla el PESV.» | Copia aprobada del equipo |
| 04 | 22.8s | 2.5s | «Todo lo que necesitas en una sola plataforma.» | Copia aprobada del equipo |
| 05 | 31.5s | 4.1s | «Control de personal: lector QR, historial diario y ausentismo.» | Nombres de submódulo (`control_personal_icono_*.webp`) |
| 06 | 38.0s | 3.8s | «Estadísticas, gráficas y registros de la plataforma.» | Nombres de las tres grabaciones de UI |
| 07 | 46.0s | 4.1s | «Conductores, vehículos, inspecciones, mantenimientos y siniestralidad vial.» | Nombres de submódulo (`seguridad_vial_icono_*.webp`) |
| 08 | 54.5s | 3.9s | «La gestión del PESV en la palma de tu mano.» | Copia aprobada del equipo |
| 09 | 61.5s | 5.1s | «RiskMann. Su aliado tecnológico estratégico.» | Copia aprobada del equipo |

## Lo que la voz NO dice, deliberadamente

El video muestra en pantalla frases que no tienen respaldo en el material entregado
(ver §0 de `PRODUCCION-VIDEOS.md`). La narración las omite todas — en particular
**no lee el «100 % · Trazabilidad del registro»** del plano 06, que es una cifra
inventada. Una afirmación leída en alto pesa más que una escrita, así que la locución
se limitó a lo verificable.

Ese texto **sigue en pantalla**. Para eliminarlo hay que editar
`compositions/frames/06-dato-vivo.html` y volver a renderizar.

## Regenerar

```bash
# una línea
echo "texto" | python -m piper -m es_ES-davefx-medium.onnx -f assets/vo/03.wav
# la mezcla completa: ver el comando ffmpeg (adelay + amix + loudnorm) en el historial
```

Las líneas se escribieron para **caber dentro de la duración que ya tenía cada plano**,
así que no hubo que re-cronometrar nada y la coreografía original quedó intacta. Si una
línea futura se pasa de largo, córtala o ajusta `--length-scale` antes de tocar los
tiempos de los planos.
