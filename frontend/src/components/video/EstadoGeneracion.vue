<script setup lang="ts">
// Mientras se crea el video: los pasos en lenguaje humano, el porcentaje y qué viene después.
import { computed } from "vue";
import { Check, Circle, LoaderCircle } from "@lucide/vue";
import { pasos } from "../../generacion";
import { MENSAJES } from "../../mensajes";
import type { VideoRender } from "../../tipos";

const props = defineProps<{ video: VideoRender | null; porcentaje: number; titulo?: string }>();
const lista = computed(() => pasos(props.video));
const enCola = computed(() => props.video?.estado === "en_cola");
</script>

<template>
  <section class="tarjeta overflow-hidden" aria-live="polite">
    <div class="chispa px-6 py-5 text-white">
      <p class="text-lg font-bold">{{ enCola ? MENSAJES.generar.enCola : MENSAJES.generar.enCurso }}</p>
      <p v-if="titulo" class="text-sm text-white/80">{{ titulo }}</p>
      <div class="mt-4 h-2.5 overflow-hidden rounded-full bg-white/25" role="progressbar" :aria-valuenow="porcentaje"
           aria-valuemin="0" aria-valuemax="100" aria-label="Avance">
        <div class="h-full rounded-full bg-white transition-[width] duration-700" :style="{ width: `${porcentaje}%` }" />
      </div>
      <p class="mt-1.5 text-right text-sm font-bold tabular-nums">{{ porcentaje }} %</p>
    </div>
    <ol class="grid gap-1 p-4 sm:grid-flow-col sm:grid-rows-3">
      <li v-for="p in lista" :key="p.id" class="flex items-center gap-3 rounded-lg px-3 py-2"
          :class="p.estado === 'actual' ? 'bg-acento-suave font-semibold text-acento' : p.estado === 'hecho' ? 'text-texto' : 'text-suave'">
        <Check v-if="p.estado === 'hecho'" class="size-4 text-exito" stroke-width="3" />
        <LoaderCircle v-else-if="p.estado === 'actual'" class="size-4 animate-spin" />
        <Circle v-else class="size-4" />
        {{ p.texto }}
      </li>
    </ol>
  </section>
</template>
