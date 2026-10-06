<script setup lang="ts">

defineProps<{ cargando: boolean; error: string | null }>();
defineEmits<{ reintentar: [] }>();
</script>

<template>
  <div v-if="error" class="tarjeta mx-auto my-10 max-w-lg p-8 text-center" role="alert">
    <span class="mx-auto mb-2 block w-fit rounded-2xl bg-white p-3"><img src="/marca/banco/sin-conexion.webp" alt="" class="h-28 w-auto" /></span>
    <h2 class="mt-3 text-lg font-bold">No pudimos cargar esta página</h2>
    <p class="mt-1 text-sm text-suave">{{ error }}</p>
    <button class="boton-primario mt-5" @click="$emit('reintentar')">Intentar de nuevo</button>
  </div>
  <!-- Mientras llegan los datos: la forma de la página, sin saltos -->
  <div v-else-if="cargando" class="animate-pulse space-y-6" role="status" aria-label="Cargando">
    <div class="space-y-3">
      <div class="h-4 w-40 rounded bg-borde" />
      <div class="h-8 w-2/3 max-w-lg rounded-lg bg-borde" />
      <div class="h-4 w-1/2 max-w-md rounded bg-borde" />
    </div>
    <div class="grid grid-cols-[minmax(0,1fr)] gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 3" :key="i" class="h-40 rounded-2xl bg-borde/70" />
    </div>
    <div class="h-64 rounded-2xl bg-borde/50" />
  </div>
</template>
