<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { CircleAlert, FileText, LoaderCircle, NotebookPen, Scale, Sparkles, Upload, X } from "lucide-vue-next";
import { api, subir } from "../api";
import { avisar } from "../composables/avisos";
import EncabezadoPagina from "../components/EncabezadoPagina.vue";
import { mb } from "../utils";

const MAX = 200 * 1024 * 1024;
const router = useRouter();

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
    error.value = `«${f.name}» no es un PPTX. Ábrelo en PowerPoint y guárdalo como .pptx.`;
    return;
  }
  if (f.size > MAX) {
    error.value = `«${f.name}» pesa ${mb(f.size)}: el máximo es 200 MB.`;
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
    error.value = "Primero elige el archivo PPTX.";
    return;
  }
  const datos = new FormData();
  datos.append("archivo", archivo.value);
  datos.append("nombre", nombre.value.trim());
  fase.value = "subiendo";
  avance.value = 0;
  try {
    const { id } = await subir<{ id: string }>("/api/trabajos", datos, (f) => {
      avance.value = f;
      if (f >= 1) fase.value = "leyendo";
    });
    avisar("Listo: leímos tu presentación. Revisa el guion y elige la marca y la voz.");
    router.push(`/cursos/${id}`);
  } catch (e) {
    error.value = (e as Error).message;
    fase.value = "eligiendo";
  }
}

async function abrirEjemplo() {
  try {
    const { id } = await api.post<{ id: string }>("/api/trabajos/ejemplo-csm");
    router.push(`/cursos/${id}`);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <div class="max-w-3xl">
    <EncabezadoPagina titulo="Crear un curso" :migas="[{ texto: 'Cursos', a: '/cursos' }, { texto: 'Crear' }]"
                      subtitulo="Sube la presentación de la capacitación. En unos segundos verás el guion de cada video." />

    <form class="space-y-5" @submit.prevent="enviar" novalidate>
      <!-- Zona para soltar el archivo -->
      <div v-if="!archivo"
           class="relative rounded-2xl border-2 border-dashed px-6 py-12 text-center transition"
           :class="encima ? 'border-acento bg-acento-suave' : 'border-borde bg-superficie hover:border-acento'"
           @dragenter.prevent="encima = true" @dragover.prevent="encima = true" @dragleave.prevent="encima = false" @drop.prevent="soltar">
        <input ref="entrada" id="archivo" type="file" class="absolute inset-0 cursor-pointer opacity-0"
               accept=".pptx,application/vnd.openxmlformats-officedocument.presentationml.presentation"
               aria-describedby="archivo-ayuda" @change="elegir(($event.target as HTMLInputElement).files?.[0])" />
        <span class="mx-auto grid size-14 place-items-center rounded-full bg-acento-suave text-acento"><Upload class="size-6" /></span>
        <p class="mt-4 text-lg font-bold">Arrastra aquí tu archivo PPTX</p>
        <p id="archivo-ayuda" class="mt-1 text-sm text-suave">o <span class="font-semibold text-acento underline">haz clic para buscarlo</span> · hasta 200 MB</p>
      </div>

      <!-- Archivo elegido -->
      <div v-else class="tarjeta flex items-center gap-4 p-4">
        <span class="grid size-12 shrink-0 place-items-center rounded-lg bg-[#D24726]/10 text-[#D24726]"><FileText class="size-6" /></span>
        <div class="min-w-0 flex-1">
          <p class="truncate font-semibold">{{ archivo.name }}</p>
          <p class="text-sm text-suave">{{ mb(archivo.size) }}</p>
          <div v-if="fase === 'subiendo'" class="mt-2 h-2 overflow-hidden rounded-full bg-superficie-2" role="progressbar"
               :aria-valuenow="Math.round(avance * 100)" aria-valuemin="0" aria-valuemax="100" aria-label="Subiendo">
            <div class="h-full rounded-full bg-acento transition-[width]" :style="{ width: `${avance * 100}%` }" />
          </div>
        </div>
        <button v-if="!ocupado" type="button" class="boton-fantasma" aria-label="Quitar este archivo" @click="quitar"><X class="size-4" /></button>
      </div>

      <p v-if="error" class="flex items-start gap-2 rounded-lg bg-error-fondo p-3 text-sm text-error" role="alert">
        <CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ error }}
      </p>

      <div>
        <label for="nombre" class="etiqueta-campo">Nombre del curso <span class="font-normal text-suave">(opcional)</span></label>
        <input id="nombre" v-model="nombre" class="campo" placeholder="Por ejemplo: Conducción segura para mensajeros" autocomplete="off" :disabled="ocupado" />
      </div>

      <button type="submit" class="boton-primario w-full py-3 text-base sm:w-auto" :disabled="ocupado">
        <template v-if="fase === 'subiendo'"><LoaderCircle class="size-5 animate-spin" /> Subiendo… {{ Math.round(avance * 100) }} %</template>
        <template v-else-if="fase === 'leyendo'"><LoaderCircle class="size-5 animate-spin" /> Leyendo la presentación…</template>
        <template v-else>Leer la presentación</template>
      </button>
    </form>

    <section class="mt-12" aria-labelledby="consejos">
      <h2 id="consejos" class="mb-4 text-lg font-bold">Para que el video salga bien</h2>
      <div class="grid gap-3 sm:grid-cols-3">
        <div class="tarjeta p-4">
          <NotebookPen class="size-5 text-acento" />
          <p class="mt-2 font-semibold">El guion va en las notas</p>
          <p class="mt-1 text-sm text-suave">Lo que escribas en las notas del orador es lo que dirá la voz. Una lámina sin notas queda muda.</p>
        </div>
        <div class="tarjeta p-4">
          <FileText class="size-5 text-acento" />
          <p class="mt-2 font-semibold">Una idea por lámina</p>
          <p class="mt-1 text-sm text-suave">Cada lámina se ve mientras la voz la explica. Si tiene demasiado texto, no alcanza a leerse.</p>
        </div>
        <div class="tarjeta p-4">
          <Scale class="size-5 text-acento" />
          <p class="mt-2 font-semibold">Normas completas</p>
          <p class="mt-1 text-sm text-suave">«Ley 1503 de 2011», no «la ley». El estudio te mostrará cada norma y cifra para revisarla.</p>
        </div>
      </div>
      <p class="mt-6 text-sm text-suave">
        ¿No tienes una presentación a mano?
        <button class="inline-flex items-center gap-1 font-semibold text-acento hover:underline" @click="abrirEjemplo">
          <Sparkles class="size-4" /> Mira el ejemplo del curso de conducción segura
        </button>
      </p>
    </section>
  </div>
</template>
