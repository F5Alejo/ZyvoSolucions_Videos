"""Genera los PPTX de prueba de `tests/fixtures/` (para detectar regresiones del extractor y del motor).

    python scripts/generar_fixtures.py

Se generan con código para que sean reproducibles y no traigan material de clientes. Si cambia
este script, se vuelven a generar y se suben con el cambio.
"""

import io
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

DESTINO = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
TITULO_Y_CONTENIDO, SOLO_TITULO, EN_BLANCO = 1, 5, 6


def _imagen(color: tuple[int, int, int], ancho: int = 800, alto: int = 600) -> io.BytesIO:
    buf = io.BytesIO()
    Image.new("RGB", (ancho, alto), color).save(buf, "PNG")
    buf.seek(0)
    return buf


def _lamina(pres, titulo: str | None, vinetas: list[str] = (), notas: str = "", diseno: int = TITULO_Y_CONTENIDO):
    s = pres.slides.add_slide(pres.slide_layouts[diseno])
    if titulo is not None and s.shapes.title is not None:
        s.shapes.title.text = titulo
    if vinetas:
        cuerpo = s.placeholders[1].text_frame if diseno == TITULO_Y_CONTENIDO else \
            s.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4)).text_frame
        cuerpo.text = vinetas[0]
        for v in vinetas[1:]:
            cuerpo.add_paragraph().text = v
    if notas:
        s.notes_slide.notes_text_frame.text = notas
    return s


def simple(pres):
    _lamina(pres, "Seguridad informática", ["Qué es", "Por qué importa"],
            "En esta presentación veremos qué es la seguridad informática y por qué importa.")
    _lamina(pres, "Contraseñas seguras", ["Largas", "Únicas", "Con gestor"],
            "Una contraseña segura es larga y única. Usa un gestor de contraseñas.")
    _lamina(pres, "Cierre", ["Revisa tus cuentas hoy"], "Revisa hoy mismo tus cuentas más importantes.")


def images(pres):
    s = _lamina(pres, "Phishing", ["Correos falsos"], "El phishing llega en correos que parecen reales.", SOLO_TITULO)
    s.shapes.add_picture(_imagen((30, 80, 150)), Inches(5), Inches(2), Inches(4))
    s = _lamina(pres, "Señales de alerta", ["Urgencia", "Enlaces raros"], "Desconfía de la urgencia y de los enlaces raros.",
                SOLO_TITULO)
    s.shapes.add_picture(_imagen((150, 40, 40)), Inches(5), Inches(2), Inches(4))
    s.shapes.add_picture(_imagen((200, 200, 200), 64, 64), Inches(9), Inches(0.2), Inches(0.5))  # un ícono


def tables(pres):
    s = _lamina(pres, "Multas por exceso de velocidad", [], "La multa depende de cuánto se pasa del límite.", SOLO_TITULO)
    filas = [("Exceso", "Multa"), ("Hasta 20 km/h", "15 SMMLV"), ("Más de 20 km/h", "30 SMMLV")]
    tabla = s.shapes.add_table(len(filas), 2, Inches(1), Inches(2), Inches(8), Inches(2)).table
    for i, fila in enumerate(filas):
        for j, texto in enumerate(fila):
            tabla.cell(i, j).text = texto
    s = _lamina(pres, "Siniestros por año", [], "Los siniestros bajaron entre 2022 y 2024.", SOLO_TITULO)
    datos = CategoryChartData()
    datos.categories = ["2022", "2023", "2024"]
    datos.add_series("Siniestros", (120, 98, 75))
    s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(2), Inches(8), Inches(4), datos)


def long_text(pres):
    largo = ("La gestión del riesgo vial en las organizaciones exige identificar los peligros, valorar los riesgos, "
             "definir controles y verificar que funcionen, con la participación de los trabajadores y la dirección. ")
    _lamina(pres, "Un título bastante largo que no debería caber en una sola línea de la pantalla del video",
            [largo, largo, "Tercera idea", "Cuarta idea", "Quinta idea", "Sexta idea", "Séptima idea"], largo * 3)


def notes(pres):
    _lamina(pres, "Ley 1503 de 2011", ["Plan estratégico"],
            "Lo exige la Ley 1503 de 2011. El 30 % de los siniestros ocurre en misión. Multas de $ 1.000.000.")
    _lamina(pres, "Sin notas", ["Esta lámina no tiene notas del orador"])


def empty_slide(pres):
    _lamina(pres, "Antes del vacío", ["Algo"], "Esta lámina sí tiene narración.")
    pres.slides.add_slide(pres.slide_layouts[EN_BLANCO])
    _lamina(pres, "Después del vacío", ["Algo más"], "Y esta también.")


def mixed_content(pres):
    simple(pres)
    images(pres)
    tables(pres)
    notes(pres)


FIXTURES = {"simple": simple, "images": images, "tables": tables, "long_text": long_text, "notes": notes,
            "empty_slide": empty_slide, "mixed_content": mixed_content}


def generar(destino: Path = DESTINO) -> list[Path]:
    destino.mkdir(parents=True, exist_ok=True)
    salida = []
    for nombre, armar in FIXTURES.items():
        pres = Presentation()
        armar(pres)
        ruta = destino / f"{nombre}.pptx"
        pres.save(ruta)
        salida.append(ruta)
    return salida


if __name__ == "__main__":
    for r in generar():
        print(f"{r.relative_to(DESTINO.parent.parent)}  {r.stat().st_size // 1024} KB")
