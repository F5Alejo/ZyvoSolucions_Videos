<script setup lang="ts">
// El reproductor grande del resultado, con la proporción del formato y los subtítulos.
import { computed } from "vue";

const props = defineProps<{ mp4: string; vtt?: string | null; formato?: string; titulo: string }>();
const proporcion = computed(() => ({ "9:16": "aspect-[9/16] max-h-[70vh]", "1:1": "aspect-square max-h-[70vh]",
  "4:5": "aspect-[4/5] max-h-[70vh]" })[props.formato ?? ""] ?? "aspect-video");

function alReproducir(e: Event) {
  document.querySelectorAll("video, audio").forEach((m) => m !== e.target && (m as HTMLMediaElement).pause());
}
</script>

<template>
  <figure class="mx-auto w-full" :class="formato && formato !== '16:9' ? 'max-w-md' : ''">
    <video :key="mp4" controls preload="metadata" :src="mp4" crossorigin="anonymous" class="w-full rounded-2xl bg-black object-contain shadow-xl"
           :class="proporcion" :aria-label="titulo" @play="alReproducir">
      <!-- Sin «default»: si los subtítulos ya van dentro de la imagen, se verían dos veces. -->
      <track v-if="vtt" kind="subtitles" srclang="es" label="Español" :src="vtt" />
    </video>
  </figure>
</template>
