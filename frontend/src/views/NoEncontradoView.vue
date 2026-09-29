<script setup lang="ts">
import { Compass } from "lucide-vue-next";
</script>

<template>
  <div class="mx-auto max-w-md py-20 text-center">
    <Compass class="mx-auto size-12 text-suave" />
    <h1 class="mt-4 text-2xl font-bold">No encontramos esta página</h1>
    <p class="mt-2 text-suave">Puede que el enlace esté mal escrito o que lo que buscabas se haya eliminado.</p>
    <RouterLink to="/" class="boton-primario mt-6">Volver al inicio</RouterLink>
  </div>
</template>
