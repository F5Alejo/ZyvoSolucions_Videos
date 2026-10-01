<script setup lang="ts">
import { computed, onUnmounted, ref, watch } from "vue";
import { ChevronDown, CircleAlert, CircleCheck, CircleX, Clapperboard, Download, FileArchive, Film, Info, ListVideo, LoaderCircle, RefreshCw, Trash2 } from "@lucide/vue";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import { catalogo } from "../../composables/catalogo";
import type { Produccion, TrabajoCompleto, VideoRender } from "../../tipos";
import PanelAgentes from "./PanelAgentes.vue";
import { cuenta, mmss } from "../../utils";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ eliminar: []; actualizado: [TrabajoCompleto] }>();

const t = computed(() => props.datos.trabajo);
const r = computed(() => props.datos.resumen);
const marca = computed(() => catalogo.value?.marcas[t.value.marca]);
const fondo = computed(() => marca.value?.paleta[0]?.hex ?? "#020202");
const tinta = computed(() => marca.value?.paleta[1]?.hex ?? "#FFFFFF");
const vertical = computed(() => t.value.formatos.length === 1 && t.value.formatos[0] === "9:16");

// ── El motor: estado de cada video; mientras alguno se produce, se consulta cada 3 s ──
const produccion = ref<Produccion | null>(null);
const pidiendo = ref<string | null>(null);
let temporizador: ReturnType<typeof setTimeout> | undefined;

const enCurso = (v: VideoRender | null | undefined) => v?.estado === "en_cola" || v?.estado === "produciendo";

async function consultar() {
  clearTimeout(temporizador);
  try {
    produccion.value = await api.get<Produccion>(`/api/trabajos/${t.value.id}/produccion`);
  } catch {
    /* sin conexión: se reintenta */
  }
  const p = produccion.value;
  if (Object.values(p?.videos ?? {}).some(enCurso) || enCurso(p?.completo as VideoRender | null)) temporizador = setTimeout(consultar, 3000);
}

async function producir(clave: string) {
  pidiendo.value = clave;
  try {
    produccion.value = await api.post<Produccion>(`/api/trabajos/${t.value.id}/producir/${clave}`);
    avisar("El video entró a la cola. Puedes seguir trabajando: aparece aquí cuando esté listo.");
    temporizador = setTimeout(consultar, 1500);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    pidiendo.value = null;
  }
}

// Al cambiar de curso, de marca o de voz, se vuelve a preguntar (un video puede quedar desactualizado).
watch(() => [t.value.id, t.value.marca, t.value.voz], consultar, { immediate: true });
onUnmounted(() => clearTimeout(temporizador));

async function producirTodo() {
  pidiendo.value = "todo";
  try {
    produccion.value = await api.post<Produccion>(`/api/trabajos/${t.value.id}/producir-todo`);
    avisar("Todo entró a la cola: primero los videos y al final el MP4 completo.");
    temporizador = setTimeout(consultar, 1500);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    pidiendo.value = null;
  }
}

async function armarCompleto() {
  pidiendo.value = "completo";
  try {
    produccion.value = await api.post<Produccion>(`/api/trabajos/${t.value.id}/completo`);
    temporizador = setTimeout(consultar, 1500);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    pidiendo.value = null;
  }
}

const trabajando = computed(() => {
  const p = produccion.value;
  return !!p && (Object.values(p.videos).some(enCurso) || enCurso(p.completo as VideoRender | null));
});
const completo = computed(() => produccion.value?.completo ?? null);

function fallas(v: VideoRender): number {
  return v.informe?.chequeos.filter((c) => c.ok === false).length ?? 0;
}
</script>

<template>
  <section aria-labelledby="titulo-resultado" class="space-y-10">
    <div>
      <h2 id="titulo-resultado" class="text-xl font-bold">Lo que sale</h2>
      <p class="mt-1 text-sm text-suave">
        {{ cuenta(r.videos.length, "video") }} · {{ mmss(r.segundos) }} min · {{ marca?.nombre_corto }} · {{ t.formatos.join(" y ") }}
      </p>
    </div>

    <div v-if="produccion?.voz_falta" class="flex gap-3 rounded-xl border-l-4 border-aviso bg-aviso-fondo p-4" role="status">
      <CircleAlert class="mt-0.5 size-5 shrink-0 text-aviso" />
      <p class="text-sm">
        <strong>Esta voz no se puede usar todavía.</strong> {{ produccion.voz_falta }}.
        Elige otra en <em>Marca y voz</em>: las voces Kokoro son gratuitas y se pueden entregar.
      </p>
    </div>
    <div v-else-if="produccion?.voz_borrador" class="flex gap-3 rounded-xl border-l-4 border-aviso bg-aviso-fondo p-4" role="status">
      <CircleAlert class="mt-0.5 size-5 shrink-0 text-aviso" />
      <p class="text-sm"><strong>Esta voz es solo para borradores.</strong>
        Los videos salen con el sello «BORRADOR»: su licencia no permite entregarlos a un cliente.</p>
    </div>
    <div v-else class="flex gap-3 rounded-xl border-l-4 border-motor bg-superficie p-4">
      <Info class="mt-0.5 size-5 shrink-0 text-motor" />
      <p class="text-sm">
        Cada video se produce en este equipo: voz, imagen, subtítulos y revisión de calidad. Se produce uno a la vez;
        uno de 2 minutos tarda unos 5. Por ahora sale en horizontal (16:9).
      </p>
    </div>

    <!-- Todo el curso: avance, producir todo, MP4 completo y paquete -->
    <div v-if="produccion" class="tarjeta space-y-4 p-5">
      <div class="flex flex-wrap items-center gap-4">
        <div class="min-w-0 flex-1">
          <h3 class="font-bold">Todo el curso</h3>
          <p class="text-sm text-suave">
            <span class="cifra text-texto">{{ produccion.listos }} de {{ produccion.total }}</span> videos listos
            <template v-if="produccion.pendientes.length && produccion.listos"> · faltan {{ produccion.pendientes.length }}</template>
          </p>
          <div class="mt-2 h-2 overflow-hidden rounded-full bg-superficie-2" aria-hidden="true">
            <div class="h-full rounded-full bg-exito transition-all" :style="{ width: `${(100 * produccion.listos) / Math.max(1, produccion.total)}%` }" />
          </div>
        </div>
        <button v-if="trabajando || produccion.pendientes.length || !completo || completo.desactualizado || completo.estado === 'error'"
                class="boton-primario" :disabled="!!produccion.voz_falta || trabajando || pidiendo === 'todo'" @click="producirTodo">
          <LoaderCircle v-if="trabajando" class="size-4 animate-spin" /><ListVideo v-else class="size-4" />
          {{ trabajando ? "Produciendo…" : produccion.pendientes.length ? "Producir lo que falta y el completo" : "Armar el MP4 completo" }}
        </button>
      </div>

      <!-- Estado del MP4 completo -->
      <div v-if="completo" class="flex flex-wrap items-center gap-3 border-t border-borde pt-4">
        <Film class="size-5 shrink-0 text-acento" />
        <div class="min-w-0 flex-1 text-sm">
          <strong>Curso completo en un MP4</strong>
          <template v-if="enCurso(completo as VideoRender)">
            <progress max="1" :value="completo.progreso ?? 0" class="mt-1 block h-2 w-full accent-[var(--c-motor)]" />
            <span class="text-xs text-suave">{{ completo.paso }}</span>
          </template>
          <span v-else-if="completo.estado === 'error'" class="block text-error">{{ completo.mensaje }}</span>
          <span v-else-if="completo.informe" class="block text-suave">
            {{ mmss(completo.informe.duracion) }} min · {{ cuenta(completo.informe.capitulos.length, "capítulo") }}
            <span v-if="completo.desactualizado" class="font-semibold text-aviso"> · desactualizado: vuelve a armarlo</span>
          </span>
        </div>
        <template v-if="completo.estado === 'listo' && completo.archivos">
          <a :href="completo.archivos.mp4 + '?descargar=1'" class="boton-secundario"><Download class="size-4" /> MP4 completo</a>
          <a :href="completo.archivos.srt + '?descargar=1'" class="boton-fantasma">SRT</a>
          <a :href="completo.archivos.vtt + '?descargar=1'" class="boton-fantasma">VTT</a>
          <a :href="completo.archivos.capitulos + '?descargar=1'" class="boton-fantasma">Capítulos</a>
        </template>
        <button v-if="!enCurso(completo as VideoRender) && !produccion.pendientes.length" class="boton-fantasma"
                :disabled="pidiendo === 'completo'" @click="armarCompleto"><RefreshCw class="size-4" /> Volver a armar</button>
      </div>

      <div v-if="produccion.listos" class="flex flex-wrap items-center gap-3 border-t border-borde pt-4">
        <FileArchive class="size-5 shrink-0 text-acento" />
        <p class="min-w-0 flex-1 text-sm"><strong>Paquete para entregar</strong>
          <span class="block text-suave">Todos los MP4, subtítulos, capítulos, informes de calidad y un manifiesto con el SHA-256 de cada archivo.</span></p>
        <a :href="`/api/trabajos/${t.id}/paquete.zip`" class="boton-secundario"><Download class="size-4" /> Descargar ZIP</a>
      </div>
    </div>

    <!-- Los videos: su plan con los colores de la marca, o el video ya producido -->
    <div class="grid gap-4" :class="vertical ? 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-5' : 'sm:grid-cols-2 xl:grid-cols-3'">
      <div v-for="(v, i) in r.videos" :key="v.clave" class="tarjeta flex flex-col overflow-hidden">
        <template v-for="p in [produccion?.videos[v.clave]]" :key="v.clave + (p?.estado ?? 'nuevo')">
          <video v-if="p?.estado === 'listo' && p.archivos" controls preload="metadata" :src="p.archivos.mp4 + '#t=2'"
                 class="aspect-video w-full bg-black" :aria-label="v.titulo">
            <track kind="subtitles" srclang="es" label="Español" :src="p.archivos.vtt" default />
          </video>
          <div v-else class="flex flex-col justify-between p-3 transition-colors" :class="vertical ? 'aspect-[9/16]' : 'aspect-video'"
               :style="{ background: fondo, color: tinta }">
            <span class="text-[11px] font-semibold opacity-80">Video {{ i + 1 }}</span>
            <span class="line-clamp-3 text-sm leading-snug font-bold">{{ v.titulo }}</span>
            <span class="self-end text-xs font-semibold tabular-nums opacity-80">{{ mmss(v.segundos) }}</span>
          </div>

          <div class="flex flex-1 flex-col gap-2 px-3 py-3">
            <div class="flex items-center justify-between gap-2">
              <span class="truncate text-xs text-suave">Video {{ i + 1 }} · láminas {{ v.laminas.join(", ") }}</span>
              <span v-if="!p" class="shrink-0 rounded-full bg-superficie-2 px-2 py-0.5 text-[11px] font-semibold text-suave">Por producir</span>
              <span v-else-if="p.estado === 'listo'" class="shrink-0 rounded-full bg-exito-fondo px-2 py-0.5 text-[11px] font-semibold text-exito">Listo</span>
              <span v-else-if="p.estado === 'error'" class="shrink-0 rounded-full bg-error-fondo px-2 py-0.5 text-[11px] font-semibold text-error">Falló</span>
              <span v-else class="shrink-0 rounded-full bg-superficie-2 px-2 py-0.5 text-[11px] font-semibold text-motor">
                {{ p.estado === "en_cola" ? "En la cola" : "Produciendo" }}</span>
            </div>

            <!-- Produciendo -->
            <template v-if="enCurso(p)">
              <progress max="1" :value="p?.progreso ?? 0" class="h-2 w-full accent-[var(--c-motor)]" :aria-label="`Progreso de ${v.titulo}`" />
              <span class="text-xs text-suave" aria-live="polite">{{ p?.paso }}</span>
            </template>

            <p v-else-if="p?.estado === 'error'" class="text-sm text-error">{{ p.mensaje }}</p>

            <!-- Listo: calidad y descargas -->
            <template v-else-if="p?.estado === 'listo' && p.informe">
              <p v-if="p.desactualizado" class="text-xs font-semibold text-aviso">Se produjo con otra marca o voz: vuelve a producirlo.</p>
              <details class="group text-sm">
                <summary class="flex cursor-pointer list-none items-center gap-1.5 font-semibold">
                  <CircleAlert v-if="fallas(p)" class="size-4 text-aviso" /><CircleCheck v-else class="size-4 text-exito" />
                  {{ fallas(p) ? `${cuenta(fallas(p), "chequeo")} por revisar` : "Calidad revisada" }} · {{ mmss(p.informe.duracion) }}
                  <ChevronDown class="ml-auto size-4 transition group-open:rotate-180" />
                </summary>
                <ul class="mt-2 space-y-1.5">
                  <li v-for="c in p.informe.chequeos" :key="c.titulo" class="flex items-start gap-2">
                    <CircleCheck v-if="c.ok === true" class="mt-0.5 size-4 shrink-0 text-exito" aria-label="Bien" />
                    <CircleX v-else-if="c.ok === false" class="mt-0.5 size-4 shrink-0 text-error" aria-label="Falla" />
                    <Info v-else class="mt-0.5 size-4 shrink-0 text-suave" aria-label="Dato" />
                    <span><strong class="block text-xs">{{ c.titulo }}</strong><span class="text-xs text-suave">{{ c.detalle }}</span></span>
                  </li>
                </ul>
              </details>
              <div v-if="p.archivos" class="flex flex-wrap gap-2">
                <a :href="p.archivos.mp4 + '?descargar=1'" class="boton-secundario !px-3 !py-1.5 text-xs"><Download class="size-3.5" /> MP4</a>
                <a :href="p.archivos.vtt + '?descargar=1'" class="boton-secundario !px-3 !py-1.5 text-xs" title="Subtítulos para LMS y web"><Download class="size-3.5" /> VTT</a>
                <a :href="p.archivos.srt + '?descargar=1'" class="boton-secundario !px-3 !py-1.5 text-xs" title="Subtítulos para YouTube"><Download class="size-3.5" /> SRT</a>
              </div>
            </template>

            <button v-if="!enCurso(p)" type="button" class="mt-auto self-start text-sm"
                    :class="p?.estado === 'listo' ? 'boton-secundario' : 'boton-primario'"
                    :disabled="!!produccion?.voz_falta || pidiendo === v.clave" @click="producir(v.clave)">
              <RefreshCw v-if="p" class="size-4" /><Clapperboard v-else class="size-4" />
              {{ p ? "Volver a producir" : "Producir video" }}
            </button>
          </div>
        </template>
      </div>
    </div>

    <PanelAgentes :trabajo="t.id" donde="resultado" @actualizado="(d) => emit('actualizado', d)" />

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
        <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.gift`" class="boton-secundario"><Download class="size-4" /> Preguntas para Moodle (GIFT)</a>
        <a v-if="t.banco" :href="`/api/trabajos/${t.id}/banco.xml`" class="boton-secundario"><Download class="size-4" /> Moodle XML</a>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="boton-peligro" @click="$emit('eliminar')"><Trash2 class="size-4" /> Eliminar este curso</button>
    </div>
  </section>
</template>
