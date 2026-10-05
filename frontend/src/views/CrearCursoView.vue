<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { CircleAlert, CircleHelp, FileText, LoaderCircle, NotebookPen, Scale, Sparkles, Upload, X } from "@lucide/vue";
import { api, subir } from "../api";
import { avisar } from "../composables/avisos";
import { abrirAyuda } from "../composables/ayuda";
import { catalogo } from "../composables/catalogo";
import { mb } from "../utils";

const MAX = 200 * 1024 * 1024;
const router = useRouter();
const ruta = useRoute();
/** Si se llega desde una empresa (?marca=id), el curso nace con su marca y su voz. */
const empresa = computed(() => {
  const id = typeof ruta.query.marca === "string" ? ruta.query.marca : "";
  return catalogo.value?.marcas[id] ?? null;
});

const archivo = ref<File | null>(null);
const nombre = ref("");
const encima = ref(false);
const error = ref<string | null>(null);
const fase = ref<"eligiendo" | "subiendo" | "leyendo">("eligiendo");
const avance = ref(0);
const entrada = ref<HTMLInputElement | null>(null);
const ocupado = computed(() => fase.value !== "eligiendo");

function elegir(f: File | undefined) {
  error.value = null;
  if (!f) return;
  if (!f.name.toLowerCase().endsWith(".pptx")) {
    error.value = `«${f.name}» no es una presentación de PowerPoint (.pptx). Ábrela en PowerPoint y usa Archivo → Guardar como → .pptx.`;
    return;
  }
  if (f.size > MAX) {
    error.value = `«${f.name}» pesa ${mb(f.size)} y el máximo es 200 MB. Prueba comprimiendo sus imágenes en PowerPoint.`;
    return;
  }
  archivo.value = f;
  if (!nombre.value) nombre.value = f.name.replace(/\.pptx$/i, "").replace(/[-_]+/g, " ");
}

function soltar(e: DragEvent) {
  encima.value = false;
  elegir(e.dataTransfer?.files[0]);
}

function quitar() {
  archivo.value = null;
  if (entrada.value) entrada.value.value = "";
}

async function enviar() {
  if (!archivo.value) {
    error.value = "Primero elige tu presentación.";
    return;
  }
  const datos = new FormData();
  datos.append("archivo", archivo.value);
  datos.append("nombre", nombre.value.trim());
  if (empresa.value) datos.append("marca", empresa.value.id);
  fase.value = "subiendo";
  avance.value = 0;
  try {
    const { id } = await subir<{ id: string }>("/api/trabajos", datos, (f) => {
      avance.value = f;
      if (f >= 1) fase.value = "leyendo";
    });
    router.push(`/cursos/${id}/asistente`);
  } catch (e) {
    error.value = (e as Error).message;
    fase.value = "eligiendo";
  }
}

async function abrirEjemplo() {
  try {
    const { id } = await api.post<{ id: string }>("/api/trabajos/ejemplo-csm");
    router.push(`/cursos/${id}/asistente`);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <!-- Cabecera con el caballero del manual (banner del modo oscuro, recortado sin el logo) -->
    <header class="relative isolate mb-8 overflow-hidden rounded-3xl border border-[#272725] bg-[#020202] px-6 py-12 text-white sm:px-10">
      <!-- El caballero a la derecha; el texto, sobre negro limpio a la izquierda -->
      <img src="/marca/banco/caballero-hud.webp" alt="" aria-hidden="true"
           class="absolute inset-y-0 right-0 -z-10 h-full w-[45%] object-cover object-[0%_50%] opacity-95 [mask-image:linear-gradient(to_left,black_75%,transparent)]" />
      <p class="text-sm font-semibold tracking-[0.2em] text-[#C8951A] uppercase">Crear un curso</p>
      <h1 class="mt-3 text-3xl font-bold sm:text-4xl">Sube tu presentación</h1>
      <p class="mt-3 max-w-sm text-white/75">La leemos en segundos y te mostramos cómo quedaría cada video. Después eliges la marca y la voz.</p>
    </header>

    <div v-if="empresa" class="tarjeta mb-5 flex items-center gap-4 rounded-2xl p-4">
      <span class="grid h-12 w-20 shrink-0 place-items-center rounded-lg border border-borde" :class="empresa.logo?.fondo === 'oscuro' ? 'bg-[#0b0d0f]' : 'bg-white'">
        <img v-if="empresa.logo_url" :src="empresa.logo_url" alt="" class="max-h-8 max-w-16 object-contain" />
        <span v-else class="text-xs font-bold text-[#111]">{{ empresa.nombre_corto }}</span>
      </span>
      <p class="min-w-0 flex-1 text-sm">Curso para <strong>{{ empresa.nombre_corto }}</strong><span class="block text-suave">Saldrá con sus colores, su logo y su voz.</span></p>
      <RouterLink to="/cursos/nuevo" class="boton-fantasma text-sm">Cambiar</RouterLink>
    </div>

    <form class="space-y-5" @submit.prevent="enviar" novalidate>
      <!-- Zona para soltar el archivo -->
      <div v-if="!archivo"
           class="relative rounded-3xl border-2 border-dashed px-6 py-14 text-center transition"
           :class="encima ? 'scale-[1.01] border-acento bg-acento-suave' : 'border-borde bg-superficie hover:border-acento hover:bg-acento-suave/40'"
           @dragenter.prevent="encima = true" @dragover.prevent="encima = true" @dragleave.prevent="encima = false" @drop.prevent="soltar">
        <input ref="entrada" id="archivo" type="file" class="absolute inset-0 cursor-pointer opacity-0"
               accept=".pptx,application/vnd.openxmlformats-officedocument.presentationml.presentation"
               aria-describedby="archivo-ayuda" @change="elegir(($event.target as HTMLInputElement).files?.[0])" />
        <span class="mx-auto grid size-16 place-items-center rounded-2xl bg-acento text-sobre-acento shadow-lg shadow-acento/30"><Upload class="size-7" /></span>
        <p class="mt-5 text-xl font-bold">Arrastra aquí tu archivo de PowerPoint</p>
        <p id="archivo-ayuda" class="mt-1.5 text-suave">o <span class="font-semibold text-acento underline underline-offset-4">haz clic para buscarlo</span> en tu equipo</p>
        <p class="mt-4 text-xs text-suave">Archivos .pptx de hasta 200 MB</p>
      </div>

      <!-- Archivo elegido -->
      <div v-else class="tarjeta flex items-center gap-4 rounded-2xl p-5">
        <span class="grid size-14 shrink-0 place-items-center rounded-xl bg-[#C43E1C]/10 text-[#C43E1C]"><FileText class="size-7" /></span>
        <div class="min-w-0 flex-1">
          <p class="truncate font-bold">{{ archivo.name }}</p>
          <p class="text-sm text-suave">
            <template v-if="fase === 'subiendo'">Subiendo… {{ Math.round(avance * 100) }} %</template>
            <template v-else-if="fase === 'leyendo'">Leyendo cada diapositiva…</template>
            <template v-else>{{ mb(archivo.size) }} · listo para leer</template>
          </p>
          <div v-if="ocupado" class="mt-2 h-2 overflow-hidden rounded-full bg-superficie-2" role="progressbar"
               :aria-valuenow="Math.round(avance * 100)" aria-valuemin="0" aria-valuemax="100" aria-label="Avance">
            <div class="h-full rounded-full bg-acento transition-[width] duration-300"
                 :class="fase === 'leyendo' && 'animate-pulse'" :style="{ width: `${fase === 'leyendo' ? 100 : avance * 100}%` }" />
          </div>
        </div>
        <button v-if="!ocupado" type="button" class="boton-fantasma" aria-label="Quitar este archivo" @click="quitar"><X class="size-5" /></button>
      </div>

      <p v-if="error" class="flex items-start gap-2 rounded-xl bg-error-fondo p-4 text-sm text-error" role="alert">
        <CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ error }}
      </p>

      <div v-if="archivo">
        <label for="nombre" class="etiqueta-campo">¿Cómo se llama el curso?</label>
        <input id="nombre" v-model="nombre" class="campo py-3 text-base" placeholder="Por ejemplo: Conducción segura para mensajeros"
               autocomplete="off" :disabled="ocupado" />
        <p class="mt-1.5 text-xs text-suave">Puedes dejar el que propusimos.</p>
      </div>

      <button v-if="archivo" type="submit" class="boton-primario w-full py-4 text-base" :disabled="ocupado">
        <LoaderCircle v-if="ocupado" class="size-5 animate-spin" />
        {{ ocupado ? "Un momento…" : "Leer mi presentación" }}
      </button>
    </form>

    <section class="mt-14" aria-labelledby="consejos">
      <h2 id="consejos" class="mb-4 text-center text-lg font-bold">Para que tus videos salgan bien</h2>
      <div class="grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-3">
        <div class="tarjeta rounded-2xl p-5">
          <NotebookPen class="size-6 text-acento" />
          <p class="mt-3 font-bold">Escribe el guion en las notas</p>
          <p class="mt-1 text-sm text-suave">Lo que escribas en las notas del orador es lo que dirá la voz.</p>
          <button class="mt-2 inline-flex items-center gap-1 text-sm font-semibold text-acento hover:underline" @click="abrirAyuda('notas')">
            <CircleHelp class="size-4" /> ¿Dónde están?
          </button>
        </div>
        <div class="tarjeta rounded-2xl p-5">
          <FileText class="size-6 text-acento" />
          <p class="mt-3 font-bold">Una idea por diapositiva</p>
          <p class="mt-1 text-sm text-suave">Cada diapositiva se ve mientras la voz la explica. Con mucho texto, no alcanza a leerse.</p>
        </div>
        <div class="tarjeta rounded-2xl p-5">
          <Scale class="size-6 text-acento" />
          <p class="mt-3 font-bold">Normas completas</p>
          <p class="mt-1 text-sm text-suave">Escribe «Ley 1503 de 2011», no «la ley». Te las mostraremos para revisarlas.</p>
        </div>
      </div>
      <p class="mt-8 text-center text-sm text-suave">
        ¿Quieres ver cómo funciona antes?
        <button class="inline-flex items-center gap-1 font-semibold text-acento hover:underline" @click="abrirEjemplo">
          <Sparkles class="size-4" /> Prueba con un curso de ejemplo
        </button>
      </p>
    </section>
  </div>
</template>
