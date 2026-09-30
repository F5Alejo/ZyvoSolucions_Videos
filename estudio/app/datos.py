"""Lectura y escritura de los datos del panel.

El registro (marca, estado, historial) vive en `datos/`. El repositorio de videos y la
carpeta de entregables se leen de disco **en solo lectura**; sus rutas salen de
`config.local.json` o de las variables REPO_VIDEOS y ENTREGABLES.
"""

import json
import os
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAIZ_DATOS = Path(os.environ.get("INTERFAZ_DATOS", RAIZ / "datos"))


def _config() -> dict:
    """Rutas del repositorio de videos y de los entregables.

    El estudio vive en `estudio/` dentro del repositorio de videos, así que lo encuentra solo en la
    carpeta de arriba. `config.local.json` y las variables de entorno mandan sobre eso.
    Las rutas relativas se toman desde la carpeta del estudio.
    """
    conf = {"repo_videos": ".."} if (RAIZ.parent / "videos").is_dir() else {}
    ruta = RAIZ / "config.local.json"
    if ruta.exists():
        conf.update(json.loads(ruta.read_text(encoding="utf-8")))
    for clave, var in (("repo_videos", "REPO_VIDEOS"), ("entregables", "ENTREGABLES")):
        if os.environ.get(var):
            conf[clave] = os.environ[var]
    rutas = {k: (RAIZ / v).resolve() for k, v in conf.items() if v}
    return {k: v for k, v in rutas.items() if v.is_dir()}


CONFIG = _config()


def ruta_segura(raiz_clave: str, relativa: str) -> Path | None:
    """Resuelve `relativa` dentro de una raíz configurada; None si sale de ella o no existe."""
    raiz = CONFIG.get(raiz_clave)
    if raiz is None:
        return None
    raiz = raiz.resolve()
    ruta = (raiz / relativa).resolve()
    if not ruta.is_relative_to(raiz) or not ruta.is_file():
        return None
    return ruta


def carpetas_videos() -> dict[str, dict]:
    """Las carpetas de `videos/` del repositorio, con su meta.json si lo tienen."""
    raiz = CONFIG.get("repo_videos")
    if raiz is None or not (raiz / "videos").is_dir():
        return {}
    salida = {}
    for d in sorted((raiz / "videos").iterdir()):
        if d.is_dir():
            meta = d / "meta.json"
            salida[d.name] = json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else None
    return salida


def sin_registrar() -> list[str]:
    """Carpetas del repositorio que ningún proyecto del panel reclama."""
    reclamadas = {c for p in proyectos() for c in p.get("carpetas", [p["id"]])}
    return [c for c in carpetas_videos() if c not in reclamadas]

# Estados de PLATAFORMA.md tarea 0.6, más `sin_estado` para lo que el maestro marca ⚠.
ESTADOS = {
    "sin_estado": "Sin estado",
    "borrador": "Borrador",
    "revision": "En revisión",
    "aprobado": "Aprobado",
    "final": "Entregado",
    "archivado": "Archivado",
}
FAMILIAS = {"A": "Curso", "B": "Marketing"}


def _leer(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def marcas() -> dict[str, dict]:
    todas = (_leer(r) for r in sorted((RAIZ_DATOS / "marcas").glob("*.json")))
    return {m["id"]: m for m in todas}


def proyectos() -> list[dict]:
    return _leer(RAIZ_DATOS / "proyectos.json")


def proyecto(id_: str) -> dict | None:
    """Un proyecto, con lo que se sabe de sus carpetas y entregables en disco."""
    p = next((p for p in proyectos() if p["id"] == id_), None)
    if p is None:
        return None
    en_repo = carpetas_videos()
    p["carpetas_detalle"] = [
        {"nombre": c, "existe": c in en_repo, "meta": en_repo.get(c)} for c in p.get("carpetas", [p["id"]])
    ]
    p["entregables_detalle"] = [
        {**e, "existe": ruta_segura("entregables", e["archivo"]) is not None} for e in p.get("entregables", [])
    ]
    return p


def cambiar_estado(id_: str, estado: str, quien: str, nota: str = "") -> dict:
    """Cambia el estado de un proyecto y lo anota en su historial. Nada se borra."""
    if estado not in ESTADOS:
        raise ValueError(f"Estado desconocido: {estado}")
    quien = quien.strip()
    if not quien:
        raise ValueError("Hace falta saber quién hace el cambio")

    lista = proyectos()
    p = next((p for p in lista if p["id"] == id_), None)
    if p is None:
        raise KeyError(id_)

    hoy = date.today().isoformat()
    p.setdefault("historial", []).append(
        {"fecha": hoy, "de": p["estado"], "a": estado, "quien": quien, "nota": nota.strip()}
    )
    p["estado"] = estado
    if estado == "aprobado":
        p["aprobado_por"], p["aprobado_el"] = quien, hoy

    ruta = RAIZ_DATOS / "proyectos.json"
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(json.dumps(lista, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporal.replace(ruta)
    return p


def pendientes() -> list[dict]:
    """Todos los pendientes y peticiones al cliente de las fichas, con su marca."""
    salida = []
    for m in marcas().values():
        for tipo, clave in (("Pendiente", "pendientes"), ("Pedir al cliente", "pedir_al_cliente")):
            for item in m.get(clave, []):
                salida.append({**item, "marca": m, "tipo": tipo})
    return salida
