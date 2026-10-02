<script setup lang="ts">
import { computed } from "vue";
import { Check, MicOff } from "lucide-vue-next";
import { catalogo } from "../composables/catalogo";
import BotonMuestraVoz from "./BotonMuestraVoz.vue";

const voz = defineModel<string>({ required: true });
const emit = defineEmits<{ cambio: [string] }>();
const voces = computed(() => catalogo.value?.voces ?? []);

function elegir(id: string) {
  if (voz.value === id) return;
  voz.value = id;
  emit("cambio", id);
}
</script>

<template>
  <div class="grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-2" role="radiogroup" aria-label="Voz del curso">
    <!-- El botón de escuchar va al lado de la opción, no dentro: son dos acciones distintas. -->
    <div v-for="v in voces" :key="v.id" @click="elegir(v.id)"
         class="flex cursor-pointer items-center gap-4 rounded-2xl border-2 bg-superficie p-4 transition"
         :class="voz === v.id ? 'border-acento shadow-md' : 'border-borde hover:border-acento/50 hover:shadow-sm'">
      <BotonMuestraVoz v-if="v.muestra_url" :url="v.muestra_url" :nombre="v.nombre" />
      <span v-else class="grid size-12 shrink-0 place-items-center rounded-full bg-superficie-2 text-suave" title="Sin muestra para escuchar">
        <MicOff class="size-5" />
      </span>
      <div role="radio" tabindex="0" :aria-checked="voz === v.id" :aria-label="`${v.nombre}. ${v.descripcion}`"
           class="flex min-w-0 flex-1 items-center gap-3 rounded-lg outline-offset-4"
           @keydown.enter.prevent="elegir(v.id)" @keydown.space.prevent="elegir(v.id)">
        <span class="min-w-0 flex-1">
          <span class="flex flex-wrap items-center gap-2 font-bold">
            {{ v.nombre }}
            <span v-if="v.id === 'carlos'" class="rounded-full bg-exito-fondo px-2 py-0.5 text-[11px] font-semibold text-exito">Recomendada</span>
          </span>
          <span class="mt-0.5 line-clamp-2 text-xs text-suave">{{ v.descripcion }}</span>
          <span v-if="v.falta" class="mt-1 block text-xs font-semibold text-aviso">Todavía no se puede producir: {{ v.falta }}</span>
          <span v-else-if="v.solo_borrador" class="mt-1 block text-xs font-semibold text-aviso">Solo para borradores</span>
        </span>
        <span class="grid size-6 shrink-0 place-items-center rounded-full border-2 transition"
              :class="voz === v.id ? 'border-acento bg-acento text-sobre-acento' : 'border-borde'">
          <Check v-if="voz === v.id" class="size-3.5" stroke-width="3" />
        </span>
      </div>
    </div>
  </div>
</template>
