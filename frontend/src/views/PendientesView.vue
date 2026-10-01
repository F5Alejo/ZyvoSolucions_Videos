<script setup lang="ts">
import { computed, ref } from "vue";
import { CircleCheck, FolderOpen } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { catalogo } from "../composables/catalogo";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import VacioCaja from "../components/VacioCaja.vue";
import type { Item, Proyecto } from "../tipos";
import { cuenta } from "../utils";

type Pendiente = Item & { marca: string; tipo: string };
const { datos, cargando, error, recargar } = useCarga(() =>
  api.get<{ pendientes: Pendiente[]; sin_estado: Proyecto[]; sin_registrar: string[] }>("/api/pendientes"));

const verCerrados = ref(false);
const tipo = ref<"" | "Pendiente" | "Pedir al cliente">("");
const grupos = computed(() => {
  const lista = (datos.value?.pendientes ?? []).filter((p) => (verCerrados.value || !p.hecho) && (!tipo.value || p.tipo === tipo.value));
  return Object.values(catalogo.value?.marcas ?? {})
    .map((m) => ({ marca: m, items: lista.filter((p) => p.marca === m.id) }))
    .filter((g) => g.items.length);
});
const abiertos = computed(() => datos.value?.pendientes.filter((p) => !p.hecho).length ?? 0);
</script>

<template>
  <EncabezadoPagina titulo="Pendientes" subtitulo="Lo que falta resolver con cada marca, y los videos que nadie ha revisado." />
  <EstadoCarga v-if="!datos" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="space-y-10">
    <section v-if="datos.sin_estado.length" aria-labelledby="titulo-sin-estado">
      <h2 id="titulo-sin-estado" class="text-lg font-bold">Videos sin estado · {{ datos.sin_estado.length }}</h2>
      <p class="mt-1 mb-3 text-sm text-suave">Nadie sabe en qué quedaron. Ábrelos y registra su estado.</p>
      <div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        <RouterLink v-for="p in datos.sin_estado" :key="p.id" :to="`/videos/${p.id}`"
                    class="tarjeta border-l-4 border-l-aviso p-3 transition hover:shadow-md">
          <span class="block font-semibold">{{ p.titulo }}</span>
          <span class="block text-xs text-suave">{{ catalogo?.marcas[p.marca]?.nombre_corto }} · {{ p.formato }}</span>
        </RouterLink>
      </div>
    </section>

    <section aria-labelledby="titulo-marcas">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 id="titulo-marcas" class="text-lg font-bold">Con las marcas · {{ abiertos }} abiertos</h2>
        <div class="flex flex-wrap items-center gap-2">
          <div class="flex rounded-lg border border-borde bg-superficie p-0.5 text-sm" role="group" aria-label="Tipo de pendiente">
            <button v-for="[v, t] in [['', 'Todos'], ['Pendiente', 'Del equipo'], ['Pedir al cliente', 'Pedir al cliente']] as const" :key="v"
                    class="rounded-md px-3 py-1.5 font-semibold transition" :class="tipo === v ? 'bg-acento text-sobre-acento' : 'text-suave hover:text-texto'"
                    :aria-pressed="tipo === v" @click="tipo = v">{{ t }}</button>
          </div>
          <label class="flex cursor-pointer items-center gap-2 text-sm text-suave">
            <input v-model="verCerrados" type="checkbox" class="size-4 accent-[var(--c-acento)]" /> Ver también los resueltos
          </label>
        </div>
      </div>
      <VacioCaja v-if="!grupos.length" :icono="CircleCheck" titulo="Nada pendiente con estos filtros" />
      <div class="grid grid-cols-[minmax(0,1fr)] gap-4 lg:grid-cols-2">
        <div v-for="g in grupos" :key="g.marca.id" class="tarjeta overflow-hidden">
          <RouterLink :to="`/marcas/${g.marca.id}`" class="flex items-center justify-between gap-3 border-b border-borde bg-superficie-2 px-4 py-3 hover:text-acento">
            <span class="flex items-center gap-2 font-bold">
              <span class="flex h-3 w-6 overflow-hidden rounded-sm" aria-hidden="true"><i v-for="c in g.marca.paleta.slice(0, 3)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" /></span>
              {{ g.marca.nombre_corto }}
            </span>
            <span class="text-xs text-suave">{{ cuenta(g.items.length, "pendiente") }}</span>
          </RouterLink>
          <ul class="divide-y divide-borde">
            <li v-for="p in g.items" :key="p.tipo + p.texto" class="flex gap-3 px-4 py-3 text-sm" :class="p.hecho && 'text-suave line-through'">
              <span class="mt-1.5 size-2 shrink-0 rounded-full" :class="p.hecho ? 'bg-exito' : p.tipo === 'Pendiente' ? 'bg-aviso' : 'bg-entra'" aria-hidden="true" />
              <span class="flex-1">{{ p.texto }}</span>
              <span class="shrink-0 text-xs text-suave">{{ p.tipo === "Pendiente" ? "Equipo" : "Cliente" }}</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section v-if="datos.sin_registrar.length" id="sin-registrar" aria-labelledby="titulo-sin-registrar">
      <h2 id="titulo-sin-registrar" class="flex items-center gap-2 text-lg font-bold"><FolderOpen class="size-5 text-suave" /> Carpetas sin registrar</h2>
      <p class="mt-1 mb-3 text-sm text-suave">Están en el repositorio de videos, pero ningún video del estudio las reclama. Hay que añadirlas a <code>datos/proyectos.json</code>.</p>
      <ul class="flex flex-wrap gap-2"><li v-for="c in datos.sin_registrar" :key="c"><code class="rounded bg-superficie-2 px-2 py-1 text-xs">videos/{{ c }}</code></li></ul>
    </section>
  </div>
</template>
