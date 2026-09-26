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

TITULOS = {19: "Apertura · ver, ser visto y confirmar",
           20: "Una maniobra en cinco pasos",
           21: "La ruta y tu estado se inspeccionan",
           22: "Caso integrador · cuatro señales de alerta",
           23: "Reto RiskMann · anticipar antes de exponerse",
           24: "Retroalimentación · la cadena de respuesta",
           25: "Repaso · tres preguntas"}


def tc(s):
    return "%d:%05.2f" % (int(s // 60), s % 60)


def main():
    escenas, total = construir.plan()
    laminas = {x["n"]: x for x in json.load(io.open(os.path.join(AQUI, "narracion.json"), encoding="utf-8"))}
    voz = cronometro.VOZ is not None

    out = ["# Guion de voz · Ruta Segura · Módulo 3",
           "",
           "Video: `ruta-segura-m3` · 1920×1080 · **%d:%02d**." % (int(total // 60), int(round(total % 60))),
           "",
           ("La locución de esta versión es sintética (ElevenLabs, modelo `eleven_v3`)."
            if voz else "Esta versión se entrega **sin voz**. Los tiempos de abajo son una "
                        "**estimación** (ver tools/estimar.py): con la locución real, "
                        "`tools/cronometro.py` los recoloca."),
           "",
           "El montaje está atado a estos tiempos: cada aparición en pantalla cae sobre la",
           "frase que la nombra. Para volver a grabar el módulo con una persona, respeta la",
           "ventana de cada lámina y el montaje encaja sin reeditar el video. Si una lámina",
           "se alarga, se corrige alargando su silencio final, nunca corriendo las siguientes.",
           "",
           "- **Voz:** colombiana, primera persona, tono de instructor — ni locutor comercial ni lectura plana.",
           "- **Silencio:** 0,4 s entre frases y 1 s antes de cambiar de lámina.",
           "- **Cifras:** se leen completas cuando las haya.",
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
    out += ["", "Cierre sin voz: **%s → %s** (rótulo de cierre)."
            % (tc(cierre["inicio"]), tc(cierre["inicio"] + cierre["dura"])), "", "---", ""]

    for e in escenas:
        n = e["lamina"]
        if n is None:
            continue
        frases = laminas[n]["frases"]
        oidas = cronometro.vigentes(n, frases)
        out += ["## Lámina %02d · %s" % (n, TITULOS[n]),
                "",
                "**%s → %s** · narración %.1f s de %.1f s disponibles."
                % (tc(e["inicio"]), tc(e["inicio"] + e["dura"]), cronometro.narracion(n), e["dura"]),
                ""]
        for t, f in oidas:
            out.append("- `+%05.1f s` %s" % (t, f))
        out.append("")

    out += ["---", "",
            "## Qué queda fuera del video",
            "",
            "- Las láminas 23 a 25 del PPTX (reto, retroalimentación, repaso y evaluación):",
            "  los quiz se implementan en la plataforma después de ver el video.",
            "- No se locutan los rótulos del documento que traen algunas notas del PPTX.",
            ""]

    io.open(os.path.join(RAIZ, "GUION-VOZ.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("GUION-VOZ.md escrito (%d:%02d)" % (int(total // 60), int(round(total % 60))))


if __name__ == "__main__":
    main()
