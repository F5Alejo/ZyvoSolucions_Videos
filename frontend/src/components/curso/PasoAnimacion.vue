<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { CircleCheck, LoaderCircle, RotateCcw, Save, Sparkles, SwatchBook } from "lucide-vue-next";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import type { AnimacionCurso, CatalogoAnim, Fase, PasoAnim, TrabajoCompleto } from "../../tipos";
import { clonar, fijarAjuste, resolverAnimacion } from "../../utils";
import PanelAgentes from "./PanelAgentes.vue";

const props = defineProps<{ datos: TrabajoCompleto }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();
const t = computed(() => props.datos.trabajo);

const catalogo = ref<CatalogoAnim | null>(null);
const defecto = ref("dinamica");
const guardada = ref<AnimacionCurso | null>(null);
const borrador = ref<AnimacionCurso | null>(null);

async function cargar() {
  const [c, a] = await Promise.all([
    api.get<CatalogoAnim>("/api/animaciones"),
    api.get<{ animacion: AnimacionCurso; defecto: string }>(`/api/trabajos/${t.value.id}/animacion`),
  ]);
  catalogo.value = c;
  defecto.value = a.defecto;
  guardada.value = a.animacion;
  borrador.value = clonar(a.animacion);
}
cargar().catch((e) => avisar((e as Error).message, "error"));

// ── Qué se edita: todo el curso o una lámina ──
const alcance = ref<number | null>(null); // null = todo el curso
const laminaVista = ref<number>(t.value.laminas.find((l) => !t.value.excluidas[String(l.n)])?.n ?? 1);
watch(alcance, (n) => { if (n !== null) laminaVista.value = n; });
const propias = computed(() => new Set(Object.keys(borrador.value?.laminas ?? {})));

const resuelta = computed(() => {
  if (!catalogo.value || !borrador.value) return null;
  return resolverAnimacion(catalogo.value.plantillas, borrador.value, defecto.value, alcance.value);
});
const plantillaActual = computed(() => catalogo.value?.plantillas.find((p) => p.id === resuelta.value?.plantilla));

function elegirPlantilla(id: string) {
  if (!borrador.value) return;
  const a = clonar(borrador.value);
  if (alcance.value === null) {
    a.plantilla = id;
    a.ajustes = {}; // los ajustes eran de la plantilla anterior
  } else {
    a.laminas[String(alcance.value)] = { plantilla: id, ajustes: {} };
  }
  borrador.value = a;
}

function cambiar(el: string, fase: Fase, clave: keyof PasoAnim, valor: string | number) {
  if (borrador.value) borrador.value = fijarAjuste(borrador.value, alcance.value, el, fase, clave, valor);
}

function restaurar() {
  if (!borrador.value) return;
  const a = clonar(borrador.value);
  if (alcance.value === null) a.ajustes = {};
  else delete a.laminas[String(alcance.value)];
  borrador.value = a;
}

const hayCambios = computed(() => JSON.stringify(borrador.value) !== JSON.stringify(guardada.value));
function descartar() { if (guardada.value) borrador.value = clonar(guardada.value); }
const guardando = ref(false);
async function guardar() {
  if (!borrador.value) return;
  guardando.value = true;
  try {
    const nuevo = await api.put<TrabajoCompleto>(`/api/trabajos/${t.value.id}/animacion`, borrador.value);
    guardada.value = clonar(borrador.value);
    emit("actualizado", nuevo);
    avisar("Animación guardada. Los videos ya producidos quedan desactualizados.");
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    guardando.value = false;
  }
}

// Al aceptar una propuesta del Director, la animación guardada cambió: se vuelve a leer.
function alAceptar(d: TrabajoCompleto) {
  emit("actualizado", d);
  cargar().catch((e) => avisar((e as Error).message, "error"));
}

const nombreNueva = ref("");
async function guardarComoPlantilla() {
  if (!resuelta.value || !nombreNueva.value.trim()) return;
  try {
    const p = await api.post<{ id: string; nombre: string }>("/api/animaciones", {
      nombre: nombreNueva.value, descripcion: `Creada desde «${t.value.nombre}»`, elementos: resuelta.value.elementos,
    });
    await cargar();
    borrador.value && elegirPlantilla(p.id);
    nombreNueva.value = "";
    avisar(`Plantilla «${p.nombre}» guardada: ya se puede usar en cualquier curso.`);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}

// ── Vista previa en vivo (se pide al servidor con lo que se está editando, sin guardar) ──
const vista = ref("");
const pidiendo = ref(false);
let espera: ReturnType<typeof setTimeout> | undefined;
async function pedirVista() {
  if (!borrador.value) return;
  pidiendo.value = true;
  try {
    const r = await fetch(`/api/trabajos/${t.value.id}/escena/${laminaVista.value}`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ animacion: borrador.value }),
    });
    if (r.ok) vista.value = await r.text();
    else avisar((await r.json().catch(() => ({}))).detail ?? "No se pudo dibujar la vista previa", "error");
  } finally {
    pidiendo.value = false;
  }
}
watch([borrador, laminaVista], () => { clearTimeout(espera); espera = setTimeout(pedirVista, 350); }, { deep: true });

// El iframe dibuja la escena a 1920×1080 y se reduce al ancho de su caja.
const caja = ref<HTMLElement | null>(null);
const escala = ref(0.3);
let observador: ResizeObserver | undefined;
onMounted(() => {
  observador = new ResizeObserver(([e]) => { if (e) escala.value = e.contentRect.width / 1920; });
  watch(caja, (c) => { observador?.disconnect(); if (c) observador?.observe(c); }, { immediate: true });
});
onUnmounted(() => { clearTimeout(espera); observador?.disconnect(); });

// ── Editor por elemento ──
const ELEMENTOS_ORDEN = ["titulo", "vinetas", "imagen", "linea", "antetitulo", "fondo", "logo", "avance"];
const elemento = ref("titulo");
const fase = ref<Fase>("entrada");
const paso = computed(() => resuelta.value?.elementos[elemento.value]?.[fase.value]);
const opciones = computed(() => catalogo.value?.elementos[elemento.value]?.[fase.value] ?? []);
const usaEscalonado = computed(() => elemento.value === "vinetas" || ["palabra-por-palabra", "maquina"].includes(paso.value?.efecto ?? ""));
const segundos = (x: number) => `${x.toFixed(2).replace(".", ",")} s`;
</script>

<template>
  <section aria-labelledby="titulo-animacion" class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 id="titulo-animacion" class="text-xl font-bold">Animación</h2>
        <p class="mt-1 text-sm text-suave">Elige un estilo y ajusta cómo entra y sale cada cosa. Puedes cambiar todo el curso o solo una lámina.</p>
      </div>
      <div class="flex items-center gap-2">
        <button v-if="hayCambios" class="boton-fantasma" @click="descartar">Descartar</button>
        <button class="boton-primario" :disabled="!hayCambios || guardando" @click="guardar">
          <LoaderCircle v-if="guardando" class="size-4 animate-spin" /><Save v-else class="size-4" /> Guardar animación
        </button>
      </div>
    </div>

    <div v-if="!catalogo || !borrador || !resuelta" class="flex items-center gap-2 text-suave"><LoaderCircle class="size-5 animate-spin" /> Cargando…</div>
    <template v-else>
      <!-- Alcance -->
      <div class="tarjeta flex flex-wrap items-center gap-3 p-4">
        <span class="text-sm font-semibold">Estás editando:</span>
        <select v-model="alcance" class="campo max-w-md" aria-label="Qué se edita">
          <option :value="null">Todo el curso</option>
          <option v-for="l in t.laminas" :key="l.n" :value="l.n">
            Solo la lámina {{ l.n }} · {{ l.titulo.slice(0, 50) }}{{ propias.has(String(l.n)) ? " ●" : "" }}
          </option>
        </select>
        <span v-if="alcance !== null && propias.has(String(alcance))" class="text-xs font-semibold text-acento">Esta lámina tiene su propia animación</span>
        <button class="boton-fantasma ml-auto" @click="restaurar">
          <RotateCcw class="size-4" /> {{ alcance === null ? "Quitar los ajustes del curso" : "Que esta lámina use la del curso" }}
        </button>
      </div>

      <div class="grid gap-6 xl:grid-cols-[1fr_1.1fr]">
        <div class="space-y-6">
          <!-- Plantillas -->
          <fieldset>
            <legend class="mb-2 font-bold">Estilo</legend>
            <div class="grid gap-2 sm:grid-cols-2">
              <label v-for="p in catalogo.plantillas" :key="p.id"
                class="tarjeta relative flex cursor-pointer flex-col gap-1 p-3 transition hover:border-acento has-[:checked]:border-acento has-[:checked]:ring-2 has-[:checked]:ring-acento/40">
                <input type="radio" name="plantilla" :value="p.id" :checked="resuelta.plantilla === p.id"
                       class="absolute top-3 right-3 size-4 accent-[var(--c-acento)]" @change="elegirPlantilla(p.id)" />
                <strong class="pr-6 text-sm">{{ p.nombre }} <span v-if="p.propia" class="text-xs font-semibold text-acento">propia</span></strong>
                <span class="text-xs text-suave">{{ p.descripcion }}</span>
              </label>
            </div>
          </fieldset>

          <!-- Editor por elemento -->
          <div class="tarjeta p-4">
            <div class="mb-3 flex flex-wrap gap-1" role="tablist" aria-label="Elemento">
              <button v-for="el in ELEMENTOS_ORDEN" :key="el" role="tab" :aria-selected="elemento === el" @click="elemento = el"
                      class="rounded-lg px-3 py-1.5 text-sm font-semibold transition"
                      :class="elemento === el ? 'bg-acento text-sobre-acento' : 'text-suave hover:bg-superficie-2'">
                {{ catalogo.elementos[el]?.nombre }}
              </button>
            </div>
            <p v-if="catalogo.continuos.includes(elemento)" class="mb-3 text-xs text-suave">
              Entra solo en la primera lámina de cada video y sale solo en la última: entre láminas se queda quieto.
            </p>
            <div class="mb-4 inline-flex rounded-lg border border-borde p-0.5" role="tablist" aria-label="Momento">
              <button v-for="f in (['entrada', 'salida'] as const)" :key="f" role="tab" :aria-selected="fase === f" @click="fase = f"
                      class="rounded-md px-4 py-1.5 text-sm font-semibold capitalize"
                      :class="fase === f ? 'bg-superficie-2 text-texto' : 'text-suave'">{{ f }}</button>
            </div>

            <div v-if="paso" class="grid gap-4 sm:grid-cols-2">
              <label class="block"><span class="etiqueta-campo">Efecto</span>
                <select class="campo" :value="paso.efecto" @change="cambiar(elemento, fase, 'efecto', ($event.target as HTMLSelectElement).value)">
                  <option v-for="o in opciones" :key="o.id" :value="o.id">{{ o.nombre }}</option>
                </select></label>
              <label class="block"><span class="etiqueta-campo">Curva</span>
                <select class="campo" :value="paso.curva" :disabled="paso.efecto === 'ninguno'"
                        @change="cambiar(elemento, fase, 'curva', ($event.target as HTMLSelectElement).value)">
                  <option v-for="c in catalogo.curvas" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select></label>
              <label v-for="k in (['duracion', 'retardo'] as const)" :key="k" class="block">
                <span class="etiqueta-campo flex justify-between">
                  <span>{{ k === "duracion" ? "Duración" : fase === "entrada" ? "Espera antes de entrar" : "Adelanto antes del final" }}</span>
                  <span class="tabular-nums text-suave">{{ segundos(paso[k]) }}</span></span>
                <input type="range" step="0.05" :min="catalogo.limites[k].min" :max="catalogo.limites[k].max" :value="paso[k]"
                       :disabled="paso.efecto === 'ninguno'" class="w-full accent-[var(--c-acento)]"
                       @input="cambiar(elemento, fase, k, +($event.target as HTMLInputElement).value)" />
              </label>
              <label v-if="usaEscalonado" class="block sm:col-span-2">
                <span class="etiqueta-campo flex justify-between">
                  <span>{{ elemento === "vinetas" ? "Separación entre viñetas" : "Separación entre palabras o letras" }}</span>
                  <span class="tabular-nums text-suave">{{ segundos(paso.escalonado) }}</span></span>
                <input type="range" step="0.01" :min="catalogo.limites.escalonado.min" :max="catalogo.limites.escalonado.max" :value="paso.escalonado"
                       :disabled="paso.efecto === 'ninguno'" class="w-full accent-[var(--c-acento)]"
                       @input="cambiar(elemento, fase, 'escalonado', +($event.target as HTMLInputElement).value)" />
              </label>
            </div>
          </div>

          <PanelAgentes :trabajo="t.id" donde="animacion" @actualizado="alAceptar" />

          <!-- Guardar como plantilla -->
          <form class="tarjeta flex flex-wrap items-end gap-3 p-4" @submit.prevent="guardarComoPlantilla">
            <label class="block min-w-48 flex-1"><span class="etiqueta-campo">Guardar esto como plantilla nueva</span>
              <input v-model="nombreNueva" class="campo" placeholder="Nombre, p. ej. «Institucional suave»" maxlength="60" /></label>
            <button class="boton-secundario" :disabled="!nombreNueva.trim()"><SwatchBook class="size-4" /> Guardar plantilla</button>
          </form>
        </div>

        <!-- Vista previa -->
        <div class="xl:sticky xl:top-28 xl:self-start">
          <div class="mb-2 flex flex-wrap items-center justify-between gap-2">
            <span class="flex items-center gap-2 text-sm font-semibold">Vista previa
              <LoaderCircle v-if="pidiendo" class="size-4 animate-spin text-acento" /><CircleCheck v-else class="size-4 text-exito" /></span>
            <select v-if="alcance === null" v-model="laminaVista" class="campo w-auto py-1.5 text-xs" aria-label="Lámina de la vista previa">
              <option v-for="l in t.laminas" :key="l.n" :value="l.n">Lámina {{ l.n }}</option>
            </select>
          </div>
          <div ref="caja" class="relative aspect-video w-full overflow-hidden rounded-xl bg-black ring-1 ring-borde">
            <iframe v-if="vista" :srcdoc="vista" title="Vista previa de la escena" sandbox="allow-scripts"
                    class="pointer-events-none absolute top-0 left-0 origin-top-left border-0"
                    :style="{ width: '1920px', height: '1080px', transform: `scale(${escala})` }" />
          </div>
          <p class="mt-2 text-xs text-suave">
            Se repite sola: entrada, 1,6 s quieta y salida. Plantilla: <strong>{{ plantillaActual?.nombre }}</strong>.
            <Sparkles class="inline size-3.5" /> El Director de animación propone estilos por lámina (a la izquierda).
          </p>
        </div>
      </div>
    </template>
  </section>
</template>
