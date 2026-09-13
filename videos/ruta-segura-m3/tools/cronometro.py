# -*- coding: utf-8 -*-
"""El reloj del módulo: convierte tiempos de una locución a los de otra.

Las láminas se componen contra **una** locución concreta —la que estaba cuando se
escribieron las marcas de tiempo— y esa queda congelada en
`tiempos-referencia.json`. Cuando la definitiva la ponga otra voz (otra de
ElevenLabs, o una persona en un estudio), las frases duran otra cosa y el montaje
tiene que seguirla.

En vez de reescribir a mano las decenas de marcas de `tools/eNN.py`, aquí se
construye un **mapa** entre las dos locuciones:

- exacto en cada frontera de frase — son las mismas frases y en el mismo orden;
- proporcional dentro de cada frase, que es donde caen los desfases de medio
  segundo de las apariciones;
- desplazamiento fijo tras la última frase, para que la cola conserve su aire.

Flujo normal:

1. `voz-eleven.py` escribe `tiempos-voz.json`.
2. La primera vez se copia a `tiempos-referencia.json` y se componen las láminas
   contra esos tiempos (el mapa es la identidad).
3. Cualquier locución posterior solo reescribe `tiempos-voz.json`; el mapa hace
   el resto.

A diferencia del módulo 1, aquí no hay medición previa con Piper: la locución de
referencia **es** la primera de ElevenLabs, que es la que de verdad se oye.
"""
import io, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))

AIRE = 1.2          # respiro al final de cada lámina, después de la última frase


def _cargar(nombre):
    ruta = os.path.join(AQUI, nombre)
    if not os.path.exists(ruta):
        return None
    d = json.load(io.open(ruta, encoding="utf-8"))
    return {o["n"]: [float(x) for x in o["inicios"]] for o in d}


VOZ = _cargar("tiempos-voz.json")
REF = _cargar("tiempos-referencia.json") or VOZ


def mapa(n):
    """Devuelve f(t) que lleva un tiempo de la referencia al de la locución."""
    if VOZ is None or REF is None or n not in VOZ or n not in REF or REF is VOZ:
        return lambda t: t
    p, v = REF[n], VOZ[n]
    if len(p) != len(v):
        raise ValueError("lámina %d: %d frases en la referencia y %d en la locución"
                         % (n, len(p) - 1, len(v) - 1))

    def f(t):
        if t <= 0:
            return t
        if t >= p[-1]:
            return round(v[-1] + (t - p[-1]), 3)
        for i in range(len(p) - 1):
            if p[i] <= t < p[i + 1]:
                ancho = p[i + 1] - p[i]
                if ancho <= 0:
                    return v[i]
                return round(v[i] + (t - p[i]) * (v[i + 1] - v[i]) / ancho, 3)
        return t
    return f


def narracion(n):
    """Cuánto dura la narración de la lámina en la locución vigente."""
    if VOZ and n in VOZ:
        return VOZ[n][-1]
    if REF and n in REF:
        return REF[n][-1]
    raise SystemExit("no hay tiempos para la lámina %d — corre antes tools/voz-eleven.py" % n)


def inicios(n):
    """Inicios de frase de la locución de referencia, para componer contra ellos."""
    return (REF or VOZ)[n]


def duracion(n, minimo=0.0):
    """Duración de la lámina: su narración más el aire, redondeada a medio segundo."""
    d = max(narracion(n) + AIRE, minimo)
    return round(d * 2) / 2.0
