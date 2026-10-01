<script setup lang="ts">
import { ChevronRight } from "@lucide/vue";

defineProps<{ titulo: string; subtitulo?: string; migas?: { texto: string; a?: string }[] }>();
</script>

<template>
  <header class="mb-8">
    <nav v-if="migas?.length" aria-label="Estás en" class="mb-3 flex flex-wrap items-center gap-1 text-sm text-suave">
      <template v-for="(m, i) in migas" :key="i">
        <ChevronRight v-if="i" class="size-3.5" aria-hidden="true" />
        <RouterLink v-if="m.a" :to="m.a" class="hover:text-acento hover:underline">{{ m.texto }}</RouterLink>
        <span v-else aria-current="page">{{ m.texto }}</span>
      </template>
    </nav>
    <div class="flex flex-wrap items-start justify-between gap-4">
      <div class="min-w-0">
        <h1 class="text-2xl font-bold sm:text-3xl">{{ titulo }}</h1>
        <p v-if="subtitulo" class="mt-1.5 max-w-3xl text-suave">{{ subtitulo }}</p>
        <slot name="debajo" />
      </div>
      <div v-if="$slots.acciones" class="flex flex-wrap gap-2"><slot name="acciones" /></div>
    </div>
  </header>
</template>
