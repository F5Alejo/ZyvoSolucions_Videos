<script setup lang="ts">
// Arrastrar o elegir el PPTX. Revisa el archivo antes de subirlo y muestra el avance de la subida.
import { ref } from "vue";
import { CircleAlert, FileText, LoaderCircle, Upload } from "@lucide/vue";
import { MENSAJES } from "../../mensajes";
import { mb } from "../../utils";

const MAX = 200 * 1024 * 1024;
defineProps<{ avance: number | null }>();
const emit = defineEmits<{ elegido: [File] }>();

const encima = ref(false);
const error = ref<string | null>(null);
const nombre = ref<string | null>(null);

function elegir(f: File | undefined) {
  error.value = null;
  if (!f) return;
  if (!f.name.toLowerCase().endsWith(".pptx")) return void (error.value = MENSAJES.subir.noEsPptx(f.name));
  if (f.size > MAX) return void (error.value = MENSAJES.subir.muyGrande(f.name, mb(f.size)));
  nombre.value = f.name;
  emit("elegido", f);
}
</script>

<template>
  <div>
    <div class="relative rounded-3xl border-2 border-dashed px-6 py-14 text-center transition"
         :class="encima ? 'scale-[1.01] border-acento bg-acento-suave' : 'border-borde bg-superficie hover:border-acento'"
         @dragenter.prevent="encima = true" @dragover.prevent="encima = true" @dragleave.prevent="encima = false"
         @drop.prevent="encima = false; elegir($event.dataTransfer?.files[0])">
      <input v-if="avance === null" type="file" class="absolute inset-0 cursor-pointer opacity-0" aria-describedby="zona-ayuda"
             accept=".pptx,application/vnd.openxmlformats-officedocument.presentationml.presentation"
             :aria-label="MENSAJES.subir.zona" @change="elegir(($event.target as HTMLInputElement).files?.[0])" />
      <template v-if="avance === null">
        <span class="chispa mx-auto grid size-16 place-items-center rounded-2xl text-white shadow-lg"><Upload class="size-7" /></span>
        <p class="mt-5 text-xl font-bold">{{ MENSAJES.subir.zona }}</p>
        <p id="zona-ayuda" class="mt-1 text-sm text-suave">
          <span class="font-semibold text-acento underline">{{ MENSAJES.subir.o }}</span> · {{ MENSAJES.subir.limite }}
        </p>
      </template>
      <template v-else>
        <span class="mx-auto grid size-16 place-items-center rounded-2xl bg-acento-suave text-acento"><FileText class="size-7" /></span>
        <p class="mt-5 truncate font-semibold">{{ nombre }}</p>
        <div class="mx-auto mt-3 h-2 max-w-sm overflow-hidden rounded-full bg-superficie-2" role="progressbar"
             :aria-valuenow="Math.round(avance * 100)" aria-valuemin="0" aria-valuemax="100" aria-label="Subiendo la presentación">
          <div class="chispa h-full rounded-full transition-[width]" :style="{ width: `${avance * 100}%` }" />
        </div>
        <p class="mt-2 flex items-center justify-center gap-2 text-sm text-suave">
          <LoaderCircle class="size-4 animate-spin" /> {{ avance < 1 ? `Subiendo… ${Math.round(avance * 100)} %` : "Leyendo la presentación…" }}
        </p>
      </template>
    </div>
    <p v-if="error" class="mt-3 flex items-start gap-2 rounded-lg bg-error-fondo p-3 text-sm text-error" role="alert">
      <CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ error }}
    </p>
  </div>
</template>
