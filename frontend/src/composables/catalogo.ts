import { ref } from "vue";
import { api } from "../api";
import type { Catalogo } from "../tipos";

/** Estados, tipos, marcas y voces: se piden una vez y los comparte toda la aplicación. */
export const catalogo = ref<Catalogo | null>(null);
let pedido: Promise<void> | null = null;

export function cargarCatalogo(forzar = false): Promise<void> {
  if (!pedido || forzar) {
    pedido = api.get<Catalogo>("/api/catalogo").then((c) => { catalogo.value = c; })
      .catch((e) => { pedido = null; throw e; });
  }
  return pedido;
}
