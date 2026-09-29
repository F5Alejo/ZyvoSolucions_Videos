<script setup lang="ts">
import { VideoOff } from "lucide-vue-next";

defineProps<{ archivo: string; titulo: string; existe?: boolean; vertical?: boolean }>();

// Un solo video o audio sonando a la vez en toda la aplicación.
function alReproducir(e: Event) {
  document.querySelectorAll("video, audio").forEach((m) => m !== e.target && (m as HTMLMediaElement).pause());
}
</script>

<template>
  <figure class="min-w-0">
    <video v-if="existe !== false" controls preload="metadata" :src="`/media/entregables/${archivo}#t=3`" @play="alReproducir"
           class="w-full rounded-xl bg-black object-contain" :class="vertical === false ? 'aspect-video' : 'aspect-[9/16] max-h-[440px]'"
           :aria-label="titulo" />
    <div v-else class="grid w-full place-items-center rounded-xl border-2 border-dashed border-borde text-center text-sm text-suave"
         :class="vertical === false ? 'aspect-video' : 'aspect-[9/16] max-h-[440px]'">
      <span><VideoOff class="mx-auto mb-2 size-6" />No encontramos este archivo</span>
    </div>
    <figcaption class="mt-2">
      <span class="block text-sm font-semibold">{{ titulo }}</span>
      <span class="block truncate text-xs text-suave" :title="archivo">{{ archivo.split("/").pop() }}</span>
    </figcaption>
  </figure>
</template>
