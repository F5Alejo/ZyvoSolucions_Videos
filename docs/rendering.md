# Cómo se dibuja el video

Código: [`motor/renderers.py`](../motor/renderers.py), [`motor/render.py`](../motor/render.py),
[`motor/camara.py`](../motor/camara.py), [`motor/escenas/`](../motor/escenas/).

## La escena

Cada lámina se rearma sobre una plantilla HTML de la marca (`motor/escenas/escena.html`): no se copia
la imagen de la diapositiva. Hay tres tipos: **portada** (primera del video), **imagen** (foto a un
lado) y **lista** (título y viñetas). Si la lámina solo trae una tabla o un gráfico, sus datos son las
viñetas.

## El renderer (`PlaywrightRenderer`)

1. Chromium abre el HTML y lleva cada animación CSS a su instante exacto: el resultado es idéntico en
   cada render.
2. Se dibujan cuadro a cuadro **solo la entrada y la salida**; ffmpeg sostiene el cuadro del medio.
   Una lámina de 40 s cuesta casi lo mismo que una de 5 s.
3. Se aplica la **cámara** y los **fundidos** con ffmpeg sobre la escena ya armada.
4. Cada escena se guarda como `escenas/<huella>.mp4`. La huella resume su HTML y sus ajustes: si no
   cambió, no se vuelve a dibujar.
5. Las escenas se unen sin recodificar.

Un renderer nuevo solo tiene que cumplir `VideoRenderer` (`motor/proveedores.py`) y registrarse en
`RENDERERS`. **Remotion no está incluido:** pide licencia de pago a empresas (ver `ARCHITECTURE.md`).

## Catálogos (lo único que se puede pedir)

| Qué | Opciones | Dónde |
|---|---|---|
| Animación de cada elemento | Plantillas Sobria, Dinámica, Cinética, Corporativa y Mínima, con entrada y salida editables | `datos/animaciones/`, `motor/escenas/efectos.py` |
| Cámara | Quieta, acercarse despacio, alejarse despacio, recorrer a la izquierda o a la derecha | `motor/catalogo.py` |
| Transición | Corte, fundido al color de la marca | `motor/catalogo.py` |
| Formato | Presentación 16:9 (1920×1080), Vertical 9:16, Cuadrado 1:1, Instagram 4:5 | `motor/escenas/__init__.py` |
| Estilo | Educativo, Corporativo, Tecnológico, Minimalista, Dinámico, Cinemático, Social | `datos/estilos/` |

La cámara mantiene fijo el borde de abajo (no recorta la barra de avance) y el fundido no se solapa
con la escena vecina (la voz no se mueve). Por eso no hay paralaje, paneos verticales ni fundido cruzado.

## Salida

H.264 High `yuv420p` (CRF 18 en final, 23 en borrador), AAC estéreo 48 kHz 192 kbps, `+faststart`.
720p dibuja el mismo lienzo a 2/3.
