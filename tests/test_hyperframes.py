"""El envoltorio de HyperFrames: cómo se arma el proyecto y cómo se lee su informe."""

import json

from motor import hyperframes
from motor.escenas import lamina as mod_lamina


def test_el_proyecto_queda_con_la_forma_que_espera_hyperframes(tmp_path):
    p = hyperframes.preparar(tmp_path / "hf", "v01")
    assert (p / "compositions").is_dir()
    conf = json.loads((p / "hyperframes.json").read_text(encoding="utf-8"))
    assert conf["paths"]["blocks"] == "compositions"
    assert conf["media"]["autoProxy"] is False  # nada sale a internet: es material del cliente

    hyperframes.escribir(p, "<html>indice</html>", {"compositions/e1.html": "<html>uno</html>"})
    assert (p / "index.html").read_text(encoding="utf-8") == "<html>indice</html>"
    assert (p / "compositions" / "e1.html").read_text(encoding="utf-8") == "<html>uno</html>"


def test_la_tipografia_y_las_imagenes_viajan_con_el_proyecto(tmp_path):
    """El render no puede depender de internet ni de lo que haya instalado el equipo."""
    media = tmp_path / "media"
    media.mkdir()
    (media / "foto.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    p = hyperframes.preparar(tmp_path / "hf")
    hyperframes.copiar_recursos(p, mod_lamina.FUENTE, media)
    assert (p / "assets" / "fuentes" / mod_lamina.FUENTE.name).exists()
    assert (p / "assets" / "media" / "foto.png").exists()


def _check(datos: dict, monkeypatch, codigo=0):
    class R:
        stdout, stderr, returncode = json.dumps(datos), "", codigo
    monkeypatch.setattr(hyperframes, "_correr", lambda *a, **k: R())


def test_un_informe_limpio_no_inventa_problemas(monkeypatch, tmp_path):
    _check({"ok": True, "browserSkipped": False,
            "lint": {"findings": []}, "layout": {"findings": []}}, monkeypatch)
    assert hyperframes.revisar(tmp_path) == []


def test_se_leen_los_errores_de_todas_las_secciones_y_no_los_avisos(monkeypatch, tmp_path):
    _check({"ok": False, "browserSkipped": False,
            "lint": {"findings": [{"code": "mal_root", "severity": "error", "message": "root mal",
                                   "sourceFile": "/x/compositions/e1.html"}]},
            "layout": {"findings": [{"code": "overflow", "severity": "error", "message": "se sale"}]},
            "contrast": {"findings": [{"code": "contraste", "severity": "warning", "message": "flojo"}]}},
           monkeypatch, codigo=1)
    r = hyperframes.revisar(tmp_path)
    assert len(r) == 2, "los avisos no son errores"
    assert "[lint] mal_root en e1.html" in r[0]
    assert "[layout] overflow" in r[1]


def test_un_cero_con_el_navegador_apagado_no_es_un_aprobado(monkeypatch, tmp_path):
    """Un error de lint apaga la auditoría, y layout/contraste vuelven en cero sin haber mirado.

    Leer solo los contadores daba un «limpio» que no significaba nada: así se nos coló durante
    varias pasadas un texto que se salía de su caja.
    """
    _check({"ok": False, "browserSkipped": True,
            "lint": {"findings": [{"code": "mal_root", "severity": "error", "message": "root mal"}]},
            "layout": {"findings": []}, "contrast": {"findings": []}}, monkeypatch, codigo=1)
    r = hyperframes.revisar(tmp_path)
    assert any("no llegó a correr" in x for x in r)


def test_sin_node_el_error_dice_que_instalar():
    d = hyperframes.disponible()
    assert set(d) >= {"ok", "detalle"}
    if not d["ok"]:
        assert d.get("arreglo"), "si falta algo, hay que decir cómo arreglarlo"
