<script setup lang="ts">
import { computed, ref } from "vue";
import { Search, Upload } from "lucide-vue-next";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import TarjetaCurso from "../components/TarjetaCurso.vue";
import VacioCaja from "../components/VacioCaja.vue";
import type { TrabajoFila } from "../tipos";
import { normalizar } from "../utils";

const { datos, cargando, error, recargar } = useCarga(() => api.get<TrabajoFila[]>("/api/trabajos"));
const busqueda = ref("");
const visibles = computed(() => {
  const q = normalizar(busqueda.value);
  return (datos.value ?? []).filter((t) => !q || normalizar(t.nombre).includes(q));
});
</script>

<template>
  <div>
    <EncabezadoPagina titulo="Mis cursos" subtitulo="Los cursos que has creado a partir de tus presentaciones.">
      <template #acciones>
        <RouterLink to="/cursos/nuevo" class="boton-primario"><Upload class="size-4" /> Crear un curso</RouterLink>
      </template>
    </EncabezadoPagina>
  
    <EstadoCarga v-if="!datos" :cargando="cargando" :error="error" @reintentar="recargar()" />
    <template v-else>
      <VacioCaja v-if="!datos.length" imagen="sin-documentos.webp" titulo="Todavía no hay cursos" texto="Sube una presentación de PowerPoint para crear el primero.">
        <RouterLink to="/cursos/nuevo" class="boton-primario"><Upload class="size-4" /> Crear un curso</RouterLink>
      </VacioCaja>
      <template v-else>
        <div v-if="datos.length > 3" class="relative mb-5 max-w-md">
          <Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-suave" />
          <input v-model="busqueda" type="search" class="campo pl-9" placeholder="Buscar curso…" aria-label="Buscar curso" />
        </div>
        <div class="grid grid-cols-[minmax(0,1fr)] gap-3 md:grid-cols-2 xl:grid-cols-3">
          <TarjetaCurso v-for="t in visibles" :key="t.id" :curso="t" />
        </div>
        <p v-if="!visibles.length" class="py-8 text-center text-suave">Ningún curso coincide con «{{ busqueda }}».</p>
      </template>
    </template>
  </div>
</template>
