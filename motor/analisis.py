"""Agente 1, el Analizador: qué trae la presentación, antes de hacer nada con ella.

Solo lee: no cambia el curso. Es determinista (no usa IA): cuenta, clasifica y avisa. Su
resultado, `PresentationAnalysis`, se guarda en `datos/trabajos/<id>/analisis.json` y la interfaz
lo muestra al terminar de subir el PPTX («Ya entendimos tu presentación»).
"""

import json
import re
import unicodedata
from collections import Counter
from datetime import datetime

from app import extractor, taller

VERSION = 1

# Palabras que no dicen de qué trata la presentación.
_VACIAS = set("""a al algo ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre
era es esa ese eso esta este esto estos estas fue hay la las le les lo los mas más me mi muy no nos o otra otro para
pero por que qué se sea ser si sí sin sobre su sus también te tiene tu un una uno unos unas y ya yo lámina parte módulo
introducción conclusión cierre preguntas gracias the and of to in""".split())


def _plano(palabra: str) -> str:
    return unicodedata.normalize("NFKD", palabra.lower()).encode("ascii", "ignore").decode()


def _tema(laminas: list[dict]) -> list[str]:
    """Las palabras que más se repiten en títulos y texto (las de los títulos pesan el doble)."""
    cuenta: Counter = Counter()
    for l in laminas:
        titulo = extractor.titulo_lamina(l)
        texto = " ".join(p for ps in l.get("formas", {}).values() for p in ps)
        for peso, fuente in ((2, titulo), (1, texto)):
            for p in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{4,}", fuente):
                if _plano(p) not in {_plano(x) for x in _VACIAS}:
                    cuenta[p.lower()] += peso
    return [p for p, _ in cuenta.most_common(6)]


def _dificultad(laminas: list[dict]) -> str:
    """Básica, media o avanzada, por el largo de las frases y de las palabras de la narración."""
    frases = [f for l in laminas for f in l.get("frases", [])]
    palabras = [p for f in frases for p in f.split()]
    if not palabras:
        return "sin narración"
    por_frase = len(palabras) / max(1, len(frases))
    largas = sum(len(p) >= 10 for p in palabras) / len(palabras)
    citas = sum(len(extractor.afirmaciones_normativas(l.get("notas", ""))) for l in laminas)
    puntos = (por_frase > 22) + (largas > 0.12) + (citas > len(laminas))
    return ("básica", "media", "avanzada", "avanzada")[puntos]


def analizar(t: dict) -> dict:
    laminas = taller.laminas_efectivas(t)
    sin_notas = [l["n"] for l in laminas if not l["notas"].strip()]
    con_imagen = [l["n"] for l in laminas if l.get("foto")]
    con_tabla = [l["n"] for l in laminas if l.get("tablas")]
    con_grafico = [l["n"] for l in laminas if l.get("graficos")]
    vacias = [l["n"] for l in laminas if not l.get("formas") and not l["notas"].strip() and not l.get("foto")
              and not l.get("tablas") and not l.get("graficos")]
    largas = [l["n"] for l in laminas if sum(len(p.split()) for ps in l.get("formas", {}).values() for p in ps) > 80]
    importantes = [{"lamina": l["n"], "cita": c} for l in laminas for c in extractor.afirmaciones_normativas(l["notas"])]
    r = taller.resumen(t)
    avisos = []
    if sin_notas:
        avisos.append(f"{len(sin_notas)} láminas sin notas del orador: la voz no tendrá qué decir en ellas")
    if vacias:
        avisos.append(f"Láminas vacías: {', '.join(map(str, vacias))}")
    if largas:
        avisos.append(f"Láminas con mucho texto para leer en pantalla: {', '.join(map(str, largas))}")
    return {
        "version": VERSION,
        "creado": datetime.now().isoformat(timespec="seconds"),
        "laminas": len(laminas),
        "titulos": [{"lamina": l["n"], "titulo": extractor.titulo_lamina(l), "seccion": extractor.seccion_lamina(l)}
                    for l in laminas],
        "con_notas": len(laminas) - len(sin_notas),
        "sin_notas": sin_notas,
        "imagenes": con_imagen,
        "tablas": con_tabla,
        "graficos": con_grafico,
        "vacias": vacias,
        "texto_largo": largas,
        "palabras": r["palabras"],
        "minutos": round(r["segundos"] / 60, 1),
        "videos": len(r["videos"]),
        "estructura": "por secciones" if any(extractor.seccion_lamina(l) for l in laminas) else "por duración",
        "tema": _tema(laminas),
        "dificultad": _dificultad(laminas),
        "puntos_importantes": importantes[:30],
        "avisos": avisos,
    }


def ruta(t: dict):
    return taller.ruta_trabajo(t["id"]).parent / "analisis.json"


def guardar(t: dict) -> dict:
    a = analizar(t)
    ruta(t).write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    return a


def leer(t: dict) -> dict:
    """El análisis guardado o, si el curso es de antes de que existiera, uno nuevo."""
    archivo = ruta(t)
    if archivo.exists():
        return json.loads(archivo.read_text(encoding="utf-8"))
    return guardar(t)
