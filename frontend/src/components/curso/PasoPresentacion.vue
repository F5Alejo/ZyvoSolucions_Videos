<script setup lang="ts">
import { computed, ref } from "vue";
import { FileText, Search, TriangleAlert } from "@lucide/vue";
import type { TrabajoCompleto } from "../../tipos";
import { mb, normalizar } from "../../utils";
import PanelAgentes from "./PanelAgentes.vue";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();
const t = computed(() => props.datos.trabajo);
const r = computed(() => props.datos.resumen);
const sinNotas = computed(() => t.value.laminas.filter((l) => !l.frases.length && !t.value.excluidas[String(l.n)]).length);

const busqueda = ref("");
const laminas = computed(() => {
  const q = normalizar(busqueda.value);
  return t.value.laminas.filter((l) => !q || normalizar(`${l.n} ${l.titulo} ${l.notas}`).includes(q));
});
</script>

<template>
  <section aria-labelledby="titulo-presentacion">
    <h2 id="titulo-presentacion" class="text-xl font-bold">Lo que entró</h2>
    <p class="mt-1 flex items-center gap-2 text-sm text-suave">
      <FileText class="size-4" />
      <template v-if="t.origen.tipo === 'pptx'">{{ t.origen.archivo }} · {{ mb(t.origen.bytes ?? 0) }}</template>
      <template v-else>{{ t.origen.nota }}</template>
    </p>

    <dl class="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div class="tarjeta p-4"><dt class="text-sm text-suave">Láminas</dt><dd class="cifra text-3xl">{{ t.laminas.length }}</dd></div>
      <div class="tarjeta p-4"><dt class="text-sm text-suave">Frases de guion</dt><dd class="cifra text-3xl">{{ r.frases }}</dd></div>
      <div class="tarjeta p-4"><dt class="text-sm text-suave">Palabras narradas</dt><dd class="cifra text-3xl">{{ r.palabras.toLocaleString("es-CO") }}</dd></div>
      <div class="tarjeta p-4" :class="sinNotas ? 'border-aviso bg-aviso-fondo' : ''">
        <dt class="flex items-center gap-1.5 text-sm" :class="sinNotas ? 'text-aviso' : 'text-suave'">
          <TriangleAlert v-if="sinNotas" class="size-4" /> Láminas sin notas
        </dt>
        <dd class="cifra text-3xl" :class="sinNotas ? 'text-aviso' : ''">{{ sinNotas }}</dd>
      </div>
    </dl>

    <div class="mt-8 flex flex-wrap items-end justify-between gap-3">
      <h3 class="font-bold">Las láminas, una por una</h3>
      <div class="relative w-full max-w-xs">
        <Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-suave" />
        <input v-model="busqueda" type="search" class="campo pl-9" placeholder="Buscar lámina…" aria-label="Buscar lámina" />
      </div>
    </div>
    <div class="tarjeta mt-3 overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="border-b border-borde text-left text-xs text-suave">
          <tr><th class="px-4 py-3 font-semibold">#</th><th class="px-4 py-3 font-semibold">Lámina</th><th class="px-4 py-3 text-right font-semibold">Frases</th></tr>
        </thead>
        <tbody>
          <tr v-for="l in laminas" :key="l.n" class="border-b border-borde last:border-0" :class="t.excluidas[String(l.n)] && 'text-suave'">
            <td class="px-4 py-2.5 align-top tabular-nums">{{ l.n }}</td>
            <td class="px-4 py-2.5">
              {{ l.titulo }}
              <span v-if="t.excluidas[String(l.n)]" class="mt-0.5 block text-xs">No va al video: {{ t.excluidas[String(l.n)] }}</span>
            </td>
            <td class="px-4 py-2.5 text-right align-top tabular-nums">
              <span v-if="l.frases.length">{{ l.frases.length }}</span>
              <span v-else-if="!t.excluidas[String(l.n)]" class="inline-flex items-center gap-1 font-semibold text-aviso"><TriangleAlert class="size-3.5" /> sin notas</span>
              <span v-else>—</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!laminas.length" class="p-6 text-center text-suave">Ninguna lámina coincide con «{{ busqueda }}».</p>
    </div>
    <div class="mt-6"><PanelAgentes :trabajo="t.id" donde="presentacion" @actualizado="(d) => emit('actualizado', d)" /></div>
  </section>
</template>
