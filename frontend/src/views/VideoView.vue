<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Archive, ChevronDown, History, Info, LoaderCircle, VideoOff } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import { confirmar } from "../composables/confirmar";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import EstadoChip from "../components/EstadoChip.vue";
import ReproductorVideo from "../components/ReproductorVideo.vue";
import type { Estado, Proyecto } from "../tipos";
import { fecha } from "../utils";

const props = defineProps<{ id: string }>();
const { datos: p, cargando, error, recargar } = useCarga(() => api.get<Proyecto>(`/api/proyectos/${props.id}`), () => props.id);

/** El siguiente paso natural según el estado; el primero es la acción principal. */
const SIGUIENTES: Record<Estado, [Estado, string][]> = {
  sin_estado: [["revision", "Enviar a revisión"], ["borrador", "Marcar como borrador"]],
  borrador: [["revision", "Enviar a revisión"]],
  revision: [["aprobado", "Aprobar"], ["borrador", "Devolver a borrador"]],
  aprobado: [["final", "Marcar como entregado"], ["revision", "Volver a revisión"]],
  final: [],
  archivado: [["borrador", "Recuperar"]],
};
const siguientes = computed(() => (p.value ? SIGUIENTES[p.value.estado] : []));
const otros = computed(() => {
  if (!p.value || !catalogo.value) return [];
  const usados = new Set<string>([p.value.estado, "archivado", ...siguientes.value.map(([e]) => e)]);
  return (Object.entries(catalogo.value.estados) as [Estado, string][]).filter(([e]) => !usados.has(e));
});

const CLAVE = "estudio.quien";
const quien = ref(leer());
const nota = ref("");
const enviando = ref<Estado | null>(null);
const faltaQuien = ref(false);
function leer() { try { return localStorage.getItem(CLAVE) ?? ""; } catch { return ""; } }
watch(quien, (v) => { if (v.trim()) faltaQuien.value = false; });

const vertical = computed(() => !p.value?.formato.includes("16:9") || p.value.formato.includes("9:16"));

async function cambiar(estado: Estado) {
  if (!p.value) return;
  if (!quien.value.trim()) { faltaQuien.value = true; return; }
  if (estado === "archivado") {
    const si = await confirmar({ titulo: "¿Archivar este video?", texto: "Deja de aparecer como pendiente, pero se puede recuperar.", aceptar: "Archivar", peligro: true });
    if (!si) return;
  }
  enviando.value = estado;
  try {
    p.value = await api.post<Proyecto>(`/api/proyectos/${props.id}/estado`, { estado, quien: quien.value.trim(), nota: nota.value.trim() });
    try { localStorage.setItem(CLAVE, quien.value.trim()); } catch { /* sin almacenamiento */ }
    nota.value = "";
    avisar(`Estado actualizado: ${catalogo.value?.estados[estado]}.`);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    enviando.value = null;
  }
}
</script>

<template>
  <EstadoCarga v-if="!p" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else>
    <EncabezadoPagina :titulo="p.titulo"
      :migas="[{ texto: 'Videos', a: '/videos' }, { texto: catalogo?.marcas[p.marca]?.nombre_corto ?? p.marca, a: `/marcas/${p.marca}` }, { texto: p.titulo }]">
      <template #debajo>
        <p class="mt-2 flex flex-wrap items-center gap-2 text-sm text-suave">
          <EstadoChip :estado="p.estado" /> <span>{{ catalogo?.familias[p.familia] }} · {{ p.formato }}<template v-if="p.duracion"> · {{ p.duracion }}</template></span>
        </p>
      </template>
    </EncabezadoPagina>

    <p v-if="p.nota" class="mb-6 flex gap-2 rounded-lg bg-aviso-fondo p-4 text-sm text-aviso"><Info class="mt-0.5 size-4 shrink-0" />{{ p.nota }}</p>

    <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_340px]">
      <!-- Videos -->
      <section aria-labelledby="titulo-videos">
        <h2 id="titulo-videos" class="mb-4 text-lg font-bold">Videos</h2>
        <div v-if="p.entregables_detalle?.length" class="grid gap-5" :class="vertical ? 'grid-cols-2 sm:grid-cols-3' : 'sm:grid-cols-2'">
          <ReproductorVideo v-for="e in p.entregables_detalle" :key="e.archivo" :archivo="e.archivo" :titulo="e.nota" :existe="e.existe" :vertical="vertical" />
        </div>
        <div v-else class="rounded-xl border-2 border-dashed border-borde p-8 text-center">
          <VideoOff class="mx-auto size-8 text-suave" />
          <p class="mt-2 font-semibold">No hay videos para ver aquí</p>
          <p class="mt-1 text-sm text-suave">Según la documentación, el archivo final está en: {{ p.donde ?? "sin registrar" }}.</p>
        </div>
      </section>

      <!-- Decisión -->
      <aside class="lg:sticky lg:top-6 lg:self-start">
        <form class="tarjeta space-y-4 p-5" @submit.prevent="siguientes[0] && cambiar(siguientes[0][0])">
          <h2 class="text-lg font-bold">¿Qué sigue?</h2>
          <p v-if="p.aprobado_por" class="text-sm text-suave">Aprobado por <strong class="text-texto">{{ p.aprobado_por }}</strong> el {{ fecha(p.aprobado_el ?? "") }}.</p>
          <div>
            <label for="quien" class="etiqueta-campo">¿Quién lo decide?</label>
            <input id="quien" v-model="quien" class="campo" :class="faltaQuien && 'border-error ring-2 ring-error/30'"
                   placeholder="Tu nombre, o «Cliente»" autocomplete="name" :aria-invalid="faltaQuien" aria-describedby="quien-error" />
            <p v-if="faltaQuien" id="quien-error" class="mt-1 text-sm text-error">Escribe quién toma la decisión: queda en el historial.</p>
          </div>
          <div>
            <label for="nota" class="etiqueta-campo">Comentario <span class="font-normal text-suave">(opcional)</span></label>
            <textarea id="nota" v-model="nota" rows="2" class="campo" placeholder="Por qué, o dónde quedó la decisión (correo, reunión…)" />
          </div>
          <div class="space-y-2">
            <button v-for="([e, texto], i) in siguientes" :key="e" type="button" :disabled="!!enviando"
                    :class="i === 0 ? 'boton-primario' : 'boton-secundario'" class="w-full" @click="cambiar(e)">
              <LoaderCircle v-if="enviando === e" class="size-4 animate-spin" /> {{ texto }}
            </button>
            <p v-if="!siguientes.length" class="text-sm text-suave">Este video ya está entregado.</p>
          </div>
          <details class="group border-t border-borde pt-3">
            <summary class="flex cursor-pointer list-none items-center justify-between text-sm text-suave hover:text-texto">
              Otras opciones <ChevronDown class="size-4 transition group-open:rotate-180" />
            </summary>
            <div class="mt-2 flex flex-col items-start gap-1">
              <button v-for="[e, txt] in otros" :key="e" type="button" class="boton-fantasma" :disabled="!!enviando" @click="cambiar(e)">Pasar a «{{ txt }}»</button>
              <button v-if="p.estado !== 'archivado'" type="button" class="boton-fantasma text-error hover:text-error" :disabled="!!enviando" @click="cambiar('archivado')">
                <Archive class="size-4" /> Archivar
              </button>
            </div>
          </details>
        </form>
      </aside>
    </div>

    <!-- Historial -->
    <section class="mt-10" aria-labelledby="titulo-historial">
      <h2 id="titulo-historial" class="mb-4 flex items-center gap-2 text-lg font-bold"><History class="size-5 text-suave" /> Historial</h2>
      <ol v-if="p.historial?.length" class="relative space-y-5 border-l-2 border-borde pl-6">
        <li v-for="(h, i) in [...p.historial].reverse()" :key="i" class="relative">
          <span class="absolute top-1.5 -left-[31px] size-3 rounded-full bg-acento ring-4 ring-fondo" aria-hidden="true" />
          <p class="text-xs text-suave">{{ fecha(h.fecha) }}</p>
          <p class="mt-0.5 flex flex-wrap items-center gap-2 text-sm"><strong>{{ h.quien }}</strong> <EstadoChip :estado="h.de" /> → <EstadoChip :estado="h.a" /></p>
          <p v-if="h.nota" class="mt-1 text-sm text-suave italic">«{{ h.nota }}»</p>
        </li>
      </ol>
      <p v-else class="text-sm text-suave">Nadie ha cambiado su estado desde el estudio.</p>
    </section>

    <details class="tarjeta group mt-10 p-5">
      <summary class="flex cursor-pointer list-none items-center justify-between text-sm font-semibold text-suave">
        Detalles técnicos <ChevronDown class="size-4 transition group-open:rotate-180" />
      </summary>
      <dl class="mt-4 grid gap-x-6 gap-y-3 text-sm sm:grid-cols-[200px_1fr]">
        <dt class="text-suave">Identificador</dt><dd><code>{{ p.id }}</code></dd>
        <dt class="text-suave">Estado según la documentación</dt><dd>{{ p.estado_original }}</dd>
        <dt class="text-suave">Dónde está el final</dt><dd>{{ p.donde ?? "sin registrar" }}</dd>
        <dt class="text-suave">Carpetas del repositorio</dt>
        <dd class="flex flex-wrap gap-1.5">
          <code v-for="c in p.carpetas_detalle" :key="c.nombre" class="rounded bg-superficie-2 px-1.5 py-0.5 text-xs" :class="!c.existe && 'text-error'">
            videos/{{ c.nombre }}<template v-if="!c.existe"> (no está)</template>
          </code>
        </dd>
      </dl>
    </details>
  </div>
</template>
