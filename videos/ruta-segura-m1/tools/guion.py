# -*- coding: utf-8 -*-
"""Escribe GUION-VOZ.md: el libreto con los tiempos del video ya montado.

El video se entrega sin voz. Este archivo es lo que recibe quien graba en
Colombia: cada lámina trae su ventana exacta dentro del máster y las frases en
el orden en que el video las va mostrando.
"""
import io, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# mismo mapa que construir.py; si cambia una duración, cambia aquí también
LAMINAS = [(1, 0.0, 60.0), (2, 60.0, 58.5), (3, 118.5, 57.5), (4, 176.0, 65.5),
           (5, 241.5, 65.0), (6, 306.5, 59.0), (7, 365.5, 70.0), (8, 435.5, 70.5),
           (9, 506.0, 61.5), (10, 567.5, 62.0), (11, 629.5, 71.0)]

TITULOS = {1: "Portada · Ruta Segura", 2: "Pregunta inicial · cinco fallas",
           3: "Propósito · los cuatro verbos", 4: "Ruta de aprendizaje · tres módulos",
           5: "Módulo 1 · ¿ser cuidadoso basta?", 6: "Módulo 1 · Sistema Seguro",
           7: "Módulo 1 · reglas en la vía", 8: "Caso práctico · ruta inundada",
           9: "Reto RiskMann · dos decisiones", 10: "Retroalimentación · respuestas",
           11: "Repaso · tres preguntas"}

# el rótulo del PPTX no se locuta: no es texto de narración
ROTULO = re.compile(r"^GUION DE VOZ\s*[—-]\s*PRIMERA PERSONA\s*", re.I)


def tc(s):
    return "%d:%05.2f" % (int(s // 60), s % 60)


def main():
    tiempos = json.load(io.open(os.path.join(AQUI, "tiempos-medidos.json"), encoding="utf-8"))
    por_n = {o["n"]: o for o in tiempos}

    out = ["# Guion de voz · Ruta Segura · Módulo 1",
           "",
           "Video: `ruta-segura-m1` · 1920×1080 · **11:47** · **sin voz**.",
           "",
           "La animación ya está montada sobre estos tiempos: cada frase tiene su elemento",
           "en pantalla. Graba lámina por lámina respetando la ventana indicada y el montaje",
           "encaja sin reeditar el video. Si una lámina se alarga, se corrige alargando el",
           "silencio final de esa lámina, nunca corriendo las siguientes.",
           "",
           "- **Voz:** colombiana, primera persona, tono de instructor — ni locutor comercial ni lectura plana.",
           "- **Ritmo de referencia:** ~130 palabras por minuto. Los tiempos de abajo se midieron a ese ritmo.",
           "- **Silencio:** deja 0,4 s entre frases y 1 s antes de cambiar de lámina.",
           "- **Cifras y normas:** se leen completas («Ley dos mil cuatrocientos sesenta y seis de dos mil veinticinco»).",
           "",
           "| Lámina | Entra | Sale | Narración | Aire |",
           "|---|---|---|---|---|"]

    for n, ini, dur in LAMINAS:
        hab = por_n[n]["total"]
        if n in (7, 11):
            hab -= 2.30   # el rótulo que no se locuta
        out.append("| %02d · %s | %s | %s | %.1f s | %.1f s |"
                   % (n, TITULOS[n], tc(ini), tc(ini + dur), hab, dur - hab))

    out += ["", "Cierre sin voz: **%s → %s** (rótulo «Fin del módulo 1»)." % (tc(700.5), tc(707.5)),
            "", "---", ""]

    for n, ini, dur in LAMINAS:
        o = por_n[n]
        frases = [dict(f) for f in o["frases"]]
        if n in (7, 11):
            frases[0]["texto"] = ROTULO.sub("", frases[0]["texto"]).strip()
            frases[0]["dur"] = round(frases[0]["dur"] - 2.30, 2)
        out += ["## Lámina %02d · %s" % (n, TITULOS[n]),
                "",
                "**%s → %s** · narración %.1f s de %.1f s disponibles." % (tc(ini), tc(ini + dur),
                                                                           sum(f["dur"] for f in frases), dur),
                ""]
        t = 0.0
        for f in frases:
            out.append("- `+%05.1f s` %s" % (t, f["texto"]))
            t += f["dur"]
        out.append("")

    out += ["---", "",
            "## Qué queda fuera del video",
            "",
            "- No se locuta el rótulo «GUION DE VOZ — PRIMERA PERSONA» que traen las notas de las",
            "  láminas 7 y 11 en el PPTX: es una marca del documento, no narración.",
            "- Las cifras de escudos (100 / 80 / 40 / +80 / +200) y la mención a la Ley 2466 de 2025",
            "  vienen del PPTX de origen. Si el cliente las ajusta, se cambian en `tools/e04.py`,",
            "  `tools/e02.py`, `tools/e09.py` y `tools/e10.py` y se vuelve a construir.",
            ""]

    io.open(os.path.join(RAIZ, "GUION-VOZ.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("GUION-VOZ.md escrito")


if __name__ == "__main__":
    main()
