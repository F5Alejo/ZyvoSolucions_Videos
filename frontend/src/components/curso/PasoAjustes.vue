<script setup lang="ts">
import { computed, ref } from "vue";
import { ChevronDown, CircleCheck, LoaderCircle, RotateCcw, Save } from "@lucide/vue";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import AjustesVideoForm from "../AjustesVideoForm.vue";
import SelectorFormato from "../SelectorFormato.vue";
import SelectorMarca from "../SelectorMarca.vue";
import SelectorVoz from "../SelectorVoz.vue";
import type { AjustesVideo, RespuestaConfig, TrabajoCompleto } from "../../tipos";
import { clonar, diferencias } from "../../utils";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();

const marca = ref(props.datos.trabajo.marca);
const voz = ref(props.datos.trabajo.voz);
const formatos = ref([...props.datos.trabajo.formatos]);
const estado = ref<"" | "guardando" | "guardado">("");

// ── Ajustes de producción propios de este curso ──
const GRUPOS = ["video", "tiempos", "audio", "completo"] as const;
const soloAjustes = (c: AjustesVideo): AjustesVideo => clonar(Object.fromEntries(GRUPOS.map((g) => [g, c[g]])) as unknown as AjustesVideo);
const config = ref<RespuestaConfig | null>(null);
const ajustes = ref<AjustesVideo | null>(null);
const guardados = ref<AjustesVideo | null>(null);
const propios = ref(0);
const guardandoAjustes = ref(false);

async function cargarAjustes() {
  const [c, a] = await Promise.all([
    api.get<RespuestaConfig>("/api/configuracion"),
    api.get<{ propios: Partial<AjustesVideo>; efectivos: AjustesVideo }>(`/api/trabajos/${props.datos.trabajo.id}/ajustes-video`),
  ]);
  config.value = c;
  ajustes.value = soloAjustes(a.efectivos);
  guardados.value = soloAjustes(a.efectivos);
  propios.value = Object.values(a.propios).reduce((n, g) => n + Object.keys(g ?? {}).length, 0);
}
cargarAjustes().catch((e) => avisar((e as Error).message, "error"));

const ajustesCambiados = computed(() => JSON.stringify(ajustes.value) !== JSON.stringify(guardados.value));

async function guardarAjustes(volverAGlobal = false) {
  if (!config.value || !ajustes.value) return;
  const cuerpo = volverAGlobal ? null : diferencias(soloAjustes(config.value.configuracion) as never, ajustes.value as never);
  guardandoAjustes.value = true;
  try {
    const r = await api.put<TrabajoCompleto>(`/api/trabajos/${props.datos.trabajo.id}/ajustes-video`, { ajustes: cuerpo });
    emit("actualizado", { trabajo: r.trabajo, resumen: r.resumen });
    await cargarAjustes();
    avisar(volverAGlobal ? "El curso vuelve a usar la configuración general." : "Ajustes del curso guardados.");
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    guardandoAjustes.value = false;
  }
}

/** Guarda enseguida; si el servidor lo rechaza, vuelve a lo último que sí quedó guardado. */
async function guardar() {
  const antes = props.datos.trabajo;
  estado.value = "guardando";
  try {
    emit("actualizado", await api.patch<TrabajoCompleto>(`/api/trabajos/${antes.id}`, { marca: marca.value, voz: voz.value, formatos: formatos.value }));
    estado.value = "guardado";
  } catch (e) {
    marca.value = antes.marca;
    voz.value = antes.voz;
    formatos.value = [...antes.formatos];
    estado.value = "";
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <div class="space-y-10">
    <p class="flex h-5 items-center justify-end gap-2 text-sm font-semibold" aria-live="polite">
      <template v-if="estado === 'guardando'"><LoaderCircle class="size-4 animate-spin text-acento" /> Guardando…</template>
      <template v-else-if="estado === 'guardado'"><CircleCheck class="size-4 text-exito" /><span class="text-exito">Cambios guardados</span></template>
      <template v-else><span class="font-normal text-suave">Los cambios se guardan solos</span></template>
    </p>
    <section aria-labelledby="a-marca">
      <h2 id="a-marca" class="text-xl font-bold">Marca</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Colores, logo y forma de hablar del video.</p>
      <SelectorMarca v-model="marca" @cambio="guardar" />
    </section>
    <section aria-labelledby="a-voz">
      <h2 id="a-voz" class="text-xl font-bold">Voz</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Toca ▶ para escuchar cada una.</p>
      <SelectorVoz v-model="voz" @cambio="guardar" />
    </section>
    <section aria-labelledby="a-formato">
      <h2 id="a-formato" class="text-xl font-bold">Dónde se verá</h2>
      <p class="mt-1 mb-4 text-sm text-suave">Puedes elegir los dos.</p>
      <SelectorFormato v-model="formatos" @cambio="guardar" />
    </section>

    <details class="tarjeta group rounded-2xl" :open="propios > 0">
      <summary class="flex cursor-pointer list-none items-center justify-between gap-3 p-5">
        <span>
          <strong class="block">Ajustes de producción de este curso</strong>
          <span class="text-sm text-suave">
            {{ propios ? `${propios} ${propios === 1 ? "ajuste propio" : "ajustes propios"}; el resto viene de Configuración` : "Usa la configuración general" }}
          </span>
        </span>
        <ChevronDown class="size-5 shrink-0 transition group-open:rotate-180" />
      </summary>
      <div v-if="config && ajustes" class="space-y-4 border-t border-borde p-5">
        <AjustesVideoForm v-model="ajustes" :opciones="config.opciones" :musica="config.musica"
                          :base="soloAjustes(config.configuracion)" />
        <div class="flex flex-wrap justify-end gap-2">
          <button v-if="propios" class="boton-fantasma" :disabled="guardandoAjustes" @click="guardarAjustes(true)">
            <RotateCcw class="size-4" /> Volver a la configuración general</button>
          <button class="boton-primario" :disabled="guardandoAjustes || !ajustesCambiados" @click="guardarAjustes()">
            <LoaderCircle v-if="guardandoAjustes" class="size-4 animate-spin" /><Save v-else class="size-4" /> Guardar ajustes del curso</button>
        </div>
      </div>
    </details>
  </div>
</template>
