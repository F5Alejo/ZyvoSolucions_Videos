# -*- coding: utf-8 -*-
"""Sonido de fegir-envivo: musica y efectos propios (ElevenLabs), mezcla con la
voz de Carlos y verificacion. Nada heredado de la serie de Yezid.

    python tools/audio.py musica     # pide la cama (una vez; se guarda)
    python tools/audio.py sfx        # pide los efectos (una vez; se guardan)
    python tools/audio.py mezcla     # voz + efectos + cama -> assets/mezcla.wav
    python tools/audio.py            # todo lo que falte

La clave se lee del entorno o de ~/.elevenlabs-key.txt, nunca del repositorio.
Los instantes salen de la misma tabla que usa index.html (V y T).
"""
import io, json, os, re, subprocess, sys, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
A = lambda *p: os.path.join(RAIZ, "assets", *p)
FIN = 19.5

# inicio de cada toma en la mezcla — igual que V en index.html
V = {1: 0.30, 2: 3.75, 3: 7.05, 4: 10.45, 5: 13.70, 6: 16.20}
CORT = 0.40

MUSICA_PROMPT = ("Bright, hopeful and modern corporate background music for a safety foundation "
                 "announcement. 104 BPM, warm piano and clean guitar plucks, light claps and soft "
                 "kick, uplifting and positive, confident but calm, no vocals, instrumental only.")

# efecto: (prompt, duracion, instantes)
SFX = {
    "cortina": ("smooth soft whoosh swipe transition, airy, short, clean, no music", 1.0,
                [V[2] - CORT, V[3] - CORT, V[4] - CORT, V[5] - CORT]),
    "visto":   ("quick marker pen check mark stroke swoosh on paper, crisp, no music", 0.8,
                [V[3] + 0.05]),
    "pop":     ("soft bubbly UI pop, friendly, short, no music", 0.5,
                [V[2] + 1.42 + 0.55, V[3] + 1.85, V[5] + 0.15]),
    "golpe":   ("warm deep cinematic low hit with short tail, subtle, no music", 1.5,
                [V[2] + 1.42]),
    "hoja":    ("calendar paper page flip and soft landing, no music", 0.9,
                [V[4] + 0.1]),
    "brillo":  ("gentle magical shimmer chime for a logo reveal, bright, short, no music", 1.6,
                [V[6] - 0.10]),
}
GAN_SFX = {"cortina": 0.35, "visto": 0.45, "pop": 0.40, "golpe": 0.55, "hoja": 0.45, "brillo": 0.40}


def clave():
    k = os.environ.get("ELEVENLABS_API_KEY")
    f = os.path.join(os.path.expanduser("~"), ".elevenlabs-key.txt")
    if not k and os.path.isfile(f):
        k = io.open(f, encoding="utf-8-sig").read().strip()
    if not k:
        raise SystemExit("falta la clave de ElevenLabs")
    return k


def pedir(ruta, cuerpo):
    req = urllib.request.Request("https://api.elevenlabs.io/v1" + ruta, method="POST",
                                 data=json.dumps(cuerpo).encode("utf-8"),
                                 headers={"xi-api-key": clave(), "Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=600).read()
    except urllib.error.HTTPError as e:
        raise RuntimeError("ElevenLabs %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def musica():
    os.makedirs(A("musica"), exist_ok=True)
    dst = A("musica", "cama.mp3")
    if os.path.isfile(dst):
        return print("musica: ya existe", dst)
    try:
        # Eleven Music: pista completa a la medida del video
        data = pedir("/music", {"prompt": MUSICA_PROMPT, "music_length_ms": int(FIN * 1000) + 1000})
        origen = "eleven-music"
    except RuntimeError as e:
        print("  /music no disponible (%s); se usa sound-generation en bucle" % e)
        data = pedir("/sound-generation", {"text": MUSICA_PROMPT, "duration_seconds": 22,
                                            "prompt_influence": 0.55, "loop": True})
        origen = "sound-generation"
    open(dst, "wb").write(data)
    io.open(A("musica", "ORIGEN.txt"), "w", encoding="utf-8").write(
        "cama.mp3 generada con ElevenLabs (%s)\nprompt: %s\n" % (origen, MUSICA_PROMPT))
    print("musica:", origen, "->", dst)


def sfx():
    os.makedirs(A("sfx"), exist_ok=True)
    for n, (prompt, dur, _) in SFX.items():
        dst = A("sfx", n + ".mp3")
        if os.path.isfile(dst):
            continue
        open(dst, "wb").write(pedir("/sound-generation", {"text": prompt, "duration_seconds": dur,
                                                           "prompt_influence": 0.6}))
        print("sfx:", n)


def integrado(f):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def nivelar(src, dst, lufs):
    # loudnorm de una pasada no llega al objetivo en clips de 1-3 s: se mide y se
    # aplica la ganancia exacta que falta
    ff("-i", src, "-af", "aresample=48000", "-ac", "2", "-ar", "48000", dst + ".tmp.wav")
    g = lufs - integrado(dst + ".tmp.wav")
    ff("-i", dst + ".tmp.wav", "-af", "volume=%.2fdB,alimiter=limit=0.89" % g, "-ar", "48000", dst)
    os.remove(dst + ".tmp.wav")


def mezcla():
    os.makedirs(A("mezcla"), exist_ok=True)
    ent, fl, voces, efectos = [], [], [], []
    # voz: cada toma nivelada por separado para que ninguna frase quede floja
    for n, t in V.items():
        nv = A("mezcla", "voz-%d.wav" % n)
        nivelar(A("voz", "f%02d.mp3" % n), nv, -16)
        ent += ["-i", nv]
        i = len(ent) // 2 - 1
        fl.append("[%d]adelay=%d:all=1[v%d]" % (i, t * 1000, n))
        voces.append("[v%d]" % n)
    k = 0
    for n, (_, _, ts) in SFX.items():
        for t in ts:
            ent += ["-i", A("sfx", n + ".mp3")]
            i = len(ent) // 2 - 1
            fl.append("[%d]aformat=channel_layouts=stereo,aresample=48000,volume=%s,adelay=%d:all=1[s%d]"
                      % (i, GAN_SFX[n], t * 1000, k))
            efectos.append("[s%d]" % k); k += 1
    ent += ["-i", A("musica", "cama.mp3")]
    im = len(ent) // 2 - 1
    fl.append("[%d]aformat=channel_layouts=stereo,aresample=48000,atrim=0:%s,"
              "afade=t=in:d=0.4,afade=t=out:st=%s:d=1.6,volume=0.30[mus]" % (im, FIN, FIN - 1.6))
    fl.append("%samix=inputs=%d:normalize=0[voz]" % ("".join(voces), len(voces)))
    fl.append("[voz]asplit=2[vozm][key]")
    # la cama baja cuando habla Carlos
    fl.append("[mus][key]sidechaincompress=threshold=0.04:ratio=5:attack=10:release=320[musd]")
    fl.append("%samix=inputs=%d:normalize=0[fx]" % ("".join(efectos), len(efectos)))
    fl.append("[vozm][fx][musd]amix=inputs=3:normalize=0,highpass=f=60,apad,atrim=0:%s[out]" % FIN)
    tmp = A("mezcla", "premezcla.wav")
    ff(*ent, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", tmp)
    dst = A("mezcla.wav")
    ff("-i", tmp, "-af", "loudnorm=I=-14:TP=-1:LRA=9,aresample=48000", "-ar", "48000", "-t", str(FIN), dst)
    print("mezcla ->", dst)
    print(medir(dst))


def medir(f):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1]
    bandas = []
    for filtro in ("lowpass=f=200", "highpass=f=400"):
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", filtro + ",volumedetect", "-f", "null", "-"],
                           capture_output=True, text=True, errors="replace").stderr
        bandas.append(re.findall(r"mean_volume: (-?[\d.]+) dB", o)[-1])
    return "%s LUFS · pico %s dBTP · graves(<200) %s dB · voz(>400) %s dB" % (i, p, bandas[0], bandas[1])


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso in ("musica", "todo"):
        musica()
    if paso in ("sfx", "todo"):
        sfx()
    if paso in ("mezcla", "todo"):
        mezcla()
