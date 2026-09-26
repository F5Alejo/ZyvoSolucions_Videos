// Reproductor de preview y ganchos de render. Un solo reloj: la voz (assets/voz/<v>.mp3)
// si existe, si no el reloj de pared. Mueve a la vez el timeline de GSAP y el estudio 3D.
import { VIDEOS, videoTimestamps, GUIONES } from "./config.js";
import { crearEstudio } from "./estudio.js";
import { construir } from "./escena.js";

const params = new URLSearchParams(location.search);
const V = VIDEOS[params.get("v")] ? params.get("v") : "v1";
const FONDO = params.get("fondo") === "plexus" ? "plexus" : "escudo";
const FIN = 12;
const RENDER = params.get("render") === "1";
if (RENDER) document.body.classList.add("render");

await document.fonts.ready;
const estudio = crearEstudio(document.getElementById("bg"), FONDO);
document.getElementById("stage").classList.add("fondo-" + FONDO);
const tl = construir(VIDEOS[V], videoTimestamps[V], FIN);
tl.seek(FIN, false).seek(0, false);   // recorrido completo: cada tween registra sus valores en orden

let t = 0, playing = false, t0 = 0, wall = 0, hayVoz = false;
const voz = document.getElementById("voz");
try { hayVoz = (await fetch(`assets/voz/${V}.mp3`, { method: "HEAD" })).ok; } catch { /* mudo */ }
if (hayVoz) voz.src = `assets/voz/${V}.mp3`;

function seek(x) {
  t = Math.max(0, Math.min(FIN, x));
  tl.seek(t, false);
  estudio.render(t);
  if (!RENDER) { clock.textContent = t.toFixed(2) + " s"; range.value = t; }
}
window.seekTo = seek;

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

const playBtn = document.getElementById("play"), loop = document.getElementById("loop");
const range = document.getElementById("range"), clock = document.getElementById("clock");
playBtn.onclick = () => (playing ? pause() : play());
document.getElementById("restart").onclick = () => { seek(0); play(); };
range.oninput = () => { pause(); seek(+range.value); };
document.getElementById("audio-state").textContent = hayVoz ? `voz: assets/voz/${V}.mp3` : "voz: sin MP3 (mudo)";
document.getElementById("guion").innerHTML = `<h4>Guion ElevenLabs</h4><p>${GUIONES[V]}</p>`;
const ir = (k, v) => { params.set(k, v); location.search = params.toString(); };
document.querySelectorAll("#tabs button").forEach((b) => { b.classList.toggle("on", b.dataset.v === V); b.onclick = () => ir("v", b.dataset.v); });
document.querySelectorAll("#fondos button").forEach((b) => { b.classList.toggle("on", b.dataset.fondo === FONDO); b.onclick = () => ir("fondo", b.dataset.fondo); });
addEventListener("keydown", (e) => {
  if (e.code === "Space") { e.preventDefault(); playing ? pause() : play(); }
  if (e.key === "ArrowRight") { pause(); seek(t + 0.1); }
  if (e.key === "ArrowLeft") { pause(); seek(t - 0.1); }
});
function fit() {
  if (RENDER) return;
  const vp = document.getElementById("viewport").getBoundingClientRect(), stage = document.getElementById("stage");
  const s = Math.min(vp.width / 1080, vp.height / 1920) * 0.94;
  stage.style.transform = `scale(${s})`;
  stage.style.left = (vp.width - 1080 * s) / 2 + "px";
  stage.style.top = (vp.height - 1920 * s) / 2 + "px";
}
addEventListener("resize", fit);
fit(); seek(0); requestAnimationFrame(tick);
if (!RENDER && params.get("autoplay") !== "0") play();
