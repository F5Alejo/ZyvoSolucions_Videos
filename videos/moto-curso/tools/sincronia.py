# -*- coding: utf-8 -*-
"""Cuándo entra cada elemento: en la frase de la narración que lo nombra.

Con 88 láminas no se escriben las marcas a mano. Para cada elemento de lista se
busca la frase de la nota que más palabras significativas comparte con él y se
toma el instante en que esa frase empieza. Tres reglas lo hacen robusto:

- **Orden.** Los elementos entran en el orden de la lámina aunque la narración
  los nombre desordenados: una marca nunca queda antes que la anterior.
- **Separación mínima.** Dos elementos no entran a menos de 0,55 s: si la nota
  nombra dos en la misma frase, el segundo espera su turno.
- **Sin coincidencia, reparto.** Si un elemento no aparece en la narración, se
  reparte entre sus vecinos en vez de apilarse al principio.
"""
import re
import unicodedata

VACIAS = set("""a al algo ante antes como con contra cual cuando de del desde donde durante el ella ellas
ellos en entre era es esa ese eso esta este esto hay la las le les lo los mas me mi muy no nos o para pero
por que se sea ser si sin sino sobre su sus tambien te tiene todo tras un una uno unos y ya""".split())


def normal(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def raices(t):
    """Palabras significativas recortadas a 5 letras: «inspección» e «inspeccionar» coinciden."""
    return {w[:5] for w in normal(t) if w not in VACIAS and len(w) > 2}


def marcas(elementos, frases, inicios, desde=1.2, hasta=None, separacion=0.55):
    """Devuelve un instante por elemento, en segundos dentro de la lámina."""
    fin = inicios[-1] if inicios else 10.0
    hasta = hasta if hasta is not None else max(fin * 0.72, desde + separacion * len(elementos))
    raiz_frases = [raices(f) for f in frases]

    # Solo vale una coincidencia clara: la mitad de las palabras del elemento (mínimo
    # dos, o todas si tiene menos). Con una sola palabra en común las notas que
    # parafrasean mandaban todos los elementos a la misma frase tardía.
    # Una coincidencia temprana de un elemento tardío no puede apretar a los de
    # antes: cada elemento sin marca propia necesita al menos PASO segundos.
    PASO = 2.5
    crudas, ultima, i_ultima = [], desde - PASO, -1
    for k, e in enumerate(elementos):
        re_ = raices(e)
        umbral = min(len(re_), max(2, -(-len(re_) // 2))) if re_ else 99
        mejor, puntos = None, 0
        for i, rf in enumerate(raiz_frases):
            p = len(re_ & rf)
            if p > puntos:
                mejor, puntos = i, p
        t = inicios[mejor] + 0.25 if mejor is not None and puntos >= umbral else None
        if t is not None and (t < ultima + (k - i_ultima) * PASO or t > hasta):
            t = None            # fuera de orden, apretado o demasiado tarde: se reparte
        crudas.append(t)
        if t is not None:
            ultima, i_ultima = t, k

    # sin coincidencia: interpolar entre vecinos conocidos
    n = len(crudas)
    for i in range(n):
        if crudas[i] is None:
            prev = next((crudas[j] for j in range(i - 1, -1, -1) if crudas[j] is not None), desde)
            nxt = next((crudas[j] for j in range(i + 1, n) if crudas[j] is not None), hasta)
            huecos = sum(1 for j in range(i, n) if crudas[j] is None) + 1
            crudas[i] = prev + max(nxt - prev, 0) / huecos

    # orden y separación
    out, ultimo = [], desde - separacion
    for t in crudas:
        t = max(min(t, hasta), ultimo + separacion)
        out.append(round(t, 2))
        ultimo = t
    return out


def frase_con(frases, inicios, patron, defecto):
    """Inicio de la primera frase que casa con `patron` (p. ej. la pregunta de pausa)."""
    for i, f in enumerate(frases):
        if re.search(patron, f, re.I):
            return round(inicios[i] + 0.2, 2)
    return defecto
