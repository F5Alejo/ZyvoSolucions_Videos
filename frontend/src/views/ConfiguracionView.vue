<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { CircleAlert, CircleCheck, LoaderCircle, Music, RefreshCw, Save, Undo2, Upload } from "lucide-vue-next";
import { api, subir } from "../api";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import { useCarga } from "../composables/carga";
import AjustesVideoForm from "../components/AjustesVideoForm.vue";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import type { Configuracion, PistaMusica, RespuestaConfig, Sistema } from "../tipos";

const { datos: respuesta, cargando, error, recargar } = useCarga(() => api.get<RespuestaConfig>("/api/configuracion"));
const sistema = ref<Sistema | null>(null);
const revisando = ref(false);

// Se edita una copia; «Guardar» la manda entera y el servidor la valida.
const borrador = ref<Configuracion | null>(null);
const musica = ref<PistaMusica[]>([]);
watch(respuesta, (r) => {
  if (!r) return;
  borrador.value = structuredClone(r.configuracion);
  musica.value = r.musica;
}, { immediate: true });

const hayCambios = computed(() => !!respuesta.value && JSON.stringify(borrador.value) !== JSON.stringify(respuesta.value.configuracion));
const guardando = ref(false);

async function guardar() {
  if (!borrador.value) return;
  guardando.value = true;
  try {
    respuesta.value = await api.put<RespuestaConfig>("/api/configuracion", borrador.value);
    avisar("Configuración guardada.");
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    guardando.value = false;
  }
}

function descartar() {
  if (respuesta.value) borrador.value = structuredClone(respuesta.value.configuracion);
}

async function revisarSistema(forzar = false) {
  revisando.value = true;
  try {
    sistema.value = await api.get<Sistema>(`/api/sistema${forzar ? "?forzar=true" : ""}`);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    revisando.value = false;
  }
}
revisarSistema();

// ── Música ──
const archivoMusica = ref<File | null>(null);
const licencia = ref("");
const fuente = ref("");
const subiendo = ref(false);
async function subirMusica() {
  if (!archivoMusica.value) return;
  const d = new FormData();
  d.append("archivo", archivoMusica.value);
  d.append("licencia", licencia.value);
  d.append("fuente", fuente.value);
  subiendo.value = true;
  try {
    musica.value = await subir<PistaMusica[]>("/api/musica", d, () => {});
    avisar("Pista agregada. Elígela en Audio → Música de fondo.");
    archivoMusica.value = null;
    licencia.value = fuente.value = "";
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    subiendo.value = false;
  }
}

const AGENTES: { id: string; nombre: string; que: string }[] = [
  { id: "redactor", nombre: "Redactor de pantalla", que: "Títulos y viñetas cortas a partir de los párrafos del PPTX" },
  { id: "director", nombre: "Director de animación", que: "Elige plantilla y efectos por lámina" },
  { id: "guionista", nombre: "Guionista", que: "Narración para láminas sin notas y videos muy largos" },
  { id: "verificador", nombre: "Verificador normativo", que: "Cifras y normas que necesitan fuente" },
  { id: "evaluador", nombre: "Evaluador", que: "Preguntas por video, exportables a Moodle" },
  { id: "publicador", nombre: "Publicador", que: "Título, descripción, etiquetas y capítulos para YouTube" },
  { id: "descriptor", nombre: "Descriptor de imágenes", que: "Texto alternativo y fotos contra logos" },
  { id: "revisor_voz", nombre: "Revisor de voz", que: "Compara lo que dijo la voz con el guion" },
];

const REVISIONES = [
  { clave: "ffmpeg", titulo: "ffmpeg", para: "Codificar los videos" },
  { clave: "chromium", titulo: "Navegador de escenas", para: "Dibujar las láminas" },
  { clave: "elevenlabs", titulo: "Clave de ElevenLabs", para: "Voces de pago (Carlos)" },
  { clave: "ollama", titulo: "Ollama", para: "Los agentes con IA local" },
  { clave: "disco", titulo: "Espacio en disco", para: "Videos y caché de voz" },
] as const;
</script>

<template>
  <EstadoCarga v-if="!respuesta || !borrador" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="pb-24">
    <EncabezadoPagina titulo="Configuración" subtitulo="Cómo se producen los videos, qué usan los cursos nuevos y qué tiene este equipo." />

    <!-- Diagnóstico -->
    <section aria-labelledby="t-sistema" class="mb-10">
      <div class="mb-3 flex items-center justify-between gap-3">
        <h2 id="t-sistema" class="text-lg font-bold">Este equipo</h2>
        <button class="boton-fantasma" :disabled="revisando" @click="revisarSistema(true)">
          <RefreshCw class="size-4" :class="{ 'animate-spin': revisando }" /> Revisar otra vez
        </button>
      </div>
      <div v-if="!sistema" class="flex items-center gap-2 text-sm text-suave"><LoaderCircle class="size-4 animate-spin" /> Revisando…</div>
      <ul v-else class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <li v-for="x in REVISIONES" :key="x.clave" class="tarjeta flex items-start gap-3 p-4">
          <CircleCheck v-if="sistema[x.clave].ok" class="mt-0.5 size-5 shrink-0 text-exito" aria-label="Bien" />
          <CircleAlert v-else class="mt-0.5 size-5 shrink-0 text-aviso" aria-label="Falta algo" />
          <span class="min-w-0">
            <strong class="block text-sm">{{ x.titulo }}</strong>
            <span class="block text-xs text-suave">{{ x.para }} · {{ sistema[x.clave].detalle }}</span>
            <code v-if="sistema[x.clave].arreglo" class="mt-1 block text-xs break-all text-acento">{{ sistema[x.clave].arreglo }}</code>
          </span>
        </li>
        <li class="tarjeta p-4 sm:col-span-2 xl:col-span-1">
          <strong class="block text-sm">Voces</strong>
          <ul class="mt-1 space-y-0.5 text-xs">
            <li v-for="v in sistema.voces" :key="v.id" class="flex justify-between gap-2">
              <span>{{ v.nombre }}</span><span :class="v.ok ? 'text-exito' : 'text-aviso'">{{ v.detalle }}</span>
            </li>
          </ul>
        </li>
      </ul>
    </section>

    <!-- Cursos nuevos -->
    <section aria-labelledby="t-cursos" class="mb-10">
      <h2 id="t-cursos" class="mb-1 text-lg font-bold">Cursos nuevos</h2>
      <p class="mb-3 text-sm text-suave">Con esto empieza cada curso que se sube. Después se puede cambiar en el curso.</p>
      <div class="tarjeta grid gap-4 p-5 sm:grid-cols-3">
        <label class="block"><span class="etiqueta-campo">Marca</span>
          <select v-model="borrador.cursos.marca" class="campo">
            <option v-for="m in catalogo?.marcas" :key="m.id" :value="m.id">{{ m.nombre_corto }}</option>
          </select></label>
        <label class="block"><span class="etiqueta-campo">Voz</span>
          <select v-model="borrador.cursos.voz" class="campo">
            <option v-for="v in catalogo?.voces" :key="v.id" :value="v.id">{{ v.nombre }}{{ v.falta ? " (no disponible)" : "" }}</option>
          </select></label>
        <fieldset><legend class="etiqueta-campo">Formatos</legend>
          <label v-for="f in ['16:9', '9:16']" :key="f" class="mr-4 inline-flex items-center gap-2 text-sm">
            <input v-model="borrador.cursos.formatos" type="checkbox" :value="f" class="size-4 accent-[var(--c-acento)]" /> {{ f }}
          </label></fieldset>
      </div>
    </section>

    <!-- Producción -->
    <section aria-labelledby="t-produccion" class="mb-10">
      <h2 id="t-produccion" class="mb-1 text-lg font-bold">Producción</h2>
      <p class="mb-3 text-sm text-suave">Cada curso puede cambiar estos ajustes para sí mismo en su paso «Marca y voz».</p>
      <AjustesVideoForm v-model="borrador" :opciones="respuesta.opciones" :musica="musica" />
    </section>

    <!-- Música -->
    <section aria-labelledby="t-musica" class="mb-10">
      <h2 id="t-musica" class="mb-1 text-lg font-bold">Música</h2>
      <p class="mb-3 text-sm text-suave">
        Los videos se entregan a clientes: sube solo pistas con licencia de uso comercial
        (p. ej. Pixabay Music o la biblioteca de audio de YouTube) y anota cuál es. Se quedan en este equipo.
      </p>
      <div class="grid gap-4 lg:grid-cols-2">
        <ul class="tarjeta divide-y divide-borde">
          <li v-if="!musica.length" class="p-4 text-sm text-suave">Todavía no hay pistas.</li>
          <li v-for="m in musica" :key="m.archivo" class="flex flex-wrap items-center gap-3 p-4">
            <Music class="size-5 shrink-0 text-acento" />
            <span class="min-w-0 flex-1"><strong class="block truncate text-sm">{{ m.archivo }}</strong>
              <span class="text-xs text-suave">{{ m.licencia ?? "Sin licencia registrada" }}{{ m.fuente ? ` · ${m.fuente}` : "" }}</span></span>
            <audio controls preload="none" :src="`/api/musica/${encodeURIComponent(m.archivo)}`" class="h-8 w-full sm:w-56" />
          </li>
        </ul>
        <form class="tarjeta space-y-3 p-5" @submit.prevent="subirMusica">
          <label class="block"><span class="etiqueta-campo">Archivo (mp3, wav, m4a, ogg o flac)</span>
            <input type="file" accept=".mp3,.wav,.m4a,.ogg,.flac" class="campo" required
                   @change="archivoMusica = ($event.target as HTMLInputElement).files?.[0] ?? null" /></label>
          <label class="block"><span class="etiqueta-campo">Licencia</span>
            <input v-model="licencia" class="campo" required minlength="3" placeholder="Pixabay Content License" /></label>
          <label class="block"><span class="etiqueta-campo">De dónde sale (opcional)</span>
            <input v-model="fuente" class="campo" placeholder="https://pixabay.com/music/…" /></label>
          <button class="boton-secundario" :disabled="subiendo || !archivoMusica">
            <LoaderCircle v-if="subiendo" class="size-4 animate-spin" /><Upload v-else class="size-4" /> Subir pista
          </button>
        </form>
      </div>
    </section>

    <!-- Agentes -->
    <section aria-labelledby="t-agentes" class="mb-10">
      <h2 id="t-agentes" class="mb-1 text-lg font-bold">Agentes con IA local (Ollama)</h2>
      <p class="mb-3 text-sm text-suave">Proponen mejoras que alguien acepta o descarta; nunca cambian nada solos. Sin Ollama usan reglas simples.</p>
      <div class="tarjeta grid gap-4 p-5 sm:grid-cols-3">
        <label class="block"><span class="etiqueta-campo">Dirección de Ollama</span><input v-model="borrador.agentes.url" class="campo" /></label>
        <label class="block"><span class="etiqueta-campo">Modelo de texto</span><input v-model="borrador.agentes.modelo_texto" class="campo" /></label>
        <label class="block"><span class="etiqueta-campo">Modelo con visión</span><input v-model="borrador.agentes.modelo_vision" class="campo" /></label>
      </div>
      <ul class="mt-3 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <li v-for="a in AGENTES" :key="a.id">
          <label class="tarjeta flex h-full cursor-pointer items-start gap-3 p-4">
            <input v-model="borrador.agentes.activos[a.id]" type="checkbox" class="mt-1 size-4 accent-[var(--c-acento)]" />
            <span><strong class="block text-sm">{{ a.nombre }}</strong><span class="text-xs text-suave">{{ a.que }}</span></span>
          </label>
        </li>
      </ul>
    </section>

    <!-- Guardar -->
    <div v-if="hayCambios" class="fixed right-4 bottom-4 left-4 z-30 flex flex-wrap items-center justify-end gap-3 rounded-xl border border-borde bg-superficie p-3 shadow-lg lg:left-[276px]"
         role="region" aria-label="Cambios sin guardar">
      <span class="mr-auto text-sm font-semibold">Hay cambios sin guardar</span>
      <button class="boton-fantasma" @click="descartar"><Undo2 class="size-4" /> Descartar</button>
      <button class="boton-primario" :disabled="guardando" @click="guardar">
        <LoaderCircle v-if="guardando" class="size-4 animate-spin" /><Save v-else class="size-4" /> Guardar cambios
      </button>
    </div>
  </div>
</template>
