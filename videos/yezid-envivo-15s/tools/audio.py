# -*- coding: utf-8 -*-
"""Audio de la campaña En Vivo PESV (3 videos): voz (ElevenLabs), efectos, música, mezcla.

    set ELEVENLABS_API_KEY=sk_...          (la clave NO se guarda en el repo)
    python tools/audio.py voz              # tomas de Carlos por tramo, elige la que cabe
    python tools/audio.py sfx              # efectos a medida (ElevenLabs) -> assets/sfx/
    python tools/audio.py musica           # «Elegant» (Pixabay), la pista aprobada del evento
    python tools/audio.py mezcla           # voz + efectos + música -> assets/mezcla/adN.wav
    python tools/audio.py montar <mp4...>  # pone la mezcla en cada video (sin recodificar la imagen)
    python tools/audio.py todo <mp4...>

Decisiones:
- **Voz por tramos, no en una sola toma.** Cada tramo cae en el segundo exacto de su
  golpe visual (EXPUESTA a los 5.7 s, REGÍSTRATE HOY a los 8.0 s). Una toma continua
  deja la frase donde el modelo quiera.
- **eleven_multilingual_v2**, no v3: Carlos es una voz profesional (PVC) y ElevenLabs la
  declara optimizada para multilingual_v2 (`high_quality_base_model_ids`); en v3 pierde
  parecido. Ajustes «vendedor máximo», los que eligió el cliente en
  ENTREGABLES-VIDEO/prueba-voz-carlos (stability 0.15 · style 0.78 · speed 1.03, seed
  20260918). v2 lee las [etiquetas] en voz alta: se quitan antes de pedir el audio.
- **Cada tramo se encadena con el anterior y el siguiente** (previous_text / next_text):
  sin eso la entonación se reinicia y se nota que son cuatro tomas.
- **Varias tomas por tramo** con semillas distintas: se queda la más larga que quepa en su
  ventana (la más pausada = la más humana). Las demás quedan en assets/voz/tomas/ para oírlas.
- **Derechos**: efectos de la librería de /media-use (licencia Pixabay, uso comercial sin
  atribución) + efectos y música generados con ElevenLabs solo si el plan de la cuenta
  permite uso comercial (se comprueba). Si no, la música es síntesis propia (tools/ritmo.py).
- La voz se nivela a disco ANTES de mezclar (lección 7 de tools/mezcla.py) y el máster
  sale a -14 LUFS / -1 dBTP, el estándar de Reels, TikTok y Shorts.
"""
import base64, json, os, re, shutil, subprocess, sys, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
REPO = os.path.dirname(os.path.dirname(RAIZ))
A = lambda *p: os.path.join(RAIZ, "assets", *p)
PIXABAY = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")
API = "https://api.elevenlabs.io/v1"
CARLOS = "4PN5DHmrfIgZksvIrawS"
DUR = 15.0
TOMAS = 3
MODELO = "eleven_multilingual_v2"
# brief: estabilidad 35 % y claridad 80 % «para que suene como un experto B2B»
AJUSTES = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.45, "speed": 1.0, "use_speaker_boost": True}
SEMILLA = 20260918
GANANCIA_MUSICA = 1.0   # la música ya llega nivelada a -18 LUFS

# ─────────────────────────── guion por tramos ───────────────────────────
# Promocional de 15 s. Copy de la landing yezidricaurte.com/en-vivos/pesv-informe-autogestion/.
# PESV deletreado; cifras en palabras; «vivo» nunca cierra frase (el modelo se come la «o»).
VOZ = {
    "ad1": [
        {"id": "hook", "en": 1.00, "hasta": 4.40, "textos": [
            "Tu P-E-S-V ya está en marcha… pero falta el informe.",
            "Tu P-E-S-V está en marcha… falta el informe."]},
        {"id": "dolor", "en": 4.50, "hasta": 6.95, "textos": [
            "Inspecciones, flota, conductores… ¿y todo a mano?",
            "Inspecciones, flota, conductores… ¿a mano?"]},
        {"id": "yezid", "en": 7.00, "hasta": 11.40, "textos": [
            "El doctor Yezid Ricaurte te enseña a generarlo… con un solo clic.",
            "El doctor Yezid Ricaurte te enseña a hacerlo con un solo clic."]},
        {"id": "cta", "en": 11.50, "hasta": 14.85, "textos": [
            "Tres de octubre, ¡en vivo y gratis! Reserva tu cupo.",
            "Tres de octubre, en vivo y gratis. Reserva tu cupo."]},
    ],
}

# ─────────────────────────── efectos ───────────────────────────
EL_SFX = {
    "rafaga": ("cinematic whoosh rushing forward into a digital tunnel, deep swell into bright sparkle, short", 1.2, "px:whoosh-cinematic"),
    "golpe": ("massive cinematic trailer hit with low boom and shimmering tail, no music", 2.0, "px:impact-bass-1"),
    "glitch": ("short digital data glitch stutter, electronic, dry", 0.5, "px:glitch-1"),
    "obturador": ("camera shutter click with quick film advance, crisp", 0.5, "px:click"),
}
SFX = {"ad1": [
    {"f": "el:rafaga", "en": 0.00, "vol": 0.7},                                      # apertura: ráfaga del túnel
    {"f": "px:impact-bass-2", "en": 0.08, "dur": 1.0, "vol": 0.5},
    {"f": "px:whoosh-short", "en": 0.80, "vol": 0.35},
    {"f": "px:impact-bass-2", "en": 3.80, "dur": 1.2, "vol": 0.55},                  # «INFORME» (3.82)
    {"f": "el:glitch", "en": 4.36, "vol": 0.45},
    {"f": "el:obturador", "en": 4.38, "vol": 0.4}, {"f": "el:obturador", "en": 5.18, "vol": 0.4},
    {"f": "el:obturador", "en": 5.57, "vol": 0.4}, {"f": "el:obturador", "en": 5.87, "vol": 0.4},   # un corte por palabra
    {"f": "el:glitch", "en": 6.24, "vol": 0.4},                                      # «¿a mano?»
    {"f": "px:impact-bass-2", "en": 6.62, "dur": 0.8, "vol": 0.4},                  # la tacha
    {"f": "px:whoosh-cinematic", "en": 6.80, "dur": 1.1, "vol": 0.4},                # sube la foto
    {"f": "px:sparkle", "en": 7.60, "vol": 0.3},
    {"f": "px:whoosh", "en": 9.18, "vol": 0.3},                                      # entra la tarjeta de RiskMann
    {"f": "px:pop", "en": 10.95, "vol": 0.4},                                       # «con un solo clic»
    {"f": "px:riser", "en": 9.90, "desde": 8.45, "dur": 1.6, "vol": 0.5},             # sube hasta el 11.5
    {"f": "el:golpe", "en": 11.50, "vol": 0.95},                                     # SPECTACLE
    {"f": "px:ping", "en": 12.64, "vol": 0.25},                                      # EN VIVO
    {"f": "px:pop", "en": 13.38, "vol": 0.45},                                       # botón
    {"f": "px:sparkle", "en": 13.90, "vol": 0.3},                                    # firma
]}

# ─────────────────────────── música ───────────────────────────
# Pista enérgica generada con ElevenLabs (plan pago: uso comercial). Se pide con energía constante
# y se mide segundo a segundo: la primera tanda de RiskMann salió baja o con fade y se regeneró.
MUSICA_PROMPT = ("Loopable instrumental cinematic electronic trailer music, 128 BPM, constant high energy from the "
                 "first second to the last, no fade in, no fade out. Driving pulsing bass, tight modern drums, "
                 "tension synth arpeggios, dramatic and premium, suitable for a live event promo.")

# ─────────────────────────── utilidades ───────────────────────────
def clave():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k.startswith("sk_"):
        sys.exit("Falta ELEVENLABS_API_KEY (empieza por sk_). El ID de la clave no sirve.")
    return k


def pedir(ruta, cuerpo=None, query=""):
    req = urllib.request.Request(API + ruta + query, method="POST" if cuerpo is not None else "GET",
                                 headers={"xi-api-key": clave(), "Content-Type": "application/json"},
                                 data=json.dumps(cuerpo).encode() if cuerpo is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {ruta}: {e.read()[:400].decode(errors='replace')}")


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def duracion(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", f]).decode().strip())


def uso_comercial():
    """El plan gratuito de ElevenLabs no permite uso comercial: ahí se usan solo recursos propios/Pixabay."""
    try:
        sub = json.loads(pedir("/user/subscription"))
    except RuntimeError as e:
        # clave sin permiso user_read: una voz profesional (PVC) solo existe en planes pagos
        cat = json.loads(urllib.request.urlopen(urllib.request.Request(
            f"{API}/voices/{CARLOS}", headers={"xi-api-key": clave()}), timeout=60).read()).get("category")
        print(f"  plan no legible ({str(e)[:60]}…); voz Carlos = {cat}")
        return cat in ("professional", "cloned")
    tier = sub.get("tier", "?")
    print(f"  plan ElevenLabs: {tier} · caracteres {sub.get('character_count')}/{sub.get('character_limit')}")
    return tier not in ("free", "?")


# ─────────────────────────── voz ───────────────────────────
def limpiar_voz(src, dst, corte):
    """Corta la cabeza donde empieza la primera letra, recorta el silencio de cola y nivela
    a disco (-16 LUFS, 48 kHz): la nivelación va aquí y no en la mezcla (lección 7)."""
    # loudnorm de una pasada no llega al objetivo en clips de 1–3 s (uno quedó en -23.8 LUFS):
    # se mide el integrado y se aplica la ganancia exacta, con limitador para no saturar.
    tmp = dst + ".tmp.wav"
    ff("-i", src, "-af",
       f"atrim=start={corte:.3f},asetpts=PTS-STARTPTS,"
       "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
       "aresample=48000", "-ac", "1", tmp)
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    medido = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])
    ff("-i", tmp, "-af", f"volume={-16 - medido:.2f}dB,alimiter=limit=0.89:level=false", "-ar", "48000", dst)
    os.remove(tmp)


def toma(ad, t, n, tramos, k, texto, v):
    """Una toma pedida con marcas de tiempo por carácter.
    Devuelve (wav, duración, {palabra: segundo en que empieza dentro del wav})."""
    base = A("voz", "tomas", f"{ad}-{t['id']}-v{v + 1}-t{k + 1}")
    if not os.path.exists(base + ".json"):
        contexto = lambda xs: " ".join(x["textos"][0] for x in xs)
        cuerpo = {"text": texto, "model_id": MODELO, "seed": SEMILLA + k, "voice_settings": AJUSTES}
        if n > 0:
            cuerpo["previous_text"] = contexto(tramos[:n])
        if n < len(tramos) - 1:
            cuerpo["next_text"] = contexto(tramos[n + 1:])
        r = json.loads(pedir(f"/text-to-speech/{CARLOS}/with-timestamps", cuerpo, "?output_format=mp3_44100_192"))
        open(base + ".mp3", "wb").write(base64.b64decode(r["audio_base64"]))
        json.dump({"texto": texto, "alignment": r["alignment"]}, open(base + ".json", "w", encoding="utf-8"),
                  ensure_ascii=False)
    al = json.load(open(base + ".json", encoding="utf-8"))["alignment"]
    chars, ini = al["characters"], al["character_start_times_seconds"]
    primera = next(i for i, c in enumerate(chars) if c.strip())
    corte = max(0.0, ini[primera] - 0.03)
    limpiar_voz(base + ".mp3", base + ".wav", corte)
    palabras, actual, t0 = {}, "", 0.0
    for c, st in zip(chars + [" "], ini + [0.0]):
        if c.isalnum() or c == "-":
            if not actual:
                t0 = st
            actual += c
        elif actual:
            palabras.setdefault(actual, t0 - corte)
            actual = ""
    return base + ".wav", duracion(base + ".wav"), palabras


def voz():
    os.makedirs(A("voz", "tomas"), exist_ok=True)
    elegidas = {}
    for ad, tramos in VOZ.items():
        fin_prev = 0.0
        for n, t in enumerate(tramos):
            elegida, candidatas = None, []
            for v, texto in enumerate(t["textos"]):
                candidatas = []
                for k in range(TOMAS):
                    wav, d, pal = toma(ad, t, n, tramos, k, texto, v)
                    en = max(t["en"], fin_prev + 0.08)
                    ancla = None
                    if "ancla" in t and t["ancla"][0] in pal:
                        en = max(en, t["ancla"][1] - pal[t["ancla"][0]])
                        ancla = en + pal[t["ancla"][0]]
                    candidatas.append({"wav": wav, "dur": d, "en": en, "fin": en + d, "texto": texto, "ancla": ancla})
                caben = [c for c in candidatas if c["fin"] <= t["hasta"]]
                if caben:   # la más larga que quepa: la más pausada, la más humana
                    elegida = dict(max(caben, key=lambda c: c["dur"]), tempo=1.0)
                    break
                durs = ", ".join(f"{c['dur']:.2f}" for c in candidatas)
                print(f"    {ad} {t['id']}: «{texto}» no cabe (tomas {durs} s)")
            dst = A("voz", f"{ad}-{t['id']}.wav")
            if elegida is None:   # último recurso: la más corta del último texto, acelerada hasta 1.12
                c = min(candidatas, key=lambda c: c["dur"])
                tempo = min(1.12, c["dur"] / max(0.3, t["hasta"] - c["en"]))
                ff("-i", c["wav"], "-af", f"atempo={tempo:.3f}", dst)
                elegida = dict(c, tempo=tempo, dur=duracion(dst))
                elegida["fin"] = elegida["en"] + elegida["dur"]
            else:
                shutil.copy(elegida["wav"], dst)
            fin_prev = elegida["fin"]
            ok = "OK" if elegida["fin"] <= t["hasta"] + 0.02 else "NO CABE"
            ancla = f"  «{t['ancla'][0]}» en {elegida['ancla']:.2f}s" if elegida.get("ancla") else ""
            print(f"  {ad} {t['id']:8s} {elegida['en']:5.2f}→{elegida['fin']:5.2f}s (≤{t['hasta']:.2f})  "
                  f"tempo {elegida['tempo']:.2f}  «{elegida['texto']}»{ancla}  {ok}")
            elegidas[f"{ad}-{t['id']}"] = {"archivo": os.path.relpath(dst, RAIZ), "en": round(elegida["en"], 3),
                                           "fin": round(elegida["fin"], 3), "texto": elegida["texto"],
                                           "tempo": round(elegida["tempo"], 3)}
    json.dump(elegidas, open(A("voz", "elegidas.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)


# ─────────────────────────── efectos ───────────────────────────
def sfx(comercial=None):
    os.makedirs(A("sfx"), exist_ok=True)
    if comercial is None:
        comercial = uso_comercial()
    for nombre, (prompt, dur, respaldo) in EL_SFX.items():
        dst = A("sfx", nombre + ".mp3")
        if os.path.exists(dst):
            continue
        if comercial:
            try:
                open(dst, "wb").write(pedir("/sound-generation", {
                    "text": prompt, "duration_seconds": dur, "prompt_influence": 0.6}))
                print(f"  sfx {nombre}: ElevenLabs ({dur}s)")
                continue
            except RuntimeError as e:
                print(f"  sfx {nombre}: ElevenLabs falló ({e}); uso respaldo")
        if nombre == "reloj":   # tic-tac propio con el clic de Pixabay, cada 0.25 s
            ff("-i", os.path.join(PIXABAY, "click-soft.mp3"), "-filter_complex", _ticks(),
               "-map", "[o]", "-t", "2.6", dst)
        else:
            shutil.copy(os.path.join(PIXABAY, respaldo[3:] + ".mp3"), dst)
        print(f"  sfx {nombre}: respaldo Pixabay")


def _ticks():
    n = 10
    partes = [f"[0:a]asplit={n}" + "".join(f"[s{i}]" for i in range(n))]
    for i in range(n):
        ms = i * 250
        partes.append(f"[s{i}]volume={0.75 if i % 2 else 1.0},adelay={ms}|{ms}[t{i}]")
    partes.append("".join(f"[t{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0[o]")
    return ";".join(partes)


# ─────────────────────────── música ───────────────────────────
OPCIONES_MUSICA = ("eleven",)


def musica(comercial=None, forzar=False):
    os.makedirs(A("musica"), exist_ok=True)
    dst = A("musica", "ad1-eleven.wav")
    if os.path.exists(dst) and not forzar:
        return
    mp3 = A("musica", "ad1-eleven.mp3")
    open(mp3, "wb").write(pedir("/sound-generation", {"text": MUSICA_PROMPT, "duration_seconds": DUR,
                                                      "prompt_influence": 0.55, "loop": True}))
    ff("-i", mp3, "-af", f"aresample=48000,apad,atrim=0:{DUR}", "-ac", "2", dst)
    print("  música: ElevenLabs →", curva(dst))


def curva(f):
    """Volumen segundo a segundo (LUFS de 1 s): delata pistas flojas o que se apagan."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=metadata=1,ametadata=print:key=lavfi.r128.M",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    m = [float(x) for x in re.findall(r"lavfi\.r128\.M=(-?[\d.]+)", out)]
    return " ".join(f"{m[min(len(m) - 1, i * 10 + 9)]:.0f}" for i in range(int(DUR)))


# ─────────────────────────── mezcla ───────────────────────────
def archivo_sfx(ref):
    kind, name = ref.split(":", 1)
    return A("sfx", name + ".mp3") if kind == "el" else os.path.join(PIXABAY, name + ".mp3")


def mezcla(con_voz=True, con_sfx=True, con_musica=True, sufijo="", opcion="eleven"):
    os.makedirs(A("mezcla"), exist_ok=True)
    elegidas = json.load(open(A("voz", "elegidas.json"), encoding="utf-8")) if con_voz else {}
    PAD = f"apad,atrim=0:{DUR}"
    for ad in VOZ:
        ins, fl, voces, efectos = [], [], [], []
        i = 0
        if con_voz:
            for t in VOZ[ad]:
                v = elegidas[f"{ad}-{t['id']}"]
                ins += ["-i", os.path.join(RAIZ, v["archivo"])]
                ms = int(v["en"] * 1000)
                g = 1.33 if t["id"] == "cta" else 1.0   # +2.5 dB: el cierre es lo que más tiene que entenderse
                fl.append(f"[{i}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume={g},adelay={ms}|{ms},{PAD}[v{i}]")
                voces.append(f"[v{i}]"); i += 1
        if con_sfx:
            for s in SFX[ad]:
                ins += ["-i", archivo_sfx(s["f"])]
                ms = int(s["en"] * 1000)
                recorte = f"atrim={s.get('desde', 0)}:{s.get('desde', 0) + s['dur']},asetpts=PTS-STARTPTS," if "dur" in s \
                    else (f"atrim=start={s['desde']},asetpts=PTS-STARTPTS," if "desde" in s else "")
                cola = f"afade=t=out:st={max(0, s['dur'] - 0.15)}:d=0.15," if "dur" in s else ""
                fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{recorte}{cola}"
                          f"volume={s['vol']},adelay={ms}|{ms},{PAD}[s{i}]")
                efectos.append(f"[s{i}]"); i += 1
        mus = None
        if con_musica:
            # cada candidata se nivela a disco a -18 LUFS: así las opciones se comparan en igualdad
            crudo, nivelado = A("musica", f"{ad}-{opcion}.wav"), A("musica", f"{ad}-{opcion}-n.wav")
            if not os.path.exists(nivelado):
                ff("-i", crudo, "-af", "loudnorm=I=-18:TP=-2:LRA=11,aresample=48000", "-ar", "48000", nivelado)
            ins += ["-i", nivelado]
            # hueco de -4 dB en 2 kHz: ahí vive la inteligibilidad de la voz (lección 5)
            fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=60,"
                      f"equalizer=f=2000:width_type=o:w=1.5:g=-4,"
                      f"afade=t=out:st={DUR - 0.6}:d=0.6,volume={GANANCIA_MUSICA},{PAD}[m]")
            mus = "[m]"; i += 1

        salidas, stems = [], []
        if voces:
            fl.append("".join(voces) + f"amix=inputs={len(voces)}:normalize=0,asplit=3[vz][key][st_voz]")
            salidas.append("[vz]"); stems.append("voz")
        if efectos:
            fl.append("".join(efectos) + f"amix=inputs={len(efectos)}:normalize=0[fx]")
            salidas.append("[fx]")
        if mus:
            if voces:  # la música se aparta ~5 dB cuando habla Carlos, no desaparece
                fl.append(f"{mus}[key]sidechaincompress=threshold=0.04:ratio=4:attack=12:release=280[mdk]")
                fl.append("[mdk]asplit=2[md][st_musica]")
                salidas.append("[md]"); stems.append("musica")
            else:
                salidas.append(mus)
        fl.append("".join(salidas) + f"amix=inputs={len(salidas)}:normalize=0,alimiter=limit=0.95[pre]")
        tmp = A("mezcla", f"{ad}{sufijo}-pre.wav")
        salida_stems = []
        for st in stems:
            salida_stems += ["-map", f"[st_{st}]", "-ar", "48000", "-t", str(DUR), A("mezcla", f"{ad}{sufijo}-stem-{st}.wav")]
        ff(*ins, "-filter_complex", ";".join(fl), "-map", "[pre]", "-ar", "48000", "-t", str(DUR), tmp, *salida_stems)
        dst = A("mezcla", f"{ad}{sufijo}.wav")
        ff("-i", tmp, "-af", "loudnorm=I=-14:TP=-1:LRA=9,aresample=48000", "-ar", "48000", "-t", str(DUR), dst)
        os.remove(tmp)
        print(f"  mezcla {ad}{sufijo}: {medir(dst)}")
        if len(stems) == 2:
            print("    " + margen(ad, sufijo, elegidas))


def margen(ad, sufijo, elegidas):
    """Voz sobre música, frase por frase (dB). Menos de 8 dB y la voz se empieza a tapar."""
    import numpy as np
    carga = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "f32le", "-ac", "1", "-"],
                                                   capture_output=True).stdout, dtype=np.float32)
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    vz, mu = carga(A("mezcla", f"{ad}{sufijo}-stem-voz.wav")), carga(A("mezcla", f"{ad}{sufijo}-stem-musica.wav"))
    partes, peor = [], 99
    for k, v in elegidas.items():
        if k.startswith(ad + "-"):
            a, b = int(v["en"] * 48000), int(v["fin"] * 48000)
            m = db(vz[a:b]) - db(mu[a:b]); peor = min(peor, m)
            partes.append(f"{k.split('-', 1)[1]} {m:+.1f}")
    return f"voz sobre música: {' · '.join(partes)} dB  → {'OK' if peor >= 8 else 'VOZ TAPADA'}"


def medir(f):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)
    bands = []
    for lo, hi in ((20, 250), (250, 4000), (4000, 16000)):
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", f"bandpass=f={(lo * hi) ** 0.5:.0f}:width_type=h:w={hi - lo},"
                            "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.search(r"mean_volume: (-?[\d.]+) dB", o)
        bands.append(m.group(1) if m else "?")
    return f"{i[-1] if i else '?'} LUFS · pico {p[-1] if p else '?'} dBTP · graves/medios/agudos {'/'.join(bands)} dB"


# ─────────────────────────── montaje ───────────────────────────
def montar(videos, sufijo=""):
    for v in videos:
        ad = "ad" + re.search(r"AD(\d)", os.path.basename(v)).group(1)
        mix = A("mezcla", f"{ad}{sufijo}.wav")
        dst = v.replace("_mudo" + os.sep, "").replace("_mudo/", "")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        ff("-i", v, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-ar", "48000", "-shortest", "-movflags", "+faststart", dst)
        print("  →", dst)


if __name__ == "__main__":
    paso = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if paso == "voz":
        voz()
    elif paso == "sfx":
        sfx()
    elif paso == "musica":
        musica()
    elif paso == "mezcla":
        mezcla()
    elif paso == "montar":
        montar(sys.argv[2:])
    elif paso == "todo":
        com = uso_comercial()
        voz(); sfx(com); musica(com); mezcla(); montar(sys.argv[2:])
    else:
        sys.exit(__doc__)
