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


def test_todas_las_paginas_cargan(cliente):
    c, _ = cliente
    for ruta in ["/proyectos", "/proyectos?marca=fegir&estado=final", "/pendientes",
                 "/pendientes?ver=todos", "/proyectos/fegir-envivo",
                 "/marcas/sofu", "/marcas/riskmann", "/marcas/fegir", "/marcas/yezid-ricaurte"]:
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


def test_filtro_por_marca(cliente):
    c, _ = cliente
    html = c.get("/proyectos?marca=sofu").text
    assert "sofu-comercial-v2" in html
    assert "fegir-envivo" not in html


def test_aprobar_deja_historial_y_quien(cliente):
    c, copia = cliente
    r = c.post("/proyectos/yezid-envivo-premium/estado",
               data={"estado": "aprobado", "quien": "Cliente", "nota": "Confirmado por correo"},
               follow_redirects=False)
    assert r.status_code == 303
    p = next(p for p in json.loads((copia / "proyectos.json").read_text(encoding="utf-8"))
             if p["id"] == "yezid-envivo-premium")
    assert p["estado"] == "aprobado"
    assert p["aprobado_por"] == "Cliente"
    assert p["historial"][-1]["de"] == "sin_estado"


def test_sin_quien_no_cambia_nada(cliente):
    c, copia = cliente
    antes = (copia / "proyectos.json").read_text(encoding="utf-8")
    r = c.post("/proyectos/fegir-envivo/estado", data={"estado": "final", "quien": "  "},
               follow_redirects=False)
    assert r.status_code == 303 and "error=" in r.headers["location"]
    assert (copia / "proyectos.json").read_text(encoding="utf-8") == antes


def test_estado_inventado_se_rechaza(cliente):
    c, copia = cliente
    antes = (copia / "proyectos.json").read_text(encoding="utf-8")
    c.post("/proyectos/fegir-envivo/estado", data={"estado": "publicado", "quien": "X"})
    assert (copia / "proyectos.json").read_text(encoding="utf-8") == antes


def test_proyecto_inexistente_da_404(cliente):
    c, _ = cliente
    assert c.get("/proyectos/no-existe").status_code == 404
    assert c.get("/marcas/no-existe").status_code == 404


def test_carpetas_sin_registrar(cliente):
    c, _ = cliente
    from app import datos
    assert datos.sin_registrar() == ["carpeta-huerfana"]
    assert "carpeta-huerfana" in c.get("/pendientes").text


def test_video_entregado_se_ve_y_el_que_falta_se_avisa(cliente):
    c, _ = cliente
    html = c.get("/proyectos/fegir-envivo").text
    assert 'src="/media/entregables/fegir-envivo/FEGIR-En-Vivo-V4.mp4#t=3"' in html
    assert "No encontramos este archivo" in html  # V2 y V3 no están en el repositorio falso
    assert c.get("/media/entregables/fegir-envivo/FEGIR-En-Vivo-V4.mp4").status_code == 200


def test_no_se_sale_de_las_carpetas_configuradas(cliente):
    c, _ = cliente
    assert c.get("/media/entregables/../fuera.mp4").status_code == 404
    assert c.get("/media/entregables/..%2Ffuera.mp4").status_code == 404
    assert c.get("/media/repo/docs/manual.pdf").status_code == 200
    assert c.get("/media/repo/tools.py").status_code == 404  # código: nunca se sirve


def test_botones_de_siguiente_paso_y_nombre_legible(cliente):
    c, copia = cliente
    html = c.get("/proyectos/yezid-envivo-premium").text
    assert "Campaña premium" in html                      # nombre legible, no el identificador
    assert 'name="estado" value="revision"' in html       # sin estado → enviar a revisión
    r = c.post("/proyectos/yezid-envivo-premium/estado", data={"estado": "revision", "quien": "Ana"}, follow_redirects=False)
    assert r.headers["location"].endswith("?ok=estado")
    html = c.get("/proyectos/yezid-envivo-premium").text
    assert ">Aprobar<" in html


def test_menu_marca_la_pagina_actual_y_cuenta_pendientes(cliente):
    c, _ = cliente
    html = c.get("/proyectos").text
    assert '<a href="/proyectos" aria-current="page">Videos</a>' in html
    assert 'class="insignia"' in html
