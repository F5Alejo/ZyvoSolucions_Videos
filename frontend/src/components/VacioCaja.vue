<script setup lang="ts">
import type { Component } from "vue";

defineProps<{ titulo: string; texto?: string; icono?: Component }>();
</script>

<template>
  <div class="rounded-xl border-2 border-dashed border-borde px-6 py-10 text-center">
    <component :is="icono" v-if="icono" class="mx-auto mb-3 size-9 text-suave" />
    <p class="font-semibold">{{ titulo }}</p>
    <p v-if="texto" class="mx-auto mt-1 max-w-md text-sm text-suave">{{ texto }}</p>
    <div v-if="$slots.default" class="mt-5 flex flex-wrap justify-center gap-2"><slot /></div>
  </div>
</template>
