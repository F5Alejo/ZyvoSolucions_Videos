import type { AjustesAnim, AnimacionCurso, ElementosAnim, Fase, PasoAnim, PlantillaAnim } from "./tipos";

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

/** Lo que `nuevo` cambia respecto a `base` (objetos de dos niveles, como los grupos de ajustes). */
export function diferencias<T extends Record<string, Record<string, unknown>>>(base: T, nuevo: T): Partial<T> {
  const salida: Record<string, Record<string, unknown>> = {};
  for (const grupo of Object.keys(nuevo)) {
    for (const [clave, valor] of Object.entries(nuevo[grupo] ?? {})) {
      if (JSON.stringify(valor) !== JSON.stringify(base[grupo]?.[clave])) (salida[grupo] ??= {})[clave] = valor;
    }
  }
  return salida as Partial<T>;
}


function mezclarAnim(base: ElementosAnim, ajustes: AjustesAnim | undefined): ElementosAnim {
  const salida = clonar(base);
  for (const [el, fases] of Object.entries(ajustes ?? {})) {
    for (const [fase, valores] of Object.entries(fases ?? {})) {
      const destino = salida[el]?.[fase as Fase];
      if (destino) Object.assign(destino, valores);
    }
  }
  return salida;
}

/** La animación resuelta de una lámina (o del curso si `n` es null): igual que animacion.plan en el servidor. */
export function resolverAnimacion(plantillas: PlantillaAnim[], a: AnimacionCurso, defecto: string, n: number | null) {
  const propia = n === null ? undefined : a.laminas[String(n)];
  const pedida = propia?.plantilla || a.plantilla || defecto;
  const p = plantillas.find((x) => x.id === pedida) ?? plantillas.find((x) => x.id === "dinamica") ?? plantillas[0]!;
  let elementos = p.elementos;
  if (!propia?.plantilla) elementos = mezclarAnim(elementos, a.ajustes);
  return { plantilla: p.id, elementos: mezclarAnim(elementos, propia?.ajustes) };
}

/** Cambia un ajuste en la capa que toca (curso o lámina) y devuelve la animación nueva. */
export function fijarAjuste(a: AnimacionCurso, n: number | null, el: string, fase: Fase, clave: keyof PasoAnim, valor: string | number): AnimacionCurso {
  const nueva = clonar(a);
  const capa = n === null ? nueva.ajustes : ((nueva.laminas[String(n)] ??= { plantilla: null, ajustes: {} }).ajustes);
  ((capa[el] ??= {})[fase] ??= {})[clave] = valor as never;
  return nueva;
}

/** Copia profunda de datos JSON. `structuredClone` falla con los objetos reactivos de Vue (Proxy). */
export function clonar<T>(x: T): T {
  return JSON.parse(JSON.stringify(x)) as T;
}
