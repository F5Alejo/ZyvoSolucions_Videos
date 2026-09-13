# -*- coding: utf-8 -*-
"""Une las partes del render y les pega la locución.

    python tools/construir.py --sin-audio --partes 4
    npx hyperframes render -c index-parte-1.html -o renders/parte-1.mp4 --quality high --low-memory-mode
    ... (una por una)
    python tools/montar.py

Por qué en partes: esta máquina tiene 8 GB y el render de once minutos de una
sola vez lo mataba el sistema — entre el Chrome del usuario (~1,5 GB), el Chrome
sin cabeza del render y un ffmpeg que se asienta en ~650 MB no hay margen.
Partirlo no baja el pico, pero **acorta la exposición y hace barato el fallo**:
si una parte muere se repite esa parte, no cuarenta minutos de trabajo.

Por qué la voz va aparte: metida en el `index.html`, Chrome decodifica el MP3
entero a PCM (~250 MB para once minutos) y ese es justo el margen que falta.

No hay riesgo de desfase: las partes se cortan en frontera de escena, se unen sin
recodificar, y la pista arranca en cero y mide lo mismo que el máster. El script
verifica las dos cosas antes de escribir nada.
"""
import glob, io, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)
RENDERS = os.path.join(RAIZ, "renders")
PISTA = os.path.join(RAIZ, "assets", "voz", "modulo-2.mp3")
FINAL = os.path.join(RENDERS, "ruta-segura-m2-narrado.mp4")

import construir


def duracion(ruta):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", ruta])
    return float(out.decode().strip())


def pistas(ruta):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                                   "-of", "csv=p=0", ruta])
    return out.decode().split()


def unir(partes, destino):
    """Concatena sin recodificar: todas salen del mismo codificador."""
    lista = os.path.join(RENDERS, "partes.txt")
    io.open(lista, "w", encoding="utf-8", newline="\n").write(
        "".join("file '%s'\n" % os.path.basename(p) for p in partes))
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                           "-i", lista, "-c", "copy", destino])
    os.remove(lista)


def main():
    _, total = construir.plan()

    partes = sorted(glob.glob(os.path.join(RENDERS, "parte-*.mp4")),
                    key=lambda p: int(re.search(r"parte-(\d+)", p).group(1)))
    if partes:
        suma = sum(duracion(p) for p in partes)
        print("%d partes, %.2f s en total:" % (len(partes), suma))
        for p in partes:
            print("   %-14s %6.2f s" % (os.path.basename(p), duracion(p)))
        if abs(suma - total) > 0.5:
            raise SystemExit("las partes suman %.2f s y el máster mide %.2f s: "
                             "falta alguna o son de otra construcción" % (suma, total))
        mudo = os.path.join(RENDERS, "completo-mudo.mp4")
        unir(partes, mudo)
    else:
        sueltos = [p for p in glob.glob(os.path.join(RENDERS, "*.mp4"))
                   if "narrado" not in p and "completo-mudo" not in p]
        if not sueltos:
            raise SystemExit("no hay render en renders/")
        mudo = max(sueltos, key=os.path.getmtime)

    dv, da = duracion(mudo), duracion(PISTA)
    print("video %.2f s  ·  pista %.2f s  ·  máster %.2f s" % (dv, da, total))
    if abs(dv - da) > 0.5:
        raise SystemExit("el video y la pista no miden lo mismo: el render no es "
                         "de esta construcción")

    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mudo, "-i", PISTA,
                           "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                           "-shortest", FINAL])

    print("")
    print("%s  %.1f MB  %.2f s  pistas: %s"
          % (os.path.relpath(FINAL, RAIZ), os.path.getsize(FINAL) / 1e6,
             duracion(FINAL), ", ".join(pistas(FINAL))))


if __name__ == "__main__":
    main()
