<script setup lang="ts">
import { computed, ref } from "vue";
import { Building2, Plus, Search } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import type { EmpresaFila } from "../tipos";
import { cuenta, normalizar } from "../utils";

const { datos: empresas, cargando, error, recargar } = useCarga(() => api.get<EmpresaFila[]>("/api/empresas"));

const busqueda = ref("");
const visibles = computed(() => {
  const q = normalizar(busqueda.value.trim());
  const lista = [...(empresas.value ?? [])].sort((a, b) => Number(b.registrada) - Number(a.registrada) || a.nombre_corto.localeCompare(b.nombre_corto));
  return q ? lista.filter((e) => normalizar(`${e.nombre} ${e.nombre_corto} ${e.que_es}`).includes(q)) : lista;
});
</script>

<template>
  <div>
    <EncabezadoPagina titulo="Empresas" subtitulo="Cada empresa tiene su logo, sus colores y su voz. Sus cursos salen con esa identidad.">
      <template #acciones>
        <RouterLink to="/empresas/nueva" class="boton-primario px-5 py-3"><Plus class="size-4" stroke-width="2.75" /> Registrar empresa</RouterLink>
      </template>
    </EncabezadoPagina>

    <EstadoCarga v-if="!empresas" :cargando="cargando" :error="error" @reintentar="recargar()" />
    <template v-else>
      <label v-if="empresas.length > 4" class="relative mb-6 block max-w-md">
        <Search class="pointer-events-none absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-suave" aria-hidden="true" />
        <input v-model="busqueda" type="search" class="campo pl-10" placeholder="Buscar empresa" aria-label="Buscar empresa" />
      </label>

      <ul class="grid grid-cols-[minmax(0,1fr)] gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <li v-for="e in visibles" :key="e.id">
          <RouterLink :to="`/marcas/${e.id}`" class="tarjeta group flex h-full flex-col overflow-hidden transition hover:-translate-y-0.5 hover:shadow-lg">
            <span class="flex h-32 items-center justify-center overflow-hidden border-b border-borde px-8 py-5" :class="e.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
              <img v-if="e.logo_url" :src="e.logo_url" :alt="`Logo de ${e.nombre_corto}`" class="max-h-full max-w-full object-contain" />
              <span v-else class="grid size-16 place-items-center rounded-2xl text-2xl font-bold text-white" :style="{ background: e.paleta[0]?.hex ?? '#26367D' }">
                {{ e.nombre_corto.slice(0, 1).toUpperCase() }}
              </span>
            </span>
            <span class="flex flex-1 flex-col p-5">
              <span class="flex items-start justify-between gap-3">
                <span class="text-lg font-bold group-hover:text-acento">{{ e.nombre_corto }}</span>
                <span class="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold" :class="e.registrada ? 'bg-acento-suave text-acento' : 'bg-borde/60 text-suave'">
                  {{ e.registrada ? "Registrada" : "Marca base" }}
                </span>
              </span>
              <span v-if="e.que_es" class="mt-1 line-clamp-2 text-sm text-suave">{{ e.que_es }}</span>
              <span class="mt-auto flex items-center justify-between gap-3 pt-4">
                <span class="flex h-2.5 w-24 overflow-hidden rounded-full ring-1 ring-borde" aria-hidden="true">
                  <i v-for="c in e.paleta.slice(0, 6)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
                </span>
                <span class="text-xs text-suave">{{ cuenta(e.cursos, "curso") }} · {{ cuenta(e.videos, "video") }}</span>
              </span>
            </span>
          </RouterLink>
        </li>
        <li v-if="!busqueda">
          <RouterLink to="/empresas/nueva"
            class="flex h-full min-h-60 flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed border-borde p-6 text-center text-suave transition hover:border-acento hover:text-acento">
            <span class="grid size-12 place-items-center rounded-2xl bg-acento-suave text-acento"><Building2 class="size-6" /></span>
            <span class="font-bold">Registrar otra empresa</span>
            <span class="text-sm">Toma 1 minuto: nombre, logo y colores.</span>
          </RouterLink>
        </li>
      </ul>
      <p v-if="busqueda && !visibles.length" class="mt-6 text-suave">Ninguna empresa coincide con «{{ busqueda }}».</p>
    </template>
  </div>
</template>
