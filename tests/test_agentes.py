import shutil
import zipfile

import pytest

from tests.test_motor import ORIGEN, pptx_con_foto
from tests.test_taller import pptx_de_prueba


@pytest.fixture()
def datos_copia(tmp_path, monkeypatch):
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos", "empresas", "musica"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    return copia


@pytest.fixture()
def ollama_falso(monkeypatch):
    """Ollama «encendido» con los modelos; `respuestas` decide qué devuelve según el esquema pedido."""
    from motor.agentes import ollama
    monkeypatch.setattr(ollama, "estado", lambda: {"encendido": True, "modelos": ["qwen3:4b", "qwen3.5:2b"], "faltan": []})
    respuestas = {}

    def chat(modelo, sistema, usuario, esquema, imagenes=None, tiempo=300):
        clave = tuple(sorted(esquema["properties"]))
        r = respuestas[clave]
        return r(usuario) if callable(r) else r
    monkeypatch.setattr(ollama, "chat", chat)
    return respuestas


def _curso(pptx=pptx_de_prueba):
    from app import taller
    return taller.desde_pptx("x.pptx", pptx(), "Curso de prueba")


def _propuestas(t, agente):
    from app import taller
    return [p for p in taller.cargar(t["id"])["propuestas"] if p["agente"] == agente and p["estado"] == "pendiente"]


def test_las_guardas_detectan_lo_inventado():
    from motor.agentes.guardas import inventado
    origen = "Lo exige la Ley 1503 de 2011: el 30 % de los siniestros. Multas de 1.500.000 pesos."
    assert inventado("El 30 % de los siniestros", origen) == []
    assert inventado("Multas de 1500000 pesos", origen) == []  # mismo número con o sin separador
    assert inventado("El 40 % de los siniestros", origen) == ["cifra 40"]
    assert "cifra 1079" in inventado("Según el Decreto 1079 de 2015", origen)


def test_redactor_con_reglas_y_aceptar_cambia_la_escena(datos_copia, sin_ollama):
    from app import taller
    from motor import escenas
    from motor.agentes import registro
    t = _curso()
    t["laminas"][2]["formas"]["Title 1"] = ["Qué aprendimos hoy sobre la conducción segura en la vía pública urbana"]
    taller.guardar(t)
    r = registro.ejecutar(t["id"], "redactor")
    assert r["con_ia"] is False and r["propuestas"] >= 1
    p = next(p for p in _propuestas(t, "redactor") if p["lamina"] == 3)
    assert p["hecha_con"] == "reglas" and len(p["despues"]["titulo"].split()) <= 9

    t = registro.aceptar(taller.cargar(t["id"]), p["id"])
    lamina = next(l for l in taller.laminas_efectivas(t) if l["n"] == 3)
    assert escenas.vista(lamina, 1, 3, "V", None)["titulo"] == p["despues"]["titulo"]
    assert t["laminas"][2]["formas"]["Title 1"][0].startswith("Qué aprendimos hoy")  # el original sigue intacto


def test_una_cifra_inventada_por_la_ia_se_descarta(datos_copia, ollama_falso):
    from motor.agentes import registro
    ollama_falso[("titulo", "vinetas")] = {"titulo": "El 45 % de los siniestros", "vinetas": ["Uno", "Dos"]}
    t = _curso()
    registro.ejecutar(t["id"], "redactor")
    assert _propuestas(t, "redactor") == []
    ollama_falso[("titulo", "vinetas")] = {"titulo": "Riesgo vial en el trabajo", "vinetas": ["El 30 % ocurre en misión"]}
    registro.ejecutar(t["id"], "redactor")
    props = _propuestas(t, "redactor")
    assert props and all(p["hecha_con"] == "qwen3:4b" for p in props)


def test_guionista_propone_narracion_para_la_lamina_muda(datos_copia, sin_ollama):
    from app import taller
    from motor.agentes import registro
    t = _curso()
    registro.ejecutar(t["id"], "guionista")
    p = next(p for p in _propuestas(t, "guionista") if p["lamina"] == 2)
    assert p["antes"]["notas"] == "" and "Lámina sin guion" in p["despues"]["notas"]
    t = registro.aceptar(taller.cargar(t["id"]), p["id"])
    falla = next(c for c in taller.resumen(t)["chequeos"] if c["clave"] == "sin_notas")
    assert falla["ok"] is True  # ya no queda ninguna lámina muda


def test_verificador_pregunta_la_fuente_y_se_marca_revisada(datos_copia):
    from app import taller
    from motor.agentes import registro
    t = _curso()
    registro.ejecutar(t["id"], "verificador")
    props = _propuestas(t, "verificador")
    assert {p["despues"]["cita"] for p in props} == {"Ley 1503 de 2011", "30 %"}
    for p in props:
        t = registro.aceptar(taller.cargar(t["id"]), p["id"])
    chequeo = next(c for c in taller.resumen(t)["chequeos"] if c["clave"] == "normativas")
    assert chequeo["ok"] is True and "ya tienen su fuente revisada" in chequeo["detalle"]
    registro.ejecutar(t["id"], "verificador")
    assert _propuestas(t, "verificador") == []  # lo revisado no se vuelve a preguntar


def test_director_con_reglas(datos_copia, sin_ollama):
    from app import taller
    from motor.agentes import registro
    from motor.escenas import animacion
    t = _curso()
    registro.ejecutar(t["id"], "director")
    props = _propuestas(t, "director")
    portada = next(p for p in props if p["lamina"] == 1)
    assert portada["despues"]["ajustes"]["titulo"]["entrada"]["efecto"] == "palabra-por-palabra"
    t = registro.aceptar(taller.cargar(t["id"]), portada["id"])
    assert animacion.plan(t, 1)["elementos"]["titulo"]["entrada"]["efecto"] == "palabra-por-palabra"


def test_director_con_ia_solo_elige_del_catalogo(datos_copia, ollama_falso):
    from motor.agentes import registro
    ollama_falso[("laminas",)] = lambda usuario: {"laminas": [
        {"n": 1, "plantilla": "cinetica", "titulo_entrada": "rebote", "vinetas_entrada": "subir", "razon": "Portada con energía"},
        {"n": 3, "plantilla": "no-existe", "titulo_entrada": "explotar", "vinetas_entrada": "subir", "razon": "x"}]}
    t = _curso()
    registro.ejecutar(t["id"], "director")
    props = {p["lamina"]: p for p in _propuestas(t, "director")}
    assert props[1]["despues"]["plantilla"] == "cinetica" and props[1]["hecha_con"] == "qwen3:4b"
    assert props.get(3, {}).get("hecha_con", "reglas") == "reglas"  # lo que no está en el catálogo cae a reglas


def test_evaluador_necesita_ia_y_exporta_a_moodle(datos_copia, sin_ollama, monkeypatch):
    from fastapi.testclient import TestClient

    from app import taller
    from app.main import app
    from motor.agentes import ollama, registro
    t = _curso()
    with pytest.raises(registro.ErrorAgente, match="necesita Ollama"):
        registro.ejecutar(t["id"], "evaluador")

    monkeypatch.setattr(ollama, "estado", lambda: {"encendido": True, "modelos": ["qwen3:4b"], "faltan": []})
    monkeypatch.setattr(ollama, "chat", lambda *a, **k: {"preguntas": [
        {"enunciado": "¿Qué ley exige gestionar el riesgo vial?", "correcta": "La Ley 1503 de 2011",
         "distractores": ["La Ley 100 de 1993", "Ninguna"], "lamina": 1},
        {"enunciado": "¿Qué porcentaje ocurre en misión?", "correcta": "El 45 %", "distractores": ["10 %", "90 %"], "lamina": 1},
        {"enunciado": "¿Qué es conducir?", "correcta": "Una tarea de alto riesgo", "distractores": ["Un juego", "Nada"], "lamina": 9},
    ]})
    registro.ejecutar(t["id"], "evaluador")
    (p,) = _propuestas(t, "evaluador")
    # Quedan fuera la del 45 % (cifra inventada) y la de la lámina 9 (no existe).
    assert [q["enunciado"] for q in p["despues"]["preguntas"]] == ["¿Qué ley exige gestionar el riesgo vial?"]
    registro.aceptar(taller.cargar(t["id"]), p["id"])

    c = TestClient(app)
    gift = c.get(f"/api/trabajos/{t['id']}/banco.gift").text
    assert "$CATEGORY:" in gift and "=La Ley 1503 de 2011" in gift and "~Ninguna" in gift
    xml = c.get(f"/api/trabajos/{t['id']}/banco.xml").text
    assert '<question type="multichoice">' in xml and 'fraction="100"' in xml


def test_publicador_y_su_texto_en_el_paquete(datos_copia, sin_ollama):
    from app import taller
    from motor import empaquetar
    from motor.agentes import registro
    t = _curso()
    registro.ejecutar(t["id"], "publicador")
    (p,) = _propuestas(t, "publicador")
    assert "Capítulos:\n0:00" in p["despues"]["descripcion"] and len(p["despues"]["historias"]) >= 1
    t = registro.aceptar(taller.cargar(t["id"]), p["id"])
    # El paquete necesita algo producido: se simula un video listo.
    salida = taller.ruta_trabajo(t["id"]).parent / "salida" / "v01"
    salida.mkdir(parents=True)
    (salida / "v01.mp4").write_bytes(b"mp4")
    (salida / "qa.json").write_text('{"archivos": ["v01.mp4"]}', encoding="utf-8")
    with zipfile.ZipFile(empaquetar.paquete(t)) as z:
        assert "publicacion.md" in z.namelist()


def test_descriptor_con_reglas_marca_la_imagen_pequena_como_decoracion(datos_copia, sin_ollama):
    from app import taller
    from motor import escenas
    from motor.agentes import registro
    t = _curso(pptx_con_foto)
    registro.ejecutar(t["id"], "descriptor")
    (p,) = _propuestas(t, "descriptor")
    assert p["despues"]["tipo"] == "contenido"  # 640×480: es contenido
    media = taller.ruta_trabajo(t["id"]).parent / "media"
    from PIL import Image
    Image.new("RGB", (120, 60)).save(media / p["despues"]["archivo"])  # ahora es un adorno pequeño
    registro.ejecutar(t["id"], "descriptor")
    (p,) = _propuestas(t, "descriptor")
    assert p["despues"]["decorativa"] is True
    t = registro.aceptar(taller.cargar(t["id"]), p["id"])
    lamina = next(l for l in taller.laminas_efectivas(t) if l["n"] == 2)
    assert escenas.vista(lamina, 1, 2, "V", media)["imagen"] is None  # la escena ya no la usa como foto


def test_agentes_por_la_api_y_ediciones(datos_copia, sin_ollama):
    from fastapi.testclient import TestClient

    from app.main import app
    from motor import cola
    c = TestClient(app)
    id_ = c.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_de_prueba())}).json()["id"]

    lista = c.get("/api/agentes").json()
    assert {a["id"] for a in lista} == {"redactor", "director", "guionista", "verificador", "evaluador",
                                        "publicador", "descriptor", "revisor_voz"}
    assert c.post(f"/api/trabajos/{id_}/agentes/verificador").status_code == 202
    cola.esperar()
    r = c.get(f"/api/trabajos/{id_}/agentes").json()
    assert r["estados"]["verificador"]["estado"] == "listo" and r["estados"]["verificador"]["propuestas"] == 2
    pid = r["propuestas"][0]["id"]
    assert c.post(f"/api/trabajos/{id_}/propuestas/{pid}/descartar").status_code == 200
    assert c.post(f"/api/trabajos/{id_}/propuestas/{pid}/aceptar").status_code == 400  # ya estaba resuelta

    # «Aceptar todas»: una sola petición resuelve las pendientes del agente.
    r = c.post(f"/api/trabajos/{id_}/agentes/verificador/aceptar").json()
    assert r["errores"] == []
    assert [p["estado"] for p in r["propuestas"] if p["agente"] == "verificador"] == ["descartada", "aceptada"]
    assert c.post(f"/api/trabajos/{id_}/agentes/nadie/aceptar").status_code == 404

    # Un agente que necesita IA, sin Ollama: el error llega al estado del agente.
    c.post(f"/api/trabajos/{id_}/agentes/evaluador")
    cola.esperar()
    e = c.get(f"/api/trabajos/{id_}/agentes").json()["estados"]["evaluador"]
    assert e["estado"] == "error" and "necesita Ollama" in e["mensaje"]

    # Edición a mano de una lámina, y vuelta al original.
    r = c.put(f"/api/trabajos/{id_}/laminas/1/edicion", json={"cambios": {"titulo": "Nuevo título", "notas": "Solo esto."}})
    lamina = r.json()["trabajo"]["laminas"][0]
    assert lamina["titulo"] == "Nuevo título" and lamina["frases"] == ["Solo esto."] and lamina["editada"]
    assert c.put(f"/api/trabajos/{id_}/laminas/1/edicion", json={"cambios": {"titulo": " "}}).status_code == 400
    r = c.put(f"/api/trabajos/{id_}/laminas/1/edicion", json={"cambios": None})
    assert r.json()["trabajo"]["laminas"][0]["notas"].startswith("El riesgo vial")


def test_el_estado_de_ollama_se_guarda_unos_segundos(monkeypatch):
    import httpx

    from motor.agentes import ollama
    llamadas = []

    def get(*a, **k):
        llamadas.append(a)
        raise httpx.ConnectError("apagado")
    monkeypatch.setattr(ollama.httpx, "get", get)
    monkeypatch.setattr(ollama, "_estado", {"hora": 0.0, "clave": None, "datos": None})
    assert not ollama.estado()["encendido"]
    assert not ollama.estado()["encendido"]
    assert len(llamadas) == 1  # la segunda vez no vuelve a esperar a Ollama
    monkeypatch.setattr(ollama, "SEGUNDOS_ESTADO", 0)
    ollama.estado()
    assert len(llamadas) == 2


def test_una_norma_cambiada_con_los_mismos_numeros_tambien_se_detecta():
    from motor.agentes.guardas import inventado
    origen = "Lo exige la Ley 1503 de 2011 y el 30 % ocurre en misión."
    assert inventado("Lo exige el Decreto 1503 de 2011", origen) == ["norma «Decreto 1503 de 2011»"]
    assert inventado("El 30% ocurre en misión", origen) == []
