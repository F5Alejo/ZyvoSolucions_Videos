# -*- coding: utf-8 -*-
"""Une los cuatro módulos de un curso en un máster continuo.

    python tools/unir-curso.py <carpeta> <salida.mp4>

Ejemplo:

    python tools/unir-curso.py "../videos-finales/curso-ruta-segura" "Ruta Segura - completo.mp4"

Los módulos se entregan por separado porque así se consumen: uno por sesión, y
rehacer uno no obliga a rehacer el resto. El máster continuo es para quien lo
quiere de una sentada, y **se genera a partir de los módulos ya aprobados**, no
al revés.

Une sin recodificar el video: los cuatro salen del mismo codificador y comparten
perfil, resolución y cadencia. El script lo verifica antes de tocar nada y aborta
si alguno se sale.

**El audio es la parte delicada.** El concatenador exige la misma estructura de
pistas en todos los archivos, así que a los módulos que no tienen locución se les
añade una pista de silencio. Eso significa que un máster armado con módulos a
medio locutar se queda mudo a partir de ese punto — el script lo avisa por
pantalla y lo escribe en el nombre del archivo.
"""
import glob, io, os, re, subprocess, sys, tempfile


def ffprobe(ruta, entradas, seccion="stream", pista=None):
    """`pista` acota a una corriente concreta ("v:0", "a:0").

    Sin acotar, ffprobe devuelve los campos de todas las pistas y los de la de
    audio pisan a los del vídeo: un archivo con voz y otro mudo parecían tener
    perfiles distintos aunque el vídeo fuera idéntico.
    """
    cmd = ["ffprobe", "-v", "error"]
    if pista:
        cmd += ["-select_streams", pista]
    cmd += ["-show_entries", "%s=%s" % (seccion, entradas), "-of", "default=nw=1", ruta]
    return subprocess.check_output(cmd).decode("utf-8", "replace")


def perfil(ruta):
    """La firma de vídeo que tiene que coincidir entre módulos."""
    v = ffprobe(ruta, "codec_name,width,height,pix_fmt,r_frame_rate", pista="v:0")
    campos = dict(l.split("=", 1) for l in v.splitlines() if "=" in l)
    return (campos.get("codec_name"), campos.get("width"), campos.get("height"),
            campos.get("pix_fmt"), campos.get("r_frame_rate"))


def tiene_audio(ruta):
    return "audio" in ffprobe(ruta, "codec_type")


def duracion(ruta):
    return float(ffprobe(ruta, "duration", "format").split("=")[1])


def con_silencio(ruta, destino):
    """Copia el vídeo tal cual y le pega una pista de silencio de su misma duración."""
    subprocess.check_call(
        ["ffmpeg", "-v", "error", "-y", "-i", ruta,
         "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
         "-shortest", destino])


def main():
    if len(sys.argv) < 3:
        raise SystemExit("uso: python tools/unir-curso.py <carpeta> <salida.mp4>")
    carpeta, salida = sys.argv[1], sys.argv[2]

    # los módulos son los MP4 numerados; las copias livianas (…b - …) quedan fuera
    modulos = sorted((p for p in glob.glob(os.path.join(carpeta, "*.mp4"))
                      if re.match(r"^\d+ - ", os.path.basename(p))),
                     key=lambda p: int(re.match(r"^(\d+)", os.path.basename(p)).group(1)))
    if not modulos:
        raise SystemExit("no hay módulos numerados en %s" % carpeta)

    base = perfil(modulos[0])
    mudos, total = [], 0.0
    print("módulos encontrados:")
    for m in modulos:
        if perfil(m) != base:
            raise SystemExit("%s no comparte perfil de vídeo con el primero: no se puede unir "
                             "sin recodificar" % os.path.basename(m))
        d = duracion(m)
        voz = tiene_audio(m)
        total += d
        if not voz:
            mudos.append(os.path.basename(m))
        print("   %-64s %6.1f s  %s" % (os.path.basename(m)[:64], d, "con voz" if voz else "SIN VOZ"))

    tmp = tempfile.mkdtemp(prefix="unir-curso-")
    piezas = []
    for i, m in enumerate(modulos):
        if tiene_audio(m):
            piezas.append(m)
        else:
            p = os.path.join(tmp, "silencio-%02d.mp4" % i)
            con_silencio(m, p)
            piezas.append(p)

    # rutas absolutas: el concatenador las resuelve contra la carpeta de la lista
    # —que es la temporal—, no contra el directorio de trabajo
    lista = os.path.join(tmp, "lista.txt")
    io.open(lista, "w", encoding="utf-8", newline="\n").write(
        "".join("file '%s'\n" % os.path.abspath(p).replace("\\", "/") for p in piezas))
    dest = os.path.join(carpeta, salida)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                           "-i", lista, "-c", "copy", "-movflags", "+faststart", dest])

    real = duracion(dest)
    print("")
    print("%s  %.1f MB  %.2f s = %d:%02d"
          % (salida, os.path.getsize(dest) / 1e6, real, int(real // 60), int(round(real % 60))))
    if abs(real - total) > 0.5:
        print("AVISO: la suma de los módulos daba %.2f s; revisa el resultado" % total)
    if mudos:
        print("")
        print("AVISO: %d módulo(s) sin locución — el máster se queda mudo en esa parte:" % len(mudos))
        for m in mudos:
            print("   %s" % m)


if __name__ == "__main__":
    main()
