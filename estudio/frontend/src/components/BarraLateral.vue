<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Bell, ChevronDown, CircleHelp, Film, House, Moon, Plus, Presentation, Sun, Users } from "lucide-vue-next";
import { catalogo } from "../composables/catalogo";
import { abrirAyuda } from "../composables/ayuda";
import { cambiarTema, tema } from "../composables/tema";

const ruta = useRoute();
const marcas = computed(() => Object.values(catalogo.value?.marcas ?? {}));
const pendientes = computed(() => catalogo.value?.pendientes_abiertos ?? 0);

// «Equipo de producción» va plegado: quien solo crea cursos no lo necesita.
// Se abre solo en sus páginas y recuerda si la persona lo dejó abierto.
const CLAVE = "estudio.equipo-abierto";
const esDelEquipo = computed(() => /^\/(videos|pendientes|marcas|casos)/.test(ruta.path));
const equipoAbierto = ref(leer() || esDelEquipo.value);
watch(esDelEquipo, (si) => { if (si) equipoAbierto.value = true; });
function leer() { try { return localStorage.getItem(CLAVE) === "1"; } catch { return false; } }
function alternarEquipo() {
  equipoAbierto.value = !equipoAbierto.value;
  try { localStorage.setItem(CLAVE, equipoAbierto.value ? "1" : "0"); } catch { /* sin almacenamiento */ }
}

const enlace = "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-white/80 transition hover:bg-white/10 hover:text-white";
const activo = "bg-white/15 text-white";
</script>

<template>
  <nav class="flex h-full flex-col overflow-y-auto border-r-2 border-dorado bg-lateral text-white" aria-label="Principal">
    <RouterLink to="/" class="flex items-center gap-3 px-5 pt-6 pb-6">
      <img src="/marca/riskmann_logo_blanco.png" alt="RiskMann by SOFU" class="h-9" />
      <span class="border-l border-white/30 pl-3 text-sm leading-tight font-semibold">Estudio<br />de video</span>
    </RouterLink>

    <div class="flex flex-1 flex-col px-3">
      <RouterLink to="/cursos/nuevo"
        class="mb-5 flex items-center justify-center gap-2 rounded-xl bg-dorado px-4 py-3 text-sm font-bold text-[#1A1A1A] shadow-lg shadow-black/20 transition hover:-translate-y-px hover:brightness-110">
        <Plus class="size-4" stroke-width="2.75" /> Crear un curso
      </RouterLink>

      <ul class="space-y-1">
        <li>
          <RouterLink to="/" :class="[enlace, ruta.path === '/' && activo]" :aria-current="ruta.path === '/' ? 'page' : undefined">
            <House class="size-[18px]" /> Inicio
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/cursos" :class="[enlace, ruta.path.startsWith('/cursos') && ruta.path !== '/cursos/nuevo' && activo]"
                      :aria-current="ruta.path === '/cursos' ? 'page' : undefined">
            <Presentation class="size-[18px]" /> Mis cursos
          </RouterLink>
        </li>
      </ul>

      <!-- Herramientas del equipo de producción -->
      <div class="mt-6 border-t border-white/10 pt-4">
        <button type="button" class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-[11px] font-semibold tracking-wider whitespace-nowrap text-white/55 uppercase transition hover:text-white"
                :aria-expanded="equipoAbierto" aria-controls="menu-equipo" @click="alternarEquipo">
          <Users class="size-4" /> Equipo de producción
          <ChevronDown class="ml-auto size-4 transition" :class="equipoAbierto && 'rotate-180'" />
        </button>
        <ul v-show="equipoAbierto" id="menu-equipo" class="mt-1 space-y-1">
          <li>
            <RouterLink to="/videos" :class="[enlace, ruta.path.startsWith('/videos') && activo]"><Film class="size-[18px]" /> Videos</RouterLink>
          </li>
          <li>
            <RouterLink to="/pendientes" :class="[enlace, ruta.path === '/pendientes' && activo]">
              <Bell class="size-[18px]" /> Pendientes
              <span v-if="pendientes" class="ml-auto rounded-full bg-dorado px-2 py-0.5 text-xs font-bold text-[#1A1A1A]"
                    :aria-label="`${pendientes} abiertos`">{{ pendientes }}</span>
            </RouterLink>
          </li>
          <li v-for="m in marcas" :key="m.id">
            <RouterLink :to="`/marcas/${m.id}`" :class="[enlace, 'py-2', ruta.path === `/marcas/${m.id}` && activo]">
              <span class="flex h-3 w-[18px] overflow-hidden rounded-sm ring-1 ring-white/20" aria-hidden="true">
                <i v-for="c in m.paleta.slice(0, 3)" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
              </span>
              Marca {{ m.nombre_corto }}
            </RouterLink>
          </li>
        </ul>
      </div>

      <div class="mt-auto pt-6 pb-5">
        <button type="button" :class="[enlace, 'w-full']" @click="abrirAyuda()">
          <CircleHelp class="size-[18px]" /> Ayuda
        </button>
        <!-- Tema: los dos modos del manual de RiskMann -->
        <div class="mt-2 flex rounded-lg bg-white/10 p-1 text-xs font-semibold" role="radiogroup" aria-label="Tema de la página">
          <button v-for="o in ([{ id: 'oscuro', texto: 'Oscuro', icono: Moon }, { id: 'claro', texto: 'Claro', icono: Sun }] as const)" :key="o.id"
                  type="button" role="radio" :aria-checked="tema === o.id" @click="cambiarTema(o.id)"
                  class="flex flex-1 items-center justify-center gap-1.5 rounded-md py-1.5 transition"
                  :class="tema === o.id ? 'bg-white text-[#020202] shadow' : 'text-white/70 hover:text-white'">
            <component :is="o.icono" class="size-3.5" /> {{ o.texto }}
          </button>
        </div>
        <p class="mt-3 px-3 text-xs text-white/40">RiskMann by SOFU</p>
      </div>
    </div>
  </nav>
</template>
