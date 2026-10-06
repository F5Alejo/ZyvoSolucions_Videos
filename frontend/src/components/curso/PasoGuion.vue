<script setup lang="ts">
import { computed, ref } from "vue";
import { CircleHelp, LoaderCircle, Pencil, RefreshCw, RotateCcw, Save, Search, TriangleAlert } from "@lucide/vue";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import { confirmar } from "../../composables/confirmar";
import { abrirAyuda } from "../../composables/ayuda";
import TextoResaltado from "../TextoResaltado.vue";
import PanelAgentes from "./PanelAgentes.vue";
import type { Lamina, TrabajoCompleto } from "../../tipos";
import { cuenta, mmss, normalizar } from "../../utils";

/** `videoInicial` y `soloRevisarInicial`: para llegar desde el Resumen directo a un video o a lo que hay que revisar. */
const props = defineProps<{ datos: TrabajoCompleto; videoInicial?: number; soloRevisarInicial?: boolean }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();

// ── Editar una lámina (sin tocar el original del PPTX) ──
const editando = ref<number | null>(null);
const borrador = ref({ titulo: "", vinetas: "", notas: "" });
const guardandoEdicion = ref(false);

function editar(l: Lamina) {
  editando.value = l.n;
  borrador.value = { titulo: l.pantalla?.titulo ?? l.titulo, vinetas: (l.pantalla?.vinetas ?? []).join("\n"), notas: l.notas };
}

async function guardarEdicion(n: number, cambios: Record<string, unknown> | null) {
  guardandoEdicion.value = true;
  try {
    const nuevo = await api.put<TrabajoCompleto>(`/api/trabajos/${props.datos.trabajo.id}/laminas/${n}/edicion`, { cambios });
    emit("actualizado", nuevo);
    editando.value = null;
    avisar(cambios ? `Lámina ${n} guardada.` : `La lámina ${n} volvió a su texto original.`);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    guardandoEdicion.value = false;
  }
}

function guardarBorrador(n: number) {
  const vinetas = borrador.value.vinetas.split("\n").map((x) => x.trim()).filter(Boolean);
  guardarEdicion(n, { titulo: borrador.value.titulo, notas: borrador.value.notas, ...(vinetas.length ? { vinetas } : {}) });
}

const reagrupando = ref(false);
async function reagrupar() {
  const si = await confirmar({
    titulo: "¿Volver a proponer los videos?",
    texto: "El estudio arma de nuevo los videos a partir de las diapositivas: un video por sección si tu presentación las marca, o por duración si no. El guion no cambia.",
    aceptar: "Proponer de nuevo",
  });
  if (!si) return;
  reagrupando.value = true;
  try {
    const antes = props.datos.resumen.videos.length;
    const nuevo = await api.post<TrabajoCompleto>(`/api/trabajos/${props.datos.trabajo.id}/reagrupar`);
    emit("actualizado", nuevo);
    elegido.value = 0;
    avisar(`Listo: ${cuenta(nuevo.resumen.videos.length, "video")} (antes ${antes}).`);
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    reagrupando.value = false;
  }
}
const t = computed(() => props.datos.trabajo);
const r = computed(() => props.datos.resumen);
const porN = computed(() => new Map(t.value.laminas.map((l) => [l.n, l])));
const porRevisar = computed(() => r.value.chequeos.filter((c) => c.ok !== true));

const elegido = ref(props.videoInicial ?? 0);
const busqueda = ref("");
const soloRevisar = ref(props.soloRevisarInicial ?? false);
const filtrando = computed(() => !!normalizar(busqueda.value) || soloRevisar.value);

const videos = computed(() =>
  r.value.videos.map((v, i) => {
    const laminas = v.laminas.map((n) => porN.value.get(n)).filter((l): l is Lamina => !!l);
    return { ...v, indice: i, laminas: laminas, citas: laminas.reduce((s, l) => s + l.citas.length, 0), mudas: laminas.filter((l) => !l.frases.length).length };
  }),
);

function pasa(l: Lamina): boolean {
  const q = normalizar(busqueda.value);
  return (!q || normalizar(`${l.titulo} ${l.notas}`).includes(q)) && (!soloRevisar.value || l.citas.length > 0 || !l.frases.length);
}
/** Sin filtro, el video elegido; con filtro, todos los videos que tengan alguna diapositiva que pase. */
const mostrados = computed(() =>
  filtrando.value
    ? videos.value.map((v) => ({ ...v, laminas: v.laminas.filter(pasa) })).filter((v) => v.laminas.length)
    : videos.value.slice(elegido.value, elegido.value + 1),
);
const totalMostradas = computed(() => mostrados.value.reduce((s, v) => s + v.laminas.length, 0));
</script>

<template>
  <section aria-labelledby="titulo-guion">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <h2 id="titulo-guion" class="text-xl font-bold">El guion de cada video</h2>
      <button v-if="datos.trabajo.origen.tipo === 'pptx'" type="button" class="boton-fantasma" :disabled="reagrupando" @click="reagrupar">
        <LoaderCircle v-if="reagrupando" class="size-4 animate-spin" /><RefreshCw v-else class="size-4" /> Volver a proponer los videos
      </button>
    </div>
    <p class="mt-1 max-w-3xl text-sm text-suave">
      Esto es lo que dirá la voz, frase por frase, tal como está en las notas de tu presentación.
      Lo <mark>resaltado</mark> son cifras y normas que conviene comprobar.
      <button class="inline-flex items-center gap-1 font-semibold text-acento hover:underline" @click="abrirAyuda('resaltado')"><CircleHelp class="size-3.5" /> ¿Por qué?</button>
    </p>

    <div v-if="porRevisar.length" class="mt-5 rounded-xl border border-aviso/40 bg-aviso-fondo p-4">
      <p class="flex items-center gap-2 font-bold text-aviso"><TriangleAlert class="size-5" /> Antes de seguir, revisa esto</p>
      <ul class="mt-2 space-y-1 pl-7 text-sm">
        <li v-for="c in porRevisar" :key="c.clave" class="list-disc"><strong>{{ c.titulo }}.</strong> {{ c.detalle }}. <span v-if="c.ayuda" class="text-suave">{{ c.ayuda }}</span></li>
      </ul>
    </div>

    <!-- Buscar y filtrar -->
    <div class="mt-6 flex flex-wrap items-center gap-3">
      <div class="relative min-w-[240px] flex-1">
        <Search class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-suave" />
        <input v-model="busqueda" type="search" class="campo pl-9" placeholder="Buscar en todo el guion…" aria-label="Buscar en el guion" />
      </div>
      <label class="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-borde bg-superficie px-3 py-2.5 text-sm has-[:checked]:border-aviso has-[:checked]:bg-aviso-fondo">
        <input v-model="soloRevisar" type="checkbox" class="size-4 accent-[var(--c-aviso)]" /> Solo lo que hay que revisar
      </label>
      <span v-if="filtrando" class="text-sm text-suave" aria-live="polite">{{ cuenta(totalMostradas, "diapositiva") }}</span>
    </div>

    <div class="mt-5 grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
      <!-- Lista de videos -->
      <nav aria-label="Videos del curso" class="lg:sticky lg:top-24 lg:max-h-[calc(100vh-8rem)] lg:overflow-y-auto">
        <ol class="flex gap-2 overflow-x-auto pb-2 lg:flex-col lg:overflow-visible lg:pb-0">
          <li v-for="v in videos" :key="v.clave" class="shrink-0 lg:shrink">
            <button type="button" @click="elegido = v.indice; busqueda = ''; soloRevisar = false"
              :aria-current="!filtrando && elegido === v.indice ? 'true' : undefined"
              class="flex w-56 items-start gap-3 rounded-lg border px-3 py-2.5 text-left transition lg:w-full"
              :class="!filtrando && elegido === v.indice ? 'border-acento bg-acento-suave' : 'border-transparent hover:bg-superficie'">
              <span class="grid size-7 shrink-0 place-items-center rounded-md bg-superficie-2 text-xs font-bold text-acento">{{ v.indice + 1 }}</span>
              <span class="min-w-0">
                <span class="line-clamp-2 text-sm font-semibold">{{ v.titulo }}</span>
                <span class="mt-0.5 flex flex-wrap gap-x-2 text-xs text-suave">
                  <span>{{ mmss(v.segundos) }}</span><span>{{ cuenta(v.frases, "frase") }}</span>
                  <span v-if="v.citas" class="font-semibold text-aviso">{{ v.citas }} por revisar</span>
                  <span v-if="v.mudas" class="font-semibold text-aviso">{{ cuenta(v.mudas, "diapositiva sin voz", "diapositivas sin voz") }}</span>
                </span>
              </span>
            </button>
          </li>
        </ol>
      </nav>

      <!-- Diapositivas y frases -->
      <div class="min-w-0 space-y-6">
        <PanelAgentes :trabajo="datos.trabajo.id" donde="guion" @actualizado="(d) => emit('actualizado', d)" />
        <p v-if="!mostrados.length" class="tarjeta p-8 text-center text-suave">Nada coincide con la búsqueda.</p>
        <article v-for="v in mostrados" :key="v.clave">
          <header class="mb-3">
            <p class="text-xs font-semibold tracking-wider text-suave uppercase">Video {{ v.indice + 1 }} · ~{{ mmss(v.segundos) }} min</p>
            <h3 class="text-lg font-bold">{{ v.titulo }}</h3>
          </header>
          <div class="space-y-3">
            <div v-for="l in v.laminas" :key="l.n" class="tarjeta p-4">
              <div class="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <span class="rounded-md bg-entra/10 px-2 py-0.5 text-xs font-bold text-entra">Diapositiva {{ l.n }}</span>
                <strong class="text-sm">{{ l.titulo }}</strong>
                <span class="text-xs text-suave">~{{ Math.round(l.segundos) }} s<template v-if="l.fuente_narracion"> · {{ l.fuente_narracion }}</template></span>
                <span v-if="l.editada" class="rounded-full bg-acento-suave px-2 py-0.5 text-[11px] font-semibold text-acento">editada</span>
                <span class="ml-auto flex gap-1">
                  <button v-if="l.editada && editando !== l.n" class="boton-fantasma !px-2 !py-1 text-xs" :disabled="guardandoEdicion"
                          @click="guardarEdicion(l.n, null)"><RotateCcw class="size-3.5" /> Original</button>
                  <button v-if="editando !== l.n" class="boton-fantasma !px-2 !py-1 text-xs" @click="editar(l)"><Pencil class="size-3.5" /> Editar</button>
                </span>
              </div>
              <form v-if="editando === l.n" class="mt-3 space-y-3" @submit.prevent="guardarBorrador(l.n)">
                <label class="block"><span class="etiqueta-campo">Título en pantalla</span>
                  <input v-model="borrador.titulo" class="campo" maxlength="120" required /></label>
                <label class="block"><span class="etiqueta-campo">Viñetas en pantalla (una por línea; vacío = las del PPTX)</span>
                  <textarea v-model="borrador.vinetas" class="campo" rows="3" /></label>
                <label class="block"><span class="etiqueta-campo">Lo que dice la voz</span>
                  <textarea v-model="borrador.notas" class="campo" rows="4" /></label>
                <div class="flex justify-end gap-2">
                  <button type="button" class="boton-fantasma" @click="editando = null">Cancelar</button>
                  <button class="boton-primario" :disabled="guardandoEdicion">
                    <LoaderCircle v-if="guardandoEdicion" class="size-4 animate-spin" /><Save v-else class="size-4" /> Guardar</button>
                </div>
              </form>
              <ol v-if="l.frases.length && editando !== l.n" class="mt-3 list-decimal space-y-1.5 pl-6 text-[15px] leading-relaxed marker:text-suave">
                <li v-for="(f, i) in l.frases" :key="i"><TextoResaltado :texto="f" :citas="l.citas" /></li>
              </ol>
              <p v-else-if="editando !== l.n" class="mt-3 flex items-center gap-2 rounded-lg bg-aviso-fondo p-3 text-sm text-aviso">
                <TriangleAlert class="size-4 shrink-0" /> Esta diapositiva no tiene notas: se vería sin voz. Escribe su guion en las notas del orador.
              </p>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
