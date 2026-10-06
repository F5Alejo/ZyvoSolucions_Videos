"""Qué pasa cuando algo falla: códigos de error, reintentos, voz de respaldo y registro técnico."""

import subprocess

import pytest

from tests.test_motor import VozDePrueba, hay_ffmpeg, pptx_con_foto


def _curso(voz="kokoro-dora"):
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", voz, ["16:9"])


def test_cada_falla_tiene_codigo_severidad_y_mensaje_para_la_persona():
    import httpx

    from motor import errores, voz
    e = errores.clasificar(voz.VozNoDisponible("Falta la clave de ElevenLabs"), "voz")
    assert (e.codigo, e.severidad, e.recuperacion) == ("TTS_001", "HIGH", "ELEGIR_OTRA_VOZ")
    assert str(e) == "Falta la clave de ElevenLabs" and not e.transitorio

    red = errores.clasificar(httpx.ConnectError("sin red"), "voz")
    assert red.codigo == "TTS_002" and red.transitorio
    assert errores.clasificar(subprocess.CalledProcessError(1, "ffmpeg"), "audio").codigo == "AUDIO_001"
    raro = errores.clasificar(KeyError("x"), "escenas")
    assert raro.codigo == "MOTOR_001" and "Traceback" not in str(raro) and "KeyError" not in str(raro)
    assert all(s in errores.SEVERIDADES for s, _, _ in errores.CODIGOS.values())


def test_una_falla_pasajera_se_reintenta_y_queda_en_el_registro(datos_copia):
    import httpx

    from motor import errores, logs, produccion
    t = _curso()
    intentos = []

    def a_veces():
        intentos.append(1)
        if len(intentos) < 3:
            raise httpx.ConnectError("sin red")
        return "listo"

    assert produccion.correr(t, "v01", "voz", a_veces) == "listo" and len(intentos) == 3
    estados = [(x["stage"], x["status"], x.get("retry")) for x in logs.leer(t["id"], "v01")]
    assert estados[-1] == ("voz", "ok", 3) and ("voz", "reintento", 1) in estados

    # Lo que se repetiría igual no se reintenta.
    intentos.clear()

    def siempre():
        intentos.append(1)
        raise subprocess.CalledProcessError(1, "ffmpeg")

    with pytest.raises(errores.ErrorZyvo) as e:
        produccion.correr(t, "v01", "audio", siempre)
    assert e.value.codigo == "AUDIO_001" and len(intentos) == 1
    ultimo = logs.leer(t["id"], "v01")[-1]
    assert ultimo["error_code"] == "AUDIO_001" and "CalledProcessError" in ultimo["stacktrace"]


class _VozQueFalla:
    extension = ".mp3"

    def __init__(self, voz):
        pass

    def generar(self, texto, destino):
        from motor.voz import VozNoDisponible
        raise VozNoDisponible("ElevenLabs rechazó la clave: ¿caducó?")


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_si_falla_elevenlabs_el_video_sale_con_kokoro_y_lo_dice(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from motor import produccion, videospec, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setitem(voz.PROVEEDORES, "ElevenLabs", _VozQueFalla)
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    t = _curso("carlos")
    informe = produccion.producir(t, "v01")
    assert informe["voz"] == "kokoro-dora"
    assert informe["respaldo_voz"] == {"pedida": "carlos", "usada": "kokoro-dora",
                                       "motivo": "ElevenLabs rechazó la clave: ¿caducó?"}
    assert any("Se usó la voz Dora" in a for a in informe["avisos"])
    salida = datos_copia / "trabajos" / t["id"] / "salida" / "v01"
    assert videospec.leer(salida / "videospec.json").voz.id == "kokoro-dora"
    assert not [c for c in informe["chequeos"] if c["ok"] is False]
    assert informe["bugs"] == [] and {"saturacion", "caracteres", "contenido"} <= {c["id"] for c in informe["chequeos"]}


def test_sin_respaldo_la_falla_llega_clasificada_a_la_cola(datos_copia, monkeypatch):
    from app import configuracion
    from motor import cola, voz
    monkeypatch.setitem(voz.PROVEEDORES, "ElevenLabs", _VozQueFalla)
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    conf = configuracion.leer()
    conf["audio"]["respaldo_voz"] = False
    configuracion.guardar(conf)
    t = _curso("carlos")
    cola.encolar(t["id"], "v01")
    cola.esperar()
    e = cola.estado(t["id"], "v01")
    assert e["estado"] == "error" and e["fase"] == "FAILED"
    assert e["codigo"] == "TTS_001" and e["recuperacion"] == "ELEGIR_OTRA_VOZ"
    assert e["mensaje"] == "ElevenLabs rechazó la clave: ¿caducó?"


def test_el_modo_diagnostico_muestra_el_registro_del_video(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    from motor import logs
    t = _curso()
    logs.escribir(t["id"], "v01", "voz", "ok", intento=1)
    c = TestClient(app)
    d = c.get(f"/api/trabajos/{t['id']}/diagnostico/v01").json()
    assert d["eventos"][0]["stage"] == "voz" and d["estado"] is None
    assert c.get(f"/api/trabajos/{t['id']}/diagnostico/..%2F..").status_code == 404


def test_el_detector_convierte_chequeos_fallidos_en_bugs(datos_copia):
    from app import taller
    from motor import bugs, produccion, videospec
    t = _curso()
    spec = videospec.construir(t, "v01", produccion.firma(t))
    laminas = taller.resumen(t)["videos"][0]["laminas_detalle"]
    assert bugs.detectar(bugs.chequeos_de_contenido(spec, laminas), spec) == []

    d = spec.model_dump()
    d["escenas"][1]["vista"]["titulo"] = "Conducci�n"
    d["escenas"][1]["vista"]["imagen"] = None  # la lámina 2 trae foto
    malo = videospec.validar(d)
    chequeos = bugs.chequeos_de_contenido(malo, laminas)
    chequeos.append({"id": "volumen", "ok": False, "titulo": "Volumen a -14 LUFS", "detalle": "-20 LUFS"})
    chequeos.append({"id": "estimada", "ok": None, "titulo": "Informativo", "detalle": ""})
    encontrados = bugs.detectar(chequeos, malo)
    assert [(b["bug"], b["severity"], b["scene"]) for b in encontrados] == [
        ("CONTENT_001", "HIGH", "escena-002"), ("AUDIO_002", "MEDIUM", None), ("TEXT_002", "LOW", "escena-002")]
    assert encontrados[0]["recovery"] == "REVISAR_CURSO"
