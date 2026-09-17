# Sonido — riskmann-consulta-pesv-vertical (37.5 s)

Cada animación se construyó dejando un **golpe visual** en un instante concreto.
Esta tabla es el mapa que consume `tools/mezcla.py`. Los planos arrancan en
**0 · 6.5 · 13 · 19.5 · 26 · 31.5**.

## La música

`assets/musica-mixkit-hip-hop-02.mp3` — Mixkit «Hip Hop 02» (id 738). Licencia
Mixkit Free: uso comercial, sin atribución, **sin restricción de plataforma**.
Ver `assets/musica-LICENCIA.txt`.

**No se usó la Biblioteca de Audio de YouTube**: sus pistas solo están
licenciadas para videos alojados en YouTube, y esta pieza también va a Reels,
TikTok y Facebook.

Sustituyó a la pista sintetizada de `tools/ritmo.py`. Medida en tres bandas,
entra con 4 dB de diferencia entre graves, medios y agudos — se oye en un
celular sin pelear con nada.

**La música va en `musica`, nunca en `pistas`.** `pistas` desemboca en el mismo
`amix` que la locución y nada la aparta: en los picos se come la voz. Esa era la
causa real de que la música tapara a Carlos.

## El nivel de la voz

ElevenLabs entrega la locución a **−33 dB de media**; una pista de catálogo viene
a **−14 dB**. Son 19 dB de desventaja que ningún ducking compensa. Por eso la voz
se nivela **antes**, a disco:

```bash
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14
```

No se hace dentro de `mezcla.py`: `loudnorm` en un `filter_complex` entrega
192 kHz y desplaza los timestamps, así que el `apad`/`atrim` posterior devuelve
**silencio sin dar ningún error**.

La verificación que manda es el **margen voz–música frase por frase**, no el
nivel general de la mezcla. Objetivo: la voz entre **+7 y +25 dB** sobre la
música en cada frase. Estado actual: mínimo **+7.5 dB**, «¿Seguro?» a **+8.2 dB**.

## Los efectos

41 en total, repartidos en `tools/etapa-sfx1.json` y `tools/etapa-sfx2.json`.

| t | Plano | Qué pasa en pantalla | Efecto |
| --- | --- | --- | --- |
| 0.00 | 1 | El barrido de luz abre la pieza | whoosh |
| 0.85 | 1 | El tachón rojo se dibuja | whoosh-short |
| 1.15 | 1 | La objeción retrocede en profundidad | whoosh-short |
| **1.45** | 1 | **El golpe grave, justo antes de la palabra** | **impact-bass-1** |
| **1.53** | 1 | **¿SEGURO? aterriza con la voz de Carlos** | *(sin efecto: la palabra manda)* |
| 2.60 | 1 | La tarjeta glass sube | pop |
| 5.55 | 1 | Salida push-through | whoosh-cinematic |
| 6.70 | 2 | Tarjeta del umbral 11 | pop |
| 7.10 | 2 | Se dibuja su barra roja | click-soft |
| 7.70 | 2 | Tarjeta del umbral 2 | pop |
| 8.10 | 2 | Se dibuja su barra roja | click-soft |
| **8.95** | 2 | **El veredicto aterriza y destella** | **impact-bass-2** |
| 12.05 | 2 | Salida | whoosh-cinematic |
| 13.15 | 3 | «No cumplir cuesta hasta» en cascada | click-soft |
| **14.45** | 3 | **500 aterriza + onda expansiva** | **impact-bass-1** |
| 15.15 | 3 | SMMLV entra de costado | whoosh-short |
| 16.15 | 3 | Chip dorado de los pesos | pop |
| 17.00 | 3 | El respaldo legal | click-soft |
| 18.55 | 3 | Salida | whoosh-cinematic |
| **19.65** | 4 | **El logo florece** | **impact-bass-2** |
| 20.35 | 4 | Regla dorada | click-soft |
| 21.45 / 21.61 / 21.77 | 4 | Los tres módulos en cascada | pop ×3 |
| 23.55 | 4 | «en una sola plataforma» | click-soft |
| 25.05 | 4 | Salida | whoosh-cinematic |
| 26.10 | 5 | La tarjeta del producto sube | pop |
| **27.15** | 5 | **70% aterriza con destello cian** | **impact-bass-1** |
| 27.75 | 5 | La barra se llena | riser |
| 30.55 | 5 | Salida | whoosh-cinematic |
| 32.35 | 6 | El logo florece | impact-bass-2 |
| **32.85** | 6 | **El botón Escríbenos aterriza** | **click** |
| 33.70 | 6 | «La consulta es gratis» | pop |
| 34.10 | 6 | La dirección | click-soft |

*(Las entradas de plano a 6.5, 13, 19.5, 26 y 31.5 llevan su propio `whoosh`.)*

## Cómo se arma

El filtro de ffmpeg con 47 entradas simultáneas **agota la memoria** de una máquina
normal — falló dos veces antes de partirlo. Se arma por etapas:

```bash
python ../../tools/nivelar-voz.py assets/voz assets/voz-nivelada -14   # voz a nivel
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
- `mezcla.py` aparta la música bajo la voz con `sidechaincompress`, y la **llave
  es solo la locución**, no los efectos: los golpes no hacen bombear la pista.
- Los efectos nunca caen encima de una palabra clave. El `impact-bass-1` del
  gancho se adelantó a 1.45 s para dejar sonar «¿Seguro?» a 1.53 s.
- **Verificar por bandas, no solo el nivel general.** Un balance sano queda dentro
  de ~12 dB entre graves, medios y agudos:
  ```bash
  ffmpeg -i salida.mp4 -af "highpass=f=2000,volumedetect" -f null -
  ```
  Si los agudos caen por debajo de −45 dB, en un celular no se va a oír.
