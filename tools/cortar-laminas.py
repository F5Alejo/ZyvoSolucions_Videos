# -*- coding: utf-8 -*-
"""Parte el MP4 de un módulo en piezas de ~1 minuto, cortando entre láminas.

    python tools/cortar-laminas.py videos/<proyecto> [--objetivo 60] [--maximo 75]

El cliente ve los módulos dentro de la plataforma y los quiere en piezas cortas.
No se quita contenido ni se recompone nada: se corta el mismo MP4 que ya está
aprobado. Los cortes caen **solo en frontera de lámina**, que es donde la lámina
saliente ya está apagada (§14.4), así que ninguna pieza empieza o termina a
mitad de una animación ni de una frase.

Las láminas duran ~1 minuto cada una, así que casi siempre una lámina es una
pieza; se agrupan mientras la suma no pase de `--maximo`. El rótulo de cierre,
que no llega a diez segundos, viaja con la última pieza.

Cortar exige recodificar: el corte tiene que caer en el fotograma exacto y los
MP4 del render no traen un fotograma clave en cada frontera. Se recodifica solo
el video (CRF 18, que sobre estas láminas planas no se distingue del original) y
el audio se copia tal cual.
"""
import json, os, re, subprocess, sys

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


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python tools/cortar-laminas.py videos/<proyecto> [--objetivo 60] [--maximo 75]")
    proyecto = os.path.abspath(sys.argv[1])
    objetivo = float(sys.argv[sys.argv.index("--objetivo") + 1]) if "--objetivo" in sys.argv else 60.0
    maximo = float(sys.argv[sys.argv.index("--maximo") + 1]) if "--maximo" in sys.argv else 75.0

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

    grupos = agrupar(escenas, objetivo, maximo)
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
