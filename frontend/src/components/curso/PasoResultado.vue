<script setup lang="ts">
import { computed } from "vue";
import { ChevronDown, CircleAlert, CircleCheck, CircleX, Download, Info, Trash2 } from "lucide-vue-next";
import { catalogo } from "../../composables/catalogo";
import type { TrabajoCompleto } from "../../tipos";
import { cuenta, mmss } from "../../utils";

const props = defineProps<{ datos: TrabajoCompleto }>();
defineEmits<{ eliminar: [] }>();

const t = computed(() => props.datos.trabajo);
const r = computed(() => props.datos.resumen);
const marca = computed(() => catalogo.value?.marcas[t.value.marca]);
const fondo = computed(() => marca.value?.paleta[0]?.hex ?? "#020202");
const tinta = computed(() => marca.value?.paleta[1]?.hex ?? "#FFFFFF");
const vertical = computed(() => t.value.formatos.length === 1 && t.value.formatos[0] === "9:16");
</script>

<template>
  <section aria-labelledby="titulo-resultado" class="space-y-10">
    <div>
      <h2 id="titulo-resultado" class="text-xl font-bold">Lo que sale</h2>
      <p class="mt-1 text-sm text-suave">
        {{ cuenta(r.videos.length, "video") }} · {{ mmss(r.segundos) }} min · {{ marca?.nombre_corto }} · {{ t.formatos.join(" y ") }}
      </p>
    </div>

    <div class="flex gap-3 rounded-xl border-l-4 border-motor bg-superficie p-4">
      <Info class="mt-0.5 size-5 shrink-0 text-motor" />
      <p class="text-sm">
        <strong>Todo está listo menos el render.</strong> Los videos todavía no se generan desde aquí.
        <template v-if="t.origen.tipo === 'ejemplo'">Este curso ya se produjo aparte y sus videos están en Drive.</template>
        Cuando el generador esté conectado, cada tarjeta mostrará su video.
      </p>
    </div>

    <!-- Los videos, con los colores de la marca elegida -->
    <div class="grid gap-4" :class="vertical ? 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-5' : 'sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'">
      <div v-for="(v, i) in r.videos" :key="v.clave" class="tarjeta overflow-hidden">
        <div class="flex flex-col justify-between p-3 transition-colors" :class="vertical ? 'aspect-[9/16]' : 'aspect-video'"
             :style="{ background: fondo, color: tinta }">
          <span class="text-[11px] font-semibold opacity-80">Video {{ i + 1 }}</span>
          <span class="line-clamp-3 text-sm leading-snug font-bold">{{ v.titulo }}</span>
          <span class="self-end text-xs font-semibold tabular-nums opacity-80">{{ mmss(v.segundos) }}</span>
        </div>
        <div class="flex items-center justify-between gap-2 px-3 py-2">
          <span class="truncate text-xs text-suave">Láminas {{ v.laminas.join(", ") }}</span>
          <span class="shrink-0 rounded-full bg-superficie-2 px-2 py-0.5 text-[11px] font-semibold text-suave">Por generar</span>
        </div>
      </div>
    </div>

    <!-- Revisión -->
    <div>
      <h3 class="mb-3 text-lg font-bold">Revisión</h3>
      <ul class="space-y-2">
        <li v-for="c in r.chequeos" :key="c.titulo" class="tarjeta flex items-start gap-3 p-4">
          <CircleCheck v-if="c.ok === true" class="size-5 shrink-0 text-exito" aria-label="Bien" />
          <CircleX v-else-if="c.ok === false" class="size-5 shrink-0 text-error" aria-label="Falla" />
          <CircleAlert v-else class="size-5 shrink-0 text-aviso" aria-label="Revisar" />
          <span><strong class="block text-sm">{{ c.titulo }}</strong><span class="text-sm text-suave">{{ c.detalle }}</span></span>
        </li>
      </ul>
      <details v-if="r.normativas.length" class="tarjeta group mt-3 p-4">
        <summary class="flex cursor-pointer list-none items-center justify-between text-sm font-semibold">
          Ver cada cifra y norma, lámina por lámina <ChevronDown class="size-4 transition group-open:rotate-180" />
        </summary>
        <dl class="mt-3 divide-y divide-borde text-sm">
          <div v-for="x in r.normativas" :key="x.lamina" class="grid grid-cols-[90px_1fr] gap-3 py-2">
            <dt class="text-suave">Lámina {{ x.lamina }}</dt><dd>{{ x.citas.join(" · ") }}</dd>
          </div>
        </dl>
      </details>
    </div>

    <!-- Preguntas -->
    <div v-if="t.banco">
      <h3 class="text-lg font-bold">Preguntas de evaluación · {{ r.preguntas }}</h3>
      <p class="mt-1 mb-3 text-sm text-suave">Cada pregunta indica de qué lámina sale. La respuesta correcta va en verde.</p>
      <div class="space-y-2">
        <details v-for="g in t.banco.grupos" :key="g.clave" class="tarjeta group">
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
    </div>

    <!-- Archivos -->
    <div class="tarjeta p-5">
      <h3 class="font-bold">Archivos para el equipo técnico</h3>
      <p class="mt-1 text-sm text-suave">Lo que recibirá el generador de video. No hace falta abrirlos para revisar el curso.</p>
      <div class="mt-4 flex flex-wrap gap-2">
        <a :href="`/api/trabajos/${t.id}/orden.json`" class="boton-secundario"><Download class="size-4" /> Orden de producción</a>
        <a :href="`/api/trabajos/${t.id}/curso.json`" class="boton-secundario"><Download class="size-4" /> Contenido extraído</a>
        <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.json`" class="boton-secundario"><Download class="size-4" /> Preguntas</a>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="boton-peligro" @click="$emit('eliminar')"><Trash2 class="size-4" /> Eliminar este curso</button>
    </div>
  </section>
</template>
