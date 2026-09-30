<script setup lang="ts">
import { computed } from "vue";
import { Play } from "lucide-vue-next";
import type { Marca } from "../tipos";
import { contraste, mmss, tintaLegible } from "../utils";

/**
 * Cómo se verá un video: fondo, logo y colores de la marca, con el texto siempre legible.
 * No es el render: es una vista previa del primer fotograma.
 */
const props = defineProps<{
  titulo: string;
  subtitulo?: string;
  numero?: number;
  segundos?: number;
  marca?: Marca;
  vertical?: boolean;
  /** Foto de fondo (public/marca/banco/): va bajo un degradado del color de la marca para que el texto se lea. */
  foto?: string;
}>();

const fondo = computed(() => props.marca?.paleta[0]?.hex ?? "#073D7A");
const paleta = computed(() => props.marca?.paleta.slice(1).map((c) => c.hex) ?? []);
/** Texto principal: blanco o casi negro, el que mejor se lea. */
const tinta = computed(() => tintaLegible(fondo.value));
/** Acento: el primer color de la marca que se distinga del fondo (≥ 3:1, suficiente para barras y rótulos grandes). */
const acento = computed(() => tintaLegible(fondo.value, paleta.value, 3));
const acentoTexto = computed(() => (contraste(acento.value, fondo.value) >= 4.5 ? acento.value : tinta.value));

/** «Módulo 1 · Una persona expuesta» → rótulo «Módulo 1» y título «Una persona expuesta». */
const partes = computed(() => {
  const i = props.titulo.indexOf(" · ");
  return i > 0 ? { rotulo: props.titulo.slice(0, i), titulo: props.titulo.slice(i + 3) } : { rotulo: "", titulo: props.titulo };
});

/** El logo va sobre una placa si su versión no se lee sobre este fondo. */
const placaLogo = computed(() => {
  const m = props.marca;
  if (!m?.logo_url) return null;
  const fondoOscuro = contraste("#FFFFFF", fondo.value) > contraste("#111111", fondo.value);
  if (m.logo?.fondo === "claro" && fondoOscuro) return "#FFFFFF";
  if (m.logo?.fondo === "oscuro" && !fondoOscuro) return "#0B0D0F";
  return "transparent";
});
</script>

<template>
  <div class="@container group relative isolate overflow-hidden rounded-xl text-left shadow-sm ring-1 ring-black/5"
       :class="vertical ? 'aspect-[9/16]' : 'aspect-video'" :style="{ background: fondo, color: tinta }"
       role="img" :aria-label="`Vista previa: ${titulo}`">
    <!-- Foto de fondo: el texto va sobre el degradado del color de la marca, que asegura su contraste -->
    <template v-if="foto">
      <img :src="`/marca/banco/${foto}`" alt="" class="absolute inset-0 -z-20 h-full w-full object-cover" />
      <div class="absolute inset-0 -z-10"
           :style="{ background: `linear-gradient(to top, ${fondo} 18%, ${fondo}d9 48%, ${fondo}40 100%)` }" />
    </template>
    <!-- Luz y los dos anillos: el motivo del manual de RiskMann, discreto -->
    <div class="absolute inset-0 -z-10 opacity-60"
         :style="{ background: `radial-gradient(120% 90% at 85% 10%, ${acento}33 0%, transparent 55%), linear-gradient(180deg, transparent 55%, #00000040 100%)` }" />
    <svg class="absolute -right-[18%] -bottom-[28%] -z-10 w-[70%] opacity-25" viewBox="0 0 100 100" aria-hidden="true">
      <circle cx="50" cy="50" r="44" fill="none" :stroke="acento" stroke-width="5" />
      <circle cx="50" cy="50" r="36" fill="none" :stroke="tinta" stroke-width="0.8" />
    </svg>

    <div class="flex h-full flex-col" :class="vertical ? 'p-[6cqw]' : 'p-[4.5cqw]'">
      <div class="flex items-start justify-between gap-2">
        <span v-if="numero" class="rounded-full px-[3cqw] py-[1cqw] text-[4.2cqw] leading-none font-bold"
              :style="{ background: `${acento}26`, color: acentoTexto }">Video {{ numero }}</span>
        <span v-if="placaLogo" class="ml-auto rounded-[1.5cqw] px-[2.2cqw] py-[1.4cqw]" :style="{ background: placaLogo }">
          <img :src="marca!.logo_url!" alt="" class="h-[7cqw] max-w-[30cqw] object-contain" />
        </span>
      </div>

      <div class="mt-auto">
        <span v-if="vertical" class="mb-[2.5cqw] block h-[1cqw] w-[12cqw] rounded-full" :style="{ background: acento }" />
        <p v-if="partes.rotulo" class="font-bold tracking-wide uppercase" :class="vertical ? 'text-[4.4cqw]' : 'text-[3.8cqw]'" :style="{ color: acentoTexto }">{{ partes.rotulo }}</p>
        <p class="font-bold leading-[1.15]" :class="vertical ? 'line-clamp-3 text-[9cqw]' : 'line-clamp-2 text-[6cqw]'">{{ partes.titulo }}</p>
        <p v-if="subtitulo" class="mt-[2cqw] opacity-80" :class="vertical ? 'line-clamp-3 text-[4.8cqw]' : 'line-clamp-1 text-[3.4cqw]'">{{ subtitulo }}</p>
      </div>

      <div class="flex items-center gap-[2.5cqw]" :class="vertical ? 'mt-[4cqw]' : 'mt-[2.5cqw]'">
        <span class="grid shrink-0 place-items-center rounded-full transition group-hover:scale-110" :class="vertical ? 'size-[8cqw]' : 'size-[6.5cqw]'"
              :style="{ background: tinta, color: fondo }" aria-hidden="true">
          <Play class="ml-[0.4cqw] size-[3.6cqw]" fill="currentColor" />
        </span>
        <span class="h-[0.9cqw] flex-1 overflow-hidden rounded-full" :style="{ background: `${tinta}33` }">
          <span class="block h-full w-1/4 rounded-full" :style="{ background: acento }" />
        </span>
        <span v-if="segundos" class="text-[3.8cqw] font-semibold tabular-nums">{{ mmss(segundos) }}</span>
      </div>
    </div>
  </div>
</template>
