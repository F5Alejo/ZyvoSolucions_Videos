# -*- coding: utf-8 -*-
"""Lámina 26 · Evaluación final 1/4. Preguntas 1 a 3."""
import cronometro, evaluacion

LAMINA = 26
DUR = cronometro.duracion(LAMINA)

PREGUNTAS = [
    ("1", "De noche, el mínimo de visibilidad incluye…",
     [("A", "Solo reflectivo trasero."),
      ("B", "Luz blanca adelante, roja atrás y prenda reflectiva aplicable."),
      ("C", "La linterna del celular.")]),
    ("2", "¿Puede circular por el andén para evitar congestión?",
     [("A", "Sí, tocando el timbre."),
      ("B", "No, salvo espacio autorizado o diseñado localmente."),
      ("C", "Sí, si lleva casco.")]),
    ("3", "Si un freno no funciona…",
     [("A", "Salir despacio."),
      ("B", "Declararla no apta y reportar."),
      ("C", "Usar solo la ciclorruta.")]),
]

TL = evaluacion.tiempos(
    lead_t=0.55,
    preguntas_t=[(5.94, 9.16), (17.41, 20.22), (25.76, 27.60)],
    aviso_t=31.69, pausa_t=34.78, nota_t=45.78)


def escena():
    return evaluacion.escena(
        "e26-evaluacion-1", LAMINA, DUR, "26",
        "1/4 · Selección múltiple · <b style=\"color:#D4A62B\">preguntas 1 a 3</b>",
        "Tres preguntas. Lee todas las alternativas antes de elegir.",
        PREGUNTAS,
        "Registra una respuesta y una razón breve para cada una.",
        "La explicación completa aparece al terminar las cuatro partes de la evaluación.",
        TL)
