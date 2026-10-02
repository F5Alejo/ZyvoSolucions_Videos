<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { Check, Plus } from "lucide-vue-next";
import { catalogo } from "../composables/catalogo";

const marca = defineModel<string>({ required: true });
const emit = defineEmits<{ cambio: [string] }>();
const ruta = useRoute();
const marcas = computed(() => Object.values(catalogo.value?.marcas ?? {}));

function elegir(id: string) {
  if (marca.value === id) return;
  marca.value = id;
  emit("cambio", id);
}
</script>

<template>
  <div class="grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-2" role="radiogroup" aria-label="Marca del curso">
    <button v-for="m in marcas" :key="m.id" type="button" role="radio" :aria-checked="marca === m.id" @click="elegir(m.id)"
      class="group relative flex items-center gap-4 rounded-2xl border-2 bg-superficie p-4 text-left transition"
      :class="marca === m.id ? 'border-acento shadow-md' : 'border-borde hover:border-acento/50 hover:shadow-sm'">
      <span class="grid h-16 w-24 shrink-0 place-items-center rounded-xl border border-borde"
            :class="m.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
        <img v-if="m.logo_url" :src="m.logo_url" alt="" class="max-h-10 max-w-20 object-contain" />
        <span v-else class="text-sm font-bold text-[#111]">{{ m.nombre_corto }}</span>
      </span>
      <span class="min-w-0 flex-1">
        <span class="block text-base font-bold">{{ m.nombre_corto }}</span>
        <span class="mt-0.5 line-clamp-2 text-xs text-suave">{{ m.que_es }}</span>
        <span class="mt-2 flex h-2 w-28 overflow-hidden rounded-full" aria-hidden="true">
          <i v-for="c in m.paleta.slice(0, 5)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
        </span>
      </span>
      <span class="grid size-6 shrink-0 place-items-center rounded-full border-2 transition"
            :class="marca === m.id ? 'border-acento bg-acento text-sobre-acento' : 'border-borde'">
        <Check v-if="marca === m.id" class="size-3.5" stroke-width="3" />
      </span>
    </button>
    <RouterLink :to="{ path: '/empresas/nueva', query: { volver: ruta.fullPath } }"
      class="flex items-center gap-4 rounded-2xl border-2 border-dashed border-borde p-4 text-suave transition hover:border-acento hover:text-acento">
      <span class="grid h-16 w-24 shrink-0 place-items-center rounded-xl bg-acento-suave text-acento"><Plus class="size-6" /></span>
      <span>
        <span class="block text-base font-bold">¿Tu empresa no está?</span>
        <span class="mt-0.5 block text-xs">Regístrala con su logo y sus colores</span>
      </span>
    </RouterLink>
  </div>
</template>
