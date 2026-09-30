<script setup lang="ts">
import type { Component } from "vue";

/** `imagen`: una ilustración del banco de RiskMann (public/marca/banco/). Va sobre placa blanca, como en su app. */
defineProps<{ titulo: string; texto?: string; icono?: Component; imagen?: string }>();
</script>

<template>
  <div class="rounded-2xl border-2 border-dashed border-borde px-6 py-10 text-center">
    <span v-if="imagen" class="mx-auto mb-5 block w-fit rounded-2xl bg-white p-4 shadow-sm">
      <img :src="`/marca/banco/${imagen}`" alt="" class="h-32 w-auto object-contain" />
    </span>
    <component :is="icono" v-else-if="icono" class="mx-auto mb-3 size-9 text-suave" />
    <p class="font-semibold">{{ titulo }}</p>
    <p v-if="texto" class="mx-auto mt-1 max-w-md text-sm text-suave">{{ texto }}</p>
    <div v-if="$slots.default" class="mt-5 flex flex-wrap justify-center gap-2"><slot /></div>
  </div>
</template>
