# -*- coding: utf-8 -*-
"""Escribe GUION-VOZ.md: el libreto con los tiempos del video ya montado.

Sirve para dos cosas: comprobar qué se locutó, y volver a grabar el módulo con
una persona respetando el mismo montaje. Las ventanas salen del mismo plano que
usa `tools/construir.py`, así que no pueden desincronizarse.
"""
import io, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)

import construir, cronometro

TITULOS = {1: "Portada · Ruta Segura", 2: "Pregunta inicial · cinco fallas",
           3: "Propósito · los cuatro verbos", 4: "Ruta de aprendizaje · tres módulos",
           5: "Módulo 1 · ¿ser cuidadoso basta?", 6: "Módulo 1 · Sistema Seguro",
           7: "Módulo 1 · reglas en la vía", 8: "Caso práctico · ruta inundada",
           9: "Reto RiskMann · dos decisiones", 10: "Retroalimentación · respuestas",
           11: "Repaso · tres preguntas"}


def tc(s):
    return "%d:%05.2f" % (int(s // 60), s % 60)


def main():
    escenas, total = construir.plan()
    laminas = {x["n"]: x for x in json.load(io.open(os.path.join(AQUI, "narracion.json"), encoding="utf-8"))}
    voz = cronometro.VOZ is not None

    out = ["# Guion de voz · Ruta Segura · Módulo 1",
           "",
           "Video: `ruta-segura-m1` · 1920×1080 · **%d:%02d**." % (int(total // 60), int(round(total % 60))),
           "",
           ("La locución de esta versión es sintética (ElevenLabs, modelo `eleven_v3`)."
            if voz else "Esta versión se entrega **sin voz**."),
           "",
           "El montaje está atado a estos tiempos: cada aparición en pantalla cae sobre la",
           "frase que la nombra. Para volver a grabar el módulo con una persona, respeta la",
           "ventana de cada lámina y el montaje encaja sin reeditar el video. Si una lámina",
           "se alarga, se corrige alargando su silencio final, nunca corriendo las siguientes.",
           "",
           "- **Voz:** colombiana, primera persona, tono de instructor — ni locutor comercial ni lectura plana.",
           "- **Silencio:** 0,4 s entre frases y 1 s antes de cambiar de lámina.",
           "- **Cifras:** se leen completas. En este módulo solo hay una: «Ley dos mil cuatrocientos",
           "  sesenta y seis de dos mil veinticinco».",
           "",
           "| Lámina | Entra | Sale | Narración | Aire |",
           "|---|---|---|---|---|"]

    for e in escenas:
        n = e["lamina"]
        if n is None:
            continue
        hab = cronometro.narracion(n)
        out.append("| %02d · %s | %s | %s | %.1f s | %.1f s |"
                   % (n, TITULOS[n], tc(e["inicio"]), tc(e["inicio"] + e["dura"]), hab, e["dura"] - hab))

    cierre = escenas[-1]
    out += ["", "Cierre sin voz: **%s → %s** (rótulo «Fin del módulo 1»)."
            % (tc(cierre["inicio"]), tc(cierre["inicio"] + cierre["dura"])), "", "---", ""]

    for e in escenas:
        n = e["lamina"]
        if n is None:
            continue
        frases = laminas[n]["frases"]
        ini = cronometro.VOZ[n] if voz else cronometro.REF[n]
        out += ["## Lámina %02d · %s" % (n, TITULOS[n]),
                "",
                "**%s → %s** · narración %.1f s de %.1f s disponibles."
                % (tc(e["inicio"]), tc(e["inicio"] + e["dura"]), ini[-1], e["dura"]),
                ""]
        for i, f in enumerate(frases):
            out.append("- `+%05.1f s` %s" % (ini[i], f))
        out.append("")

    out += ["---", "",
            "## Qué queda fuera del video",
            "",
            "- No se locuta el rótulo «GUION DE VOZ — PRIMERA PERSONA» que traen las notas de las",
            "  láminas 7 y 11 en el PPTX: es una marca del documento, no narración.",
            "- Las cifras de escudos (100 / 80 / 40 / +80 / +200) y la mención a la Ley 2466 de 2025",
            "  vienen del PPTX de origen. Si el cliente las ajusta, se cambian en `tools/narracion.json`",
            "  y en la lámina correspondiente, y se vuelve a construir.",
            ""]

    io.open(os.path.join(RAIZ, "GUION-VOZ.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("GUION-VOZ.md escrito (%d:%02d)" % (int(total // 60), int(round(total % 60))))


if __name__ == "__main__":
    main()
