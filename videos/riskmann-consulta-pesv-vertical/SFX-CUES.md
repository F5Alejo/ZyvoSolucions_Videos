# Sonido — riskmann-consulta-pesv-vertical (37.5 s)

Cada animación se construyó dejando un **golpe visual** en un instante concreto.
Esta tabla es el mapa que consume `tools/mezcla.py`. Los planos arrancan en
**0 · 6.5 · 13 · 19.5 · 26 · 31.5**.

## La música

`tools/ritmo-video.json` → `tools/ritmo.py` genera `assets/ritmo.wav` a **120 BPM**.

**No usar una cama de senos sostenidos.** Se intentó primero y quedó inaudible: un
acorde entre 146 y 440 Hz mide bien en el vúmetro pero un parlante de celular corta
por debajo de 500 Hz. Medido, esa cama daba −62.7 dB en agudos contra −31.5 dB de
la pista rítmica. Es la misma lección que ya advierte el encabezado de `ritmo.py`.

La instrumentación crece con la narrativa:

| Tramo | Instrumentos |
| --- | --- |
| 0 – 6.5 · la objeción | bombo + platillos (tenso, vacío) |
| 6.5 – 13 · los umbrales | + bajo |
| 13 – 26 · el costo y la solución | + palmas + acordes (lleno) |
| 26 – 31.5 · la prueba | lleno |
| 31.5 – 37.5 · el contacto | bombo, platillos, bajo, acordes |

Las **subidas de ruido** terminan justo en cada corte (6.5, 13, 19.5, 26, 31.5), así
refuerzan las salidas que atraviesan la lente.

## Los efectos

41 en total, repartidos en `tools/etapa-sfx1.json` y `tools/etapa-sfx2.json`.

| t | Plano | Qué pasa en pantalla | Efecto |
| --- | --- | --- | --- |
| 0.00 | 1 | El barrido de luz abre la pieza | whoosh |
| 1.00 | 1 | El tachón rojo se dibuja | whoosh-short |
| 1.40 | 1 | La objeción retrocede en profundidad | whoosh-short |
| **1.80** | 1 | **¿SEGURO? aterriza con overshoot** | **impact-bass-1** |
| 2.60 | 1 | La tarjeta glass sube | pop |
| 5.55 | 1 | Salida push-through | whoosh-cinematic |
| 6.70 | 2 | Tarjeta del umbral 11 | pop |
| 7.10 | 2 | Se dibuja su barra roja | click-soft |
| 7.45 | 2 | Tarjeta del umbral 2 | pop |
| 7.85 | 2 | Se dibuja su barra roja | click-soft |
| **8.55** | 2 | **El veredicto aterriza y destella** | **impact-bass-2** |
| 12.05 | 2 | Salida | whoosh-cinematic |
| 13.20 | 3 | «No cumplir cuesta hasta» en cascada | click-soft |
| **14.00** | 3 | **500 aterriza + onda expansiva** | **impact-bass-1** |
| 14.70 | 3 | SMMLV entra de costado | whoosh-short |
| 15.90 | 3 | Chip dorado de los pesos | pop |
| 16.70 | 3 | El respaldo legal | click-soft |
| 18.55 | 3 | Salida | whoosh-cinematic |
| **19.65** | 4 | **El logo florece** | **impact-bass-2** |
| 20.35 | 4 | Regla dorada | click-soft |
| 21.60 / 21.76 / 21.92 | 4 | Los tres módulos en cascada | pop ×3 |
| 22.90 | 4 | «en una sola plataforma» | click-soft |
| 25.05 | 4 | Salida | whoosh-cinematic |
| 26.10 | 5 | La tarjeta del producto sube | pop |
| **27.00** | 5 | **70% aterriza con destello cian** | **impact-bass-1** |
| 27.60 | 5 | La barra se llena | riser |
| 30.55 | 5 | Salida | whoosh-cinematic |
| 32.40 | 6 | El logo florece | impact-bass-2 |
| **33.00** | 6 | **El botón Escríbenos aterriza** | **click** |
| 33.90 | 6 | «La consulta es gratis» | pop |
| 34.25 | 6 | La dirección | click-soft |

*(Las entradas de plano a 6.5, 13, 19.5, 26 y 31.5 llevan su propio `whoosh`.)*

## Cómo se arma

El filtro de ffmpeg con 47 entradas simultáneas **agota la memoria** de una máquina
normal — falló dos veces antes de partirlo. Se arma por etapas:

```bash
python ../../tools/ritmo.py tools/ritmo-video.json     # la música
python ../../tools/mezcla.py tools/etapa-sfx1.json     # 20 efectos
python ../../tools/mezcla.py tools/etapa-sfx2.json     # 21 efectos
python ../../tools/mezcla.py tools/final-A.json        # música + efectos + voz
python ../../tools/mezcla.py tools/final-B.json        # música + efectos
python ../../tools/mezcla.py tools/final-C.json        # solo música
```

Luego cada mezcla se pega al MP4 reemplazando su audio:

```bash
ffmpeg -i video.mp4 -i assets/mezcla-A.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ac 2 -shortest salida-A.mp4
```

## Reglas de mezcla

- La mezcla se normaliza a **−16 LUFS**, la referencia del repositorio.
- `mezcla.py` aparta la música bajo la voz con su propio ducking; por eso en A la
  pista va a 0.30 de ganancia y en B a 0.62.
- **Verificar por bandas, no solo el nivel general.** Un balance sano queda dentro
  de ~12 dB entre graves, medios y agudos:
  ```bash
  ffmpeg -i salida.mp4 -af "highpass=f=2000,volumedetect" -f null -
  ```
  Si los agudos caen por debajo de −45 dB, en un celular no se va a oír.
