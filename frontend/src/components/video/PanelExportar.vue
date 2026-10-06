<script setup lang="ts">
// Descargar lo producido: cada video, el curso completo, los subtítulos y el paquete con todo.
import { Captions, Download, FileArchive, Film } from "@lucide/vue";
import type { Produccion } from "../../tipos";

defineProps<{ trabajo: string; videos: { clave: string; titulo: string }[]; produccion: Produccion }>();
</script>

<template>
  <section class="tarjeta p-5" aria-labelledby="exportar">
    <h2 id="exportar" class="flex items-center gap-2 font-bold"><Download class="size-5 text-acento" /> Exportar</h2>
    <ul class="mt-3 divide-y divide-borde">
      <li v-if="produccion.completo?.archivos && videos.length > 1" class="flex flex-wrap items-center gap-3 py-3">
        <Film class="size-5 text-acento" />
        <span class="min-w-0 flex-1 font-semibold">Curso completo, con capítulos</span>
        <a class="boton-primario" :href="`${produccion.completo.archivos.mp4}?descargar=1`">Exportar MP4</a>
      </li>
      <li v-for="v in videos" :key="v.clave" class="flex flex-wrap items-center gap-3 py-3">
        <Film class="size-5 text-suave" />
        <span class="min-w-0 flex-1 truncate">{{ v.titulo }}</span>
        <template v-if="produccion.videos[v.clave]?.archivos">
          <a class="boton-fantasma" :href="`${produccion.videos[v.clave]!.archivos!.srt}?descargar=1`" title="Subtítulos para YouTube">
            <Captions class="size-4" /> Subtítulos</a>
          <a class="boton-secundario" :href="`${produccion.videos[v.clave]!.archivos!.mp4}?descargar=1`">Exportar MP4</a>
        </template>
        <span v-else class="text-sm text-suave">Todavía no está listo</span>
      </li>
    </ul>
    <a class="boton-fantasma mt-2" :href="`/api/trabajos/${trabajo}/paquete.zip`"><FileArchive class="size-4" /> Todo en un ZIP (videos, subtítulos e informes)</a>
  </section>
</template>
