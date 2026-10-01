<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Menu, X } from "@lucide/vue";
import BarraLateral from "./components/BarraLateral.vue";
import AvisosFlotantes from "./components/AvisosFlotantes.vue";
import DialogoConfirmar from "./components/DialogoConfirmar.vue";
import EstadoCarga from "./components/EstadoCarga.vue";
import { catalogo, cargarCatalogo } from "./composables/catalogo";

const ruta = useRoute();
const menuAbierto = ref(false);
const errorCatalogo = ref<string | null>(null);

function iniciar() {
  errorCatalogo.value = null;
  cargarCatalogo(true).catch((e: Error) => (errorCatalogo.value = e.message));
}
iniciar();
watch(() => ruta.fullPath, () => (menuAbierto.value = false));
</script>

<template>
  <a href="#contenido" class="sr-only z-50 rounded-lg bg-superficie px-4 py-2 text-acento focus:not-sr-only focus:fixed focus:left-3 focus:top-3">
    Saltar al contenido
  </a>

  <!-- Escritorio: barra lateral fija -->
  <aside class="fixed inset-y-0 left-0 hidden w-64 lg:block">
    <BarraLateral />
  </aside>

  <!-- Móvil: barra superior y menú deslizable -->
  <header class="sticky top-0 z-30 flex items-center justify-between border-b-2 border-dorado bg-lateral px-4 py-3 lg:hidden">
    <RouterLink to="/" class="flex items-center gap-2">
      <img src="/marca/riskmann_logo_blanco.png" alt="RiskMann by SOFU" class="h-7" />
      <span class="border-l border-white/30 pl-2 text-sm font-semibold text-white">Estudio de video</span>
    </RouterLink>
    <button class="rounded-lg p-2 text-white hover:bg-white/10" :aria-expanded="menuAbierto" aria-controls="menu-movil"
            aria-label="Abrir el menú" @click="menuAbierto = true">
      <Menu class="size-6" />
    </button>
  </header>
  <Transition enter-from-class="opacity-0" leave-to-class="opacity-0" enter-active-class="transition" leave-active-class="transition">
    <div v-if="menuAbierto" class="fixed inset-0 z-40 bg-black/50 lg:hidden" @click="menuAbierto = false" />
  </Transition>
  <Transition enter-from-class="-translate-x-full" leave-to-class="-translate-x-full" enter-active-class="transition-transform" leave-active-class="transition-transform">
    <div v-if="menuAbierto" id="menu-movil" class="fixed inset-y-0 left-0 z-50 w-72 max-w-[85vw] lg:hidden" role="dialog" aria-label="Menú">
      <BarraLateral />
      <button class="absolute right-3 top-4 rounded-lg p-2 text-white hover:bg-white/10" aria-label="Cerrar el menú" @click="menuAbierto = false">
        <X class="size-5" />
      </button>
    </div>
  </Transition>

  <main id="contenido" class="min-h-screen lg:pl-64">
    <div class="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-10 lg:py-10">
      <EstadoCarga v-if="!catalogo" :cargando="!errorCatalogo" :error="errorCatalogo" @reintentar="iniciar" />
      <RouterView v-else v-slot="{ Component }">
        <Transition mode="out-in" enter-from-class="opacity-0 translate-y-1" enter-active-class="transition duration-150">
          <component :is="Component" :key="ruta.path" />
        </Transition>
      </RouterView>
    </div>
  </main>

  <AvisosFlotantes />
  <DialogoConfirmar />
</template>
