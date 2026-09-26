// «En Vivo: PESV · Autogestión» — promocional de 15 s.
// Un timeline de GSAP en pausa, registrado en window.__timelines (seek-safe para HyperFrames).
import { bgState } from "./bg.js";

/* global gsap */

// ─────────── anclas de la locución ───────────
// Los cuatro bloques del brief. Las sub-anclas son el segundo exacto en que Carlos dice cada
// palabra clave (medido con marcas de tiempo por carácter, tools/audio.py). Regrabar la voz =
// cambiar estos números; la animación y la cámara 3D se recolocan solas.
// Medidos el 2026-09-24 sobre la voz de Carlos (multilingual_v2, stability 0.35, clarity 0.8).
export const elevenLabsTimestamps = {
  hook: 1.0, falta: 3.40, informe: 3.82,
  dolor: 4.5, flota: 5.30, conductores: 5.69, mano: 6.62,
  presentacionYezid: 7.0, yezid: 7.62, generarlo: 9.28, clic: 10.95,
  fechaEvento: 11.5, vivo: 12.79, gratis: 13.43,
};
const T = elevenLabsTimestamps;
export const videoTimelines = { hook: T.hook, valor: T.presentacionYezid, cta: T.fechaEvento, end: 15.0 };
export const VERSION = 1;
const END = 15.0;

// Velocidad de la cámara 3D (unidades/s): arranque en ráfaga, aceleración en el dolor y
// máximo en el clímax del 3 de octubre. bg.js integra esta curva: es determinista.
export const VELOCIDAD = [
  [0, 140], [0.9, 16], [T.hook + 0.2, 10], [T.dolor - 0.25, 12], [T.dolor, 52], [T.presentacionYezid - 0.35, 44],
  [T.presentacionYezid, 7], [T.fechaEvento - 0.5, 6], [T.fechaEvento, 110], [T.fechaEvento + 1.1, 16], [END, 12],
];

// Cero fades lineales: físicas extremas.
const EXPLOTA = "back.out(1.7)";
const CORTE = "expo.inOut";
const SALE = "power4.in";
const LLEGA = "power4.out";

export const SCRIPTS = {
  ad1: {
    segs: [
      { id: "hook", t: "1.0 s", vo: "Tu P-E-S-V ya está en marcha… pero falta el informe.", dir: "Pregunta de diagnóstico; «informe» con peso." },
      { id: "hook", t: "4.5 s", vo: "Inspecciones, flota, conductores… ¿a mano?", dir: "Enumeración rápida, un golpe por palabra." },
      { id: "valor", t: "7.0 s", vo: "El doctor Yezid Ricaurte te enseña a generarlo… con un solo clic.", dir: "Autoridad y alivio." },
      { id: "cta", t: "11.5 s", vo: "Tres de octubre, ¡en vivo y gratis! Reserva tu cupo.", dir: "Clímax: «Tres de octubre» cae con el golpe." },
    ],
    board: [],
  },
};

// ─────────── utilidades ───────────
const $ = (r, s) => r.querySelector(s);
const $$ = (r, s) => [...r.querySelectorAll(s)];
const azar = (i, k = 1) => { const x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };

function partirLetras(root) {
  $$(root, "[data-letras]").forEach((el) => {
    const txt = el.textContent;
    el.textContent = "";
    for (const c of txt) {
      const s = document.createElement("span");
      s.className = c === " " ? "sp" : "ch";
      if (c !== " ") s.textContent = c;
      el.appendChild(s);
    }
  });
}
// Entrada letra por letra, explosiva y en cascada: cada letra llega desde escala, giro y desenfoque
// distintos (deterministas por índice), con back.out(1.7).
function letras(tl, els, at, { escala = 2.6, y = -120, giro = 40, s = 0.035, d = 0.8, ease = EXPLOTA } = {}) {
  els.forEach((el, i) => {
    tl.fromTo(el, { opacity: 0, scale: escala, y: y * (0.6 + azar(i) * 0.8), rotation: (azar(i, 2) - 0.5) * giro * 2, filter: "blur(14px)" },
      { opacity: 1, scale: 1, y: 0, rotation: 0, filter: "blur(0px)", duration: d, ease }, at + i * s);
  });
}
function sacude(tl, el, at, k = 1) {
  tl.to(el, { keyframes: [
    { x: -26 * k, y: 12 * k, rotation: -0.6 * k, duration: 0.04 }, { x: 22 * k, y: -10 * k, rotation: 0.5 * k, duration: 0.04 },
    { x: -12 * k, y: 6 * k, rotation: -0.2 * k, duration: 0.05 }, { x: 6 * k, y: -3 * k, rotation: 0, duration: 0.06 }, { x: 0, y: 0, duration: 0.08 } ] }, at);
}
// Destellos con tope 0.5: más alto lava la imagen y es agresivo para fotosensibilidad.
function flash(tl, root, at, pico = 0.3) {
  const f = $(root, ".flash");
  tl.to(f, { opacity: pico, duration: 0.02, ease: "none" }, at);
  tl.to(f, { opacity: 0, duration: 0.35, ease: "power2.out" }, at + 0.02);
}
function golpeCamara(tl, at, fov = 12, roll = 0.04) {
  tl.to(bgState, { fov, roll, brillo: 1, duration: 0.12, ease: LLEGA }, at);
  tl.to(bgState, { fov: 0, roll: 0, brillo: 0, duration: 0.9, ease: "power3.out" }, at + 0.12);
}
// Ambient idle: flotación en Y + escalado ultra-lento 1.02 → 1.05 (repeticiones contadas: seek-safe)
function flota(tl, el, desde, hasta, amp = 14, periodo = 2.4) {
  const media = periodo / 2, n = Math.max(1, Math.floor((hasta - desde) / media));
  tl.fromTo(el, { y: 0 }, { y: -amp, duration: media, ease: "sine.inOut", repeat: n - 1, yoyo: true, immediateRender: false }, desde);
  tl.fromTo(el, { scale: 1.02 }, { scale: 1.05, duration: hasta - desde, ease: "none", immediateRender: false }, desde);
}
function sale(tl, el, at, d = 0.3, extra = {}) {
  tl.to(el, { opacity: 0, scale: 1.18, y: -80, filter: "blur(12px)", duration: d, ease: SALE, ...extra }, at);
}

// ─────────── el video ───────────
function video(root, stage) {
  const tl = gsap.timeline({ paused: true });
  const shake = $(root, ".shake");
  tl.fromTo(bgState, { fov: 0, roll: 0, brillo: 0 }, { fov: 0, duration: 0.01 }, 0);

  // cromo + progreso
  tl.fromTo($(root, ".rotulo"), { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.8, ease: LLEGA }, 0.6);
  tl.fromTo($(root, ".filete"), { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: CORTE }, 0.7);
  tl.fromTo($(root, ".rotulo .punto"), { scale: 1 }, { scale: 1.4, duration: 0.6, ease: "sine.inOut", repeat: 22, yoyo: true }, 1.0);
  tl.fromTo($(stage, ".progress i"), { scaleX: 0 }, { scaleX: 1, duration: END, ease: "none" }, 0);
  gsap.set([$(stage, ".grano")], { x: 0, y: 0 }); gsap.set($(root, ".flash"), { opacity: 0 });
  tl.to($(stage, ".grano"), { keyframes: Array.from({ length: 30 }, (_, i) => ({ x: (azar(i) - 0.5) * 60, y: (azar(i, 3) - 0.5) * 60, duration: 0.5, ease: "steps(1)" })) }, 0);

  // ── 0.0 APERTURA: ráfaga de túnel + «EN VIVO» con separación cromática ──
  const rgb = $$(root, ".rgb span");
  tl.fromTo(rgb, { scale: 2.4, filter: "blur(18px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.55, ease: "expo.out", stagger: 0.03 }, 0.05);
  tl.fromTo(rgb[0], { x: -60 }, { x: -9, duration: 0.6, ease: "expo.out" }, 0.05);
  tl.fromTo(rgb[1], { x: 60 }, { x: 9, duration: 0.6, ease: "expo.out" }, 0.05);
  flash(tl, root, 0.05, 0.45);
  golpeCamara(tl, 0.05, 16, 0.06);
  sale(tl, $(root, ".apertura"), T.hook - 0.22, 0.24);

  // ── 1.0 HOOK ──
  partirLetras(root);
  letras(tl, $$(root, ".pre .ch"), T.hook, { escala: 1.4, y: 60, giro: 8, s: 0.018, d: 0.6 });
  letras(tl, $$(root, ".falta .l1 .ch"), T.falta - 0.08, { escala: 3, y: -160, giro: 35, s: 0.04 });
  letras(tl, $$(root, ".falta .l2 .ch"), T.informe - 0.1, { escala: 0.2, y: 220, giro: 25, s: 0.045, d: 0.9, ease: "expo.out" });
  flash(tl, root, T.informe, 0.25);
  golpeCamara(tl, T.informe, 9, -0.03);
  sacude(tl, shake, T.informe + 0.05, 0.6);
  tl.fromTo($(root, ".sello"), { opacity: 0, scale: 0.5, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: EXPLOTA }, T.informe + 0.12);
  tl.fromTo($(root, ".pre"), { scale: 1 }, { scale: 1.06, duration: T.falta - T.hook, ease: "none", immediateRender: false }, T.hook + 0.6);
  sale(tl, $(root, ".hook"), T.dolor - 0.25, 0.25);

  // ── 4.5 DOLOR: montaje rápido, un corte por palabra ──
  const cortes = $$(root, ".corte"), items = $$(root, ".item");
  const golpes = [T.dolor, T.flota, T.conductores, T.conductores + 0.3];   // «Mantenimiento» no se dice: entra en el siguiente pulso
  tl.fromTo($(root, ".duo"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: LLEGA }, T.dolor - 0.1);
  golpes.forEach((g, i) => {
    const dir = ["inset(0% 0% 100% 0%)", "inset(0% 100% 0% 0%)", "inset(100% 0% 0% 0%)", "inset(0% 0% 0% 100%)"][i];
    tl.fromTo(cortes[i], { clipPath: dir }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.32, ease: CORTE }, g - 0.12);
    tl.fromTo(cortes[i].querySelector("img"), { scale: 1.3 }, { scale: 1.05, duration: 1.1, ease: LLEGA }, g - 0.12);
    tl.fromTo(items[i], { opacity: 0, scale: 1.8, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: EXPLOTA }, g);
    tl.fromTo(items[i].querySelector("img"), { rotation: -25 }, { rotation: 0, duration: 0.5, ease: EXPLOTA }, g);
    flash(tl, root, g, 0.14);
    sacude(tl, shake, g + 0.02, 0.35);
  });
  // los cuatro insumos quedan en rejilla y salen juntos cuando llega la pregunta
  tl.to($(root, ".items"), { opacity: 0, scale: 0.8, filter: "blur(10px)", duration: 0.18, ease: SALE }, T.mano - 0.45);
  letras(tl, $$(root, ".mano .ch"), T.mano - 0.38, { escala: 2.2, y: -100, giro: 30, s: 0.025, d: 0.55 });
  tl.fromTo($(root, ".tacha"), { scaleX: 0 }, { scaleX: 1, duration: 0.22, ease: CORTE }, T.mano);
  sacude(tl, shake, T.mano + 0.1, 0.5);
  tl.fromTo($(root, ".dolor"), { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 100% 0%)", duration: 0.35, ease: CORTE, immediateRender: false }, T.presentacionYezid - 0.2);

  // ── 7.0 PRESENTACIÓN: foto con máscara de cristal ──
  const marco = $(root, ".marco"), foto = $(root, ".foto");
  tl.fromTo(marco, { clipPath: "inset(100% 0% 0% 0% round 70px)" }, { clipPath: "inset(0% 0% 0% 0% round 70px)", duration: 0.85, ease: CORTE }, T.presentacionYezid - 0.1);
  tl.fromTo(foto, { scale: 1.35, y: 140 }, { scale: 1, y: 0, duration: 1.3, ease: "expo.out" }, T.presentacionYezid);
  tl.fromTo($(root, ".luz"), { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 1.2, ease: LLEGA }, T.presentacionYezid + 0.2);
  golpeCamara(tl, T.presentacionYezid, 6, 0.02);
  flota(tl, $(root, ".marco-float"), T.presentacionYezid + 0.9, T.fechaEvento - 0.3, 16, 2.6);
  tl.fromTo(foto, { scale: 1 }, { scale: 1.04, duration: T.fechaEvento - T.presentacionYezid - 1.3, ease: "none", immediateRender: false }, T.presentacionYezid + 1.3);
  letras(tl, $$(root, ".dr .ch"), T.presentacionYezid + 0.35, { escala: 1.8, y: 80, giro: 15, s: 0.03, d: 0.7 });
  tl.fromTo($(root, ".trayectoria"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: LLEGA }, T.presentacionYezid + 0.95);
  tl.fromTo($(root, ".firma"), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.1, ease: "power2.inOut" }, T.presentacionYezid + 1.2);
  const app = $(root, ".app");
  tl.fromTo(app, { opacity: 0, x: 420, rotationY: -45, scale: 0.8 }, { opacity: 1, x: 0, rotationY: 0, scale: 1, duration: 0.8, ease: EXPLOTA }, T.generarlo - 0.1);
  tl.fromTo($(root, ".app-tag b"), { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: EXPLOTA }, T.clic);
  flash(tl, root, T.clic, 0.18);
  flota(tl, $(root, ".app-float"), T.generarlo + 0.7, T.fechaEvento - 0.3, 12, 1.8);
  sale(tl, $(root, ".presenta"), T.fechaEvento - 0.26, 0.26);

  // ── 11.5 SPECTACLE BEAT: «3 DE OCTUBRE · EN VIVO» ──
  const F = T.fechaEvento, num = $(root, ".f-num");
  tl.fromTo(num, { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 1.0, ease: "back.out(3.2)" }, F);
  tl.fromTo(num, { filter: "drop-shadow(0px 0px 0px rgba(241,236,176,0))" },
    { filter: "drop-shadow(0px 0px 110px rgba(241,236,176,1))", duration: 0.16, ease: LLEGA }, F);
  tl.to(num, { filter: "drop-shadow(0px 0px 38px rgba(241,236,176,0.7))", duration: 0.8, ease: "power2.out" }, F + 0.18);
  tl.to(num, { filter: "drop-shadow(0px 0px 80px rgba(241,236,176,0.95))", duration: 0.6, ease: "sine.inOut", repeat: 3, yoyo: true }, F + 1.0);
  letras(tl, $$(root, ".f-de"), F + 0.12, { escala: 2, y: 60, giro: 0, s: 0, d: 0.7 });
  flash(tl, root, F, 0.5);
  sacude(tl, shake, F + 0.03, 1.3);
  golpeCamara(tl, F, 18, 0.07);
  tl.fromTo($(root, ".f-vivo"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.7, ease: EXPLOTA }, T.vivo - 0.2);
  letras(tl, $$(root, ".f-vivo .ch"), T.vivo - 0.15, { escala: 2, y: -40, giro: 10, s: 0.04, d: 0.5 });
  tl.fromTo($(root, ".f-vivo .punto"), { scale: 1 }, { scale: 1.5, duration: 0.5, ease: "sine.inOut", repeat: 3, yoyo: true }, T.vivo + 0.3);
  tl.fromTo($(root, ".f-hora"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: LLEGA }, F + 0.7);
  const cta = $(root, ".cta");
  tl.fromTo(cta, { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(3)" }, T.gratis - 0.05);
  tl.fromTo(cta, { filter: "drop-shadow(0px 0px 0px rgba(240,110,73,0))" },
    { filter: "drop-shadow(0px 0px 70px rgba(240,110,73,1))", duration: 0.16, ease: LLEGA }, T.gratis - 0.05);
  tl.to(cta, { filter: "drop-shadow(0px 0px 26px rgba(240,110,73,0.6))", duration: 0.7, ease: "power2.out" }, T.gratis + 0.15);
  tl.fromTo(cta, { scale: 1 }, { scale: 1.04, duration: 0.45, ease: "sine.inOut", repeat: 3, yoyo: true, immediateRender: false }, T.gratis + 0.8);
  sacude(tl, shake, T.gratis, 0.4);
  tl.fromTo($(root, ".web"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: LLEGA }, T.gratis + 0.35);
  tl.fromTo($(root, ".firma-cierre"), { opacity: 0, clipPath: "inset(0% 100% 0% 0%)" }, { opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.9, ease: "power2.inOut" }, T.gratis + 0.5);
  flota(tl, $(root, ".f-dia"), F + 1.1, END, 10, 1.8);
  return tl;
}

export function buildAds(stage) {
  const tl = video($(stage, "#ad1"), stage);
  window.__timelines = Object.assign(window.__timelines || {}, { "en-vivo-pesv-15s": tl });
  return { ad1: tl };
}
