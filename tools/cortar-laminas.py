# -*- coding: utf-8 -*-
"""Parte el MP4 de un módulo en piezas de ~1 minuto, cortando entre láminas.

    python tools/cortar-laminas.py videos/<proyecto> [--objetivo 60] [--maximo 75]

El cliente ve los módulos dentro de la plataforma y los quiere en piezas cortas.
No se quita contenido ni se recompone nada: se corta el mismo MP4 que ya está
aprobado. Los cortes caen **solo en frontera de lámina**, que es donde la lámina
saliente ya está apagada (§14.4), así que ninguna pieza empieza o termina a
mitad de una animación ni de una frase.

Con `--piezas N` manda el número de piezas: se reparten las láminas en N trozos
lo más parejos posible, que es lo que pide la plataforma (dos o tres por módulo,
de uno a dos minutos). Sin él manda la duración: se agrupan láminas mientras la
suma no pase de `--maximo`. El rótulo de cierre, que no llega a diez segundos,
viaja siempre con la última pieza.

Cortar exige recodificar: el corte tiene que caer en el fotograma exacto y los
MP4 del render no traen un fotograma clave en cada frontera. Se recodifica solo
el video (CRF 18, que sobre estas láminas planas no se distingue del original) y
el audio se copia tal cual.
"""
import itertools, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def duracion(ruta):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", ruta])
    return float(out.decode().strip())


def plan(proyecto):
    """Orden, inicio y duración de cada lámina, leídos del propio proyecto."""
    codigo = ("import sys, json; sys.path.insert(0, r'%s'); import construir; "
              "print(json.dumps(construir.plan()))" % os.path.join(proyecto, "tools"))
    out = subprocess.check_output([sys.executable, "-c", codigo], cwd=proyecto)
    return json.loads(out.decode())


def _pieza(trozo):
    return {"desde": trozo[0]["inicio"],
            "hasta": round(trozo[-1]["inicio"] + trozo[-1]["dura"], 3),
            "dura": round(trozo[-1]["inicio"] + trozo[-1]["dura"] - trozo[0]["inicio"], 3),
            "laminas": [e["lamina"] for e in trozo]}


def agrupar(escenas, objetivo, maximo):
    """Junta láminas consecutivas mientras la pieza no pase de `maximo`.

    El rótulo de cierre (sin número de lámina) nunca abre pieza: es un cierre.
    """
    grupos = []
    for e in escenas:
        cierre = e["lamina"] is None
        if grupos and (cierre or grupos[-1]["dura"] + e["dura"] <= maximo
                       or grupos[-1]["dura"] < objetivo / 2):
            g = grupos[-1]
            g["hasta"] = round(e["inicio"] + e["dura"], 3)
            g["dura"] = round(g["hasta"] - g["desde"], 3)
            g["laminas"].append(e["lamina"])
        else:
            grupos.append({"desde": e["inicio"], "hasta": round(e["inicio"] + e["dura"], 3),
                           "dura": e["dura"], "laminas": [e["lamina"]]})
    return grupos


def repartir(escenas, piezas):
    """Reparte las láminas en exactamente `piezas` trozos lo más parejos posible.

    Se usa cuando lo que manda es **cuántas piezas** tiene el módulo, no cuánto
    dura cada una: la plataforma quiere dos o tres por módulo. Se prueban todos
    los cortes posibles —son pocas láminas— y gana el reparto cuya pieza más
    larga sea la más corta; a igualdad, el de menor diferencia entre la más larga
    y la más corta. Los cortes siguen cayendo en frontera de lámina.
    """
    n = len(escenas)
    piezas = max(1, min(piezas, n))
    mejor = None
    for cortes in itertools.combinations(range(1, n), piezas - 1):
        limites = (0,) + cortes + (n,)
        trozos = [escenas[a:b] for a, b in zip(limites, limites[1:])]
        duras = [sum(e["dura"] for e in t) for t in trozos]
        clave = (round(max(duras), 3), round(max(duras) - min(duras), 3))
        if mejor is None or clave < mejor[0]:
            mejor = (clave, trozos)
    return [_pieza(t) for t in mejor[1]]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python tools/cortar-laminas.py videos/<proyecto> "
                         "[--piezas N | --objetivo 60 --maximo 75]")
    proyecto = os.path.abspath(sys.argv[1])
    objetivo = float(sys.argv[sys.argv.index("--objetivo") + 1]) if "--objetivo" in sys.argv else 60.0
    maximo = float(sys.argv[sys.argv.index("--maximo") + 1]) if "--maximo" in sys.argv else 75.0
    piezas = int(sys.argv[sys.argv.index("--piezas") + 1]) if "--piezas" in sys.argv else 0

    nombre = os.path.basename(proyecto.rstrip("/\\"))
    entero = os.path.join(proyecto, "renders", "%s-narrado.mp4" % nombre)
    if not os.path.exists(entero):
        raise SystemExit("falta %s — corre antes tools/montar.py" % entero)

    escenas, total = plan(proyecto)
    if abs(duracion(entero) - total) > 0.5:
        raise SystemExit("el MP4 mide %.2f s y el montaje %.2f s: no es de esta construcción"
                         % (duracion(entero), total))

    dest = os.path.join(proyecto, "renders", "cortes")
    if not os.path.isdir(dest):
        os.makedirs(dest)

    grupos = repartir(escenas, piezas) if piezas else agrupar(escenas, objetivo, maximo)
    for i, g in enumerate(grupos, 1):
        laminas = [x for x in g["laminas"] if x is not None]
        etiqueta = "lamina %d" % laminas[0] if len(laminas) == 1 else "laminas %d-%d" % (laminas[0], laminas[-1])
        salida = os.path.join(dest, "%s-parte-%d-de-%d.mp4" % (nombre, i, len(grupos)))
        subprocess.check_call(
            ["ffmpeg", "-v", "error", "-y", "-i", entero, "-ss", "%.3f" % g["desde"],
             "-to", "%.3f" % g["hasta"], "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", salida])
        print("parte %d/%d  %-22s  %6.1f -> %6.1f  (%4.1f s)  %s"
              % (i, len(grupos), etiqueta, g["desde"], g["hasta"], duracion(salida),
                 os.path.basename(salida)))

    print("-" * 60)
    print("%d piezas en %s" % (len(grupos), os.path.relpath(dest, RAIZ)))


if __name__ == "__main__":
    main()
