"""Estilos, efectos de sonido, el director de música y la línea de tiempo."""

import json

import numpy as np
import pytest
import soundfile as sf

from tests.test_motor import VozDePrueba, hay_ffmpeg, pptx_con_foto


def _curso():
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", "kokoro-dora", ["16:9"])


def _pista(carpeta, nombre, energia):
    carpeta.mkdir(parents=True, exist_ok=True)
    t = np.arange(48000 * 4) / 48000
    sf.write(str(carpeta / f"{nombre}.wav"), (0.4 * np.sin(2 * np.pi * 330 * t)).astype(np.float32), 48000)
    (carpeta / f"{nombre}.json").write_text(json.dumps({"licencia": "Propia", "fuente": "", "energia": energia}), encoding="utf-8")


def test_los_siete_estilos_solo_usan_el_catalogo(datos_copia):
    from motor import estilos
    todos = estilos.estilos()
    assert set(todos) == {"educativo", "corporativo", "tecnologico", "minimalista", "dinamico", "cinematico", "social"}
    assert all(e["version"] == 1 and e["icono"] and e["descripcion"] for e in todos.values())

    (datos_copia / "estilos" / "raro.json").write_text(json.dumps(
        {**todos["social"], "id": "raro", "camara": "explosion_super_3d"}), encoding="utf-8")
    with pytest.raises(estilos.EstiloInvalido, match="cámara|camara"):
        estilos.estilos()


def test_aplicar_un_estilo_escribe_sus_elecciones_y_conserva_las_de_cada_lamina(datos_copia):
    from app import configuracion
    from motor import estilos
    t = _curso()
    t["escena"] = {"laminas": {"2": {"camara": "estatica"}}}
    estilos.aplicar(t, "social")
    assert t["estilo"] == "social" and t["formatos"] == ["9:16"]
    assert t["animacion"]["plantilla"] == "cinetica"
    assert t["escena"] == {"camara": "zoom_lento_entrada", "transicion": "corte", "laminas": {"2": {"camara": "estatica"}}}
    assert configuracion.para_trabajo(t)["video"]["subtitulos_quemados"] is True
    estilos.aplicar(t, "corporativo", con_formato=False)
    assert t["formatos"] == ["9:16"] and configuracion.para_trabajo(t)["video"]["subtitulos_quemados"] is False
    with pytest.raises(estilos.EstiloInvalido):
        estilos.aplicar(t, "no-existe")


def test_el_director_de_sfx_es_sobrio_y_el_de_musica_respeta_la_energia(datos_copia):
    from motor import estilos, sfx, videospec
    assert sfx.dirigir([{}, {}, {}], None) == [[], [], []]
    sutil = sfx.dirigir([{}, {"transicion_previa": "fundido"}, {"transicion_previa": "corte"}], "sutil")
    assert sutil[0] == [] and [x["id"] for x in sutil[1]] == ["transicion"] and [x["id"] for x in sutil[2]] == ["whoosh"]
    assert all(len(x) <= 1 and all(e["volumen"] <= sfx.VOLUMEN_MAXIMO for e in x) for x in sutil)
    with pytest.raises(Exception, match="taparía la voz"):
        videospec.Efecto(id="pop", volumen=-3)
    with pytest.raises(Exception, match="catálogo"):
        videospec.Efecto(id="explosion")

    pistas = [{"archivo": "a.wav", "energia": "calmada"}, {"archivo": "b.wav", "energia": "energica"}, {"archivo": "c.wav"}]
    assert estilos.elegir_musica("energica", pistas) == "b.wav"
    assert estilos.elegir_musica("media", pistas) == "c.wav"       # ninguna declara esa energía: la que no declara
    assert estilos.elegir_musica(None, pistas) is None              # el estilo no pide música
    assert estilos.elegir_musica("calmada", []) is None             # nunca se baja música de internet


def test_la_linea_de_tiempo_del_plan(datos_copia):
    from fastapi.testclient import TestClient

    from app import taller
    from app.main import app
    from motor import estilos
    t = estilos.aplicar(_curso(), "dinamico", con_formato=False)
    taller.guardar(t)
    c = TestClient(app)
    linea = c.get(f"/api/trabajos/{t['id']}/linea/v01").json()
    p = linea["pistas"]
    assert linea["resuelto"] is False and [e["lamina"] for e in p["escenas"]] == [1, 2]
    assert p["escenas"][1]["inicio"] == pytest.approx(p["escenas"][0]["duracion"], abs=0.02)
    assert len(p["voz"]) == 3 and p["voz"][0]["texto"].startswith("El riesgo vial")
    assert [x["id"] for x in p["sfx"]] == ["whoosh"] and p["musica"] == []  # no hay pistas subidas
    assert c.get(f"/api/trabajos/{t['id']}/linea/no-existe").status_code == 404
    assert len(c.get("/api/estilos").json()) == 7
    assert c.put(f"/api/trabajos/{t['id']}/estilo", json={"estilo": "nada"}).status_code == 400


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_un_video_con_estilo_lleva_su_musica_y_sus_efectos(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from fastapi.testclient import TestClient

    from app import taller
    from app.main import app
    from motor import estilos, produccion, videospec, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    _pista(datos_copia / "musica", "tranquila", "calmada")
    _pista(datos_copia / "musica", "movida", "media")
    t = estilos.aplicar(_curso(), "dinamico", con_formato=False)
    taller.guardar(t)
    informe = produccion.producir(t, "v01")
    fallas = [c for c in informe["chequeos"] if c["ok"] is False]
    assert not fallas, fallas
    spec = videospec.leer(datos_copia / "trabajos" / t["id"] / "salida" / "v01" / "videospec.json")
    assert spec.estilo_video == "dinamico" and spec.audio.musica == "movida.wav" and spec.audio.musica_elegida_por == "estilo"
    assert spec.escenas[1].sfx[0].inicio == pytest.approx(spec.escenas[1].inicio + 0.05)
    assert (datos_copia / "trabajos" / t["id"] / "cache" / "sfx" / "whoosh.wav").exists()

    linea = TestClient(app).get(f"/api/trabajos/{t['id']}/linea/v01").json()
    assert linea["resuelto"] is True and linea["pistas"]["musica"][0]["archivo"] == "movida.wav"
    assert linea["duracion"] == pytest.approx(informe["duracion"], abs=0.01)
