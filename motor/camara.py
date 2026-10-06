"""Cámara y transiciones sobre una escena ya dibujada (ffmpeg, sin volver a abrir el navegador).

La escena se dibuja quieta (Chromium solo dibuja su entrada y su salida) y después ffmpeg le
aplica el movimiento de cámara y los fundidos. Así una escena de 40 s sigue costando poco.

- La cámara amplía la imagen al doble antes de moverla, para que el movimiento sea suave (sin
  saltos de un píxel), y mantiene siempre el borde de abajo: la barra de avance no se recorta.
- El fundido va al color de fondo de la marca y no se solapa con la escena vecina: la duración de
  cada escena no cambia y la voz sigue en su sitio.
"""

import subprocess
from pathlib import Path

from motor import catalogo
from motor.render import codificar

ZOOM = 1.06        # cuánto se acerca la cámara (6 %)
PANEO = 1.08       # el encuadre de un paneo (8 % más grande que la pantalla)
FUNDIDO = 0.3      # segundos de cada fundido


def _suave(p: str) -> str:
    """Curva suave (smoothstep) de 0 a 1 para que la cámara arranque y frene sin golpes."""
    return f"({p})*({p})*(3-2*({p}))"


def filtro_camara(efecto: str, cuadros: int, ancho: int, alto: int, fps: int) -> str | None:
    """El filtro de ffmpeg de un efecto de cámara del catálogo (None para «estatica»)."""
    if efecto not in catalogo.CAMARA:
        raise ValueError(f"La cámara «{efecto}» no está en el catálogo")
    if efecto == "estatica":
        return None
    p = _suave(f"on/{max(1, cuadros - 1)}")
    abajo = "ih-ih/zoom"  # el borde de abajo fijo
    if efecto == "zoom_lento_entrada":
        z, x = f"1+{ZOOM - 1}*{p}", "iw/2-iw/zoom/2"
    elif efecto == "zoom_lento_salida":
        z, x = f"{ZOOM}-{ZOOM - 1}*{p}", "iw/2-iw/zoom/2"
    elif efecto == "paneo_derecha":
        z, x = f"{PANEO}", f"(iw-iw/zoom)*{p}"
    else:  # paneo_izquierda
        z, x = f"{PANEO}", f"(iw-iw/zoom)*(1-{p})"
    return (f"scale={ancho * 2}:{alto * 2}:flags=lanczos,"
            f"zoompan=z='{z}':x='{x}':y='{abajo}':d=1:s={ancho}x{alto}:fps={fps}")


def filtro_fundidos(entra: bool, sale: bool, cuadros: int, fps: int, color: str) -> list[str]:
    hexa = "0x" + color.lstrip("#")
    total = cuadros / fps
    salida = []
    if entra:
        salida.append(f"fade=t=in:st=0:d={FUNDIDO}:color={hexa}")
    if sale:
        salida.append(f"fade=t=out:st={max(0.0, total - FUNDIDO):.3f}:d={FUNDIDO}:color={hexa}")
    return salida


def aplicar(parte: Path, destino: Path, camara: str, entra: bool, sale: bool, cuadros: int, ancho: int, alto: int,
            fps: int, color: str, crf: str, preset: str) -> Path:
    """Escribe en `destino` la escena con su cámara y sus fundidos. Si no hay nada que hacer, devuelve `parte`."""
    filtros = [f for f in [filtro_camara(camara, cuadros, ancho, alto, fps)] if f]
    filtros += filtro_fundidos(entra, sale, cuadros, fps, color)
    if not filtros:
        return parte
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(parte), "-vf", ",".join(filtros),
                    "-frames:v", str(cuadros), *codificar(fps, crf, preset), "-an", str(destino)], check=True)
    parte.unlink()
    return destino
