# -*- coding: utf-8 -*-
"""El reloj del módulo: convierte tiempos de una locución a los de otra.

Las once láminas se compusieron contra una medición de referencia hecha con
Piper (`tiempos-medidos.json`). Cuando la locución definitiva la pone otra voz
—ElevenLabs ahora, una persona más adelante— las frases duran otra cosa y el
montaje tiene que seguirla.

En vez de reescribir a mano las ochenta y tantas marcas de tiempo de
`tools/eNN.py`, aquí se construye un **mapa** entre las dos locuciones:

- exacto en cada frontera de frase — las frases son las mismas y en el mismo orden;
- proporcional dentro de cada frase — que es justo donde caen los desfases de
  medio segundo que tienen las apariciones;
- desplazamiento fijo después de la última frase, para que la cola de la lámina
  conserve su aire.

Si no existe `tools/tiempos-voz.json`, el mapa es la identidad y el video se
construye con los tiempos de referencia.
"""
import io, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))

AIRE = 1.2          # respiro al final de cada lámina, después de la última frase
ROTULO = 2.30       # «GUION DE VOZ — PRIMERA PERSONA»: está en la medición, no se locuta
CON_ROTULO = (7, 11)


def _inicios(duraciones):
    t, out = 0.0, []
    for d in duraciones:
        out.append(round(t, 3))
        t += d
    out.append(round(t, 3))      # el último elemento es el final de la narración
    return out


def _referencia():
    d = json.load(io.open(os.path.join(AQUI, "tiempos-medidos.json"), encoding="utf-8"))
    ref = {}
    for o in d:
        durs = [f["dur"] for f in o["frases"]]
        if o["n"] in CON_ROTULO:
            durs[0] = round(durs[0] - ROTULO, 3)
        ref[o["n"]] = _inicios(durs)
    return ref


def _voz():
    ruta = os.path.join(AQUI, "tiempos-voz.json")
    if not os.path.exists(ruta):
        return None
    d = json.load(io.open(ruta, encoding="utf-8"))
    return {o["n"]: [float(x) for x in o["inicios"]] for o in d}


REF = _referencia()
VOZ = _voz()


def mapa(n):
    """Devuelve f(t) que lleva un tiempo de la referencia al de la locución."""
    if VOZ is None or n not in VOZ:
        return lambda t: t
    p, v = REF[n], VOZ[n]
    if len(p) != len(v):
        raise ValueError("lámina %d: %d frases medidas y %d locutadas" % (n, len(p) - 1, len(v) - 1))

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
    return (VOZ[n][-1] if VOZ and n in VOZ else REF[n][-1])


def duracion(n, minimo=0.0):
    """Duración de la lámina: su narración más el aire, redondeada a medio segundo."""
    d = max(narracion(n) + AIRE, minimo)
    return round(d * 2) / 2.0
