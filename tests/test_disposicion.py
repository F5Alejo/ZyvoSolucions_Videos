"""La geometría de la lámina y su reconstrucción animada (modo fiel).

Lo que aquí se prueba es lo que distingue al modo fiel del de siempre: que la lámina salga
donde estaba y que sus formas entren al ritmo de la voz, no todas de golpe.
"""

import io
from dataclasses import dataclass

import pytest
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

from app import disposicion
from motor.escenas import lamina as mod_lamina


@dataclass
class Frase:
    inicio: float
    duracion: float = 1.0
    texto: str = ""


def pptx_con_disposicion() -> io.BytesIO:
    """Una lámina con la convención de nombres de los cursos: marco, fondo y tarjetas numeradas."""
    pres = Presentation()
    pres.slide_width, pres.slide_height = Emu(12192000), Emu(6858000)  # 16:9
    s = pres.slides.add_slide(pres.slide_layouts[6])  # en blanco

    def caja(nombre, x, y, w, h, texto=None, relleno=None, pt=18):
        f = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        f.name = nombre
        if relleno:
            f.fill.solid()
            f.fill.fore_color.rgb = RGBColor.from_string(relleno)
        if texto:
            f.text_frame.text = texto
            r = f.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold = Pt(pt), True
            r.font.color.rgb = RGBColor.from_string("FFFFFF")
        return f

    caja("cover-field", 0, 0, 13.333, 7.5, relleno="1F4E79")   # fondo por nombre
    caja("title", 0.5, 0.5, 8, 1, "Conducción segura", pt=40)  # marco
    caja("decoracion", 11, 0.4, 1, 1, relleno="D79B27")        # sin texto: escenografía
    caja("bar-1", 0.5, 2.0, 5, 0.8, relleno="333333")
    caja("bar-label-1", 0.7, 2.1, 4, 0.6, "Percibir")
    caja("bar-2", 0.5, 3.0, 5, 0.8, relleno="333333")
    caja("bar-label-2", 0.7, 3.1, 4, 0.6, "Anticipar")
    caja("bar-3", 0.5, 4.0, 5, 0.8, relleno="333333")
    caja("bar-label-3", 0.7, 4.1, 4, 0.6, "Decidir")

    buf = io.BytesIO()
    pres.save(buf)
    buf.seek(0)
    return buf


@pytest.fixture()
def lamina_leida():
    d = disposicion.leer(pptx_con_disposicion())
    return d, d["laminas"][0]["formas"]


def test_cada_forma_conserva_su_sitio_su_color_y_su_letra(lamina_leida):
    d, formas = lamina_leida
    assert d["proporcion"] == pytest.approx(1.7778, abs=1e-3)
    assert d["escala_pt"] == pytest.approx(1.0)  # la lámina mide las 7,5 pulgadas de referencia

    por_id = {f["id"]: f for f in formas}
    titulo = por_id["title"]
    # Las cajas salen normalizadas: media pulgada sobre 13,333 de ancho.
    assert titulo["x"] == pytest.approx(0.5 / 13.333, abs=1e-3)
    assert titulo["y"] == pytest.approx(0.5 / 7.5, abs=1e-3)
    assert titulo["texto"] == "Conducción segura"
    run = titulo["parrafos"][0]["runs"][0]
    assert (run["pt"], run["negrita"], run["color"]) == (40.0, True, "#ffffff")
    assert por_id["cover-field"]["relleno"] == "#1f4e79"
    # El z respeta el orden de pintado del PPTX.
    assert por_id["cover-field"]["z"] < por_id["title"]["z"] < por_id["bar-1"]["z"]


def test_el_fondo_y_el_marco_se_reconocen(lamina_leida):
    _, formas = lamina_leida
    por_id = {f["id"]: f for f in formas}
    assert por_id["cover-field"]["fondo"] is True       # por nombre y porque cubre la lámina
    assert por_id["title"]["es_marco"] is True
    assert por_id["bar-label-1"]["fondo"] is False
    assert por_id["bar-label-1"]["es_marco"] is False


def test_la_escenografia_entra_de_una_y_el_contenido_se_escalona(lamina_leida):
    """El defecto que había al principio: la decoración se comía los turnos y el título llegaba tarde."""
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))

    base = {f["id"] for f in bloques[0]}
    assert {"cover-field", "title", "decoracion"} <= base, "fondo, marco y decoración van juntos al inicio"
    # Cada tarjeta es un bloque: su fondo y su texto entran a la vez, no por separado.
    assert [sorted(f["id"] for f in b) for b in bloques[1:]] == [
        ["bar-1", "bar-label-1"], ["bar-2", "bar-label-2"], ["bar-3", "bar-label-3"]]


def test_cada_bloque_entra_cuando_la_voz_lo_nombra(lamina_leida):
    """Lo que de verdad coordina la lámina con la voz: la tarjeta entra con *su* frase.

    Aquí la narración nombra las tarjetas **desordenadas** respecto a su sitio en la lámina
    (primero decidir, luego percibir…). Repartiendo por orden, «Percibir» saldría en la
    primera frase; enganchando por contenido, sale en la que habla de percibir.
    """
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    narracion = [
        Frase(0.0, texto="Conducir exige tres competencias que veremos una a una."),
        Frase(5.0, texto="Primero hay que percibir el riesgo que ya está en la vía."),
        Frase(11.0, texto="Después toca anticipar lo que puede ocurrir enseguida."),
        Frase(18.0, texto="Y por último decidir la maniobra más segura."),
    ]
    t = mod_lamina.tiempos(bloques, narracion, 26.0, hay_base=True)

    assert t[0] == 0.0                       # la escenografía nunca espera
    assert t[1:] == [4.8, 10.8, 17.8]     # percibir, anticipar y decidir, cada una con su frase
    assert t == sorted(t), "los bloques entran en orden"


def test_un_bloque_no_puede_entrar_antes_que_el_anterior():
    """La frase que mejor coincide puede ir hacia atrás; en la lámina eso no puede pasar."""
    # La segunda frase nombra la tarjeta 3, y la tercera la 2: si se hiciera caso sin más,
    # la tarjeta 3 entraría antes que la 2.
    enganches = mod_lamina.emparejar(
        ["Percibir el riesgo", "Anticipar lo que viene", "Decidir la maniobra"],
        ["Veamos el proceso completo.",
         "Hay que decidir rápido la maniobra.",
         "Pero antes conviene anticipar lo que viene."])
    puestos = [j for j in enganches if j is not None]
    assert puestos == sorted(puestos), f"los enganches van hacia atrás: {enganches}"


def test_una_narracion_que_no_nombra_nada_reparte_por_orden(lamina_leida):
    """Sin coincidencias no se inventa ninguna: se vuelve al reparto por frases."""
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    generica = [Frase(0.0, texto="Bienvenidos a este módulo."),
                Frase(4.0, texto="Vamos a empezar ahora mismo."),
                Frase(9.0, texto="Preste mucha atención, por favor.")]
    t = mod_lamina.tiempos(bloques, generica, 14.0, hay_base=True)
    assert t == [0.0, 0.0, 3.8, 8.8]


def test_un_bloque_sin_coincidencia_cae_en_un_cambio_de_frase(lamina_leida):
    """Interpolar deja la entrada a mitad de frase y se nota: se lleva al borde más cercano."""
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    narracion = [
        Frase(0.0, texto="Empecemos."),
        Frase(5.0, texto="Lo primero es percibir el riesgo."),
        Frase(10.0, texto="Algo que no tiene que ver con nada."),
        Frase(15.0, texto="Y al final hay que decidir la maniobra."),
    ]
    t = mod_lamina.tiempos(bloques, narracion, 22.0, hay_base=True)
    # «Anticipar» no lo nombra ninguna frase: cae en el arranque de una, no en medio.
    inicios = {0.0, 5.0, 10.0, 15.0}
    assert (t[2] + mod_lamina.ADELANTO) in inicios, f"{t[2]} no coincide con ningún cambio de frase"


def test_los_tiempos_de_la_frase_son_del_video_y_hay_que_pasarlos_a_la_escena(lamina_leida):
    """La lámina 3 de un curso no mostraba nada: sus frases empiezan en el segundo 108 del video.

    `videospec.Frase.inicio` cuenta desde el principio del video; la composición de una lámina
    cuenta desde cero. Sin restar dónde arranca la escena, todos los bloques se amontonaban
    contra el final de la lámina y no llegaban a verse.
    """
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    narracion = [Frase(108.7), Frase(115.9), Frase(122.6)]  # tal como salen del spec resuelto

    t = mod_lamina.tiempos(bloques, narracion, 48.1, hay_base=True, desde=107.7)
    assert t == [0.0, 0.8, 8.0, 14.7]
    assert max(t) < 48.1 - mod_lamina.DURACION_ENTRADA, "los bloques caben dentro de la lámina"

    # Sin el `desde`, es justo el defecto: todo contra el final y nada visible.
    malos = mod_lamina.tiempos(bloques, narracion, 48.1, hay_base=True)
    assert malos[1:] == [47.85, 47.85, 47.85]


def test_sin_narracion_los_bloques_se_reparten_por_la_lamina(lamina_leida):
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    t = mod_lamina.tiempos(bloques, [], 12.0, hay_base=True)
    assert t == [0.0, 0.0, 3.8, 7.8]


def test_ningun_bloque_entra_despues_de_que_termine_la_lamina(lamina_leida):
    _, formas = lamina_leida
    bloques = mod_lamina.grupos(mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0))
    # Una narración más larga que la lámina: los tiempos se recortan, no se salen.
    t = mod_lamina.tiempos(bloques, [Frase(0.0), Frase(30.0), Frase(90.0)], 5.0, hay_base=True)
    assert max(t) <= 5.0 - mod_lamina.DURACION_ENTRADA


def _forma_texto(texto, w, h, pt=15.0, negrita=True):
    """Una forma con una caja de `w`×`h` normalizada sobre 1920×1080."""
    return {"id": "x", "nombre": "x", "tipo": "texto", "z": 1, "x": 0.1, "y": 0.1,
            "w": w / 1920, "h": h / 1080, "giro": 0, "relleno": None, "borde": None,
            "texto": texto, "fondo": False, "es_marco": False,
            "marco": {"margenes_pt": [3.6, 7.2, 3.6, 7.2], "ancla": "flex-start", "ajustar_texto": True},
            "parrafos": [{"runs": [{"texto": texto, "pt": pt, "negrita": negrita, "cursiva": False,
                                    "subrayado": False, "color": "#000000", "fuente": "Aptos"}],
                          "alineacion": None, "nivel": 0, "vacio": False, "interlineado": None}]}


def test_un_texto_que_cabe_no_se_toca():
    f = _forma_texto("Breve", 400, 80)
    assert mod_lamina.encajar(f, 2.0, 400, 80) == 1.0


def test_un_texto_que_se_sale_se_achica_hasta_entrar():
    """Sin esto, la viñeta larga se salía de su barra y la barra de abajo se la comía."""
    f = _forma_texto("La seguridad está por encima de la rapidez", 286, 65)
    k = mod_lamina.encajar(f, 2.0, 286, 65)
    assert mod_lamina.MINIMO < k < 1.0
    # Y, ya achicado, cabe de verdad.
    assert mod_lamina._alto_texto(f, k, 2.0, 286 - 14.4 - 14.4) <= 65 + 1


def test_el_texto_se_mide_con_el_peso_con_el_que_se_dibuja():
    """Montserrat es variable y su eje de peso viene en 100 (Thin).

    Al abrirla sin fijar el peso se medía la variante más estrecha que existe, mientras el
    navegador dibuja en 400 o en 700: todo «cabía» y no se achicaba nada.
    """
    texto = "Ninguna práctica premia maniobras"
    fino = mod_lamina._tipo(30, 100).getlength(texto)
    normal = mod_lamina._ancho(texto, 30, negrita=False)
    negrita = mod_lamina._ancho(texto, 30, negrita=True)
    assert fino < normal < negrita, "el peso tiene que cambiar lo que mide el texto"


def test_el_ancho_decide_cuantas_lineas_ocupa():
    largo = "La experiencia se comparte con responsabilidad"
    assert mod_lamina._lineas(largo, 30, True, 2000) == 1
    assert mod_lamina._lineas(largo, 30, True, 260) > 1
    assert mod_lamina._lineas("", 30, False, 100) == 1  # un párrafo vacío ocupa su línea


def test_el_texto_ya_viene_encajado_en_el_html(lamina_leida):
    """El ajuste se hace en Python: en el navegador la lámina está oculta y mide cero."""
    _, formas = lamina_leida
    apretada = [dict(f) for f in formas]
    for f in apretada:
        if f["id"] == "bar-label-1":
            f["parrafos"][0]["runs"][0].update({"texto": "Un texto larguísimo que no entra ni de lejos "
                                                         "en esta caja tan pequeña", "pt": 40.0})
            f["texto"] = f["parrafos"][0]["runs"][0]["texto"]
    listas = mod_lamina.preparar(apretada, "l1", 1920, 1080, 1.0)
    label = next(f for f in listas if f["id"] == "bar-label-1")
    assert label["_k"] < 1.0
    # El tamaño final ya está escrito en el estilo; no queda nada que medir en el navegador.
    esperado = round(40.0 * (1080 / (7.5 * 72)) * label["_k"], 2)
    assert f"font-size:{esperado}px" in label["parrafos"][0]["runs"][0]["_estilo"]

    html = mod_lamina.composicion(apretada, [Frase(0.0)], 8.0, "l1", 1920, 1080, 1.0)
    assert "scrollHeight" not in html, "no puede quedar ajuste de texto en el navegador"


def _pasos(formas, duracion=20.0, narracion=None):
    listas = mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0)
    bloques = mod_lamina.grupos(listas)
    inst = mod_lamina.tiempos(bloques, narracion or [], duracion, True)
    return mod_lamina.animacion(bloques, inst, None, hay_base=True, duracion=duracion)


def test_la_lamina_entra_con_un_fundido_en_vez_de_forma_por_forma(lamina_leida):
    """El corte seco entre láminas era lo que más se notaba.

    La escenografía (fondo, marco, decoración) no se anima pieza a pieza: entra toda junta con
    un fundido. Así no hay ni salto de fondo ni diez elementos moviéndose a la vez.
    """
    _, formas = lamina_leida
    pasos = _pasos(formas)
    fundidos = [p for p in pasos if p["selector"] == ".todo"]
    # Uno al entrar y otro al salir: el cambio de lámina es un bajón a fondo, no un corte.
    assert len(fundidos) == 2
    entra, sale = fundidos
    assert entra["desde"] == {"opacity": 0} and entra["en"] == 0.0
    assert sale["hasta"] == {"opacity": 0}
    assert sale["en"] == pytest.approx(20.0 - mod_lamina.SALIDA_LAMINA)
    # Y ninguna forma de la escenografía tiene además su propio tween.
    animadas = {p["selector"] for p in pasos}
    for id_ in ("cover-field", "title", "decoracion"):
        assert f"#l1-{id_} > .a" not in animadas


def test_el_escalonado_de_un_bloque_cabe_en_un_solo_golpe(lamina_leida):
    """`items × stagger ≤ ~0,5 s`: pasado eso el bloque gotea en vez de llegar."""
    _, formas = lamina_leida
    # Un bloque con muchas formas: el escalonado se aprieta para no estirarse.
    muchas = list(formas)
    for i in range(10):
        muchas.append(dict(formas[-1], id=f"bar-extra-{i}-1", nombre=f"bar-extra-{i}-1",
                           z=50 + i, y=0.3 + i * 0.01))
    pasos = _pasos(muchas)
    deltas = {}
    for p in pasos:
        if p["selector"] != ".todo":
            deltas.setdefault(round(p["en"] // 1), []).append(p["en"])
    for grupo in deltas.values():
        assert max(grupo) - min(grupo) <= mod_lamina.ESCALONADO_MAXIMO + 0.01


def test_las_formas_de_un_bloque_entran_en_orden_de_lectura():
    """De arriba abajo: si entran en orden de pintado, el ojo va dando saltos."""
    bloque = [
        {"id": "c", "x": 0.1, "y": 0.8, "z": 1},
        {"id": "a", "x": 0.1, "y": 0.1, "z": 9},
        {"id": "b", "x": 0.5, "y": 0.1, "z": 5},
    ]
    assert [f["id"] for f in mod_lamina._orden_lectura(bloque)] == ["a", "b", "c"]


def test_el_resaltado_va_siguiendo_a_la_voz_por_la_lamina(lamina_leida):
    """El rasgo más reconocible de las referencias: la viñeta recién nombrada queda resaltada.

    Se enciende cuando entra su bloque y se apaga cuando entra el siguiente, así que en cada
    momento hay una sola encendida y quien mira sabe de qué se está hablando.
    """
    _, formas = lamina_leida
    listas = mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0)
    bloques = mod_lamina.grupos(listas)
    inst = mod_lamina.tiempos(bloques, [], 30.0, True)
    pasos = mod_lamina.animacion(bloques, inst, None, hay_base=True, duracion=30.0,
                                 resalte="rgba(253,193,0,0.18)")

    de_label1 = [p for p in pasos if p["selector"] == "#l1-bar-label-1 > .a > p"
                 and "backgroundColor" in p["desde"]]
    assert len(de_label1) == 2, "la primera viñeta se enciende y luego se apaga"
    enciende, apaga = de_label1
    assert enciende["hasta"]["backgroundColor"] == "rgba(253,193,0,0.18)"
    assert apaga["hasta"]["backgroundColor"] == "rgba(0,0,0,0)"
    # Se apaga justo cuando entra la segunda viñeta, no antes ni después.
    entrada2 = next(p["en"] for p in pasos if p["selector"] == "#l1-bar-label-2 > .a"
                    and "x" in p["desde"])
    assert apaga["en"] == pytest.approx(entrada2, abs=0.1)

    # La última se queda encendida hasta que la lámina empieza a irse.
    de_label3 = [p for p in pasos if p["selector"] == "#l1-bar-label-3 > .a > p"
                 and "backgroundColor" in p["desde"]]
    assert de_label3[-1]["en"] == pytest.approx(30.0 - mod_lamina.SALIDA_LAMINA, abs=0.1)


def test_no_se_resalta_una_forma_que_ya_tiene_su_propio_fondo(lamina_leida):
    """Ponerle un velo encima a una tarjeta con relleno la rompería."""
    _, formas = lamina_leida
    listas = mod_lamina.preparar(formas, "l1", 1920, 1080, 1.0)
    bloques = mod_lamina.grupos(listas)
    pasos = mod_lamina.animacion(bloques, mod_lamina.tiempos(bloques, [], 30.0, True), None,
                                 hay_base=True, duracion=30.0, resalte="rgba(253,193,0,0.18)")
    con_fondo = {p["selector"] for p in pasos if "backgroundColor" in p["desde"]}
    assert "#l1-bar-1 > .a > p" not in con_fondo, "bar-1 tiene relleno propio"
    assert "#l1-bar-label-1 > .a > p" in con_fondo


def test_el_resaltado_siempre_se_apaga_aunque_el_siguiente_entre_pegado():
    """Dos bloques casi a la vez dejaban el resaltado encendido para siempre."""
    bloques = [[{"id": "a", "_cid": "l1-a", "tipo": "texto", "relleno": None, "texto": "Uno",
                 "parrafos": [{"runs": [{"texto": "Uno"}], "vacio": False}]}],
               [{"id": "b", "_cid": "l1-b", "tipo": "texto", "relleno": None, "texto": "Dos",
                 "parrafos": [{"runs": [{"texto": "Dos"}], "vacio": False}]}]]
    # El segundo bloque entra 0,05 s después del primero: menos que el encendido.
    pasos = mod_lamina._resaltes(bloques, [3.0, 3.05], hay_base=False, duracion=20.0,
                                 color="rgba(1,2,3,0.18)")
    apagados = [p for p in pasos if p["hasta"]["backgroundColor"] == "rgba(0,0,0,0)"]
    assert len(apagados) == 2, "los dos bloques tienen que apagarse"
    assert all(p["en"] >= 3.0 + mod_lamina.RESALTE_ENTRA for p in apagados)


def test_no_se_resalta_una_lista_entera():
    """Subrayar cinco viñetas a la vez no señala nada: pinta medio lienzo."""
    lista = {"tipo": "texto", "relleno": None, "texto": "a\nb\nc",
             "parrafos": [{"runs": [{"texto": x}], "vacio": False} for x in "abc"]}
    corta = {"tipo": "texto", "relleno": None, "texto": "Percibir",
             "parrafos": [{"runs": [{"texto": "Percibir"}], "vacio": False}]}
    assert mod_lamina._resaltable(lista) is False
    assert mod_lamina._resaltable(corta) is True


def test_se_mide_cuanto_de_la_lamina_llega_a_decir_la_voz():
    """El número que separa «el video cuenta la lámina» de «van cada uno por su lado».

    En los videos de referencia del curso la voz enumera la lámina casi palabra por palabra
    (cobertura 1,0). Con unas notas que son un ensayo paralelo baja a 0,3-0,4, y entonces se
    lee una cosa mientras se oye otra.
    """
    visible = "Exterior: fugas, golpes, parabrisas, espejos, puertas"
    # Como en la referencia: la voz nombra todo lo que se ve.
    dice_todo = ("Se revisa el exterior buscando fugas, golpes, estado de parabrisas, "
                 "espejos y puertas antes de mover el vehículo.")
    assert mod_lamina.cobertura(visible, dice_todo) == 1.0
    # Como en el PPTX del motociclista: habla del tema, pero no de lo que se muestra.
    habla_de_otra_cosa = ("El aprendizaje funciona cuando las experiencias reales pueden "
                          "analizarse sin convertir la conversación en una competencia.")
    assert mod_lamina.cobertura(visible, habla_de_otra_cosa) < 0.2
    # Una lámina sin texto no puede estar mal contada.
    assert mod_lamina.cobertura("", "lo que sea") == 1.0


def test_el_color_del_resaltado_sale_de_la_marca():
    assert mod_lamina._diluir("#fdc100") == "rgba(253,193,0,0.18)"
    assert mod_lamina._diluir(None) is None
    assert mod_lamina._diluir("rojo") is None


def test_las_imagenes_derivan_despacio_durante_toda_la_lamina(lamina_leida):
    """Un plano completamente quieto delata que el video es una diapositiva."""
    _, formas = lamina_leida
    con_foto = [*formas, {**formas[0], "id": "foto", "nombre": "foto", "tipo": "imagen",
                          "archivo": "x.png", "z": 99, "fondo": False, "es_marco": False,
                          "texto": "", "parrafos": []}]
    pasos = _pasos(con_foto, duracion=30.0)
    deriva = [p for p in pasos if p["selector"] == "#l1-foto > .a" and "scale" in p["desde"]]
    assert len(deriva) == 1
    assert deriva[0]["hasta"]["scale"] > 1 and deriva[0]["duracion"] == 30.0
    assert deriva[0]["curva"] == mod_lamina.CURVA_CONTINUA
    # Es un segundo tween sobre la misma forma: no puede aplicar su estado inicial al construir.
    assert deriva[0]["inmediato"] is False


def test_las_entradas_usan_la_curva_y_los_recorridos_de_la_casa():
    """Medido en las referencias: la entrada dura ~0,23 s y el elemento viaja ~10 px."""
    assert mod_lamina.CURVAS["suave"] == "power3.out"
    assert mod_lamina.DURACION_ENTRADA <= 0.3
    assert mod_lamina.TWEENS["deslizar-derecha"]["x"] == 10
    assert all(abs(v.get("x", 0)) <= 10 and abs(v.get("y", 0)) <= 10
               for v in mod_lamina.TWEENS.values() if v and "scale" not in v)


def test_la_composicion_cumple_el_contrato_de_hyperframes(lamina_leida):
    d, formas = lamina_leida
    html = mod_lamina.composicion(formas, [Frase(0.0), Frase(3.0)], 10.0, "lamina1",
                                  1920, 1080, d["escala_pt"], media="assets/media/",
                                  fuente="assets/fuentes/Montserrat.ttf", fondo="#f2f4f8")

    # Sub-composición: va envuelta en <template> o el ensamblador le tira el estilo y el script.
    assert "<template>" in html
    assert 'data-composition-id="lamina1"' in html
    assert 'data-width="1920"' in html and 'data-height="1080"' in html and 'data-duration="10.0"' in html
    # Una sola línea de tiempo, en pausa y con la clave del root.
    assert html.count("gsap.timeline({ paused: true })") == 1
    assert 'window.__timelines["lamina1"]' in html
    # La tipografía viaja con el proyecto: el render no sale a internet.
    assert "assets/fuentes/Montserrat.ttf" in html and "file://" not in html
    assert "#f2f4f8" in html


def test_la_capa_que_gira_y_la_que_anima_estan_separadas(lamina_leida):
    """`hyperframes lint` rechaza que un transform del CSS y un tween de GSAP toquen lo mismo."""
    d, formas = lamina_leida
    giradas = [dict(f, giro=12.5) for f in formas]
    html = mod_lamina.composicion(giradas, [Frase(0.0)], 6.0, "lamina1", 1920, 1080, d["escala_pt"])
    # El giro va en la capa de fuera (.f); GSAP solo toca la de dentro (.a).
    assert "rotate(12.5deg)" in html
    # Se mira una forma de contenido: el marco y el fondo entran con el fundido de la lámina.
    assert '"selector": "#lamina1-bar-label-1 > .a"' in html


def test_el_video_encadena_las_laminas_sin_envolver_el_root():
    laminas = [{"n": 1, "cid": "lamina1", "archivo": "compositions/e1.html", "inicio": 0.0, "duracion": 8.0},
               {"n": 2, "cid": "lamina2", "archivo": "compositions/e2.html", "inicio": 8.0, "duracion": 5.0}]
    html = mod_lamina.indice(laminas, 1920, 1080, 13.0, "#020202")

    # Root standalone: nunca va en <template> (lint: standalone_composition_wrapped_in_template).
    assert "<template>" not in html
    assert 'data-composition-id="video"' in html and 'data-duration="13.0"' in html
    assert 'data-composition-src="compositions/e2.html"' in html
    assert 'data-start="8.0"' in html and 'data-duration="5.0"' in html
    # El video es mudo: el audio lo mezcla ffmpeg después, con su ducking y su -14 LUFS.
    assert "<audio" not in html and "<video" not in html
