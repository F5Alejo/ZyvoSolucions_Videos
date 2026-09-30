<script setup lang="ts">
import { computed } from "vue";
import { catalogo } from "../composables/catalogo";
import type { Estado } from "../tipos";

const props = defineProps<{ estado: Estado }>();

const COLORES: Record<Estado, string> = {
  sin_estado: "bg-aviso-fondo text-aviso ring-aviso/30",
  borrador: "bg-superficie-2 text-suave ring-borde",
  revision: "bg-acento-suave text-entra ring-entra/30",
  aprobado: "bg-exito-fondo text-exito ring-exito/30",
  final: "bg-acento-suave text-acento ring-acento/30",
  archivado: "bg-superficie-2 text-suave ring-borde line-through decoration-1",
};
const texto = computed(() => catalogo.value?.estados[props.estado] ?? props.estado);
</script>

<template>
  <span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold whitespace-nowrap ring-1 ring-inset"
        :class="COLORES[estado]">
    <span class="size-1.5 rounded-full bg-current" aria-hidden="true" />{{ texto }}
  </span>
</template>
