import io
import json
import shutil
from pathlib import Path

import pytest
from PIL import Image

from tests.test_taller import pptx_de_prueba

ORIGEN = Path(__file__).resolve().parent.parent / "datos"


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos", "empresas", "musica", "bancos", "cache", "*.mp4"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    from fastapi.testclient import TestClient

    from app.main import app
    return TestClient(app), copia


def logo_png(colores=((200, 30, 40), (20, 60, 160)), fondo=(255, 255, 255, 0)) -> bytes:
    """Un logo de prueba: dos bloques de color sobre fondo transparente."""
    im = Image.new("RGBA", (200, 100), fondo)
    for i, c in enumerate(colores):
        im.paste(c + (255,), (i * 100 + 10, 10, i * 100 + 90, 90))
    b = io.BytesIO()
    im.save(b, "PNG")
    return b.getvalue()


def registrar(c, logo: bytes | None = logo_png(), **campos):
    datos = {"nombre": "Transportes del Llano S.A.S.", "nombre_corto": "Transllano", "colores": ["#C81E28", "#143CA0"], **campos}
    files = {"logo": ("logo.png", logo, "image/png")} if logo else None
    return c.post("/api/empresas", data={"datos": json.dumps(datos)}, files=files)


def test_propone_los_colores_del_logo_sin_el_fondo(cliente):
    c, _ = cliente
    r = c.post("/api/empresas/colores", files={"logo": ("l.png", logo_png(fondo=(255, 255, 255, 255)), "image/png")})
    colores = r.json()["colores"]
    assert "#FFFFFF" not in colores
    assert len(colores) == 2
    assert any(int(h[1:3], 16) > 150 and int(h[5:7], 16) < 90 for h in colores)   # el rojo
    assert any(int(h[5:7], 16) > 120 and int(h[1:3], 16) < 60 for h in colores)   # el azul


def test_registrar_una_empresa_la_deja_lista_para_usar(cliente):
    c, copia = cliente
    r = registrar(c, que_es="Transporte de carga", sitio_web="https://transllano.com/", voz="carlos")
    assert r.status_code == 201, r.text
    m = r.json()
    assert m["id"] == "transllano" and m["registrada"] is True
    assert m["dominio"] == "transllano.com"
    assert [x["hex"] for x in m["paleta"]] == ["#C81E28", "#143CA0"]
    assert m["logo_url"] == "/media/empresas/transllano.png"
    # Aparece donde se elige la marca
    assert "transllano" in c.get("/api/catalogo").json()["marcas"]
    assert any(e["id"] == "transllano" for e in c.get("/api/empresas").json())
    assert c.get("/api/marcas/transllano").status_code == 200
    # El logo se sirve re-codificado en PNG, y vive fuera de las marcas base
    logo = c.get(m["logo_url"])
    assert logo.status_code == 200 and logo.content[:8] == b"\x89PNG\r\n\x1a\n"
    assert (copia / "empresas" / "transllano.json").exists()
    assert not (copia / "marcas" / "transllano.json").exists()


def test_dos_empresas_con_el_mismo_nombre_no_se_pisan(cliente):
    c, _ = cliente
    assert registrar(c).json()["id"] == "transllano"
    assert registrar(c).json()["id"] == "transllano-2"
    assert registrar(c, nombre_corto="RiskMann").json()["id"] == "riskmann-2"  # no choca con la marca base


@pytest.mark.parametrize("campos, mensaje", [
    ({"nombre": " "}, "nombre"),
    ({"colores": []}, "al menos un color"),
    ({"colores": ["#12345"]}, "no es válido"),
    ({"colores": ["#111111"] * 7}, "máximo 6"),
    ({"sitio_web": "no es un sitio"}, "sitio web"),
    ({"voz": "inventada"}, "voz"),
    ({"nombre_corto": "x" * 30}, "nombre corto"),
])
def test_valida_lo_que_escribe_la_persona(cliente, campos, mensaje):
    c, copia = cliente
    r = registrar(c, **campos)
    assert r.status_code == 400 and mensaje in r.json()["detail"]
    assert not (copia / "empresas").exists() or not list((copia / "empresas").glob("*.json"))


@pytest.mark.parametrize("contenido", [b"no soy una imagen", b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'])
def test_solo_acepta_imagenes_de_verdad_como_logo(cliente, contenido):
    c, _ = cliente
    r = registrar(c, logo=contenido)
    assert r.status_code == 400 and "PNG, JPG o WebP" in r.json()["detail"]


def test_sin_logo_tambien_se_puede_registrar(cliente):
    c, _ = cliente
    r = registrar(c, logo=None)
    assert r.status_code == 201 and r.json()["logo_url"] is None


def test_editar_y_proteger_las_marcas_base(cliente):
    c, _ = cliente
    registrar(c)
    r = c.put("/api/empresas/transllano", data={"datos": json.dumps({"nombre": "Transllano", "colores": ["#000000"], "cta": "Escríbenos"})})
    assert r.status_code == 200 and r.json()["cta"] == "Escríbenos" and r.json()["paleta"][0]["hex"] == "#000000"
    assert r.json()["logo_url"] == "/media/empresas/transllano.png"  # sin logo nuevo, conserva el que tenía
    base = c.put("/api/empresas/riskmann", data={"datos": json.dumps({"nombre": "X", "colores": ["#000000"]})})
    assert base.status_code == 400
    assert c.delete("/api/empresas/riskmann").status_code == 400
    assert c.put("/api/empresas/no-existe", data={"datos": json.dumps({"nombre": "X", "colores": ["#000000"]})}).status_code == 404


def test_un_curso_nuevo_toma_la_marca_y_la_voz_de_la_empresa(cliente):
    c, _ = cliente
    registrar(c, voz="juan")
    r = c.post("/api/trabajos", files={"archivo": ("c.pptx", pptx_de_prueba())}, data={"marca": "transllano"})
    t = c.get(f"/api/trabajos/{r.json()['id']}").json()["trabajo"]
    assert t["marca"] == "transllano" and t["voz"] == "juan"
    # En uso: no se puede eliminar
    r = c.delete("/api/empresas/transllano")
    assert r.status_code == 400 and "curso" in r.json()["detail"]


def test_eliminar_una_empresa_sin_uso(cliente):
    c, copia = cliente
    registrar(c)
    assert c.delete("/api/empresas/transllano").status_code == 204
    assert "transllano" not in c.get("/api/catalogo").json()["marcas"]
    assert not (copia / "empresas" / "logos" / "transllano.png").exists()


def test_los_logos_no_se_salen_de_su_carpeta(cliente):
    c, _ = cliente
    registrar(c)
    # «..» nunca entrega un archivo de afuera. La ruta cae en la aplicación Vue: index.html si el
    # frontend está compilado, y un 503 si no lo está (como en el CI, que no lo compila). Lo que se
    # comprueba es que no sea el JSON de afuera: ni su contenido, ni un 200 de tipo JSON.
    r = c.get("/media/empresas/..%2F..%2Fproyectos.json")
    assert "estado_original" not in r.text
    assert r.status_code != 200 or "application/json" not in r.headers.get("content-type", "")
    assert c.get("/media/empresas/transllano.json").status_code == 404   # solo PNG de la carpeta de logos
