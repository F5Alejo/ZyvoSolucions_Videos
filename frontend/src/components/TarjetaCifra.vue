<script setup lang="ts">
import type { Component } from "vue";

defineProps<{ valor: number | string; texto: string; icono?: Component; a?: string; tono?: "normal" | "aviso" | "exito" }>();
</script>

<template>
  <component :is="a ? 'RouterLink' : 'div'" :to="a"
    class="tarjeta group flex items-center gap-4 p-4 transition"
    :class="[a && 'hover:border-acento hover:shadow-sm', tono === 'aviso' && 'border-aviso/40']">
    <span v-if="icono" class="grid size-11 shrink-0 place-items-center rounded-lg"
          :class="{ 'bg-acento-suave text-acento': !tono || tono === 'normal', 'bg-aviso-fondo text-aviso': tono === 'aviso', 'bg-exito-fondo text-exito': tono === 'exito' }">
      <component :is="icono" class="size-5" />
    </span>
    <span class="min-w-0">
      <span class="cifra block text-2xl leading-none">{{ valor }}</span>
      <span class="mt-1 block text-sm text-suave group-hover:text-texto">{{ texto }}</span>
    </span>
  </component>
</template>
