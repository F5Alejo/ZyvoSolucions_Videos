<script setup lang="ts">
// El banco de medios de una marca: los clips y fotos propios que el Director pone de fondo en los videos.
import { onMounted, ref } from "vue";
import { Clapperboard, Image as Imagen, Trash2, Upload } from "@lucide/vue";
import { api, subir } from "../api";
import { avisar } from "../composables/avisos";
import { confirmar } from "../composables/confirmar";
import type { TomaBanco } from "../tipos";

const props = defineProps<{ marca: string; nombre: string }>();
const tomas = ref<TomaBanco[]>([]);
const cargando = ref(true);
const progreso = ref<number | null>(null);
const descripcion = ref("");
const etiquetas = ref("");
const entrada = ref<HTMLInputElement | null>(null);
const base = () => `/api/marcas/${props.marca}/banco`;

async function cargar() {
  try {
    tomas.value = await api.get<TomaBanco[]>(base());
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    cargando.value = false;
  }
}
onMounted(cargar);

async function alElegir(ev: Event) {
  const archivos = Array.from((ev.target as HTMLInputElement).files ?? []);
  for (const [i, archivo] of archivos.entries()) {
    const d = new FormData();
    d.append("archivo", archivo);
    d.append("descripcion", descripcion.value);
    d.append("etiquetas", etiquetas.value);
    try {
      progreso.value = 0;
      const t = await subir<TomaBanco>(base(), d, (f) => (progreso.value = (i + f) / archivos.length));
      tomas.value.push(t);
    } catch (e) {
      avisar(`${archivo.name}: ${(e as Error).message}`, "error");
    }
  }
  progreso.value = null;
  if (entrada.value) entrada.value.value = "";
  if (archivos.length) avisar(archivos.length === 1 ? "La toma quedó en el banco." : `${archivos.length} tomas en el banco.`);
}

async function guardar(t: TomaBanco) {
  try {
    const r = await api.patch<TomaBanco>(`${base()}/${t.id}`, { descripcion: t.descripcion, etiquetas: t.etiquetas });
    Object.assign(t, r);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}

function cambiarEtiquetas(t: TomaBanco, texto: string) {
  t.etiquetas = texto.split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);
  guardar(t);
}

async function eliminar(t: TomaBanco) {
  const si = await confirmar({ titulo: "¿Quitar esta toma del banco?", texto: "Los videos ya producidos no cambian.",
                              aceptar: "Quitar", peligro: true });
  if (!si) return;
  try {
    await api.delete(`${base()}/${t.id}`);
    tomas.value = tomas.value.filter((x) => x.id !== t.id);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}
const segundos = (s: number | null) => (s == null ? "" : `${Math.round(s)} s`);
</script>

<template>
  <section aria-labelledby="titulo-banco">
    <h2 id="titulo-banco" class="flex items-center gap-2 text-lg font-bold"><Clapperboard class="size-5 text-acento" /> Banco de medios</h2>
    <p class="mt-1 max-w-3xl text-sm text-suave">
      Los clips y fotos de {{ nombre }} que salen de fondo en sus videos. El Director elige, frase por frase, la toma
      cuya <strong>descripción y etiquetas</strong> coinciden con lo que dice la voz. Marca con la etiqueta
      <code>general</code> las tomas que sirven para cualquier momento.
    </p>

    <div class="tarjeta mt-4 grid gap-3 p-5 md:grid-cols-[1fr_1fr_auto] md:items-end">
      <label class="text-sm"><span class="mb-1 block font-semibold">Descripción (para las que subas ahora)</span>
        <input v-model="descripcion" class="campo w-full" placeholder="La impresora de resina imprimiendo una pieza" maxlength="400" /></label>
      <label class="text-sm"><span class="mb-1 block font-semibold">Etiquetas, separadas por comas</span>
        <input v-model="etiquetas" class="campo w-full" placeholder="impresora, resina, general" /></label>
      <label class="boton-primario cursor-pointer" :class="progreso !== null && 'pointer-events-none opacity-60'">
        <Upload class="size-4" /> {{ progreso === null ? "Subir clips o fotos" : `Subiendo… ${Math.round(progreso * 100)} %` }}
        <input ref="entrada" type="file" class="sr-only" multiple accept="video/mp4,video/quicktime,video/webm,image/jpeg,image/png,image/webp" @change="alElegir" />
      </label>
    </div>

    <p v-if="!cargando && !tomas.length" class="tarjeta mt-4 p-5 text-sm text-suave">
      Todavía no hay tomas. Sin banco, los videos usan las imágenes de cada lámina sobre el fondo animado de la marca.
    </p>
    <ul v-else class="mt-4 grid grid-cols-[minmax(0,1fr)] gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <li v-for="t in tomas" :key="t.id" class="tarjeta overflow-hidden">
        <div class="relative aspect-video bg-superficie-2">
          <img v-if="t.miniatura" :src="`${base()}/${t.id}/miniatura`" :alt="t.descripcion || t.nombre" class="size-full object-cover" loading="lazy" />
          <span class="absolute top-2 left-2 flex items-center gap-1 rounded-full bg-black/70 px-2 py-0.5 text-[11px] font-semibold text-white">
            <Clapperboard v-if="t.tipo === 'clip'" class="size-3" /><Imagen v-else class="size-3" />
            {{ t.tipo === "clip" ? `Clip · ${segundos(t.duracion)}` : "Foto" }}</span>
          <button type="button" class="absolute top-2 right-2 rounded-full bg-black/70 p-1.5 text-white hover:bg-error"
                  :aria-label="`Quitar ${t.nombre}`" @click="eliminar(t)"><Trash2 class="size-3.5" /></button>
        </div>
        <div class="space-y-2 p-3 text-sm">
          <textarea v-model="t.descripcion" rows="2" class="campo w-full text-sm" placeholder="¿Qué se ve en esta toma?"
                    :aria-label="`Descripción de ${t.nombre}`" maxlength="400" @change="guardar(t)" />
          <input :value="t.etiquetas.join(', ')" class="campo w-full text-xs" placeholder="etiquetas, separadas, por comas"
                 :aria-label="`Etiquetas de ${t.nombre}`" @change="cambiarEtiquetas(t, ($event.target as HTMLInputElement).value)" />
        </div>
      </li>
    </ul>
  </section>
</template>
