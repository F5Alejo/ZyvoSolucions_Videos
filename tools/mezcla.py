"""Mezclador de la serie PESV: cama sintetizada + locucion + pistas + efectos.

Uso (desde la carpeta del proyecto):  python ../../tools/mezcla.py tools/mezcla-<nombre>.json

La mezcla es CONFIGURACION, no codigo: cada pieza nueva es un JSON con la
duracion y, todas opcionales, las capas de la "cama", las lineas de "voz", las
"pistas" (archivos completos, p. ej. la de tools/ritmo.py) y los "efectos", cada uno
en su segundo exacto. "pasa_altos" (Hz) recorta la subgrave antes de normalizar.
Este script no cambia entre modulos.

Cuatro lecciones de produccion estan escritas aqui para que no se repitan:

1. La cama vive en 110 Hz hacia arriba. Un drone en 55-82 Hz mide bien en el
   vumetro y suena a silencio en un portatil o un telefono.
2. El bus de voz se duplica con asplit antes del ducking. Un pad de ffmpeg solo
   se consume una vez; usarlo dos veces borro la voz entera de una mezcla, sin
   error y con codigo de salida 0.
3. Al terminar se VERIFICA el espectro: si la banda alta (>400 Hz) no tiene
   nivel, el script falla en vez de entregar un archivo mudo.
4. Con bombo e impactos, la subgrave se lleva la normalizacion y deja los agudos
   16 dB abajo. "pasa_altos": 90 lo corrige; mide tres bandas despues.

Los efectos salen de la libreria incluida en /media-use (licencia Pixabay: uso
comercial sin atribucion). La cama es sintesis propia: no hay derechos de nadie.
"""

import json, os, re, subprocess, sys

SFX_DIR = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    total = cfg["duracion"]
    out = cfg["salida"]
    inputs, filters, bed, fg = [], [], [], []
    i = 0

    for c in cfg.get("cama", []):
        dur = min(c["fin"], total) - c["inicio"]
        inputs += ["-f", "lavfi", "-t", f"{dur}", "-i",
                   f"sine=frequency={c['hz']}:sample_rate=44100"]
        filters.append(
            f"[{i}]tremolo=f=0.12:d=0.30,lowpass=f=2200,"
            f"afade=t=in:st=0:d={c.get('entrada', 2)},"
            f"afade=t=out:st={max(0, dur - c.get('salida', 3))}:d={c.get('salida', 3)},"
            f"volume={c['ganancia']},adelay={int(c['inicio']*1000)}|{int(c['inicio']*1000)}[b{i}]")
        bed.append(f"[b{i}]"); i += 1

    # "pistas" (p. ej. tools/ritmo.py) entran igual que la voz: un archivo en un segundo
    for v in cfg.get("voz", []) + cfg.get("pistas", []):
        inputs += ["-i", v["archivo"]]
        ms = int(v["en"] * 1000)
        filters.append(f"[{i}]volume={v.get('ganancia', 1.0)},adelay={ms}|{ms}[v{i}]")
        fg.append(f"[v{i}]"); i += 1

    for e in cfg.get("efectos", []):
        path = os.path.join(SFX_DIR, e["efecto"] + ".mp3")
        if not os.path.exists(path):
            sys.exit("falta el efecto: " + e["efecto"])
        inputs += ["-i", path]
        ms = int(e["en"] * 1000)
        filters.append(f"[{i}]volume={e['ganancia']},adelay={ms}|{ms}[v{i}]")
        fg.append(f"[v{i}]"); i += 1

    chain = ";".join(filters)
    chain += ";" + "".join(fg) + f"amix=inputs={len(fg)}:normalize=0[fgmix]"
    if bed:
        chain += ";" + "".join(bed) + f"amix=inputs={len(bed)}:normalize=0,aecho=0.8:0.85:180|320:0.25|0.15[bed]"
        chain += ";[fgmix]asplit=2[fg1][fg2]"  # leccion 2: el bus se duplica, nunca se reutiliza
        chain += ";[bed][fg1]sidechaincompress=threshold=0.05:ratio=6:attack=15:release=420[bedduck]"
        chain += ";[bedduck][fg2]amix=inputs=2:normalize=0,"
    else:
        chain += ";[fgmix]"
    # "pasa_altos" (Hz, opcional): recorta la subgrave antes de normalizar, para que no se
    # lleve el volumen de lo que sí suena en parlantes pequeños
    hp = f"highpass=f={cfg['pasa_altos']}:poles=2," if cfg.get("pasa_altos") else ""
    chain += f"apad,atrim=0:{total},{hp}loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[out]"

    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs +
                   ["-filter_complex", chain, "-map", "[out]", "-ar", "44100", out], check=True)

    # leccion 3: verificar que la voz esta de verdad en el archivo
    r = subprocess.run(["ffmpeg", "-i", out, "-af", "highpass=f=400,volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
    alta = float(m.group(1)) if m else -99.0
    print(f"mezcla: {len(bed)} capas de cama + {len(cfg.get('voz', []))} voces + "
          f"{len(cfg.get('pistas', []))} pistas + {len(cfg.get('efectos', []))} efectos -> {out}")
    print(f"banda alta (>400 Hz): {alta:.1f} dB de media")
    if (cfg.get("voz") or cfg.get("pistas")) and alta < -40:
        sys.exit("FALLO: la banda de voz esta vacia. La voz no llego a la mezcla.")


if __name__ == "__main__":
    main(sys.argv[1])
