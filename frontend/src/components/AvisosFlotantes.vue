<script setup lang="ts">
import { CircleCheck, CircleAlert, X } from "lucide-vue-next";
import { avisos, cerrarAviso } from "../composables/avisos";
</script>

<template>
  <div class="fixed right-4 bottom-4 z-[60] flex w-[min(420px,calc(100vw-2rem))] flex-col gap-2" aria-live="polite">
    <TransitionGroup enter-from-class="opacity-0 translate-y-2" leave-to-class="opacity-0 translate-y-2"
                     enter-active-class="transition" leave-active-class="transition">
      <div v-for="a in avisos" :key="a.id" :role="a.tipo === 'error' ? 'alert' : 'status'"
           class="tarjeta flex items-start gap-3 border-l-4 px-4 py-3 shadow-lg"
           :class="a.tipo === 'error' ? 'border-l-error' : 'border-l-exito'">
        <component :is="a.tipo === 'error' ? CircleAlert : CircleCheck" class="mt-0.5 size-5 shrink-0"
                   :class="a.tipo === 'error' ? 'text-error' : 'text-exito'" />
        <p class="flex-1 text-sm font-medium">{{ a.texto }}</p>
        <button class="rounded p-0.5 text-suave hover:text-texto" aria-label="Cerrar aviso" @click="cerrarAviso(a.id)">
          <X class="size-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>
