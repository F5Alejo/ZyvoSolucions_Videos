# -*- coding: utf-8 -*-
"""Exporta el audio del video a MP3.

    python tools/exportar-mp3.py voz          # arma la locución desde assets/voz/
    python tools/exportar-mp3.py video        # extrae la pista del MP4 ya renderizado

`voz` no necesita el render: coloca cada locución de ElevenLabs en el segundo
exacto en que empieza su plano y normaliza a -16 LUFS (la misma referencia que
usa tools/mezcla.py del repositorio). Sirve para las tres versiones del A/B
testing, porque la pista de voz es la misma en la Versión A y se omite en B y C.

Los segundos de inicio salen de STORYBOARD.md: son la suma de las duraciones de
los planos anteriores. Si cambias una duración, cambia también aquí.
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
VOZ = os.path.join(RAIZ, "assets", "voz")
RENDERS = os.path.join(RAIZ, "renders")

# plano -> segundo en que arranca dentro del video completo (45 s)
INICIOS = [0, 8, 15, 23, 30, 38]
TOTAL = 45
MP4 = os.path.join(RENDERS, "riskmann-consulta-pesv-A.mp4")


def correr(cmd):
    subprocess.run(cmd, check=True)


def desde_voz():
    entradas, filtros, etiquetas = [], [], []
    for i, inicio in enumerate(INICIOS):
        mp3 = os.path.join(VOZ, "f%02d.mp3" % (i + 1))
        if not os.path.exists(mp3):
            raise SystemExit("falta %s — corre antes tools/voz-eleven.py" % mp3)
        entradas += ["-i", mp3]
        filtros.append("[%d]adelay=%d:all=1[a%d]" % (i, inicio * 1000, i))
        etiquetas.append("[a%d]" % i)

    cadena = ";".join(filtros) + ";" + "".join(etiquetas)
    cadena += ("amix=inputs=%d:normalize=0,apad,atrim=0:%d,"
               "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[out]" % (len(INICIOS), TOTAL))

    salida = os.path.join(RENDERS, "riskmann-consulta-pesv-locucion.mp3")
    correr(["ffmpeg", "-y", "-loglevel", "error"] + entradas +
           ["-filter_complex", cadena, "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "192k", salida])
    print("escrito", salida)


def desde_video():
    if not os.path.exists(MP4):
        raise SystemExit("todavía no existe %s — renderiza primero" % MP4)
    salida = os.path.join(RENDERS, "riskmann-consulta-pesv-A-audio.mp3")
    correr(["ffmpeg", "-y", "-loglevel", "error", "-i", MP4, "-vn",
            "-c:a", "libmp3lame", "-b:a", "192k", salida])
    print("escrito", salida)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "voz"
    if not os.path.isdir(RENDERS):
        os.makedirs(RENDERS)
    if modo == "voz":
        desde_voz()
    elif modo == "video":
        desde_video()
    else:
        raise SystemExit("uso: python tools/exportar-mp3.py [voz|video]")
