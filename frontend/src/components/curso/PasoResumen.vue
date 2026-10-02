<script setup lang="ts">
import { computed } from "vue";
import { ArrowRight, ChevronDown, CircleAlert, CircleCheck, Clapperboard, Download, Palette, Presentation, Trash2 } from "lucide-vue-next";
import { catalogo } from "../../composables/catalogo";
import VistaPreviaVideo from "../VistaPreviaVideo.vue";
import PanelAgentes from "./PanelAgentes.vue";
import type { TrabajoCompleto } from "../../tipos";
import { cuenta, mmss } from "../../utils";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ ir: [vista: "guion" | "ajustes" | "producir", video?: number, soloRevisar?: boolean]; eliminar: []; actualizado: [TrabajoCompleto] }>();

const t = computed(() => props.datos.trabajo);
const r = computed(() => props.datos.resumen);
const marca = computed(() => catalogo.value?.marcas[t.value.marca]);
const voz = computed(() => catalogo.value?.voces.find((v) => v.id === t.value.voz));
const vertical = computed(() => t.value.formatos.length === 1 && t.value.formatos[0] === "9:16");
const porRevisar = computed(() => r.value.chequeos.filter((c) => c.ok !== true));
const fallas = computed(() => r.value.chequeos.filter((c) => c.ok === false));

function frase(numeros: number[]) {
  return t.value.laminas.find((l) => numeros.includes(l.n) && l.frases.length)?.frases[0];
}
</script>

<template>
  <div class="space-y-10">
    <!-- Estado y siguiente paso -->
    <section class="grid grid-cols-[minmax(0,1fr)] gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]" aria-label="Estado del curso">
      <ol class="tarjeta divide-y divide-borde rounded-2xl">
        <li class="flex items-center gap-4 p-4">
          <span class="grid size-10 shrink-0 place-items-center rounded-full bg-exito-fondo text-exito"><Presentation class="size-5" /></span>
          <span class="min-w-0 flex-1"><span class="block font-semibold">Presentación leída</span>
            <span class="block text-sm text-suave">{{ cuenta(t.laminas.length, "diapositiva") }} · {{ r.frases }} frases de guion</span></span>
          <CircleCheck class="size-5 text-exito" aria-label="Hecho" />
        </li>
        <li class="flex items-center gap-4 p-4">
          <span class="grid size-10 shrink-0 place-items-center rounded-full" :class="porRevisar.length ? 'bg-aviso-fondo text-aviso' : 'bg-exito-fondo text-exito'">
            <CircleAlert v-if="porRevisar.length" class="size-5" /><CircleCheck v-else class="size-5" />
          </span>
          <span class="min-w-0 flex-1"><span class="block font-semibold">Guion</span>
            <span class="block text-sm text-suave">{{ porRevisar.length ? `${cuenta(porRevisar.length, "cosa")} por revisar` : "Todo en orden" }}</span></span>
          <button class="text-sm font-semibold text-acento hover:underline" @click="emit('ir', 'guion', undefined, porRevisar.length > 0)">
            {{ porRevisar.length ? "Revisar" : "Ver" }}
          </button>
        </li>
        <li class="flex items-center gap-4 p-4">
          <span class="grid size-10 shrink-0 place-items-center rounded-full bg-exito-fondo text-exito"><Palette class="size-5" /></span>
          <span class="min-w-0 flex-1"><span class="block font-semibold">Marca y voz</span>
            <span class="block truncate text-sm text-suave">{{ marca?.nombre_corto }} · voz {{ voz?.nombre }} · {{ t.formatos.map((f) => (f === "16:9" ? "horizontal" : "vertical")).join(" y ") }}</span></span>
          <button class="text-sm font-semibold text-acento hover:underline" @click="emit('ir', 'ajustes')">Cambiar</button>
        </li>
        <li class="flex items-center gap-4 p-4">
          <span class="grid size-10 shrink-0 place-items-center rounded-full bg-superficie-2 text-suave"><Clapperboard class="size-5" /></span>
          <span class="min-w-0 flex-1"><span class="block font-semibold">Videos</span>
            <span class="block text-sm text-suave">{{ cuenta(r.videos.length, "video") }} · {{ mmss(r.segundos) }} min</span></span>
          <button class="text-sm font-semibold text-acento hover:underline" @click="emit('ir', 'producir')">Producir</button>
        </li>
      </ol>

      <!-- Siguiente paso: una sola cosa, bien clara -->
      <div class="relative overflow-hidden rounded-2xl border border-[#272725] p-6 text-white" :class="fallas.length ? 'bg-[#B42318]' : porRevisar.length ? 'bg-[#8A4209]' : 'bg-lateral'">
        <p class="text-sm font-semibold tracking-wider uppercase opacity-80">Siguiente paso</p>
        <template v-if="fallas.length">
          <h2 class="mt-2 text-2xl font-bold">{{ fallas[0]!.titulo }}</h2>
          <p class="mt-2 opacity-90">{{ fallas[0]!.detalle }}. {{ fallas[0]!.ayuda }}</p>
          <button class="mt-5 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-bold text-[#111] transition hover:brightness-95"
                  @click="emit('ir', 'guion', undefined, true)">Ver en el guion <ArrowRight class="size-4" /></button>
        </template>
        <template v-else-if="porRevisar.length">
          <h2 class="mt-2 text-2xl font-bold">{{ porRevisar[0]!.titulo }}</h2>
          <p class="mt-2 opacity-90">{{ porRevisar[0]!.detalle }}. {{ porRevisar[0]!.ayuda }}</p>
          <button class="mt-5 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-bold text-[#111] transition hover:brightness-95"
                  @click="emit('ir', 'guion', undefined, true)">Revisar ahora <ArrowRight class="size-4" /></button>
        </template>
        <template v-else>
          <h2 class="mt-2 text-2xl font-bold">Tu curso está listo para producir</h2>
          <p class="mt-2 opacity-90">El guion, la marca y la voz están en orden. Produce los videos en este equipo y descárgalos listos para entregar.</p>
          <button class="mt-5 inline-flex items-center gap-2 rounded-lg bg-dorado px-4 py-2.5 text-sm font-bold text-[#1A1A1A] transition hover:brightness-110"
                  @click="emit('ir', 'producir')"><Clapperboard class="size-4" /> Producir los videos</button>
        </template>
        <svg class="pointer-events-none absolute -right-10 -bottom-12 size-44 opacity-25" viewBox="0 0 100 100" aria-hidden="true">
          <circle cx="50" cy="50" r="42" fill="none" stroke="#06C7FB" stroke-width="6" /><circle cx="50" cy="50" r="34" fill="none" stroke="#C8951A" stroke-width="1.5" />
        </svg>
      </div>
    </section>

    <!-- Los videos -->
    <section aria-labelledby="t-videos">
      <div class="mb-4 flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="t-videos" class="text-xl font-bold">Tus videos</h2>
        <p class="text-sm text-suave">Así se verá el inicio de cada uno. Toca uno para leer su guion.</p>
      </div>
      <div class="grid grid-cols-[minmax(0,1fr)] gap-4" :class="vertical ? 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5' : 'grid-cols-[minmax(0,1fr)] sm:grid-cols-2 xl:grid-cols-3'">
        <button v-for="(v, i) in r.videos" :key="v.clave" type="button" class="group text-left" @click="emit('ir', 'guion', i)">
          <VistaPreviaVideo :titulo="v.titulo" :subtitulo="frase(v.laminas)" :numero="i + 1" :segundos="v.segundos" :marca="marca" :vertical="vertical" />
          <span class="mt-2 block truncate text-sm font-semibold group-hover:text-acento">{{ v.titulo }}</span>
          <span class="block text-xs text-suave">{{ cuenta(v.laminas.length, "diapositiva") }} · {{ mmss(v.segundos) }} min</span>
        </button>
      </div>
    </section>

    <!-- Preguntas -->
    <section v-if="t.banco" aria-labelledby="t-preguntas">
      <h2 id="t-preguntas" class="text-xl font-bold">Preguntas de evaluación <span class="text-suave">· {{ r.preguntas }}</span></h2>
      <p class="mt-1 mb-4 text-sm text-suave">Cada pregunta indica de qué diapositiva sale. La respuesta correcta va en verde.</p>
      <div class="space-y-2">
        <details v-for="g in t.banco.grupos" :key="g.clave" class="tarjeta group rounded-2xl">
          <summary class="flex cursor-pointer list-none items-center justify-between gap-3 p-4">
            <span><strong>{{ g.titulo }}</strong> <span class="text-sm text-suave">· {{ g.tema }} · {{ cuenta(g.preguntas.length, "pregunta") }}</span></span>
            <ChevronDown class="size-4 shrink-0 transition group-open:rotate-180" />
          </summary>
          <ol class="list-decimal space-y-4 border-t border-borde px-4 py-4 pl-10">
            <li v-for="(p, i) in g.preguntas" :key="i">
              <p class="font-semibold">{{ p.enunciado }}</p>
              <ul class="mt-1.5 space-y-1 text-sm">
                <li class="flex gap-2 font-semibold text-exito"><CircleCheck class="mt-0.5 size-4 shrink-0" />{{ p.correcta }}</li>
                <li v-for="x in p.distractores" :key="x" class="pl-6 text-suave">{{ x }}</li>
              </ul>
              <span class="mt-2 inline-block rounded-md bg-entra/10 px-2 py-0.5 text-xs font-semibold text-entra">{{ p.fuente }}</span>
            </li>
          </ol>
        </details>
      </div>
    </section>

    <PanelAgentes :trabajo="t.id" donde="presentacion" @actualizado="(d) => emit('actualizado', d)" />

    <!-- Para el equipo técnico -->
    <details class="tarjeta group rounded-2xl">
      <summary class="flex cursor-pointer list-none items-center justify-between p-5 text-sm font-semibold text-suave hover:text-texto">
        Opciones avanzadas <ChevronDown class="size-4 transition group-open:rotate-180" />
      </summary>
      <div class="space-y-5 border-t border-borde p-5">
        <div>
          <p class="font-semibold">Archivos para el equipo técnico</p>
          <p class="mt-1 text-sm text-suave">Lo que recibe el generador de video. No hace falta abrirlos para revisar el curso.</p>
          <div class="mt-3 flex flex-wrap gap-2">
            <a :href="`/api/trabajos/${t.id}/orden.json`" class="boton-secundario"><Download class="size-4" /> Orden de producción</a>
            <a :href="`/api/trabajos/${t.id}/curso.json`" class="boton-secundario"><Download class="size-4" /> Contenido extraído</a>
            <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.json`" class="boton-secundario"><Download class="size-4" /> Preguntas</a>
            <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.gift`" class="boton-secundario"><Download class="size-4" /> Preguntas para Moodle (GIFT)</a>
            <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.xml`" class="boton-secundario"><Download class="size-4" /> Moodle XML</a>
          </div>
        </div>
        <div class="border-t border-borde pt-5">
          <p class="font-semibold">Eliminar el curso</p>
          <p class="mt-1 text-sm text-suave">Se borra también la presentación que subiste. No se puede deshacer.</p>
          <button class="boton-peligro mt-3" @click="emit('eliminar')"><Trash2 class="size-4" /> Eliminar este curso</button>
        </div>
      </div>
    </details>
  </div>
</template>
