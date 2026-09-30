<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowDownUp, Search, TriangleAlert, X } from "lucide-vue-next";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { catalogo } from "../composables/catalogo";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import EstadoChip from "../components/EstadoChip.vue";
import VacioCaja from "../components/VacioCaja.vue";
import type { Estado, Proyecto } from "../tipos";
import { cuenta, normalizar } from "../utils";

const ruta = useRoute();
const router = useRouter();
const { datos, cargando, error, recargar } = useCarga(() =>
  api.get<{ proyectos: Proyecto[]; carpetas: number; sin_registrar: string[] }>("/api/proyectos"));

// Los filtros viven en la dirección: se pueden compartir y sobreviven a recargar.
const q = (k: string) => (typeof ruta.query[k] === "string" ? (ruta.query[k] as string) : "");
const estado = computed(() => q("estado"));
const marca = computed(() => q("marca"));
const familia = computed(() => q("familia"));
const atencion = computed(() => q("atencion") === "1");
function filtrar(cambios: Record<string, string | undefined>) {
  const query = { ...ruta.query, ...cambios };
  for (const k of Object.keys(query)) if (!query[k]) delete query[k];
  router.replace({ query });
}
const hayFiltros = computed(() => !!(estado.value || marca.value || familia.value || atencion.value || busqueda.value));
function limpiar() { busqueda.value = ""; router.replace({ query: {} }); }

const busqueda = ref("");
const orden = ref<{ campo: "titulo" | "marca" | "estado"; asc: boolean }>({ campo: "estado", asc: true });
const ORDEN_ESTADO: Estado[] = ["sin_estado", "revision", "borrador", "aprobado", "final", "archivado"];

const todos = computed(() => datos.value?.proyectos ?? []);
const conteo = computed(() => {
  const c: Partial<Record<Estado, number>> = {};
  for (const p of todos.value.filter((p) => (!marca.value || p.marca === marca.value) && (!familia.value || p.familia === familia.value)))
    c[p.estado] = (c[p.estado] ?? 0) + 1;
  return c;
});
const filas = computed(() => {
  const b = normalizar(busqueda.value);
  const lista = todos.value.filter((p) =>
    (!estado.value || p.estado === estado.value) &&
    (!atencion.value || p.estado === "sin_estado" || p.estado === "revision") &&
    (!marca.value || p.marca === marca.value) &&
    (!familia.value || p.familia === familia.value) &&
    (!b || normalizar(`${p.titulo} ${p.formato} ${p.id}`).includes(b)));
  const clave = (p: Proyecto) =>
    orden.value.campo === "estado" ? String(ORDEN_ESTADO.indexOf(p.estado))
    : orden.value.campo === "marca" ? (catalogo.value?.marcas[p.marca]?.nombre_corto ?? p.marca) : p.titulo;
  return [...lista].sort((a, z) => clave(a).localeCompare(clave(z), "es") * (orden.value.asc ? 1 : -1));
});
function ordenar(campo: typeof orden.value.campo) {
  orden.value = { campo, asc: orden.value.campo === campo ? !orden.value.asc : true };
}
</script>

<template>
  <div>
    <EncabezadoPagina titulo="Videos" subtitulo="Todos los videos hechos para las cuatro marcas y en qué punto está cada uno." />
  
    <EstadoCarga v-if="!datos" :cargando="cargando" :error="error" @reintentar="recargar()" />
    <template v-else>
      <!-- Estados -->
      <div class="mb-4 flex flex-wrap gap-2" role="group" aria-label="Filtrar por estado">
        <button class="rounded-full border px-3 py-1.5 text-sm font-semibold transition"
                :class="!estado && !atencion ? 'border-acento bg-acento text-sobre-acento' : 'border-borde bg-superficie hover:border-acento'"
                :aria-pressed="!estado && !atencion" @click="filtrar({ estado: undefined, atencion: undefined })">
          Todos <span class="ml-1 opacity-75">{{ Object.values(conteo).reduce((a, b) => a + (b ?? 0), 0) }}</span>
        </button>
        <button v-if="(conteo.sin_estado ?? 0) + (conteo.revision ?? 0)"
                class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-semibold transition"
                :class="atencion ? 'border-aviso bg-aviso text-white' : 'border-aviso/40 bg-aviso-fondo text-aviso hover:border-aviso'"
                :aria-pressed="atencion" @click="filtrar({ atencion: atencion ? undefined : '1', estado: undefined })">
          <TriangleAlert class="size-3.5" /> Necesitan atención <span class="opacity-75">{{ (conteo.sin_estado ?? 0) + (conteo.revision ?? 0) }}</span>
        </button>
        <template v-for="(txt, e) in catalogo?.estados" :key="e">
          <button v-if="conteo[e]" class="rounded-full border px-3 py-1.5 text-sm font-semibold transition"
                  :class="estado === e ? 'border-acento bg-acento text-sobre-acento' : 'border-borde bg-superficie hover:border-acento'"
                  :aria-pressed="estado === e" @click="filtrar({ estado: estado === e ? undefined : e, atencion: undefined })">
            {{ txt }} <span class="ml-1 opacity-75">{{ conteo[e] }}</span>
          </button>
        </template>
      </div>
  
      <!-- Búsqueda, marca y tipo -->
      <div class="mb-4 flex flex-wrap items-end gap-3">
        <div class="relative min-w-[240px] flex-1">
          <Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-suave" />
          <input v-model="busqueda" type="search" class="campo pl-9" placeholder="Buscar video…" aria-label="Buscar video" />
        </div>
        <label class="w-40">
          <span class="etiqueta-campo">Marca</span>
          <select class="campo" :value="marca" @change="filtrar({ marca: ($event.target as HTMLSelectElement).value })">
            <option value="">Todas</option>
            <option v-for="m in catalogo?.marcas" :key="m.id" :value="m.id">{{ m.nombre_corto }}</option>
          </select>
        </label>
        <label class="w-40">
          <span class="etiqueta-campo">Tipo</span>
          <select class="campo" :value="familia" @change="filtrar({ familia: ($event.target as HTMLSelectElement).value })">
            <option value="">Todos</option>
            <option v-for="(txt, f) in catalogo?.familias" :key="f" :value="f">{{ txt }}</option>
          </select>
        </label>
        <button v-if="hayFiltros" class="boton-fantasma" @click="limpiar"><X class="size-4" /> Quitar filtros</button>
      </div>
  
      <VacioCaja v-if="!filas.length" imagen="sin-novedades.webp" titulo="No hay videos con estos filtros">
        <button class="boton-secundario" @click="limpiar">Quitar filtros</button>
      </VacioCaja>
      <div v-else class="tarjeta overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="border-b border-borde text-left text-xs text-suave">
            <tr>
              <th class="px-4 py-3"><button class="inline-flex items-center gap-1 font-semibold hover:text-texto" @click="ordenar('titulo')">Video <ArrowDownUp class="size-3" /></button></th>
              <th class="px-4 py-3"><button class="inline-flex items-center gap-1 font-semibold hover:text-texto" @click="ordenar('marca')">Marca <ArrowDownUp class="size-3" /></button></th>
              <th class="hidden px-4 py-3 font-semibold md:table-cell">Tipo</th>
              <th class="hidden px-4 py-3 font-semibold sm:table-cell">Duración</th>
              <th class="px-4 py-3"><button class="inline-flex items-center gap-1 font-semibold hover:text-texto" @click="ordenar('estado')">Estado <ArrowDownUp class="size-3" /></button></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in filas" :key="p.id" class="group cursor-pointer border-b border-borde transition last:border-0 hover:bg-acento-suave/50"
                @click="router.push(`/videos/${p.id}`)">
              <td class="px-4 py-3">
                <RouterLink :to="`/videos/${p.id}`" class="font-semibold group-hover:text-acento" @click.stop>{{ p.titulo }}</RouterLink>
                <span class="block text-xs text-suave">{{ p.formato }}</span>
              </td>
              <td class="px-4 py-3">{{ catalogo?.marcas[p.marca]?.nombre_corto }}</td>
              <td class="hidden px-4 py-3 md:table-cell">{{ catalogo?.familias[p.familia] }}</td>
              <td class="hidden px-4 py-3 tabular-nums sm:table-cell">{{ p.duracion ?? "—" }}</td>
              <td class="px-4 py-3"><EstadoChip :estado="p.estado" /></td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="mt-3 text-sm text-suave">
        {{ cuenta(filas.length, "video") }}
        <template v-if="datos.sin_registrar.length">
          · <RouterLink to="/pendientes#sin-registrar" class="text-acento hover:underline">{{ cuenta(datos.sin_registrar.length, "carpeta") }} del repositorio sin registrar</RouterLink>
        </template>
      </p>
    </template>
  </div>
</template>
