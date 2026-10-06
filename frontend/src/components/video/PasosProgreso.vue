<script setup lang="ts">
// Dónde está la persona y cuánto falta: los pasos del flujo, con los ya hechos clicables.
import { Check } from "@lucide/vue";

const props = defineProps<{ pasos: { id: string; texto: string }[]; actual: string; hasta: number }>();
defineEmits<{ ir: [string] }>();
const posicion = (id: string) => props.pasos.findIndex((p) => p.id === id);
</script>

<template>
  <nav aria-label="Pasos para crear el video">
    <ol class="flex flex-wrap items-center gap-x-2 gap-y-3">
      <li v-for="(p, i) in pasos" :key="p.id" class="flex items-center gap-2">
        <button type="button" class="flex items-center gap-2 rounded-full py-1 pr-3 pl-1 text-sm font-semibold transition"
                :class="p.id === actual ? 'bg-acento text-sobre-acento shadow' : i <= hasta ? 'text-texto hover:bg-superficie-2' : 'cursor-default text-suave'"
                :disabled="i > hasta" :aria-current="p.id === actual ? 'step' : undefined" @click="$emit('ir', p.id)">
          <span class="grid size-6 place-items-center rounded-full text-xs"
                :class="p.id === actual ? 'bg-white/20' : i < posicion(actual) ? 'bg-exito text-white' : 'bg-superficie-2'">
            <Check v-if="i < posicion(actual)" class="size-3.5" stroke-width="3" /><template v-else>{{ i + 1 }}</template>
          </span>
          {{ p.texto }}
        </button>
        <span v-if="i < pasos.length - 1" class="h-px w-4 bg-borde" aria-hidden="true" />
      </li>
    </ol>
  </nav>
</template>
