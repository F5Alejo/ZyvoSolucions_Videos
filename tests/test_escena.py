"""Cámara, transiciones y formatos (16:9, 9:16, 1:1 y 4:5)."""

import json
import subprocess

import pytest

from tests.test_motor import VozDePrueba, hay_ffmpeg, pptx_con_foto


def _curso(formato="16:9"):
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", "kokoro-dora", [formato])


def test_la_camara_y_los_fundidos_salen_del_catalogo():
    from motor import camara
    assert camara.filtro_camara("estatica", 90, 1920, 1080, 30) is None
    z = camara.filtro_camara("zoom_lento_entrada", 90, 1920, 1080, 30)
    assert "zoompan" in z and "s=1920x1080" in z and "y='ih-ih/zoom'" in z  # el borde de abajo no se mueve
    with pytest.raises(ValueError, match="catálogo"):
        camara.filtro_camara("explosion_super_3d", 90, 1920, 1080, 30)
    assert camara.filtro_fundidos(True, True, 90, 30, "#020202") == [
        "fade=t=in:st=0:d=0.3:color=0x020202", "fade=t=out:st=2.700:d=0.3:color=0x020202"]


def test_los_ajustes_de_escena_se_validan(datos_copia):
    from motor import catalogo
    assert catalogo.validar_escena({"camara": "zoom_lento_entrada", "laminas": {"2": {"transicion": "fundido"}, "3": {}}}) == \
        {"camara": "zoom_lento_entrada", "laminas": {"2": {"transicion": "fundido"}}}
    for malo in ({"camara": "giro"}, {"laminas": {"dos": {}}}, {"laminas": {"2": {"transicion": "xfade"}}}):
        with pytest.raises(ValueError):
            catalogo.validar_escena(malo)


def test_el_formato_y_la_escena_cambian_la_firma_solo_si_no_son_los_de_siempre(datos_copia):
    from app import taller
    from motor import produccion, videospec
    t = _curso()
    base = produccion.firma(t)
    assert produccion.formato(t) == "16:9"
    vertical = taller.ajustar(t, "riskmann", "kokoro-dora", ["9:16"])
    assert produccion.formato(vertical) == "9:16" and produccion.firma(vertical) != base
    t = taller.ajustar(vertical, "riskmann", "kokoro-dora", ["16:9"])
    assert produccion.firma(t) == base
    t["escena"] = {"camara": "paneo_derecha"}
    assert produccion.firma(t) != base
    spec = videospec.construir(t, "v01", produccion.firma(t))
    assert {e.camara for e in spec.escenas} == {"paneo_derecha"}


def test_la_escena_por_la_api(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    c = TestClient(app)
    t = _curso()
    cat = c.get("/api/catalogo/escena").json()
    assert {x["id"] for x in cat["camaras"]} >= {"estatica", "zoom_lento_entrada"}
    assert {x["id"] for x in cat["formatos"]} == {"16:9", "9:16", "1:1", "4:5"}
    r = c.put(f"/api/trabajos/{t['id']}/escena", json={"transicion": "fundido", "laminas": {"2": {"camara": "zoom_lento_salida"}}})
    assert r.status_code == 200 and r.json()["trabajo"]["escena"]["transicion"] == "fundido"
    assert c.put(f"/api/trabajos/{t['id']}/escena", json={"camara": "giro"}).status_code == 400
    assert "escena" not in c.put(f"/api/trabajos/{t['id']}/escena", json={}).json()["trabajo"]


@pytest.mark.parametrize("formato", ["1:1", "4:5"])
def test_las_escenas_caben_en_cada_formato(datos_copia, formato):
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright

    from app import taller
    from motor import escenas, recursos
    t = _curso(formato)
    media = recursos.media(t)
    ancho, alto = escenas.FORMATOS[formato]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pagina = b.new_page(viewport={"width": ancho, "height": alto})
        for i, l in enumerate(taller.laminas_efectivas(t)):
            v = escenas.vista(l, i, 2, "Curso de prueba", media, "Curso")
            pagina.set_content(escenas.html(v, escenas.estilo({"paleta": [{"hex": "#000000"}, {"hex": "#FFCC00"}]}), formato))
            sobra = pagina.evaluate("() => { const c = document.querySelector('.cuerpo'); return c.scrollHeight - c.clientHeight; }")
            assert sobra <= 2, (formato, v["tipo"], sobra)
        b.close()


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_video_vertical_con_camara_y_fundidos(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from app import taller
    from motor import produccion, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    t = _curso("9:16")
    t["escena"] = {"camara": "zoom_lento_entrada", "transicion": "fundido"}
    taller.guardar(t)
    informe = produccion.producir(t, "v01")
    assert informe["formato"] == "9:16"
    assert {x["camara"] for x in informe["linea_de_tiempo"]} == {"zoom_lento_entrada"}
    fallas = [c for c in informe["chequeos"] if c["ok"] is False]
    assert not fallas, fallas  # también «Sin pantallas negras»: el fundido dura menos de 1 s
    mp4 = datos_copia / "trabajos" / t["id"] / "salida" / "v01" / "v01.mp4"
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(mp4)],
                                     capture_output=True, text=True).stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (v["width"], v["height"]) == (1080, 1920)
