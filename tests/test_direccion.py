"""El Director de ritmo, el banco de medios y el renderer HyperFrames."""

import io
import shutil
import subprocess

import pytest

from tests.test_motor import VozDePrueba, hay_ffmpeg, pptx_con_foto


def _curso():
    from app import taller
    t = taller.desde_pptx("x.pptx", pptx_con_foto(), "Curso de prueba")
    return taller.ajustar(t, "riskmann", "kokoro-dora", ["16:9"])


def _spec(t, tmp_path, frases=None):
    """El VideoSpec resuelto con una duración fija por frase (sin generar voz)."""
    from motor import produccion, videospec
    spec = videospec.construir(t, "v01", produccion.firma(t))
    if frases:
        d = spec.model_dump()
        d["escenas"][0]["narracion"] = [{"texto": f, "texto_voz": f} for f in frases]
        spec = videospec.validar(d)
    wav = tmp_path / "f.wav"
    wav.write_bytes(b"")
    return videospec.resolver(spec, generar=lambda texto: wav, duracion_de=lambda w: 2.0)


def _foto(color=(200, 30, 30)) -> bytes:
    from PIL import Image
    b = io.BytesIO()
    Image.new("RGB", (64, 48), color).save(b, "PNG")
    return b.getvalue()


def _subir(marca, nombre, contenido, tmp_path, **campos):
    from app import banco
    origen = tmp_path / f"subida-{nombre}"
    origen.write_bytes(contenido)
    return banco.agregar(marca, nombre, origen, **campos)


# ── Trozos y reglas ──────────────────────────────────────────────────────────

def test_una_frase_larga_se_parte_y_cada_palabra_tiene_su_segundo():
    from motor import direccion
    f = {"texto": "Fumado, efecto en minutos, dura de una a tres horas y daña las vías respiratorias.",
         "inicio": 10.0, "duracion": 6.0}
    ts = direccion.trozos(f)
    assert len(ts) >= 2 and sum(len(x["palabras"]) for x in ts) == len(f["texto"].split())
    tiempos = [s for x in ts for s in x["tiempos"]]
    assert tiempos == sorted(tiempos) and tiempos[0] == 10.0 and ts[-1]["fin"] == pytest.approx(16.0)


def test_las_reglas_nunca_quitan_una_negacion_ni_la_unidad_de_una_cifra():
    from motor import direccion
    for frase, debe in [("No produce efecto psicoactivo.", "No produce efecto psicoactivo"),
                        ("Efecto en minutos; dura 1–3 h.", "1–3 h"),
                        ("El consumo frecuente nunca es seguro para la salud mental de nadie", "nunca")]:
        palabras = [direccion._limpia(p) for p in frase.split()]
        i, j = direccion._ventana(palabras)
        assert debe in " ".join(palabras[i:j]), (frase, palabras[i:j])
    assert direccion._etiqueta("¿Qué es el cannabis?") == "CANNABIS"


def test_la_ia_solo_puede_elegir_palabras_de_la_frase_y_tomas_del_banco():
    from motor import direccion
    lista = [{"n": 1, "palabras": "El CBD no produce efecto psicoactivo.".split()},
             {"n": 2, "palabras": "Tarda treinta minutos en hacer efecto.".split()}]
    r = {"momentos": [
        {"n": 1, "texto": "produce efecto psicoactivo", "resaltado": ["psicoactivo"], "etiqueta": "cbd", "toma": "x1"},
        {"n": 2, "texto": "tarda cuarenta minutos", "resaltado": ["cuarenta"], "etiqueta": "", "toma": "inventada"},
    ]}
    d = direccion._con_ia(r, lista, {"x1", "marca"})
    assert 2 not in d  # «cuarenta» no lo dice la voz: ese momento va con reglas
    uno = d[1]
    assert " ".join(lista[0]["palabras"][uno["desde"]:uno["hasta"]]).startswith("no produce")  # el «no» vuelve
    assert uno["toma"] == "x1" and uno["etiqueta"] == "CBD"
    assert lista[0]["palabras"][uno["desde"] + uno["resaltado"][0]].startswith("psicoactivo")


def test_el_director_arma_momentos_validos_para_cada_frase(datos_copia, tmp_path):
    from motor import direccion
    t = _curso()
    spec = direccion.dirigir(_spec(t, tmp_path), t)
    for e in spec.escenas:
        assert e.beats and e.beats[0].inicio == 0
        assert e.beats[-1].fin == pytest.approx(e.cuadros / spec.video.fps, abs=0.01)
        for a, b in zip(e.beats, e.beats[1:]):
            assert a.fin == b.inicio  # sin huecos: siempre hay algo en pantalla
        for b in e.beats:
            assert len(b.palabras) == len(b.texto.split()) and b.resaltado


def test_las_tomas_salen_del_banco_por_lo_que_dice_la_voz(datos_copia, tmp_path):
    from motor import direccion
    t = _curso()
    impresora = _subir(t["marca"], "impresora.png", _foto(), tmp_path, descripcion="La impresora de resina imprimiendo",
                       etiquetas="impresora, resina")
    general = _subir(t["marca"], "taller.png", _foto((0, 90, 200)), tmp_path, etiquetas="general")
    frases = ["La impresora de resina trabaja capa por capa.", "Después se limpia la pieza con alcohol.",
              "La resina sobrante se recicla en la impresora."]
    spec = direccion.dirigir(_spec(t, tmp_path, frases), t)
    tomas = [b.toma for b in spec.escenas[0].beats]
    assert tomas[0].id == impresora["id"] and tomas[0].tipo == "foto"
    assert tomas[1].id == general["id"]  # nada coincide: la toma «general»


def test_un_clip_no_repite_el_mismo_pedazo(monkeypatch):
    from pathlib import Path

    from app import banco
    from motor import direccion
    monkeypatch.setattr(banco, "ruta", lambda marca, archivo: Path(archivo))
    tomas = direccion.Tomas([{"id": "c", "tipo": "clip", "archivo": "c.mp4", "duracion": 10.0, "etiquetas": []}], "m")
    a, b, c = (tomas.toma("c", 4.0, None) for _ in range(3))
    assert (a.desde, b.desde, c.desde) == (0.0, 4.0, 0.0)  # el tercero ya no cabe: vuelve al principio


# ── Banco ────────────────────────────────────────────────────────────────────

def test_el_banco_revisa_lo_que_entra(datos_copia, tmp_path):
    from app import banco
    item = _subir("riskmann", "foto.png", _foto(), tmp_path, descripcion="  Una foto  ", etiquetas="Taller, taller, Resina")
    assert item["tipo"] == "foto" and item["etiquetas"] == ["taller", "resina"] and item["descripcion"] == "Una foto"
    with pytest.raises(banco.BancoInvalido, match="Sube un video"):
        _subir("riskmann", "virus.exe", b"MZ", tmp_path)
    with pytest.raises(banco.BancoInvalido, match="no se pudo abrir"):
        _subir("riskmann", "rota.png", b"no es una imagen", tmp_path)
    assert banco.ruta("riskmann", "../../configuracion.json") is None
    with pytest.raises(banco.BancoInvalido):
        banco.listar("../otra")
    banco.actualizar("riskmann", item["id"], etiquetas=["general"])
    assert banco.listar("riskmann")[0]["etiquetas"] == ["general"]
    banco.eliminar("riskmann", item["id"])
    assert banco.listar("riskmann") == [] and not list(banco.carpeta("riskmann").glob("*.png"))


def test_el_banco_por_la_api(datos_copia):
    from fastapi.testclient import TestClient

    from app.main import app
    c = TestClient(app)
    r = c.post("/api/marcas/riskmann/banco", files={"archivo": ("toma.png", _foto(), "image/png")},
               data={"descripcion": "La pieza terminada", "etiquetas": "pieza, resultado"})
    assert r.status_code == 201, r.text
    item = r.json()
    lista = c.get("/api/marcas/riskmann/banco").json()
    assert [x["id"] for x in lista] == [item["id"]]
    assert c.get(f"/api/marcas/riskmann/banco/{item['id']}/archivo").status_code == 200
    assert c.patch(f"/api/marcas/riskmann/banco/{item['id']}", json={"etiquetas": ["general"]}).json()["etiquetas"] == ["general"]
    assert c.delete(f"/api/marcas/riskmann/banco/{item['id']}").status_code == 204
    assert c.get("/api/marcas/no-existe/banco").status_code == 404


# ── Composición y render ─────────────────────────────────────────────────────

def test_la_composicion_lleva_cada_palabra_con_su_tiempo(datos_copia, tmp_path):
    from motor import direccion, hyperframes
    if not hyperframes.GSAP.exists():
        pytest.skip("faltan las dependencias de HyperFrames")
    t = _curso()
    spec = direccion.dirigir(_spec(t, tmp_path, ["Son 100 cannabinoides.", "No produce efecto psicoactivo."]), t)
    indice, usados = hyperframes.componer(spec, tmp_path / "hf")
    html = indice.read_text(encoding="utf-8")
    assert 'data-cuenta="100"' in html and ">No</span>" in html and 'class="w on"' in html
    assert (tmp_path / "hf" / "assets" / "gsap.min.js").exists() and "cdn." not in html  # nada de internet
    assert hyperframes.huella(indice, usados, spec) == hyperframes.huella(indice, usados, spec)


def test_el_tamano_del_texto_cabe_en_la_pantalla():
    from motor import hyperframes
    c = hyperframes.capa(1080, 1920)
    larga = hyperframes.tam_letra(["Tetrahidrocannabinol"], "termino", c)
    assert larga * 0.74 * (len("Tetrahidrocannabinol") + 0.6) <= c["ancho_texto"]
    assert hyperframes.tam_letra(["THC"], "termino", c) > larga


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_un_video_completo_con_hyperframes(datos_copia, con_hyperframes, monkeypatch):
    """De punta a punta (tarda ~1-2 min): el video sale con los cuadros exactos que pide la voz."""
    from motor import produccion, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    t = _curso()
    informe = produccion.producir(t, "v01")
    assert informe["bugs"] == [] or all(b["codigo"] != "RENDER_001" for b in informe["bugs"])
    mp4 = produccion.carpeta_salida(t, "v01") / "v01.mp4"
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets,width,height", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True)
    ancho, alto, cuadros = (int(x) for x in r.stdout.strip().split(","))
    assert (ancho, alto) == (1920, 1080) and cuadros == round(informe["duracion"] * 30)
    assert shutil.which("node")
