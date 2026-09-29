import json
import shutil
from pathlib import Path

import pytest

ORIGEN = Path(__file__).resolve().parent.parent / "datos"


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    """Cada prueba trabaja sobre una copia de `datos/`, nunca sobre el original."""
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos"))

    # Un repositorio de videos y unos entregables falsos, para no depender del equipo.
    repo, entregables = tmp_path / "repo", tmp_path / "entregables"
    for c in ["fegir-envivo", "sofu-comercial", "carpeta-huerfana"]:
        (repo / "videos" / c).mkdir(parents=True)
    (repo / "videos" / "fegir-envivo" / "meta.json").write_text('{"id": "fegir-envivo"}', encoding="utf-8")
    (repo / "docs").mkdir()
    (repo / "docs" / "manual.pdf").write_bytes(b"%PDF")
    (repo / "tools.py").write_text("secreto = 1", encoding="utf-8")
    (entregables / "fegir-envivo").mkdir(parents=True)
    (entregables / "fegir-envivo" / "FEGIR-En-Vivo-V4.mp4").write_bytes(b"\0" * 16)
    (tmp_path / "fuera.mp4").write_bytes(b"\0")

    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    monkeypatch.setitem(datos.CONFIG, "repo_videos", repo)
    monkeypatch.setitem(datos.CONFIG, "entregables", entregables)
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app), copia


def test_todas_las_consultas_responden(cliente):
    c, _ = cliente
    for ruta in ["/api/inicio", "/api/catalogo", "/api/proyectos", "/api/proyectos/fegir-envivo",
                 "/api/pendientes", "/api/marcas/sofu", "/api/marcas/riskmann", "/api/marcas/fegir",
                 "/api/marcas/yezid-ricaurte", "/api/casos/capacitaciones", "/api/trabajos"]:
        assert c.get(ruta).status_code == 200, ruta


def test_cada_proyecto_apunta_a_una_marca_y_estado_validos(cliente):
    from app import datos
    marcas = datos.marcas()
    ids = [p["id"] for p in datos.proyectos()]
    assert len(ids) == len(set(ids)), "ids repetidos"
    for p in datos.proyectos():
        assert p["marca"] in marcas, p["id"]
        assert p["estado"] in datos.ESTADOS, p["id"]
        assert p["familia"] in datos.FAMILIAS, p["id"]
        assert p.get("titulo"), p["id"]


def test_aprobar_deja_historial_y_quien(cliente):
    c, copia = cliente
    r = c.post("/api/proyectos/yezid-envivo-premium/estado",
               json={"estado": "aprobado", "quien": "Cliente", "nota": "Confirmado por correo"})
    assert r.status_code == 200 and r.json()["estado"] == "aprobado"
    p = next(p for p in json.loads((copia / "proyectos.json").read_text(encoding="utf-8"))
             if p["id"] == "yezid-envivo-premium")
    assert p["aprobado_por"] == "Cliente"
    assert p["historial"][-1]["de"] == "sin_estado"


def test_sin_quien_o_con_estado_inventado_no_cambia_nada(cliente):
    c, copia = cliente
    antes = (copia / "proyectos.json").read_text(encoding="utf-8")
    r = c.post("/api/proyectos/fegir-envivo/estado", json={"estado": "final", "quien": "  "})
    assert r.status_code == 400 and "quién" in r.json()["detail"]
    r = c.post("/api/proyectos/fegir-envivo/estado", json={"estado": "publicado", "quien": "X"})
    assert r.status_code == 400
    assert (copia / "proyectos.json").read_text(encoding="utf-8") == antes


def test_lo_que_no_existe_da_404(cliente):
    c, _ = cliente
    for ruta in ["/api/proyectos/no-existe", "/api/marcas/no-existe", "/api/casos/no-existe",
                 "/api/trabajos/no-existe", "/api/inventada"]:
        assert c.get(ruta).status_code == 404, ruta


def test_carpetas_sin_registrar(cliente):
    c, _ = cliente
    assert c.get("/api/proyectos").json()["sin_registrar"] == ["carpeta-huerfana"]
    assert c.get("/api/pendientes").json()["sin_registrar"] == ["carpeta-huerfana"]


def test_video_entregado_existe_y_el_que_falta_se_marca(cliente):
    c, _ = cliente
    ents = c.get("/api/proyectos/fegir-envivo").json()["entregables_detalle"]
    assert {e["archivo"]: e["existe"] for e in ents}["fegir-envivo/FEGIR-En-Vivo-V4.mp4"] is True
    assert any(not e["existe"] for e in ents)  # V2 y V3 no están en el repositorio falso
    assert c.get("/media/entregables/fegir-envivo/FEGIR-En-Vivo-V4.mp4").status_code == 200


def test_no_se_sale_de_las_carpetas_configuradas(cliente):
    c, _ = cliente
    # «..» nunca entrega el archivo de afuera (el cliente puede normalizar la ruta y caer en la interfaz).
    assert c.get("/media/entregables/../fuera.mp4").content != b"\0"
    assert c.get("/media/entregables/..%2Ffuera.mp4").status_code == 404
    assert c.get("/media/repo/docs/manual.pdf").status_code == 200
    assert c.get("/media/repo/tools.py").status_code == 404  # código: nunca se sirve


def test_el_catalogo_trae_marcas_voces_y_estados(cliente):
    c, _ = cliente
    cat = c.get("/api/catalogo").json()
    assert set(cat["marcas"]) == {"sofu", "riskmann", "fegir", "yezid-ricaurte"}
    assert cat["estados"]["final"] == "Entregado"
    assert any(v["id"] == "carlos" for v in cat["voces"])
    assert cat["pendientes_abiertos"] > 0


def test_la_paleta_de_riskmann_tiene_sus_cuatro_capas_con_fuente(cliente):
    c, _ = cliente
    m = c.get("/api/marcas/riskmann").json()
    assert set(m["capas_paleta"]) == {"manual", "logo", "web", "app"}
    for capa in m["capas_paleta"].values():
        assert capa["fuente"]
    assert {x["capa"] for x in m["paleta"]} == set(m["capas_paleta"])
