<script setup lang="ts">
// Una escena en el editor: cómo se ve, qué dice la voz, su cámara y su transición, y «Regenerar escena».
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { LoaderCircle, RefreshCw, RotateCcw, Save } from "@lucide/vue";
import type { CatalogoEscena, Lamina } from "../../tipos";

const props = defineProps<{
  trabajo: string; lamina: Lamina; numero: number; formato: string; catalogo: CatalogoEscena;
  camara: string; transicion: string; ocupado: boolean;
}>();
const emit = defineEmits<{
  narracion: [string]; escena: [{ camara?: string; transicion?: string }]; regenerar: []; restaurar: [];
}>();

const texto = ref(props.lamina.notas);
watch(() => props.lamina.notas, (n) => (texto.value = n));
const cambiado = computed(() => texto.value.trim() !== props.lamina.notas.trim());

// Vista previa de la escena (la misma página que dibuja el motor), escalada a la tarjeta.
const [ancho, alto] = { "9:16": [1080, 1920], "1:1": [1080, 1080], "4:5": [1080, 1350] }[props.formato] ?? [1920, 1080];
const caja = ref<HTMLElement | null>(null);
const escala = ref(0.2);
let observador: ResizeObserver | undefined;
onMounted(() => {
  observador = new ResizeObserver(([e]) => { if (e) escala.value = e.contentRect.width / ancho; });
  if (caja.value) observador.observe(caja.value);
});
onUnmounted(() => observador?.disconnect());
const fuente = computed(() => `/api/trabajos/${props.trabajo}/escena/${props.lamina.n}?formato=${encodeURIComponent(props.formato)}&v=${props.lamina.notas.length}`);
</script>

<template>
  <article class="tarjeta grid gap-4 p-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
    <div ref="caja" class="relative w-full overflow-hidden rounded-lg bg-black" :style="{ aspectRatio: `${ancho} / ${alto}` }">
      <iframe :src="fuente" sandbox="allow-scripts" title="Vista previa de la escena" loading="lazy"
              class="pointer-events-none absolute top-0 left-0 origin-top-left border-0"
              :style="{ width: `${ancho}px`, height: `${alto}px`, transform: `scale(${escala})` }" />
      <span class="absolute top-2 left-2 rounded-md bg-black/60 px-2 py-0.5 text-xs font-bold text-white">{{ String(numero).padStart(2, "0") }}</span>
    </div>

    <div class="flex min-w-0 flex-col gap-3">
      <p class="truncate font-bold" :title="lamina.titulo">{{ lamina.titulo }}</p>
      <label class="block">
        <span class="etiqueta-campo">Lo que dice la voz</span>
        <textarea v-model="texto" rows="4" class="campo resize-y" :disabled="ocupado" />
      </label>
      <div class="flex flex-wrap gap-2">
        <button v-if="cambiado" class="boton-primario" :disabled="ocupado" @click="emit('narracion', texto.trim())"><Save class="size-4" /> Guardar texto</button>
        <button v-if="lamina.editada" class="boton-fantasma" :disabled="ocupado" @click="emit('restaurar')"><RotateCcw class="size-4" /> Volver al original</button>
      </div>
      <div class="grid gap-3 sm:grid-cols-2">
        <label class="block">
          <span class="etiqueta-campo">Movimiento</span>
          <select class="campo" :value="camara" :disabled="ocupado" @change="emit('escena', { camara: ($event.target as HTMLSelectElement).value })">
            <option v-for="c in catalogo.camaras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
        </label>
        <label class="block">
          <span class="etiqueta-campo">Paso a la siguiente</span>
          <select class="campo" :value="transicion" :disabled="ocupado" @change="emit('escena', { transicion: ($event.target as HTMLSelectElement).value })">
            <option v-for="x in catalogo.transiciones" :key="x.id" :value="x.id">{{ x.nombre }}</option>
          </select>
        </label>
      </div>
      <button class="boton-secundario mt-auto self-start" :disabled="ocupado" @click="emit('regenerar')">
        <LoaderCircle v-if="ocupado" class="size-4 animate-spin" /><RefreshCw v-else class="size-4" /> Regenerar esta escena
      </button>
    </div>
  </article>
</template>
