<script setup lang="ts">
import { computed } from "vue";
import { catalogo } from "../composables/catalogo";
import type { TrabajoFila } from "../tipos";
import { cuenta, fecha, mmss } from "../utils";
import VistaPreviaVideo from "./VistaPreviaVideo.vue";

const props = defineProps<{ curso: TrabajoFila }>();
const marca = computed(() => catalogo.value?.marcas[props.curso.marca]);
</script>

<template>
  <RouterLink :to="`/cursos/${curso.id}`" class="tarjeta group flex flex-col overflow-hidden rounded-2xl transition hover:-translate-y-0.5 hover:border-acento hover:shadow-lg">
    <div class="p-3 pb-0"><VistaPreviaVideo :titulo="curso.nombre" :segundos="curso.segundos" :marca="marca" /></div>
    <div class="flex flex-1 flex-col p-4">
      <span class="text-xs font-semibold text-suave">{{ marca?.nombre_corto }} · {{ fecha(curso.creado) }}</span>
      <span class="mt-1 line-clamp-2 font-bold group-hover:text-acento">{{ curso.nombre }}</span>
      <span class="mt-auto pt-3 text-sm text-suave">{{ cuenta(curso.videos, "video") }} · {{ mmss(curso.segundos) }} min</span>
    </div>
  </RouterLink>
</template>
