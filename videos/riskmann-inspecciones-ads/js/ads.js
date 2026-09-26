// Los tres anuncios de 12 s. Un timeline de GSAP en pausa por anuncio: nada corre por
// su cuenta (sin setTimeout, sin Math.random en tiempo de reproducción), así que
// cualquier segundo se puede buscar y sale idéntico — la condición de HyperFrames.
import { bgState } from "./bg.js";

/* global gsap */

// Estructura de 12 s del storyboard — todas las posiciones cuelgan de aquí.
export const videoTimelines = { hook: 0.0, valor: 2.0, cta: 8.0, end: 12.0 };
const T = videoTimelines;

// Reglas físicas: cero fades lineales. Toda entrada usa una de estas dos.
const IN = "power4.out";
const POP = "back.out(1.5)";
const OUT = "power4.in"; // solo para salidas

// Versión. V1: rojo en todo acento. V2: el rojo queda SOLO para peligro (novedad pendiente,
// grietas, No apto, EXPUESTA, la aguja que se come el tiempo); lo que llama a la acción
// —TODOS, «al día?», REGÍSTRATE HOY, el botón— pasa al dorado del manual / de la landing.
export const VERSION = new URLSearchParams(location.search).get("v") === "2" ? 2 : 1;
const ACCENT = VERSION === 2 ? "200,149,26" : "255,51,51"; // #c8951a : #FF3333

// ─────────────────────────── Guiones (Agente 1) ───────────────────────────
// Texto listo para ElevenLabs `eleven_v3` (voz «Carlos», 4PN5DHmrfIgZksvIrawS).
// Cada frase sale literal o casi literal de riskmann.com/inspecciones-gratis/.
export const SCRIPTS = {
  ad1: {
    name: "AD 1 · Autodiagnóstico",
    segs: [
      { id: "hook", t: "0 – 2 s", vo: "¿Inspeccionas TODOS tus vehículos?", dir: "Pregunta seca, énfasis en TODOS. Sin respirar antes." },
      { id: "valor", t: "2 – 8 s", vo: "¿Cuándo fue la última vez que revisaste una? · Con RiskMann… la haces desde el celular. ¡En MINUTOS!", dir: "El guion largo abre el silencio antes de la pregunta; se acelera en «desde el celular» y remata «en minutos»." },
      { id: "cta", t: "8 – 12 s", vo: "¡Regístrate HOY! Gratis… y sin tarjeta.", dir: "Golpe comercial: «HOY» cae con el overshoot en pantalla." },
    ],
    board: [
      ["0.00", "Eyebrow «Inspección preoperacional · 100% gratis» entra desde la izquierda. Fondo con tensión roja leve."],
      ["0.10", "Cascada: «¿Inspeccionas» → «TODOS» (rojo, 280 px, pop 1.6→1) → «tus vehículos?»."],
      ["1.78", "Salida del hook hacia arriba (power4.in)."],
      ["2.00", "Pulso del fondo. «¿Cuándo fue la última vez…?» en cascada. El reloj SVG se DIBUJA (stroke-dashoffset 1→0): aro, aro interior, 12 marcas."],
      ["2.60", "Agujas aparecen (back.out) y giran 720°: el tiempo que se va. El líquido se retuerce."],
      ["4.40", "El reloj se encoge a la izquierda; la tarjeta Glassmorphism del celular sube (back.out) y el fondo vira a cian."],
      ["4.80", "Los tres pasos de la landing en cascada; los checks se trazan en 5.6 / 6.2 / 6.8."],
      ["7.10", "Sello «EN MINUTOS». La tarjeta flota en Y (ambient idle)."],
      ["8.00", "SPECTACLE BEAT: «REGÍSTRATE HOY» 1.5→1.0 con overshoot violento + drop-shadow rojo + sacudida + destello del fondo."],
      ["8.55", "Botón «Quiero mi inspección gratis» · «Gratis · Sin tarjeta de crédito» · logo · URL."],
    ],
  },
  ad2: {
    name: "AD 2 · Consecuencia",
    segs: [
      { id: "hook", t: "0 – 2 s", vo: "Papel. Excel. WhatsApp.", dir: "Tono de problema. Cada palabra cae con su tarjeta." },
      { id: "valor", t: "2 – 8 s", vo: "Y el vehículo… sigue rodando. · Con una novedad pendiente. · ¿Quién lo inspeccionó? ¿Cuándo?", dir: "Sigue el problema hasta el segundo 8: grave, sin alivio todavía." },
      { id: "cta", t: "8 – 12 s", vo: "Tranquilo… RiskMann lo centraliza todo. ¡Regístrate hoy!", dir: "Cambio de color: alivio, sonrisa en la voz." },
    ],
    board: [
      ["0.05", "Tarjetas Papel / Excel / WhatsApp caen en cascada (back.out) sincronizadas con la voz. Fondo en rojo."],
      ["2.00", "«El vehículo sigue rodando…» en cascada."],
      ["3.10", "«con una novedad pendiente.» en rojo; la tensión del fondo sube al máximo; las tarjetas tiemblan."],
      ["3.40", "Grietas rojas se trazan sobre cada tarjeta."],
      ["4.40", "«¿Quién lo inspeccionó? ¿Cuándo?»"],
      ["5.50", "QUIEBRE: las tres tarjetas estallan en 8 esquirlas cada una; destello del fondo."],
      ["6.00", "«Todo en un solo lugar.» + interfaz móvil Glassmorphism brillante (barrido de brillo). Fondo vira de rojo a cian."],
      ["6.60", "Resultados de la landing: Apto · Con control específico · No apto. La tarjeta flota."],
      ["8.00", "SPECTACLE BEAT «REGÍSTRATE HOY» + «Todo en un solo lugar · Gratis» · logo · URL."],
    ],
  },
  ad3: {
    name: "AD 3 · Urgencia",
    segs: [
      { id: "hook", t: "0 – 2 s", vo: "¿Tu técnico-mecánica al día?", dir: "Pregunta de control, como un auditor." },
      { id: "valor", t: "2 – 8 s", vo: "¿Y la inspección diaria del P-E-S-V? · Sin registro, tu empresa queda… EXPUESTA.", dir: "Doble pausa antes de revelar la exposición; «EXPUESTA» cae seca." },
      { id: "cta", t: "8 – 12 s", vo: "¡Regístrate HOY! RiskMann la registra gratis.", dir: "Solución firme, no alarmista." },
    ],
    board: [
      ["0.10", "«¿Tu técnico‑mecánica… al día?» en cascada; «al día?» en rojo con pop."],
      ["0.50", "Tarjeta Glass «Hoja de vida del vehículo»: SOAT / Revisión técnico‑mecánica / Inspección de hoy con «?» dorados que laten."],
      ["2.00", "«El PESV exige registrar la inspección…» en cascada."],
      ["3.00", "«todos los días.» grande + línea dorada; píldora «Resolución 20223040040595 de 2022 · Paso 16»."],
      ["4.70", "PAUSA: el texto sale, el fondo se tensa (heat ↑) en silencio."],
      ["4.90", "«Sin registro… tu empresa queda»"],
      ["5.70", "«EXPUESTA» golpea (2.2→1, back.out) con sacudida y destello rojo."],
      ["6.20", "El texto sube; el ESCUDO se ensambla pieza por pieza (6 piezas, back.out, stagger)."],
      ["7.10", "Contorno cian y check blanco se trazan; «PESV · Paso 16». Fondo pasa a cian."],
      ["8.00", "SPECTACLE BEAT «REGÍSTRATE HOY» + «Aplica para todos los niveles del PESV» · logo · URL."],
    ],
  },
};

// ─────────────────────────── utilidades de movimiento ───────────────────────────
const $ = (root, s) => root.querySelector(s);
const $$ = (root, s) => [...root.querySelectorAll(s)];

function enterWords(tl, els, at, { y = 80, d = 0.75, s = 0.09, ease = IN } = {}) {
  tl.fromTo(els, { opacity: 0, y }, { opacity: 1, y: 0, duration: d, ease, stagger: s }, at);
  tl.fromTo(els, { filter: "blur(10px)" }, { filter: "blur(0px)", duration: 0.35, ease: "power2.out", stagger: s, immediateRender: false }, at);
}

function exitLayer(tl, el, at, d = 0.28) {
  tl.to(el, { opacity: 0, y: -110, scale: 0.96, duration: d, ease: OUT }, at);
}

// Ambient idle: flotación continua en Y, seek-safe (repeticiones contadas, sin loop infinito).
function idle(tl, el, from, to, amp = 18, period = 2.4) {
  const half = period / 2;
  const reps = Math.max(1, Math.floor((to - from) / half));
  tl.fromTo(el, { y: 0 }, { y: -amp, duration: half, ease: "sine.inOut", repeat: reps - 1, yoyo: true }, from);
}

function sheen(tl, glass, at) {
  const s = $(glass, ".sheen");
  if (s) tl.fromTo(s, { x: 0 }, { x: 1500, duration: 1.3, ease: "power2.inOut" }, at);
}

function draw(tl, els, at, d = 0.6, s = 0) {
  tl.fromTo(els, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: IN, stagger: s }, at);
}

function shake(tl, el, at, k = 1) {
  tl.to(el, {
    keyframes: [
      { x: -22 * k, y: 10 * k, duration: 0.045 },
      { x: 18 * k, y: -8 * k, duration: 0.045 },
      { x: -11 * k, y: 5 * k, duration: 0.05 },
      { x: 6 * k, y: -3 * k, duration: 0.06 },
      { x: 0, y: 0, duration: 0.08 },
    ],
  }, at);
}

function flash(tl, at, peak = 1) {
  tl.to(bgState, { pulse: peak, duration: 0.07, ease: IN }, at);
  tl.to(bgState, { pulse: 0, duration: 0.8, ease: "power2.out" }, at + 0.07);
}

function common(tl, root) {
  tl.fromTo($(root, ".eyebrow"), { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.8, ease: IN }, 0.05);
  tl.fromTo($(root.closest("#stage"), ".progress i"), { scaleX: 0 }, { scaleX: 1, duration: T.end, ease: "none" }, 0);
}

// ─────────────────────────── CTA compartido · Spectacle Beat ───────────────────────────
function buildCTA(root) {
  const L = $(root, ".layer.cta");
  L.innerHTML = `
    <div class="cta-title"><span class="c1">REGÍSTRATE</span><span class="c2">HOY</span></div>
    <div class="cta-pill-box"><span class="cta-pill">Quiero mi inspección gratis</span></div>
    <div class="cta-sub">${L.dataset.sub}</div>
    <!-- ASSET DE MARCA: logo oficial en blanco (assets/public/riskmann_logo_blanco.png). Nunca redibujar ni recolorear. -->
    <img class="cta-logo" src="assets/riskmann_logo_blanco.png" alt="RiskMann" />
    <div class="cta-url">riskmann.com/inspecciones-gratis</div>`;
  gsap.set(L, { autoAlpha: 0 });
  return L;
}

function cta(tl, root) {
  const L = buildCTA(root);
  const title = $(L, ".cta-title");
  tl.set(L, { autoAlpha: 1 }, T.cta);

  // Overshoot violento 1.5 → 1.0 (back.out(4) baja hasta ~0.86 y rebota)
  tl.fromTo(title, { scale: 1.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.95, ease: "back.out(4)" }, T.cta);
  // Resplandor dinámico: estallido, asentamiento y respiración
  tl.fromTo(title, { filter: `drop-shadow(0px 0px 0px rgba(${ACCENT},0))` },
    { filter: `drop-shadow(0px 0px 80px rgba(${ACCENT},1))`, duration: 0.18, ease: IN }, T.cta);
  tl.to(title, { filter: `drop-shadow(0px 0px 26px rgba(${ACCENT},0.55))`, duration: 0.7, ease: "power2.out" }, T.cta + 0.2);
  tl.to(title, { filter: `drop-shadow(0px 0px 60px rgba(${ACCENT},0.9))`, duration: 0.55, ease: "sine.inOut", repeat: 3, yoyo: true }, T.cta + 1.0);

  shake(tl, $(root, ".shake"), T.cta + 0.04, 1.2);
  if (VERSION === 2) tl.to(bgState, { gold: 1, duration: 0.05, ease: IN }, T.cta - 0.06);
  flash(tl, T.cta, 1);
  tl.to(bgState, { zoom: 0.8, warp: 0.7, duration: 1.4, ease: IN }, T.cta);

  tl.fromTo($(L, ".cta-pill"), { opacity: 0, scale: 0.55, y: 50 }, { opacity: 1, scale: 1, y: 0, duration: 0.75, ease: POP }, T.cta + 0.55);
  tl.fromTo($(L, ".cta-pill"), { scale: 1 }, { scale: 1.045, duration: 0.5, ease: "sine.inOut", repeat: 4, yoyo: true, immediateRender: false }, T.cta + 1.4);
  tl.fromTo($(L, ".cta-sub"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, T.cta + 0.85);
  tl.fromTo($(L, ".cta-logo"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.8, ease: POP }, T.cta + 1.1);
  tl.fromTo($(L, ".cta-url"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, T.cta + 1.35);
}

// ─────────────────────────── AD 1 · Autodiagnóstico ───────────────────────────
function ad1(root) {
  const tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), valor = $(root, ".valor");

  // marcas del reloj
  const g = $(root, ".ticks");
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2, major = i % 3 === 0;
    const r1 = major ? 116 : 126, r2 = 140;
    const l = document.createElementNS("http://www.w3.org/2000/svg", "line");
    l.setAttribute("x1", 200 + Math.sin(a) * r1); l.setAttribute("y1", 200 - Math.cos(a) * r1);
    l.setAttribute("x2", 200 + Math.sin(a) * r2); l.setAttribute("y2", 200 - Math.cos(a) * r2);
    l.setAttribute("pathLength", "1");
    l.setAttribute("class", "draw tick" + (major ? " major" : ""));
    g.appendChild(l);
  }

  tl.fromTo(bgState, { heat: 0, calm: 0, pulse: 0, gold: 0, warp: 0, zoom: 1.15 }, { heat: 0.35, zoom: 1, duration: 2, ease: IN }, 0);
  common(tl, root);

  // HOOK 0–2
  enterWords(tl, $$(hook, ".w"), T.hook + 0.1, { y: 100, s: 0.22 });
  tl.fromTo($(hook, ".mega"), { scale: 1.6 }, { scale: 1, duration: 0.8, ease: POP }, T.hook + 0.32);
  exitLayer(tl, hook, T.valor - 0.22, 0.24);

  // VALOR 2–8 — el reloj se dibuja en el segundo 2
  enterWords(tl, $$(root, ".q1 .w"), T.valor, { y: 60, s: 0.08 });
  flash(tl, T.valor, 0.45);
  tl.to(bgState, { warp: 0.9, duration: 2.4, ease: "power2.inOut" }, T.valor);
  const cw = $(root, ".clock-wrap");
  tl.fromTo(cw, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.9, ease: IN }, T.valor);
  draw(tl, $(root, ".ring"), T.valor, 1.1);
  draw(tl, $(root, ".ring-in"), T.valor + 0.12, 1.1);
  draw(tl, $$(root, ".tick"), T.valor + 0.2, 0.4, 0.045);
  // el pivote se fija una vez: pasarlo dentro de un tween con varios objetivos lo desplaza
  $$(root, ".hand, .hub").forEach((h) => gsap.set(h, { svgOrigin: "200 200" }));
  tl.fromTo($$(root, ".hand, .hub"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: POP }, T.valor + 0.6);
  tl.fromTo($(root, ".min"), { rotation: 0 }, { rotation: 720, duration: 2.2, ease: "power2.inOut", immediateRender: false }, T.valor + 0.6);
  tl.fromTo($(root, ".hour"), { rotation: 0 }, { rotation: 60, duration: 2.2, ease: "power2.inOut", immediateRender: false }, T.valor + 0.6);

  // 4.4 — la solución: el celular
  tl.to(cw, { x: -300, y: -140, scale: 0.46, duration: 0.8, ease: IN }, 4.4);
  tl.to(bgState, { heat: 0, calm: 0.85, duration: 1.6, ease: "power2.inOut" }, 4.4);
  tl.to(bgState, { warp: 0.2, duration: 1.2, ease: "power2.out" }, 4.4);
  const phone = $(root, ".phone");
  tl.fromTo(phone, { opacity: 0, y: 700, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 1.0, ease: POP }, 4.5);
  sheen(tl, phone, 5.3);
  tl.fromTo($$(root, ".steps li"), { opacity: 0, x: 70 }, { opacity: 1, x: 0, duration: 0.6, ease: IN, stagger: 0.12 }, 4.85);
  $$(root, ".steps path").forEach((p, i) => draw(tl, p, 5.6 + i * 0.6, 0.45));
  tl.fromTo($(root, ".badge"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.6, ease: POP }, 7.1);
  idle(tl, $(root, ".phone-float"), 5.4, T.cta, 18);
  exitLayer(tl, valor, T.cta - 0.28);

  cta(tl, root);
  return tl;
}

// ─────────────────────────── AD 2 · Consecuencia ───────────────────────────
// Esquirlas: cada tarjeta se duplica en 8 triángulos con clip-path que parten de un punto de impacto.
function buildShards(card, k) {
  const W = 280, H = 360;
  const cx = 130 + k * 12, cy = 160 + (k % 2) * 30;
  const P = [[0, 0], [150, 0], [W, 0], [W, 190], [W, H], [130, H], [0, H], [0, 170]];
  const face = $(card, ".face");
  const shards = P.map((p, i) => {
    const q = P[(i + 1) % P.length];
    const d = document.createElement("div");
    d.className = "shard";
    d.innerHTML = face.innerHTML;
    d.style.clipPath = `polygon(${cx}px ${cy}px, ${p[0]}px ${p[1]}px, ${q[0]}px ${q[1]}px)`;
    const mx = (cx + p[0] + q[0]) / 3 - cx, my = (cy + p[1] + q[1]) / 3 - cy;
    const len = Math.hypot(mx, my) || 1;
    d._fly = { x: (mx / len) * (380 + ((i * 53) % 140)), y: (my / len) * (380 + ((i * 37) % 120)) + 180, rotation: (i % 2 ? 1 : -1) * (50 + ((i * 29) % 110)) };
    card.appendChild(d);
    return d;
  });
  gsap.set(shards, { opacity: 0 });
  // grieta
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("class", "crack");
  svg.innerHTML = `<path pathLength="1" class="draw" d="M${cx} ${cy} l-38 -34 l-14 -62 l-40 -40" />
    <path pathLength="1" class="draw" d="M${cx} ${cy} l46 -20 l30 -70 l52 -30" />
    <path pathLength="1" class="draw" d="M${cx} ${cy} l10 60 l-30 58 l12 70" />`;
  card.appendChild(svg);
  return { shards, cracks: $$(svg, "path"), svg, face };
}

function ad2(root) {
  const tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), valor = $(root, ".valor");
  const cards = $$(root, ".icon-card");
  const broken = cards.map(buildShards);

  tl.fromTo(bgState, { heat: 0.2, calm: 0, pulse: 0, gold: 0, warp: 0.2, zoom: 1.1 }, { heat: 0.7, warp: 0.6, zoom: 1, duration: 2, ease: IN }, 0);
  common(tl, root);

  // HOOK 0–2 — una tarjeta por palabra de la voz
  cards.forEach((c, i) => {
    tl.fromTo(c, { opacity: 0, y: 260, rotation: (i - 1) * 10, scale: 0.8 }, { opacity: 1, y: 0, rotation: (i - 1) * 3, scale: 1, duration: 0.8, ease: POP }, 0.05 + i * 0.4);
  });

  // VALOR 2–8 — el problema (tono grave hasta 8 s)
  enterWords(tl, $$(root, ".l1 .w"), T.valor, { s: 0.08 });
  enterWords(tl, $$(root, ".l2 .w"), 3.65, { s: 0.08 });
  flash(tl, 3.65, 0.3);
  tl.to(bgState, { heat: 1, duration: 1.0, ease: IN }, 3.65);
  cards.forEach((c, i) => shake(tl, c, 3.75 + i * 0.08, 0.5));
  broken.forEach((b, i) => draw(tl, b.cracks, 3.95 + i * 0.15, 0.35, 0.08));
  enterWords(tl, $$(root, ".l3 .w"), 5.0, { y: 50, s: 0.1 });

  // 6.0 — QUIEBRE, justo después de «¿Cuándo?»
  const Q = 6.0;
  [".l1", ".l2", ".l3"].forEach((s) => exitLayer(tl, $(root, s), Q - 0.05, 0.3));
  broken.forEach((b) => {
    tl.set([b.face, b.svg], { opacity: 0 }, Q);
    tl.set(b.shards, { opacity: 1 }, Q);
    b.shards.forEach((s) => {
      tl.fromTo(s, { x: 0, y: 0, rotation: 0 }, { ...s._fly, duration: 1.0, ease: IN, immediateRender: false }, Q);
      tl.to(s, { opacity: 0, duration: 0.5, ease: "power2.in" }, Q + 0.45);
    });
  });
  flash(tl, Q, 0.8);
  tl.to(bgState, { warp: 1.3, duration: 0.5, ease: IN }, Q);
  tl.to(bgState, { warp: 0.3, duration: 1.8, ease: "power2.out" }, Q + 0.5);
  tl.set(hook, { autoAlpha: 0 }, 7.1);

  // 6.4 — el alivio visual: interfaz móvil Glassmorphism
  tl.to(bgState, { heat: 0, duration: 1.6, ease: "power2.inOut" }, 6.4);
  tl.to(bgState, { calm: 1, duration: 1.3, ease: "power2.inOut" }, 6.6);
  enterWords(tl, $$(root, ".l4 .w"), 6.4, { s: 0.07 });
  const phone = $(root, ".phone");
  tl.fromTo(phone, { opacity: 0, y: 620, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: POP }, 6.45);
  sheen(tl, phone, 7.1);
  tl.fromTo($$(root, ".chip"), { opacity: 0, x: -90 }, { opacity: 1, x: 0, duration: 0.55, ease: IN, stagger: 0.16 }, 6.85);
  tl.fromTo($$(root, ".chip i"), { scale: 0 }, { scale: 1, duration: 0.45, ease: POP, stagger: 0.16 }, 7.0);
  idle(tl, $(root, ".phone-float"), 7.2, T.cta, 12, 0.8);
  exitLayer(tl, valor, T.cta - 0.28);

  cta(tl, root);
  return tl;
}

// ─────────────────────────── AD 3 · Urgencia ───────────────────────────
function ad3(root) {
  const tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), valor = $(root, ".valor");

  tl.fromTo(bgState, { heat: 0.3, calm: 0, pulse: 0, gold: 0, warp: 0.1, zoom: 1.1 }, { heat: 0.5, zoom: 1, duration: 2, ease: IN }, 0);
  common(tl, root);

  // HOOK 0–2
  enterWords(tl, $$(hook, ".hook-title .w"), T.hook + 0.1, { y: 90, s: 0.18 });
  tl.fromTo($(hook, ".mega2"), { scale: 1.5 }, { scale: 1, duration: 0.8, ease: POP }, T.hook + 0.46);
  tl.fromTo($(root, ".hv"), { opacity: 0, y: 320 }, { opacity: 1, y: 0, duration: 0.85, ease: POP }, 0.5);
  tl.fromTo($$(root, ".hv-row"), { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.55, ease: IN, stagger: 0.12 }, 0.8);
  tl.fromTo($$(root, ".hv-row em"), { scale: 0.7 }, { scale: 1.12, duration: 0.25, ease: "sine.inOut", repeat: 3, yoyo: true, stagger: 0.1 }, 1.0);
  idle(tl, $(root, ".hv-float"), 0.9, T.valor, 12, 1.0);
  exitLayer(tl, hook, T.valor - 0.22, 0.24);

  // VALOR 2–8
  enterWords(tl, $$(root, ".m1 .w"), T.valor, { s: 0.07 });
  enterWords(tl, $$(root, ".m2 .w"), 3.0, { y: 120, s: 0.12, ease: POP });
  tl.fromTo($(root, ".gold-line"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: IN }, 3.4);
  tl.fromTo($(root, ".tag"), { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: POP }, 3.7);

  // 4.7 — la pausa: el texto se va y el fondo se tensa en silencio
  [".m1", ".m2", ".tag"].forEach((s) => exitLayer(tl, $(root, s), 4.0, 0.3));
  tl.to(bgState, { heat: 1, warp: 0.8, duration: 1.2, ease: "power2.inOut" }, 4.2);
  enterWords(tl, $$(root, ".m3 .w"), 4.3, { s: 0.12 });

  // 6.05 — EXPUESTA (la voz la dice en 6.08 s)
  const m4 = $(root, ".m4");
  tl.fromTo(m4, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.55, ease: "back.out(2)" }, 6.05);
  shake(tl, $(root, ".shake"), 6.09, 1);
  flash(tl, 6.05, 1);

  // 6.5 — el escudo se ensambla pieza por pieza
  tl.to([$(root, ".m3"), m4], { y: -300, scale: 0.55, duration: 0.55, ease: IN }, 6.5);
  tl.to(bgState, { heat: 0, duration: 0.9, ease: "power2.inOut" }, 6.6);
  tl.to(bgState, { calm: 1, warp: 0.2, duration: 1.1, ease: "power2.inOut" }, 6.7);
  const off = [[-260, -200, -70], [260, -200, 70], [-320, 20, -50], [320, 20, 50], [-220, 260, -80], [220, 260, 80]];
  $$(root, ".pc").forEach((p, i) => {
    const [x, y, r] = off[i];
    tl.fromTo(p, { opacity: 0, x, y, rotation: r, scale: 0.6, transformOrigin: "50% 50%" },
      { opacity: 1, x: 0, y: 0, rotation: 0, scale: 1, duration: 0.5, ease: POP }, 6.6 + i * 0.09);
  });
  draw(tl, $(root, ".outline"), 7.2, 0.45);
  draw(tl, $(root, ".check"), 7.38, 0.3);
  tl.to(bgState, { pulse: 0.3, duration: 0.07, ease: IN }, 7.4);
  tl.to(bgState, { pulse: 0, duration: 0.45, ease: "power2.out" }, 7.47);
  tl.fromTo($(root, ".shield-cap"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: IN }, 7.45);
  exitLayer(tl, valor, T.cta - 0.2, 0.2);

  cta(tl, root);
  return tl;
}

export function buildAds(stage) {
  // Los espacios entre palabras animadas se retiran del DOM y pasan a CSS (.w + .w):
  // así ningún reflujo ni script externo puede pegarlas o correrlas.
  stage.querySelectorAll(".w").forEach((w) => {
    const n = w.nextSibling;
    if (n && n.nodeType === 3 && !n.textContent.trim()) n.remove();
    const p = w.previousSibling;
    if (p && p.nodeType === 3 && !p.textContent.trim()) p.remove();
  });
  const tls = {
    ad1: ad1($(stage, "#ad1")),
    ad2: ad2($(stage, "#ad2")),
    ad3: ad3($(stage, "#ad3")),
  };
  // Registro al estilo HyperFrames: cada composición expone su timeline en pausa.
  window.__timelines = Object.assign(window.__timelines || {}, {
    "ad1-autodiagnostico": tls.ad1, "ad2-consecuencia": tls.ad2, "ad3-urgencia": tls.ad3,
  });
  return tls;
}
