# -*- coding: utf-8 -*-
"""Genera la página del banco de preguntas con el formato del banco COPASST.

    python videos/csm-curso/tools/banco_html.py <salida.html>

Toma el CSS tal cual del artefacto COPASST (guardado en la sesión) para que las
dos páginas se vean como una sola serie. Las preguntas no se numeran: en la
plataforma salen al azar. La respuesta correcta se reparte entre A, B y C.
"""
import io, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "datos"))
import banco_preguntas as B

REF = sys.argv[2] if len(sys.argv) > 2 else None


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def css_referencia():
    s = io.open(REF, encoding="utf-8").read()
    bloques = re.findall(r"<style>(.*?)</style>", s, re.S)
    return bloques[1]


def pregunta(i, q):
    enun, ok, d1, d2, fuente = q
    pos = (sum(map(ord, enun)) + i) % 3
    opciones = [d1, d2]
    opciones.insert(pos, ok)
    lis = "".join('<li%s><span class="mark">%s</span>%s</li>' % (' class="correct"' if j == pos else "", "ABC"[j], esc(o))
                  for j, o in enumerate(opciones))
    return ('<li><p class="q-text">%s</p><ul class="opts">%s</ul><p class="src">%s</p></li>'
            % (esc(enun), lis, esc(fuente)))


def seccion(ident, badge, titulo, preguntas):
    cuerpo = "\n".join(pregunta(i, q) for i, q in enumerate(preguntas))
    return ('<section class="card" id="%s"><div class="kicker"><span class="badge">%s</span><h2>%s</h2>'
            '<span class="duration">%d preguntas</span></div><ul class="questions">\n%s\n</ul></section>'
            % (ident, esc(badge), esc(titulo), len(preguntas), cuerpo))


def main():
    salida = sys.argv[1]
    todas = B.VIDEOS + [B.FINAL]
    total = sum(len(v[3]) for v in todas)
    css = css_referencia().replace("ol.questions", "ul.questions")
    nav = "".join('<a href="#%s">%s</a>' % (v[0], esc(v[1])) for v in todas)
    html = """<title>Evaluaciones Conducción Segura</title>
<style>%s</style>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<div class="wrap"><header class="hero"><p class="eyebrow">Conducción Segura · para cargar en RiskMann</p><h1>Banco de preguntas A/B/C</h1><p>Preguntas de selección múltiple por video: enunciado completo, tres opciones y la respuesta correcta resaltada. Cada pregunta cita la parte y la diapositiva del video de donde sale su respuesta. Las preguntas no van numeradas porque la plataforma las presenta al azar. Total: %d preguntas.</p><p>Elaborado a partir del contenido de los videos (diapositivas y narración). La evaluación final incluye además el caso integrador de la presentación original, que no aparece en los videos.</p></header><section class="card" id="datos"><div class="kicker"><span class="badge">Datos</span><h2>Datos de la capacitación</h2></div><div class="field"><span class="field-label">Nombre de la capacitación</span><div class="field-value title">%s</div></div><div class="field"><span class="field-label">Descripción del curso</span><div class="field-value">%s</div></div></section><nav class="toc" aria-label="Videos"><a href="#datos">Datos</a>%s</nav>
%s
<footer class="close"><strong>Nota:</strong> respuesta correcta resaltada en cada pregunta. Revisa las fuentes citadas antes de cargar el banco en RiskMann.</footer></div>
""" % (css, total, esc(B.CURSO["nombre"]), esc(B.CURSO["descripcion"]), nav,
       "\n".join(seccion(*v) for v in todas))
    io.open(salida, "w", encoding="utf-8", newline="\n").write(html)
    print("%s  %d preguntas en %d secciones" % (salida, total, len(todas)))


if __name__ == "__main__":
    main()
