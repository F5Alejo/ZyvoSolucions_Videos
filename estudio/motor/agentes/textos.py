"""Agentes del guion: Redactor de pantalla, Guionista y Verificador normativo."""

import re

from app import datos, extractor, taller
from motor import escenas
from motor.agentes.base import Agente, Contexto, en_videos, registrar, texto_de
from motor.agentes.guardas import inventado

SISTEMA = ("Trabajas en un estudio que convierte presentaciones en videos de formación en español de Colombia. "
           "Nunca inventes datos, cifras, normas ni nombres: usa solo lo que está en el texto que se te da. "
           "Responde solo con el JSON pedido.")


def _palabras(texto: str, maximo: int) -> str:
    """Recorta a `maximo` palabras, sin dejar signos colgando."""
    p = texto.split()
    return texto.strip() if len(p) <= maximo else " ".join(p[:maximo]).rstrip(",;:-") + "…"


def _primera_idea(parrafo: str) -> str:
    """La primera idea de un párrafo: hasta el primer punto, dos puntos o punto y coma."""
    return re.split(r"(?<=[\.:;])\s", parrafo.strip(), maxsplit=1)[0].rstrip(".:;")


# ── Redactor de pantalla ─────────────────────────────────────────────────────

ESQUEMA_PANTALLA = {
    "type": "object",
    "properties": {"titulo": {"type": "string"},
                   "vinetas": {"type": "array", "items": {"type": "string"}, "minItems": 0, "maxItems": 4}},
    "required": ["titulo", "vinetas"],
}


def _redactor(t: dict, ctx: Contexto) -> list[dict]:
    salida = []
    lista = en_videos(t)
    for k, (video, l, i) in enumerate(lista):
        ctx.avisar(f"Lámina {l['n']} ({k + 1} de {len(lista)})", k / len(lista))
        v = escenas.vista(l, i, len(video["laminas"]), video["titulo"], None, t["nombre"])
        antes = {"titulo": v["titulo"], "vinetas": v["vinetas"]}
        parrafos = [p for ps in l.get("formas", {}).values() for p in ps]
        r = ctx.chat(SISTEMA + " Escribes el texto que se ve en pantalla: corto, claro y fácil de leer en 3 segundos.",
                     f"Reescribe el título (máximo 8 palabras) y de 2 a 4 viñetas (máximo 10 palabras cada una) "
                     f"para esta lámina. Si la lámina es una portada, puede quedar sin viñetas.\n\n"
                     f"Título actual: {antes['titulo']}\nTexto de la lámina:\n" + "\n".join(f"- {p}" for p in parrafos)
                     + f"\n\nLo que dice la voz: {l['notas'][:1200]}", ESQUEMA_PANTALLA)
        con_ia = r is not None
        if r is None:  # reglas: recortar lo que hay
            r = {"titulo": _palabras(antes["titulo"], 8),
                 "vinetas": [_palabras(_primera_idea(x), 10) for x in antes["vinetas"]][:4]}
        despues = {"titulo": _palabras(r["titulo"].strip(), 10),
                   "vinetas": [_palabras(x.strip(), 12) for x in r["vinetas"] if x.strip()][:4]}
        if v["tipo"] != "portada" and not despues["vinetas"]:
            despues["vinetas"] = antes["vinetas"][:4]
        if despues == antes or inventado(" ".join([despues["titulo"], *despues["vinetas"]]), texto_de(l)):
            continue
        salida.append({"lamina": l["n"], "video": video["clave"], "titulo": f"Lámina {l['n']}: texto en pantalla",
                       "antes": antes, "despues": despues, "con_ia": con_ia,
                       "razon": "Texto más corto para leer mientras habla la voz" if con_ia else "Recortado por reglas (sin IA)"})
    return salida


def _aplicar_pantalla(t: dict, p: dict) -> None:
    taller.editar_lamina(t, p["lamina"], {"titulo": p["despues"]["titulo"], "vinetas": p["despues"]["vinetas"]})


registrar(Agente("redactor", "Redactor de pantalla", "Títulos y viñetas cortas a partir de los párrafos del PPTX",
                 "guion", "texto", _redactor, _aplicar_pantalla))


# ── Guionista ────────────────────────────────────────────────────────────────

ESQUEMA_GUION = {"type": "object", "properties": {"narracion": {"type": "string"}}, "required": ["narracion"]}


def _guionista(t: dict, ctx: Contexto) -> list[dict]:
    salida = []
    r_curso = taller.resumen(t)
    largos = {v["clave"] for v in r_curso["videos"] if v["segundos"] > 240}
    lista = en_videos(t)
    for k, (video, l, i) in enumerate(lista):
        ctx.avisar(f"Lámina {l['n']} ({k + 1} de {len(lista)})", k / len(lista))
        parrafos = [p for ps in l.get("formas", {}).values() for p in ps]
        if not l["notas"].strip():
            r = ctx.chat(SISTEMA + " Escribes guiones para voz en off: frases cortas, tono cercano y claro.",
                         "Esta lámina no tiene narración. Escribe lo que dirá la voz (de 2 a 4 frases, máximo 70 "
                         "palabras) usando solo lo que muestra la lámina:\n" + "\n".join(f"- {p}" for p in parrafos),
                         ESQUEMA_GUION)
            con_ia = r is not None
            narracion = r["narracion"].strip() if r else ". ".join(x.rstrip(".") for x in parrafos if x.strip()) + "."
            razon = "La lámina no tenía narración: se vería sin voz"
        elif video["clave"] in largos and len(l["notas"].split()) > 90:
            r = ctx.chat(SISTEMA + " Editas guiones para voz en off.",
                         "Acorta esta narración un 30 % sin perder ninguna idea, cifra ni norma. Mantén el tono:\n\n"
                         + l["notas"], ESQUEMA_GUION)
            if r is None:
                continue  # acortar bien necesita IA
            con_ia, narracion = True, r["narracion"].strip()
            razon = f"El video «{video['titulo']}» pasa de 4 minutos"
        else:
            continue
        if not narracion.strip(". ") or narracion == l["notas"] or inventado(narracion, texto_de(l)):
            continue
        salida.append({"lamina": l["n"], "video": video["clave"], "titulo": f"Lámina {l['n']}: narración",
                       "antes": {"notas": l["notas"]}, "despues": {"notas": narracion}, "con_ia": con_ia, "razon": razon})
    return salida


def _aplicar_guion(t: dict, p: dict) -> None:
    taller.editar_lamina(t, p["lamina"], {"notas": p["despues"]["notas"]})


registrar(Agente("guionista", "Guionista", "Narración para láminas sin notas y para acortar videos muy largos",
                 "guion", "texto", _guionista, _aplicar_guion))


# ── Verificador normativo ────────────────────────────────────────────────────

def _tipo_cita(c: str) -> str:
    if re.match(r"(?i)(ley|decreto|resoluci|circular|art)", c):
        return "Norma"
    if "%" in c:
        return "Porcentaje"
    if "$" in c or "SMMLV" in c.upper():
        return "Dinero"
    return "Umbral o medida"


def _verificador(t: dict, ctx: Contexto) -> list[dict]:
    marca = datos.marcas().get(t["marca"], {})
    abiertos = [x["texto"] for x in marca.get("pendientes", []) + marca.get("pedir_al_cliente", []) if not x["hecho"]]
    revisadas = t.get("verificadas") or {}
    salida = []
    for video, l, _ in en_videos(t):
        for cita in extractor.afirmaciones_normativas(l["notas"]):
            clave = f"{l['n']}|{cita}"
            if clave in revisadas:
                continue
            palabras = {w for w in re.findall(r"[a-záéíóúñ]{5,}", cita.lower())} | set(re.findall(r"\d+", cita))
            choques = [x for x in abiertos if palabras & ({w for w in re.findall(r"[a-záéíóúñ]{5,}", x.lower())}
                                                          | set(re.findall(r"\d+", x)))]
            tipo = _tipo_cita(cita)
            salida.append({
                "lamina": l["n"], "video": video["clave"], "titulo": f"Lámina {l['n']}: «{cita}»",
                "antes": None, "despues": {"cita": cita, "tipo": tipo, "clave": clave,
                                           "pregunta": f"¿De qué documento sale «{cita}»? Anota la fuente antes de publicar."},
                "razon": ("⚠ Choca con un pendiente de la marca: " + "; ".join(choques)) if choques
                         else f"{tipo}: en formación normativa toda cifra necesita su fuente",
            })
    return salida


def _aplicar_verificada(t: dict, p: dict) -> None:
    from datetime import date
    t.setdefault("verificadas", {})[p["despues"]["clave"]] = date.today().isoformat()


registrar(Agente("verificador", "Verificador normativo", "Cada cifra y norma del guion, con la pregunta por su fuente",
                 "guion", None, _verificador, _aplicar_verificada))
