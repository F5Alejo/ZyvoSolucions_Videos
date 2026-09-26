// Campaña «En Vivo PESV · Informe de Autogestión» — tres videos de 12 s, uno por correo.
// Un timeline de GSAP en pausa por video, registrado en window.__timelines: nada corre por
// su cuenta, cualquier segundo se puede buscar y sale idéntico (condición de HyperFrames).
import { bgState } from "./bg.js";

/* global gsap */

// ─────────── sincronía con la locución (ElevenLabs) ───────────
// Segundo en que la voz dice cada frase clave. Se midieron sobre la locución real con
// marcas de tiempo por carácter (tools/audio.py → assets/voz/elegidas.json); si se regraba
// la voz, basta con cambiar estos números y todo lo demás se recoloca solo.
// Medidos el 2026-09-24 sobre la voz de Carlos (multilingual_v2, stability 0.35, clarity 0.8).
export const audioTimestampsV1 = { hook: 0.0, dieciocho: 0.49, fecha: 4.5, hora: 6.25, cta: 8.0 };
export const audioTimestampsV2 = { hook: 0.0, hora: 3.05, info: 4.0, grupo: 5.2, cuenta: 6.16, cta: 8.0 };
export const audioTimestampsV3 = { hook: 0.0, hora: 2.41, redes: 3.6, instagram: 3.93, tiktok: 4.51, youtube: 5.33, cuenta: 6.07, cta: 8.0 };
export const videoTimelines = { hook: 0.0, valor: 4.0, cta: 8.0, end: 12.0 };
export const VERSION = 1;
const END = 12.0;

// Cero fades lineales: toda entrada usa una de estas dos físicas.
const IN = "power4.out";
const POP = "back.out(1.5)";
const OUT = "power4.in";   // solo salidas

// ─────────── guiones y storyboard (panel del preview) ───────────
export const SCRIPTS = {
  ad1: {
    segs: [
      { id: "hook", t: "0 – 4.5 s", vo: "Faltan dieciocho días… para En Vivo P-E-S-V: Informe de Autogestión.", dir: "Expectativa, sin prisa. La cifra es la protagonista." },
      { id: "valor", t: "4.5 – 8 s", vo: "Sábado tres de octubre… a las diez de la mañana, hora Colombia.", dir: "Claro y firme: es un dato para agendar." },
      { id: "cta", t: "8 – 12 s", vo: "Crea hoy tu cuenta en app punto riskmann punto com.", dir: "Invitación directa; el botón golpea con «cuenta»." },
    ],
    board: [
      ["0.05", "Rótulo «EN VIVO PESV | Informe de Autogestión» y filete dorado (el encabezado del correo)."],
      ["0.10", "Reloj de arena SVG: marco y vidrio se DIBUJAN (stroke-dashoffset); la arena empieza a caer."],
      ["0.20", "«Faltan / 18 / días» palabra por palabra; el 18 entra 1.5→1 con back.out y destello pálido."],
      ["1.60", "«para En Vivo PESV» en cascada. El reloj flota."],
      ["4.50", "Tarjeta glass de calendario sube: anillas dibujadas, «OCTUBRE 2026», «03», «Sábado», «10:00 a. m. (Hora Colombia)». Flota y respira a escala 1.02."],
      ["8.00", "«Nos vemos en vivo.» + SPECTACLE: botón coral «Crea tu cuenta» 1.6→1 (back.out(4)) con resplandor dinámico."],
      ["8.50", "app.riskmann.com/registrarse · «y entra al grupo oficial de WhatsApp» · firma · yezidricaurte.com."],
    ],
  },
  ad2: {
    segs: [
      { id: "hook", t: "0 – 4 s", vo: "¡Mañana es En Vivo P-E-S-V!… a las diez de la mañana, hora Colombia.", dir: "Urgencia: más energía que el video 1." },
      { id: "valor", t: "4 – 8 s", vo: "Los enlaces van por el grupo oficial de WhatsApp. Ten lista tu cuenta en RiskMann.", dir: "Instrucción práctica, ritmo ágil." },
      { id: "cta", t: "8 – 12 s", vo: "Entra ya al grupo de WhatsApp.", dir: "Imperativo corto, cae con el botón." },
    ],
    board: [
      ["0.10", "«Mañana» golpea 1.5→1 (back.out); «es En Vivo PESV» en cascada. El líquido acelera (energía ↑)."],
      ["1.50", "Chip «10:00 a. m. · Hora Colombia»: el reloj se dibuja."],
      ["4.00", "Tarjeta glass con los dos pasos del correo; los iconos se trazan cuando la voz los nombra."],
      ["8.00", "«¡Te esperamos!» + SPECTACLE: botón coral «Entrar al grupo de WhatsApp» (el mismo texto del correo)."],
      ["8.50", "«Mañana · 10:00 a. m. (Hora Colombia)» · firma · yezidricaurte.com."],
    ],
  },
  ad3: {
    segs: [
      { id: "hook", t: "0 – 3.6 s", vo: "¡Hoy es En Vivo P-E-S-V!… a las diez de la mañana.", dir: "Imperativo y rápido." },
      { id: "valor", t: "3.6 – 8 s", vo: "Transmitimos por Instagram, TikTok y YouTube. Ten abierta tu cuenta en RiskMann.", dir: "Enumeración con pulso: una red por golpe." },
      { id: "cta", t: "8 – 12 s", vo: "Ve ya al grupo de WhatsApp.", dir: "Cierre seco, cae con el botón." },
    ],
    board: [
      ["0.05", "Indicador EN VIVO: aro dibujado, núcleo pálido y dos ondas que laten los 12 s (sin rojo, por regla del cliente)."],
      ["0.20", "«Hoy es / En Vivo / PESV» palabra por palabra; «10:00 a. m. · Hora Colombia»."],
      ["3.60", "«La transmisión va por» + tres tarjetas glass: Instagram, TikTok, YouTube (iconos trazados, en cascada)."],
      ["6.20", "Tarjeta «Ten abierta tu cuenta en app.riskmann.com»."],
      ["8.00", "«Los enlaces, en el grupo oficial» + SPECTACLE: botón coral «Ir al grupo de WhatsApp»."],
    ],
  },
};

// ─────────── utilidades ───────────
const $ = (r, s) => r.querySelector(s);
const $$ = (r, s) => [...r.querySelectorAll(s)];

function palabras(tl, els, at, { y = 80, d = 0.75, s = 0.09, ease = IN } = {}) {
  tl.fromTo(els, { opacity: 0, y }, { opacity: 1, y: 0, duration: d, ease, stagger: s }, at);
  tl.fromTo(els, { filter: "blur(10px)" }, { filter: "blur(0px)", duration: 0.35, ease: "power2.out", stagger: s, immediateRender: false }, at);
}
function sale(tl, el, at, d = 0.28) {
  tl.to(el, { opacity: 0, y: -110, scale: 0.96, duration: d, ease: OUT }, at);
}
function traza(tl, els, at, d = 0.6, s = 0) {
  tl.fromTo(els, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: IN, stagger: s }, at);
}
// Ambient idle: flotación en Y y respiración a escala 1.02, con repeticiones contadas (seek-safe)
function flota(tl, el, desde, hasta, amp = 16, periodo = 2.2) {
  const media = periodo / 2, n = Math.max(1, Math.floor((hasta - desde) / media));
  tl.fromTo(el, { y: 0, scale: 1 }, { y: -amp, scale: 1.02, duration: media, ease: "sine.inOut", repeat: n - 1, yoyo: true, immediateRender: false }, desde);
}
function destello(tl, at, pico = 1) {
  tl.to(bgState, { pulso: pico, duration: 0.07, ease: IN }, at);
  tl.to(bgState, { pulso: 0, duration: 0.8, ease: "power2.out" }, at + 0.07);
}
function sacude(tl, el, at, k = 1) {
  tl.to(el, { keyframes: [
    { x: -20 * k, y: 9 * k, duration: 0.045 }, { x: 16 * k, y: -7 * k, duration: 0.045 },
    { x: -9 * k, y: 4 * k, duration: 0.05 }, { x: 5 * k, y: -2 * k, duration: 0.06 }, { x: 0, y: 0, duration: 0.08 } ] }, at);
}
function comun(tl, stage) {
  tl.fromTo($(stage, ".rotulo"), { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.8, ease: IN }, 0.05);
  tl.fromTo($(stage, ".filete"), { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: IN }, 0.2);
  tl.fromTo($(stage, ".rotulo .punto"), { scale: 1 }, { scale: 1.35, duration: 0.62, ease: "sine.inOut", repeat: 18, yoyo: true }, 0.4);
  tl.fromTo($(stage, ".progress i"), { scaleX: 0 }, { scaleX: 1, duration: END, ease: "none" }, 0);
}

// ─────────── CTA: el botón coral del correo, con spectacle beat ───────────
const ICONO_CHAT = '<svg viewBox="0 0 64 64"><path class="draw" pathLength="1" d="M32 8c14 0 24 10 24 22s-10 22-24 22c-4 0-7-.6-10-1.8L10 54l3.6-10.4C10 39.8 8 35 8 30 8 18 18 8 32 8z"/></svg>';
function montaCTA(root, sube) {
  const L = $(root, ".layer.cta");
  const chat = /WhatsApp/.test(L.dataset.boton) ? ICONO_CHAT : "";
  L.innerHTML = `
    <div class="cta-sube">${sube.split(" ").map((w) => `<span class="w">${w}</span>`).join("")}</div>
    <div class="cta-boton-box"><span class="cta-boton">${chat}${L.dataset.boton}</span></div>
    <div class="cta-url">${L.dataset.url}</div>
    ${L.dataset.extra ? `<div class="cta-extra">${L.dataset.extra}</div>` : ""}
    <!-- ASSET DE MARCA: firma oficial en blanco (versión en negativo del manual). Solo se escala. -->
    <img class="cta-firma" src="assets/firma-yezid-blanca.png" alt="Yezid Ricaurte" />
    <div class="cta-web">yezidricaurte.com</div>`;
  gsap.set(L, { autoAlpha: 0 });
  return L;
}
function cta(tl, root, at, sube) {
  const L = montaCTA(root, sube);
  const btn = $(L, ".cta-boton");
  tl.set(L, { autoAlpha: 1 }, at);
  palabras(tl, $$(L, ".cta-sube .w"), at, { y: 60, s: 0.08 });
  // Spectacle beat: overshoot severo 1.6 → 1.0 y resplandor coral que estalla y respira
  tl.fromTo(btn, { scale: 1.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.95, ease: "back.out(4)" }, at + 0.05);
  tl.fromTo(btn, { filter: "drop-shadow(0px 0px 0px rgba(240,110,73,0))" },
    { filter: "drop-shadow(0px 0px 80px rgba(240,110,73,1))", duration: 0.18, ease: IN }, at + 0.05);
  tl.to(btn, { filter: "drop-shadow(0px 0px 24px rgba(240,110,73,0.55))", duration: 0.7, ease: "power2.out" }, at + 0.25);
  tl.to(btn, { filter: "drop-shadow(0px 0px 56px rgba(241,236,176,0.85))", duration: 0.55, ease: "sine.inOut", repeat: 3, yoyo: true }, at + 1.05);
  tl.fromTo(btn, { scale: 1 }, { scale: 1.04, duration: 0.5, ease: "sine.inOut", repeat: 4, yoyo: true, immediateRender: false }, at + 1.3);
  if ($(btn, "path")) traza(tl, $(btn, "path"), at + 0.3, 0.6);
  sacude(tl, $(root, ".shake"), at + 0.09, 1.1);
  tl.to(bgState, { coral: 1, duration: 0.05, ease: IN }, at - 0.06);
  destello(tl, at + 0.05, 1);
  tl.to(bgState, { zoom: 0.84, warp: 0.7, duration: 1.4, ease: IN }, at);
  tl.fromTo($(L, ".cta-url"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, at + 0.5);
  if ($(L, ".cta-extra")) tl.fromTo($(L, ".cta-extra"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, at + 0.8);
  tl.fromTo($(L, ".cta-firma"), { opacity: 0, scale: 0.75 }, { opacity: 1, scale: 1, duration: 0.8, ease: POP }, at + 1.1);
  tl.fromTo($(L, ".cta-web"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, at + 1.35);
}

// ─────────── VIDEO 1 · Faltan 18 días ───────────
function v1(root, stage) {
  const A = audioTimestampsV1, tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), fecha = $(root, ".fecha");
  tl.fromTo(bgState, { energia: 0.1, pulso: 0, coral: 0, warp: 0.2, zoom: 1.12 }, { zoom: 1, duration: 2, ease: IN }, 0);
  comun(tl, stage);

  // reloj de arena: se dibuja y la arena cae mientras se habla de los días que faltan
  traza(tl, $(root, ".marco"), A.hook + 0.1, 0.8);
  traza(tl, $(root, ".vidrio"), A.hook + 0.15, 1.1);
  tl.fromTo($(root, ".arena-arriba"), { scaleY: 1 }, { scaleY: 0.25, svgOrigin: "100 150", duration: 3.2, ease: "none" }, A.hook + 0.8);
  tl.fromTo($(root, ".arena-abajo"), { scaleY: 0.1 }, { scaleY: 1, svgOrigin: "100 280", duration: 3.2, ease: "none" }, A.hook + 0.8);
  tl.fromTo($(root, ".chorro"), { opacity: 0 }, { opacity: 0.9, duration: 0.2, ease: IN }, A.hook + 0.8);
  flota(tl, $(root, ".reloj-arena"), A.hook + 1.2, A.fecha - 0.3, 12, 2.0);

  palabras(tl, $$(root, ".titulo .w"), A.hook + 0.2, { y: 100, s: 0.22 });
  tl.fromTo($(root, ".cifra"), { scale: 1.5 }, { scale: 1, duration: 0.9, ease: POP }, A.dieciocho - 0.04);
  destello(tl, A.dieciocho, 0.6);
  palabras(tl, $$(root, ".bajada .w"), A.hook + 1.6, { y: 50, s: 0.08 });
  sale(tl, hook, A.fecha - 0.3, 0.3);

  // calendario glass
  tl.to(bgState, { energia: 0.35, warp: 0.4, duration: 1.2, ease: "power2.inOut" }, A.fecha);
  tl.fromTo($(root, ".cal"), { opacity: 0, y: 700, rotation: 5 }, { opacity: 1, y: 0, rotation: 0, duration: 1.0, ease: POP }, A.fecha);
  traza(tl, $(root, ".anillas path"), A.fecha + 0.2, 0.6);
  tl.fromTo($(root, ".cal-mes"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.6, ease: POP }, A.fecha + 0.3);
  tl.fromTo($(root, ".cal-dia"), { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.8, ease: POP }, A.fecha + 0.4);
  destello(tl, A.fecha + 0.45, 0.45);
  tl.fromTo($(root, ".cal-sem"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: IN }, A.fecha + 0.7);
  tl.fromTo($(root, ".cal-linea"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: IN }, A.hora - 0.3);
  tl.fromTo($(root, ".cal-hora"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, A.hora - 0.08);
  flota(tl, $(root, ".cal-float"), A.fecha + 1.2, A.cta - 0.3, 14, 1.6);
  sale(tl, fecha, A.cta - 0.28);

  cta(tl, root, A.cta, "Nos vemos en vivo.");
  return tl;
}

// ─────────── VIDEO 2 · Mañana ───────────
function v2(root, stage) {
  const A = audioTimestampsV2, tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), info = $(root, ".info");
  tl.fromTo(bgState, { energia: 0.45, pulso: 0, coral: 0, warp: 0.4, zoom: 1.12 }, { energia: 0.6, zoom: 1, duration: 2, ease: IN }, 0);
  comun(tl, stage);

  palabras(tl, $$(root, ".t2 .w"), A.hook + 0.1, { y: 100, s: 0.12 });
  tl.fromTo($(root, ".t2 .cifra-txt"), { scale: 1.5 }, { scale: 1, duration: 0.85, ease: POP }, A.hook + 0.1);
  destello(tl, A.hook + 0.15, 0.6);
  tl.fromTo($(root, ".chip-hora"), { opacity: 0, y: 50, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: POP }, A.hora - 0.12);
  traza(tl, $$(root, ".chip-hora circle, .chip-hora path"), A.hora, 0.6, 0.12);
  flota(tl, $(root, ".chip-hora"), A.hora + 0.6, A.info - 0.3, 6, 0.8);
  sale(tl, hook, A.info - 0.28);

  tl.to(bgState, { energia: 0.8, warp: 0.6, duration: 1.2, ease: "power2.inOut" }, A.info);
  tl.fromTo($(root, ".pasos"), { opacity: 0, y: 650, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.95, ease: POP }, A.info);
  const pasos = $$(root, ".paso");
  tl.fromTo(pasos[0], { opacity: 0, x: -90 }, { opacity: 1, x: 0, duration: 0.6, ease: IN }, A.info + 0.3);
  traza(tl, pasos[0].querySelectorAll(".draw"), A.grupo, 0.7);                 // «…grupo de WhatsApp»
  tl.fromTo(pasos[1], { opacity: 0, x: -90 }, { opacity: 1, x: 0, duration: 0.6, ease: IN }, A.cuenta - 0.15);
  traza(tl, pasos[1].querySelectorAll(".draw"), A.cuenta, 0.6, 0.2);           // «Ten lista tu cuenta»
  flota(tl, $(root, ".pasos-float"), A.info + 1.0, A.cta - 0.3, 14, 1.5);
  sale(tl, info, A.cta - 0.28);

  cta(tl, root, A.cta, "¡Te esperamos!");
  return tl;
}

// ─────────── VIDEO 3 · Hoy ───────────
function v3(root, stage) {
  const A = audioTimestampsV3, tl = gsap.timeline({ paused: true });
  const hook = $(root, ".hook"), redes = $(root, ".redes");
  tl.fromTo(bgState, { energia: 0.7, pulso: 0, coral: 0, warp: 0.5, zoom: 1.12 }, { energia: 0.85, zoom: 1, duration: 2, ease: IN }, 0);
  comun(tl, stage);

  // indicador EN VIVO: vive los 12 s
  const live = $(root, ".live");
  tl.fromTo(live, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.7, ease: POP }, 0.05);
  traza(tl, $(root, ".live .aro"), 0.1, 0.8);
  tl.fromTo($(root, ".live .nucleo"), { scale: 0 }, { scale: 1, svgOrigin: "60 60", duration: 0.6, ease: POP }, 0.15);
  $$(root, ".live .onda").forEach((o, i) => {
    tl.fromTo(o, { scale: 1, opacity: 0.85 }, { scale: 2.7, opacity: 0, svgOrigin: "60 60", duration: 1.2, ease: "power2.out", repeat: 8, delay: 0 }, 0.3 + i * 0.6);
  });
  tl.fromTo($(root, ".live .nucleo"), { scale: 1 }, { scale: 0.8, svgOrigin: "60 60", duration: 0.6, ease: "sine.inOut", repeat: 17, yoyo: true, immediateRender: false }, 0.8);

  palabras(tl, $$(root, ".t3 .w"), A.hook + 0.2, { y: 100, s: 0.14 });
  destello(tl, A.hook + 0.5, 0.5);
  palabras(tl, $$(root, ".b3 .w"), A.hora - 0.1, { y: 40, s: 0.06 });
  sale(tl, hook, A.redes - 0.25, 0.25);

  palabras(tl, $$(root, ".redes-tit .w"), A.redes, { y: 50, s: 0.07 });
  const chips = $$(root, ".red");
  [A.instagram, A.tiktok, A.youtube].forEach((t, i) => {     // cada red entra cuando la voz la nombra
    tl.fromTo(chips[i], { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.7, ease: POP }, t - 0.05);
    traza(tl, chips[i].querySelectorAll(".draw"), t + 0.1, 0.6, 0.1);
  });
  flota(tl, $(root, ".redes-float"), A.redes + 1.8, A.cta - 0.3, 12, 1.4);
  tl.fromTo($(root, ".cuenta"), { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.7, ease: POP }, A.cuenta - 0.05);
  sale(tl, redes, A.cta - 0.28);
  tl.to(live, { y: -60, scale: 0.8, duration: 0.5, ease: IN }, A.cta - 0.3);

  cta(tl, root, A.cta, "Los enlaces, en el grupo oficial");
  return tl;
}

export function buildAds(stage) {
  // el espacio entre palabras va por CSS (.w + .w): se retiran los nodos de texto en blanco
  stage.querySelectorAll(".w").forEach((w) => {
    for (const n of [w.nextSibling, w.previousSibling]) if (n && n.nodeType === 3 && !n.textContent.trim()) n.remove();
  });
  const tls = { ad1: v1($(stage, "#ad1"), stage), ad2: v2($(stage, "#ad2"), stage), ad3: v3($(stage, "#ad3"), stage) };
  window.__timelines = Object.assign(window.__timelines || {}, {
    "v1-faltan-18-dias": tls.ad1, "v2-manana": tls.ad2, "v3-hoy": tls.ad3,
  });
  return tls;
}
