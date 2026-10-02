"""Versiones de cada video, regeneración selectiva y muestra de voz."""

import pytest

from tests.test_motor import VozDePrueba, hay_ffmpeg, pptx_con_foto


def _curso():
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", "kokoro-dora", ["16:9"])


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_cada_produccion_es_una_version_y_se_regenera_por_partes(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from fastapi.testclient import TestClient

    from app import taller
    from app.main import app
    from motor import cola, versiones, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    c = TestClient(app)
    t = _curso()
    salida = datos_copia / "trabajos" / t["id"] / "salida" / "v01"

    c.post(f"/api/trabajos/{t['id']}/producir/v01")
    cola.esperar()
    escenas_antes = {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")}
    v1 = (salida / "versiones" / "v001" / "video.mp4").read_bytes()

    # Regenerar solo la escena de la lámina 2: la de la lámina 1 queda igual.
    assert c.post(f"/api/trabajos/{t['id']}/regenerar/v01", json={"escena": 2}).status_code == 202
    cola.esperar()
    despues = {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")}
    iguales = [n for n in despues if escenas_antes.get(n) == despues[n]]
    assert len(despues) == 2 and len(iguales) == 1

    # Regenerar solo la voz: se vuelven a crear las frases, las escenas no se tocan.
    cache = datos_copia / "trabajos" / t["id"] / "cache" / "voz"
    frases = {p.name: p.stat().st_mtime_ns for p in cache.glob("*.wav")}
    c.post(f"/api/trabajos/{t['id']}/regenerar/v01", json={"voz": True})
    cola.esperar()
    assert all(p.stat().st_mtime_ns != frases[p.name] for p in cache.glob("*.wav"))
    assert {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")} == despues

    lista = c.get(f"/api/trabajos/{t['id']}/versiones/v01").json()
    assert [v["version"] for v in lista] == ["v003", "v002", "v001"] and lista[0]["fallas"] == 0
    # La versión 1 no cambió aunque el video se volvió a producir (no se reescribe el archivo enlazado).
    assert (salida / "versiones" / "v001" / "video.mp4").read_bytes() == v1
    r = c.get(lista[-1]["mp4"] + "?descargar=1")
    assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
    assert c.get(f"/api/trabajos/{t['id']}/versiones/v01/v001/..%2Fqa.json").status_code == 404
    assert c.post(f"/api/trabajos/{t['id']}/regenerar/v01", json={"escena": 99}).status_code == 404

    # Solo se guardan las últimas MAXIMO.
    monkeypatch.setattr(versiones, "MAXIMO", 2)
    versiones.guardar(taller.cargar(t["id"]), "v01")
    assert [v["version"] for v in versiones.lista(t, "v01")] == ["v004", "v003"]


def test_la_muestra_de_voz(datos_copia, monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import app
    from motor import voz
    c = TestClient(app)
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    assert c.get("/api/voces/carlos/muestra").status_code == 400   # falta la clave: lo dice
    assert c.get("/api/voces/no-existe/muestra").status_code == 404
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    if hay_ffmpeg:
        r = c.get("/api/voces/kokoro-dora/muestra")
        assert r.status_code == 200 and r.headers["content-type"] == "audio/wav"
        assert list((datos_copia / "cache" / "muestras").glob("*.wav"))
