import shutil
from pathlib import Path

import pytest

ORIGEN = Path(__file__).resolve().parent.parent / "datos"


@pytest.fixture()
def datos_copia(tmp_path, monkeypatch):
    """Una copia de `datos/` (sin los cursos) para que la prueba escriba sin tocar los reales."""
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos", "empresas", "musica"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    return copia


@pytest.fixture()
def sin_ollama(monkeypatch):
    from motor.agentes import ollama
    monkeypatch.setattr(ollama, "estado", lambda: {"encendido": False, "modelos": [], "faltan": ["qwen3:4b"]})
