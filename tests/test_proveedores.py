"""Proveedores (voz, IA, render) y el control de los agentes: permisos y respuestas validadas."""

import pytest

from tests.test_taller import pptx_de_prueba


def _curso():
    from app import taller
    return taller.desde_pptx("x.pptx", pptx_de_prueba(), "Curso de prueba")


def test_cada_proveedor_cumple_su_interfaz():
    from motor import proveedores, renderers, voz
    from motor.agentes import base
    for clase in voz.PROVEEDORES.values():
        assert hasattr(clase, "extension") and callable(clase.generar)
    assert isinstance(base.LLM, proveedores.LLMProvider)
    for clase in renderers.RENDERERS.values():
        assert isinstance(clase(), proveedores.VideoRenderer)
    assert renderers.renderer("no-existe").nombre == renderers.RENDERER_DEFECTO


def test_ningun_agente_tiene_acceso_a_todo_el_curso():
    from motor.agentes import registro
    for a in registro.REGISTRO.values():
        assert a.version and a.tiempo > 0
        assert set(a.escribe) <= set(a.lee) | {"verificadas", "imagenes", "banco", "publicacion", "animacion"}
        assert not {"laminas", "videos", "marca", "voz", "origen", "id"} & set(a.escribe)


def test_un_agente_que_toca_lo_que_no_le_corresponde_no_cambia_nada(datos_copia, monkeypatch):
    from app import taller
    from motor.agentes import base, registro
    t = _curso()
    t["propuestas"] = [{"id": "p1", "agente": "publicador", "estado": "pendiente",
                        "despues": {"titulo": "T", "descripcion": "D", "etiquetas": []}}]
    taller.guardar(t)

    def aplicar_de_mas(t, p):
        t["publicacion"] = p["despues"]
        t["marca"] = "fegir"  # no le corresponde

    monkeypatch.setattr(registro.REGISTRO["publicador"], "aplicar", aplicar_de_mas)
    t = taller.cargar(t["id"])
    with pytest.raises(base.ErrorAgente, match="marca"):
        registro.aceptar(t, "p1")
    assert t["marca"] == "riskmann" and "publicacion" not in t
    assert taller.cargar(t["id"])["propuestas"][0]["estado"] == "pendiente"


def test_la_respuesta_de_la_ia_se_valida_antes_de_usarse():
    from motor.agentes.base import LLM, Contexto
    esquema = {"type": "object", "required": ["laminas"], "properties": {"laminas": {"type": "array", "items": {
        "type": "object", "required": ["n", "efecto"],
        "properties": {"n": {"type": "integer"}, "efecto": {"type": "string", "enum": ["subir", "aparecer"]}}}}}}
    respuestas = iter([
        {"laminas": [{"n": 1, "efecto": "subir"}, {"n": 2, "efecto": "explosion_super_3d"}, {"n": "3", "efecto": "subir"}]},
        {"otra_cosa": True},
        ["no", "es", "un", "objeto"],
    ])
    ctx = Contexto(con_ia=True, modelo="qwen3:4b", avisar=lambda *a: None)
    original = LLM.chat
    LLM.chat = lambda *a, **k: next(respuestas)
    try:
        assert ctx.chat("s", "u", esquema) == {"laminas": [{"n": 1, "efecto": "subir"}]}  # solo lo válido
        assert ctx.invalidas == 2
        assert ctx.chat("s", "u", esquema) is None and ctx.chat("s", "u", esquema) is None  # el agente usa reglas
        assert ctx.invalidas == 4
    finally:
        LLM.chat = original


def test_una_opcion_nueva_en_la_configuracion_no_desactualiza_los_videos(datos_copia):
    from app import configuracion
    from motor import produccion
    t = _curso()
    antes = produccion.firma(t)
    conf = configuracion.leer()
    conf["audio"]["respaldo_voz"] = False
    configuracion.guardar(conf)
    assert produccion.firma(t) == antes
    conf["audio"]["lufs"] = -16
    configuracion.guardar(conf)
    assert produccion.firma(t) != antes
