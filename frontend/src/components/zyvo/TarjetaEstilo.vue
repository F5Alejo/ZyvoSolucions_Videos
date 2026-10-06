<script setup lang="ts">
// Un estilo como tarjeta visual, con una vista previa animada en miniatura de cómo se mueve.
import { CircleCheck } from "@lucide/vue";
import type { Estilo } from "../../tipos";

defineProps<{ estilo: Estilo; elegido: boolean }>();
defineEmits<{ elegir: [] }>();
</script>

<template>
  <button type="button" class="group tarjeta relative flex flex-col overflow-hidden text-left transition hover:-translate-y-0.5 hover:shadow-lg"
          :class="elegido ? 'ring-2 ring-acento' : ''" :aria-pressed="elegido" @click="$emit('elegir')">
    <!-- Miniatura: una lámina que entra y se mueve como lo haría con este estilo -->
    <div class="relative aspect-video overflow-hidden bg-[#0B0B12]" aria-hidden="true">
      <div class="lienzo absolute inset-0 p-[9%]" :class="[`cam-${estilo.camara}`, `tr-${estilo.transicion}`]">
        <div class="anim" :class="`an-${estilo.animacion}`">
          <i class="titulo" /><i class="linea" />
          <i class="vineta" /><i class="vineta" /><i class="vineta" />
        </div>
      </div>
      <span v-if="estilo.formato === '9:16'" class="absolute top-2 right-2 rounded-md bg-white/15 px-1.5 py-0.5 text-[10px] font-bold text-white">Vertical</span>
    </div>
    <div class="flex flex-1 flex-col p-4">
      <p class="flex items-center gap-2 font-bold"><span class="text-xl">{{ estilo.icono }}</span> {{ estilo.nombre }}
        <CircleCheck v-if="elegido" class="ml-auto size-5 text-acento" /></p>
      <p class="mt-1 text-sm text-suave">{{ estilo.descripcion }}</p>
      <p class="mt-3 flex flex-wrap gap-1.5 text-[11px] font-semibold text-suave">
        <span class="rounded-full bg-superficie-2 px-2 py-0.5">{{ estilo.camara_nombre }}</span>
        <span class="rounded-full bg-superficie-2 px-2 py-0.5">{{ estilo.transicion_nombre }}</span>
        <span v-if="estilo.musica_nombre" class="rounded-full bg-superficie-2 px-2 py-0.5">Música {{ estilo.musica_nombre.toLowerCase() }}</span>
        <span v-if="estilo.subtitulos_quemados" class="rounded-full bg-superficie-2 px-2 py-0.5">Subtítulos en la imagen</span>
      </p>
    </div>
  </button>
</template>

<style scoped>
/* Todo en un ciclo de 4 s que se repite: entra, se queda (con la cámara) y sale según la transición. */
/* Alturas con padding-top: un % de alto no se resuelve dentro de la grilla; el de padding va contra el ancho. */
.anim { display: flex; flex-direction: column; justify-content: center; gap: 6px; height: 100%; }
.anim i { display: block; border-radius: 3px; background: #E9E7F7; padding-top: 5%; }
.anim .titulo { width: 70%; padding-top: 8%; }
.anim .linea { width: 22%; padding-top: 2%; background: #8B7CF6; }
.anim .vineta { width: 55%; background: #6E6A86; }
.anim .vineta:nth-child(4) { width: 46%; }
.anim .vineta:nth-child(5) { width: 38%; }
.anim > i { animation: 4s infinite both; }
.anim > i:nth-child(2) { animation-delay: .1s; } .anim > i:nth-child(3) { animation-delay: .2s; }
.anim > i:nth-child(4) { animation-delay: .3s; } .anim > i:nth-child(5) { animation-delay: .4s; }

.an-sobria > i { animation-name: sobria; }
.an-dinamica > i { animation-name: dinamica; }
.an-cinetica > i { animation-name: cinetica; }
.an-corporativa > i { animation-name: corporativa; }
.an-minima > i { animation-name: minima; }
@keyframes sobria { 0% { opacity: 0 } 20%, 85% { opacity: 1 } 100% { opacity: 0 } }
@keyframes dinamica { 0% { opacity: 0; transform: translateY(40%) } 18%, 82% { opacity: 1; transform: none } 100% { opacity: 0; transform: translateY(-40%) } }
@keyframes cinetica { 0% { opacity: 0; transform: scale(.4) } 12% { opacity: 1; transform: scale(1.12) } 18%, 85% { transform: scale(1) } 100% { opacity: 0 } }
@keyframes corporativa { 0% { clip-path: inset(0 100% 0 0) } 22%, 82% { clip-path: inset(0 0 0 0) } 100% { clip-path: inset(0 0 0 0); transform: translateX(-30%); opacity: 0 } }
@keyframes minima { 0% { opacity: 0 } 8%, 100% { opacity: 1 } }

.lienzo { animation: 4s ease-in-out infinite both; }
.cam-zoom_lento_entrada { animation-name: acercar; }
.cam-zoom_lento_salida { animation-name: alejar; }
.cam-paneo_derecha { animation-name: derecha; }
.cam-paneo_izquierda { animation-name: izquierda; }
@keyframes acercar { from { transform: scale(1) } to { transform: scale(1.08) } }
@keyframes alejar { from { transform: scale(1.08) } to { transform: scale(1) } }
@keyframes derecha { from { transform: scale(1.1) translateX(3%) } to { transform: scale(1.1) translateX(-3%) } }
@keyframes izquierda { from { transform: scale(1.1) translateX(-3%) } to { transform: scale(1.1) translateX(3%) } }
.tr-fundido::after { content: ""; position: absolute; inset: 0; background: #0B0B12; animation: fundido 4s infinite; }
@keyframes fundido { 0%, 88% { opacity: 0 } 100% { opacity: 1 } }
</style>
