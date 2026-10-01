import io
import json
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
        ("Riesgo vial laboral", "El riesgo vial se gestiona como cualquier peligro. "
                                "Lo exige la Ley 1503 de 2011: el 30 % de los siniestros ocurre en misión."),
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


def _lamina(n, notas="Una frase de guion.", **formas):
    return {"n": n, "formas": {k: [v] for k, v in formas.items()}, "notas": notas, "frases": [notas], "foto": None, "icono": None}


def test_agrupa_por_seccion_cuando_el_pptx_la_marca():
    from app import extractor
    laminas = [
        _lamina(1, **{"cover-kicker": "RISKMANN", "cover-title": "Motociclista"}),   # portada sin sección
        _lamina(2, section="APERTURA", title="Propósito de la formación"),
        _lamina(3, section="APERTURA", title="Reglas"),
        _lamina(4, section="MÓDULO 1", title="Una persona expuesta"),
        _lamina(5, section="MÓDULO 1", title="Los seis factores"),
        _lamina(6, section="MÓDULO 2", title="La norma como barrera"),
        _lamina(7, **{"Título 1": "Gracias"}),                                      # cierre sin sección
    ]
    grupos = extractor.agrupar(laminas)
    assert [g["laminas"] for g in grupos] == [[1, 2, 3], [4, 5], [6, 7]]
    assert [g["titulo"] for g in grupos] == [
        "Apertura · Propósito de la formación", "Módulo 1 · Una persona expuesta", "Módulo 2 · La norma como barrera"]
    assert extractor.titulo_lamina(laminas[6]) == "Gracias"  # «Título 1» de PowerPoint cuenta como título


def test_sin_secciones_agrupa_por_duracion():
    from app import extractor
    largas = [_lamina(n, notas="palabra " * 150) for n in range(1, 7)]  # ~65 s cada una
    grupos = extractor.agrupar(largas)
    assert len(grupos) == 3 and all(len(g["laminas"]) == 2 for g in grupos)


def test_detecta_normas_y_cifras():
    from app import extractor
    citas = extractor.afirmaciones_normativas("Ley 1503 de 2011, el 30 % y 500 SMMLV; también la Resolución 20223040040595 de 2022.")
    assert citas == ["Ley 1503 de 2011", "30 %", "500 SMMLV", "Resolución 20223040040595 de 2022"]
    # Las cifras técnicas también piden fuente; el umbral del PESV es el caso que ya se contradijo.
    citas = extractor.afirmaciones_normativas("A 80 kilómetros por hora, deja 50 metros. El PESV aplica desde 11 vehículos.")
    assert citas == ["80 kilómetros por hora", "50 metros", "11 vehículos"]


def crear(c, nombre="Curso de prueba"):
    r = c.post("/api/trabajos", files={"archivo": ("seguridad.pptx", pptx_de_prueba())}, data={"nombre": nombre})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_entra_pptx_y_sale_el_curso(cliente, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "de-prueba")  # Carlos, la voz de la configuración, está lista
    c, copia = cliente
    id_ = crear(c)
    assert (copia / "trabajos" / id_ / "entrada.pptx").exists()

    d = c.get(f"/api/trabajos/{id_}").json()
    t, r = d["trabajo"], d["resumen"]
    assert t["nombre"] == "Curso de prueba"
    assert t["laminas"][0]["citas"] == ["Ley 1503 de 2011", "30 %"]
    assert t["laminas"][0]["titulo"] == "Riesgo vial laboral"
    assert "laminas_detalle" not in r["videos"][0]  # la API no duplica las láminas

    curso = c.get(f"/api/trabajos/{id_}/curso.json").json()
    assert len(curso) == 3 and curso[0]["n"] == 1

    orden = c.get(f"/api/trabajos/{id_}/orden.json").json()
    assert orden["marca"]["id"] == "riskmann" and orden["voz"]["id"] == "carlos"
    assert sum(len(v["laminas"]) for v in orden["videos"]) == 3
    falla = next(x for x in orden["verificacion"] if x["titulo"].startswith("Todas las láminas del video tienen"))
    assert falla["ok"] is False and "lámina 2" in falla["detalle"]


def test_cambiar_marca_voz_y_formato(cliente):
    c, _ = cliente
    id_ = crear(c)
    r = c.patch(f"/api/trabajos/{id_}", json={"marca": "fegir", "voz": "piper-davefx", "formatos": ["16:9", "9:16"]})
    assert r.status_code == 200 and r.json()["trabajo"]["marca"] == "fegir"
    orden = c.get(f"/api/trabajos/{id_}/orden.json").json()
    assert orden["voz"]["proveedor"] == "Piper" and orden["formatos"] == ["16:9", "9:16"]

    for malo in [{"marca": "fegir", "voz": "inventada", "formatos": ["16:9"]},
                 {"marca": "inventada", "voz": "carlos", "formatos": ["16:9"]},
                 {"marca": "fegir", "voz": "carlos", "formatos": []}]:
        r = c.patch(f"/api/trabajos/{id_}", json=malo)
        assert r.status_code == 400 and r.json()["detail"], malo
    assert c.get(f"/api/trabajos/{id_}/orden.json").json()["formatos"] == ["16:9", "9:16"]  # nada se pisó


def test_lo_que_no_es_pptx_se_rechaza_sin_dejar_basura(cliente):
    c, copia = cliente
    r = c.post("/api/trabajos", files={"archivo": ("notas.txt", b"hola")})
    assert r.status_code == 400 and "pptx" in r.json()["detail"].lower()
    r = c.post("/api/trabajos", files={"archivo": ("roto.pptx", b"no soy un zip")})
    assert r.status_code == 400
    carpeta = copia / "trabajos"
    assert not carpeta.exists() or not list(carpeta.glob("*/trabajo.json"))
    assert not carpeta.exists() or not list(carpeta.glob("_subida-*"))


def test_caso_csm_trae_modulos_exclusiones_y_banco_sin_ejecutarlo(cliente, capfd):
    c, _ = cliente
    r = c.post("/api/trabajos/ejemplo-csm")
    assert r.status_code == 201
    id_ = r.json()["id"]
    orden = c.get(f"/api/trabajos/{id_}/orden.json").json()
    assert [v["clave"] for v in orden["videos"]][:3] == ["ap1", "ap2", "m01"]
    assert len(orden["videos"]) == 15
    assert "7" in orden["excluidas"] and "52" in orden["excluidas"]

    banco = c.get(f"/api/trabajos/{id_}/banco.json").json()
    assert [g["clave"] for g in banco["grupos"]] == ["m01", "final"]
    assert banco["grupos"][0]["preguntas"][0]["fuente"] == "Lámina 4"
    assert "esto-no-debe-ejecutarse" not in capfd.readouterr().out

    t = c.get(f"/api/trabajos/{id_}").json()["trabajo"]
    assert next(l for l in t["laminas"] if l["n"] == 5)["notas"] == "Texto armado para la parte dos."
    assert t["videos"][2]["titulo"] == "Módulo 1 · Tema"


def test_inicio_trae_las_cifras_del_ejemplo_y_los_cursos(cliente):
    c, _ = cliente
    crear(c, "Primero")
    d = c.get("/api/inicio").json()
    assert d["cifras_ejemplo"]["laminas"] == 55
    assert d["ejemplo_disponible"] is True
    assert [t["nombre"] for t in d["trabajos"]] == ["Primero"]
    assert d["total_videos"] == sum(d["conteo_estados"].values())


def test_eliminar_un_curso(cliente):
    c, copia = cliente
    id_ = crear(c)
    assert c.delete(f"/api/trabajos/{id_}").status_code == 204
    assert not (copia / "trabajos" / id_).exists()
    assert c.get(f"/api/trabajos/{id_}").status_code == 404
    assert c.delete("/api/trabajos/no-existe").status_code == 404


def test_ids_de_trabajo_no_se_salen_de_la_carpeta(cliente):
    c, _ = cliente
    assert c.get("/api/trabajos/..%2F..%2Fdatos").status_code == 404
    assert c.get("/api/trabajos/no-existe/orden.json").status_code == 404


def test_rutas_de_la_interfaz_devuelven_la_aplicacion(cliente, tmp_path, monkeypatch):
    c, _ = cliente
    from app import main
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<div id=app></div>", encoding="utf-8")
    (dist / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
    monkeypatch.setattr(main, "DIST", dist)
    assert c.get("/cursos/abc").text == "<div id=app></div>"      # ruta de Vue
    assert c.get("/assets/app.js").text == "console.log(1)"       # archivo compilado
    assert c.get("/..%2F..%2Fdatos%2Fproyectos.json").text == "<div id=app></div>"  # nunca sale de dist


def test_volver_a_proponer_los_videos(cliente):
    c, _ = cliente
    id_ = crear(c)
    r = c.post(f"/api/trabajos/{id_}/reagrupar")
    assert r.status_code == 200 and r.json()["resumen"]["videos"]
    ej = c.post("/api/trabajos/ejemplo-csm").json()["id"]
    r = c.post(f"/api/trabajos/{ej}/reagrupar")
    assert r.status_code == 400  # el ejemplo conserva los módulos con los que se produjo


def test_curso_nuevo_toma_una_voz_que_este_equipo_pueda_usar(cliente, monkeypatch):
    from motor import voz
    c, _ = cliente
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    # Sin clave de ElevenLabs, con Kokoro listo: la primera voz que se puede entregar (nunca Piper).
    monkeypatch.setattr(voz, "disponible", lambda v: None if v["proveedor"] in ("Kokoro", "Piper") else "falta")
    assert c.get(f"/api/trabajos/{crear(c)}").json()["trabajo"]["voz"] == "kokoro-dora"
    # Si nada está listo, queda la de la configuración y el taller dice qué le falta.
    monkeypatch.setattr(voz, "disponible", lambda v: "falta")
    assert c.get(f"/api/trabajos/{crear(c)}").json()["trabajo"]["voz"] == "carlos"
    # Con la clave, la de la configuración.
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    assert c.get(f"/api/trabajos/{crear(c)}").json()["trabajo"]["voz"] == "carlos"
