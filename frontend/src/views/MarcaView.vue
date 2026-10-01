<script setup lang="ts">
import { computed, ref } from "vue";
import { Check, Copy, ExternalLink, FileText, Lightbulb, TriangleAlert } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import EstadoChip from "../components/EstadoChip.vue";
import type { Color, Marca, Proyecto } from "../tipos";
import { fecha } from "../utils";

const props = defineProps<{ id: string }>();
const { datos: m, cargando, error, recargar } = useCarga(
  () => api.get<Marca & { proyectos: Proyecto[] }>(`/api/marcas/${props.id}`), () => props.id);

const capas = computed(() => {
  if (!m.value) return [];
  if (!m.value.capas_paleta) return [{ id: "", titulo: "", uso: "", fuente: m.value.paleta_fuente, colores: m.value.paleta }];
  return Object.entries(m.value.capas_paleta).map(([id, c]) => ({ id, ...c, colores: m.value!.paleta.filter((x) => x.capa === id) }));
});

/** Texto oscuro o claro sobre la muestra, según su luminancia. */
function tintaSobre(hex: string) {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255);
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b! > 0.5 ? "#111" : "#fff";
}

const copiado = ref("");
async function copiar(c: Color) {
  try {
    await navigator.clipboard.writeText(c.hex);
    copiado.value = c.hex;
    setTimeout(() => copiado.value === c.hex && (copiado.value = ""), 1500);
  } catch {
    avisar("No se pudo copiar: el navegador no lo permitió.", "error");
  }
}
const abiertos = computed(() => (m.value?.pendientes.filter((p) => !p.hecho).length ?? 0) + (m.value?.pedir_al_cliente.filter((p) => !p.hecho).length ?? 0));
</script>

<template>
  <EstadoCarga v-if="!m" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="space-y-10">
    <EncabezadoPagina :titulo="m.nombre" :subtitulo="m.que_es" :migas="[{ texto: 'Marcas' }, { texto: m.nombre_corto }]">
      <template #acciones>
        <span v-if="m.logo_url" class="rounded-xl border border-borde px-4 py-3" :class="m.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
          <img :src="m.logo_url" :alt="`Logo de ${m.nombre_corto}`" class="h-12 max-w-[220px] object-contain" />
        </span>
      </template>
      <template #debajo>
        <dl class="mt-4 flex flex-wrap gap-x-8 gap-y-2 text-sm">
          <div><dt class="text-suave">Dominio</dt><dd class="font-semibold">{{ m.dominio ?? "Por confirmar" }}</dd></div>
          <div><dt class="text-suave">Responsable</dt><dd class="font-semibold">{{ m.responsable ?? "Por confirmar" }}</dd></div>
          <div><dt class="text-suave">Ficha revisada</dt><dd class="font-semibold">{{ fecha(m.revisada) }}</dd></div>
          <div><dt class="text-suave">Pendientes</dt><dd class="font-semibold" :class="abiertos ? 'text-aviso' : ''">{{ abiertos }} abiertos</dd></div>
        </dl>
      </template>
    </EncabezadoPagina>

    <!-- Paleta -->
    <section aria-labelledby="titulo-paleta">
      <h2 id="titulo-paleta" class="text-lg font-bold">Paleta</h2>
      <p v-if="m.capas_paleta" class="mt-1 text-sm text-suave">{{ m.paleta_fuente }} Haz clic en un color para copiarlo.</p>
      <div class="mt-4 space-y-6">
        <div v-for="c in capas" :key="c.id" class="tarjeta p-5">
          <h3 v-if="c.titulo" class="font-bold">{{ c.titulo }}</h3>
          <p v-if="c.uso" class="mt-1 text-sm text-suave">{{ c.uso }}</p>
          <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
            <button v-for="col in c.colores" :key="col.hex + col.nombre" type="button" @click="copiar(col)"
                    class="group overflow-hidden rounded-lg border border-borde text-left transition hover:shadow-md" :aria-label="`Copiar ${col.hex}, ${col.nombre}`">
              <span class="flex h-16 items-end justify-end p-2" :style="{ background: col.hex, color: tintaSobre(col.hex) }">
                <Check v-if="copiado === col.hex" class="size-4" /><Copy v-else class="size-4 opacity-0 transition group-hover:opacity-80" />
              </span>
              <span class="block p-2">
                <code class="block text-xs font-bold">{{ col.hex }}</code>
                <span class="block text-xs leading-snug text-suave">{{ col.nombre }}</span>
              </span>
            </button>
          </div>
          <p class="mt-3 text-xs text-suave">Fuente: {{ c.fuente }}</p>
        </div>
      </div>
    </section>

    <!-- Identidad -->
    <section class="grid gap-4 md:grid-cols-3" aria-label="Identidad">
      <div class="tarjeta p-5"><h3 class="text-sm font-semibold text-suave">Tipografía</h3><p class="mt-1 text-sm">{{ m.tipografia }}</p></div>
      <div class="tarjeta p-5"><h3 class="text-sm font-semibold text-suave">Voz</h3><p class="mt-1 text-sm">{{ m.voz }}</p></div>
      <div class="tarjeta p-5"><h3 class="text-sm font-semibold text-suave">Llamado a la acción</h3><p class="mt-1 text-sm">{{ m.cta ?? "Faltan los datos de contacto y el CTA" }}</p></div>
    </section>

    <section v-if="m.hallazgos?.length" aria-labelledby="titulo-hallazgos">
      <h2 id="titulo-hallazgos" class="mb-3 flex items-center gap-2 text-lg font-bold"><Lightbulb class="size-5 text-dorado" /> Hallazgos</h2>
      <ul class="space-y-2">
        <li v-for="h in m.hallazgos" :key="h.texto" class="tarjeta p-4 text-sm"><span class="mr-2 text-xs text-suave">{{ fecha(h.fecha) }}</span>{{ h.texto }}</li>
      </ul>
    </section>

    <section v-if="m.contradicciones.length" aria-labelledby="titulo-contradicciones">
      <h2 id="titulo-contradicciones" class="mb-3 flex items-center gap-2 text-lg font-bold"><TriangleAlert class="size-5 text-aviso" /> Contradicciones abiertas</h2>
      <ul class="space-y-2">
        <li v-for="c in m.contradicciones" :key="c" class="rounded-xl border border-aviso/40 bg-aviso-fondo p-4 text-sm">{{ c }}</li>
      </ul>
    </section>

    <div class="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-2">
      <section aria-labelledby="titulo-pendientes">
        <h2 id="titulo-pendientes" class="mb-3 text-lg font-bold">Pendientes</h2>
        <ul class="tarjeta divide-y divide-borde">
          <li v-for="p in [...m.pendientes.map((x) => ({ ...x, tipo: 'Del equipo' })), ...m.pedir_al_cliente.map((x) => ({ ...x, tipo: 'Pedir al cliente' }))]"
              :key="p.tipo + p.texto" class="flex gap-3 p-3 text-sm" :class="p.hecho && 'text-suave line-through'">
            <input type="checkbox" :checked="p.hecho" disabled class="mt-0.5 size-4 accent-[var(--c-exito)]" :aria-label="p.hecho ? 'Hecho' : 'Pendiente'" />
            <span class="flex-1">{{ p.texto }}</span>
            <span class="shrink-0 text-xs text-suave no-underline">{{ p.tipo }}</span>
          </li>
        </ul>
      </section>
      <section aria-labelledby="titulo-fuentes">
        <h2 id="titulo-fuentes" class="mb-3 text-lg font-bold">Fuentes oficiales</h2>
        <ul class="tarjeta divide-y divide-borde">
          <li v-for="f in m.fuentes" :key="f.fuente" class="flex items-start gap-3 p-3 text-sm">
            <FileText class="mt-0.5 size-4 shrink-0 text-suave" />
            <span class="min-w-0 flex-1">
              <span class="font-semibold">{{ f.fuente }}</span> <span class="text-xs text-suave">· {{ f.tipo }}</span>
              <a v-if="f.url" :href="f.url" target="_blank" rel="noopener" class="mt-0.5 flex items-center gap-1 truncate text-xs text-acento hover:underline">
                {{ f.donde }} <ExternalLink class="size-3 shrink-0" />
              </a>
              <span v-else class="mt-0.5 block text-xs break-all text-suave">{{ f.donde }}</span>
            </span>
          </li>
        </ul>
      </section>
    </div>

    <section aria-labelledby="titulo-videos-marca">
      <h2 id="titulo-videos-marca" class="mb-3 text-lg font-bold">Videos de {{ m.nombre_corto }}</h2>
      <div class="tarjeta divide-y divide-borde">
        <RouterLink v-for="p in m.proyectos" :key="p.id" :to="`/videos/${p.id}`"
                    class="flex items-center justify-between gap-3 p-3 transition hover:bg-acento-suave/50">
          <span class="min-w-0"><span class="block truncate font-semibold">{{ p.titulo }}</span>
            <span class="block truncate text-xs text-suave">{{ catalogo?.familias[p.familia] }} · {{ p.formato }}</span></span>
          <EstadoChip :estado="p.estado" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>
