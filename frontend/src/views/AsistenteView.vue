<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft, ArrowRight, CircleAlert, CircleCheck, LoaderCircle, PartyPopper, Sparkles } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import { abrirAyuda } from "../composables/ayuda";
import EstadoCarga from "../components/EstadoCarga.vue";
import SelectorFormato from "../components/SelectorFormato.vue";
import SelectorMarca from "../components/SelectorMarca.vue";
import SelectorVoz from "../components/SelectorVoz.vue";
import VistaPreviaVideo from "../components/VistaPreviaVideo.vue";
import type { TrabajoCompleto } from "../tipos";
import { cuenta, mmss } from "../utils";

const props = defineProps<{ id: string }>();
const ruta = useRoute();
const router = useRouter();
const { datos: d, cargando, error, recargar } = useCarga(() => api.get<TrabajoCompleto>(`/api/trabajos/${props.id}`), () => props.id);

const PASOS = [
  { id: "revision", titulo: "Tu presentación" },
  { id: "marca", titulo: "Marca" },
  { id: "voz", titulo: "Voz" },
  { id: "formato", titulo: "Formato" },
  { id: "listo", titulo: "Listo" },
] as const;
type Paso = (typeof PASOS)[number]["id"];
const paso = computed<Paso>(() => PASOS.find((p) => p.id === ruta.query.paso)?.id ?? "revision");
const indice = computed(() => PASOS.findIndex((p) => p.id === paso.value));
function ir(p: Paso) {
  router.push({ query: { paso: p } });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Lo elegido. Se guarda al elegir; si el servidor lo rechaza, vuelve a lo guardado.
const marca = ref("");
const voz = ref("");
const formatos = ref<string[]>([]);
const guardando = ref(false);
watch(d, (x) => {
  if (!x) return;
  marca.value = x.trabajo.marca;
  voz.value = x.trabajo.voz;
  formatos.value = [...x.trabajo.formatos];
}, { immediate: true });

async function guardar() {
  if (!d.value) return;
  guardando.value = true;
  try {
    d.value = await api.patch<TrabajoCompleto>(`/api/trabajos/${props.id}`, { marca: marca.value, voz: voz.value, formatos: formatos.value });
  } catch (e) {
    marca.value = d.value.trabajo.marca;
    voz.value = d.value.trabajo.voz;
    formatos.value = [...d.value.trabajo.formatos];
    avisar((e as Error).message, "error");
  } finally {
    guardando.value = false;
  }
}

const r = computed(() => d.value?.resumen);
const t = computed(() => d.value?.trabajo);
const porRevisar = computed(() => r.value?.chequeos.filter((c) => c.ok !== true) ?? []);
const marcaElegida = computed(() => catalogo.value?.marcas[marca.value]);
const vozElegida = computed(() => catalogo.value?.voces.find((v) => v.id === voz.value));
const vertical = computed(() => formatos.value.length === 1 && formatos.value[0] === "9:16");

/** La primera frase de un video, para la vista previa. */
function frase(numeros: number[]) {
  const l = t.value?.laminas.find((x) => numeros.includes(x.n) && x.frases.length);
  return l?.frases[0];
}
const primero = computed(() => r.value?.videos[0]);
const puedeSeguir = computed(() => paso.value !== "formato" || formatos.value.length > 0);
</script>

<template>
  <EstadoCarga v-if="!d || !r || !t" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="mx-auto max-w-5xl">
    <!-- Progreso -->
    <div class="mb-8">
      <div class="flex items-center justify-between text-sm">
        <p class="font-semibold text-suave">
          <template v-if="paso !== 'listo'">Paso {{ indice + 1 }} de {{ PASOS.length - 1 }} · </template>{{ t.nombre }}
        </p>
        <RouterLink :to="`/cursos/${id}`" class="text-suave hover:text-acento hover:underline">Terminar después</RouterLink>
      </div>
      <ol class="mt-3 flex gap-2" aria-label="Pasos">
        <li v-for="(p, i) in PASOS.slice(0, -1)" :key="p.id" class="flex-1">
          <span class="block h-1.5 rounded-full transition-colors duration-500" :class="i <= indice ? 'bg-acento' : 'bg-borde'" />
          <span class="mt-1.5 hidden text-xs sm:block" :class="i === indice ? 'font-bold text-texto' : 'text-suave'">{{ p.titulo }}</span>
        </li>
      </ol>
    </div>

    <Transition mode="out-in" enter-from-class="opacity-0 translate-x-4" leave-to-class="opacity-0 -translate-x-4"
                enter-active-class="transition duration-200" leave-active-class="transition duration-150">
      <!-- 1. Lo que encontramos -->
      <section v-if="paso === 'revision'" key="revision" aria-labelledby="t-revision">
        <p class="flex items-center gap-2 text-sm font-semibold text-exito"><CircleCheck class="size-5" /> Leímos tu presentación</p>
        <h1 id="t-revision" class="mt-2 text-3xl font-bold">Así quedó tu curso</h1>
        <div class="mt-6 grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-3">
          <div class="tarjeta p-5"><p class="text-sm text-suave">Diapositivas</p><p class="cifra mt-1 text-4xl">{{ t.laminas.length }}</p></div>
          <div class="tarjeta p-5"><p class="text-sm text-suave">Videos</p><p class="cifra mt-1 text-4xl">{{ r.videos.length }}</p></div>
          <div class="tarjeta p-5"><p class="text-sm text-suave">Duración total</p><p class="cifra mt-1 text-4xl">{{ mmss(r.segundos) }} <span class="text-lg font-semibold text-suave">min</span></p></div>
        </div>

        <div v-if="porRevisar.length" class="mt-6 rounded-2xl border border-aviso/40 bg-aviso-fondo p-5">
          <p class="flex items-center gap-2 font-bold text-aviso"><CircleAlert class="size-5" /> Hay {{ cuenta(porRevisar.length, "cosa") }} que conviene revisar</p>
          <ul class="mt-3 space-y-2 text-sm">
            <li v-for="c in porRevisar" :key="c.clave"><strong>{{ c.titulo }}.</strong> {{ c.detalle }}. <span v-if="c.ayuda" class="text-suave">{{ c.ayuda }}</span></li>
          </ul>
          <p class="mt-3 text-sm text-suave">No tienes que resolverlo ahora: después puedes revisarlo con calma en el guion.
            <button class="font-semibold text-acento hover:underline" @click="abrirAyuda('resaltado')">¿Por qué pasa esto?</button></p>
        </div>
        <p v-else class="mt-6 flex items-center gap-2 rounded-2xl bg-exito-fondo p-5 font-semibold text-exito">
          <CircleCheck class="size-5" /> Todo en orden: cada diapositiva tiene su guion.
        </p>

        <h2 class="mt-8 mb-3 font-bold">Los videos que armamos</h2>
        <ol class="tarjeta divide-y divide-borde">
          <li v-for="(v, i) in r.videos.slice(0, 8)" :key="v.clave" class="flex items-center gap-4 px-4 py-3">
            <span class="grid size-8 shrink-0 place-items-center rounded-lg bg-acento-suave text-sm font-bold text-acento">{{ i + 1 }}</span>
            <span class="min-w-0 flex-1 truncate font-medium">{{ v.titulo }}</span>
            <span class="text-sm text-suave tabular-nums">{{ mmss(v.segundos) }}</span>
          </li>
          <li v-if="r.videos.length > 8" class="px-4 py-3 text-sm text-suave">y {{ cuenta(r.videos.length - 8, "video") }} más</li>
        </ol>
      </section>

      <!-- 2. Marca -->
      <section v-else-if="paso === 'marca'" key="marca" aria-labelledby="t-marca" class="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div>
          <h1 id="t-marca" class="text-3xl font-bold">¿Para qué marca es este curso?</h1>
          <p class="mt-2 text-suave">El video usará sus colores, su logo y su forma de hablar.</p>
          <div class="mt-6"><SelectorMarca v-model="marca" @cambio="guardar" /></div>
        </div>
        <aside v-if="primero" class="lg:pt-24">
          <p class="mb-2 text-sm font-semibold text-suave">Así se verá</p>
          <VistaPreviaVideo :titulo="primero.titulo" :subtitulo="frase(primero.laminas)" :numero="1" :segundos="primero.segundos"
                            :marca="marcaElegida" :vertical="vertical" />
        </aside>
      </section>

      <!-- 3. Voz -->
      <section v-else-if="paso === 'voz'" key="voz" aria-labelledby="t-voz">
        <h1 id="t-voz" class="text-3xl font-bold">Elige la voz que narrará el curso</h1>
        <p class="mt-2 text-suave">Toca <span class="font-semibold text-texto">▶</span> para escuchar cada una. Si no sabes cuál, la recomendada funciona muy bien.</p>
        <div class="mt-6"><SelectorVoz v-model="voz" @cambio="guardar" /></div>
      </section>

      <!-- 4. Formato -->
      <section v-else-if="paso === 'formato'" key="formato" aria-labelledby="t-formato">
        <h1 id="t-formato" class="text-3xl font-bold">¿Dónde se van a ver los videos?</h1>
        <p class="mt-2 text-suave">Puedes elegir los dos: se hará una versión para cada uno.</p>
        <div class="mt-6"><SelectorFormato v-model="formatos" @cambio="guardar" /></div>
        <p v-if="!formatos.length" class="mt-3 text-sm font-semibold text-aviso" role="alert">Elige al menos uno para continuar.</p>
      </section>

      <!-- 5. Listo -->
      <section v-else key="listo" aria-labelledby="t-listo" class="text-center">
        <span class="mx-auto grid size-20 place-items-center rounded-full bg-exito-fondo text-exito"><PartyPopper class="size-10" /></span>
        <h1 id="t-listo" class="mt-5 text-3xl font-bold">¡Tu curso está listo para producir!</h1>
        <p class="mx-auto mt-2 max-w-xl text-suave">
          {{ cuenta(r.videos.length, "video") }} · {{ mmss(r.segundos) }} min · marca {{ marcaElegida?.nombre_corto }} ·
          voz {{ vozElegida?.nombre }} · {{ formatos.map((f) => (f === "16:9" ? "horizontal" : "vertical")).join(" y ") }}
        </p>
        <div class="mx-auto mt-8 grid grid-cols-[minmax(0,1fr)] max-w-3xl gap-4" :class="vertical ? 'grid-cols-3' : 'sm:grid-cols-3'">
          <VistaPreviaVideo v-for="(v, i) in r.videos.slice(0, 3)" :key="v.clave" :titulo="v.titulo" :subtitulo="frase(v.laminas)"
                            :numero="i + 1" :segundos="v.segundos" :marca="marcaElegida" :vertical="vertical" />
        </div>
        <RouterLink :to="`/cursos/${id}`" class="boton-primario mt-10 px-8 py-3.5 text-base"><Sparkles class="size-5" /> Ver mi curso</RouterLink>
      </section>
    </Transition>

    <!-- Navegación -->
    <div v-if="paso !== 'listo'" class="mt-10 flex items-center justify-between gap-3 border-t border-borde pt-6">
      <button v-if="indice > 0" class="boton-fantasma" @click="ir(PASOS[indice - 1]!.id)"><ArrowLeft class="size-4" /> Atrás</button>
      <span v-else />
      <span class="flex items-center gap-3">
        <span v-if="guardando" class="flex items-center gap-1.5 text-sm text-suave" aria-live="polite"><LoaderCircle class="size-4 animate-spin" /> Guardando…</span>
        <button class="boton-primario px-6 py-3 text-base" :disabled="!puedeSeguir || guardando" @click="ir(PASOS[indice + 1]!.id)">
          {{ paso === "revision" ? "Se ve bien, continuar" : paso === "formato" ? "Terminar" : "Continuar" }} <ArrowRight class="size-4" />
        </button>
      </span>
    </div>
  </div>
</template>
