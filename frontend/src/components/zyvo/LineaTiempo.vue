<script setup lang="ts">
// La línea de tiempo de un video: escenas, voz, música, efectos y subtítulos, sin código ni números técnicos.
import { computed } from "vue";
import type { LineaDeTiempo } from "../../tipos";
import { mmss } from "../../utils";

const props = defineProps<{ linea: LineaDeTiempo; elegida?: number | null }>();
defineEmits<{ elegir: [number] }>();

const total = computed(() => Math.max(props.linea.duracion, 0.1));
const pos = (inicio: number, fin?: number) => ({
  left: `${(100 * inicio) / total.value}%`,
  ...(fin !== undefined ? { width: `${Math.max(0.4, (100 * (fin - inicio)) / total.value)}%` } : {}),
});
const marcas = computed(() => {
  const paso = total.value > 120 ? 30 : total.value > 40 ? 10 : 5;
  return Array.from({ length: Math.floor(total.value / paso) + 1 }, (_, i) => i * paso);
});
</script>

<template>
  <section class="tarjeta p-4" aria-label="Línea de tiempo">
    <div class="mb-3 flex items-center justify-between text-sm">
      <p class="font-bold">Línea de tiempo</p>
      <p class="text-suave">{{ mmss(linea.duracion) }} · {{ linea.resuelto ? "tiempos reales" : "tiempos estimados" }}</p>
    </div>
    <div class="grid grid-cols-[88px_1fr] items-center gap-x-3 gap-y-2 text-xs">
      <span class="font-semibold text-suave">Escenas</span>
      <div class="relative h-9">
        <button v-for="(e, i) in linea.pistas.escenas" :key="e.id" type="button"
                class="absolute top-0 h-full truncate rounded-md border px-1.5 text-left font-semibold transition"
                :class="elegida === e.lamina ? 'border-acento bg-acento text-sobre-acento' : 'border-borde bg-superficie-2 hover:border-acento'"
                :style="pos(e.inicio, e.inicio + e.duracion)" :title="`${String(i + 1).padStart(2, '0')} · ${e.titulo}`"
                @click="$emit('elegir', e.lamina)">{{ String(i + 1).padStart(2, "0") }}</button>
      </div>

      <span class="font-semibold text-suave">Voz</span>
      <div class="relative h-4 rounded bg-superficie-2">
        <i v-for="(v, i) in linea.pistas.voz" :key="i" class="chispa absolute top-0 h-full rounded" :style="pos(v.inicio, v.fin)" :title="v.texto" />
      </div>

      <span class="font-semibold text-suave">Música</span>
      <div class="relative h-4 rounded bg-superficie-2">
        <i v-for="(m, i) in linea.pistas.musica" :key="i" class="absolute top-0 h-full rounded bg-dorado/70" :style="pos(m.inicio, m.fin)" :title="m.archivo" />
        <span v-if="!linea.pistas.musica.length" class="absolute inset-0 grid place-items-center text-[10px] text-suave">Sin música</span>
      </div>

      <span class="font-semibold text-suave">Efectos</span>
      <div class="relative h-4 rounded bg-superficie-2">
        <i v-for="(x, i) in linea.pistas.sfx" :key="i" class="absolute top-1/2 size-2.5 -translate-x-1/2 -translate-y-1/2 rotate-45 bg-entra"
           :style="pos(x.inicio)" :title="x.nombre" />
      </div>

      <span class="font-semibold text-suave">Subtítulos</span>
      <div class="relative h-4 rounded bg-superficie-2">
        <i v-for="(s, i) in linea.pistas.subtitulos" :key="i" class="absolute top-0 h-full rounded bg-exito/60" :style="pos(s.inicio, s.fin)" :title="s.texto" />
      </div>

      <span />
      <div class="relative h-4 text-[10px] text-suave">
        <span v-for="m in marcas" :key="m" class="absolute -translate-x-1/2" :style="pos(m)">{{ mmss(m) }}</span>
      </div>
    </div>
  </section>
</template>
