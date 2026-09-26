// Arma el DOM desde config.js y construye UN timeline de GSAP en pausa (seek-safe:
// sin setTimeout, sin repeat:-1, sin azar en reproducción).
import { COMUN } from "./config.js";
import { fondoEstado } from "./red.js";

/* global gsap */
const IN = "power4.out";          // entradas
const POP = "back.out(1.5)";      // entradas con rebote
const OUT = "power4.in";          // solo salidas
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

// «Aprende a *dominar* y _acento_» → spans por palabra (y por letra si se pide)
function marcar(el, texto, { letras = false } = {}) {
  el.textContent = "";
  for (const m of texto.matchAll(/\*([^*]+)\*|_([^_]+)_|([^*_]+)/g)) {
    const [trozo, cls] = m[1] ? [m[1], "b"] : m[2] ? [m[2], "acento"] : [m[3], ""];
    for (const palabra of trozo.split(/\s+/).filter(Boolean)) {
      const w = document.createElement("span");
      w.className = "w" + (cls ? " " + cls : "");
      if (letras) for (const c of palabra) { const ch = document.createElement("span"); ch.className = "ch"; ch.textContent = c; w.appendChild(ch); }
      else w.textContent = palabra;
      el.appendChild(w);
    }
  }
}

// flotación en Y (respiración): repeticiones contadas hasta `hasta`
function flotar(tl, el, desde, hasta, amp = 14, periodo = 3.2) {
  const medio = periodo / 2, n = Math.max(1, Math.floor((hasta - desde) / medio));
  tl.fromTo(el, { y: 0 }, { y: -amp, duration: medio, ease: "sine.inOut", repeat: n - 1, yoyo: true }, desde);
}

function destello(tl, t, pico = 1) {
  tl.to(fondoEstado, { pulso: pico, duration: 0.08, ease: IN }, t);
  tl.to(fondoEstado, { pulso: 0, duration: 0.9, ease: "power2.out" }, t + 0.08);
}

export function construir(cfg) {
  const T = cfg.tiempos;

  // ── textos desde la configuración ──
  $$("[data-t]").forEach((el) => (el.textContent = COMUN[el.dataset.t]));
  marcar($("#titular"), cfg.titular, { letras: true });
  marcar($("#bajada"), cfg.bajada);
  $("#fecha-dia").textContent = cfg.fecha.dia;
  $("#fecha-hora").textContent = `${cfg.fecha.hora} · ${cfg.fecha.zona}`;
  $("#pasos").innerHTML = "";
  cfg.pasos.forEach((p) => { const li = document.createElement("li"); const s = document.createElement("span"); marcar(s, p); li.appendChild(s); $("#pasos").appendChild(li); });
  $("#boton").textContent = cfg.boton;
  $("#sub").textContent = cfg.sub;

  const tl = gsap.timeline({ paused: true });

  // ── estado inicial del fondo y barra de progreso ──
  tl.fromTo(fondoEstado, { energia: 0.25, pulso: 0, calma: 0 }, { energia: 0.4, duration: 1.2, ease: IN }, 0);
  tl.fromTo(".progreso i", { scaleX: 0 }, { scaleX: 1, duration: T.fin, ease: "none" }, 0);

  // ── rótulo + latido (pings contados, nunca repeat:-1) ──
  tl.fromTo(".eyebrow", { opacity: 0, y: -30, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: POP }, 0.05);
  for (let t = 0.6; t < T.fin - 0.8; t += 1.2) {
    tl.fromTo(".latido", { scale: 1 }, { scale: 1.45, duration: 0.18, ease: "power2.out", immediateRender: false }, t);
    tl.to(".latido", { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.18);
  }

  // ═════ ESCENA A · la foto en cristal + la urgencia con valor ═════
  tl.fromTo("#foto-card", { opacity: 0, y: 140, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 1.0, ease: POP }, T.foto);
  tl.fromTo("#foto", { scale: 1.16 }, { scale: 1, duration: 1.4, ease: IN }, T.foto);
  tl.fromTo(".brillo", { x: 0 }, { x: 1200, duration: 1.4, ease: "power2.inOut" }, T.foto + 0.6);
  tl.fromTo("#nombre", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.8, ease: IN }, T.foto + 0.7);
  flotar(tl, "#foto-flota", T.foto + 1.0, T.fin, 16, 3.4);            // ambient idle: los 12 s

  // titular letra por letra; el acento pálido entra con rebote
  const letras = $$("#titular .ch");
  tl.fromTo(letras, { opacity: 0, y: 90, rotationX: -70 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.8, ease: IN, stagger: 0.035 }, T.titular);
  tl.fromTo($$("#titular .acento"), { scale: 1.25 }, { scale: 1, duration: 0.9, ease: POP, transformOrigin: "50% 60%" }, T.titular + 0.25);
  destello(tl, T.titular + 0.3, 0.45);
  tl.fromTo($$("#bajada .w"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: IN, stagger: 0.06 }, T.bajada);
  tl.fromTo($$("#bajada .w"), { filter: "blur(8px)" }, { filter: "blur(0px)", duration: 0.35, ease: "power2.out", stagger: 0.06, immediateRender: false }, T.bajada);
  tl.to("#escena-a", { opacity: 0, y: -120, duration: 0.35, ease: OUT }, T.fecha - 0.4);

  // la foto sube y se achica para dar paso a la información
  tl.to("#foto-card", { scale: 0.62, y: -40, duration: 0.8, ease: IN, transformOrigin: "50% 0%" }, T.fecha - 0.3);
  tl.to("#nombre", { y: -330, x: 90, scale: 0.85, duration: 0.8, ease: IN, transformOrigin: "0% 50%" }, T.fecha - 0.3);
  tl.to(fondoEstado, { energia: 0.55, calma: 0.6, duration: 1.2, ease: "power2.inOut" }, T.fecha - 0.3);

  // ═════ ESCENA B · cuándo y qué hacer ═════
  tl.fromTo("#fecha", { opacity: 0, y: 90, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: POP }, T.fecha);
  tl.fromTo(".cal .draw", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.8, ease: IN, stagger: 0.15 }, T.fecha + 0.15);
  flotar(tl, "#fecha-flota", T.fecha + 0.8, T.cta - 0.3, 10, 2.4);
  tl.fromTo("#pasos", { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.8, ease: POP }, T.pasos);
  tl.fromTo($$("#pasos li"), { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.6, ease: IN, stagger: 0.35 }, T.pasos + 0.2);
  flotar(tl, "#pasos-flota", T.pasos + 0.8, T.cta - 0.3, 10, 2.0);
  tl.to("#escena-b", { opacity: 0, y: -100, scale: 0.97, duration: 0.3, ease: OUT }, T.cta - 0.3);

  // ═════ ESCENA C · SPECTACLE BEAT: todo el lienzo rebota hacia el botón ═════
  tl.fromTo("#camara", { scale: 1 }, { scale: 1.06, duration: 0.16, ease: "power2.out" }, T.cta);
  tl.to("#camara", { scale: 1, duration: 0.9, ease: "back.out(2.6)" }, T.cta + 0.16);
  tl.fromTo("#boton", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.95, ease: "back.out(3.2)" }, T.cta);
  // resplandor pálido con base dorada: estalla, se asienta y respira
  tl.fromTo("#boton", { filter: "drop-shadow(0px 0px 0px rgba(241,236,176,0))" },
    { filter: "drop-shadow(0px 0px 46px rgba(241,236,176,0.85))", duration: 0.2, ease: IN }, T.cta);
  tl.to("#boton", { filter: "drop-shadow(0px 0px 22px rgba(210,185,106,0.6))", duration: 0.8, ease: "power2.out" }, T.cta + 0.25);
  tl.to("#boton", { filter: "drop-shadow(0px 0px 40px rgba(241,236,176,0.55))", duration: 0.6, ease: "sine.inOut", repeat: 3, yoyo: true }, T.cta + 1.1);
  flotar(tl, "#boton-flota", T.cta + 0.9, T.fin, 8, 1.6);
  destello(tl, T.cta, 1);
  tl.to(fondoEstado, { energia: 0.95, duration: 1.2, ease: IN }, T.cta);
  tl.fromTo("#sub", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: IN }, T.cta + 0.5);
  tl.fromTo("#firma", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.8, ease: POP }, T.cta + 0.9);
  tl.fromTo(".web", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: IN }, T.cta + 1.2);

  window.__timelines = Object.assign(window.__timelines || {}, { "yezid-envivo-premium": tl });
  return tl;
}
