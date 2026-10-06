"""El Analizador y los PPTX de prueba de `tests/fixtures/` (generados con scripts/generar_fixtures.py)."""

from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _subir(nombre: str):
    from app import taller
    return taller.desde_pptx(f"{nombre}.pptx", (FIXTURES / f"{nombre}.pptx").read_bytes(), nombre)


@pytest.mark.parametrize("nombre,laminas", [("simple", 3), ("images", 2), ("tables", 2), ("long_text", 1),
                                            ("notes", 2), ("empty_slide", 3), ("mixed_content", 9)])
def test_cada_fixture_se_lee_y_se_analiza(datos_copia, nombre, laminas):
    from motor import analisis
    t = _subir(nombre)
    a = analisis.leer(t)
    assert a["laminas"] == laminas and a["version"] == analisis.VERSION
    assert (datos_copia / "trabajos" / t["id"] / "analisis.json").exists()  # se guarda al subir
    assert a["dificultad"] in ("básica", "media", "avanzada", "sin narración") and a["tema"]


def test_el_analizador_encuentra_tablas_graficos_imagenes_y_problemas(datos_copia):
    from motor import analisis
    a = analisis.leer(_subir("mixed_content"))
    assert a["imagenes"] == [4, 5] and a["tablas"] == [6] and a["graficos"] == [7]
    assert a["sin_notas"] == [9] and any("sin notas" in x for x in a["avisos"])
    assert {"lamina": 8, "cita": "Ley 1503 de 2011"} in a["puntos_importantes"]

    vacio = analisis.leer(_subir("empty_slide"))
    assert vacio["vacias"] == [2] and any("vacías" in x for x in vacio["avisos"])
    assert analisis.leer(_subir("long_text"))["texto_largo"] == [1]


def test_una_lamina_con_solo_una_tabla_o_un_grafico_muestra_sus_datos(datos_copia):
    from app import taller
    from motor import escenas
    t = _subir("tables")
    tabla, grafico = taller.laminas_efectivas(t)
    v = escenas.vista(tabla, 1, 2, "Video", None)
    assert v["vinetas"] == ["Exceso · Multa", "Hasta 20 km/h · 15 SMMLV", "Más de 20 km/h · 30 SMMLV"]
    assert escenas.vista(grafico, 1, 2, "Video", None)["vinetas"] == ["2022: 120", "2023: 98", "2024: 75"]


def test_el_analisis_por_la_api(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    c = TestClient(app)
    r = c.post("/api/trabajos", files={"archivo": ("x.pptx", (FIXTURES / "simple.pptx").read_bytes())}, data={"nombre": "X"})
    id_ = r.json()["id"]
    a = c.get(f"/api/trabajos/{id_}/analisis").json()
    assert a["laminas"] == 3 and a["con_notas"] == 3
    assert c.get(f"/api/trabajos/{id_}/analisis?rehacer=true").json()["laminas"] == 3
    assert c.get("/api/trabajos/no-existe/analisis").status_code == 404
