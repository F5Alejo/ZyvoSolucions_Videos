<script setup lang="ts">
import { ref } from "vue";
import { CircleCheck, LoaderCircle } from "lucide-vue-next";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import SelectorFormato from "../SelectorFormato.vue";
import SelectorMarca from "../SelectorMarca.vue";
import SelectorVoz from "../SelectorVoz.vue";
import type { TrabajoCompleto } from "../../tipos";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();

const marca = ref(props.datos.trabajo.marca);
const voz = ref(props.datos.trabajo.voz);
const formatos = ref([...props.datos.trabajo.formatos]);
const estado = ref<"" | "guardando" | "guardado">("");

/** Guarda enseguida; si el servidor lo rechaza, vuelve a lo último que sí quedó guardado. */
async function guardar() {
  const antes = props.datos.trabajo;
  estado.value = "guardando";
  try {
    emit("actualizado", await api.patch<TrabajoCompleto>(`/api/trabajos/${antes.id}`, { marca: marca.value, voz: voz.value, formatos: formatos.value }));
    estado.value = "guardado";
  } catch (e) {
    marca.value = antes.marca;
    voz.value = antes.voz;
    formatos.value = [...antes.formatos];
    estado.value = "";
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <div class="space-y-10">
    <p class="flex h-5 items-center justify-end gap-2 text-sm font-semibold" aria-live="polite">
      <template v-if="estado === 'guardando'"><LoaderCircle class="size-4 animate-spin text-acento" /> Guardando…</template>
      <template v-else-if="estado === 'guardado'"><CircleCheck class="size-4 text-exito" /><span class="text-exito">Cambios guardados</span></template>
      <template v-else><span class="font-normal text-suave">Los cambios se guardan solos</span></template>
    </p>
    <section aria-labelledby="a-marca">
      <h2 id="a-marca" class="text-xl font-bold">Marca</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Colores, logo y forma de hablar del video.</p>
      <SelectorMarca v-model="marca" @cambio="guardar" />
    </section>
    <section aria-labelledby="a-voz">
      <h2 id="a-voz" class="text-xl font-bold">Voz</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Toca ▶ para escuchar cada una.</p>
      <SelectorVoz v-model="voz" @cambio="guardar" />
    </section>
    <section aria-labelledby="a-formato">
      <h2 id="a-formato" class="text-xl font-bold">Dónde se verá</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Puedes elegir los dos.</p>
      <SelectorFormato v-model="formatos" @cambio="guardar" />
    </section>
  </div>
</template>
