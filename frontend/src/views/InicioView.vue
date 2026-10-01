<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { ArrowRight, Bell, CircleCheck, Film, FileText, Presentation, Sparkles, Upload, Clapperboard } from "@lucide/vue";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import EstadoCarga from "../components/EstadoCarga.vue";
import TarjetaCifra from "../components/TarjetaCifra.vue";
import TarjetaCurso from "../components/TarjetaCurso.vue";
import VacioCaja from "../components/VacioCaja.vue";
import type { Inicio } from "../tipos";
import { cuenta } from "../utils";

const router = useRouter();
const { datos: d, cargando, error, recargar } = useCarga(() => api.get<Inicio>("/api/inicio"));

const atencion = computed(() => (d.value?.conteo_estados.sin_estado ?? 0) + (d.value?.conteo_estados.revision ?? 0));
const cursosRecientes = computed(() => d.value?.trabajos.slice(0, 3) ?? []);

async function abrirEjemplo() {
  try {
    const { id } = await api.post<{ id: string }>("/api/trabajos/ejemplo-csm");
    router.push(`/cursos/${id}`);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <EstadoCarga v-if="!d" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="space-y-10">
    <!-- Portada: qué hace el estudio y la acción principal -->
    <section class="relative overflow-hidden rounded-2xl bg-lateral px-6 py-8 text-white sm:px-10 sm:py-10">
      <div class="relative max-w-2xl">
        <p class="text-sm font-semibold tracking-wider text-dorado uppercase">Estudio de video</p>
        <h1 class="mt-2 text-3xl leading-tight font-bold sm:text-4xl">Entra un PPTX.<br />Sale el curso en video.</h1>
        <p class="mt-3 text-white/80">
          Sube una presentación de capacitación y el estudio la convierte en los videos del curso, con la marca y la voz que elijas.
          Cada frase que dice el video sale de tu presentación.
        </p>
        <div class="mt-6 flex flex-wrap gap-3">
          <RouterLink to="/cursos/nuevo"
            class="inline-flex items-center gap-2 rounded-lg bg-dorado px-5 py-3 text-sm font-bold text-[#1A1A1A] transition hover:brightness-110">
            <Upload class="size-4" /> Crear un curso
          </RouterLink>
          <button v-if="d.ejemplo_disponible" @click="abrirEjemplo"
            class="inline-flex items-center gap-2 rounded-lg border border-white/40 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/10">
            <Sparkles class="size-4" /> Ver un ejemplo real
          </button>
        </div>
      </div>
      <!-- Los dos anillos del manual de RiskMann: cian y dorado -->
      <svg class="pointer-events-none absolute -right-16 -bottom-24 hidden size-80 opacity-60 md:block" viewBox="0 0 200 200" aria-hidden="true">
        <circle cx="100" cy="100" r="80" fill="none" stroke="#06C7FB" stroke-width="10" opacity=".55" />
        <circle cx="100" cy="100" r="66" fill="none" stroke="#C8951A" stroke-width="2" />
      </svg>
    </section>

    <!-- Cifras -->
    <section aria-label="Resumen" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      <TarjetaCifra :valor="d.trabajos.length" texto="cursos en el estudio" :icono="Presentation" a="/cursos" />
      <TarjetaCifra :valor="d.conteo_estados.final ?? 0" texto="videos entregados" :icono="CircleCheck" tono="exito" a="/videos?estado=final" />
      <TarjetaCifra :valor="atencion" texto="videos sin estado o en revisión" :icono="Film" :tono="atencion ? 'aviso' : 'normal'" a="/videos?atencion=1" />
      <TarjetaCifra :valor="d.pendientes_abiertos" texto="pendientes con las marcas" :icono="Bell" a="/pendientes" />
    </section>

    <!-- Cómo funciona -->
    <section aria-labelledby="como-funciona">
      <h2 id="como-funciona" class="mb-4 text-lg font-bold">Cómo funciona</h2>
      <ol class="grid gap-3 md:grid-cols-3">
        <li class="tarjeta border-t-4 border-t-entra p-5">
          <span class="text-xs font-bold tracking-wider text-entra uppercase">1 · Entra</span>
          <p class="mt-1 font-bold">Tu presentación</p>
          <p class="mt-1 text-sm text-suave">El PPTX con sus láminas y las notas del orador, que son el guion.</p>
          <p v-if="d.cifras_ejemplo" class="mt-4 text-sm text-suave"><span class="cifra text-2xl text-texto">{{ d.cifras_ejemplo.laminas }}</span> láminas en el ejemplo</p>
        </li>
        <li class="tarjeta border-t-4 border-t-motor p-5">
          <span class="text-xs font-bold tracking-wider text-motor uppercase">2 · El estudio</span>
          <p class="mt-1 font-bold">Lo prepara contigo</p>
          <ul class="mt-1 space-y-1 text-sm text-suave">
            <li>Arma el guion lámina por lámina</li>
            <li>Muestra de dónde sale cada frase</li>
            <li>Aplica la marca y la voz</li>
            <li>Avisa si hay cifras o normas por revisar</li>
          </ul>
        </li>
        <li class="tarjeta border-t-4 border-t-exito p-5">
          <span class="text-xs font-bold tracking-wider text-exito uppercase">3 · Sale</span>
          <p class="mt-1 font-bold">Los videos del curso</p>
          <p class="mt-1 text-sm text-suave">Un video por módulo, las preguntas de evaluación y un informe de revisión.</p>
          <p v-if="d.cifras_ejemplo" class="mt-4 text-sm text-suave">
            <span class="cifra text-2xl text-texto">{{ d.cifras_ejemplo.videos }}</span> videos · {{ d.cifras_ejemplo.minutos }} min en el ejemplo
          </p>
        </li>
      </ol>
    </section>

    <!-- Cursos -->
    <section aria-labelledby="tus-cursos">
      <div class="mb-4 flex items-center justify-between gap-4">
        <h2 id="tus-cursos" class="text-lg font-bold">Tus cursos</h2>
        <RouterLink v-if="d.trabajos.length > 3" to="/cursos" class="inline-flex items-center gap-1 text-sm font-semibold text-acento hover:underline">
          Ver los {{ d.trabajos.length }} <ArrowRight class="size-4" />
        </RouterLink>
      </div>
      <div v-if="cursosRecientes.length" class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <TarjetaCurso v-for="t in cursosRecientes" :key="t.id" :curso="t" />
      </div>
      <VacioCaja v-else :icono="FileText" titulo="Todavía no hay cursos"
                 texto="Sube una presentación para crear el primero, o mira cómo quedó un curso real.">
        <RouterLink to="/cursos/nuevo" class="boton-primario"><Upload class="size-4" /> Crear un curso</RouterLink>
        <button v-if="d.ejemplo_disponible" class="boton-secundario" @click="abrirEjemplo">Ver el ejemplo</button>
      </VacioCaja>
    </section>

    <!-- Piezas de marketing -->
    <section aria-labelledby="marketing">
      <h2 id="marketing" class="text-lg font-bold">Piezas de marketing ya hechas</h2>
      <p class="mt-1 mb-4 text-sm text-suave">No salen de un PPTX: el equipo las diseña una por una. Mira qué entró y qué salió.</p>
      <div class="grid gap-3 md:grid-cols-3">
        <RouterLink v-for="c in d.casos" :key="c.id" :to="`/casos/${c.id}`"
                    class="tarjeta group flex gap-4 p-3 transition hover:border-acento hover:shadow-sm">
          <video v-if="c.portada" :src="`/media/entregables/${c.portada}#t=3`" muted playsinline preload="metadata" aria-hidden="true"
                 class="aspect-[9/16] w-20 shrink-0 rounded-lg bg-black object-cover" />
          <div v-else class="grid aspect-[9/16] w-20 shrink-0 place-items-center rounded-lg bg-superficie-2"><Clapperboard class="size-6 text-suave" /></div>
          <div class="min-w-0 py-1">
            <p class="text-xs font-semibold text-suave">{{ catalogo?.marcas[c.marca]?.nombre_corto }}</p>
            <p class="font-bold group-hover:text-acento">{{ c.titulo }}</p>
            <p class="mt-1 text-sm text-suave">{{ c.resumen }}</p>
            <p class="mt-2 text-xs font-semibold text-acento">{{ cuenta(c.total_videos, "video") }} →</p>
          </div>
        </RouterLink>
      </div>
    </section>

    <p v-if="!d.repositorio_conectado" class="rounded-lg bg-aviso-fondo p-4 text-sm text-aviso">
      La carpeta del repositorio de videos no está conectada: no se verán videos, logos ni el ejemplo. Revisa <code>config.local.json</code>.
    </p>
  </div>
</template>
