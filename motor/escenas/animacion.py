"""Plantillas de animación: entradas y salidas de cada elemento de la escena.

Una plantilla dice, por elemento (título, viñetas, imagen…), qué efecto usa al entrar y al
salir, cuánto dura, con qué retardo y curva, y cuánto se escalona entre viñetas. Las de
fábrica están en `datos/animaciones/`; las que guarda la persona, en `datos/animaciones/propias/`.

La animación de una lámina se arma por capas, de menos a más específica:

    plantilla del curso  →  ajustes del curso  →  ajustes de esa lámina (puede cambiar de plantilla)

Cada capa trae solo lo que cambia. Todo se valida contra el catálogo de `efectos.py`.
"""

import copy
import json
import re

from app import datos
from motor.escenas import efectos

PORCION = ("efecto", "duracion", "retardo", "curva", "escalonado")


class AnimacionInvalida(ValueError):
    pass


def _carpeta():
    return datos.RAIZ_DATOS / "animaciones"


def plantillas() -> dict[str, dict]:
    """Todas las plantillas: primero las de fábrica, luego las propias."""
    salida = {}
    for sub, propia in ((_carpeta(), False), (_carpeta() / "propias", True)):
        if sub.exists():
            for f in sorted(sub.glob("*.json")):
                p = json.loads(f.read_text(encoding="utf-8"))
                salida[p["id"]] = {**p, "propia": propia}
    return salida


def _paso(elemento: str, fase: str, d: dict, completo: bool) -> dict:
    """Valida una entrada o salida. Con `completo` exige todas las claves (plantillas)."""
    if not isinstance(d, dict):
        raise AnimacionInvalida(f"{elemento}.{fase} tiene que ser un objeto")
    limpio = {}
    for k, v in d.items():
        if k not in PORCION:
            raise AnimacionInvalida(f"{elemento}.{fase}: «{k}» no es un ajuste de animación")
        if k == "efecto":
            if v not in efectos.ELEMENTOS[elemento][fase]:
                raise AnimacionInvalida(f"{elemento}.{fase}: el efecto «{v}» no está permitido aquí")
        elif k == "curva":
            if v not in efectos.CURVAS:
                raise AnimacionInvalida(f"{elemento}.{fase}: la curva «{v}» no existe")
        else:
            minimo, maximo = efectos.LIMITES[k]
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not minimo <= v <= maximo:
                raise AnimacionInvalida(f"{elemento}.{fase}.{k} tiene que estar entre {minimo:g} y {maximo:g} s")
            v = round(float(v), 3)
        limpio[k] = v
    if completo:
        faltan = [k for k in ("efecto", "duracion", "retardo", "curva") if k not in limpio]
        if faltan:
            raise AnimacionInvalida(f"{elemento}.{fase}: faltan {', '.join(faltan)}")
        limpio.setdefault("escalonado", 0.0)
    return limpio


def validar_elementos(elementos: dict, completo: bool = False) -> dict:
    if not isinstance(elementos, dict):
        raise AnimacionInvalida("«elementos» tiene que ser un objeto")
    limpio = {}
    for el, fases in elementos.items():
        if el not in efectos.ELEMENTOS:
            raise AnimacionInvalida(f"«{el}» no es un elemento de la escena")
        limpio[el] = {f: _paso(el, f, v, completo) for f, v in fases.items() if f in ("entrada", "salida")}
    if completo:
        faltan = [el for el in efectos.ELEMENTOS if el not in limpio or set(limpio[el]) != {"entrada", "salida"}]
        if faltan:
            raise AnimacionInvalida(f"La plantilla no define entrada y salida de: {', '.join(faltan)}")
    return limpio


def validar_plantilla(p: dict) -> dict:
    nombre = str(p.get("nombre", "")).strip()
    if not nombre:
        raise AnimacionInvalida("La plantilla necesita un nombre")
    return {"id": p.get("id") or "", "nombre": nombre[:60], "descripcion": str(p.get("descripcion", ""))[:240],
            "elementos": validar_elementos(p.get("elementos", {}), completo=True)}


def guardar_propia(p: dict) -> dict:
    """Guarda una plantilla nueva en `propias/` con un id que no choca con ninguna otra."""
    limpia = validar_plantilla(p)
    base = re.sub(r"[^a-z0-9]+", "-", limpia["nombre"].lower()).strip("-")[:40] or "plantilla"
    existentes = plantillas()
    id_, i = f"propia-{base}", 2
    while id_ in existentes:
        id_, i = f"propia-{base}-{i}", i + 1
    limpia["id"] = id_
    carpeta = _carpeta() / "propias"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{id_}.json").write_text(json.dumps(limpia, ensure_ascii=False, indent=1), encoding="utf-8")
    return {**limpia, "propia": True}


def borrar_propia(id_: str) -> None:
    p = plantillas().get(id_)
    if p is None or not p["propia"]:
        raise AnimacionInvalida("Solo se pueden borrar las plantillas propias")
    (_carpeta() / "propias" / f"{id_}.json").unlink()


# ── La animación de un curso ─────────────────────────────────────────────────

def validar_curso(a: dict | None) -> dict:
    """`trabajo["animacion"]`: {plantilla, ajustes: {elemento: {entrada, salida}}, laminas: {"n": {plantilla?, ajustes?}}}."""
    a = a or {}
    todas = plantillas()
    if a.get("plantilla") is not None and a["plantilla"] not in todas:
        raise AnimacionInvalida(f"La plantilla «{a['plantilla']}» no existe")
    laminas = {}
    for n, x in (a.get("laminas") or {}).items():
        if not str(n).isdigit():
            raise AnimacionInvalida(f"«{n}» no es un número de lámina")
        x = x or {}
        if x.get("plantilla") is not None and x["plantilla"] not in todas:
            raise AnimacionInvalida(f"Lámina {n}: la plantilla «{x['plantilla']}» no existe")
        entrada = {"plantilla": x.get("plantilla"), "ajustes": validar_elementos(x.get("ajustes") or {})}
        if entrada["plantilla"] or entrada["ajustes"]:
            laminas[str(n)] = entrada
    return {"plantilla": a.get("plantilla"), "ajustes": validar_elementos(a.get("ajustes") or {}), "laminas": laminas}


def _mezclar(base: dict, ajustes: dict) -> dict:
    salida = copy.deepcopy(base)
    for el, fases in (ajustes or {}).items():
        for fase, valores in fases.items():
            salida[el][fase].update(valores)
    return salida


def plan(t: dict, n: int) -> dict:
    """La animación ya resuelta de la lámina `n` del curso: {"plantilla": id, "elementos": {...}}."""
    from app import configuracion

    todas = plantillas()
    a = t.get("animacion") or {}
    propia = (a.get("laminas") or {}).get(str(n)) or {}
    id_ = propia.get("plantilla") or a.get("plantilla") or configuracion.leer()["cursos"]["animacion"]
    if id_ not in todas:
        id_ = "dinamica" if "dinamica" in todas else next(iter(todas))
    elementos = todas[id_]["elementos"]
    if not propia.get("plantilla"):  # los ajustes del curso valen para su plantilla
        elementos = _mezclar(elementos, a.get("ajustes"))
    return {"plantilla": id_, "elementos": _mezclar(elementos, propia.get("ajustes"))}


# ── Tiempos y CSS ────────────────────────────────────────────────────────────

def _cuantos(el: str, v: dict) -> int:
    """Cuántos trozos se escalonan: viñetas, o palabras/letras del título."""
    if el == "vinetas":
        return max(1, len(v.get("vinetas", [])))
    return 1


def _activo(el: str, fase: str, v: dict) -> bool:
    """Si el elemento existe en esta escena y le toca animarse (fondo y logo: solo al abrir y cerrar el video)."""
    existe = {"antetitulo": v["tipo"] == "portada" and bool(v.get("antetitulo")), "linea": bool(v.get("vinetas")),
              "vinetas": bool(v.get("vinetas")), "imagen": bool(v.get("imagen")) and v["tipo"] != "portada"}.get(el, True)
    if not existe:
        return False
    if el in efectos.CONTINUOS:
        return v["indice"] == 0 if fase == "entrada" else v["indice"] == v["total"] - 1
    return True


def trozos(texto: str, efecto: str) -> list[str] | None:
    """Palabras (con su espacio) o letras, para los efectos que animan trozo por trozo."""
    if efecto == "palabra-por-palabra":
        return re.findall(r"\S+\s*", texto)
    if efecto == "maquina":
        return list(texto)
    return None


def duraciones(p: dict, v: dict) -> tuple[float, float]:
    """(entrada, salida): cuánto tarda en entrar todo y cuánto antes del final empieza a salir."""
    entrada = salida = 0.0
    for el, fases in p["elementos"].items():
        ent, sal = fases["entrada"], fases["salida"]
        if ent["efecto"] != "ninguno" and _activo(el, "entrada", v):
            n = _cuantos(el, v)
            partes = None
            if el in ("titulo", "antetitulo"):
                partes = trozos(v.get("titulo" if el == "titulo" else "antetitulo", ""), ent["efecto"])
            if partes:
                n = len(partes)
            paso = ent.get("escalonado", 0) or (0.03 if ent["efecto"] == "maquina" else 0.08 if partes else 0)
            entrada = max(entrada, ent["retardo"] + ent["duracion"] + paso * (n - 1))
        if sal["efecto"] != "ninguno" and _activo(el, "salida", v):
            n = _cuantos(el, v)
            salida = max(salida, sal["retardo"] + sal["duracion"] + sal.get("escalonado", 0) * (n - 1))
    return round(entrada, 3), round(salida, 3)


def css(p: dict, v: dict, total: float, avance_desde: float, avance_hasta: float) -> tuple[str, dict]:
    """Las reglas CSS de la escena (dura `total` segundos) y cómo partir los textos animados por trozo."""
    reglas, keyframes, partir = [], [], {}
    for el, fases in p["elementos"].items():
        sel = efectos.ELEMENTOS[el]["selector"]
        ent, sal = fases["entrada"], fases["salida"]
        n = _cuantos(el, v)
        anim_ent = ent["efecto"] != "ninguno" and _activo(el, "entrada", v)
        anim_sal = sal["efecto"] != "ninguno" and _activo(el, "salida", v)

        # Entrada
        cuerpo_ent = efectos.ENTRADA[ent["efecto"]] if anim_ent else None
        if el == "avance" and anim_ent:
            cuerpo_ent = f"from {{ width: {avance_desde:.2f}%; }} to {{ width: {avance_hasta:.2f}%; }}"
        if cuerpo_ent:
            keyframes.append(f"@keyframes ent-{el} {{ {cuerpo_ent} }}")
        # Salida: `forwards`, para que no actúe antes de su momento (la entrada es `both`).
        if anim_sal:
            keyframes.append(f"@keyframes sal-{el} {{ {efectos.SALIDA[sal['efecto']]} }}")

        curva_ent, curva_sal = efectos.CURVAS[ent["curva"]], efectos.CURVAS[sal["curva"]]
        partes = None
        if el in ("titulo", "antetitulo") and anim_ent:
            partes = trozos(v.get("titulo" if el == "titulo" else "antetitulo", ""), ent["efecto"])
        if partes:
            partir[el] = partes
            paso = ent.get("escalonado", 0) or (0.03 if ent["efecto"] == "maquina" else 0.08)
            reglas.append(f"{sel} .trozo {{ display: inline-block; white-space: pre; }}")
            for i in range(len(partes)):
                reglas.append(f"{sel} .trozo:nth-child({i + 1}) {{ animation: ent-{el} {ent['duracion']:.3f}s "
                              f"{ent['retardo'] + paso * i:.3f}s {curva_ent} both; }}")
            if anim_sal:
                reglas.append(f"{sel} {{ animation: sal-{el} {sal['duracion']:.3f}s "
                              f"{max(0.0, total - sal['duracion'] - sal['retardo']):.3f}s {curva_sal} forwards; }}")
            continue

        for i in range(n):
            anims = []
            if cuerpo_ent:
                anims.append(f"ent-{el} {ent['duracion']:.3f}s {ent['retardo'] + ent.get('escalonado', 0) * i:.3f}s {curva_ent} both")
            if anim_sal:
                # Las viñetas salen en orden: la última termina justo al final de la escena.
                adelanto = sal["retardo"] + sal.get("escalonado", 0) * (n - 1 - i)
                anims.append(f"sal-{el} {sal['duracion']:.3f}s {max(0.0, total - sal['duracion'] - adelanto):.3f}s {curva_sal} forwards")
            if anims:
                objetivo = f"{sel}:nth-child({i + 1})" if el == "vinetas" else sel
                reglas.append(f"{objetivo} {{ animation: {', '.join(anims)}; }}")
    return "\n  ".join(k for k in keyframes + reglas if k), partir
