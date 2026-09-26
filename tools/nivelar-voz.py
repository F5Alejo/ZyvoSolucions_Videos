# -*- coding: utf-8 -*-
"""Lleva una locucion de TTS a nivel de emision, archivo por archivo.

    python ../../tools/nivelar-voz.py <carpeta-origen> <carpeta-destino> [LUFS]

Por que existe este paso, en vez de hacerlo dentro de mezcla.py: loudnorm dentro
de un filter_complex entrega 192 kHz y desplaza los timestamps, asi que el
apad/atrim posterior devuelve silencio -- sin error y con codigo de salida 0.
Nivelar a disco lo evita y deja un master de voz que se puede escuchar.

Cadena: compresor suave (empareja silabas) -> loudnorm al LUFS pedido -> 44.1 kHz.
"""
import os, re, subprocess, sys


def main(origen, destino, lufs=-14.0):
    if not os.path.isdir(destino):
        os.makedirs(destino)
    archivos = sorted(f for f in os.listdir(origen) if f.lower().endswith((".mp3", ".wav")))
    if not archivos:
        sys.exit("no hay locucion en " + origen)
    for nombre in archivos:
        ent = os.path.join(origen, nombre)
        sal = os.path.join(destino, os.path.splitext(nombre)[0] + ".wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ent, "-af",
                        "acompressor=threshold=0.1:ratio=3:attack=10:release=180,"
                        f"loudnorm=I={lufs}:TP=-1.5:LRA=7",
                        "-ar", "44100", sal], check=True)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", sal, "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True)
        med = float(re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr).group(1))
        pico = float(re.search(r"max_volume: (-?[\d.]+) dB", r.stderr).group(1))
        print("  %-10s media %6.1f dB   pico %6.1f dB  -> %s" % (nombre, med, pico, sal))
    print("%d lineas niveladas a %.1f LUFS" % (len(archivos), lufs))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else -14.0)
