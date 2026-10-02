<script setup lang="ts">
// El editor simple: escena por escena, con la línea de tiempo arriba. No es un editor de video
// completo: cambia el texto de la voz, el movimiento y la transición, y regenera solo esa escena.
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, Mic, Palette } from "@lucide/vue";
import { avisar } from "../composables/avisos";
import {
  abrir, editarNarracion, fijarEscena, generacion, lineaDeTiempo, proyecto, regenerar, restaurarLamina, trabajo,
} from "../composables/proyecto";
import { MENSAJES } from "../mensajes";
import type { LineaDeTiempo } from "../tipos";
import EstadoCarga from "../components/EstadoCarga.vue";
import EstadoGeneracion from "../components/zyvo/EstadoGeneracion.vue";
import LineaTiempo from "../components/zyvo/LineaTiempo.vue";
import TarjetaEscena from "../components/zyvo/TarjetaEscena.vue";

const props = defineProps<{ id: string; clave: string }>();
const router = useRouter();

watch(() => props.id, (id) => { if (proyecto.id !== id || !proyecto.datos) abrir(id); }, { immediate: true });

const video = computed(() => trabajo.value?.videos.find((v) => v.clave === props.clave) ?? null);
const laminas = computed(() => (video.value?.laminas ?? []).map((n) => proyecto.datos!.trabajo.laminas.find((l) => l.n === n)!).filter(Boolean));
const formato = computed(() => trabajo.value?.formatos[0] ?? "16:9");
const escenaDe = (n: number) => {
  const e = trabajo.value?.escena ?? {};
  const propia = e.laminas?.[String(n)] ?? {};
  return { camara: propia.camara ?? e.camara ?? "estatica", transicion: propia.transicion ?? e.transicion ?? "corte" };
};

const linea = ref<LineaDeTiempo | null>(null);
const elegida = ref<number | null>(null);
async function recargarLinea() {
  try { linea.value = await lineaDeTiempo(props.clave); } catch { linea.value = null; }
}
watch(() => [proyecto.datos, generacion.value.produciendo] as const, recargarLinea, { immediate: true });

const ocupado = ref(false);
async function con(f: () => Promise<unknown>, ok?: string) {
  ocupado.value = true;
  try { await f(); if (ok) avisar(ok); } catch (e) { avisar((e as Error).message, "error"); } finally { ocupado.value = false; }
}
function cambiarEscena(n: number, cambio: { camara?: string; transicion?: string }) {
  const e = trabajo.value?.escena ?? {};
  const laminasEscena = { ...(e.laminas ?? {}), [String(n)]: { ...(e.laminas?.[String(n)] ?? {}), ...cambio } };
  return con(() => fijarEscena({ ...e, laminas: laminasEscena }), "Escena actualizada. Regenérala para verla en el video.");
}
function regenerarEscena(n: number) {
  return con(() => regenerar(props.clave, { escena: n }), "Regenerando solo esa escena…");
}
function irA(n: number) {
  elegida.value = n;
  document.getElementById(`escena-${n}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
}
</script>

<template>
  <EstadoCarga v-if="!proyecto.datos" :cargando="proyecto.cargando" :error="proyecto.error" @reintentar="abrir(id)" />
  <div v-else-if="!video" class="py-16 text-center text-suave">Ese video no existe en este proyecto.</div>
  <div v-else class="mx-auto max-w-6xl space-y-5">
    <header class="flex flex-wrap items-center gap-3">
      <button class="boton-fantasma" @click="router.push({ path: `/crear/${id}`, query: { paso: 'listo' } })"><ArrowLeft class="size-4" /> Volver al video</button>
      <div class="min-w-0 flex-1">
        <h1 class="truncate text-xl font-bold">{{ MENSAJES.editor.titulo }}</h1>
        <p class="text-sm text-suave">{{ video.titulo }} · {{ MENSAJES.editor.ayuda }}</p>
      </div>
      <RouterLink class="boton-fantasma" :to="{ path: `/crear/${id}`, query: { paso: 'voz' } }"><Mic class="size-4" /> Cambiar voz</RouterLink>
      <RouterLink class="boton-fantasma" :to="{ path: `/crear/${id}`, query: { paso: 'estilo' } }"><Palette class="size-4" /> Cambiar estilo</RouterLink>
    </header>

    <EstadoGeneracion v-if="generacion.produciendo" :video="generacion.actual" :porcentaje="generacion.porcentaje" />
    <LineaTiempo v-if="linea" :linea="linea" :elegida="elegida" @elegir="irA" />

    <div class="space-y-4">
      <TarjetaEscena v-for="(l, i) in laminas" :id="`escena-${l.n}`" :key="l.n" :trabajo="id" :lamina="l" :numero="i + 1" :formato="formato"
                     :catalogo="proyecto.escena!" v-bind="escenaDe(l.n)" :ocupado="ocupado || generacion.produciendo"
                     @narracion="(t) => con(() => editarNarracion(l.n, t), 'Texto guardado. Regenera para escucharlo.')"
                     @restaurar="con(() => restaurarLamina(l.n), 'Volvió el texto original de la presentación.')"
                     @escena="(c) => cambiarEscena(l.n, c)" @regenerar="regenerarEscena(l.n)" />
    </div>
  </div>
</template>
