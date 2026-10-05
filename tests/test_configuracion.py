import io
import json
import shutil
import subprocess

import numpy as np
import pytest
import soundfile as sf

from tests.test_motor import ORIGEN, VozDePrueba, hay_ffmpeg, pptx_con_foto


@pytest.fixture()
def datos_copia(tmp_path, monkeypatch):
    copia = tmp_path / "datos"
    shutil.copytree(ORIGEN, copia, ignore=shutil.ignore_patterns("trabajos", "empresas", "musica"))
    from app import datos
    monkeypatch.setattr(datos, "RAIZ_DATOS", copia)
    return copia


@pytest.fixture()
def cliente(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    return TestClient(app)


def test_lo_que_falta_en_el_archivo_toma_el_valor_por_defecto(datos_copia):
    from app import configuracion
    (datos_copia / "configuracion.json").write_text('{"video": {"fps": 25}}', encoding="utf-8")
    conf = configuracion.leer()
    assert conf["video"]["fps"] == 25 and conf["video"]["resolucion"] == "1080p"
    assert conf["tiempos"] == configuracion.DEFECTO["tiempos"]


@pytest.mark.parametrize("cambio, error", [
    ({"video": {"fps": 24}}, "video.fps"),
    ({"audio": {"lufs": -30}}, "audio.lufs"),
    ({"tiempos": {"pausa": 9}}, "tiempos.pausa"),
    ({"tiempos": {"entrada": "uno"}}, "tiempos.entrada"),
    ({"video": {"subtitulos_quemados": "sí"}}, "subtitulos_quemados"),
    ({"cursos": {"voz": "inventada"}}, "voz"),
    ({"audio": {"musica": "no-existe.mp3"}}, "música"),
    ({"agentes": {"url": "localhost"}}, "Ollama"),
])
def test_la_configuracion_invalida_se_rechaza(cliente, cambio, error):
    r = cliente.put("/api/configuracion", json=cambio)
    assert r.status_code == 400 and error in r.json()["detail"]


def test_guardar_y_cursos_nuevos_usan_lo_configurado(cliente, datos_copia):
    conf = cliente.get("/api/configuracion").json()
    assert {"video.fps", "audio.lufs", "tiempos.pausa"} <= set(conf["opciones"])
    nueva = conf["configuracion"]
    nueva["cursos"].update(voz="kokoro-dora", marca="fegir")
    assert cliente.put("/api/configuracion", json=nueva).status_code == 200
    guardada = json.loads((datos_copia / "configuracion.json").read_text(encoding="utf-8"))
    assert guardada["cursos"]["voz"] == "kokoro-dora"

    id_ = cliente.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_con_foto())}).json()["id"]
    t = cliente.get(f"/api/trabajos/{id_}").json()["trabajo"]
    assert (t["voz"], t["marca"]) == ("kokoro-dora", "fegir")


def test_ajustes_por_curso_solo_pisan_lo_que_cambian(cliente):
    id_ = cliente.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_con_foto())}).json()["id"]
    r = cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": {"video": {"fps": 60}, "cursos": {"voz": "x"}}})
    assert r.status_code == 200
    ef = r.json()["ajustes_efectivos"]
    assert ef["video"]["fps"] == 60 and ef["video"]["resolucion"] == "1080p"
    assert cliente.get(f"/api/trabajos/{id_}/ajustes-video").json()["propios"] == {"video": {"fps": 60}}  # «cursos» no se puede por curso
    assert cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": {"video": {"fps": 7}}}).status_code == 400
    cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": None})
    assert cliente.get(f"/api/trabajos/{id_}/ajustes-video").json()["propios"] == {}


def _tono(segundos=4.0, hz=330) -> bytes:
    t = np.arange(int(48000 * segundos)) / 48000
    buf = io.BytesIO()
    sf.write(buf, (0.4 * np.sin(2 * np.pi * hz * t)).astype(np.float32), 48000, format="WAV")
    return buf.getvalue()


def test_la_musica_exige_licencia(cliente):
    r = cliente.post("/api/musica", files={"archivo": ("fondo.wav", _tono())}, data={"licencia": ""})
    assert r.status_code == 400
    r = cliente.post("/api/musica", files={"archivo": ("../fondo raro.wav", _tono())}, data={"licencia": "Pixabay Content License"})
    assert r.status_code == 201
    assert r.json() == [{"archivo": "fondo-raro.wav", "licencia": "Pixabay Content License", "fuente": "", "energia": None}]
    assert cliente.get("/api/musica/fondo-raro.wav").status_code == 200
    assert cliente.get("/api/musica/..%2Fconfiguracion.json").status_code == 404


def test_el_sistema_dice_que_hay_y_que_falta(cliente):
    s = cliente.get("/api/sistema?forzar=true").json()
    assert {"ffmpeg", "chromium", "elevenlabs", "voces", "ollama", "disco"} <= set(s)
    assert "sk_" not in json.dumps(s)  # la clave nunca sale


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_producir_con_la_configuracion_del_curso(cliente, monkeypatch):
    pytest.importorskip("playwright")
    from motor import cola, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setattr(voz, "disponible", lambda v: None)

    cliente.post("/api/musica", files={"archivo": ("fondo.wav", _tono(3.0))}, data={"licencia": "Propia"})
    id_ = cliente.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_con_foto())}).json()["id"]
    cliente.patch(f"/api/trabajos/{id_}", json={"marca": "riskmann", "voz": "kokoro-dora", "formatos": ["16:9"]})
    ajustes = {"video": {"fps": 25, "resolucion": "720p", "calidad": "borrador", "subtitulos_quemados": True},
               "audio": {"lufs": -16, "musica": "fondo.wav", "musica_volumen": -20},
               "tiempos": {"entrada": 0.5, "pausa": 0.2, "salida": 0.8}}
    assert cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": ajustes}).status_code == 200

    cliente.post(f"/api/trabajos/{id_}/producir/v01")
    cola.esperar()
    v = cliente.get(f"/api/trabajos/{id_}/produccion").json()["videos"]["v01"]
    assert v["estado"] == "listo", v
    chequeos = {c["titulo"]: c for c in v["informe"]["chequeos"]}
    assert chequeos["Resolución y cuadros por segundo"]["detalle"] == "1280×720 a 25 fps"
    assert chequeos["Volumen a -16 LUFS"]["ok"] is True
    assert not [c for c in v["informe"]["chequeos"] if c["ok"] is False]

    # Cambiar un ajuste deja el video desactualizado.
    cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": {**ajustes, "tiempos": {"pausa": 0.5}}})
    assert cliente.get(f"/api/trabajos/{id_}/produccion").json()["videos"]["v01"]["desactualizado"] is True


# ── Curso completo y paquete ─────────────────────────────────────────────────

@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_producir_todo_arma_el_mp4_completo_y_el_zip(cliente, monkeypatch):
    pytest.importorskip("playwright")
    import hashlib
    import zipfile

    from app import taller
    from motor import cola, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setattr(voz, "disponible", lambda v: None)

    id_ = cliente.post("/api/trabajos", files={"archivo": ("x.pptx", pptx_con_foto())}).json()["id"]
    cliente.patch(f"/api/trabajos/{id_}", json={"marca": "riskmann", "voz": "kokoro-dora", "formatos": ["16:9"]})
    t = taller.cargar(id_)
    t["videos"] = [{"clave": "v01", "titulo": "Uno", "laminas": [1]}, {"clave": "v02", "titulo": "Dos", "laminas": [2]}]
    taller.guardar(t)

    # Sin videos no hay completo ni paquete.
    assert cliente.post(f"/api/trabajos/{id_}/completo").status_code == 400
    assert cliente.get(f"/api/trabajos/{id_}/paquete.zip").status_code == 400

    assert cliente.post(f"/api/trabajos/{id_}/producir-todo").status_code == 202
    cola.esperar()
    p = cliente.get(f"/api/trabajos/{id_}/produccion").json()
    assert (p["listos"], p["total"], p["pendientes"]) == (2, 2, [])
    c = p["completo"]
    assert c["estado"] == "listo", c
    assert all(x["ok"] for x in c["informe"]["chequeos"])

    mp4 = cliente.get(c["archivos"]["mp4"])
    assert mp4.status_code == 200
    capitulos = cliente.get(c["archivos"]["capitulos"]).text.splitlines()
    assert capitulos[0] == "0:00 Uno" and capitulos[1].endswith(" Dos")
    from app import datos
    ruta = datos.RAIZ_DATOS / "trabajos" / id_ / "salida" / "completo" / "completo.mp4"
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-show_format", "-of", "json", str(ruta)],
                                     capture_output=True, text=True).stdout)
    assert [x["tags"]["title"] for x in info["chapters"]] == ["Uno", "Dos"]
    # El segundo video empieza después de la tarjeta de 3 s, el primer video y la segunda tarjeta.
    inicio_dos = c["informe"]["capitulos"][1]["inicio"]
    vtt = cliente.get(c["archivos"]["vtt"]).text
    assert "Ley 1503 de 2011" in vtt and "Anticipa lo que harán los demás." in vtt
    ultimo = [l for l in vtt.splitlines() if "-->" in l][-1]
    assert float(ultimo.split(" --> ")[0].split(":")[-1]) + 60 * int(ultimo.split(":")[1]) > inicio_dos

    z = cliente.get(f"/api/trabajos/{id_}/paquete.zip")
    assert z.status_code == 200 and z.headers["content-type"] == "application/zip"
    with zipfile.ZipFile(io.BytesIO(z.content)) as paquete:
        nombres = set(paquete.namelist())
        assert {"v01/v01.mp4", "v02/v02.srt", "completo/completo.mp4", "completo/capitulos.txt", "manifiesto.json"} <= nombres
        manifiesto = json.loads(paquete.read("manifiesto.json"))
        for a in manifiesto["archivos"]:
            assert hashlib.sha256(paquete.read(a["ruta"])).hexdigest() == a["sha256"]

    # Un cambio deja todo desactualizado; el completo también.
    cliente.put(f"/api/trabajos/{id_}/ajustes-video", json={"ajustes": {"tiempos": {"pausa": 0.6}}})
    p = cliente.get(f"/api/trabajos/{id_}/produccion").json()
    assert p["completo"]["desactualizado"] and p["listos"] == 0 and len(p["pendientes"]) == 2
