"""Guardas contra lo inventado: una propuesta no puede traer cifras ni normas que no estén en su origen.

Un modelo pequeño puede «mejorar» un texto cambiando un 30 % por un 40 % o citando una ley que
no estaba. Aquí se compara lo propuesto con el texto de la lámina: si aparece una cifra o una
norma nueva, la propuesta se descarta.
"""

import re

from app import extractor

_NUMERO = re.compile(r"\d[\d\.,]*")


def _numeros(texto: str) -> set[str]:
    """Los números del texto, sin separadores de miles («1.500» y «1500» son el mismo)."""
    salida = set()
    for m in _NUMERO.findall(texto or ""):
        limpio = m.rstrip(".,")
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", limpio):
            limpio = limpio.replace(".", "")
        salida.add(limpio.replace(",", "."))
    return salida


def _plano(texto: str) -> str:
    """Sin mayúsculas ni espacios: «30%» y «30 %» son lo mismo."""
    return re.sub(r"\s+", "", (texto or "").lower())


def inventado(propuesta: str, origen: str) -> list[str]:
    """Lo que la propuesta afirma y el origen no: cifras nuevas y normas nuevas."""
    nuevas = sorted(_numeros(propuesta) - _numeros(origen))
    plano = _plano(origen)
    # Una norma con números conocidos pero otro nombre («Decreto 1503» donde decía «Ley 1503»).
    # Si trae números nuevos ya quedó como «cifra».
    normas = [c for c in extractor.afirmaciones_normativas(propuesta)
              if _plano(c) not in plano and _numeros(c) <= _numeros(origen)]
    return [f"cifra {n}" for n in nuevas] + [f"norma «{c}»" for c in normas]
