# Puntos de SFX — riskmann-consulta-pesv-vertical

Cada animación de este video se construyó dejando un **golpe visual** en un
instante concreto, para que al añadir los efectos de sonido el video no parezca
"con sonido encima" sino sincronizado. Esta tabla es la que consume
`tools/mezcla.py` al armar las **Versiones A y B** (la C va sin SFX).

`t` es el segundo dentro del video completo de 45 s. Los planos arrancan en
0 · 8 · 15 · 23 · 30 · 38.

## Cortes entre planos (whoosh)

| t | Transición | Efecto sugerido |
| --- | --- | --- |
| 8.0 | zoom-through | whoosh corto con cola |
| 15.0 | crossfade | whoosh suave |
| 23.0 | push-slide | whoosh lateral |
| 30.0 | zoom-through | whoosh corto con cola |
| 38.0 | crossfade | whoosh suave |

## Plano 1 — Hook (0–8 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 0.25 | La cifra **11** entra con golpe (escala 1.18 → 1) | impacto grave |
| 0.42 | La barra roja subraya la cifra (wipe) | swipe corto |
| 1.95 | La cifra **2** releva a la anterior | impacto grave |
| 2.12 | Segunda barra roja | swipe corto |
| 3.85 | Entra la frase que resuelve | whoosh + impacto suave |
| 4.90 / 5.12 | Los dos chips de umbral | pop ×2 |

## Plano 2 — Marca (8–15 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 8.08 / 8.18 / 8.28 / 8.38 | Las cuatro escuadras entran una por esquina | tick ×4, mismo tono |
| 8.45 | El lockup florece desde el centro | bloom / sub grave |
| 9.25 | Regla dorada | swipe fino |
| 10.20 / 10.45 | Los dos chips de garantía | pop ×2 |

## Plano 3 — Excel / Automatización (15–23 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 15.05 | La tarjeta de producto se asienta | impacto suave |
| 15.85 / 15.95 | Las escuadras cian marcan la tarjeta | tick ×2 agudo |
| 16.05 | Barra cian que barre el borde inferior | escaneo / sweep |
| 16.55 / 17.25 / 17.95 | Los tres módulos entran uno a uno | pop ×3 ascendente |

## Plano 4 — Ahorro de tiempo (23–30 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 23.00 | La tarjeta de estadísticas entra | impacto suave |
| 24.00 → 25.55 | La cifra cuenta de 0 a 70 y la barra se llena | riser continuo (1.55 s) |
| 25.45 | La cifra aterriza y asienta | impacto, cierra el riser |

## Plano 5 — Beneficio (30–38 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 30.30 | Ficha 1 — «24 pasos» | impacto |
| 32.93 | Ficha 2 — auditoría al día | impacto |
| 34.87 | Ficha 3 — «500 SMMLV» | impacto más seco, es el remate |

## Plano 6 — Cierre (38–45 s)

| t | Qué pasa en pantalla | Efecto sugerido |
| --- | --- | --- |
| 38.00 | El lockup florece | bloom / sub grave |
| 38.50 | Regla dorada | swipe fino |
| 39.60 | El botón **Escríbenos** entra con golpe | click / pop marcado |
| 40.40 | Aparece la dirección | tick suave |

## Reglas de mezcla

- La cama musical va **bajo −31 LUFS** cuando hay voz, para no taparla.
- Los SFX de impacto no deben pasar de −12 dB de pico: el video se ve en celular
  y con el volumen alto la voz se pierde.
- La mezcla final se normaliza a **−16 LUFS**, que es la referencia que usa
  `tools/mezcla.py` en todo el repositorio.
- Versión **A** = voz + SFX + música · **B** = SFX + música · **C** = solo música.
