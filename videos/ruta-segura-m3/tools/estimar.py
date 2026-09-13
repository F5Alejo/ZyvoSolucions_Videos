# -*- coding: utf-8 -*-
"""Estima los tiempos de la locución cuando todavía no se puede generar.

    python tools/estimar.py

Escribe `tiempos-referencia.json` con la misma forma que produce
`voz-eleven.py`, para poder componer las láminas sin esperar a la API.

El ajuste sale de medir las 187 frases ya locutadas de los módulos 1 y 2 con
esta misma voz (`nPczCjzI2devNBz1zQrb`, `eleven_v3`):

    duración = 0.06786 x caracteres + 0.374 s      error medio 0.49 s

**Esto es un andamio, no el resultado.** En cuanto haya clave se corre
`voz-eleven.py`, que escribe `tiempos-voz.json` con los tiempos reales, y
`cronometro.py` recoloca las marcas de todas las láminas: exacto en cada
frontera de frase. El error de esta estimación no llega al video final.
"""
import io, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
POR_CARACTER = 0.06786
ARRANQUE = 0.374


def main():
    laminas = json.load(io.open(os.path.join(AQUI, "narracion.json"), encoding="utf-8"))
    out, total = [], 0.0
    for x in laminas:
        t, ini = 0.0, []
        for f in x["frases"]:
            ini.append(round(t, 3))
            t += POR_CARACTER * len(f) + ARRANQUE
        ini.append(round(t, 3))
        out.append({"n": x["n"], "inicios": ini})
        total += t
        print("lámina %02d  %6.2f s estimados  (%d frases)" % (x["n"], t, len(x["frases"])))

    io.open(os.path.join(AQUI, "tiempos-referencia.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print("-" * 44)
    print("narración estimada %.1f s = %d:%02d" % (total, int(total // 60), int(round(total % 60))))
    print("escrito tools/tiempos-referencia.json (estimado — reemplazar con la locución real)")


if __name__ == "__main__":
    main()
