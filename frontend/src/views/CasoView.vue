<script setup lang="ts">
import { ArrowDown, ArrowRight, ExternalLink, FileText } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { catalogo } from "../composables/catalogo";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import EstadoChip from "../components/EstadoChip.vue";
import ReproductorVideo from "../components/ReproductorVideo.vue";
import type { Caso } from "../tipos";

const props = defineProps<{ id: string }>();
const { datos: c, cargando, error, recargar } = useCarga(() => api.get<Caso>(`/api/casos/${props.id}`), () => props.id);
</script>

<template>
  <EstadoCarga v-if="!c" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else>
    <EncabezadoPagina :titulo="c.titulo" :subtitulo="c.resumen"
      :migas="[{ texto: 'Inicio', a: '/' }, { texto: catalogo?.marcas[c.marca]?.nombre_corto ?? c.marca, a: `/marcas/${c.marca}` }, { texto: c.titulo }]" />

    <section class="grid items-stretch gap-3 lg:grid-cols-[1fr_auto_1.3fr_auto_1fr]" aria-label="Recorrido de la pieza">
      <div class="tarjeta border-t-4 border-t-entra p-5">
        <p class="text-xs font-bold tracking-wider text-entra uppercase">Entra</p>
        <ul class="mt-3 space-y-3 text-sm">
          <li v-for="e in c.entra" :key="e.tipo">
            <strong class="block">{{ e.tipo }}</strong>
            <a v-if="e.url" :href="e.url" target="_blank" rel="noopener" class="text-acento hover:underline">{{ e.texto }} <ExternalLink class="inline size-3" /></a>
            <span v-else class="text-suave">{{ e.texto }}</span>
          </li>
        </ul>
      </div>
      <ArrowRight class="hidden size-6 self-center text-suave lg:block" aria-hidden="true" /><ArrowDown class="mx-auto size-6 text-suave lg:hidden" aria-hidden="true" />
      <div class="tarjeta border-t-4 border-t-motor p-5">
        <p class="text-xs font-bold tracking-wider text-motor uppercase">El proceso</p>
        <ol class="mt-3 list-decimal space-y-1.5 pl-5 text-sm">
          <li v-for="p in c.motor" :key="p">{{ p }}</li>
        </ol>
        <a v-if="c.documento_url" :href="c.documento_url" target="_blank" class="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-acento hover:underline">
          <FileText class="size-4" /> Documento del proyecto
        </a>
      </div>
      <ArrowRight class="hidden size-6 self-center text-suave lg:block" aria-hidden="true" /><ArrowDown class="mx-auto size-6 text-suave lg:hidden" aria-hidden="true" />
      <div class="tarjeta border-t-4 border-t-exito p-5">
        <p class="text-xs font-bold tracking-wider text-exito uppercase">Sale</p>
        <p class="mt-2"><span class="cifra text-3xl">{{ c.videos.length }}</span> <span class="text-sm text-suave">videos</span></p>
        <ul class="mt-3 space-y-2">
          <li v-for="p in c.salida" :key="p.id" class="flex flex-wrap items-center gap-2 text-sm">
            <RouterLink :to="`/videos/${p.id}`" class="font-semibold text-acento hover:underline">{{ p.titulo }}</RouterLink>
            <EstadoChip :estado="p.estado" />
          </li>
        </ul>
      </div>
    </section>

    <h2 class="mt-10 mb-4 text-lg font-bold">Los videos</h2>
    <div class="grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4">
      <ReproductorVideo v-for="e in c.videos" :key="e.archivo" :archivo="e.archivo" :titulo="e.nota" />
    </div>
  </div>
</template>
