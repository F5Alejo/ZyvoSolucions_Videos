# -*- coding: utf-8 -*-
"""Arma la pista de voz del módulo: cada lámina en su sitio del máster.

    python tools/pista.py

Toma los once MP3 de `assets/voz/` y los coloca en el instante en que empieza su
lámina (el mismo plano que usa `tools/construir.py`), normaliza a −16 LUFS y
escribe `assets/voz/modulo-2.wav`. Verifica al final que la pista no salió muda.
"""
import io, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)
VOZ = os.path.join(RAIZ, "assets", "voz")
# MP3 y no WAV: el WAV de estos once minutos pesa 61 MB y el navegador
# tarda mas de los 10 s que da `check` en cargarlo antes de la primera muestra.
SALIDA = os.path.join(VOZ, "modulo-2.mp3")

import construir, cronometro


def duracion(ruta):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", ruta])
    return float(out.decode().strip())


def volumen(ruta):
    p = subprocess.run(["ffmpeg", "-v", "info", "-i", ruta, "-af", "volumedetect",
                        "-f", "null", "-"], capture_output=True)
    for linea in p.stderr.decode("utf-8", "replace").splitlines():
        if "mean_volume" in linea:
            return linea.split(":")[-1].strip()
    return "?"


def recortar(n, mp3):
    """Quita de la locución de la lámina los tramos de `cronometro.tramos(n)`.

    Devuelve la ruta a usar: el MP3 original si no hay cortes, o un WAV con los
    tramos que quedan unidos. Los cortes caen en el silencio entre frases.
    """
    tramos = cronometro.tramos(n)
    if not tramos:
        return mp3
    fin = duracion(mp3)
    quedan, t = [], 0.0
    for a, b in tramos:
        if a > t:
            quedan.append((t, a))
        t = b
    if t < fin:
        quedan.append((t, fin))
    partes = "".join("[0:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS[p%d];" % (a, b, i)
                     for i, (a, b) in enumerate(quedan))
    cadena = partes + "".join("[p%d]" % i for i in range(len(quedan))) + "concat=n=%d:v=0:a=1[out]" % len(quedan)
    salida = os.path.join(VOZ, "s%02d-recortada.wav" % n)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-filter_complex", cadena,
                           "-map", "[out]", salida])
    return salida


def main():
    escenas, total = construir.plan()
    entradas, filtros, etiquetas = [], [], []
    for i, e in enumerate(escenas):
        if e["lamina"] is None:
            continue
        mp3 = os.path.join(VOZ, "s%02d.mp3" % e["lamina"])
        if not os.path.exists(mp3):
            raise SystemExit("falta %s — corre antes tools/voz-eleven.py" % mp3)
        mp3 = recortar(e["lamina"], mp3)
        d = duracion(mp3)
        if d > e["dura"]:
            raise SystemExit("lámina %d: la locución dura %.2f s y su plano %.2f s"
                             % (e["lamina"], d, e["dura"]))
        entradas += ["-i", mp3]
        n = len(etiquetas)
        # adelay quiere milisegundos y un valor por canal
        filtros.append("[%d:a]aresample=44100,adelay=%d|%d[v%d]"
                       % (n, int(e["inicio"] * 1000), int(e["inicio"] * 1000), n))
        etiquetas.append("[v%d]" % n)

    cadena = ";".join(filtros) + ";" + "".join(etiquetas)
    cadena += ("amix=inputs=%d:normalize=0,apad,atrim=0:%s,"
               "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[out]" % (len(etiquetas), total))

    cmd = (["ffmpeg", "-v", "error", "-y"] + entradas
           + ["-filter_complex", cadena, "-map", "[out]", "-ac", "1",
              "-c:a", "libmp3lame", "-b:a", "128k", SALIDA])
    subprocess.check_call(cmd)

    print("%s  %.2f s  (máster %.2f s)" % (os.path.relpath(SALIDA, RAIZ), duracion(SALIDA), total))
    # sin flechas ni tipografía fina: la consola de Windows es cp1252
    print("volumen medio: %s  (si dice -91 dB la pista salio muda)" % volumen(SALIDA))


if __name__ == "__main__":
    main()
