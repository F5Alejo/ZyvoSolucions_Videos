<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft, ArrowRight, CircleCheck, Download } from "lucide-vue-next";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import { confirmar } from "../composables/confirmar";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import PasoPresentacion from "../components/curso/PasoPresentacion.vue";
import PasoGuion from "../components/curso/PasoGuion.vue";
import PasoMarcaVoz from "../components/curso/PasoMarcaVoz.vue";
import PasoResultado from "../components/curso/PasoResultado.vue";
import type { TrabajoCompleto } from "../tipos";
import { cuenta, mmss } from "../utils";

const props = defineProps<{ id: string }>();
const ruta = useRoute();
const router = useRouter();
const { datos: d, cargando, error, recargar } = useCarga(() => api.get<TrabajoCompleto>(`/api/trabajos/${props.id}`), () => props.id);

const PASOS = [
  { id: "presentacion", titulo: "Presentación" },
  { id: "guion", titulo: "Guion" },
  { id: "marca", titulo: "Marca y voz" },
  { id: "resultado", titulo: "Resultado" },
] as const;
type Paso = (typeof PASOS)[number]["id"];

const paso = computed<Paso>(() => {
  const q = ruta.query.paso;
  return PASOS.find((p) => p.id === q)?.id ?? "presentacion";
});
const indice = computed(() => PASOS.findIndex((p) => p.id === paso.value));

function ir(p: Paso) {
  router.replace({ query: { ...ruta.query, paso: p } });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

const porRevisar = computed(() => d.value?.resumen.chequeos.filter((c) => c.ok !== true) ?? []);

/** Lo que dice cada paso debajo de su nombre. */
function detalle(p: Paso): string {
  if (!d.value) return "";
  const { trabajo: t, resumen: r } = d.value;
  switch (p) {
    case "presentacion":
      return cuenta(t.laminas.length, "lámina");
    case "guion":
      return porRevisar.value.length ? `${cuenta(porRevisar.value.length, "cosa")} por revisar` : "Todo en orden";
    case "marca": {
      const m = catalogo.value?.marcas[t.marca]?.nombre_corto ?? t.marca;
      const v = catalogo.value?.voces.find((x) => x.id === t.voz)?.nombre ?? t.voz;
      return `${m} · ${v}`;
    }
    case "resultado":
      return `${cuenta(r.videos.length, "video")} · ${mmss(r.segundos)} min`;
  }
}

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

// Después de guardar marca o voz, la API devuelve el curso actualizado.
function actualizar(nuevo: TrabajoCompleto) {
  d.value = nuevo;
}
</script>

<template>
  <EstadoCarga v-if="!d" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else>
    <EncabezadoPagina :titulo="d.trabajo.nombre" :migas="[{ texto: 'Cursos', a: '/cursos' }, { texto: d.trabajo.nombre }]">
      <template #debajo>
        <p class="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-suave">
          <span>{{ cuenta(d.trabajo.laminas.length, "lámina") }}</span>
          <ArrowRight class="size-3.5" aria-label="se convierten en" />
          <span class="font-semibold text-texto">{{ cuenta(d.resumen.videos.length, "video") }}</span>
          <span>· {{ mmss(d.resumen.segundos) }} min</span>
          <span v-if="d.resumen.preguntas">· {{ cuenta(d.resumen.preguntas, "pregunta") }}</span>
        </p>
      </template>
      <template #acciones>
        <a :href="`/api/trabajos/${id}/orden.json`" class="boton-secundario"><Download class="size-4" /> Orden de producción</a>
      </template>
    </EncabezadoPagina>

    <!-- Los cuatro pasos -->
    <nav class="sticky top-[60px] z-20 -mx-4 mb-8 bg-fondo/95 px-4 py-2 backdrop-blur sm:-mx-6 sm:px-6 lg:top-0 lg:-mx-10 lg:px-10"
         aria-label="Pasos del curso">
      <ol class="grid grid-cols-4 gap-2">
        <li v-for="(p, i) in PASOS" :key="p.id">
          <button type="button" :aria-current="paso === p.id ? 'step' : undefined" @click="ir(p.id)"
            class="flex w-full flex-col items-center gap-1 rounded-xl border px-2 py-2 text-center transition sm:flex-row sm:gap-3 sm:px-3 sm:py-2.5 sm:text-left"
            :class="paso === p.id ? 'border-acento bg-superficie shadow-sm ring-1 ring-acento' : 'border-borde bg-superficie hover:border-acento'">
            <span class="grid size-8 shrink-0 place-items-center rounded-full text-sm font-bold"
                  :class="paso === p.id ? 'bg-acento text-sobre-acento' : i < indice ? 'bg-exito-fondo text-exito' : 'bg-superficie-2 text-suave'">
              <CircleCheck v-if="i < indice" class="size-4" aria-label="visto" /><template v-else>{{ i + 1 }}</template>
            </span>
            <span class="min-w-0">
              <span class="block text-xs font-bold sm:text-sm">{{ p.titulo }}</span>
              <span class="hidden truncate text-xs text-suave sm:block">{{ detalle(p.id) }}</span>
            </span>
          </button>
        </li>
      </ol>
    </nav>

    <PasoPresentacion v-if="paso === 'presentacion'" :datos="d" />
    <PasoGuion v-else-if="paso === 'guion'" :datos="d" @actualizado="actualizar" />
    <PasoMarcaVoz v-else-if="paso === 'marca'" :datos="d" @actualizado="actualizar" />
    <PasoResultado v-else :datos="d" @eliminar="eliminar" />

    <!-- Avanzar o volver -->
    <div class="mt-10 flex flex-wrap items-center justify-between gap-3 border-t border-borde pt-6">
      <button v-if="indice > 0" class="boton-fantasma" @click="ir(PASOS[indice - 1]!.id)">
        <ArrowLeft class="size-4" /> {{ PASOS[indice - 1]!.titulo }}
      </button>
      <span v-else />
      <button v-if="indice < PASOS.length - 1" class="boton-primario" @click="ir(PASOS[indice + 1]!.id)">
        Siguiente: {{ PASOS[indice + 1]!.titulo }} <ArrowRight class="size-4" />
      </button>
    </div>
  </div>
</template>
