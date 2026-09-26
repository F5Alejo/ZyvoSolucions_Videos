// Reproductor de preview. El reloj es uno solo: o el MP3 de la locución (si existe)
// o el reloj de pared. Ese tiempo se empuja al timeline de GSAP y al shader.
import { createBackground, BG_MODES } from "./bg.js";
import { buildAds, SCRIPTS, VERSION, videoTimelines as T } from "./ads.js";

const params = new URLSearchParams(location.search);
const RENDER = params.get("render") === "1";
if (RENDER) document.body.classList.add("render");

const BG = BG_MODES.includes(params.get("bg")) ? params.get("bg") : "liquido";
const stage = document.getElementById("stage");
stage.classList.toggle("v2", VERSION === 2);
stage.classList.add("bg-" + BG);
const bg = createBackground(document.getElementById("bg"), BG);
const tls = buildAds(stage);
const SEED = { ad1: 0, ad2: 23, ad3: 57 }; // cada video con su propia forma de líquido

let cur = "ad" + (params.get("ad") || "1");
let t = 0, playing = false, wallStart = 0, tStart = 0;

// ── audio: se activa solo si el archivo existe en assets/voz/ ──
const voices = {};
const audioState = document.getElementById("audio-state");
async function probeAudio() {
  for (const el of document.querySelectorAll("audio[data-src]")) {
    try {
      const r = await fetch(el.dataset.src, { method: "HEAD" });
      if (r.ok) { el.src = el.dataset.src; voices[el.id] = el; }
    } catch { /* sin archivo: el preview sigue mudo */ }
  }
  refreshAudioLabel();
}
const vo = () => voices["vo-" + cur];
function refreshAudioLabel() {
  audioState.textContent = vo() ? "voz: " + vo().dataset.src : "voz: sin MP3 (mudo)";
}

// ── escala del lienzo ──
function fit() {
  if (RENDER) return;
  const vp = document.getElementById("viewport").getBoundingClientRect();
  const s = Math.min(vp.width / 1080, vp.height / 1920) * 0.94;
  stage.style.transform = `scale(${s})`;
  stage.style.left = (vp.width - 1080 * s) / 2 + "px";
  stage.style.top = (vp.height - 1920 * s) / 2 + "px";
}
addEventListener("resize", fit);

// ── cambio de anuncio ──
function select(id) {
  pause();
  cur = id;
  stage.querySelectorAll(".ad").forEach((a) => a.classList.toggle("active", a.id === id));
  // recorrido completo para que todos los tweens registren sus valores en orden
  tls[id].seek(T.end, false).seek(0, false);
  seek(0);
  document.querySelectorAll("#tabs button").forEach((b) => b.classList.toggle("on", b.dataset.ad === id));
  renderScript();
  refreshAudioLabel();
  history.replaceState(null, "", `?ad=${id.slice(2)}&v=${VERSION}&bg=${BG}` + (RENDER ? "&render=1" : ""));
}

function seek(time) {
  t = Math.max(0, Math.min(T.end, time));
  tls[cur].seek(t, false);
  bg.render(t, SEED[cur]);
  ui();
}
window.seekTo = seek; // gancho para capturas fotograma a fotograma

function play() {
  if (t >= T.end - 0.01) seek(0);
  playing = true; wallStart = performance.now(); tStart = t;
  Object.values(voices).forEach((a) => a.pause());
  const a = vo(); if (a) { a.currentTime = t; a.play().catch(() => {}); }
  const m = voices.music; if (m) { m.currentTime = t; m.volume = vo() ? 0.25 : 0.8; m.play().catch(() => {}); }
  playBtn.textContent = "❚❚";
}
function pause() {
  playing = false;
  Object.values(voices).forEach((a) => a.pause());
  playBtn.textContent = "▶";
}

function tick(now) {
  if (playing) {
    const a = vo();
    let nt = a && !a.paused ? a.currentTime : tStart + (now - wallStart) / 1000;
    if (nt >= T.end) {
      if (loopChk.checked) { seek(0); play(); requestAnimationFrame(tick); return; }
      nt = T.end; pause();
    }
    seek(nt);
  }
  requestAnimationFrame(tick);
}

// ── UI ──
const playBtn = document.getElementById("play");
const loopChk = document.getElementById("loop");
const range = document.getElementById("range");
const clock = document.getElementById("clock");
playBtn.onclick = () => (playing ? pause() : play());
document.getElementById("restart").onclick = () => { seek(0); play(); };
range.oninput = () => { pause(); seek(+range.value); };
document.querySelectorAll("#tabs button").forEach((b) => (b.onclick = () => { select(b.dataset.ad); play(); }));
addEventListener("keydown", (e) => {
  if (e.code === "Space") { e.preventDefault(); playing ? pause() : play(); }
  if (e.key === "ArrowRight") { pause(); seek(t + 0.1); }
  if (e.key === "ArrowLeft") { pause(); seek(t - 0.1); }
  if (["1", "2", "3"].includes(e.key)) { select("ad" + e.key); play(); }
});

function segAt(time) { return time < T.valor ? "hook" : time < T.cta ? "valor" : "cta"; }
function ui() {
  if (RENDER) return;
  clock.textContent = t.toFixed(2) + " s";
  range.value = t;
  const s = segAt(t);
  document.querySelectorAll("#script .seg-card").forEach((c) => c.classList.toggle("on", c.dataset.seg === s));
}
function renderScript() {
  const S = SCRIPTS[cur];
  document.getElementById("script").innerHTML = S.segs.map((g) => `
    <div class="seg-card" data-seg="${g.id}">
      <h4>${g.id.toUpperCase()} · ${g.t}</h4>
      <div class="vo">${g.vo}</div>
      <div class="dir">${g.dir}</div>
    </div>`).join("");
  document.querySelector("#board div").innerHTML =
    "<table>" + S.board.map(([k, v]) => `<tr><td>${k}s</td><td>${v}</td></tr>`).join("") + "</table>";
}

// selectores de versión y fondo: recargan con los parámetros nuevos
for (const [id, key, val] of [["sel-v", "v", String(VERSION)], ["sel-bg", "bg", BG]]) {
  const el = document.getElementById(id);
  if (!el) continue;
  el.value = val;
  el.onchange = () => { params.set(key, el.value); params.set("ad", cur.slice(2)); location.search = params.toString(); };
}

await document.fonts.ready;
fit();
probeAudio();
select(cur);
requestAnimationFrame(tick);
if (!RENDER && params.get("autoplay") !== "0") play();
