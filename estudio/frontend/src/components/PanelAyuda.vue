<script setup lang="ts">
import { nextTick, ref, watch } from "vue";
import { CircleHelp, X } from "lucide-vue-next";
import { ayuda } from "../composables/ayuda";
import IlustracionNotas from "./IlustracionNotas.vue";

const cerrar = ref<HTMLButtonElement | null>(null);
watch(() => ayuda.abierta, async (a) => { if (a) { await nextTick(); cerrar.value?.focus(); } });
</script>

<template>
  <Transition enter-from-class="opacity-0" leave-to-class="opacity-0" enter-active-class="transition" leave-active-class="transition">
    <div v-if="ayuda.abierta" class="fixed inset-0 z-[65] bg-black/40" @click="ayuda.abierta = false" />
  </Transition>
  <Transition enter-from-class="translate-x-full" leave-to-class="translate-x-full" enter-active-class="transition-transform duration-300" leave-active-class="transition-transform duration-200">
    <aside v-if="ayuda.abierta" class="fixed inset-y-0 right-0 z-[66] flex w-full max-w-md flex-col bg-superficie shadow-2xl"
           role="dialog" aria-modal="true" aria-labelledby="ayuda-titulo" @keydown.esc="ayuda.abierta = false">
      <header class="flex items-center justify-between border-b border-borde px-6 py-4">
        <h2 id="ayuda-titulo" class="flex items-center gap-2 text-lg font-bold"><CircleHelp class="size-5 text-acento" /> Ayuda</h2>
        <button ref="cerrar" class="boton-fantasma" aria-label="Cerrar la ayuda" @click="ayuda.abierta = false"><X class="size-5" /></button>
      </header>

      <div class="flex-1 space-y-8 overflow-y-auto px-6 py-6 text-sm leading-relaxed">
        <section id="ayuda-como-funciona">
          <h3 class="text-base font-bold">¿Cómo funciona?</h3>
          <ol class="mt-3 space-y-3">
            <li class="flex gap-3"><span class="grid size-7 shrink-0 place-items-center rounded-full bg-acento-suave font-bold text-acento">1</span>
              <span><strong>Subes tu presentación</strong> de PowerPoint, con el guion escrito en las notas del orador.</span></li>
            <li class="flex gap-3"><span class="grid size-7 shrink-0 place-items-center rounded-full bg-acento-suave font-bold text-acento">2</span>
              <span><strong>Revisas lo que encontramos</strong>: el guion de cada video y lo que conviene corregir.</span></li>
            <li class="flex gap-3"><span class="grid size-7 shrink-0 place-items-center rounded-full bg-acento-suave font-bold text-acento">3</span>
              <span><strong>Eliges la marca, la voz y dónde se verá.</strong> El estudio arma un video por módulo.</span></li>
          </ol>
        </section>

        <section id="ayuda-notas">
          <h3 class="text-base font-bold">¿Dónde escribo lo que dirá la voz?</h3>
          <p class="mt-2 text-suave">
            En las <strong class="text-texto">notas del orador</strong> de cada diapositiva: el recuadro que aparece debajo de la diapositiva en PowerPoint.
            Si no lo ves, entra a <strong class="text-texto">Vista → Notas</strong>.
          </p>
          <div class="mt-3"><IlustracionNotas /></div>
          <p class="mt-3 text-suave">Una diapositiva sin notas queda sin voz: el estudio te avisará cuáles son.</p>
        </section>

        <section id="ayuda-resaltado">
          <h3 class="text-base font-bold">¿Por qué hay textos resaltados?</h3>
          <p class="mt-2 text-suave">
            Son <mark>leyes, porcentajes y cifras</mark>. No están mal: se resaltan para que los compares con su fuente antes de producir,
            porque un dato equivocado en un video es difícil de corregir cuando ya se publicó.
          </p>
        </section>

        <section id="ayuda-videos">
          <h3 class="text-base font-bold">¿Cuándo tengo los videos?</h3>
          <p class="mt-2 text-suave">
            El estudio deja listo todo lo que se necesita para producirlos: el guion, la marca, la voz y la lista de videos.
            El último paso, generar los archivos de video, todavía lo hace el equipo de producción; pronto se hará desde aquí.
          </p>
        </section>

        <section id="ayuda-cambiar">
          <h3 class="text-base font-bold">¿Puedo cambiar la marca o la voz después?</h3>
          <p class="mt-2 text-suave">Sí, cuando quieras, en la pestaña <strong class="text-texto">Ajustes</strong> del curso. Se guarda solo.</p>
        </section>

        <section id="ayuda-privacidad">
          <h3 class="text-base font-bold">¿Qué pasa con mi presentación?</h3>
          <p class="mt-2 text-suave">Se guarda en el equipo donde funciona el estudio. No se publica en internet y puedes eliminarla cuando quieras desde el curso.</p>
        </section>
      </div>
    </aside>
  </Transition>
</template>
