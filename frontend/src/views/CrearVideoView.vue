<script setup lang="ts">
// El flujo creativo de Zyvo: Subir → Analizar → Estilo → Voz → Opciones → Crear → Listo.
// Todo lo técnico queda escondido; el estado vive en composables/proyecto.ts.
import { computed, onUnmounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft, ArrowRight, Check, LoaderCircle, Pencil, RefreshCw, Sparkles } from "@lucide/vue";
import { api, subir } from "../api";
import { avisar } from "../composables/avisos";
import { catalogo, cargarCatalogo } from "../composables/catalogo";
import {
  abrir, cambiarAjuste, detener, elegirEstilo, elegirVozYFormato, generacion, generar, proyecto, trabajo,
} from "../composables/proyecto";
import { FORMATOS_HUMANOS, MENSAJES } from "../mensajes";
import type { RespuestaConfig, VersionVideo } from "../tipos";
import { cuenta, mmss } from "../utils";
import AjustesAvanzados from "../components/video/AjustesAvanzados.vue";
import EstadoGeneracion from "../components/video/EstadoGeneracion.vue";
import EstadoCarga from "../components/EstadoCarga.vue";
import MensajeError from "../components/video/MensajeError.vue";
import PanelExportar from "../components/video/PanelExportar.vue";
import PasosProgreso from "../components/video/PasosProgreso.vue";
import ReproductorPrevio from "../components/video/ReproductorPrevio.vue";
import TarjetaEstilo from "../components/video/TarjetaEstilo.vue";
import TarjetaVoz from "../components/video/TarjetaVoz.vue";
import ZonaSubida from "../components/video/ZonaSubida.vue";

const props = defineProps<{ id?: string }>();
const ruta = useRoute();
const router = useRouter();

const PASOS = [
  { id: "analizar", texto: "Analizar" }, { id: "estilo", texto: "Estilo" }, { id: "voz", texto: "Voz" },
  { id: "opciones", texto: "Opciones" }, { id: "crear", texto: "Crear" }, { id: "listo", texto: "Resultado" },
];
const paso = computed(() => (ruta.query.paso as string) || pasoInicial.value);
const pasoInicial = computed(() => generacion.value.listo ? "listo" : generacion.value.produciendo ? "crear" : "analizar");
const hasta = computed(() => (generacion.value.listo ? 5 : 4));
function ir(p: string) { router.push({ query: { paso: p } }); }
function siguiente() { ir(PASOS[PASOS.findIndex((p) => p.id === paso.value) + 1]?.id ?? "listo"); }
function anterior() { ir(PASOS[Math.max(0, PASOS.findIndex((p) => p.id === paso.value) - 1)]!.id); }

// ── Subir ──
const avance = ref<number | null>(null);
async function subirPptx(f: File) {
  const datos = new FormData();
  datos.append("archivo", f);
  datos.append("nombre", f.name.replace(/\.pptx$/i, "").replace(/[-_]+/g, " "));
  avance.value = 0;
  try {
    const { id } = await subir<{ id: string }>("/api/trabajos", datos, (x) => (avance.value = x));
    avisar(MENSAJES.subir.cargada);
    router.push({ path: `/crear/${id}`, query: { paso: "analizar" } });
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    avance.value = null;
  }
}

watch(() => props.id, (id) => { if (id) { abrir(id); cargarCatalogo().catch(() => undefined); } }, { immediate: true });
onUnmounted(detener);

// ── Analizar: la lista se va marcando para que se sienta el trabajo hecho ──
const marcados = ref(0);
let reloj: ReturnType<typeof setInterval> | undefined;
watch(() => [paso.value, proyecto.analisis] as const, ([p, a]) => {
  clearInterval(reloj);
  if (p !== "analizar" || !a) return;
  marcados.value = 0;
  reloj = setInterval(() => { marcados.value++; if (marcados.value >= 4) clearInterval(reloj); }, 450);
}, { immediate: true });
onUnmounted(() => clearInterval(reloj));

// ── Voz ──
const voces = computed(() => {
  const todas = catalogo.value?.voces ?? [];
  const orden = (v: (typeof todas)[number]) => (v.falta ? 2 : v.solo_borrador ? 1 : 0);
  return [...todas].sort((a, b) => orden(a) - orden(b));
});
const formato = computed(() => trabajo.value?.formatos[0] ?? "16:9");
const ocupado = ref(false);
async function con(f: () => Promise<unknown>) {
  ocupado.value = true;
  try { await f(); } catch (e) { avisar((e as Error).message, "error"); } finally { ocupado.value = false; }
}

// ── Opciones ──
const config = ref<RespuestaConfig | null>(null);
const efectivos = ref<RespuestaConfig["configuracion"] | null>(null);
watch(paso, async (p) => {
  if (p !== "opciones" || !props.id) return;
  const [c, a] = await Promise.all([api.get<RespuestaConfig>("/api/configuracion"),
    api.get<{ efectivos: RespuestaConfig["configuracion"] }>(`/api/trabajos/${props.id}/ajustes-video`)]);
  config.value = c;
  efectivos.value = a.efectivos;
}, { immediate: true });
const estiloActual = computed(() => proyecto.estilos.find((e) => e.id === trabajo.value?.estilo) ?? null);
const conAnimaciones = computed(() => (trabajo.value?.animacion?.plantilla ?? "dinamica") !== "minima");
async function cambiar(grupo: string, clave: string, valor: unknown) {
  await con(async () => {
    await cambiarAjuste(grupo, clave, valor);
    efectivos.value = (await api.get<{ efectivos: RespuestaConfig["configuracion"] }>(`/api/trabajos/${props.id}/ajustes-video`)).efectivos;
  });
}
async function animaciones(si: boolean) {
  const plantilla = si ? (estiloActual.value?.animacion ?? "dinamica") : "minima";
  await con(async () => {
    const actual = (trabajo.value?.animacion ?? {}) as Record<string, unknown>;
    await api.put(`/api/trabajos/${props.id}/animacion`, { ...actual, plantilla });
    await abrir(props.id!);
  });
}

// ── Crear y resultado ──
const videoActual = computed(() => generacion.value.actual);
const clave = ref<string | null>(null);
const videos = computed(() => trabajo.value?.videos ?? []);
watch(videos, (v) => { if (!clave.value && v.length) clave.value = v[0]!.clave; }, { immediate: true });
watch(() => generacion.value.listo, (listo, antes) => { if (listo && antes === false && paso.value === "crear") ir("listo"); });

async function crear() {
  await con(async () => {
    await generar();
    if (!generacion.value.produciendo && generacion.value.listo) avisar("Ya está al día: cambia algo en «Editar» para volver a crearlo.");
  });
}
const enReproductor = computed(() => {
  const p = proyecto.produccion;
  if (!p || !clave.value) return null;
  if (clave.value === "completo") return p.completo?.archivos ? { mp4: p.completo.archivos.mp4, vtt: p.completo.archivos.vtt } : null;
  const a = p.videos[clave.value]?.archivos;
  return a ? { mp4: a.mp4, vtt: a.vtt } : null;
});
const versiones = ref<VersionVideo[]>([]);
const version = ref<string | null>(null);
watch(() => [clave.value, generacion.value.listo] as const, async ([c]) => {
  version.value = null;
  versiones.value = c && c !== "completo" && props.id ? await api.get<VersionVideo[]>(`/api/trabajos/${props.id}/versiones/${c}`) : [];
});
const videoMostrado = computed(() => (version.value ? { mp4: versiones.value.find((v) => v.version === version.value)!.mp4, vtt: null }
  : enReproductor.value));

function accionError(a: string) {
  if (a === "voz") ir("voz");
  else if (a === "curso") router.push(`/cursos/${props.id}`);
  else crear();
}
const claveConError = computed(() => Object.entries(proyecto.produccion?.videos ?? {}).find(([, v]) => v?.estado === "error")?.[0]);
</script>

<template>
  <!-- Sin proyecto: subir la presentación -->
  <div v-if="!id" class="mx-auto max-w-2xl py-6 text-center">
    <p class="texto-chispa text-sm font-extrabold tracking-[.25em] uppercase">Zyvo</p>
    <h1 class="mt-2 text-3xl leading-tight font-bold sm:text-4xl">{{ MENSAJES.subir.titulo }}</h1>
    <p class="mt-3 text-suave">Sube tu presentación y Zyvo se encarga del resto: narración, animaciones, música y subtítulos.</p>
    <ZonaSubida class="mt-8" :avance="avance" @elegido="subirPptx" />
    <ol class="mt-10 grid gap-3 text-left sm:grid-cols-3">
      <li class="tarjeta p-4"><p class="font-bold">1. Sube</p><p class="text-sm text-suave">Tu PPTX, con lo que dirá la voz en las notas.</p></li>
      <li class="tarjeta p-4"><p class="font-bold">2. Elige</p><p class="text-sm text-suave">Un estilo, una voz y el formato.</p></li>
      <li class="tarjeta p-4"><p class="font-bold">3. Crea</p><p class="text-sm text-suave">Zyvo arma el video y revisa su calidad.</p></li>
    </ol>
  </div>

  <EstadoCarga v-else-if="!proyecto.datos || !proyecto.analisis" :cargando="proyecto.cargando" :error="proyecto.error" @reintentar="abrir(id)" />

  <div v-else class="mx-auto max-w-5xl space-y-6">
    <header class="flex flex-wrap items-end justify-between gap-3">
      <div class="min-w-0">
        <p class="texto-chispa text-xs font-extrabold tracking-[.25em] uppercase">Zyvo</p>
        <h1 class="truncate text-2xl font-bold">{{ trabajo!.nombre }}</h1>
      </div>
    </header>
    <PasosProgreso :pasos="PASOS" :actual="paso" :hasta="hasta" @ir="ir" />

    <!-- Analizar -->
    <section v-if="paso === 'analizar'" class="space-y-5">
      <div class="tarjeta p-6">
        <p class="text-lg font-bold">{{ marcados < 4 ? MENSAJES.analizar.titulo : MENSAJES.analizar.listo }}</p>
        <ul class="mt-4 space-y-2">
          <li v-for="(texto, i) in MENSAJES.analizar.pasos" :key="texto" class="flex items-center gap-3"
              :class="i < marcados ? 'text-texto' : 'text-suave'">
            <Check v-if="i < marcados" class="size-4 text-exito" stroke-width="3" />
            <LoaderCircle v-else-if="i === marcados" class="size-4 animate-spin text-acento" />
            <span v-else class="size-4" />
            {{ texto }}
          </li>
        </ul>
      </div>
      <div v-if="marcados >= 4" class="aparecer grid gap-3 sm:grid-cols-4">
        <div class="tarjeta p-4"><p class="cifra text-2xl">{{ proyecto.analisis.laminas }}</p><p class="text-sm text-suave">diapositivas</p></div>
        <div class="tarjeta p-4"><p class="cifra text-2xl">~{{ Math.max(1, Math.round(proyecto.analisis.minutos)) }} min</p><p class="text-sm text-suave">de video</p></div>
        <div class="tarjeta p-4"><p class="cifra text-2xl">{{ proyecto.analisis.imagenes.length }}</p><p class="text-sm text-suave">con imágenes</p></div>
        <div class="tarjeta p-4"><p class="cifra text-2xl">{{ cuenta(proyecto.analisis.videos, "video") }}</p><p class="text-sm text-suave">{{ proyecto.analisis.estructura }}</p></div>
      </div>
      <div v-if="marcados >= 4 && proyecto.analisis.tema.length" class="aparecer text-sm text-suave">
        Trata sobre <span class="font-semibold text-texto">{{ proyecto.analisis.tema.slice(0, 4).join(", ") }}</span> · nivel {{ proyecto.analisis.dificultad }}
      </div>
      <ul v-if="marcados >= 4 && proyecto.analisis.avisos.length" class="aparecer space-y-1 rounded-xl bg-aviso-fondo p-4 text-sm text-aviso">
        <li v-for="a in proyecto.analisis.avisos" :key="a">• {{ a }}</li>
      </ul>
      <div class="flex justify-end"><button class="boton-primario" :disabled="marcados < 4" @click="siguiente">Elegir estilo <ArrowRight class="size-4" /></button></div>
    </section>

    <!-- Estilo -->
    <section v-else-if="paso === 'estilo'" class="space-y-5">
      <div><h2 class="text-xl font-bold">{{ MENSAJES.estilo.titulo }}</h2><p class="text-sm text-suave">{{ MENSAJES.estilo.ayuda }}</p></div>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <TarjetaEstilo v-for="e in proyecto.estilos" :key="e.id" :estilo="e" :elegido="trabajo!.estilo === e.id"
                       @elegir="con(() => elegirEstilo(e.id))" />
      </div>
      <div class="flex justify-between">
        <button class="boton-fantasma" @click="anterior"><ArrowLeft class="size-4" /> Atrás</button>
        <button class="boton-primario" :disabled="!trabajo!.estilo || ocupado" @click="siguiente">Elegir voz <ArrowRight class="size-4" /></button>
      </div>
    </section>

    <!-- Voz -->
    <section v-else-if="paso === 'voz'" class="space-y-5">
      <h2 class="text-xl font-bold">{{ MENSAJES.voz.titulo }}</h2>
      <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <TarjetaVoz v-for="v in voces" :key="v.id" :voz="v" :elegida="trabajo!.voz === v.id"
                    @elegir="con(() => elegirVozYFormato(v.id, formato))" />
      </div>
      <div class="flex justify-between">
        <button class="boton-fantasma" @click="anterior"><ArrowLeft class="size-4" /> Atrás</button>
        <button class="boton-primario" :disabled="ocupado" @click="siguiente">Opciones <ArrowRight class="size-4" /></button>
      </div>
    </section>

    <!-- Opciones -->
    <section v-else-if="paso === 'opciones'" class="space-y-5">
      <h2 class="text-xl font-bold">{{ MENSAJES.opciones.titulo }}</h2>
      <div class="grid gap-4 lg:grid-cols-2">
        <fieldset class="tarjeta space-y-3 p-5" :disabled="ocupado">
          <legend class="sr-only">Qué lleva el video</legend>
          <label class="flex items-center gap-3"><input type="checkbox" checked disabled class="size-4 accent-acento" />
            <span><span class="font-semibold">Narración</span><span class="block text-sm text-suave">La voz lee las notas de cada diapositiva.</span></span></label>
          <label class="flex items-center gap-3">
            <input type="checkbox" class="size-4 accent-acento" :disabled="!config?.musica.length"
                   :checked="!!config?.musica.length && efectivos?.audio.musica_estilo !== false"
                   @change="cambiar('audio', 'musica_estilo', ($event.target as HTMLInputElement).checked)" />
            <span><span class="font-semibold">Música</span><span class="block text-sm text-suave">
              {{ config?.musica.length ? "Baja sola cuando habla la voz." : "Sube una pista en Configuración para usarla." }}</span></span></label>
          <label class="flex items-center gap-3">
            <input type="checkbox" class="size-4 accent-acento" :checked="efectivos?.video.subtitulos_quemados"
                   @change="cambiar('video', 'subtitulos_quemados', ($event.target as HTMLInputElement).checked)" />
            <span><span class="font-semibold">Subtítulos en la imagen</span><span class="block text-sm text-suave">Para que se entienda sin sonido. Los archivos de subtítulos salen siempre.</span></span></label>
          <label class="flex items-center gap-3">
            <input type="checkbox" class="size-4 accent-acento" :checked="conAnimaciones" @change="animaciones(($event.target as HTMLInputElement).checked)" />
            <span><span class="font-semibold">Animaciones</span><span class="block text-sm text-suave">Los textos entran y salen con movimiento.</span></span></label>
        </fieldset>
        <fieldset class="tarjeta p-5" :disabled="ocupado">
          <legend class="sr-only">Formato</legend>
          <p class="mb-3 font-semibold">¿Dónde se va a ver?</p>
          <div class="grid gap-2">
            <label v-for="f in proyecto.escena?.formatos ?? []" :key="f.id"
                   class="flex cursor-pointer items-center gap-3 rounded-lg border p-3 transition"
                   :class="formato === f.id ? 'border-acento bg-acento-suave' : 'border-borde hover:border-acento'">
              <input type="radio" name="formato" class="accent-acento" :checked="formato === f.id" @change="con(() => elegirVozYFormato(trabajo!.voz, f.id))" />
              <span class="grid h-7 w-7 place-items-center"><i class="block rounded-sm border-2 border-current text-acento"
                    :style="{ width: `${(f.ancho / Math.max(f.ancho, f.alto)) * 26}px`, height: `${(f.alto / Math.max(f.ancho, f.alto)) * 26}px` }" /></span>
              <span><span class="font-semibold">{{ FORMATOS_HUMANOS[f.id]?.titulo ?? f.nombre }}</span>
                <span class="block text-sm text-suave">{{ FORMATOS_HUMANOS[f.id]?.uso }}</span></span>
            </label>
          </div>
        </fieldset>
      </div>
      <AjustesAvanzados :trabajo="id" />
      <div class="flex justify-between">
        <button class="boton-fantasma" @click="anterior"><ArrowLeft class="size-4" /> Atrás</button>
        <button class="boton-primario" @click="siguiente">Continuar <ArrowRight class="size-4" /></button>
      </div>
    </section>

    <!-- Crear -->
    <section v-else-if="paso === 'crear'" class="space-y-5">
      <MensajeError v-if="generacion.error && !generacion.produciendo" :mensaje="generacion.error.mensaje"
                    :recuperacion="generacion.error.recuperacion" :codigo="generacion.error.codigo" :trabajo="id" :clave="claveConError"
                    @accion="accionError" />
      <EstadoGeneracion v-else-if="generacion.produciendo" :video="videoActual" :porcentaje="generacion.porcentaje"
                        :titulo="videos.length > 1 ? cuenta(videos.length, 'video') : undefined" />
      <div v-else class="tarjeta p-8 text-center">
        <Sparkles class="mx-auto size-10 text-acento" />
        <p class="mt-3 text-lg font-bold">Todo listo para crear tu video</p>
        <p class="mt-1 text-sm text-suave">{{ estiloActual ? `${estiloActual.icono} ${estiloActual.nombre}` : "Estilo de siempre" }} ·
          {{ FORMATOS_HUMANOS[formato]?.titulo }} · ~{{ Math.max(1, Math.round(proyecto.analisis.minutos)) }} min</p>
        <button class="boton-primario mt-6 px-8 py-3 text-base" :disabled="ocupado" @click="crear">{{ MENSAJES.generar.boton }}</button>
      </div>
      <button v-if="!generacion.produciendo" class="boton-fantasma" @click="anterior"><ArrowLeft class="size-4" /> Atrás</button>
    </section>

    <!-- Resultado -->
    <section v-else class="space-y-5">
      <div class="text-center">
        <p class="festejo text-2xl font-bold">{{ MENSAJES.listo.titulo }}</p>
        <p v-if="videos.length > 1" class="text-sm text-suave">{{ MENSAJES.listo.varios(videos.length) }}</p>
      </div>
      <div v-if="videos.length > 1 || versiones.length > 1" class="flex flex-wrap justify-center gap-2">
        <button v-if="proyecto.produccion?.completo?.archivos" class="rounded-full px-3 py-1 text-sm font-semibold"
                :class="clave === 'completo' ? 'bg-acento text-sobre-acento' : 'bg-superficie-2'" @click="clave = 'completo'">Curso completo</button>
        <button v-for="v in videos" :key="v.clave" class="max-w-56 truncate rounded-full px-3 py-1 text-sm font-semibold"
                :class="clave === v.clave ? 'bg-acento text-sobre-acento' : 'bg-superficie-2'" @click="clave = v.clave">{{ v.titulo }}</button>
      </div>
      <ReproductorPrevio v-if="videoMostrado" :mp4="videoMostrado.mp4" :vtt="videoMostrado.vtt" :formato="formato" :titulo="trabajo!.nombre" />
      <div v-if="versiones.length > 1" class="flex flex-wrap items-center justify-center gap-2 text-sm">
        <span class="text-suave">Versiones:</span>
        <button v-for="v in versiones" :key="v.version" class="rounded-lg px-2.5 py-1 font-semibold"
                :class="(version ?? versiones[0]!.version) === v.version ? 'bg-acento-suave text-acento' : 'hover:bg-superficie-2'"
                :title="v.duracion ? mmss(v.duracion) : ''" @click="version = v.version === versiones[0]!.version ? null : v.version">
          Versión {{ v.numero }}</button>
      </div>
      <div class="flex flex-wrap justify-center gap-2">
        <RouterLink v-if="clave && clave !== 'completo'" class="boton-primario" :to="`/crear/${id}/editar/${clave}`"><Pencil class="size-4" /> Editar</RouterLink>
        <button class="boton-secundario" :disabled="ocupado" @click="ir('crear'); crear()"><RefreshCw class="size-4" /> Regenerar</button>
      </div>
      <PanelExportar v-if="proyecto.produccion" :trabajo="id" :videos="videos" :produccion="proyecto.produccion" />
    </section>
  </div>
</template>
