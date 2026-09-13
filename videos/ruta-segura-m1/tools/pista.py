# -*- coding: utf-8 -*-
"""Arma la pista de voz del módulo: cada lámina en su sitio del máster.

    python tools/pista.py

Toma los once MP3 de `assets/voz/` y los coloca en el instante en que empieza su
lámina (el mismo plano que usa `tools/construir.py`), normaliza a −16 LUFS y
escribe `assets/voz/modulo-1.wav`. Verifica al final que la pista no salió muda.
"""
import io, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
RAIZ = os.path.dirname(AQUI)
VOZ = os.path.join(RAIZ, "assets", "voz")
# MP3 y no WAV: el WAV de estos once minutos pesa 61 MB y el navegador
# tarda mas de los 10 s que da `check` en cargarlo antes de la primera muestra.
SALIDA = os.path.join(VOZ, "modulo-1.mp3")

import construir


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


def main():
    escenas, total = construir.plan()
    entradas, filtros, etiquetas = [], [], []
    for i, e in enumerate(escenas):
        if e["lamina"] is None:
            continue
        mp3 = os.path.join(VOZ, "s%02d.mp3" % e["lamina"])
        if not os.path.exists(mp3):
            raise SystemExit("falta %s — corre antes tools/voz-eleven.py" % mp3)
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
