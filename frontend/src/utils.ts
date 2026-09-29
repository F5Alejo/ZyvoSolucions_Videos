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
