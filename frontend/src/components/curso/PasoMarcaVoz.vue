<script setup lang="ts">
import { computed, ref } from "vue";
import { CircleCheck, LoaderCircle, Monitor, Smartphone } from "lucide-vue-next";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import { catalogo } from "../../composables/catalogo";
import type { TrabajoCompleto } from "../../tipos";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();

const marca = ref(props.datos.trabajo.marca);
const voz = ref(props.datos.trabajo.voz);
const formatos = ref([...props.datos.trabajo.formatos]);
const estado = ref<"" | "guardando" | "guardado">("");

const marcas = computed(() => Object.values(catalogo.value?.marcas ?? {}));
const voces = computed(() => catalogo.value?.voces ?? []);
const FORMATOS = [
  { id: "16:9", titulo: "Horizontal 16:9", uso: "Computador, plataforma, proyector", icono: Monitor },
  { id: "9:16", titulo: "Vertical 9:16", uso: "Celular, Reels, TikTok", icono: Smartphone },
];

/** Guarda enseguida; si el servidor lo rechaza, vuelve a lo último que sí quedó guardado. */
async function guardar() {
  const antes = props.datos.trabajo;
  estado.value = "guardando";
  try {
    const nuevo = await api.patch<TrabajoCompleto>(`/api/trabajos/${antes.id}`, {
      marca: marca.value, voz: voz.value, formatos: formatos.value,
    });
    emit("actualizado", nuevo);
    estado.value = "guardado";
  } catch (e) {
    marca.value = antes.marca;
    voz.value = antes.voz;
    formatos.value = [...antes.formatos];
    estado.value = "";
    avisar((e as Error).message, "error");
  }
}

function pausarOtros(e: Event) {
  document.querySelectorAll("audio, video").forEach((m) => m !== e.target && (m as HTMLMediaElement).pause());
}
</script>

<template>
  <section aria-labelledby="titulo-marca" class="space-y-8">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div>
        <h2 id="titulo-marca" class="text-xl font-bold">Marca, voz y formato</h2>
        <p class="mt-1 text-sm text-suave">Los cambios se guardan solos.</p>
      </div>
      <p class="flex items-center gap-2 text-sm font-semibold" aria-live="polite">
        <template v-if="estado === 'guardando'"><LoaderCircle class="size-4 animate-spin text-acento" /> Guardando…</template>
        <template v-else-if="estado === 'guardado'"><CircleCheck class="size-4 text-exito" /> <span class="text-exito">Guardado</span></template>
      </p>
    </div>

    <fieldset>
      <legend class="mb-3 font-bold">¿De quién es el video?</legend>
      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <label v-for="m in marcas" :key="m.id"
          class="tarjeta relative flex cursor-pointer flex-col gap-3 p-4 transition hover:border-acento has-[:checked]:border-acento has-[:checked]:ring-2 has-[:checked]:ring-acento/40">
          <input v-model="marca" type="radio" name="marca" :value="m.id" class="absolute top-4 right-4 size-4 accent-[var(--c-acento)]" @change="guardar" />
          <span class="flex h-12 items-center">
            <span v-if="m.logo_url" class="rounded-md border border-borde px-2 py-1.5" :class="m.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
              <img :src="m.logo_url" alt="" class="h-7 max-w-[120px] object-contain" />
            </span>
          </span>
          <span class="font-bold">{{ m.nombre_corto }}</span>
          <span class="flex h-3 overflow-hidden rounded ring-1 ring-borde" aria-hidden="true">
            <i v-for="c in m.paleta.slice(0, 5)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
          </span>
        </label>
      </div>
    </fieldset>

    <fieldset>
      <legend class="mb-1 font-bold">¿Qué voz lo narra?</legend>
      <p class="mb-3 text-sm text-suave">Escucha las muestras antes de elegir.</p>
      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <label v-for="v in voces" :key="v.id"
          class="tarjeta relative flex cursor-pointer flex-col gap-2 p-4 transition hover:border-acento has-[:checked]:border-acento has-[:checked]:ring-2 has-[:checked]:ring-acento/40">
          <input v-model="voz" type="radio" name="voz" :value="v.id" class="absolute top-4 right-4 size-4 accent-[var(--c-acento)]" @change="guardar" />
          <span class="pr-6 font-bold">{{ v.nombre }}
            <span v-if="v.id === 'carlos'" class="ml-1 rounded-full bg-superficie-2 px-2 py-0.5 text-[11px] font-semibold text-suave">La de siempre</span>
          </span>
          <span class="text-xs text-suave">{{ v.proveedor }} · {{ v.descripcion }}</span>
          <span v-if="v.falta" class="text-xs font-semibold text-aviso">No se puede producir todavía: {{ v.falta }}</span>
          <span v-else-if="v.solo_borrador" class="text-xs font-semibold text-aviso">Solo borradores: no se puede entregar</span>
          <audio v-if="v.muestra_url" controls preload="none" :src="v.muestra_url" class="mt-auto h-9 w-full" @play="pausarOtros" />
          <span v-else class="mt-auto text-xs text-suave italic">Sin muestra para escuchar</span>
        </label>
      </div>
    </fieldset>

    <fieldset>
      <legend class="mb-3 font-bold">¿Dónde se va a ver?</legend>
      <div class="flex flex-wrap gap-3">
        <label v-for="f in FORMATOS" :key="f.id"
          class="tarjeta flex cursor-pointer items-center gap-4 px-4 py-3 transition hover:border-acento has-[:checked]:border-acento has-[:checked]:ring-2 has-[:checked]:ring-acento/40">
          <input v-model="formatos" type="checkbox" :value="f.id" class="size-4 accent-[var(--c-acento)]" @change="guardar" />
          <component :is="f.icono" class="size-6 text-acento" />
          <span><span class="block font-bold">{{ f.titulo }}</span><span class="block text-xs text-suave">{{ f.uso }}</span></span>
        </label>
      </div>
    </fieldset>
  </section>
</template>
