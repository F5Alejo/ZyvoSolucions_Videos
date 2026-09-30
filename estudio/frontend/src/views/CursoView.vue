<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { LayoutDashboard, ListChecks, SlidersHorizontal } from "lucide-vue-next";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import { confirmar } from "../composables/confirmar";
import EstadoCarga from "../components/EstadoCarga.vue";
import PasoAjustes from "../components/curso/PasoAjustes.vue";
import PasoGuion from "../components/curso/PasoGuion.vue";
import PasoResumen from "../components/curso/PasoResumen.vue";
import type { TrabajoCompleto } from "../tipos";
import { cuenta, fecha, mmss } from "../utils";

const props = defineProps<{ id: string }>();
const ruta = useRoute();
const router = useRouter();
const { datos: d, cargando, error, recargar } = useCarga(() => api.get<TrabajoCompleto>(`/api/trabajos/${props.id}`), () => props.id);

type Vista = "resumen" | "guion" | "ajustes";
const vista = computed<Vista>(() => (["guion", "ajustes"].includes(ruta.query.vista as string) ? ruta.query.vista : "resumen") as Vista);
const videoInicial = computed(() => (ruta.query.video !== undefined ? Number(ruta.query.video) : undefined));
const soloRevisar = computed(() => ruta.query.revisar === "1");

/** Cambia de pestaña. Desde el Resumen se puede llegar a un video concreto o a lo que hay que revisar. */
function ir(v: Vista, video?: number, revisar?: boolean) {
  const query: Record<string, string> = v === "resumen" ? {} : { vista: v };
  if (video !== undefined) query.video = String(video);
  if (revisar) query.revisar = "1";
  router.push({ query });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

const porRevisar = computed(() => d.value?.resumen.chequeos.filter((c) => c.ok !== true).length ?? 0);
const marca = computed(() => (d.value ? catalogo.value?.marcas[d.value.trabajo.marca] : undefined));

async function eliminar() {
  if (!d.value) return;
  const si = await confirmar({
    titulo: `¿Eliminar «${d.value.trabajo.nombre}»?`,
    texto: "Se borra también la presentación que subiste. No se puede deshacer.",
    aceptar: "Eliminar curso",
    peligro: true,
  });
  if (!si) return;
  try {
    await api.delete(`/api/trabajos/${props.id}`);
    avisar("El curso se eliminó.");
    router.push("/cursos");
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}

// Después de guardar, la API devuelve el curso actualizado.
function actualizar(nuevo: TrabajoCompleto) { d.value = nuevo; }
</script>

<template>
  <EstadoCarga v-if="!d" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else>
    <nav aria-label="Estás en" class="mb-3 text-sm text-suave">
      <RouterLink to="/cursos" class="hover:text-acento hover:underline">Mis cursos</RouterLink> <span aria-hidden="true">›</span> {{ d.trabajo.nombre }}
    </nav>
    <header class="flex flex-wrap items-center gap-4">
      <span v-if="marca?.logo_url" class="grid h-14 w-20 shrink-0 place-items-center rounded-xl border border-borde"
            :class="marca.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
        <img :src="marca.logo_url" alt="" class="max-h-9 max-w-16 object-contain" />
      </span>
      <div class="min-w-0 flex-1">
        <h1 class="text-2xl font-bold sm:text-3xl">{{ d.trabajo.nombre }}</h1>
        <p class="mt-1 text-sm text-suave">
          {{ cuenta(d.resumen.videos.length, "video") }} · {{ mmss(d.resumen.segundos) }} min ·
          {{ cuenta(d.trabajo.laminas.length, "diapositiva") }} · creado el {{ fecha(d.trabajo.creado) }}
        </p>
      </div>
    </header>

    <!-- Pestañas -->
    <div class="sticky top-[60px] z-20 -mx-4 mt-6 mb-8 border-b border-borde bg-fondo/95 px-4 backdrop-blur sm:-mx-6 sm:px-6 lg:top-0 lg:-mx-10 lg:px-10">
      <nav class="-mb-px flex gap-1 overflow-x-auto" aria-label="Secciones del curso">
        <button v-for="p in ([
          { id: 'resumen', texto: 'Resumen', icono: LayoutDashboard },
          { id: 'guion', texto: 'Guion', icono: ListChecks },
          { id: 'ajustes', texto: 'Marca y voz', icono: SlidersHorizontal },
        ] as const)" :key="p.id" type="button" :aria-current="vista === p.id ? 'page' : undefined" @click="ir(p.id)"
          class="flex shrink-0 items-center gap-2 border-b-[3px] px-3 py-3.5 text-sm font-semibold whitespace-nowrap transition sm:px-4"
          :class="vista === p.id ? 'border-acento text-acento' : 'border-transparent text-suave hover:border-borde hover:text-texto'">
          <component :is="p.icono" class="size-4" /> {{ p.texto }}
          <span v-if="p.id === 'guion' && porRevisar" class="rounded-full bg-aviso-fondo px-2 py-0.5 text-xs font-bold text-aviso"
                :aria-label="`${porRevisar} por revisar`">{{ porRevisar }}</span>
        </button>
      </nav>
    </div>

    <PasoResumen v-if="vista === 'resumen'" :datos="d" @ir="ir" @eliminar="eliminar" />
    <PasoGuion v-else-if="vista === 'guion'" :key="`${videoInicial}-${soloRevisar}`" :datos="d"
               :video-inicial="videoInicial" :solo-revisar-inicial="soloRevisar" @actualizado="actualizar" />
    <PasoAjustes v-else :datos="d" @actualizado="actualizar" />
  </div>
</template>
