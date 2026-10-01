import copy
import shutil

import pytest

from tests.test_motor import ORIGEN, hay_ffmpeg


@pytest.fixture()
def datos_copia(tmp_path, monkeypatch):
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos", "musica"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    return copia


def _vista(indice=1, total=3, vinetas=2, titulo="Conducción defensiva"):
    return {"tipo": "portada" if indice == 0 else "lista", "titulo": titulo, "vinetas": [f"Viñeta {i}" for i in range(vinetas)],
            "imagen": None, "video": "Video", "antetitulo": "Curso", "indice": indice, "total": total}


def test_las_plantillas_de_fabrica_son_validas(datos_copia):
    from motor.escenas import animacion
    todas = animacion.plantillas()
    assert {"sobria", "dinamica", "cinetica", "corporativa", "minima"} <= set(todas)
    for p in todas.values():
        animacion.validar_plantilla(p)


@pytest.mark.parametrize("elementos, error", [
    ({"titulo": {"entrada": {"efecto": "explotar"}}}, "explotar"),
    ({"vinetas": {"entrada": {"efecto": "palabra-por-palabra"}}}, "no está permitido"),
    ({"titulo": {"entrada": {"duracion": 9}}}, "entre 0 y 3"),
    ({"titulo": {"entrada": {"curva": "rara"}}}, "curva"),
    ({"marciano": {"entrada": {}}}, "no es un elemento"),
    ({"titulo": {"entrada": {"color": "rojo"}}}, "no es un ajuste"),
])
def test_ajustes_invalidos_se_rechazan(datos_copia, elementos, error):
    from motor.escenas import animacion
    with pytest.raises(animacion.AnimacionInvalida, match=error):
        animacion.validar_curso({"ajustes": elementos})


def test_la_animacion_se_arma_por_capas(datos_copia):
    from motor.escenas import animacion
    t = {"animacion": animacion.validar_curso({
        "plantilla": "sobria",
        "ajustes": {"titulo": {"entrada": {"efecto": "subir"}}},
        "laminas": {"2": {"ajustes": {"titulo": {"salida": {"efecto": "desenfoque", "duracion": 0.8}}}},
                    "3": {"plantilla": "cinetica"}},
    })}
    uno, dos, tres = (animacion.plan(t, n) for n in (1, 2, 3))
    assert uno["plantilla"] == "sobria" and uno["elementos"]["titulo"]["entrada"]["efecto"] == "subir"
    assert uno["elementos"]["titulo"]["entrada"]["duracion"] == 0.8  # lo demás sigue siendo de «sobria»
    assert dos["elementos"]["titulo"]["salida"] == {**uno["elementos"]["titulo"]["salida"], "efecto": "desenfoque", "duracion": 0.8}
    assert tres["plantilla"] == "cinetica" and tres["elementos"]["titulo"]["entrada"]["efecto"] == "palabra-por-palabra"


def test_duraciones_y_elementos_continuos(datos_copia):
    from motor.escenas import animacion
    p = {"plantilla": "dinamica", "elementos": animacion.plantillas()["dinamica"]["elementos"]}
    ent, sal = animacion.duraciones(p, _vista(indice=1, vinetas=3))
    # Viñetas: 0,45 + 0,5 + 0,12 × 2 = 1,19 s; el fondo (1,2 s) no entra fuera de la primera escena.
    assert ent == pytest.approx(1.19) and sal > 0
    ent0, _ = animacion.duraciones(p, _vista(indice=0))
    assert ent0 >= 1.2  # en la portada sí entra el fondo
    reglas, _ = animacion.css(p, _vista(indice=1), 5.0, 33, 66)
    assert "ent-fondo" not in reglas and "sal-fondo" not in reglas
    reglas, _ = animacion.css(p, _vista(indice=2), 5.0, 66, 100)
    assert "sal-fondo" in reglas  # la última escena del video cierra el fondo


def test_palabra_por_palabra_parte_el_titulo(datos_copia):
    from motor import escenas
    from motor.escenas import animacion
    p = {"plantilla": "cinetica", "elementos": animacion.plantillas()["cinetica"]["elementos"]}
    html = escenas.html(_vista(titulo="Tres palabras juntas"), escenas.estilo({"paleta": [{"hex": "#000000"}, {"hex": "#FFCC00"}]}),
                        plan=p, segundos=5)
    assert html.count('<span class="trozo">') == 3 and ".trozo:nth-child(3)" in html


def _estado_final(html: str, segundos: float, selector: str) -> dict:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.set_content(html)
        pg.evaluate("(ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }", segundos * 1000 - 1)
        estilo = pg.evaluate(
            f"() => {{ const s = getComputedStyle(document.querySelector('{selector}')); return {{opacity: +s.opacity}}; }}")
        b.close()
    return estilo


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_la_salida_se_ve_al_final_de_la_escena(datos_copia):
    pytest.importorskip("playwright")
    from motor import escenas
    from motor.escenas import animacion
    base = copy.deepcopy(animacion.plantillas()["sobria"]["elementos"])
    estilo = escenas.estilo({"paleta": [{"hex": "#000000"}, {"hex": "#FFCC00"}]})
    con_salida = escenas.html(_vista(), estilo, plan={"plantilla": "x", "elementos": base}, segundos=4)
    assert _estado_final(con_salida, 4, "h1")["opacity"] < 0.05

    base["titulo"]["salida"]["efecto"] = "ninguno"
    sin_salida = escenas.html(_vista(), estilo, plan={"plantilla": "x", "elementos": base}, segundos=4)
    assert _estado_final(sin_salida, 4, "h1")["opacity"] == 1


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_el_revisor_de_encuadre_detecta_texto_que_no_cabe(tmp_path, datos_copia):
    pytest.importorskip("playwright")
    from motor import escenas, render
    estilo = escenas.estilo({"paleta": [{"hex": "#000000"}, {"hex": "#FFCC00"}]})
    bien = escenas.html(_vista(vinetas=2), estilo, segundos=2)
    mal = escenas.html({**_vista(vinetas=5), "vinetas": ["Una viñeta larguísima que ocupa varias líneas " * 4] * 5}, estilo, segundos=2)
    problemas = render.video([(bien, 60, 1.0, 0.3), (mal, 60, 1.0, 0.3)], 1920, 1080, tmp_path / "v.mp4", tmp_path / "t")
    assert problemas and all(p["escena"] == 1 for p in problemas)
    assert (tmp_path / "v.mp4").exists()


# ── API ──────────────────────────────────────────────────────────────────────

@pytest.fixture()
def cliente(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    return TestClient(app)


def test_api_de_animaciones(cliente):
    from tests.test_motor import pptx_con_foto
    cat = cliente.get("/api/animaciones").json()
    assert {p["id"] for p in cat["plantillas"]} >= {"sobria", "cinetica"}
    assert {"id": "palabra-por-palabra", "nombre": "Palabra por palabra"} in cat["elementos"]["titulo"]["entrada"]
    assert all(x["id"] != "palabra-por-palabra" for x in cat["elementos"]["vinetas"]["entrada"])

    id_ = cliente.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_con_foto())}).json()["id"]
    a = {"plantilla": "corporativa", "ajustes": {"titulo": {"salida": {"efecto": "desenfoque"}}},
         "laminas": {"2": {"plantilla": "cinetica"}}}
    assert cliente.put(f"/api/trabajos/{id_}/animacion", json=a).status_code == 200
    guardada = cliente.get(f"/api/trabajos/{id_}/animacion").json()
    assert guardada["plantilla"] == "corporativa" and guardada["animacion"]["laminas"]["2"]["plantilla"] == "cinetica"
    assert cliente.put(f"/api/trabajos/{id_}/animacion", json={"plantilla": "no-existe"}).status_code == 400

    # Vista previa: sin rutas locales, con el bucle y con lo que se está editando (sin guardar).
    html = cliente.post(f"/api/trabajos/{id_}/escena/2", json={"animacion": {"plantilla": "sobria"}}).text
    assert "file://" not in html and "/api/escenas/fuente.ttf" in html and "setInterval" in html
    assert "/api/trabajos/" in html and "/media/" in html  # la lámina 2 trae foto
    assert cliente.get("/api/escenas/fuente.ttf").status_code == 200
    assert cliente.get(f"/api/trabajos/{id_}/escena/9").status_code == 404
    assert cliente.get(f"/api/trabajos/{id_}/media/..%2Ftrabajo.json").status_code == 404


def test_plantillas_propias(cliente):
    base = next(p for p in cliente.get("/api/animaciones").json()["plantillas"] if p["id"] == "sobria")
    r = cliente.post("/api/animaciones", json={"nombre": "Mi estilo", "descripcion": "prueba", "elementos": base["elementos"]})
    assert r.status_code == 201 and r.json()["id"] == "propia-mi-estilo" and r.json()["propia"] is True
    otra = cliente.post("/api/animaciones", json={"nombre": "Mi estilo", "elementos": base["elementos"]})
    assert otra.json()["id"] == "propia-mi-estilo-2"
    rota = cliente.post("/api/animaciones", json={"nombre": "Rota", "elementos": {"titulo": base["elementos"]["titulo"]}})
    assert rota.status_code == 400
    assert cliente.delete("/api/animaciones/sobria").status_code == 400  # las de fábrica no se borran
    assert cliente.delete("/api/animaciones/propia-mi-estilo").status_code == 204
