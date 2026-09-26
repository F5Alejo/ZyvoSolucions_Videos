// Coreografía GSAP: arma el DOM desde config.js y devuelve UN timeline en pausa
// (seek-safe: sin setTimeout, sin repeat:-1, sin azar). Entradas con máscaras de
// recorte y staggers letra por letra — cero fades lineales.
import { COMUN, BOTON } from "./config.js";
import { estado } from "./estudio.js";

/* global gsap */
const EXPO = "expo.out", POP = "back.out(1.5)", P4 = "power4.out", SALE = "power4.in";
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

// palabra → <span class="mascara"><span>…</span></span> (la máscara recorta la entrada)
function enMascaras(el, texto, { letras = false } = {}) {
  el.textContent = "";
  for (const m of texto.matchAll(/\*([^*]+)\*|_([^_]+)_|([^*_]+)/g)) {
    const [trozo, cls] = m[1] ? [m[1], "b"] : m[2] ? [m[2], "acento"] : [m[3], ""];
    for (const palabra of trozo.split(/\s+/).filter(Boolean)) {
      // la puntuación suelta («.», «,») se pega a la palabra anterior: sin espacio delante
      if (/^[.,;:!?…]+$/.test(palabra) && el.lastChild && !letras) { el.lastChild.firstChild.textContent += palabra; continue; }
      const mask = document.createElement("span"); mask.className = "mascara";
      const dentro = document.createElement("span"); if (cls) dentro.className = cls;
      if (letras) for (const c of palabra) { const ch = document.createElement("span"); ch.className = "ch"; ch.textContent = c; dentro.appendChild(ch); }
      else dentro.textContent = palabra;
      mask.appendChild(dentro); el.appendChild(mask);
    }
  }
}

// ambient idle: flotación en Y con repeticiones contadas
function flotar(tl, el, desde, hasta, amp, periodo) {
  const medio = periodo / 2, n = Math.max(1, Math.floor((hasta - desde) / medio));
  tl.fromTo(el, { y: 0 }, { y: -amp, duration: medio, ease: "sine.inOut", repeat: n - 1, yoyo: true }, desde);
}

export function construir(video, T, FIN = 12) {
  // ── textos ──
  $$("[data-t]").forEach((el) => (el.textContent = COMUN[el.dataset.t]));
  $("#foto").src = COMUN.foto;
  enMascaras($("#titular"), video.titular, { letras: true });
  enMascaras($("#subtitulo"), video.subtitulo);
  $("#info").innerHTML = video.info.map(([k, v]) => `<div class="dato cristal"><small>${k}</small><b>${v}</b></div>`).join("");
  $("#boton").textContent = video.boton;
  $("#sub").textContent = video.sub;
  $("#stage").classList.add("boton-" + BOTON);
  $("#stage").classList.toggle("es-hoy", !!video.enVivo);

  const tl = gsap.timeline({ paused: true });
  tl.fromTo(estado, { pulso: 0, zoom: 0 }, { pulso: 0, zoom: 0, duration: 0.01 }, 0);
  tl.fromTo(".progreso i", { scaleX: 0 }, { scaleX: 1, duration: FIN, ease: "none" }, 0);

  // TODO el conjunto flota microscópicamente: la pantalla nunca es una imagen fija
  flotar(tl, "#contenido", 0, FIN, 6, 4.0);

  // ── rótulo + latido del punto pálido (pings contados) ──
  tl.fromTo("#eyebrow", { clipPath: "inset(0 50% 0 50% round 100px)", y: -20 },
    { clipPath: "inset(0 0% 0 0% round 100px)", y: 0, duration: 0.9, ease: P4 }, 0.05);
  for (let t = 0.6; t < FIN - 0.8; t += 1.2) {
    tl.fromTo(".latido, .en-vivo i", { scale: 1 }, { scale: 1.5, duration: 0.18, ease: "power2.out", immediateRender: false }, t);
    tl.to(".latido, .en-vivo i", { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.18);
  }

  // ── la foto: el cristal se abre de abajo arriba y la foto entra con punch-in ──
  tl.fromTo("#foto-card", { clipPath: "inset(100% 0 0 0 round 40px)" },
    { clipPath: "inset(0% 0 0 0 round 40px)", duration: 1.1, ease: P4 }, 0.1);
  tl.fromTo("#foto", { scale: 1.25, y: 60 }, { scale: 1, y: 0, duration: 1.4, ease: EXPO }, 0.1);
  tl.fromTo("#nombre", { clipPath: "inset(0 100% 0 0 round 22px)", x: -30 },
    { clipPath: "inset(0 0% 0 0 round 22px)", x: 0, duration: 0.8, ease: P4 }, 0.8);
  flotar(tl, "#foto-flota", 1.0, FIN, 16, 3.2);

  // ═════ HOOK · titular letra por letra desde su máscara ═════
  tl.fromTo($$("#titular .ch"), { yPercent: 115, rotation: 6 },
    { yPercent: 0, rotation: 0, duration: 0.85, ease: EXPO, stagger: 0.035 }, T.hook);
  tl.to(estado, { pulso: 0.5, duration: 0.08, ease: P4 }, T.hook + 0.25);
  tl.to(estado, { pulso: 0, duration: 0.9, ease: "power2.out" }, T.hook + 0.33);

  // ═════ VALOR · subtítulo en cascada por palabras, datos en cristal ═════
  tl.fromTo($$("#subtitulo .mascara > span"), { yPercent: 110 },
    { yPercent: 0, duration: 0.8, ease: P4, stagger: 0.045 }, T.valor);
  tl.fromTo($$("#info .dato"), { clipPath: "inset(0 100% 0 0 round 24px)", x: -40 },
    { clipPath: "inset(0 0% 0 0 round 24px)", x: 0, duration: 0.8, ease: P4, stagger: 0.18 }, T.valor + 0.8);
  flotar(tl, "#info", T.valor + 1.6, T.cta - 0.3, 8, 2.2);

  // salida por máscara: todo sube y se recorta
  tl.fromTo("#mensaje", { clipPath: "inset(0% 0 0% 0)", y: 0 }, { clipPath: "inset(0% 0 100% 0)", y: -80, duration: 0.4, ease: SALE }, T.cta - 0.45);
  tl.set("#mensaje", { visibility: "hidden" }, T.cta);

  // ═════ CTA · SPECTACLE: zoom-in de la cámara 3D + rebote del botón 1.5→1 ═════
  tl.fromTo(estado, { zoom: 0 }, { zoom: 1, duration: 1.4, ease: "power3.inOut", immediateRender: false }, T.cta - 0.2);
  tl.to(estado, { pulso: 1, duration: 0.08, ease: P4 }, T.cta);
  tl.to(estado, { pulso: 0, duration: 1.0, ease: "power2.out" }, T.cta + 0.08);
  tl.fromTo("#boton", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.9, ease: POP }, T.cta);
  const tono = BOTON === "verde" ? "69,160,53" : "210,185,106";
  tl.fromTo("#boton", { filter: `drop-shadow(0px 0px 0px rgba(${tono},0))` },
    { filter: `drop-shadow(0px 0px 60px rgba(${tono},0.95))`, duration: 0.22, ease: P4 }, T.cta);
  tl.to("#boton", { filter: `drop-shadow(0px 0px 22px rgba(${tono},0.55))`, duration: 0.8, ease: "power2.out" }, T.cta + 0.25);
  tl.to("#boton", { filter: "drop-shadow(0px 0px 44px rgba(241,236,176,0.6))", duration: 0.55, ease: "sine.inOut", repeat: 3, yoyo: true }, T.cta + 1.1);
  flotar(tl, "#boton-flota", T.cta + 0.9, FIN, 8, 1.6);
  tl.fromTo("#sub", { clipPath: "inset(0 50% 0 50%)" }, { clipPath: "inset(0 0% 0 0%)", duration: 0.8, ease: P4 }, T.cta + 0.45);
  tl.fromTo("#firma", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 1.0, ease: P4 }, T.cta + 0.8);
  tl.fromTo(".web", { yPercent: 120, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.6, ease: EXPO }, T.cta + 1.2);

  window.__timelines = Object.assign(window.__timelines || {}, { "yezid-envivo-estudio": tl });
  return tl;
}
