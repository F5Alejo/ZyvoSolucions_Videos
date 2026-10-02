"""Director de animación: propone plantilla y efectos por lámina, solo del catálogo.

El modelo no escribe CSS ni inventa efectos: recibe un resumen de cada lámina (tipo, cuántas
viñetas, si trae cifras o imagen) y elige de listas cerradas. Lo que no está en el catálogo se
descarta. Sin Ollama usa reglas fijas.
"""

from app import extractor
from motor import escenas
from motor.agentes.base import Agente, Contexto, en_videos, registrar
from motor.escenas import animacion, efectos

LOTE = 10  # láminas por pregunta: un modelo de 4 B responde bien con listas cortas


def _reglas(v: dict, cifras: list[str], plantilla: dict) -> tuple[dict, str]:
    ajustes, motivos = {}, []
    titulo_ent = plantilla["elementos"]["titulo"]["entrada"]["efecto"]
    if v["tipo"] == "portada" and titulo_ent not in ("palabra-por-palabra", "maquina"):
        ajustes["titulo"] = {"entrada": {"efecto": "palabra-por-palabra", "escalonado": 0.08}}
        motivos.append("portada: el título entra palabra por palabra")
    elif cifras and titulo_ent != "escalar":
        ajustes["titulo"] = {"entrada": {"efecto": "escalar", "curva": "rebote"}}
        motivos.append(f"trae una cifra ({cifras[0]}): el título entra con fuerza")
    if len(v["vinetas"]) >= 4:
        ajustes["vinetas"] = {"entrada": {"escalonado": 0.08}}
        motivos.append("muchas viñetas: llegan más seguidas")
    if v["imagen"] and v["tipo"] != "portada" and plantilla["elementos"]["imagen"]["entrada"]["efecto"] in ("ninguno", "aparecer"):
        ajustes["imagen"] = {"entrada": {"efecto": "revelar"}}
        motivos.append("tiene imagen: se revela")
    return ajustes, "; ".join(motivos)


def _director(t: dict, ctx: Contexto) -> list[dict]:
    todas = animacion.plantillas()
    lista = en_videos(t)
    fichas = []
    for video, l, i in lista:
        v = escenas.vista(l, i, len(video["laminas"]), video["titulo"], None, t["nombre"])
        v["imagen"] = bool(l.get("foto"))
        fichas.append((video, l, v, extractor.afirmaciones_normativas(" ".join([v["titulo"], *v["vinetas"], l["notas"]]))))

    ids = list(todas)
    entradas_titulo = [x for x in efectos.ELEMENTOS["titulo"]["entrada"] if x != "ninguno"]
    entradas_vinetas = [x for x in efectos.ELEMENTOS["vinetas"]["entrada"] if x != "ninguno"]
    esquema = {"type": "object", "properties": {"laminas": {"type": "array", "items": {
        "type": "object", "properties": {
            "n": {"type": "integer"}, "plantilla": {"type": "string", "enum": ids},
            "titulo_entrada": {"type": "string", "enum": entradas_titulo},
            "vinetas_entrada": {"type": "string", "enum": entradas_vinetas},
            "razon": {"type": "string"}},
        "required": ["n", "plantilla", "titulo_entrada", "vinetas_entrada", "razon"]}}}, "required": ["laminas"]}

    ia: dict[int, dict] = {}
    for k in range(0, len(fichas), LOTE):
        ctx.avisar(f"Láminas {k + 1} a {min(k + LOTE, len(fichas))} de {len(fichas)}", k / max(1, len(fichas)))
        lote = fichas[k:k + LOTE]
        descripcion = "\n".join(
            f"- Lámina {l['n']}: {v['tipo']}, título de {len(v['titulo'].split())} palabras, {len(v['vinetas'])} viñetas"
            f"{', con cifras' if c else ''}{', con imagen' if v['imagen'] else ''}"
            for _, l, v, c in lote)
        r = ctx.chat(
            "Eres director de animación de videos de formación. Eliges, para cada lámina, un estilo de animación "
            "que ayude a entender sin distraer. Solo puedes elegir de las listas dadas. Responde solo con el JSON pedido.",
            "Estilos disponibles:\n" + "\n".join(f"- {p['id']}: {p['descripcion']}" for p in todas.values())
            + f"\n\nEl curso usa hoy «{animacion.plan(t, lote[0][1]['n'])['plantilla']}». Cambia de estilo solo si "
              "la lámina lo pide (p. ej. una portada o una cifra importante). Láminas:\n" + descripcion, esquema)
        for x in (r or {}).get("laminas", []):
            ia[x["n"]] = x

    salida = []
    for video, l, v, cifras in fichas:
        actual = animacion.plan(t, l["n"])
        plantilla = todas[actual["plantilla"]]
        x = ia.get(l["n"])
        if x and x.get("plantilla") in todas:
            nueva = x["plantilla"] if x["plantilla"] != actual["plantilla"] else None
            base = todas[x["plantilla"]]["elementos"]
            ajustes = {}
            if x.get("titulo_entrada") in efectos.ELEMENTOS["titulo"]["entrada"] and x["titulo_entrada"] != base["titulo"]["entrada"]["efecto"]:
                ajustes["titulo"] = {"entrada": {"efecto": x["titulo_entrada"]}}
            if v["vinetas"] and x.get("vinetas_entrada") in efectos.ELEMENTOS["vinetas"]["entrada"] and x["vinetas_entrada"] != base["vinetas"]["entrada"]["efecto"]:
                ajustes["vinetas"] = {"entrada": {"efecto": x["vinetas_entrada"]}}
            razon, con_ia = x.get("razon", "").strip()[:200] or "Elegido por la IA", True
        else:
            nueva = None
            ajustes, razon = _reglas(v, cifras, plantilla)
            con_ia = False
        if not nueva and not ajustes:
            continue
        try:
            animacion.validar_elementos(ajustes)
        except animacion.AnimacionInvalida:
            continue
        cambios = [f"{efectos.ELEMENTOS[el]['nombre']}: "
                   + (efectos.NOMBRES[a["entrada"]["efecto"]] if "efecto" in a["entrada"] else "más seguidas")
                   for el, a in ajustes.items()]
        nombre = todas[nueva]["nombre"] if nueva else plantilla["nombre"]
        salida.append({"lamina": l["n"], "video": video["clave"], "titulo": f"Lámina {l['n']}: animación",
                       "antes": {"plantilla": actual["plantilla"]},
                       "despues": {"plantilla": nueva, "ajustes": ajustes, "resumen": " · ".join([nombre, *cambios])},
                       "razon": razon, "con_ia": con_ia})
    return salida


def _aplicar(t: dict, p: dict) -> None:
    a = animacion.validar_curso(t.get("animacion"))
    propia = a["laminas"].setdefault(str(p["lamina"]), {"plantilla": None, "ajustes": {}})
    if p["despues"]["plantilla"]:
        propia["plantilla"] = p["despues"]["plantilla"]
        propia["ajustes"] = {}
    for el, fases in p["despues"]["ajustes"].items():
        for fase, valores in fases.items():
            propia["ajustes"].setdefault(el, {}).setdefault(fase, {}).update(valores)
    t["animacion"] = animacion.validar_curso(a)


registrar(Agente("director", "Director de animación", "Elige estilo y efectos por lámina, solo del catálogo",
                 "animacion", "texto", _director, _aplicar))
