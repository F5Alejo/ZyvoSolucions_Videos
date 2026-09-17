"""Mezclador de la serie PESV: cama sintetizada + locucion + pistas + musica + efectos.

Uso (desde la carpeta del proyecto):  python ../../tools/mezcla.py tools/mezcla-<nombre>.json

La mezcla es CONFIGURACION, no codigo: cada pieza nueva es un JSON con la
duracion y, todas opcionales, las capas de la "cama", las lineas de "voz", las
"pistas" (archivos completos, p. ej. la de tools/ritmo.py), la "musica" y los
"efectos", cada uno en su segundo exacto. "pasa_altos" (Hz) recorta la subgrave
antes de normalizar. Este script no cambia entre modulos.

Siete lecciones de produccion estan escritas aqui para que no se repitan:

1. La cama vive en 110 Hz hacia arriba. Un drone en 55-82 Hz mide bien en el
   vumetro y suena a silencio en un portatil o un telefono.
2. El bus de voz se duplica con asplit antes del ducking. Un pad de ffmpeg solo
   se consume una vez; usarlo dos veces borro la voz entera de una mezcla, sin
   error y con codigo de salida 0.
3. Al terminar se VERIFICA el espectro: si la banda alta (>400 Hz) no tiene
   nivel, el script falla en vez de entregar un archivo mudo.
4. Con bombo e impactos, la subgrave se lleva la normalizacion y deja los agudos
   16 dB abajo. "pasa_altos": 90 lo corrige; mide tres bandas despues.
5. Una pista de musica real va en "musica", nunca en "pistas". "pistas" desemboca
   en el mismo amix que la locucion y nada la aparta: en los picos se come la voz.
   "musica" pasa por el bus con ducking y admite "hueco_voz" (dB, negativo) para
   abrirle sitio a la voz en los medios, donde vive la inteligibilidad.
6. Toda rama se rellena hasta la duracion final antes de mezclarse. Con ramas de
   2 s y de 37 s colgando del mismo asplit, ffmpeg acumula bufer hasta atascarse:
   una mezcla de 37 s tardo 7 minutos en vez de 2 segundos.
7. Un TTS no entrega nivel de emision: la voz sale ~19 dB por debajo de una pista
   de catalogo, y ningun ducking compensa eso. Se nivela ANTES, a disco, con
   tools/nivelar-voz.py; aqui no, porque loudnorm dentro del filter_complex
   entrega 192 kHz y desplaza los timestamps: el apad/atrim posterior devuelve
   silencio sin dar ningun error. Verificar SIEMPRE el margen voz-musica frase
   por frase, no el nivel general de la mezcla.

Los efectos salen de la libreria incluida en /media-use (licencia Pixabay: uso
comercial sin atribucion). La cama es sintesis propia: no hay derechos de nadie.
"""

import json, os, re, subprocess, sys

SFX_DIR = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    total = cfg["duracion"]
    out = cfg["salida"]
    inputs, filters, bed, fg, mus, voz = [], [], [], [], [], []
    i = 0
    # leccion 6: toda rama se rellena hasta la duracion final antes de mezclarse.
    # Con ramas de 2 s y de 37 s colgando del mismo asplit, ffmpeg acumula bufer
    # hasta atascarse: una mezcla de 37 s se quedo 7 minutos sin terminar.
    PAD = f"apad,atrim=0:{total}"

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
    n_voz = len(cfg.get("voz", []))
    for k, v in enumerate(cfg.get("voz", []) + cfg.get("pistas", [])):
        inputs += ["-i", v["archivo"]]
        ms = int(v["en"] * 1000)
        filters.append(f"[{i}]volume={v.get('ganancia', 1.0)},adelay={ms}|{ms},{PAD}[v{i}]")
        if k < n_voz and cfg.get("musica"):
            # leccion 2 otra vez: para servir de llave el pad se duplica, no se reusa
            filters.append(f"[v{i}]asplit=2[v{i}a][v{i}b]")
            fg.append(f"[v{i}a]")
            voz.append(f"[v{i}b]")   # la llave del ducking: solo la locucion, no los efectos
        else:
            fg.append(f"[v{i}]")
        i += 1

    # leccion 5: una "pista" de musica real NO va en el bus de la voz.
    # "pistas" desemboca en el mismo amix que la locucion, asi que nada la aparta
    # y en los picos se come la voz. "musica" pasa por el bus que SI se duckea, y
    # ademas puede abrirle un hueco a la voz en los medios ("hueco_voz", en dB).
    for m in cfg.get("musica", []):
        inputs += ["-i", m["archivo"]]
        desde = m.get("desde", 0)
        ms = int(m.get("en", 0) * 1000)
        # se recorta SIEMPRE al tramo que se usa: una pista de catalogo trae
        # minutos de sobra y arrastrarlos entero por el ducking cuesta minutos de CPU
        pre = f"atrim=start={desde}:end={desde + total},asetpts=PTS-STARTPTS,"
        # el hueco es una campana ancha centrada donde vive la inteligibilidad
        hueco = (f"equalizer=f={m.get('hueco_hz', 1900)}:t=q:w=1.0:g={m['hueco_voz']},"
                 if m.get("hueco_voz") else "")
        fade = ""
        if m.get("entrada"):
            fade += f"afade=t=in:st=0:d={m['entrada']},"
        if m.get("salida"):
            fade += f"afade=t=out:st={max(0, total - ms / 1000.0 - m['salida'])}:d={m['salida']},"
        filters.append(f"[{i}]{pre}{hueco}{fade}volume={m.get('ganancia', 1.0)},"
                       f"adelay={ms}|{ms},{PAD}[m{i}]")
        mus.append(f"[m{i}]"); i += 1

    for e in cfg.get("efectos", []):
        path = os.path.join(SFX_DIR, e["efecto"] + ".mp3")
        if not os.path.exists(path):
            sys.exit("falta el efecto: " + e["efecto"])
        inputs += ["-i", path]
        ms = int(e["en"] * 1000)
        filters.append(f"[{i}]volume={e['ganancia']},adelay={ms}|{ms},{PAD}[v{i}]")
        fg.append(f"[v{i}]"); i += 1

    chain = ";".join(filters)
    chain += ";" + "".join(fg) + f"amix=inputs={len(fg)}:normalize=0[fgmix]"

    # todo lo que debe apartarse bajo la voz: la cama sintetizada y la musica
    duck = []
    if bed:
        chain += ";" + "".join(bed) + f"amix=inputs={len(bed)}:normalize=0,aecho=0.8:0.85:180|320:0.25|0.15[bed]"
        duck.append("[bed]")
    duck += mus

    if duck:
        if len(duck) > 1:
            chain += ";" + "".join(duck) + f"amix=inputs={len(duck)}:normalize=0[duckin]"
        else:
            chain += f";{duck[0]}anull[duckin]"
        # la llave: la locucion sola si la hay, si no todo el frente (comportamiento previo)
        if voz:
            chain += ";" + "".join(voz) + (f"amix=inputs={len(voz)}:normalize=0[llave]"
                                           if len(voz) > 1 else "anull[llave]")
            llave = "[llave]"
            resto = "[fgmix]"
        else:
            chain += ";[fgmix]asplit=2[fg1][fg2]"  # leccion 2: el bus se duplica, nunca se reutiliza
            llave, resto = "[fg1]", "[fg2]"
        d = cfg.get("ducking", {})
        chain += (f";[duckin]{llave}sidechaincompress="
                  f"threshold={d.get('umbral', 0.05)}:ratio={d.get('ratio', 6)}:"
                  f"attack={d.get('ataque', 15)}:release={d.get('reposo', 420)}[duckout]")
        chain += f";[duckout]{resto}amix=inputs=2:normalize=0,"
    else:
        chain += ";[fgmix]"
    # "pasa_altos" (Hz, opcional): recorta la subgrave antes de normalizar, para que no se
    # lleve el volumen de lo que sí suena en parlantes pequeños
    hp = f"highpass=f={cfg['pasa_altos']}:poles=2," if cfg.get("pasa_altos") else ""
    chain += f"apad,atrim=0:{total},{hp}loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[out]"

    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs +
                   ["-filter_complex", chain, "-map", "[out]", "-t", str(total),
                    "-ar", "44100", out], check=True)

    # leccion 3: verificar que la voz esta de verdad en el archivo
    r = subprocess.run(["ffmpeg", "-i", out, "-af", "highpass=f=400,volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
    alta = float(m.group(1)) if m else -99.0
    print(f"mezcla: {len(bed)} capas de cama + {len(cfg.get('voz', []))} voces + "
          f"{len(cfg.get('pistas', []))} pistas + {len(mus)} musica + "
          f"{len(cfg.get('efectos', []))} efectos -> {out}")
    print(f"banda alta (>400 Hz): {alta:.1f} dB de media")
    if (cfg.get("voz") or cfg.get("pistas") or cfg.get("musica")) and alta < -40:
        sys.exit("FALLO: la banda de voz esta vacia. La voz no llego a la mezcla.")


if __name__ == "__main__":
    main(sys.argv[1])
