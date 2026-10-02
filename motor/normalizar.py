"""Texto del guion → texto que la voz lee bien.

La voz no debe adivinar cómo se leen «Ley 1503 de 2011», «30 %», «$ 1.500.000» o «SMMLV».
Aquí se escriben en palabras, con las convenciones de Colombia: el punto separa miles y la
coma separa decimales. El guion que se ve en pantalla y en los subtítulos no cambia: esto
solo afecta a lo que se le manda a la voz.
"""

import re

from num2words import num2words

# Siglas que la voz debe decir de una forma concreta. Cada marca puede añadir o cambiar las
# suyas en su ficha (`datos/marcas/<id>.json`, clave «pronunciacion»).
# ⚠ Confirmar con el cliente cómo se dice PESV (ver docs/bitacora.md).
PRONUNCIACION = {
    "SMMLV": "salarios mínimos mensuales legales vigentes",
    "SMLMV": "salarios mínimos mensuales legales vigentes",
    "PESV": "pe e ese ve",
    "SST": "ese ese te",
    "SG-SST": "sistema de gestión de seguridad y salud en el trabajo",
    "ARL": "a erre ele",
    "EPP": "e pe pe",
    "km/h": "kilómetros por hora",
    "Art.": "artículo",
}

_ORDINALES = {1: "primero", 2: "segundo", 3: "tercero", 4: "cuarto", 5: "quinto",
              6: "sexto", 7: "séptimo", 8: "octavo", 9: "noveno", 10: "décimo"}


def _entero(digitos: str) -> str:
    """Un entero en palabras; los identificadores largos (radicados) se leen cifra por cifra."""
    if len(digitos) > 9 or (digitos.startswith("0") and len(digitos) > 1):
        return " ".join(num2words(int(c), lang="es") for c in digitos)
    return num2words(int(digitos), lang="es")


def _numero(texto: str) -> str:
    """«1.500.000» → un millón quinientos mil · «2,5» → dos coma cinco."""
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", texto):  # miles con punto
        return _entero(texto.replace(".", ""))
    m = re.fullmatch(r"(\d+)[,\.](\d+)", texto)  # decimal
    if m:
        entera, decimales = m.groups()
        dec = " ".join(num2words(int(c), lang="es") for c in decimales) if decimales.startswith("0") \
            else num2words(int(decimales), lang="es")
        return f"{_entero(entera)} coma {dec}"
    return _entero(texto)


_NUM = r"\d{1,3}(?:\.\d{3})+|\d+[,\.]\d+|\d+"


def _millon_de(palabras: str) -> str:
    """«un millón» + pesos → «un millón de pesos» (regla del español con millones exactos)."""
    return palabras + (" de" if re.search(r"(?:millón|millones)$", palabras) else "")


def para_voz(texto: str, pronunciacion: dict | None = None) -> str:
    """Devuelve el texto listo para la voz."""
    siglas = {**PRONUNCIACION, **(pronunciacion or {})}
    t = texto or ""

    # Siglas y abreviaturas, de la más larga a la más corta para que SG-SST gane a SST.
    for sigla in sorted(siglas, key=len, reverse=True):
        borde_izq = r"(?<![\w])" if sigla[0].isalnum() else ""
        borde_der = r"(?![\w])" if sigla[-1].isalnum() else ""
        t = re.sub(borde_izq + re.escape(sigla) + borde_der, siglas[sigla], t)

    # «No. 1503» → «número 1503» (solo delante de una cifra: un «No.» suelto es una respuesta).
    t = re.sub(r"(?<![\w])No\.\s?(?=\d)", "número ", t)
    # Dinero: «$ 1.500.000» y «$1.500.000» → «un millón quinientos mil pesos».
    t = re.sub(rf"\$\s?({_NUM})", lambda m: _millon_de(_numero(m.group(1))) + " pesos", t)
    # Porcentajes: «30 %» y «30%».
    t = re.sub(rf"({_NUM})\s?%", lambda m: _numero(m.group(1)) + " por ciento", t)
    # Ordinales: «1.º», «1°», «2.ª».
    t = re.sub(r"(\d+)\s?\.?\s?[º°]", lambda m: _ORDINALES.get(int(m.group(1)), _entero(m.group(1))), t)
    t = re.sub(r"(\d+)\s?\.?\s?ª", lambda m: re.sub(r"o$", "a", _ORDINALES.get(int(m.group(1)), _entero(m.group(1)))), t)
    # El resto de números.
    t = re.sub(rf"(?<![\w]){_NUM}(?![\w])", lambda m: _numero(m.group(0)), t)
    # Espacios de más que dejan los reemplazos.
    return re.sub(r"\s{2,}", " ", t).strip()
