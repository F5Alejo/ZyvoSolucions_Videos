<script setup lang="ts">
import { computed } from "vue";
import { LayoutDashboard, Plus, Presentation, Film, Bell, Settings } from "@lucide/vue";
import { catalogo } from "../composables/catalogo";

const principal = [
  { a: "/", texto: "Inicio", icono: LayoutDashboard, exacto: true },
  { a: "/cursos", texto: "Cursos", icono: Presentation, exacto: false },
  { a: "/videos", texto: "Videos", icono: Film, exacto: false },
];
const marcas = computed(() => Object.values(catalogo.value?.marcas ?? {}));
const pendientes = computed(() => catalogo.value?.pendientes_abiertos ?? 0);
</script>

<template>
  <nav class="flex h-full flex-col overflow-y-auto border-r-2 border-dorado bg-lateral text-white" aria-label="Principal">
    <RouterLink to="/" class="flex items-center gap-3 px-5 pt-6 pb-5">
      <img src="/marca/riskmann_logo_blanco.png" alt="RiskMann by SOFU" class="h-9" />
      <span class="border-l border-white/30 pl-3 text-sm leading-tight font-semibold">Estudio<br />de video</span>
    </RouterLink>

    <div class="px-3">
      <RouterLink to="/cursos/nuevo"
        class="mb-4 flex items-center justify-center gap-2 rounded-lg bg-dorado px-4 py-2.5 text-sm font-bold text-[#1A1A1A] shadow-sm transition hover:brightness-110">
        <Plus class="size-4" stroke-width="2.5" /> Crear un curso
      </RouterLink>

      <ul class="space-y-0.5">
        <li v-for="e in principal" :key="e.a">
          <RouterLink :to="e.a" v-slot="{ href, navigate, isActive, isExactActive }" custom>
            <a :href="href" @click="navigate" :aria-current="(e.exacto ? isExactActive : isActive) ? 'page' : undefined"
               class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white/80 transition hover:bg-white/10 hover:text-white aria-[current=page]:bg-white/15 aria-[current=page]:text-white">
              <component :is="e.icono" class="size-[18px]" /> {{ e.texto }}
            </a>
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/pendientes"
             class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white/80 transition hover:bg-white/10 hover:text-white [&.router-link-active]:bg-white/15 [&.router-link-active]:text-white">
            <Bell class="size-[18px]" /> Pendientes
            <span v-if="pendientes" class="ml-auto rounded-full bg-dorado px-2 py-0.5 text-xs font-bold text-[#1A1A1A]"
                  :aria-label="`${pendientes} abiertos`">{{ pendientes }}</span>
          </RouterLink>
        </li>
      </ul>

      <p class="mt-6 mb-2 px-3 text-xs font-semibold tracking-wider text-white/50 uppercase">Marcas</p>
      <ul class="space-y-0.5">
        <li v-for="m in marcas" :key="m.id">
          <RouterLink :to="`/marcas/${m.id}`"
             class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-white/80 transition hover:bg-white/10 hover:text-white [&.router-link-active]:bg-white/15 [&.router-link-active]:text-white">
            <span class="flex h-3 w-6 overflow-hidden rounded-sm ring-1 ring-white/20" aria-hidden="true">
              <i v-for="c in m.paleta.slice(0, 3)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
            </span>
            {{ m.nombre_corto }}
          </RouterLink>
        </li>
      </ul>
    </div>

    <div class="mt-auto px-3 pt-6">
      <RouterLink to="/configuracion"
         class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white/80 transition hover:bg-white/10 hover:text-white [&.router-link-active]:bg-white/15 [&.router-link-active]:text-white">
        <Settings class="size-[18px]" /> Configuración
      </RouterLink>
    </div>
    <p class="px-6 py-5 text-xs text-white/40">RiskMann by SOFU</p>
  </nav>
</template>
