"""Subtítulos .vtt y .srt a partir del guion y de los tiempos reales de cada frase.

No se transcribe nada: el texto es el del guion (tal como se ve en pantalla, sin normalizar) y
los tiempos salen del audio generado. Las frases largas se parten en bloques de dos líneas de
hasta 42 caracteres, repartiendo el tiempo según el largo de cada bloque.
"""

from pathlib import Path

LINEA = 42
LINEAS = 2


def _lineas(palabras: list[str]) -> list[str]:
    lineas, actual = [], ""
    for p in palabras:
        if actual and len(actual) + 1 + len(p) > LINEA:
            lineas.append(actual)
            actual = p
        else:
            actual = f"{actual} {p}".strip()
    if actual:
        lineas.append(actual)
    return lineas


def bloques(texto: str) -> list[str]:
    """Parte una frase en bloques de hasta dos líneas (cada bloque ya trae su salto de línea)."""
    lineas = _lineas(texto.split())
    return ["\n".join(lineas[i:i + LINEAS]) for i in range(0, len(lineas), LINEAS)]


def cues(frases: list[tuple[float, float, str]]) -> list[tuple[float, float, str]]:
    """(inicio, fin, frase) → (inicio, fin, bloque), con el tiempo repartido por caracteres."""
    salida = []
    for inicio, fin, texto in frases:
        partes = bloques(texto)
        total = sum(len(p) for p in partes) or 1
        t = inicio
        for p in partes:
            dur = (fin - inicio) * len(p) / total
            salida.append((t, t + dur, p))
            t += dur
    return salida


def _tiempo(s: float, separador: str) -> str:
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    seg, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{seg:02d}{separador}{ms:03d}"


def escribir_vtt(lista: list[tuple[float, float, str]], destino: Path) -> None:
    cuerpo = "".join(f"{_tiempo(a, '.')} --> {_tiempo(b, '.')}\n{t}\n\n" for a, b, t in lista)
    destino.write_text("WEBVTT\n\n" + cuerpo, encoding="utf-8")


def escribir_srt(lista: list[tuple[float, float, str]], destino: Path) -> None:
    cuerpo = "".join(f"{i}\n{_tiempo(a, ',')} --> {_tiempo(b, ',')}\n{t}\n\n" for i, (a, b, t) in enumerate(lista, 1))
    destino.write_text(cuerpo, encoding="utf-8")
