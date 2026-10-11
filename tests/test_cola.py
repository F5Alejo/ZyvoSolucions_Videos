"""Los carriles de la cola: un render no deja la interfaz sin poder hacer nada más.

Antes todo compartía una cola y un hilo, así que pedir un video bloqueaba también a los
agentes. Ahora cada tipo de trabajo tiene su carril (`motor/cola.CARRILES`).
"""

import threading
import time

from motor import cola


def test_cada_trabajo_va_a_su_carril():
    assert cola.carril("v01") == "render"
    assert cola.carril("completo") == "render"
    assert cola.carril(f"{cola.PREFIJO_AGENTE}redactor") == "agentes"
    assert set(cola.CARRILES) == {"render", "agentes"}


def test_un_render_largo_no_bloquea_a_un_agente(monkeypatch, tmp_path):
    """Lo que el usuario reportaba: con un video en curso no se podía generar nada más."""
    arrancado = threading.Event()
    soltar = threading.Event()
    hecho = threading.Event()

    def produccion_lenta(t, clave, avisar, fase):
        arrancado.set()
        assert soltar.wait(10), "el render se quedó esperando para siempre"

    def agente_rapido(id_, nombre, avisar):
        hecho.set()
        return {"propuestas": [], "con_ia": False}

    monkeypatch.setattr(cola.produccion, "producir", produccion_lenta)
    monkeypatch.setattr(cola.taller, "cargar", lambda id_: {"id": id_, "videos": []})
    monkeypatch.setattr(cola, "_escribir", lambda *a, **k: None)
    from motor.agentes import registro
    monkeypatch.setattr(registro, "ejecutar", agente_rapido)

    assert cola.encolar("curso", "v01") is True
    assert arrancado.wait(10), "el render no arrancó"

    # Con el render ocupando su carril, el agente tiene que poder correr igual.
    assert cola.encolar("curso", f"{cola.PREFIJO_AGENTE}redactor") is True
    assert hecho.wait(10), "el agente se quedó esperando al render: los carriles no funcionan"

    soltar.set()
    cola.esperar()


def test_dos_renders_siguen_yendo_de_a_uno(monkeypatch):
    """El carril de render es de uno: dos videos a la vez saturarían el equipo."""
    a_la_vez, maximo = [], [0]
    candado = threading.Lock()

    def produccion(t, clave, avisar, fase):
        with candado:
            a_la_vez.append(clave)
            maximo[0] = max(maximo[0], len(a_la_vez))
        time.sleep(0.2)
        with candado:
            a_la_vez.remove(clave)

    monkeypatch.setattr(cola.produccion, "producir", produccion)
    monkeypatch.setattr(cola.taller, "cargar", lambda id_: {"id": id_, "videos": []})
    monkeypatch.setattr(cola, "_escribir", lambda *a, **k: None)

    for clave in ("v01", "v02", "v03"):
        assert cola.encolar("curso", clave) is True
    cola.esperar()
    assert maximo[0] == 1, f"se produjeron {maximo[0]} videos a la vez"


def test_el_mismo_trabajo_no_se_encola_dos_veces(monkeypatch):
    monkeypatch.setattr(cola, "_escribir", lambda *a, **k: None)
    monkeypatch.setattr(cola.taller, "cargar", lambda id_: None)  # el hilo lo descarta enseguida
    puesto = threading.Event()

    with cola._candado:
        cola._activos.add(("curso", "v09"))
    try:
        assert cola.encolar("curso", "v09") is False
    finally:
        with cola._candado:
            cola._activos.discard(("curso", "v09"))
    assert not puesto.is_set()
