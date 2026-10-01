"""VideoSpec: el contrato entre el curso y el render, y la caché de escenas que permite regenerar por partes."""

import json
import shutil

import pytest
from test_motor import VozDePrueba, pptx_con_foto

hay_ffmpeg = shutil.which("ffmpeg") is not None


def _curso():
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", "kokoro-dora", ["16:9"])


def test_el_plan_describe_cada_escena_con_datos_del_catalogo(datos_copia):
    from motor import produccion, videospec
    t = _curso()
    spec = videospec.construir(t, "v01", produccion.firma(t))
    assert not spec.resuelto and spec.version == videospec.VERSION
    assert [e.lamina for e in spec.escenas] == [1, 2]
    assert spec.escenas[0].vista["tipo"] == "portada" and spec.escenas[1].vista["tipo"] == "imagen"
    primera = spec.escenas[0].narracion[1]
    assert primera.texto == "Lo exige la Ley 1503 de 2011."           # los subtítulos, tal cual
    assert "mil quinientos tres" in primera.texto_voz                   # la voz, en palabras
    assert all(e.duracion_estimada > 0 and e.camara == "estatica" and e.transicion == "corte" for e in spec.escenas)
    assert (spec.video.ancho, spec.video.alto, spec.video.fps) == (1920, 1080, 30)


def test_lo_que_no_esta_en_el_catalogo_no_se_ejecuta(datos_copia):
    from motor import produccion, videospec
    t = _curso()
    d = videospec.construir(t, "v01", produccion.firma(t)).model_dump()

    d["escenas"][0]["camara"] = "explosion_super_3d"
    with pytest.raises(videospec.VideoSpecInvalido, match="cámara"):
        videospec.validar(json.loads(json.dumps(d)))
    corregido, avisos = videospec.sanear(d)
    assert corregido["escenas"][0]["camara"] == "estatica" and avisos[0].startswith("INVALID_EFFECT")
    videospec.validar(corregido)

    for campo, valor, error in [(("video", "fps"), 24, "fps"), (("video", "formato"), "21:9", "formato"),
                                (("version",), 99, "v99")]:
        malo = json.loads(json.dumps(corregido))
        destino = malo
        for k in campo[:-1]:
            destino = destino[k]
        destino[campo[-1]] = valor
        with pytest.raises(videospec.VideoSpecInvalido, match=error):
            videospec.validar(malo)

    malo = json.loads(json.dumps(corregido))
    malo["escenas"][1]["animacion"]["elementos"]["titulo"]["entrada"]["efecto"] = "inventado"
    with pytest.raises(videospec.VideoSpecInvalido):
        videospec.validar(malo)


def test_resolver_fija_la_linea_de_tiempo_en_cuadros_exactos(datos_copia, tmp_path):
    from motor import produccion, videospec
    t = _curso()
    spec = videospec.construir(t, "v01", produccion.firma(t))
    wav = tmp_path / "x.wav"
    r = videospec.resolver(spec, generar=lambda texto: wav, duracion_de=lambda w: 1.5)
    assert r.resuelto
    e0, e1 = r.escenas
    assert e0.inicio == 0 and e1.inicio == pytest.approx(e0.cuadros / 30)
    assert e0.narracion[0].inicio == pytest.approx(r.tiempos.entrada)
    assert e0.narracion[1].inicio == pytest.approx(r.tiempos.entrada + 1.5 + r.tiempos.pausa)
    assert r.duracion == pytest.approx((e0.cuadros + e1.cuadros) / 30)
    # Un plan sin resolver no sirve como resuelto.
    d = spec.model_dump() | {"resuelto": True}
    with pytest.raises(videospec.VideoSpecInvalido, match="cuadros"):
        videospec.validar(d)


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_editar_una_lamina_solo_vuelve_a_dibujar_su_escena(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from app import taller
    from motor import produccion, videospec, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    t = _curso()
    produccion.producir(t, "v01")
    salida = datos_copia / "trabajos" / t["id"] / "salida" / "v01"
    assert videospec.leer(salida / "videospec.json").resuelto
    assert (salida / "videospec.plan.json").exists()
    antes = {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")}
    assert len(antes) == 2

    # Sin cambios: ninguna escena se vuelve a dibujar.
    produccion.producir(taller.cargar(t["id"]), "v01")
    assert {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")} == antes

    # Se edita lo que se ve en la lámina 2: solo cambia su escena; la vieja se borra.
    t = taller.editar_lamina(taller.cargar(t["id"]), 2, {"titulo": "Anticipa siempre"})
    informe = produccion.producir(t, "v01")
    despues = {p.name: p.stat().st_mtime_ns for p in (salida / "escenas").glob("*.mp4")}
    assert len(despues) == 2 and len(set(despues) & set(antes)) == 1
    comun = (set(despues) & set(antes)).pop()
    assert despues[comun] == antes[comun]
    assert not [c for c in informe["chequeos"] if c["ok"] is False]
