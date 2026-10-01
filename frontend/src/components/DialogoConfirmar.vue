<script setup lang="ts">
import { nextTick, ref, watch } from "vue";
import { TriangleAlert } from "@lucide/vue";
import { dialogo } from "../composables/confirmar";

const cancelar = ref<HTMLButtonElement | null>(null);
let antes: Element | null = null;

// Al abrir, el foco va a «Cancelar» (la opción segura); al cerrar, vuelve a donde estaba.
watch(() => dialogo.abierto, async (abierto) => {
  if (abierto) {
    antes = document.activeElement;
    await nextTick();
    cancelar.value?.focus();
  } else if (antes instanceof HTMLElement) {
    antes.focus();
  }
});
</script>

<template>
  <Transition enter-from-class="opacity-0" leave-to-class="opacity-0" enter-active-class="transition" leave-active-class="transition">
    <div v-if="dialogo.abierto" class="fixed inset-0 z-[70] flex items-center justify-center bg-black/50 p-4"
         @click.self="dialogo.responder(false)" @keydown.esc="dialogo.responder(false)">
      <div class="tarjeta w-full max-w-md p-6 shadow-2xl" role="alertdialog" aria-modal="true"
           aria-labelledby="dialogo-titulo" aria-describedby="dialogo-texto">
        <div class="flex gap-4">
          <span v-if="dialogo.peligro" class="grid size-10 shrink-0 place-items-center rounded-full bg-error-fondo text-error">
            <TriangleAlert class="size-5" />
          </span>
          <div>
            <h2 id="dialogo-titulo" class="text-lg font-bold">{{ dialogo.titulo }}</h2>
            <p id="dialogo-texto" class="mt-1 text-sm text-suave">{{ dialogo.texto }}</p>
          </div>
        </div>
        <div class="mt-6 flex justify-end gap-2">
          <button ref="cancelar" class="boton-fantasma" @click="dialogo.responder(false)">Cancelar</button>
          <button :class="dialogo.peligro ? 'boton-peligro' : 'boton-primario'" @click="dialogo.responder(true)">
            {{ dialogo.aceptar }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>
