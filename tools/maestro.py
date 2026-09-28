# -*- coding: utf-8 -*-
"""Arma docs/MAESTRO.md: toda la documentacion general en un solo archivo, con indice.

El maestro es GENERADO. Se edita cada documento fuente y luego se reconstruye:

    python tools/maestro.py              # escribe docs/MAESTRO.md
    python tools/maestro.py --verificar  # falla si el maestro no esta al dia

Que entra y en que orden lo fija CAPITULOS. Cada documento se vuelve un capitulo:
su titulo se reemplaza por el del capitulo, sus encabezados bajan de nivel y sus
enlaces relativos se reescriben (a otro capitulo, o a la ruta vista desde docs/).
Los .md de videos/ no entran: son de cada proyecto.
"""
import io, os, posixpath, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = "docs/MAESTRO.md"

# (numero, titulo, ruta | None para una parte con subcapitulos, [subcapitulos])
CAPITULOS = [
    ("0", "Cómo usar esta documentación", "docs/README.md", []),
    ("1", "Paso a paso", "docs/PASO-A-PASO.md", []),
    ("2", "Ecosistema de marcas", "docs/marcas/ECOSISTEMA.md", []),
    ("3", "Fichas de marca", None, [
        ("3.1", "SOFU BIC S.A.S.", "docs/marcas/sofu/ficha.md"),
        ("3.2", "RiskMann", "docs/marcas/riskmann/ficha.md"),
        ("3.3", "FEGIR", "docs/marcas/fegir/ficha.md"),
        ("3.4", "Dr. Yezid Ricaurte", "docs/marcas/yezid-ricaurte/ficha.md"),
    ]),
    ("4", "Glosario", "docs/marcas/GLOSARIO.md", []),
    ("5", "Playbook", "docs/PLAYBOOK.md", []),
    ("6", "Estándar de producción", "PRODUCCION-VIDEOS.md", []),
    ("7", "Guía de prompts", "GUIA-PROMPTS.md", []),
    ("8", "Arranque en otro equipo", "docs/ARRANQUE-EN-OTRO-EQUIPO.md", []),
    ("9", "Plataforma: ideas y decisiones", "docs/PLATAFORMA.md", []),
    ("10", "Anexos", None, [
        ("10.1", "Bitácora del 17 y 18 de septiembre", "docs/BITACORA-2026-09-17-18.md"),
        ("10.2", "PoC Seguridad Vial para Pasajeros", "docs/POC-SEGURIDAD-VIAL-PASAJEROS.md"),
        ("10.3", "Lectura del manual de RiskMann", "docs/marcas/riskmann/LEEME.md"),
        ("10.4", "README del repositorio", "README.md"),
        ("10.5", "Instrucciones para agentes (CLAUDE.md)", "CLAUDE.md"),
    ]),
]

ENLACE = re.compile(r"(\]\()([^)\s]+)(\))|((?:src|href)=\")([^\"]+)(\")")
CERCA = re.compile(r"^\s*(```|~~~)")
TITULO = re.compile(r"^(#{1,6})(\s+.*)$")


def ancla(num):
    return "cap-" + num.replace(".", "-")


def fuentes():
    for num, tit, ruta, subs in CAPITULOS:
        if ruta:
            yield num, tit, ruta
        for s in subs:
            yield s


RUTA_A_ANCLA = {ruta: ancla(num) for num, _, ruta in fuentes()}


def capitulo(num, tit, ruta, nivel):
    """Un documento convertido en capitulo de nivel `nivel` (2 o 3)."""
    txt = io.open(os.path.join(RAIZ, ruta), encoding="utf-8").read().replace("\r\n", "\n")
    lineas = txt.split("\n")
    base = posixpath.dirname(ruta)

    def enlace(destino):
        if re.match(r"^[a-z]+:|^#|^/", destino):
            return destino
        camino, _, frag = destino.partition("#")
        abs_ = posixpath.normpath(posixpath.join(base, camino)) if camino else ruta
        if abs_ in RUTA_A_ANCLA:
            return "#" + RUTA_A_ANCLA[abs_]
        rel = posixpath.relpath(abs_, "docs")
        if camino.endswith("/"):
            rel += "/"
        return rel + ("#" + frag if frag else "")

    def sub(m):
        if m.group(1):
            return m.group(1) + enlace(m.group(2)) + m.group(3)
        return m.group(4) + enlace(m.group(5)) + m.group(6)

    salida, en_codigo, titulo_quitado = [], False, False
    for l in lineas:
        if CERCA.match(l):
            en_codigo = not en_codigo
            salida.append(l)
            continue
        if not en_codigo:
            m = TITULO.match(l)
            if m and len(m.group(1)) == 1 and not titulo_quitado:
                titulo_quitado = True        # el titulo del documento lo pone el capitulo
                continue
            if m:
                l = "#" * min(6, len(m.group(1)) + nivel - 1) + m.group(2)
            l = ENLACE.sub(sub, l)
        salida.append(l)

    cuerpo = "\n".join(salida).strip("\n")
    cab = "#" * nivel
    return (f'<a id="{ancla(num)}"></a>\n\n{cab} {num}. {tit}\n\n'
            f"> Fuente: [`{ruta}`]({posixpath.relpath(ruta, 'docs')}) — se edita ahí, no aquí.\n\n"
            f"{cuerpo}\n")


def armar():
    indice, partes = [], []
    for num, tit, ruta, subs in CAPITULOS:
        indice.append(f"- [{num}. {tit}](#{ancla(num)})")
        if ruta:
            partes.append(capitulo(num, tit, ruta, 2))
        else:
            partes.append(f'<a id="{ancla(num)}"></a>\n\n## {num}. {tit}\n')
        for snum, stit, sruta in subs:
            indice.append(f"  - [{snum}. {stit}](#{ancla(snum)})")
            partes.append(capitulo(snum, stit, sruta, 3))

    cabecera = (
        "# Documento maestro — riskmann2-marketing-videos\n\n"
        "> **Archivo generado. No se edita a mano.** Reúne en un solo lugar la documentación\n"
        "> general del repositorio. Para cambiar algo, edita el documento fuente que aparece al\n"
        "> inicio de cada capítulo y reconstruye con `python tools/maestro.py`.\n"
        "> Los documentos propios de cada video (`videos/<proyecto>/*.md`) no están aquí.\n\n"
        "## Índice\n\n" + "\n".join(indice) + "\n"
    )
    return cabecera + "\n---\n\n" + "\n---\n\n".join(partes)


def main():
    nuevo = armar()
    destino = os.path.join(RAIZ, SALIDA)
    if "--verificar" in sys.argv:
        actual = io.open(destino, encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists(destino) else ""
        if actual != nuevo:
            sys.exit(f"{SALIDA} no está al día: corre python tools/maestro.py")
        print(f"{SALIDA} al día")
        return
    io.open(destino, "w", encoding="utf-8", newline="\n").write(nuevo)
    print(f"{SALIDA}: {nuevo.count(chr(10))} líneas, {sum(1 for _ in fuentes())} documentos")


if __name__ == "__main__":
    main()
