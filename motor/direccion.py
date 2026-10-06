"""El Director de ritmo: lo que dice la voz → lo que se ve, momento a momento.

Antes, cada lámina era una sola imagen durante toda su narración. Ahora cada frase (o cada trozo
de una frase larga) es un **momento** (`videospec.Beat`) con:

- el **texto en pantalla**: de 1 a 6 palabras, siempre sacadas de lo que dice la voz, que entran
  palabra por palabra justo cuando la voz las dice;
- la palabra **resaltada** (en el color de acento) y una **etiqueta** corta encima;
- la **toma** de fondo: un clip o una foto del banco de la empresa (app/banco.py), la imagen de
  la lámina, o el fondo animado de la marca.

Lo decide la IA de los agentes (Ollama o Claude, según Configuración) o, sin IA, unas reglas. La
IA solo **elige**: palabras que ya están en la frase y tomas que ya están en el banco. Lo que no
cumpla eso se descarta y ese momento se hace con reglas. No hay forma de que invente un dato.

La sincronía palabra a palabra se reparte por la longitud de cada palabra dentro del audio de su
frase: Kokoro y ElevenLabs hablan a ritmo parejo y el error queda por debajo de un cuarto de segundo.
"""

import hashlib
import json
import re
import unicodedata
from pathlib import Path

from app import banco, taller
from motor import videospec

VERSION = 1
MAX_PANTALLA = 6        # palabras en pantalla por momento
MAX_TROZO = 9           # una frase más larga que esto se parte en trozos
MIN_MOMENTO = 0.9       # segundos: un momento más corto se une al anterior

_VACIAS = set("""a al algo ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre
era es esa ese eso esta este esto estos estas fue ha han hay la las le les lo los me mi muy nos o otra otro para
pero por que se sea ser si sobre su sus también te tiene tienen tu un una uno unos unas y ya yo sus son está están
puede pueden cada qué cómo""".split())
# Cambian el sentido de la frase: nunca se quitan («No produce efecto» no es «produce efecto»).
_NEGACIONES = {"no", "nunca", "jamas", "ni", "sin", "tampoco", "nadie", "nada", "ningun", "ninguna", "ninguno"}
_CIFRA = re.compile(r"\d")


def _plano(palabra: str) -> str:
    p = unicodedata.normalize("NFKD", palabra.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9%]", "", p)


def _raiz(palabra: str) -> str:
    """Una raíz tosca para comparar («impresoras» ≈ «impresora»)."""
    p = _plano(palabra)
    return p[:-2] if p.endswith("es") and len(p) > 5 else p[:-1] if p.endswith("s") and len(p) > 4 else p


def _limpia(palabra: str) -> str:
    """La palabra como se ve en pantalla: sin la puntuación de los bordes (salvo ¿?¡! y %)."""
    return palabra.strip(".,;:()«»\"'“”‘’…—-")


def _contenido(palabra: str) -> bool:
    plano = _plano(palabra)
    return plano in _NEGACIONES or (plano not in _VACIAS and (len(plano) > 2 or bool(_CIFRA.search(palabra))))


def _con_negacion(palabras: list[str], i: int) -> int:
    """Si justo antes de la ventana hay una negación, la ventana empieza en ella."""
    while i > 0 and _plano(palabras[i - 1]) in _NEGACIONES:
        i -= 1
    return i


# ── Trozos: la frase partida en ideas cortas, con su tiempo ─────────────────

def trozos(frase: dict) -> list[dict]:
    """Parte una frase larga por comas, «y», «pero»… Cada trozo lleva sus palabras y el segundo de cada una."""
    palabras = frase["texto"].split()
    if not palabras:
        return []
    grupos, actual = [], []
    for p in palabras:
        actual.append(p)
        corte = p.endswith((",", ";", ":")) or (len(actual) >= MAX_TROZO)
        if corte and len(actual) >= 3:
            grupos.append(actual)
            actual = []
    if actual:
        if grupos and len(actual) < 3:
            grupos[-1] += actual
        else:
            grupos.append(actual)
    # El tiempo se reparte por caracteres (más un poco por palabra: las pausas cortas).
    pesos = [len(p) + 2 for p in palabras]
    total = sum(pesos)
    t, salida, k = frase["inicio"], [], 0
    for g in grupos:
        tiempos = []
        for _ in g:
            tiempos.append(round(t, 3))
            t += frase["duracion"] * pesos[k] / total
            k += 1
        salida.append({"palabras": g, "tiempos": tiempos, "inicio": tiempos[0], "fin": round(t, 3)})
    return salida


# ── Reglas (sin IA) ──────────────────────────────────────────────────────────

def _ventana(palabras: list[str]) -> tuple[int, int]:
    """La ventana de hasta MAX_PANTALLA palabras con más contenido (sin empezar ni terminar en palabra vacía)."""
    n = len(palabras)
    if n <= MAX_PANTALLA:
        i, j = 0, n
    else:
        mejor, i, j = -1, 0, MAX_PANTALLA
        for a in range(n):
            for b in range(a + 2, min(n, a + MAX_PANTALLA) + 1):
                v = palabras[a:b]
                puntos = sum(len(_plano(x)) + 6 * bool(_CIFRA.search(x)) for x in v if _contenido(x)) - 2 * len(v)
                if puntos > mejor:
                    mejor, i, j = puntos, a, b
    while i < j - 1 and not _contenido(palabras[i]) and not palabras[i].startswith(("¿", "¡")):
        i += 1
    while j > i + 1 and not _contenido(palabras[j - 1]) and not _CIFRA.search(palabras[j - 2]):
        j -= 1  # sin cortar la unidad de una cifra («1–3 h», «30 %»)
    if j < n and _CIFRA.search(palabras[j - 1]) and len(_plano(palabras[j])) <= 3 and j - i < MAX_PANTALLA:
        j += 1
    return _con_negacion(palabras, i), j


def _resaltar(palabras: list[str]) -> list[int]:
    """La cifra si hay una; si no, la última palabra con contenido (como «A TUS **MANOS**»)."""
    cifras = [i for i, p in enumerate(palabras) if _CIFRA.search(p)]
    if cifras:
        return cifras[:2]
    con = [i for i, p in enumerate(palabras) if _contenido(p)]
    return [con[-1]] if con else [len(palabras) - 1]


def _estilo(palabras: list[str]) -> str:
    if any(_CIFRA.search(p) for p in palabras) and len(palabras) <= 4:
        return "cifra"
    if len(palabras) <= 2 and sum(len(p) for p in palabras) <= 16:
        return "termino"
    return "cajas"


def _etiqueta(titulo: str) -> str | None:
    """El rótulo de la lámina: las primeras palabras con contenido de su título (máximo 3)."""
    con = [_limpia(p).strip("¿?¡!") for p in titulo.split() if _contenido(p)]
    return " ".join(x for x in con[:3] if x).upper()[:28] or None


# ── Tomas ────────────────────────────────────────────────────────────────────

def _palabras_de(item: dict) -> set[str]:
    texto = " ".join([item.get("descripcion") or "", *item.get("etiquetas", [])])
    return {_raiz(p) for p in texto.split() if _contenido(p)}


class Tomas:
    """Elige el fondo de cada momento sin repetir la misma toma seguida, y avanza dentro de cada clip."""

    def __init__(self, items: list[dict], marca: str):
        self.items = {x["id"]: x for x in items}
        self.marca = marca
        self.claves = {x["id"]: _palabras_de(x) for x in items}
        self.generales = [x["id"] for x in items if "general" in x.get("etiquetas", [])]
        self.anterior: str | None = None
        self.usos: dict[str, float] = {}
        self.turno = 0

    def catalogo(self) -> list[dict]:
        return [{"id": i, "tipo": x["tipo"], "descripcion": x.get("descripcion") or "",
                 "etiquetas": x.get("etiquetas", [])} for i, x in self.items.items()]

    def por_reglas(self, texto: str) -> str | None:
        """La toma del banco que comparte más palabras con lo que se dice; si ninguna, una «general»."""
        buscadas = {_raiz(p) for p in texto.split() if _contenido(p)}
        puntaje = {i: len(buscadas & c) for i, c in self.claves.items()}
        candidatas = sorted((i for i, v in puntaje.items() if v > 0), key=lambda i: (-puntaje[i], i == self.anterior))
        if candidatas:
            return candidatas[0]
        if self.generales:
            libres = [g for g in self.generales if g != self.anterior] or self.generales
            self.turno += 1
            return libres[self.turno % len(libres)]
        return None

    def toma(self, id_: str | None, duracion: float, imagen_lamina: str | None) -> videospec.Toma:
        if id_ in self.items:
            x = self.items[id_]
            archivo = banco.ruta(self.marca, x["archivo"])
            if archivo is not None:
                desde = 0.0
                if x["tipo"] == "clip":
                    largo = x.get("duracion") or 0
                    desde = self.usos.get(id_, 0.0)
                    if desde + duracion > largo:
                        desde = 0.0
                    self.usos[id_] = desde + duracion
                self.anterior = id_
                return videospec.Toma(tipo=x["tipo"], archivo=str(archivo), desde=round(desde, 3), id=id_)
        self.anterior = None
        if imagen_lamina and id_ != "marca":
            return videospec.Toma(tipo="lamina", archivo=imagen_lamina)
        return videospec.Toma(tipo="marca")


# ── IA ───────────────────────────────────────────────────────────────────────

SISTEMA = ("Eres el director de un estudio de video que convierte presentaciones en videos cortos de formación, "
           "con texto cinético al estilo de los reels: frases de 2 a 5 palabras en cajas, una palabra resaltada. "
           "Trabajas en español de Colombia. Nunca inventes: el texto en pantalla usa solo palabras que la voz dice "
           "en ese momento, en el mismo orden. Responde solo con el JSON pedido.")

ESQUEMA = {
    "type": "object",
    "properties": {"momentos": {"type": "array", "items": {
        "type": "object",
        "properties": {"n": {"type": "integer"}, "texto": {"type": "string"},
                       "resaltado": {"type": "array", "items": {"type": "string"}},
                       "etiqueta": {"type": "string"}, "toma": {"type": "string"}},
        "required": ["n", "texto", "resaltado", "etiqueta", "toma"]}}},
    "required": ["momentos"],
}


def _pedido(titulo: str, lista: list[dict], catalogo: list[dict], imagen: bool) -> str:
    tomas = "\n".join(f'- "{c["id"]}" ({c["tipo"]}): {c["descripcion"]} [{", ".join(c["etiquetas"])}]' for c in catalogo)
    extra = ['- "lamina": la imagen de la diapositiva'] if imagen else []
    return (f"Lámina: «{titulo}».\n\nMomentos (lo que dice la voz en cada uno):\n"
            + "\n".join(f'{x["n"]}. {" ".join(x["palabras"])}' for x in lista)
            + "\n\nPara cada momento decide:\n"
            f"- texto: de 1 a {MAX_PANTALLA} palabras seguidas de ese momento, las que mejor cuentan la idea "
            "(como «DE LA PANTALLA A TUS MANOS», «LISTO PARA IMPRIMIR», «CAPA POR CAPA»).\n"
            "- resaltado: 1 o 2 palabras del texto, las más importantes.\n"
            "- etiqueta: de 1 a 3 palabras sobre el tema de la lámina (como «MODELADO 3D», «RESULTADO»).\n"
            "- toma: el id del fondo que mejor muestra lo que se dice. No repitas la misma toma en dos momentos "
            "seguidos si hay otra que sirva.\n\nTomas disponibles:\n" + "\n".join([*extra, *tomas.splitlines(),
                                                                                    '- "marca": fondo animado de la marca']))


def _con_ia(r: dict | None, lista: list[dict], validas: set[str]) -> dict[int, dict]:
    """Lo que la IA decidió y pasa las guardas, por número de momento."""
    salida = {}
    for m in (r or {}).get("momentos", []) if isinstance(r, dict) else []:
        x = next((x for x in lista if x["n"] == m.get("n")), None)
        if x is None:
            continue
        pantalla = [_limpia(p) for p in str(m.get("texto", "")).split() if _limpia(p)]
        origen = [_plano(_limpia(p)) for p in x["palabras"]]
        # Las palabras tienen que estar en el trozo, seguidas y en orden: así no hay nada inventado.
        planas = [_plano(p) for p in pantalla]
        inicio = next((i for i in range(len(origen) - len(planas) + 1) if origen[i:i + len(planas)] == planas), None)
        if not pantalla or len(pantalla) > MAX_PANTALLA or inicio is None:
            continue
        desde = _con_negacion(x["palabras"], inicio)  # la IA tampoco puede dejar fuera un «no»
        if inicio - desde + len(planas) > MAX_PANTALLA + 1:
            continue
        resaltado = [i for i, p in enumerate(planas) if p in {_plano(_limpia(w)) for w in m.get("resaltado") or []}][:2]
        etiqueta = " ".join(str(m.get("etiqueta") or "").split()[:3]).upper().strip("¿?¡!")[:28] or None
        resaltado = [r + inicio - desde for r in resaltado]
        salida[x["n"]] = {"desde": desde, "hasta": inicio + len(planas), "resaltado": resaltado or None,
                          "etiqueta": etiqueta, "toma": m.get("toma") if m.get("toma") in validas else None}
    return salida


# ── El director ──────────────────────────────────────────────────────────────

def _huella(spec: videospec.VideoSpec, items: list[dict], con_ia: bool, modelo: str | None) -> str:
    base = [VERSION, con_ia, modelo, spec.video.formato, items,
            [(e.vista.get("titulo"), e.vista.get("imagen"), [(f.texto, f.inicio, f.duracion) for f in e.narracion])
             for e in spec.escenas]]
    return hashlib.sha256(json.dumps(base, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:24]


def dirigir(spec: videospec.VideoSpec, t: dict, ctx=None, avisar=lambda paso, x: None,
            cache: Path | None = None) -> videospec.VideoSpec:
    """El VideoSpec resuelto, con los momentos de cada escena. `ctx`: el Contexto de la IA (None = reglas)."""
    items = banco.listar(t["marca"]) if t.get("marca") else []
    con_ia = bool(ctx and ctx.con_ia)
    archivo = cache / f"{_huella(spec, items, con_ia, ctx.modelo if ctx else None)}.json" if cache else None
    if archivo is not None and archivo.exists():
        guardado = json.loads(archivo.read_text(encoding="utf-8"))
        d = spec.model_dump()
        for e, beats in zip(d["escenas"], guardado):
            e["beats"] = beats
        return videospec.validar(d)

    tomas = Tomas(items, t.get("marca") or "")
    d = spec.model_dump()
    usadas_ia = 0
    for k, e in enumerate(d["escenas"]):
        avisar(f"Dirigiendo la lámina {e['lamina']}", k / max(1, len(d["escenas"])))
        lista, n = [], 0
        for f in e["narracion"]:
            for x in trozos({**f, "inicio": f["inicio"] - e["inicio"]}):
                n += 1
                lista.append({**x, "n": n})
        if not lista:
            e["beats"] = []
            continue
        imagen = e["vista"].get("imagen")
        validas = set(tomas.items) | {"marca"} | ({"lamina"} if imagen else set())
        decidido = {}
        if con_ia:
            r = ctx.chat(SISTEMA, _pedido(e["vista"].get("titulo") or "", lista, tomas.catalogo(), bool(imagen)), ESQUEMA)
            decidido = _con_ia(r, lista, validas)
            usadas_ia += bool(decidido)
        etiqueta_lamina = _etiqueta(e["vista"].get("titulo") or "")
        beats = []
        for x in lista:
            m = decidido.get(x["n"]) or {}
            palabras = [_limpia(p) or p for p in x["palabras"]]
            i, j = (m["desde"], m["hasta"]) if m else _ventana(palabras)
            pantalla = palabras[i:j]
            id_toma = m.get("toma") if m else tomas.por_reglas(" ".join(x["palabras"]) + " " + (e["vista"].get("titulo") or ""))
            if id_toma == "lamina":
                id_toma = None
            beats.append({
                "inicio": x["inicio"], "fin": x["fin"], "texto": " ".join(pantalla),
                "resaltado": m.get("resaltado") or _resaltar(pantalla),
                "etiqueta": m.get("etiqueta") or etiqueta_lamina, "estilo": _estilo(pantalla),
                "palabras": x["tiempos"][i:j], "_toma": id_toma,
            })
        beats = _unir_cortos(beats)
        # Cada momento dura hasta que empieza el siguiente; el último, hasta el final de la escena.
        largo = e["cuadros"] / d["video"]["fps"]
        for b, siguiente in zip(beats, beats[1:] + [None]):
            b["fin"] = round(siguiente["inicio"] if siguiente else largo, 3)
        beats[0]["inicio"] = 0.0
        for b in beats:
            b["toma"] = tomas.toma(b.pop("_toma"), b["fin"] - b["inicio"], imagen).model_dump()
        e["beats"] = beats
    if archivo is not None:
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(json.dumps([e["beats"] for e in d["escenas"]], ensure_ascii=False), encoding="utf-8")
    d.setdefault("avisos", [])
    if con_ia and not usadas_ia:
        d["avisos"].append("La IA no respondió bien: el texto en pantalla se armó con reglas")
    return videospec.validar(d)


def _unir_cortos(beats: list[dict]) -> list[dict]:
    """Un momento de menos de MIN_MOMENTO segundos se suma al anterior (si cabe en pantalla)."""
    salida = []
    for b in beats:
        if salida and b["inicio"] - salida[-1]["inicio"] < MIN_MOMENTO:
            a = salida[-1]
            juntas = a["texto"].split() + b["texto"].split()
            if len(juntas) <= MAX_PANTALLA:
                corrido = len(a["texto"].split())
                a.update(texto=" ".join(juntas), palabras=a["palabras"] + b["palabras"],
                         resaltado=a["resaltado"] + [corrido + r for r in b["resaltado"]][:1],
                         estilo=_estilo(juntas), fin=b["fin"])
                continue
        salida.append(b)
    return salida


def para_produccion(spec: videospec.VideoSpec, t: dict, cache: Path, avisar=lambda paso, x: None) -> videospec.VideoSpec:
    """La etapa de producción: dirige con la IA configurada (o reglas) y libera el modelo al terminar."""
    from motor.agentes import base
    ctx = base.contexto("texto", avisar, tiempo=180)
    try:
        return dirigir(spec, t, ctx, avisar, cache)
    finally:
        if ctx.usadas:
            ctx.llm.liberar(ctx.modelo)


def carpeta_cache(t: dict) -> Path:
    return taller.ruta_trabajo(t["id"]).parent / "cache" / "direccion"
