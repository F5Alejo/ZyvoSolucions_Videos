"""Lámina del PPTX → composición de HyperFrames: la diapositiva, animada forma por forma.

La diferencia con `motor/escenas/__init__.py`: aquella **rearma** la lámina sobre la plantilla de
la marca (título, viñetas, foto y los anillos), y por eso el video no se parece a la
presentación. Esta la **redibuja**: cada forma va donde estaba, del tamaño que era y con su
color, y se anima por separado.

    PPTX ─▶ app/disposicion.py ─▶ formas con caja, color y texto
                                       │
                                       ▼
                        grupos de aparición (este módulo)
                                       │
                            cada grupo ◀── una frase de la narración
                                       ▼
                        composición de HyperFrames (lamina.html)

## Los grupos de aparición

En la lámina no entra todo a la vez: entra por bloques, al ritmo de lo que dice la voz. Los
bloques salen de los nombres de las formas, que en una presentación bien hecha ya los traen:

    section · page · header-rule · title · body · bar-1 · bar-accent-1 · bar-num-1 · bar-2 · …

- Las formas de **fondo** (`fondo=True`) entran con la escena: nunca se ve el lienzo vacío.
- Las que terminan en un número (`bar-1`, `bar-accent-1`, `bar-num-1`) son **un mismo bloque**:
  la tarjeta 1 entra entera, no a pedazos.
- Las demás entran una por una, en orden de pintado.

Después cada bloque se engancha a la frase de la narración que le toca, con los tiempos reales
que midió `motor/voz.py`. Si hay más bloques que frases, varios comparten frase; si hay menos,
se reparten a lo largo de la lámina.

## El contrato de HyperFrames

Una composición por lámina, cargada como sub-composición desde el `index.html` del video
(`data-composition-src`). Dentro: un `<template>` con su `<style>` y su `<script>`, un root
dimensionado con `data-width`/`data-height`/`data-duration`, y **una sola** línea de tiempo de
GSAP en pausa registrada en `window.__timelines[<id>]`. El render la lleva cuadro a cuadro a su
instante exacto, así que el resultado es idéntico en cada pasada.

Cada forma va en dos capas: la de fuera lleva su sitio, su tamaño y su giro en CSS; la de
dentro es la que se anima. Así nunca chocan un `transform` del CSS y un tween de GSAP sobre la
misma propiedad, que es lo que `hyperframes lint` rechaza con `gsap_css_transform_conflict`.
"""

import json
import math
import re
import unicodedata
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from motor.escenas import efectos

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "fuentes" / "Montserrat.ttf"

_entorno = Environment(loader=FileSystemLoader(AQUI), autoescape=select_autoescape(["html"]))

# Un punto de PowerPoint son 1/72 de pulgada sobre una lámina de 7,5 pulgadas de alto.
PT_POR_PULGADA = 72

# Efecto del catálogo → el tween de GSAP que lo reproduce. `desde` es el estado inicial.
# Son los mismos nombres que usan las plantillas de animación, para que el vocabulario no cambie.
#
# Los recorridos son **cortos** a propósito. Un elemento que viaja 60 px en medio segundo se
# ve brusco; el mismo recorrido en 24 px se lee como un asentamiento. Es la norma de
# HyperFrames para las entradas (`hyperframes-animation`, adapters/gsap-easing-and-stagger).
TWEENS = {
    "ninguno": None,
    "aparecer": {"opacity": 0},
    "subir": {"opacity": 0, "y": 10},
    "bajar": {"opacity": 0, "y": -10},
    "deslizar-izquierda": {"opacity": 0, "x": -10},
    "deslizar-derecha": {"opacity": 0, "x": 10},
    "escalar": {"opacity": 0, "scale": 0.97},
    "desenfoque": {"opacity": 0, "filter": "blur(6px)"},
    "revelar": {"clipPath": "inset(0 100% 0 0)"},
    "rebote": {"opacity": 0, "scale": 0.6},
    "girar": {"opacity": 0, "rotation": -8, "scale": 0.96},
    "crecer": {"scaleX": 0},
}
# El estado final de cada propiedad que un efecto puede mover: la forma, ya en su sitio.
EN_SITIO = {"opacity": 1, "x": 0, "y": 0, "scale": 1, "scaleX": 1, "rotation": 0,
            "filter": "blur(0px)", "clipPath": "inset(0 0 0 0)"}
# Las curvas del catálogo en el lenguaje de GSAP. `power3.out` es la curva de la casa: arranca
# rápido y se posa largo, que es lo que hace que una entrada se sienta fluida y no mecánica.
# El rebote (`back`) queda como registro aparte, para cuando se pide algo juguetón: de serie no.
CURVAS = {
    "suave": "power3.out",
    "energica": "expo.out",
    "rebote": "back.out(1.4)",
    "lineal": "none",
}
CURVA_CONTINUA = "sine.inOut"  # para lo que no entra ni sale, sino que respira

# Qué efecto usa cada tipo de forma cuando la plantilla no dice otra cosa. Es la entrada
# discreta del video de referencia: el elemento sube un poco y aparece.
# Medido en las referencias: el elemento entra desplazado ~10 px a la derecha y se asienta;
# las imágenes se descubren con un barrido horizontal anclado a la izquierda.
POR_TIPO = {
    "imagen": "revelar",
    "linea": "crecer",
    "figura": "deslizar-derecha",
    "tabla": "aparecer",
    "grafico": "aparecer",
    "texto": "deslizar-derecha",
}
# Los tiempos salen de medir los videos de referencia cuadro a cuadro (ver `docs/bitacora.md`):
# la entrada dura 0,23 s y la opacidad sube en 0,13; el elemento viaja unos 10 px. Es decir,
# entradas **rápidas y pequeñas**, muy separadas entre sí. Lo que da el ritmo no es la
# animación: es cada cuánto habla la voz.
DURACION_ENTRADA = 0.25
ESCALONADO = 0.06         # entre las piezas de un mismo bloque (el número y su etiqueta)
ESCALONADO_MAXIMO = 0.25  # un bloque entero tiene que leerse como una sola llegada
ADELANTO = 0.2            # el elemento empieza a entrar justo antes de que la voz lo nombre

# La lámina entra con un fundido y **también sale con uno**. En las referencias el cambio de
# sección es un bajón a fondo: lo de antes se funde entero, hay un respiro vacío y lo nuevo se
# reconstruye. No es un encadenado.
FUNDIDO_LAMINA = 0.5
SALIDA_LAMINA = 0.45
LAMINA_MINIMA_PARA_SALIR = 6.0  # en una lámina corta, fundir al salir se comería el contenido

# Las imágenes no se quedan quietas: crecen muy despacio a lo largo de la lámina (Ken Burns).
# Es casi imperceptible por cuadro y es lo que hace que el plano no parezca congelado.
DERIVA_IMAGEN = 0.04

# El resaltado que sigue a la voz: la viñeta recién nombrada se queda sobre un fondo del color
# de la marca, muy diluido, y se apaga cuando entra la siguiente. Es lo que más ayuda a seguir
# la lámina mientras se escucha, y el rasgo más reconocible de los videos de referencia.
RESALTE_ALFA = 0.18
RESALTE_ENTRA = 0.25
RESALTE_SALE = 0.45


def _sufijo(id_: str) -> str | None:
    """El número con el que termina el nombre de una forma: `bar-accent-12` → `12`."""
    m = re.search(r"-(\d+)$", id_)
    return m.group(1) if m else None


def _es_escenografia(f: dict) -> bool:
    """Una forma que no es una idea que la voz desarrolle: está ahí desde el principio.

    Son el fondo, el marco de la lámina (título, sección, numeración, filetes) y la
    decoración: toda forma sin texto que no pertenezca a un bloque numerado. Sin esta regla,
    la foto y la barra de color se comen los turnos de aparición y el título acaba entrando
    medio minuto tarde, que es justo lo que no se quiere.
    """
    if f["fondo"] or f.get("es_marco"):
        return True
    return not f["texto"].strip() and _sufijo(f["id"]) is None


def grupos(formas: list[dict]) -> list[list[dict]]:
    """Las formas repartidas en bloques de aparición, en orden.

    El primer bloque es la escenografía: entra con la escena, para que la lámina nunca se vea
    a medio montar. Después, un bloque por número de sufijo (`bar-1`, `bar-num-1` → el mismo)
    y uno por cada forma suelta con texto, ordenados por z.
    """
    base = [f for f in formas if _es_escenografia(f)]
    resto = [f for f in formas if not _es_escenografia(f)]

    bloques: dict[str, list[dict]] = {}
    for f in sorted(resto, key=lambda f: f["z"]):
        n = _sufijo(f["id"])
        clave = f"n{n}" if n else f"z{f['z']}"
        bloques.setdefault(clave, []).append(f)

    ordenados = sorted(bloques.values(), key=lambda b: min(f["z"] for f in b))
    return ([base] if base else []) + ordenados


# ── Enganchar cada bloque con lo que dice la voz ──────────────────────────────
#
# Repartir los bloques por orden («el tercero de ocho entra en la tercera frase de ocho») es
# fácil y queda mal: si la voz habla de «Percibir» en la quinta frase, la tarjeta sale cuatro
# frases antes y la lámina va por su lado. Aquí se busca, para cada bloque, **la frase que lo
# nombra**, comparando sus palabras.
#
# Las palabras no pesan igual: una que sale en todas las frases no distingue nada, y una que
# sale en una sola señala esa frase. De ahí el peso tipo IDF. Un bloque solo se da por
# enganchado si la coincidencia pasa de `UMBRAL`; los demás se reparten entre sus vecinos
# enganchados, que es mejor que forzar una coincidencia mala.

PALABRAS_VACIAS = frozenset("""
al algo alguna algunas alguno algunos ante antes aqui asi aun aunque bien cada como con contra
cual cuales cuando cuanto desde donde dos durante ella ellas ello ellos entre era eran eres esa
esas ese eso esos esta estan estas este esto estos fue fueron hace hacia han has hasta incluso
los las le les lo mas menos mientras muy nos otra otras otro otros para pero poco por porque
pues que quien quienes segun ser si sin sobre solo son su sus tambien tanto tiene tienen todo
toda todas todos tras una uno unos
""".split())
UMBRAL = 0.9  # por debajo de esto la coincidencia no es de fiar: mejor repartir


RAIZ = 5  # cuántas letras se conservan de cada palabra


def _tokens(texto: str) -> set[str]:
    """Las **raíces** de las palabras con contenido, sin tildes ni mayúsculas.

    Se comparan raíces y no palabras enteras porque unas buenas notas del orador no leen la
    lámina: la parafrasean. La diapositiva dice «Los errores se analizan» y la voz dice «las
    experiencias pueden analizarse»; «experiencia» y «experiencias» son la misma idea. Cortar
    a las primeras letras es tosco, pero en español pilla casi todas las flexiones (plurales,
    conjugaciones, derivados) sin meter un lematizador entero en el motor.
    """
    t = unicodedata.normalize("NFD", (texto or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return {p[:RAIZ] for p in re.findall(r"[a-z0-9]{3,}", t) if p not in PALABRAS_VACIAS}


def cobertura(visible: str, narracion: str) -> float:
    """Qué parte de lo que se ve en la lámina llega a nombrar la voz (0..1).

    Es la medida de si el video «cuenta la lámina» o va por su lado. En los videos de
    referencia del curso da **1,0**: la voz enumera la lámina casi palabra por palabra. Cuando
    las notas del orador son un ensayo paralelo baja a 0,3-0,4, y entonces se oye una cosa
    mientras se ve otra, por bien escritas que estén las dos.

    La usa el agente guionista (`motor/agentes/textos.py`) para proponer un arreglo.
    """
    v, n = _tokens(visible), _tokens(narracion)
    return len(v & n) / len(v) if v else 1.0


def _pesos(frases: list[set[str]]) -> dict[str, float]:
    """Cuánto distingue cada palabra: mucho si sale en una frase, nada si sale en todas."""
    cuenta: dict[str, int] = {}
    for f in frases:
        for w in f:
            cuenta[w] = cuenta.get(w, 0) + 1
    n = max(len(frases), 1)
    return {w: math.log(1 + n / v) for w, v in cuenta.items()}


def _afinidad(bloque: set[str], frase: set[str], pesos: dict[str, float]) -> float:
    if not bloque or not frase:
        return 0.0
    # Se divide por el tamaño del bloque para que un texto largo no gane solo por serlo.
    return sum(pesos.get(w, 1.0) for w in bloque & frase) / math.sqrt(len(bloque))


def emparejar(textos: list[str], frases: list[str]) -> list[int | None]:
    """Para cada bloque, la frase que lo nombra, o None si ninguna lo hace con claridad.

    El resultado es monótono: un bloque nunca se engancha a una frase anterior a la de un
    bloque que ya entró, porque en la lámina las cosas aparecen en orden.
    """
    conjuntos = [_tokens(f) for f in frases]
    pesos = _pesos(conjuntos)
    salida: list[int | None] = []
    for texto in textos:
        b = _tokens(texto)
        puntos = [_afinidad(b, f, pesos) for f in conjuntos]
        if not puntos or max(puntos) < UMBRAL:
            salida.append(None)
            continue
        salida.append(max(range(len(puntos)), key=lambda i: puntos[i]))

    tope = -1
    for i, j in enumerate(salida):
        if j is None:
            continue
        if j < tope:
            salida[i] = None  # iría hacia atrás: no vale como ancla
        else:
            tope = j
    return salida


def _repartir(anclas: list[float | None], primero: float, ultimo: float) -> list[float]:
    """Los bloques sin ancla se reparten entre los que sí la tienen."""
    t = list(anclas)
    puestos = [i for i, x in enumerate(t) if x is not None]
    if not puestos:
        n = len(t)
        return [primero + (ultimo - primero) * i / max(n - 1, 1) for i in range(n)]
    for i in range(len(t)):
        if t[i] is not None:
            continue
        antes = [p for p in puestos if p < i]
        despues = [p for p in puestos if p > i]
        if antes and despues:
            a, d = antes[-1], despues[0]
            t[i] = t[a] + (t[d] - t[a]) * (i - a) / (d - a)
        elif antes:  # después del último ancla: hacia el final de la lámina
            a = antes[-1]
            t[i] = t[a] + (ultimo - t[a]) * (i - a) / max(len(t) - a, 1)
        else:        # antes del primer ancla
            d = despues[0]
            t[i] = primero + (t[d] - primero) * i / max(d, 1)
    return [float(x) for x in t]


def tiempos(bloques: list[list[dict]], narracion: list, duracion: float, hay_base: bool,
            desde: float = 0.0) -> list[float]:
    """El segundo **de la escena** en que entra cada bloque, enganchado a lo que dice la voz.

    Ojo con `desde`: el `inicio` de una frase resuelta es el segundo del **video** entero
    (`videospec.Frase`), no el de su escena. La composición de una lámina empieza a contar en
    cero, así que hay que restarle dónde empieza la escena. Sin eso, en la lámina 3 de un curso
    todos los bloques se iban al final y no se veía entrar nada.

    La escenografía entra en 0. Cada bloque de contenido entra con la frase que lo nombra
    (ver `emparejar`); los que no coinciden con ninguna se reparten entre sus vecinos.
    """
    animables = [b for i, b in enumerate(bloques) if not (hay_base and i == 0)]
    inicios = [max(0.0, (f.inicio or 0.0) - desde) for f in narracion] if narracion else []
    tope = max(duracion - DURACION_ENTRADA, 0)

    n = len(animables)
    if inicios:
        textos = [" ".join(f["texto"] for f in b) for b in animables]
        enganches = emparejar(textos, [getattr(f, "texto", "") or "" for f in narracion])
        if any(j is not None for j in enganches):
            crudos = _repartir([inicios[j] if j is not None else None for j in enganches],
                               inicios[0], inicios[-1])
            # Un bloque sin ancla cae interpolado, a mitad de una frase. Se lleva al comienzo
            # de la frase más cercana: una entrada que coincide con un cambio de frase parece
            # intencionada, y una que cae en medio parece un descuadre.
            crudos = [t if j is not None else min(inicios, key=lambda x: abs(x - t))
                      for t, j in zip(crudos, enganches)]
        else:
            # Ninguna frase nombra a ningún bloque (narración genérica): se reparten por orden.
            crudos = [inicios[min(len(inicios) - 1, round(k * len(inicios) / max(n, 1)))]
                      for k in range(n)]
    else:
        crudos = [duracion * k / max(n, 1) for k in range(n)]

    salida = [0.0] if hay_base else []
    salida += [round(max(0.0, min(t - ADELANTO, tope)), 3) for t in crudos]
    return salida


def _efecto(f: dict, plan: dict | None) -> tuple[str, float, str]:
    """(efecto, duración, curva) con que entra una forma."""
    base = POR_TIPO.get(f["tipo"], "aparecer")
    dur, curva = DURACION_ENTRADA, "suave"
    if plan:
        # La plantilla manda por el rol que más se le parece: el título usa «titulo», el resto «vinetas».
        rol = "titulo" if f["id"].startswith(("title", "titulo", "cover-title")) else "vinetas"
        paso = (plan.get("elementos") or {}).get(rol, {}).get("entrada") or {}
        if paso.get("efecto") in TWEENS:
            base = paso["efecto"]
        dur = paso.get("duracion") or dur
        curva = paso.get("curva") or curva
    return base, round(float(dur), 3), curva


def _orden_lectura(bloque: list[dict]) -> list[dict]:
    """Las formas de un bloque en el orden en que se leen: de arriba abajo y de izquierda a derecha."""
    return sorted(bloque, key=lambda f: (round(f["y"], 2), round(f["x"], 2), f["z"]))


def animacion(bloques: list[list[dict]], instantes: list[float], plan: dict | None,
              hay_base: bool = False, duracion: float = 0.0, resalte: str | None = None) -> list[dict]:
    """Los tweens de la lámina: a quién, desde qué estado, cuándo y con qué curva.

    Tres capas, de menos a más visible:

    - **La lámina entera** entra con un fundido (`.todo`). La escenografía —fondo, marco,
      decoración— viaja con él, en vez de animarse forma por forma: así no hay un corte seco
      al cambiar de lámina ni un revuelo de diez elementos moviéndose a la vez.
    - **Cada bloque de contenido** entra con su efecto, escalonando sus formas en orden de
      lectura. El escalonado se reparte dentro de `ESCALONADO_MAXIMO` para que la llegada del
      bloque se lea como un solo gesto y no como un goteo.
    - **Las imágenes** crecen muy despacio durante toda la lámina. Va `inmediato: False`
      porque es un segundo tween sobre la misma forma: sin eso GSAP aplicaría su estado
      inicial al construir la línea de tiempo y pisaría la entrada.
    - **El resaltado** acompaña a la voz de una viñeta a la siguiente (ver `_resaltes`), y la
      lámina se funde al final para que el cambio no sea un corte.
    """
    pasos: list[dict] = []
    if hay_base:
        pasos.append({"selector": ".todo", "desde": {"opacity": 0}, "hasta": {"opacity": 1},
                      "duracion": FUNDIDO_LAMINA, "curva": CURVA_CONTINUA, "en": 0.0})

    for i, (bloque, t) in enumerate(zip(bloques, instantes)):
        if hay_base and i == 0:
            continue  # la escenografía ya entra con el fundido de la lámina
        formas = _orden_lectura(bloque)
        paso = min(ESCALONADO, ESCALONADO_MAXIMO / max(len(formas) - 1, 1)) if len(formas) > 1 else 0.0
        for k, f in enumerate(formas):
            ef, dur, curva = _efecto(f, plan)
            desde = TWEENS.get(ef)
            if desde is None:
                continue
            pasos.append({
                "selector": f"#{f['_cid']} > .a",
                "desde": desde,
                # Solo se devuelve a su sitio lo que el efecto movió: si se tocara todo, cada
                # forma acabaría con un `clip-path` y un `transform` que no pidió nadie.
                "hasta": {k2: EN_SITIO[k2] for k2 in desde},
                "duracion": dur,
                "curva": CURVAS.get(curva, CURVAS["suave"]),
                "en": round(t + k * paso, 3),
                "origen": "left center" if ef == "crecer" else "center center",
            })

    if duracion > 0:
        for f in (x for b in bloques for x in b if x["tipo"] == "imagen"):
            pasos.append({
                "selector": f"#{f['_cid']} > .a",
                "desde": {"scale": 1}, "hasta": {"scale": round(1 + DERIVA_IMAGEN, 3)},
                "duracion": round(duracion, 3), "curva": CURVA_CONTINUA, "en": 0.0,
                "origen": "center center", "inmediato": False,
            })
        pasos += _resaltes(bloques, instantes, hay_base, duracion, resalte)
        if duracion >= LAMINA_MINIMA_PARA_SALIR:
            # La lámina se funde al final: el cambio de lámina es un bajón a fondo, no un corte.
            pasos.append({"selector": ".todo", "desde": {"opacity": 1}, "hasta": {"opacity": 0},
                          "duracion": SALIDA_LAMINA, "curva": CURVA_CONTINUA,
                          "en": round(duracion - SALIDA_LAMINA, 3), "inmediato": False})
    return pasos


def _diluir(hexa: str | None) -> str | None:
    """El color de la marca como un velo: `#fdc100` → `rgba(253,193,0,0.18)`."""
    h = (hexa or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None
    return f"rgba({r},{g},{b},{RESALTE_ALFA})"


PARRAFOS_RESALTABLES = 2  # más que esto ya no es «lo que se está diciendo», es una lista


def _resaltable(f: dict) -> bool:
    """Una viñeta de texto corta y sin fondo propio: se le puede poner el resaltado detrás.

    Una caja con muchos párrafos queda fuera: resaltar una lista entera de cinco viñetas no
    señala nada, solo pinta medio lienzo. En las referencias lo que se resalta son etiquetas
    de una o dos líneas, que es donde el resaltado dice «de esto se está hablando ahora».
    """
    return (f["tipo"] == "texto" and not f.get("relleno") and bool(f["texto"].strip())
            and len([p for p in (f.get("parrafos") or []) if not p.get("vacio")]) <= PARRAFOS_RESALTABLES)


def _resaltes(bloques: list[list[dict]], instantes: list[float], hay_base: bool,
              duracion: float, color: str | None) -> list[dict]:
    """El resaltado que va siguiendo a la voz por la lámina.

    Cuando entra un bloque, su texto se queda sobre un fondo del color de la marca muy
    diluido; cuando entra el siguiente, se apaga. Así, quien mira sabe en todo momento de qué
    se está hablando, que es lo que hace legibles los videos de referencia.

    Solo se resaltan las viñetas de texto sin relleno propio: ponerle un fondo a una forma que
    ya tiene el suyo la rompería.
    """
    if not color:
        return []
    pasos = []
    contenido = [(i, b) for i, b in enumerate(bloques) if not (hay_base and i == 0)]
    for n, (i, bloque) in enumerate(contenido):
        objetivos = [f for f in bloque if _resaltable(f)]
        if not objetivos:
            continue
        entra = instantes[i]
        # Se apaga cuando llega el bloque siguiente; el último se queda encendido hasta el final.
        siguiente = contenido[n + 1][0] if n + 1 < len(contenido) else None
        apaga = instantes[siguiente] if siguiente is not None else max(duracion - SALIDA_LAMINA, entra)
        # Nunca antes de terminar de encenderse. Sin este tope, dos bloques que entran casi a
        # la vez dejaban el resaltado encendido para siempre: el apagado no llegaba a emitirse
        # y acababa media lámina subrayada.
        apaga = max(apaga, entra + RESALTE_ENTRA)
        for f in objetivos:
            # El resaltado va sobre los párrafos, no sobre la caja de la forma. Así abraza al
            # texto —como en las referencias— y, de paso, no se ve nada raro cuando el texto
            # rebasa un poco su caja, que en un PPTX pasa a menudo.
            sel = f"#{f['_cid']} > .a > p"
            pasos.append({"selector": sel, "desde": {"backgroundColor": "rgba(0,0,0,0)"},
                          "hasta": {"backgroundColor": color}, "duracion": RESALTE_ENTRA,
                          "curva": CURVAS["suave"], "en": round(entra, 3), "inmediato": False})
            pasos.append({"selector": sel, "desde": {"backgroundColor": color},
                          "hasta": {"backgroundColor": "rgba(0,0,0,0)"},
                          "duracion": RESALTE_SALE, "curva": CURVAS["suave"],
                          "en": round(apaga, 3), "inmediato": False})
    return pasos


# ── Lo que se dibuja ──────────────────────────────────────────────────────────

def _px(v: float, total: int) -> float:
    return round(v * total, 2)


def _caja_px(f: dict, ancho: int, alto: int) -> tuple[float, float]:
    return _px(f["w"], ancho), max(_px(f["h"], alto), 1)


def _estilo_forma(f: dict, ancho: int, alto: int) -> str:
    w, h = _caja_px(f, ancho, alto)
    # También en línea: ver `_estilo_caja`. Sin el `position` la forma no se queda en su sitio.
    partes = ["position:absolute", "box-sizing:border-box",
              f"left:{_px(f['x'], ancho)}px", f"top:{_px(f['y'], alto)}px",
              f"width:{w}px", f"height:{h}px", f"z-index:{f['z']}"]
    if f.get("giro"):
        partes.append(f"transform:rotate({f['giro']}deg)")
    return ";".join(partes)


def _estilo_caja(f: dict, pt_px: float) -> str:
    """El relleno, el borde y los márgenes internos de la forma (la capa que se anima).

    Va en línea, no en la hoja de estilos, y trae también su tamaño y su caja: así la forma
    mide lo que tiene que medir desde el primer momento. El estilo de una sub-composición lo
    reescribe el runtime para scoparlo, y mientras tanto el ajuste de texto ya está midiendo.
    """
    partes = ["box-sizing:border-box", "width:100%", "height:100%",
              "display:flex", "flex-direction:column"]
    if f.get("relleno"):
        partes.append(f"background:{f['relleno']}")
    b = f.get("borde")
    if b:
        propiedad = "border-top" if f["tipo"] == "linea" else "border"
        partes.append(f"{propiedad}:{max(b['grosor_pt'] * pt_px, 1):.2f}px solid {b['color']}")
    elif f["tipo"] == "linea" and f.get("relleno"):
        partes.append(f"border-top:{max(1.5 * pt_px, 1):.2f}px solid {f['relleno']}")
    marco = f.get("marco") or {}
    if marco.get("margenes_pt") and f["tipo"] == "texto":
        t, r, b_, l = (round((m or 0) * pt_px, 2) for m in marco["margenes_pt"])
        partes.append(f"padding:{t}px {r}px {b_}px {l}px")
        partes.append(f"justify-content:{marco.get('ancla', 'flex-start')}")
    return ";".join(partes)


# ── Encajar el texto en su caja ───────────────────────────────────────────────
#
# La lámina está diseñada con la tipografía del PPTX y se dibuja con la del proyecto, que no
# tiene las mismas medidas: un texto que en PowerPoint entraba en dos líneas aquí puede pedir
# tres y salirse de su caja, y la forma de al lado se lo come.
#
# PowerPoint resuelve esto achicando el texto («reducir el texto al desbordarse») y aquí se
# hace igual, **en Python**. En el navegador no se puede: cuando la composición se arma, cada
# lámina está fuera de su ventana de tiempo y el framework la tiene oculta, así que mide cero
# y no hay nada que comparar. Con las métricas de la fuente el cálculo es exacto y, además,
# sale siempre el mismo número en cada render.

MINIMO = 0.4  # no se achica a menos de esto: antes se prefiere que el desvío se note
PASO = 0.03
PESO_NORMAL, PESO_NEGRITA = 400, 700
_fuentes: dict[tuple[str, int, int], object] = {}


def _tipo(tam: int, peso: int):
    """La fuente a un tamaño y un peso, en caché: abrirla por cada línea sería carísimo.

    El peso hay que **fijarlo**: Montserrat es una fuente variable y su eje de peso viene con
    `default: 100` (Thin), así que al abrirla sin más se mide la variante más estrecha que
    existe, mientras el navegador dibuja en 400 o en 700. Midiendo así el texto parecía
    entrar siempre y no se achicaba nada.
    """
    clave = (str(FUENTE), tam, peso)
    if clave not in _fuentes:
        from PIL import ImageFont
        try:
            f = ImageFont.truetype(str(FUENTE), tam)
            try:
                f.set_variation_by_axes([peso])
            except (OSError, AttributeError, ValueError):
                pass  # fuente no variable: su único peso es el que hay
            _fuentes[clave] = f
        except OSError:
            _fuentes[clave] = None
    return _fuentes[clave]


def _ancho(texto: str, px: float, negrita: bool) -> float:
    f = _tipo(max(1, round(px)), PESO_NEGRITA if negrita else PESO_NORMAL)
    if f is None:  # sin la fuente a mano, una estimación: 0,55 em por carácter
        return len(texto) * px * 0.55
    return f.getlength(texto)


def _lineas(texto: str, px: float, negrita: bool, ancho: float) -> int:
    """Cuántas líneas ocupa un párrafo al cortarlo por palabras en un ancho dado."""
    if not texto.strip():
        return 1
    n, actual = 1, ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if actual and _ancho(prueba, px, negrita) > ancho:
            n, actual = n + 1, palabra
        else:
            actual = prueba
    return n


def _alto_texto(f: dict, k: float, pt_px: float, ancho: float) -> float:
    """Lo que mide el texto de una forma con las letras al `k` de su tamaño."""
    total = 0.0
    for p in f.get("parrafos") or []:
        if p.get("vacio"):
            total += 0.6 * 16 * k
            continue
        px = max((r.get("pt") or 18) for r in p["runs"]) * pt_px * k
        negrita = any(r.get("negrita") for r in p["runs"])
        texto = "".join(r["texto"] for r in p["runs"])
        sangria = (p.get("nivel") or 0) * 24
        total += _lineas(texto, px, negrita, max(ancho - sangria, 1)) * px * (p.get("interlineado") or 1.22)
    return total


def encajar(f: dict, pt_px: float, ancho_px: float, alto_px: float, estricto: bool = False) -> float:
    """Cuánto hay que achicar el texto de una forma para que entre en su caja (1.0 = nada).

    Con `estricto` se descuentan también los márgenes de arriba y abajo. Se usa cuando la caja
    va a **verse** —porque lleva el resaltado detrás—: ahí el texto tiene que caber de verdad.
    Si la caja es invisible no hace falta, y descontarlos achicaría media lámina sin motivo
    (una caja ajustada al texto «desbordaría» siempre).
    """
    if not (f.get("parrafos") and f["texto"].strip()):
        return 1.0
    t, r, b, l = ((m or 0) * pt_px for m in (f.get("marco") or {}).get("margenes_pt") or (0, 0, 0, 0))
    # Los márgenes de los lados siempre: son los que deciden dónde corta la línea.
    util_ancho = max(ancho_px - l - r, 1)
    util_alto = max(alto_px - t - b, 1) if estricto else alto_px
    k = 1.0
    while k > MINIMO and _alto_texto(f, k, pt_px, util_ancho) > util_alto + 1:
        k -= PASO
    return round(max(k, MINIMO), 3)


def _estilo_run(r: dict, pt_px: float, k: float = 1.0) -> str:
    partes = []
    if r.get("pt"):
        partes.append(f"font-size:{round(r['pt'] * pt_px * k, 2)}px")
    if r.get("color"):
        partes.append(f"color:{r['color']}")
    if r.get("negrita"):
        partes.append("font-weight:700")
    if r.get("cursiva"):
        partes.append("font-style:italic")
    if r.get("subrayado"):
        partes.append("text-decoration:underline")
    return ";".join(partes)


def preparar(formas: list[dict], cid: str, ancho: int, alto: int, escala_pt: float,
             media: str = "") -> list[dict]:
    """Añade a cada forma lo que la plantilla necesita: su id único y sus estilos ya calculados.

    `media` es el prefijo con el que la composición llega a las imágenes (p. ej. `assets/media/`).
    Son rutas relativas, no `file://`: la composición se sirve por HTTP, tanto al previsualizar
    como al renderizar, y un `file://` no cargaría.
    """
    pt_px = alto / (7.5 * PT_POR_PULGADA) * (escala_pt or 1)
    listas = []
    for f in formas:
        f = dict(f)
        f["_cid"] = f"{cid}-{f['id']}"  # único en la página ya ensamblada
        f["_estilo"] = _estilo_forma(f, ancho, alto)
        f["_caja"] = _estilo_caja(f, pt_px)
        f["_w"], f["_h"] = _caja_px(f, ancho, alto)
        f["_k"] = encajar(f, pt_px, f["_w"], f["_h"])
        for p in f.get("parrafos") or []:
            for r in p["runs"]:
                r["_estilo"] = _estilo_run(r, pt_px, f["_k"])
        if f["tipo"] == "imagen":
            f["_src"] = f"{media}{f['archivo']}" if media else None
        listas.append(f)
    return listas


def composicion(formas: list[dict], narracion: list, duracion: float, cid: str,
                ancho: int = 1920, alto: int = 1080, escala_pt: float = 1.0,
                media: str = "", plan: dict | None = None, fuente: str = "",
                fondo: str | None = None, inicio_escena: float = 0.0,
                acento: str | None = None) -> str:
    """La sub-composición de HyperFrames de una lámina: su HTML completo.

    `inicio_escena` es el segundo del video en que arranca esta lámina: sirve para pasar los
    tiempos de la narración, que son absolutos, al reloj de la composición, que empieza en 0.
    """
    listas = preparar(formas, cid, ancho, alto, escala_pt, media)
    bloques = grupos(listas)
    hay_base = bool(bloques) and all(_es_escenografia(f) for f in bloques[0])
    instantes = tiempos(bloques, narracion, duracion, hay_base, inicio_escena)
    pasos = animacion(bloques, instantes, plan, hay_base, duracion, _diluir(acento))
    return _entorno.get_template("lamina.html").render(
        formas=listas, cid=cid, ancho=ancho, alto=alto, duracion=round(duracion, 3),
        pasos=json.dumps(pasos, ensure_ascii=False), fuente=fuente or FUENTE.resolve().as_uri(),
        fondo=fondo)


def indice(laminas: list[dict], ancho: int, alto: int, total: float, fondo: str = "#000000") -> str:
    """El `index.html` del video: cada lámina es una sub-composición con su sitio en el tiempo.

    `laminas`: [{"cid", "archivo", "inicio", "duracion"}] en orden.
    """
    return _entorno.get_template("video.html").render(
        laminas=laminas, ancho=ancho, alto=alto, total=round(total, 3), fondo=fondo)


# El catálogo que entiende este modo, para que la interfaz y las pruebas lo puedan consultar.
EFECTOS = tuple(k for k, v in TWEENS.items() if k in efectos.ENTRADA)
