<script setup lang="ts">
import { CircleAlert, LoaderCircle } from "@lucide/vue";

defineProps<{ cargando: boolean; error: string | null }>();
defineEmits<{ reintentar: [] }>();
</script>

<template>
  <div v-if="error" class="tarjeta mx-auto my-10 max-w-lg p-8 text-center" role="alert">
    <CircleAlert class="mx-auto size-10 text-error" />
    <h2 class="mt-3 text-lg font-bold">No pudimos cargar esta página</h2>
    <p class="mt-1 text-sm text-suave">{{ error }}</p>
    <button class="boton-primario mt-5" @click="$emit('reintentar')">Intentar de nuevo</button>
  </div>
  <div v-else-if="cargando" class="flex items-center justify-center gap-3 py-24 text-suave" role="status">
    <LoaderCircle class="size-6 animate-spin text-acento" /> Cargando…
  </div>
</template>
