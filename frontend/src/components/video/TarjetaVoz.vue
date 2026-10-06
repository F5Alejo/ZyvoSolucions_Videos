<script setup lang="ts">
// Una voz para elegir: su nombre humano, cómo suena y el botón «Escuchar». Nada de proveedores ni modelos.
import { onUnmounted, ref } from "vue";
import { CircleCheck, LoaderCircle, Pause, Play } from "@lucide/vue";
import { MENSAJES } from "../../mensajes";
import type { Voz } from "../../tipos";

const props = defineProps<{ voz: Voz; elegida: boolean }>();
defineEmits<{ elegir: [] }>();

const sonando = ref(false);
const cargando = ref(false);
const error = ref<string | null>(null);
let audio: HTMLAudioElement | null = null;

/** El nombre sin el proveedor: «Dora · Kokoro» → «Dora». */
const nombre = props.voz.nombre.split("·")[0]!.trim();
/** La primera idea de la descripción, sin detalles de licencia. */
const como = props.voz.descripcion.split(/[.:(]/)[0]!.trim();

async function escuchar() {
  if (sonando.value && audio) {
    audio.pause();
    return;
  }
  document.querySelectorAll("video, audio").forEach((m) => (m as HTMLMediaElement).pause());
  error.value = null;
  cargando.value = true;
  audio = new Audio(props.voz.muestra_url ?? `/api/voces/${props.voz.id}/muestra`);
  audio.onplaying = () => { cargando.value = false; sonando.value = true; };
  audio.onpause = audio.onended = () => { sonando.value = false; };
  audio.onerror = () => { cargando.value = false; sonando.value = false; error.value = "No pudimos reproducir la muestra."; };
  audio.play().catch(() => { cargando.value = false; });
}
onUnmounted(() => audio?.pause());
</script>

<template>
  <div class="tarjeta flex items-center gap-4 p-4 transition" :class="[elegida ? 'ring-2 ring-acento' : '', voz.falta ? 'opacity-60' : 'hover:shadow-md']">
    <button type="button" class="grid size-12 shrink-0 place-items-center rounded-full text-white transition disabled:opacity-40"
            :class="voz.falta ? 'bg-suave' : 'chispa hover:brightness-110'" :disabled="!!voz.falta"
            :aria-label="`${sonando ? 'Pausar' : MENSAJES.voz.escuchar} a ${nombre}`" @click="escuchar">
      <LoaderCircle v-if="cargando" class="size-5 animate-spin" /><Pause v-else-if="sonando" class="size-5" /><Play v-else class="size-5 translate-x-px" />
    </button>
    <button type="button" class="min-w-0 flex-1 text-left disabled:cursor-not-allowed" :disabled="!!voz.falta" :aria-pressed="elegida" @click="$emit('elegir')">
      <p class="flex items-center gap-2 font-bold">{{ nombre }} <CircleCheck v-if="elegida" class="size-4 text-acento" /></p>
      <p class="text-sm text-suave">{{ como }}</p>
      <p v-if="voz.falta" class="mt-1 text-xs font-semibold text-aviso">{{ MENSAJES.voz.noDisponible }}</p>
      <p v-else-if="voz.solo_borrador" class="mt-1 text-xs font-semibold text-aviso">{{ MENSAJES.voz.borrador }}</p>
      <p v-if="error" class="mt-1 text-xs text-error">{{ error }}</p>
    </button>
  </div>
</template>
