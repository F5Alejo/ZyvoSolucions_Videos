<script setup lang="ts">
import { computed, onBeforeUnmount } from "vue";
import { Pause, Play } from "lucide-vue-next";
import { alternarMuestra, detenerMuestra, muestra } from "../composables/muestra";

const props = defineProps<{ url: string; nombre: string }>();

const esta = computed(() => muestra.url === props.url);
const sonando = computed(() => esta.value && muestra.sonando);
const C = 2 * Math.PI * 22;

onBeforeUnmount(() => { if (esta.value) detenerMuestra(); });
</script>

<template>
  <button type="button" class="relative grid size-12 shrink-0 place-items-center rounded-full bg-acento text-sobre-acento shadow-sm transition hover:scale-105"
          :aria-label="sonando ? `Pausar la muestra de ${nombre}` : `Escuchar a ${nombre}`" :aria-pressed="sonando"
          @click.stop.prevent="alternarMuestra(url)">
    <svg class="absolute inset-0 -rotate-90" viewBox="0 0 48 48" aria-hidden="true">
      <template v-if="esta">
        <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-opacity=".25" stroke-width="3" />
        <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"
                :stroke-dasharray="C" :stroke-dashoffset="C * (1 - muestra.avance)" />
      </template>
    </svg>
    <Pause v-if="sonando" class="size-5" fill="currentColor" />
    <Play v-else class="ml-0.5 size-5" fill="currentColor" />
  </button>
</template>
