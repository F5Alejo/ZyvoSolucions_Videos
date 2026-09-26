// Hoja de contactos rápida: node tools/snap.mjs <ad> <t1,t2,...> <salida.png> [base]
import puppeteer from "puppeteer-core";
import { existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
const [ad, lista, out, base = "http://localhost:5530"] = process.argv.slice(2);
const CHROME = ["C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"].find(existsSync);
const b = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--hide-scrollbars"] });
const p = await b.newPage();
const errores = [];
p.on("pageerror", (e) => errores.push(String(e)));
p.on("console", (m) => m.type() === "error" && errores.push(m.text()));
await p.setViewport({ width: 1080, height: 1920 });
await p.goto(`${base}/?ad=${ad}&render=1&autoplay=0`, { waitUntil: "networkidle0" });
await p.waitForFunction(() => typeof window.seekTo === "function", { timeout: 15000 });
const tiempos = lista.split(",").map(Number), archivos = [];
for (const [i, t] of tiempos.entries()) {
  await p.evaluate((t) => { return Promise.resolve(window.seekTo(t)).then(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))); }, t);
  const f = out.replace(/\.png$/, `-${i}.png`);
  await p.screenshot({ path: f }); archivos.push(f);
}
await b.close();
const ins = archivos.flatMap((f) => ["-i", f]);
const fil = archivos.map((_, i) => `[${i}]scale=270:-1[s${i}]`).join(";") + ";" + archivos.map((_, i) => `[s${i}]`).join("") + `hstack=${archivos.length}`;
execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...ins, "-filter_complex", fil, out]);
console.log(errores.filter((e) => !/404|Failed to load resource/.test(e)).join("\n") || "sin errores");
