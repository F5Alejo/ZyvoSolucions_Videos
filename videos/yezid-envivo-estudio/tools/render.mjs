// Render determinista a MP4: abre el lienzo en modo render (?render=1), busca cada
// fotograma con window.seekTo(t) —GSAP y shader leen el mismo t— lo captura y lo
// pasa a ffmpeg por tubería. Usa el Chrome instalado en el sistema.
//
//   node tools/render.mjs --out <carpeta> [--variantes v1,v2,v3] [--fondo escudo|plexus] [--fps 30]
//                         [--base http://localhost:5540] [--prefix nombre]
//
// Requiere el servidor de preview corriendo (npm run dev) y ffmpeg en el PATH.
import { spawn } from "node:child_process";
import { mkdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import puppeteer from "puppeteer-core";

const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i > 0 ? process.argv[i + 1] : d; };
const OUT = arg("out", "renders");
const VARIANTES = arg("variantes", "v1,v2,v3").split(",");
const FONDO = arg("fondo", "escudo");
const FPS = +arg("fps", "30");
const BASE = arg("base", "http://localhost:5540");
const PREFIX = arg("prefix", "V4");
const DUR = 12;
const NAMES = { v1: "01-Faltan-pocos-dias", v2: "02-Es-manana", v3: "03-Es-hoy" };

const CHROME = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
].find(existsSync);

mkdirSync(OUT, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: CHROME, headless: true,
  args: ["--hide-scrollbars", "--force-device-scale-factor=1", "--ignore-gpu-blocklist", "--enable-webgl"],
});

for (const ad of VARIANTES) {
  const file = join(OUT, `${PREFIX}-${NAMES[ad]}.mp4`);
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto(`${BASE}/?v=${ad}&fondo=${FONDO}&render=1&autoplay=0`, { waitUntil: "networkidle0" });
  await page.waitForFunction(() => typeof window.seekTo === "function");
  await page.evaluate(() => document.fonts.ready);
  const cdp = await page.createCDPSession();

  const ff = spawn("ffmpeg", [
    "-y", "-loglevel", "error",
    "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",           // pista muda: algunas redes exigen audio
    "-map", "0:v", "-map", "1:a", "-shortest",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", String(FPS),
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", file,
  ], { stdio: ["pipe", "inherit", "inherit"] });

  const frames = DUR * FPS;
  const t0 = Date.now();
  for (let f = 0; f < frames; f++) {
    await page.evaluate((t) => { window.seekTo(t); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); }, f / FPS);
    const { data } = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 95, optimizeForSpeed: true });
    if (!ff.stdin.write(Buffer.from(data, "base64"))) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 60 === 0) process.stdout.write(`\r${NAMES[ad]}  ${f}/${frames}`);
  }
  ff.stdin.end();
  await new Promise((r, j) => ff.on("close", (c) => (c === 0 ? r() : j(new Error("ffmpeg " + c)))));
  console.log(`\r${NAMES[ad]}  ${frames}/${frames}  → ${file}  (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  await page.close();
}
await browser.close();
