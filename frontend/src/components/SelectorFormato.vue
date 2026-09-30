<script setup lang="ts">
import { Check } from "lucide-vue-next";

const formatos = defineModel<string[]>({ required: true });
const emit = defineEmits<{ cambio: [string[]] }>();

const OPCIONES = [
  { id: "16:9", titulo: "Horizontal", detalle: "Computador, plataforma de cursos, proyector" },
  { id: "9:16", titulo: "Vertical", detalle: "Celular, Instagram, TikTok, WhatsApp" },
];

function alternar(id: string) {
  const nuevo = formatos.value.includes(id) ? formatos.value.filter((f) => f !== id) : [...formatos.value, id];
  formatos.value = nuevo;
  emit("cambio", nuevo);
}
</script>

<template>
  <div class="grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-2" role="group" aria-label="Formatos del video">
    <button v-for="o in OPCIONES" :key="o.id" type="button" role="checkbox" :aria-checked="formatos.includes(o.id)" @click="alternar(o.id)"
      class="flex items-center gap-5 rounded-2xl border-2 bg-superficie p-5 text-left transition"
      :class="formatos.includes(o.id) ? 'border-acento shadow-md' : 'border-borde hover:border-acento/50 hover:shadow-sm'">
      <!-- La forma del video, dibujada -->
      <span class="grid h-20 w-24 shrink-0 place-items-center" aria-hidden="true">
        <span class="relative rounded-lg border-[3px] transition"
              :class="[o.id === '16:9' ? 'h-12 w-20' : 'h-20 w-11', formatos.includes(o.id) ? 'border-acento bg-acento-suave' : 'border-suave/50']">
          <span class="absolute inset-x-2 bottom-2 h-1 rounded-full" :class="formatos.includes(o.id) ? 'bg-acento' : 'bg-suave/40'" />
        </span>
      </span>
      <span class="min-w-0 flex-1">
        <span class="block text-base font-bold">{{ o.titulo }} <span class="text-sm font-medium text-suave">{{ o.id }}</span></span>
        <span class="mt-0.5 block text-sm text-suave">{{ o.detalle }}</span>
      </span>
      <span class="grid size-6 shrink-0 place-items-center rounded-md border-2 transition"
            :class="formatos.includes(o.id) ? 'border-acento bg-acento text-sobre-acento' : 'border-borde'">
        <Check v-if="formatos.includes(o.id)" class="size-3.5" stroke-width="3" />
      </span>
    </button>
  </div>
</template>
