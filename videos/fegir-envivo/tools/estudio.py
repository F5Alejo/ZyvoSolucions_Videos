# -*- coding: utf-8 -*-
"""Reorganiza fegir-envivo para el Studio de HyperFrames (se ejecuto una vez).

Parte de tools/index-antes-de-studio.html (la composicion en un solo archivo)
y escribe:
  compositions/<escena>.html  una sub-composicion por escena (fila propia)
  index.html                  solo anfitriones + audio (voz, efectos, musica)

Despues de esto, el index.html y compositions/ son la fuente: se editan en el
Studio o a mano, no se vuelve a correr este script (lo sobrescribiria todo).

    python tools/estudio.py
"""
import io, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
src = io.open('tools/index-antes-de-studio.html', encoding='utf-8').read()
css = src[src.index('<style>') + 7:src.index('</style>')]


def bloque(ini, fin):
    a = css.index(ini)
    b = css.index(fin, a) if fin else len(css)
    return css[a:b]


FONTS = bloque('      @font-face', '\n\n      * {')
TOKENS = '''
          --verde:        #45a035;
          --verde-claro:  #a8c875;
          --crema:        #f1ecb0;
          --banda-a:      #50cd72;
          --banda-b:      #4ecd25;
          --verde-fondo:  #3a8f2c;
          --verde-hondo:  #22621a;
          --tinta:        #1d2b1a;'''
CORT_CSS = bloque('      .cortina {', '      /* ---------- plano 2')
P1 = bloque('      #foto-caja {', '      /* ---------- cortinas')
P2 = bloque('      #logo-blanco {', '      /* ---------- plano 3')
P3 = bloque('      #visto {', '      /* ---------- plano 4')
P4 = bloque('      #cal {', '      /* ---------- plano 5')
P5 = bloque('      #cta-rot {', '      /* ---------- sello')
SELLO = bloque('      #sello {', None)

TIEMPOS = '''
        /* TIEMPOS - globales, en segundos del video completo.
           V: inicio de cada toma de voz (tools/tiempos-voz.json + index.html).
           S: inicio de ESTA escena (su data-start en index.html).
           Si mueves la escena en el Studio, cambia S aqui tambien. */
        var V = { f1: 0.30, f2: 3.75, f3: 7.05, f4: 10.45, f5: 13.70, f6: 16.20 };
        var CORT = 0.40;   // la cortina entra 0.40 s antes de su frase
        var S = %s;
        var L = function (t) { return t - S; };   // global -> local
'''


def archivo(cid, estilos, cuerpo, js, fondo):
    return '''<!doctype html>
<html lang="es">
  <head><meta charset="UTF-8"><title>%s</title></head>
  <body>
    <template>
      <style>
%s
        #root {
          position: absolute; inset: 0; overflow: hidden; background: %s;
          font-family: "FEGIR Sans", sans-serif; color: #fff;%s
        }
        .capa { position: absolute; inset: 0; }
%s
      </style>

      <div id="root" data-composition-id="%s" data-width="1080" data-height="1920">
%s
      </div>

      <script>
      (function () {
        window.__timelines = window.__timelines || {};
        var tl = gsap.timeline({ paused: true });
%s
        window.__timelines["%s"] = tl;
      })();
      </script>
    </template>
  </body>
</html>
''' % (cid, FONTS, fondo, TOKENS, estilos.rstrip(), cid, cuerpo, js, cid)


def cortina(sel, rot, frase):
    return '''
        tl.fromTo("#%s", { rotation: %d, yPercent: 105 },
          { rotation: %d, yPercent: 0, duration: 0.75, ease: "power3.inOut" }, L(V.%s - CORT));
        tl.fromTo("#%s", { rotation: %d }, { rotation: 0, immediateRender: false, duration: 0.9, ease: "power2.out" }, L(V.%s + 0.2));
''' % (sel, rot, rot, frase, sel, rot, frase)


ESC = [
  ('escena-pregunta', P1, '''        <div id="foto-caja" class="capa">
          <img id="foto" src="assets/fotos/portada-manual-vertical.jpg" alt="">
          <div id="foto-tinte" class="capa"></div>
          <div id="foto-sombra" class="capa"></div>
          <div id="pregunta">
            <div class="l"><span>¿Tu informe</span></div>
            <div class="l"><span class="marca">PESV</span> <span>todavía</span></div>
            <div class="l"><span>se arma a mano?</span></div>
          </div>
        </div>''', TIEMPOS % '0' + '''
        // la foto respira y la pregunta sube por mascara
        tl.fromTo("#foto", { scale: 1.12, y: 0 }, { scale: 1.0, y: -40, duration: 4.1, ease: "none" }, 0);
        tl.fromTo("#pregunta .l span", { yPercent: 110 },
          { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.28 }, L(V.f1));''',
   0, 4.1, '#2e7a22', 1, 1, '1 · la pregunta, sobre la foto del manual'),

  ('escena-invita', CORT_CSS + P2, '''        <div id="cortina-verde" class="cortina"><div class="filo"></div></div>
        <img id="logo-blanco" src="assets/logo/fegir-logo-blanco.png" alt="FEGIR">
        <div id="invita">te invita a un</div>
        <div id="envivo" data-layout-allow-overlap>EN VIVO</div>
        <div id="gratis">Gratuito</div>''', TIEMPOS % '3.30' + cortina('cortina-verde', -32, 'f2') + '''
        var envivo = V.f2 + 1.42;   // "a un en vivo" arranca en +1.416
        tl.fromTo("#logo-blanco", { opacity: 0, y: 40, scale: 0.92 },
          { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "expo.out" }, L(V.f2 + 0.05));
        tl.fromTo("#invita", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(V.f2 + 0.9));
        tl.fromTo("#envivo", { opacity: 0, scale: 1.5, filter: "blur(20px)" },
          { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power4.out" }, L(envivo));
        tl.fromTo("#gratis", { opacity: 0, scale: 0.6 },
          { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2)" }, L(envivo + 0.55));''',
   3.30, 4.1, 'transparent', 2, 2, '2 · FEGIR te invita a un EN VIVO (verde)'),

  ('escena-tema', CORT_CSS + P3, '''        <div id="cortina-blanca" class="cortina"><div class="filo"></div></div>
        <svg id="visto" viewBox="0 0 300 240"><path id="visto-trazo" d="M 30 120 L 110 200 L 270 30"/></svg>
        <div id="tema-rot">El tema</div>
        <div id="tema">
          <div class="l"><span>Informe de</span></div>
          <div class="l"><span>Autogestión PESV</span></div>
        </div>
        <div id="clic">en 1 clic</div>''', TIEMPOS % '6.60' + cortina('cortina-blanca', 28, 'f3') + '''
        var clic = V.f3 + 1.85;   // "en un solo clic" en +1.927
        tl.fromTo("#visto-trazo", { strokeDasharray: 420, strokeDashoffset: 420 },
          { strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, L(V.f3 + 0.05));
        tl.fromTo("#tema-rot", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(V.f3 + 0.1));
        tl.fromTo("#tema .l span", { yPercent: 110 },
          { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.25 }, L(V.f3 + 0.2));
        tl.fromTo("#clic", { opacity: 0, scale: 0.5 },
          { opacity: 1, scale: 1, duration: 0.65, ease: "back.out(2.2)" }, L(clic));''',
   6.60, 4.2, 'transparent', 1, 3, '3 · el tema, con el visto (blanco)'),

  ('escena-fecha', CORT_CSS + P4, '''        <div id="cortina-verde2" class="cortina"><div class="filo"></div></div>
        <div id="cal">
          <div id="cal-cab">SÁBADO</div>
          <div id="cal-num">3</div>
          <div id="cal-mes">OCTUBRE</div>
        </div>
        <div id="hora">10:00 a. m.</div>
        <div id="zona">Hora Colombia</div>''', TIEMPOS % '10.00' + cortina('cortina-verde2', -32, 'f4') + '''
        var hora = V.f4 + 1.55;   // "a las diez" en +1.614
        tl.fromTo("#cal", { opacity: 0, y: -260, rotation: -8 },
          { opacity: 1, y: 0, rotation: 0, duration: 0.9, ease: "back.out(1.4)" }, L(V.f4 + 0.1));
        tl.fromTo("#cal-num", { scale: 0.4 }, { scale: 1, duration: 0.7, ease: "back.out(2.4)" }, L(V.f4 + 0.55));
        tl.fromTo("#hora", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(hora));
        tl.fromTo("#zona", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(hora + 0.25));''',
   10.00, 4.05, 'transparent', 2, 4, '4 · la fecha, hoja de calendario (verde)'),

  ('escena-reserva', CORT_CSS + P5, '''        <div id="cortina-blanca2" class="cortina"><div class="filo"></div></div>
        <div id="cta-rot">Cupos limitados</div>
        <div id="boton">Reserva tu cupo gratis</div>
        <div id="web">fegir.org</div>
        <div id="resumen">En vivo · sábado 3 de octubre · 10:00 a. m.</div>
        <img id="logo-color" src="assets/logo/fegir-logo-color.png" alt="FEGIR - Fundación Especializada en Gestión Integral del Riesgo">
        <div id="lema">¡Tu seguridad, nuestra prioridad!</div>''', TIEMPOS % '13.25' + cortina('cortina-blanca2', 28, 'f5') + '''
        var FIN = 19.5;
        var web = V.f5 + 1.05;    // "en fegir punto org" en +1.126
        var lema = V.f6 + 0.62;   // "tu seguridad" en +0.673
        tl.fromTo("#cta-rot", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(V.f5));
        tl.fromTo("#boton", { opacity: 0, scale: 0.55 },
          { opacity: 1, scale: 1, duration: 0.75, ease: "back.out(1.9)" }, L(V.f5 + 0.15));
        tl.fromTo("#web", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(web));
        tl.fromTo("#resumen", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, L(web + 0.3));
        // el logo primario, como lo pide el manual
        tl.fromTo("#logo-color", { opacity: 0, y: 40, scale: 0.94 },
          { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: "expo.out" }, L(V.f6 - 0.10));
        tl.fromTo("#lema", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, L(lema));
        // el boton respira hasta el final (tweens explicitos, seek-safe)
        for (var b = 0; V.f5 + 1.2 + b * 1.2 < FIN - 0.6; b++) {
          var tb = V.f5 + 1.2 + b * 1.2;
          tl.to("#boton", { scale: 1.045, duration: 0.6, ease: "sine.inOut" }, L(tb));
          tl.to("#boton", { scale: 1.0, duration: 0.6, ease: "sine.inOut" }, L(tb + 0.6));
        }''',
   13.25, 6.25, 'transparent', 1, 5, '5 · reserva y logo (blanco)'),

  ('sello-envivo', SELLO, '''        <div id="sello">
          <span id="latido"><i></i><span id="aro"></span></span>En vivo · 3 oct
        </div>''', '''
        var FIN = 19.5;
        tl.fromTo("#sello", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.55, ease: "back.out(1.6)" }, 0.3);
        for (var k = 0; 0.7 + 1.2 * k < FIN - 1.0; k++) {
          var tp = 0.7 + 1.2 * k;
          tl.to("#latido i", { scale: 1.3, duration: 0.16, ease: "power2.out" }, tp);
          tl.to("#latido i", { scale: 1.0, duration: 0.44, ease: "power2.inOut" }, tp + 0.16);
          tl.fromTo("#aro", { scale: 0.55, opacity: 0.8 },
            { scale: 2.1, opacity: 0, immediateRender: false, duration: 0.9, ease: "power2.out" }, tp);
        }''',
   0, 19.5, 'transparent', 3, 10, 'sello EN VIVO, presente todo el video'),
]

hosts = []
for cid, estilos, cuerpo, js, start, dur, fondo, pista, z, nota in ESC:
    io.open('compositions/%s.html' % cid, 'w', encoding='utf-8', newline='\n').write(
        archivo(cid, estilos, cuerpo, js, fondo))
    hosts.append('''      <!-- %s -->
      <div id="%s" data-composition-id="%s" data-composition-src="compositions/%s.html"
        data-track-kind="graphics" data-start="%s" data-duration="%s" data-track-index="%d"
        data-width="1080" data-height="1920" style="z-index:%d"></div>''' % (nota, cid, cid, cid, start, dur, pista, z))

# ---------------- audio ----------------
V = {1: 0.30, 2: 3.75, 3: 7.05, 4: 10.45, 5: 13.70, 6: 16.20}
DUR = {1: 3.02, 2: 2.88, 3: 2.97, 4: 2.83, 5: 2.04, 6: 2.32}   # tools/tiempos-voz.json
FIN, CORT = 19.5, 0.40
voz = ['      <audio id="voz-%d" src="assets/mezcla/voz-%d.wav" data-start="%.2f" data-duration="%.2f" '
       'data-track-index="10" data-volume="1"></audio>' % (n, n, V[n], DUR[n]) for n in V]

SFX = {"cortina": (1.0, 0.35, [V[2] - CORT, V[3] - CORT, V[4] - CORT, V[5] - CORT]),
       "visto": (0.8, 0.45, [V[3] + 0.05]),
       "pop": (0.5, 0.40, [V[2] + 1.42 + 0.55, V[3] + 1.85, V[5] + 0.15]),
       "golpe": (1.5, 0.55, [V[2] + 1.42]),
       "hoja": (0.9, 0.45, [V[4] + 0.1]),
       "brillo": (1.6, 0.40, [V[6] - 0.10])}
ev = sorted((t, n, d, g) for n, (d, g, ts) in SFX.items() for t in ts)
fin_pista, cont, sfx = {11: -1.0, 12: -1.0}, {}, []
for t, n, d, g in ev:
    pista = 11 if fin_pista[11] <= t else 12   # dos filas: los efectos nunca se pisan en una misma fila
    fin_pista[pista] = t + d
    cont[n] = cont.get(n, 0) + 1
    sfx.append('      <audio id="sfx-%s-%d" src="assets/sfx/%s.mp3" data-start="%.2f" data-duration="%.2f" '
               'data-track-index="%d" data-volume="%.2f"></audio>' % (n, cont[n], n, t, d, pista, g))

# la cama baja bajo cada frase y vuelve a subir entre frases
BASE, BAJO = 0.30, 0.13
pts = [(0, 0), (0.4, BASE)]
for n in V:
    a, b = V[n], V[n] + DUR[n]
    pts += [(max(a - 0.12, 0.41), BASE), (a, BAJO), (b, BAJO), (b + 0.3, BASE)]
pts += [(FIN - 1.6, BASE), (FIN, 0)]
auto = json.dumps({"version": 1, "lanes": [{"target": "volume",
                   "points": [{"t": round(t, 2), "v": v} for t, v in pts]}]}, separators=(',', ':'))
musica = ('      <audio id="musica-cama" src="assets/musica/cama.mp3" data-start="0" data-duration="%s" '
          'data-track-index="13" data-volume="1"\n        data-automation=\'%s\'></audio>' % (FIN, auto))

INDEX = '''<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
    <style>
      /* ==================================================================
         FEGIR · EN VIVO PESV — pieza PROPIA de la fundacion, sin otra marca.
         Organizada para el Studio de HyperFrames: aqui solo hay ANFITRIONES
         (una fila por escena) y AUDIO (voz, efectos, musica). Cada escena
         vive en compositions/ con su estilo y su animacion.

         Identidad: Fegir.org/Manual identidad FEGIR.pdf
           #45a035 verde · #a8c875 verde claro · #f1ecb0 crema
           banda del manual #50cd72 -> #4ecd25 · letra Segoe UI
         Las escenas alternan verde y blanco; el orden de apilado lo da el
         z-index de cada anfitrion (el numero de pista es solo visual).
         ================================================================== */
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #2e7a22; }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #2e7a22; }
      #root > div { position: absolute; inset: 0; }
    </style>
  </head>

  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="1080" data-height="1920">
%s

      <!-- VOZ · Carlos (ElevenLabs), una toma por frase, niveladas a -15 LUFS -->
%s

      <!-- EFECTOS · ElevenLabs, cada uno en el instante visual que lo justifica -->
%s

      <!-- MUSICA · cama generada para FEGIR; baja sola bajo cada frase (curva de volumen) -->
%s
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
'''
io.open('index.html', 'w', encoding='utf-8', newline='\n').write(
    INDEX % (FIN, '\n'.join(hosts), '\n'.join(voz), '\n'.join(sfx), musica))
print('escenas:', len(ESC), '· efectos:', len(sfx))
