<script setup lang="ts">
// Lo técnico, escondido: calidad, resolución, cuadros por segundo y volúmenes. No aparece en el flujo normal.
import { ref } from "vue";
import { ChevronDown, Settings } from "@lucide/vue";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import { cambiarAjuste } from "../../composables/proyecto";
import { MENSAJES } from "../../mensajes";
import type { AjustesVideo, OpcionesConfig, RespuestaConfig } from "../../tipos";

const props = defineProps<{ trabajo: string }>();
const opciones = ref<OpcionesConfig | null>(null);
const efectivos = ref<AjustesVideo | null>(null);
const guardando = ref(false);

async function abrir(e: Event) {
  if (!(e.target as HTMLDetailsElement).open || opciones.value) return;
  const [c, a] = await Promise.all([api.get<RespuestaConfig>("/api/configuracion"),
    api.get<{ efectivos: AjustesVideo }>(`/api/trabajos/${props.trabajo}/ajustes-video`)]);
  opciones.value = c.opciones;
  efectivos.value = a.efectivos;
}

async function cambiar(grupo: string, clave: string, valor: unknown) {
  guardando.value = true;
  try {
    await cambiarAjuste(grupo, clave, valor);
    efectivos.value = (await api.get<{ efectivos: AjustesVideo }>(`/api/trabajos/${props.trabajo}/ajustes-video`)).efectivos;
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    guardando.value = false;
  }
}

const lista = (k: string) => (opciones.value?.[k] as { valor: string | number; texto: string }[]) ?? [];
const CAMPOS = [
  { grupo: "video", clave: "calidad", titulo: "Calidad" },
  { grupo: "video", clave: "resolucion", titulo: "Resolución" },
  { grupo: "video", clave: "fps", titulo: "Cuadros por segundo (fps)" },
  { grupo: "audio", clave: "lufs", titulo: "Volumen final" },
] as const;
</script>

<template>
  <details class="group tarjeta" @toggle="abrir">
    <summary class="flex cursor-pointer items-center gap-2 p-4 font-semibold select-none">
      <Settings class="size-4 text-suave" /> {{ MENSAJES.opciones.avanzado }}
      <ChevronDown class="ml-auto size-4 transition group-open:rotate-180" />
    </summary>
    <div v-if="efectivos" class="grid gap-4 border-t border-borde p-4 sm:grid-cols-2">
      <label v-for="c in CAMPOS" :key="c.clave" class="block">
        <span class="etiqueta-campo">{{ c.titulo }}</span>
        <select class="campo" :disabled="guardando" :value="(efectivos[c.grupo] as Record<string, unknown>)[c.clave]"
                @change="cambiar(c.grupo, c.clave, lista(`${c.grupo}.${c.clave}`).find((o) => String(o.valor) === ($event.target as HTMLSelectElement).value)?.valor)">
          <option v-for="o in lista(`${c.grupo}.${c.clave}`)" :key="o.valor" :value="o.valor">{{ o.texto }}</option>
        </select>
      </label>
      <label class="flex items-center gap-3 text-sm sm:col-span-2">
        <input type="checkbox" class="size-4 accent-acento" :checked="efectivos.audio.respaldo_voz !== false" :disabled="guardando"
               @change="cambiar('audio', 'respaldo_voz', ($event.target as HTMLInputElement).checked)" />
        Si la voz elegida falla, terminar el video con una voz gratuita
      </label>
      <p class="text-sm text-suave sm:col-span-2">
        ¿Necesitas más? En el <RouterLink :to="`/cursos/${trabajo}`" class="font-semibold text-acento underline">modo experto</RouterLink>
        puedes editar el guion, la animación de cada elemento, la marca y los agentes.
      </p>
    </div>
  </details>
</template>
