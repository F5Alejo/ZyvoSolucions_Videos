/** 125 → «2:05». */
export function mmss(segundos: number): string {
  const s = Math.round(segundos);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** cuenta(1, "video") → «1 video»; cuenta(3, "video") → «3 videos». */
export function cuenta(n: number, uno: string, varios = uno + "s"): string {
  return `${n.toLocaleString("es-CO")} ${n === 1 ? uno : varios}`;
}

/** Para buscar sin importar tildes ni mayúsculas. */
export function normalizar(t: string): string {
  return t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
}

export function mb(bytes: number): string {
  return (bytes / 1048576).toLocaleString("es-CO", { maximumFractionDigits: 1 }) + " MB";
}

export function fecha(iso: string): string {
  const d = new Date(iso.length === 10 ? iso + "T12:00:00" : iso);
  return d.toLocaleDateString("es-CO", { day: "numeric", month: "short", year: "numeric" });
}

// ── Color ───────────────────────────────────────────────────────────────────

function luminancia(hex: string): number {
  const c = hex.replace("#", "");
  const [r, g, b] = [0, 2, 4].map((i) => {
    const v = parseInt(c.slice(i, i + 2), 16) / 255;
    return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!;
}

/** Contraste WCAG entre dos colores (1 a 21). */
export function contraste(a: string, b: string): number {
  const [x, y] = [luminancia(a), luminancia(b)].sort((m, n) => n - m);
  return (x! + 0.05) / (y! + 0.05);
}

/**
 * El primer color de `candidatos` que se lee sobre `fondo` (≥ `minimo`:1).
 * Si ninguno llega, blanco o casi negro: el que más contraste dé.
 */
export function tintaLegible(fondo: string, candidatos: string[] = [], minimo = 4.5): string {
  const bueno = candidatos.find((c) => contraste(c, fondo) >= minimo);
  if (bueno) return bueno;
  return contraste("#FFFFFF", fondo) >= contraste("#111111", fondo) ? "#FFFFFF" : "#111111";
}

export interface Trozo { texto: string; marcado: boolean }

/**
 * Parte un texto en trozos, marcando las citas (normas y cifras) que hay que revisar.
 * Se usa con interpolación de Vue, nunca con v-html: el texto del cliente no se interpreta.
 */
export function resaltar(texto: string, citas: string[]): Trozo[] {
  const validas = [...new Set(citas.filter(Boolean))].sort((a, b) => b.length - a.length);
  if (!validas.length) return [{ texto, marcado: false }];
  const escapar = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const patron = new RegExp(`(${validas.map(escapar).join("|")})`, "g");
  return texto
    .split(patron)
    .filter((t) => t !== "")
    .map((t) => ({ texto: t, marcado: validas.includes(t) }));
}
