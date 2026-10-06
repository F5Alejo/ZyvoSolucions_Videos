"""La configuración del estudio: lo que se usa por defecto y cómo se produce cada video.

Vive en `datos/configuracion.json` (va a git: no tiene secretos). Lo que falta en el archivo
toma el valor de `DEFECTO`, así que agregar una opción nueva no rompe configuraciones viejas.

Cada curso puede cambiar los grupos de `POR_CURSO` en `trabajo["ajustes_video"]`: solo lo que
cambie; el resto sale de aquí.
"""

import copy
import json

from app import datos

DEFECTO = {
    "cursos": {"marca": "riskmann", "voz": "carlos", "formatos": ["16:9"], "animacion": "dinamica"},
    "video": {"resolucion": "1080p", "fps": 30, "calidad": "final", "subtitulos_quemados": False, "renderer": "playwright"},
    "tiempos": {"entrada": 1.0, "pausa": 0.35, "salida": 1.3},
    "audio": {"lufs": -14, "musica": None, "musica_volumen": -22, "respaldo_voz": True, "musica_estilo": True},
    "completo": {"tarjetas": True, "duracion_tarjeta": 3.0, "capitulos": True},
    # Cuántos trabajos corren a la vez en cada carril de la cola (motor/cola.py). Renders None: según los núcleos.
    "cola": {"render": None, "agentes": 4},
    "agentes": {
        "url": "http://localhost:11434",
        "modelo_texto": "qwen3:4b",
        "modelo_vision": "qwen3.5:2b",
        "activos": {"redactor": True, "director": True, "guionista": True, "verificador": True,
                    "evaluador": True, "publicador": True, "descriptor": True, "revisor_voz": True},
    },
}

# Los grupos que un curso puede cambiar para sí mismo.
POR_CURSO = ("video", "tiempos", "audio", "completo")

# Valores permitidos (lo que no está aquí se valida por tipo y rango en `_validar`).
OPCIONES = {
    ("video", "resolucion"): {"1080p": "1920×1080 (Full HD)", "720p": "1280×720 (más liviano)"},
    ("video", "fps"): {25: "25 fps", 30: "30 fps", 60: "60 fps (animaciones más suaves, render más lento)"},
    ("video", "calidad"): {"final": "Final (CRF 18, más lento)", "borrador": "Borrador rápido (CRF 23)"},
    ("video", "renderer"): {"playwright": "Navegador (Chromium) y ffmpeg"},
    ("audio", "lufs"): {-14: "-14 LUFS · YouTube y redes", -16: "-16 LUFS · podcast y web", -23: "-23 LUFS · TV (EBU R128)"},
}
RANGOS = {
    ("tiempos", "entrada"): (0.0, 5.0), ("tiempos", "pausa"): (0.0, 3.0), ("tiempos", "salida"): (0.3, 5.0),
    ("audio", "musica_volumen"): (-40.0, -6.0), ("completo", "duracion_tarjeta"): (1.0, 8.0),
}

RESOLUCIONES = {"1080p": 1.0, "720p": 2 / 3}  # escala sobre el lienzo de 1920×1080
CALIDADES = {"final": ("18", "medium"), "borrador": ("23", "veryfast")}


def _ruta():
    return datos.RAIZ_DATOS / "configuracion.json"


def _mezclar(base: dict, cambios: dict) -> dict:
    """Mezcla profunda: `cambios` solo pisa las claves que trae."""
    salida = copy.deepcopy(base)
    for k, v in (cambios or {}).items():
        if isinstance(v, dict) and isinstance(salida.get(k), dict):
            salida[k] = _mezclar(salida[k], v)
        else:
            salida[k] = v
    return salida


def leer() -> dict:
    ruta = _ruta()
    guardada = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    return _mezclar(DEFECTO, guardada)


def _numero(grupo: str, clave: str, valor) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"«{grupo}.{clave}» tiene que ser un número")
    minimo, maximo = RANGOS[(grupo, clave)]
    if not minimo <= valor <= maximo:
        raise ValueError(f"«{grupo}.{clave}» tiene que estar entre {minimo:g} y {maximo:g}")
    return float(valor)


def _validar(conf: dict, estricto: bool = True) -> dict:
    """Revisa tipos y valores; devuelve la configuración limpia o lanza ValueError con el motivo.

    Sin `estricto`, una pista de música que no está en este equipo se ignora en vez de fallar
    (la configuración va a git, pero la música no).
    """
    conf = _mezclar(DEFECTO, conf)
    for (grupo, clave), permitidos in OPCIONES.items():
        if conf[grupo][clave] not in permitidos:
            raise ValueError(f"«{grupo}.{clave}» no admite {conf[grupo][clave]!r}")
    for grupo, clave in RANGOS:
        conf[grupo][clave] = _numero(grupo, clave, conf[grupo][clave])
    for grupo, clave in (("video", "subtitulos_quemados"), ("completo", "tarjetas"), ("completo", "capitulos"),
                         ("audio", "respaldo_voz"), ("audio", "musica_estilo")):
        if not isinstance(conf[grupo][clave], bool):
            raise ValueError(f"«{grupo}.{clave}» tiene que ser sí o no")

    c = conf["cursos"]
    if c["marca"] not in datos.marcas():
        raise ValueError("La marca por defecto no existe")
    ids_voces = {v["id"] for v in json.loads((datos.RAIZ_DATOS / "voces.json").read_text(encoding="utf-8"))}
    if c["voz"] not in ids_voces:
        raise ValueError("La voz por defecto no existe")
    if not c["formatos"] or any(f not in ("16:9", "9:16", "1:1", "4:5") for f in c["formatos"]):
        raise ValueError("Elige al menos un formato válido")

    musica = conf["audio"]["musica"]
    if musica is not None and musica not in {m["archivo"] for m in pistas()}:
        if estricto:
            raise ValueError("Esa pista de música no está en datos/musica")
        conf["audio"]["musica"] = None

    for carril, n in conf["cola"].items():
        if carril not in DEFECTO["cola"]:
            raise ValueError(f"La cola no tiene el carril «{carril}»")
        if n is None and carril == "render":
            continue
        if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 8:
            raise ValueError(f"«cola.{carril}» tiene que ser un número entero entre 1 y 8")

    a = conf["agentes"]
    if not str(a["url"]).startswith(("http://", "https://")):
        raise ValueError("La dirección de Ollama tiene que empezar por http:// o https://")
    a["activos"] = {k: bool(a["activos"].get(k, True)) for k in DEFECTO["agentes"]["activos"]}
    return conf


def guardar(conf: dict) -> dict:
    limpia = _validar(conf)
    ruta = _ruta()
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(limpia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(ruta)
    return limpia


def para_trabajo(t: dict) -> dict:
    """La configuración con la que se produce este curso: la global más sus propios ajustes."""
    propios = {g: v for g, v in (t.get("ajustes_video") or {}).items() if g in POR_CURSO}
    return _validar(_mezclar(leer(), propios), estricto=False)


def ajustar_trabajo(t: dict, cambios: dict | None) -> dict:
    """Guarda los ajustes propios del curso (solo los grupos de POR_CURSO). None vuelve a lo global."""
    if cambios is None:
        t.pop("ajustes_video", None)
        return t
    propios = {g: v for g, v in cambios.items() if g in POR_CURSO and isinstance(v, dict)}
    _validar(_mezclar(leer(), propios))  # falla antes de guardar si algo no vale
    t["ajustes_video"] = propios
    return t


# ── Música ───────────────────────────────────────────────────────────────────

EXTENSIONES_MUSICA = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}


def carpeta_musica():
    return datos.RAIZ_DATOS / "musica"


def pistas() -> list[dict]:
    """Las pistas de `datos/musica/`, cada una con su licencia (archivo .json al lado)."""
    carpeta = carpeta_musica()
    if not carpeta.exists():
        return []
    salida = []
    for f in sorted(carpeta.iterdir()):
        if f.suffix.lower() in EXTENSIONES_MUSICA:
            info = f.with_suffix(".json")
            meta = json.loads(info.read_text(encoding="utf-8")) if info.exists() else {}
            salida.append({"archivo": f.name, "licencia": meta.get("licencia"), "fuente": meta.get("fuente"),
                           "energia": meta.get("energia")})
    return salida
