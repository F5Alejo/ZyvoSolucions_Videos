# -*- coding: utf-8 -*-
"""Lámina 27 · Evaluación final 2/4. Preguntas 4 a 6."""
import cronometro, evaluacion

LAMINA = 27
DUR = cronometro.duracion(LAMINA)

PREGUNTAS = [
    ("4", "Antes de cambiar de trayectoria…",
     [("A", "Girar y luego avisar."),
      ("B", "Observar, señalizar, verificar y ejecutar."),
      ("C", "Tocar el timbre y cruzar.")]),
    ("5", "La ruta más segura es…",
     [("A", "Siempre la más corta."),
      ("B", "La que reduce exposición y tiene alternativa."),
      ("C", "La más conocida.")]),
    ("6", "Una llamada urgente se atiende…",
     [("A", "Con manos libres, en marcha."),
      ("B", "Detenido, fuera del flujo."),
      ("C", "A baja velocidad.")]),
]

TL = evaluacion.tiempos(
    lead_t=0.55,
    preguntas_t=[(4.95, 9.06), (13.84, 17.50), (29.72, 32.40)],
    aviso_t=40.14, pausa_t=40.60, nota_t=47.64)


def escena():
    return evaluacion.escena(
        "e27-evaluacion-2", LAMINA, DUR, "27",
        "2/4 · Selección múltiple · <b style=\"color:#D4A62B\">preguntas 4 a 6</b>",
        "Seguridad y distancia no son equivalentes: una ruta algo más larga puede exponer menos.",
        PREGUNTAS,
        "Justifica cuál alternativa reduce realmente la exposición.",
        "Al terminar, continúa con los dos casos de decisión.",
        TL)
