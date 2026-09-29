import { reactive } from "vue";

export interface Aviso { id: number; texto: string; tipo: "ok" | "error" }

export const avisos = reactive<Aviso[]>([]);
let siguiente = 1;

/** Un aviso flotante que se va solo. Los errores duran más para que dé tiempo a leerlos. */
export function avisar(texto: string, tipo: Aviso["tipo"] = "ok") {
  const id = siguiente++;
  avisos.push({ id, texto, tipo });
  setTimeout(() => cerrarAviso(id), tipo === "error" ? 7000 : 3500);
}

export function cerrarAviso(id: number) {
  const i = avisos.findIndex((a) => a.id === id);
  if (i >= 0) avisos.splice(i, 1);
}
