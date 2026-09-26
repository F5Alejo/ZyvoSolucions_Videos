// Hoja de contactos rápida: captura instantes concretos de una variante.
//   node tools/snap.mjs <variante> <salida.png> 1.0 3.0 6.0 9.5
import { existsSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import puppeteer from "puppeteer-core";

const [variante, salida, ...tiempos] = process.argv.slice(2);
const CHROME = ["C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"].find(existsSync);
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--hide-scrollbars"] });
const page = await browser.newPage();
const errores = [];
page.on("pageerror", (e) => errores.push(e.message));
page.on("console", (m) => m.type() === "error" && errores.push(m.text()));
await page.setViewport({ width: 1080, height: 1920 });
await page.goto(`http://localhost:5530/?v=${variante}&render=1&autoplay=0`, { waitUntil: "networkidle0" });
await page.waitForFunction(() => typeof window.seekTo === "function", { timeout: 20000 });
const dir = join(dirname(salida), "_snap"); mkdirSync(dir, { recursive: true });
const pngs = [];
for (const t of tiempos) {
  await page.evaluate((x) => { window.seekTo(x); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); }, +t);
  const f = join(dir, `${variante}-${t}.png`); await page.screenshot({ path: f }); pngs.push(f);
}
await browser.close();
const ins = pngs.flatMap((p) => ["-i", p]);
const fc = pngs.map((_, i) => `[${i}]scale=270:-1[s${i}]`).join(";") + ";" + (pngs.length > 1 ? pngs.map((_, i) => `[s${i}]`).join("") + `hstack=${pngs.length}` : "[s0]null");
execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...ins, "-filter_complex", fc, salida]);
console.log(errores.length ? "ERRORES:\n" + errores.join("\n") : "sin errores de consola", "→", salida);
