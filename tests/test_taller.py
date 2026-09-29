import io
import json
import re
import shutil
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.util import Inches

ORIGEN = Path(__file__).resolve().parent.parent / "datos"


def pptx_de_prueba() -> bytes:
    """Tres láminas: una con norma y cifra, una sin notas y una con formas de nombre repetido."""
    pres = Presentation()
    diapos = [
        ("Riesgo vial laboral", "El riesgo vial se gestiona como cualquier peligro. Lo exige la Ley 1503 de 2011: el 30 % de los siniestros ocurre en misión."),
        ("Lámina sin guion", ""),
        ("Cierre", "¿Qué aprendimos? Conducir es una tarea de alto riesgo."),
    ]
    for titulo, notas in diapos:
        s = pres.slides.add_slide(pres.slide_layouts[5])
        s.shapes.title.text = titulo
        for _ in range(2):
            caja = s.shapes.add_textbox(Inches(1), Inches(2), Inches(4), Inches(1))
            caja.name = "Dato"
            caja.text_frame.text = "Primer párrafo"
            caja.text_frame.add_paragraph().text = "Segundo párrafo"
        if notas:
            s.notes_slide.notes_text_frame.text = notas
    buf = io.BytesIO()
    pres.save(buf)
    return buf.getvalue()


def repo_falso(raiz: Path) -> Path:
    datos_csm = raiz / "videos" / "csm-curso" / "datos"
    datos_csm.mkdir(parents=True)
    laminas = [{"n": n, "formas": {"Text 1": [f"Título {n}"]}, "notas": f"Narración de la lámina {n}. Según el Decreto 1079 de 2015.",
                "frases": [], "foto": None, "icono": None} for n in range(1, 56)]
    (datos_csm / "curso.json").write_text(json.dumps(laminas), encoding="utf-8")
    (datos_csm / "guion-partes.json").write_text(json.dumps({"5": "Texto armado para la parte dos."}), encoding="utf-8")
    (datos_csm / "banco_preguntas.py").write_text(
        'import os\nos.system("echo esto-no-debe-ejecutarse")\n'
        'CURSO = {"nombre": "Prueba"}\n'
        'VIDEOS = [("m01", "Módulo 1", "Tema", [("¿P?", "Sí", "No", "Tal vez", "Lámina 4")])]\n'
        'FINAL = ("final", "Evaluación final", "Examen", [("¿Q?", "A", "B", "C", "Caso integrador")])\n',
        encoding="utf-8")
    return raiz


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    monkeypatch.setitem(datos.CONFIG, "repo_videos", repo_falso(tmp_path / "repo"))
    monkeypatch.delitem(datos.CONFIG, "entregables", raising=False)
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app), copia


def test_extractor_lee_formas_notas_y_frases(tmp_path):
    from app import extractor
    ruta = tmp_path / "c.pptx"
    ruta.write_bytes(pptx_de_prueba())
    laminas = extractor.leer_pptx(ruta)
    assert [l["n"] for l in laminas] == [1, 2, 3]
    assert set(laminas[0]) == {"n", "formas", "notas", "frases", "foto", "icono"}  # formato de csm
    assert "Dato" in laminas[0]["formas"] and "Dato (2)" in laminas[0]["formas"]  # no se pisan
    assert laminas[0]["formas"]["Dato"] == ["Primer párrafo", "Segundo párrafo"]
    assert laminas[0]["frases"][1].startswith("Lo exige la Ley 1503 de 2011:")
    assert laminas[1]["notas"] == "" and laminas[1]["frases"] == []
    assert laminas[2]["frases"] == ["¿Qué aprendimos?", "Conducir es una tarea de alto riesgo."]


def test_detecta_normas_y_cifras():
    from app import extractor
    citas = extractor.afirmaciones_normativas("Ley 1503 de 2011, el 30 % y 500 SMMLV; también la Resolución 20223040040595 de 2022.")
    assert citas == ["Ley 1503 de 2011", "30 %", "500 SMMLV", "Resolución 20223040040595 de 2022"]
    # Las cifras técnicas también piden fuente; el umbral del PESV es el caso que ya se contradijo.
    citas = extractor.afirmaciones_normativas("A 80 kilómetros por hora, deja 50 metros. El PESV aplica desde 11 vehículos.")
    assert citas == ["80 kilómetros por hora", "50 metros", "11 vehículos"]


def test_entra_pptx_y_sale_el_curso(cliente):
    c, copia = cliente
    r = c.post("/taller/nuevo", files={"archivo": ("seguridad.pptx", pptx_de_prueba())},
               data={"nombre": "Curso de prueba"}, follow_redirects=False)
    assert r.status_code == 303
    url = r.headers["location"].split("?")[0]
    id_ = url.rsplit("/", 1)[1]
    assert (copia / "trabajos" / id_ / "entrada.pptx").exists()

    html = c.get(url).text
    assert "Curso de prueba" in html
    assert "<mark>Ley 1503 de 2011</mark>" in html
    assert "Esta lámina no tiene notas" in html  # la lámina 2

    curso = c.get(f"{url}/curso.json").json()
    assert len(curso) == 3 and curso[0]["n"] == 1

    orden = c.get(f"{url}/orden.json").json()
    assert orden["marca"]["id"] == "riskmann" and orden["voz"]["id"] == "carlos"
    assert sum(len(v["laminas"]) for v in orden["videos"]) == 3
    falla = next(x for x in orden["verificacion"] if x["titulo"].startswith("Todas las láminas del video tienen"))
    assert falla["ok"] is False and "lámina 2" in falla["detalle"]


def test_cambiar_marca_voz_y_formato(cliente):
    c, _ = cliente
    url = c.post("/taller/nuevo", files={"archivo": ("x.pptx", pptx_de_prueba())}, follow_redirects=False).headers["location"].split("?")[0]
    c.post(f"{url}/ajustes", data={"marca": "fegir", "voz": "piper-davefx", "formatos": ["16:9", "9:16"]})
    orden = c.get(f"{url}/orden.json").json()
    assert orden["marca"]["id"] == "fegir" and orden["voz"]["proveedor"] == "Piper"
    assert orden["formatos"] == ["16:9", "9:16"]

    r = c.post(f"{url}/ajustes", data={"marca": "fegir", "voz": "inventada"}, follow_redirects=False)
    assert "error=" in r.headers["location"]
    r = c.post(f"{url}/ajustes", data={"marca": "fegir", "voz": "carlos"}, follow_redirects=False)
    assert "error=" in r.headers["location"]  # sin formatos


def test_lo_que_no_es_pptx_se_rechaza(cliente):
    c, copia = cliente
    r = c.post("/taller/nuevo", files={"archivo": ("notas.txt", b"hola")}, follow_redirects=False)
    assert "error=" in r.headers["location"]
    r = c.post("/taller/nuevo", files={"archivo": ("roto.pptx", b"no soy un zip")}, follow_redirects=False)
    assert "error=" in r.headers["location"]
    assert not list((copia / "trabajos").glob("*/trabajo.json")) if (copia / "trabajos").exists() else True
    assert not list((copia / "trabajos").glob("_subida-*")) if (copia / "trabajos").exists() else True


def test_caso_csm_trae_modulos_exclusiones_y_banco_sin_ejecutarlo(cliente, capfd):
    c, _ = cliente
    url = c.post("/taller/ejemplo-csm", follow_redirects=False).headers["location"].split("?")[0]
    orden = c.get(f"{url}/orden.json").json()
    assert [v["clave"] for v in orden["videos"]][:3] == ["ap1", "ap2", "m01"]
    assert len(orden["videos"]) == 15
    assert "7" in orden["excluidas"] and "52" in orden["excluidas"]

    banco = c.get(f"{url}/banco.json").json()
    assert [g["clave"] for g in banco["grupos"]] == ["m01", "final"]
    assert banco["grupos"][0]["preguntas"][0]["fuente"] == "Lámina 4"
    assert "esto-no-debe-ejecutarse" not in capfd.readouterr().out

    html = c.get(url).text
    assert "Texto armado para la parte dos." in html  # guion-partes.json manda sobre las notas
    assert "Módulo 1 · Tema" in html


def test_portada_muestra_el_recorrido(cliente):
    c, _ = cliente
    html = c.get("/").text
    assert "Entra un PPTX. Sale el curso en video." in html
    assert re.search(r"55\s*<small>láminas", html)


def test_ids_de_trabajo_no_se_salen_de_la_carpeta(cliente):
    c, _ = cliente
    assert c.get("/taller/..%2F..%2Fdatos").status_code == 404
    assert c.get("/taller/no-existe/orden.json").status_code == 404


def test_al_crear_se_avisa_y_el_guardado_automatico_responde_json(cliente):
    c, _ = cliente
    r = c.post("/taller/nuevo", files={"archivo": ("x.pptx", pptx_de_prueba())}, follow_redirects=False)
    assert r.headers["location"].endswith("?ok=creado")
    url = r.headers["location"].split("?")[0]
    assert "Listo: leímos tu presentación" in c.get(r.headers["location"]).text

    j = c.post(f"{url}/ajustes", data={"marca": "sofu", "voz": "carlos", "formatos": ["9:16"]},
               headers={"Accept": "application/json"})
    assert j.status_code == 200 and j.json()["ok"] is True
    j = c.post(f"{url}/ajustes", data={"marca": "sofu", "voz": "carlos"}, headers={"Accept": "application/json"})
    assert j.status_code == 400 and j.json()["ok"] is False and "formato" in j.json()["mensaje"]
    assert c.get(f"{url}/orden.json").json()["formatos"] == ["9:16"]  # el error no pisó lo guardado


def test_eliminar_un_curso(cliente):
    c, copia = cliente
    url = c.post("/taller/nuevo", files={"archivo": ("x.pptx", pptx_de_prueba())}, follow_redirects=False).headers["location"].split("?")[0]
    id_ = url.rsplit("/", 1)[1]
    r = c.post(f"{url}/eliminar", follow_redirects=False)
    assert r.headers["location"] == "/?ok=eliminado"
    assert not (copia / "trabajos" / id_).exists()
    assert c.get(url).status_code == 404
    assert c.post("/taller/no-existe/eliminar").status_code == 404
