# -*- coding: utf-8 -*-
"""Mide cuanto sobresale la voz sobre la musica DENTRO de cada frase hablada.

No basta con el nivel general de la mezcla: la queja tipica -"la musica tapa la
voz"- ocurre en momentos concretos. Se extraen los dos buses por separado con el
mismo grafo que usa mezcla.py y se comparan ventana por ventana.

    python tools/margen-voz.py tools/final-A.json

Objetivo: la voz entre +7 y +25 dB sobre la musica en CADA frase. Por debajo de
+7 la voz pelea; por encima de +25 la musica se hunde y suena a bombeo.
"""
import io, json, os, re, subprocess, sys

cfg_path = sys.argv[1] if len(sys.argv) > 1 else "tools/final-A.json"
cfg = json.load(io.open(cfg_path, encoding="utf-8"))
total = cfg["duracion"]
m = cfg["musica"][0]
PAD = "apad,atrim=0:%s" % total
d = cfg.get("ducking", {})

inputs, fil, voz = [], [], []
i = 0
for v in cfg["voz"]:
    inputs += ["-i", v["archivo"]]
    ms = int(v["en"] * 1000)
    fil.append("[%d]volume=%s,adelay=%d|%d,%s[v%d]" % (i, v.get("ganancia", 1.0), ms, ms, PAD, i))
    voz.append("[v%d]" % i)
    i += 1

desde = m.get("desde", 0)
hueco = ("equalizer=f=%s:t=q:w=1.0:g=%s," % (m.get("hueco_hz", 1900), m["hueco_voz"])
         if m.get("hueco_voz") else "")
fade = ""
if m.get("entrada"):
    fade += "afade=t=in:st=0:d=%s," % m["entrada"]
if m.get("salida"):
    fade += "afade=t=out:st=%s:d=%s," % (total - m["salida"], m["salida"])
inputs += ["-i", m["archivo"]]
fil.append("[%d]atrim=start=%s:end=%s,asetpts=PTS-STARTPTS,%s%svolume=%s,%s[mus]"
           % (i, desde, desde + total, hueco, fade, m.get("ganancia", 1.0), PAD))

chain = ";".join(fil)
chain += ";" + "".join(voz) + "amix=inputs=%d:normalize=0[vozbus]" % len(voz)
chain += ";[vozbus]asplit=2[k][vout]"
chain += (";[mus][k]sidechaincompress=threshold=%s:ratio=%s:attack=%s:release=%s[mout]"
          % (d.get("umbral", 0.05), d.get("ratio", 6), d.get("ataque", 15), d.get("reposo", 420)))

subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", chain,
                "-map", "[vout]", "-t", str(total), "bus-voz.wav",
                "-map", "[mout]", "-t", str(total), "bus-musica.wav"], check=True)


def nivel(archivo, desde_s, dur):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(desde_s), "-t", str(dur),
                        "-i", archivo, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr).group(1))


# los arranques se leen de la propia mezcla: no se vuelven a escribir a mano
bases = [v["en"] for v in cfg["voz"]]
tiempos = json.load(io.open("tools/tiempos-voz.json", encoding="utf-8"))
print("  frase                                        voz     musica   margen")
print("  " + "-" * 68)
peor = 99
for t in tiempos:
    b = bases[t["n"] - 1]
    for k, f in enumerate(t["frases"]):
        ini = b + t["inicios"][k]
        dur = t["inicios"][k + 1] - t["inicios"][k]
        if dur < 0.3:
            continue
        v, mu = nivel("bus-voz.wav", ini, dur), nivel("bus-musica.wav", ini, dur)
        margen = v - mu
        peor = min(peor, margen)
        print("  %-42s %7.1f %8.1f %+8.1f dB" % (f[:42], v, mu, margen))
print("  " + "-" * 68)
print("  margen minimo: %+.1f dB" % peor)
os.remove("bus-voz.wav")
os.remove("bus-musica.wav")
