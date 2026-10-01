"""Catálogos cerrados de cámara y transiciones: lo único que un estilo, un agente o una persona puede pedir.

Las animaciones de entrada y salida tienen su propio catálogo en `motor/escenas/efectos.py`.
Un valor que no está aquí no se ejecuta: el VideoSpec lo cambia por el de por defecto y deja el
aviso `INVALID_EFFECT` (ver `motor/videospec.py`).
"""

# Movimiento de cámara durante la escena (zoom o paneo suave sobre la lámina ya armada).
CAMARA = {
    "estatica": "Quieta",
}
CAMARA_DEFECTO = "estatica"

# Cómo se pasa de una escena a la siguiente.
TRANSICION = {
    "corte": "Corte directo",
}
TRANSICION_DEFECTO = "corte"
