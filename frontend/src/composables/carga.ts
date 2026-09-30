import { ref, shallowRef, watch, type WatchSource } from "vue";

/**
 * Pide datos y expone su estado: cargando, error y los datos.
 * Si se pasa `dependencia` (p. ej. el id de la ruta), vuelve a pedir cuando cambia.
 */
export function useCarga<T>(pedir: () => Promise<T>, dependencia?: WatchSource) {
  const datos = shallowRef<T | null>(null);
  const cargando = ref(true);
  const error = ref<string | null>(null);
  let turno = 0;

  async function recargar(silencioso = false) {
    const mio = ++turno;
    if (!silencioso) cargando.value = true;
    error.value = null;
    try {
      const d = await pedir();
      if (mio === turno) datos.value = d;
    } catch (e) {
      if (mio === turno) error.value = (e as Error).message;
    } finally {
      if (mio === turno) cargando.value = false;
    }
  }

  if (dependencia) watch(dependencia, () => recargar(), { immediate: true });
  else recargar();
  return { datos, cargando, error, recargar };
}
