"""La cola: renders y agentes en carriles aparte, varios a la vez y con turno justo entre cursos."""

import threading

import pytest

from tests.test_agentes import _curso


@pytest.fixture()
def render_lento(monkeypatch):
    """Un «render» que no termina hasta que la prueba suelta `seguir`; anota cuántos corren a la vez."""
    from motor import produccion
    seguir, empezaron = threading.Event(), []
    corriendo, maximo = [], [0]

    def producir(t, clave, avisar=None, fase=None):
        corriendo.append(clave)
        maximo[0] = max(maximo[0], len(corriendo))
        empezaron.append((t["id"], clave))
        assert seguir.wait(10)
        corriendo.remove(clave)
    monkeypatch.setattr(produccion, "producir", producir)
    return seguir, empezaron, maximo


def _limites(render=2, agentes=4):
    from app import configuracion
    conf = configuracion.leer()
    conf["cola"] = {"render": render, "agentes": agentes}
    configuracion.guardar(conf)


def test_un_agente_no_espera_a_que_termine_un_render(datos_copia, sin_ollama, render_lento):
    from motor import cola
    seguir, _, _ = render_lento
    _limites(render=1)
    t = _curso()
    cola.encolar(t["id"], "v01")
    cola.encolar(t["id"], f"{cola.PREFIJO_AGENTE}verificador")
    for _ in range(100):  # el agente termina mientras el render sigue
        if cola.estado(t["id"], f"{cola.PREFIJO_AGENTE}verificador")["estado"] == "listo":
            break
        threading.Event().wait(0.05)
    assert cola.estado(t["id"], f"{cola.PREFIJO_AGENTE}verificador")["estado"] == "listo"
    assert cola.estado(t["id"], "v01")["estado"] == "produciendo"
    seguir.set()
    cola.esperar()
    assert cola.estado(t["id"], "v01")["estado"] == "listo"


def test_varios_renders_a_la_vez_sin_pasar_el_limite(datos_copia, render_lento):
    from motor import cola
    seguir, empezaron, maximo = render_lento
    _limites(render=2)
    t = _curso()
    for clave in ("a", "b", "c", "d"):
        cola.encolar(t["id"], clave)
    for _ in range(100):
        if len(empezaron) == 2:
            break
        threading.Event().wait(0.05)
    threading.Event().wait(0.2)
    assert len(empezaron) == 2  # el tercero espera su turno
    seguir.set()
    cola.esperar()
    assert len(empezaron) == 4 and maximo[0] == 2


def test_el_turno_es_justo_entre_cursos():
    from motor import cola
    # El curso A tiene uno corriendo; B llegó después, pero no tiene ninguno: va primero.
    pendientes = [("A", "v02"), ("A", "v03"), ("B", "v01")]
    listos = [x for i, x in enumerate(pendientes) if cola._puede_empezar(x, pendientes[:i], [("A", "v01")])]
    siguiente = min(listos, key=lambda x: sum(1 for c in [("A", "v01")] if c[0] == x[0]))
    assert siguiente == ("B", "v01")


def test_el_paquete_corre_solo_y_despues_de_los_videos_del_curso():
    from motor import cola, empaquetar
    paquete = ("A", empaquetar.CLAVE)
    assert not cola._puede_empezar(paquete, [], [("A", "v01")])         # un video del curso corriendo
    assert not cola._puede_empezar(paquete, [("A", "v02")], [])         # un video pedido antes
    assert cola._puede_empezar(paquete, [("B", "v01")], [("B", "v02")])  # otro curso no lo frena
    assert not cola._puede_empezar(("A", "v03"), [], [paquete])          # mientras se arma, nada del curso
    assert cola._puede_empezar(("B", "v03"), [], [paquete])


def test_los_limites_de_la_cola_se_validan(datos_copia):
    from app import configuracion
    from motor import cola
    conf = configuracion.leer()
    assert conf["cola"] == {"render": None, "agentes": 4} and cola.limite("render") >= 1
    for malo in ({"render": 0}, {"agentes": 9}, {"agentes": None}, {"render": True}, {"otro": 1}):
        with pytest.raises(ValueError):
            configuracion.guardar({**conf, "cola": {**conf["cola"], **malo}})
