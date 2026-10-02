"""Catálogos cerrados de cámara y transiciones: lo único que un estilo, un agente o una persona puede pedir.

Las animaciones de entrada y salida tienen su propio catálogo en `motor/escenas/efectos.py`.
Un valor que no está aquí no se ejecuta: el VideoSpec lo cambia por el de por defecto y deja el
aviso `INVALID_EFFECT` (ver `motor/videospec.py`). Cómo se hace cada uno: `motor/camara.py`.

No están (y por qué): el paralaje y el enfoque necesitan la escena en capas, y los paneos
verticales recortarían la barra de avance. El fundido cruzado y el deslizamiento solapan dos
escenas y cambiarían la línea de tiempo de la voz.
"""

# Movimiento de cámara durante la escena (suave, sobre la lámina ya armada).
CAMARA = {
    "estatica": "Quieta",
    "zoom_lento_entrada": "Acercarse despacio",
    "zoom_lento_salida": "Alejarse despacio",
    "paneo_izquierda": "Recorrer hacia la izquierda",
    "paneo_derecha": "Recorrer hacia la derecha",
}
CAMARA_DEFECTO = "estatica"

# Cómo se pasa de una escena a la siguiente.
TRANSICION = {
    "corte": "Corte directo",
    "fundido": "Fundido al color de la marca",
}
TRANSICION_DEFECTO = "corte"


def validar_escena(e: dict | None) -> dict:
    """`trabajo["escena"]`: {camara?, transicion?, laminas: {"n": {camara?, transicion?}}}. Lanza ValueError."""
    e = e or {}
    if not isinstance(e, dict):
        raise ValueError("Los ajustes de escena tienen que ser un objeto")

    def una(x: dict, donde: str) -> dict:
        limpio = {}
        for campo, cat in (("camara", CAMARA), ("transicion", TRANSICION)):
            v = x.get(campo)
            if v is None:
                continue
            if v not in cat:
                raise ValueError(f"{donde}: «{v}» no está en el catálogo de {campo}")
            limpio[campo] = v
        return limpio

    salida = una(e, "Curso")
    laminas = {}
    for n, x in (e.get("laminas") or {}).items():
        if not str(n).isdigit() or not isinstance(x, dict):
            raise ValueError(f"«{n}» no es un número de lámina")
        propia = una(x, f"Lámina {n}")
        if propia:
            laminas[str(n)] = propia
    if laminas:
        salida["laminas"] = laminas
    return salida
