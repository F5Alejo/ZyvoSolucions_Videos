import { nextTick, reactive } from "vue";

export type TemaAyuda = "como-funciona" | "notas" | "resaltado" | "videos" | "cambiar" | "privacidad";

export const ayuda = reactive({ abierta: false });

/** Abre la ayuda; si se pide un tema, lo lleva a la vista. */
export async function abrirAyuda(tema?: TemaAyuda) {
  ayuda.abierta = true;
  if (!tema) return;
  await nextTick();
  document.getElementById(`ayuda-${tema}`)?.scrollIntoView({ block: "start" });
}
