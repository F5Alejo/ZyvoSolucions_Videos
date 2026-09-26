// Reproductor de preview y ganchos de render. Un solo reloj: el MP3 de la voz si
// existe (assets/voz/<variante>.mp3), si no el reloj de pared. Ese tiempo mueve el
// timeline de GSAP y el fondo WebGL a la vez.
import { CAMPANA } from "./config.js";
import { crearFondo } from "./red.js";
import { construir } from "./escena.js";

const params = new URLSearchParams(location.search);
const V = CAMPANA[params.get("v")] ? params.get("v") : "pocos";
const cfg = CAMPANA[V];
const FIN = cfg.tiempos.fin;
const RENDER = params.get("render") === "1";
if (RENDER) document.body.classList.add("render");

const stage = document.getElementById("stage");
await document.fonts.ready;
const fondo = crearFondo(document.getElementById("bg"), { pocos: 7, manana: 19, hoy: 31 }[V]);
const tl = construir(cfg);
tl.seek(FIN, false).seek(0, false);   // recorrido completo: cada tween registra sus valores en orden

let t = 0, playing = false, t0 = 0, wall = 0;
const voz = document.getElementById("voz");
let hayVoz = false;
try { hayVoz = (await fetch(`assets/voz/${V}.mp3`, { method: "HEAD" })).ok; } catch { /* sin voz: mudo */ }
if (hayVoz) voz.src = `assets/voz/${V}.mp3`;

function seek(x) {
  t = Math.max(0, Math.min(FIN, x));
  tl.seek(t, false);
  fondo.render(t);
  if (!RENDER) { clock.textContent = t.toFixed(2) + " s"; range.value = t; }
}
window.seekTo = seek;   // render fotograma a fotograma (tools/render.mjs)

function play() {
  if (t >= FIN - 0.01) seek(0);
  playing = true; t0 = t; wall = performance.now();
  if (hayVoz) { voz.currentTime = t; voz.play().catch(() => {}); }
  playBtn.textContent = "❚❚";
}
function pause() { playing = false; voz.pause(); playBtn.textContent = "▶"; }
function tick(now) {
  if (playing) {
    let nt = hayVoz && !voz.paused ? voz.currentTime : t0 + (now - wall) / 1000;
    if (nt >= FIN) { if (loop.checked) { seek(0); play(); requestAnimationFrame(tick); return; } nt = FIN; pause(); }
    seek(nt);
  }
  requestAnimationFrame(tick);
}

// ── panel ──
const playBtn = document.getElementById("play"), loop = document.getElementById("loop");
const range = document.getElementById("range"), clock = document.getElementById("clock");
range.max = FIN;
playBtn.onclick = () => (playing ? pause() : play());
document.getElementById("restart").onclick = () => { seek(0); play(); };
range.oninput = () => { pause(); seek(+range.value); };
document.getElementById("audio-state").textContent = hayVoz ? `voz: assets/voz/${V}.mp3` : "voz: sin MP3 (mudo)";
document.querySelectorAll("#tabs button").forEach((b) => {
  b.classList.toggle("on", b.dataset.v === V);
  b.onclick = () => { params.set("v", b.dataset.v); location.search = params.toString(); };
});
addEventListener("keydown", (e) => {
  if (e.code === "Space") { e.preventDefault(); playing ? pause() : play(); }
  if (e.key === "ArrowRight") { pause(); seek(t + 0.1); }
  if (e.key === "ArrowLeft") { pause(); seek(t - 0.1); }
});
function fit() {
  if (RENDER) return;
  const vp = document.getElementById("viewport").getBoundingClientRect();
  const s = Math.min(vp.width / 1080, vp.height / 1920) * 0.94;
  stage.style.transform = `scale(${s})`;
  stage.style.left = (vp.width - 1080 * s) / 2 + "px";
  stage.style.top = (vp.height - 1920 * s) / 2 + "px";
}
addEventListener("resize", fit);

fit();
seek(0);
requestAnimationFrame(tick);
if (!RENDER && params.get("autoplay") !== "0") play();
