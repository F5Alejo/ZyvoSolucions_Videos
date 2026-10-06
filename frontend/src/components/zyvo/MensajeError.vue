<script setup lang="ts">
// Un problema dicho para la persona, con qué hacer. El detalle técnico solo en «Modo diagnóstico».
import { computed, ref } from "vue";
import { ChevronDown, TriangleAlert } from "@lucide/vue";
import { api } from "../../api";
import { mensajeHumano } from "../../generacion";
import { MENSAJES, RECUPERACIONES } from "../../mensajes";
import type { EventoRegistro } from "../../tipos";

const props = defineProps<{ mensaje: string | null; recuperacion?: string | null; codigo?: string | null; trabajo?: string; clave?: string }>();
defineEmits<{ accion: ["voz" | "reintentar" | "curso" | "diagnostico"] }>();

const sugerencia = computed(() => RECUPERACIONES[props.recuperacion ?? ""] ?? RECUPERACIONES.REINTENTAR!);
const eventos = ref<EventoRegistro[] | null>(null);

async function diagnostico(e: Event) {
  if (!(e.target as HTMLDetailsElement).open || eventos.value || !props.trabajo || !props.clave) return;
  eventos.value = (await api.get<{ eventos: EventoRegistro[] }>(`/api/trabajos/${props.trabajo}/diagnostico/${props.clave}`)).eventos;
}
</script>

<template>
  <section class="rounded-2xl border border-aviso/40 bg-aviso-fondo p-5" role="alert">
    <p class="flex items-center gap-2 font-bold text-aviso"><TriangleAlert class="size-5" /> {{ MENSAJES.generar.fallo }}</p>
    <p class="mt-2 text-texto">{{ mensajeHumano(mensaje) }}</p>
    <p class="mt-1 text-sm text-suave">{{ sugerencia.texto }}</p>
    <div class="mt-4 flex flex-wrap gap-2">
      <button v-if="sugerencia.accion === 'voz'" class="boton-primario" @click="$emit('accion', 'voz')">Elegir otra voz</button>
      <button v-if="sugerencia.accion === 'curso'" class="boton-primario" @click="$emit('accion', 'curso')">Revisar la presentación</button>
      <button class="boton-secundario" @click="$emit('accion', 'reintentar')">Intentar de nuevo</button>
    </div>
    <details v-if="trabajo && clave" class="group mt-4 text-sm" @toggle="diagnostico">
      <summary class="flex cursor-pointer items-center gap-1 text-suave select-none hover:text-texto">
        <ChevronDown class="size-4 transition group-open:rotate-180" /> Modo diagnóstico
      </summary>
      <p class="mt-2 text-xs text-suave">Para quien da soporte técnico. Código: <code>{{ codigo ?? "—" }}</code></p>
      <ol v-if="eventos" class="mt-2 max-h-64 space-y-1 overflow-auto rounded-lg bg-superficie p-3 font-mono text-xs">
        <li v-for="(x, i) in eventos" :key="i" :class="x.status === 'error' ? 'text-error' : 'text-suave'">
          {{ x.timestamp.slice(11, 19) }} · {{ x.stage }} · {{ x.status }}<template v-if="x.retry"> · intento {{ x.retry }}</template>
          <template v-if="x.error_code"> · {{ x.error_code }}</template><template v-if="x.message"> · {{ x.message }}</template>
          <pre v-if="x.stacktrace" class="mt-1 whitespace-pre-wrap opacity-80">{{ x.stacktrace }}</pre>
        </li>
      </ol>
    </details>
  </section>
</template>
