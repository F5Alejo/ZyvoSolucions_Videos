<script setup lang="ts">
import { computed } from "vue";
import { ArrowRight } from "@lucide/vue";
import { catalogo } from "../composables/catalogo";
import type { TrabajoFila } from "../tipos";
import { cuenta, fecha, mmss } from "../utils";

const props = defineProps<{ curso: TrabajoFila }>();
const marca = computed(() => catalogo.value?.marcas[props.curso.marca]);
</script>

<template>
  <RouterLink :to="`/cursos/${curso.id}`" class="tarjeta group relative flex flex-col overflow-hidden p-5 pt-6 transition hover:border-acento hover:shadow-md">
    <span class="absolute inset-x-0 top-0 h-1.5" aria-hidden="true"
          :style="{ background: `linear-gradient(90deg, ${marca?.paleta[0]?.hex}, ${marca?.paleta[1]?.hex})` }" />
    <span class="text-xs font-semibold text-suave">{{ marca?.nombre_corto }} · {{ curso.origen.tipo === "pptx" ? "Desde tu PPTX" : "Ejemplo real" }}</span>
    <span class="mt-1 line-clamp-2 font-bold group-hover:text-acento">{{ curso.nombre }}</span>
    <span class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-suave">
      <span>{{ cuenta(curso.laminas, "lámina") }}</span>
      <span>{{ cuenta(curso.videos, "video") }}</span>
      <span>{{ mmss(curso.segundos) }} min</span>
    </span>
    <span class="mt-4 flex items-center justify-between text-xs text-suave">
      {{ fecha(curso.creado) }}
      <span class="inline-flex items-center gap-1 text-sm font-semibold text-acento">Abrir <ArrowRight class="size-4 transition group-hover:translate-x-0.5" /></span>
    </span>
  </RouterLink>
</template>
