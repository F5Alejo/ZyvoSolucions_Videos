"""El catálogo de efectos de animación: lo único que una plantilla (o un agente) puede pedir.

Cada efecto es CSS puro: el render lleva cada animación a su instante exacto, así que el
resultado es idéntico en cada render. La entrada va desde el estado del efecto hasta el
elemento en su sitio; la salida, desde el elemento en su sitio hasta el estado del efecto.
"""

# Efecto → cuerpo de @keyframes (entrada). `None` = sin animación.
ENTRADA = {
    "ninguno": None,
    "aparecer": "from { opacity: 0; }",
    "subir": "from { opacity: 0; transform: translateY(60px); }",
    "bajar": "from { opacity: 0; transform: translateY(-60px); }",
    "deslizar-izquierda": "from { opacity: 0; transform: translateX(-140px); }",
    "deslizar-derecha": "from { opacity: 0; transform: translateX(140px); }",
    "escalar": "from { opacity: 0; transform: scale(.72); }",
    "desenfoque": "from { opacity: 0; filter: blur(22px); }",
    "revelar": "from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); }",
    "rebote": "0% { opacity: 0; transform: scale(.3); } 55% { opacity: 1; transform: scale(1.08); } "
              "75% { transform: scale(.96); } 100% { transform: scale(1); }",
    "girar": "from { opacity: 0; transform: rotate(-25deg) scale(.9); }",
    "crecer": "from { transform: scaleX(0); }",
    # Por palabra o por letra: el CSS se aplica a cada trozo (ver animacion.py).
    "palabra-por-palabra": "from { opacity: 0; transform: translateY(0.45em); filter: blur(6px); }",
    "maquina": "from { opacity: 0; }",
}

SALIDA = {
    "ninguno": None,
    "aparecer": "to { opacity: 0; }",
    "subir": "to { opacity: 0; transform: translateY(-60px); }",
    "bajar": "to { opacity: 0; transform: translateY(60px); }",
    "deslizar-izquierda": "to { opacity: 0; transform: translateX(-140px); }",
    "deslizar-derecha": "to { opacity: 0; transform: translateX(140px); }",
    "escalar": "to { opacity: 0; transform: scale(.8); }",
    "desenfoque": "to { opacity: 0; filter: blur(22px); }",
    "revelar": "from { clip-path: inset(0 0 0 0); } to { clip-path: inset(0 0 0 100%); }",
    "rebote": "0% { transform: scale(1); } 35% { transform: scale(1.06); } 100% { opacity: 0; transform: scale(.3); }",
    "girar": "to { opacity: 0; transform: rotate(20deg) scale(.9); }",
    "crecer": "to { transform: scaleX(0); }",
}

NOMBRES = {
    "ninguno": "Sin animación", "aparecer": "Aparecer (fundido)", "subir": "Subir", "bajar": "Bajar",
    "deslizar-izquierda": "Deslizar por la izquierda", "deslizar-derecha": "Deslizar por la derecha",
    "escalar": "Escalar", "desenfoque": "Desenfoque", "revelar": "Revelar (cortina)", "rebote": "Rebote",
    "girar": "Girar", "crecer": "Crecer (barra)", "palabra-por-palabra": "Palabra por palabra",
    "maquina": "Máquina de escribir (letra por letra)",
}

CURVAS = {
    "suave": "cubic-bezier(.2, .7, .2, 1)",
    "energica": "cubic-bezier(.16, 1, .3, 1)",
    "rebote": "cubic-bezier(.34, 1.56, .64, 1)",
    "lineal": "linear",
}
NOMBRES_CURVAS = {"suave": "Suave", "energica": "Enérgica", "rebote": "Con rebote", "lineal": "Lineal"}

# Qué se anima de cada escena, con qué selector CSS y qué efectos admite.
_TEXTO = ["ninguno", "aparecer", "subir", "bajar", "deslizar-izquierda", "deslizar-derecha", "escalar",
          "desenfoque", "revelar", "rebote"]
ELEMENTOS = {
    "fondo": {"nombre": "Fondo (anillos)", "selector": ".anillo",
              "entrada": ["ninguno", "aparecer", "girar", "escalar", "desenfoque"],
              "salida": ["ninguno", "aparecer", "girar", "escalar", "desenfoque"]},
    "logo": {"nombre": "Logo y título del video", "selector": ".cabeza",
             "entrada": ["ninguno", "aparecer", "bajar", "deslizar-izquierda", "desenfoque"],
             "salida": ["ninguno", "aparecer", "subir", "deslizar-izquierda", "desenfoque"]},
    "antetitulo": {"nombre": "Antetítulo (portada)", "selector": ".kicker",
                   "entrada": _TEXTO + ["palabra-por-palabra", "maquina"], "salida": _TEXTO},
    "titulo": {"nombre": "Título", "selector": "h1",
               "entrada": _TEXTO + ["palabra-por-palabra", "maquina"], "salida": _TEXTO},
    "linea": {"nombre": "Línea bajo el título", "selector": ".linea",
              "entrada": ["ninguno", "aparecer", "crecer", "revelar"], "salida": ["ninguno", "aparecer", "crecer", "revelar"]},
    "vinetas": {"nombre": "Viñetas", "selector": "li", "entrada": _TEXTO, "salida": _TEXTO},
    "imagen": {"nombre": "Imagen", "selector": ".foto",
               "entrada": ["ninguno", "aparecer", "subir", "deslizar-izquierda", "deslizar-derecha", "escalar",
                           "desenfoque", "revelar", "rebote", "girar"],
               "salida": ["ninguno", "aparecer", "subir", "bajar", "deslizar-izquierda", "deslizar-derecha", "escalar",
                          "desenfoque", "revelar"]},
    "avance": {"nombre": "Barra de avance", "selector": ".avance", "entrada": ["ninguno", "crecer"], "salida": ["ninguno"]},
}

# Solo en la primera escena del video entran, y solo en la última salen: entre láminas se
# quedan quietos (si no, parpadearían en cada cambio de lámina).
CONTINUOS = ("fondo", "logo")

LIMITES = {"duracion": (0.0, 3.0), "retardo": (0.0, 3.0), "escalonado": (0.0, 0.6)}
