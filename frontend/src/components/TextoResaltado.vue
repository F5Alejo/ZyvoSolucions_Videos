<script setup lang="ts">
import { computed } from "vue";
import { resaltar } from "../utils";

const props = defineProps<{ texto: string; citas: string[] }>();
const trozos = computed(() => resaltar(props.texto, props.citas));
</script>

<template>
  <span><template v-for="(t, i) in trozos" :key="i"><mark v-if="t.marcado" title="Cifra o norma: revísala contra su fuente">{{ t.texto }}</mark><template v-else>{{ t.texto }}</template></template></span>
</template>
