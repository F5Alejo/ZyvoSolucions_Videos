<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { ArrowRight, Bell, CircleCheck, Clapperboard, Film, Palette, Sparkles, Upload } from "lucide-vue-next";
import { api } from "../api";
import { useCarga } from "../composables/carga";
import { avisar } from "../composables/avisos";
import { catalogo } from "../composables/catalogo";
import EstadoCarga from "../components/EstadoCarga.vue";
import TarjetaCurso from "../components/TarjetaCurso.vue";
import VistaPreviaVideo from "../components/VistaPreviaVideo.vue";
import type { Inicio } from "../tipos";
import { cuenta, fecha, mmss } from "../utils";

const router = useRouter();
const { datos: d, cargando, error, recargar } = useCarga(() => api.get<Inicio>("/api/inicio"));

const reciente = computed(() => d.value?.trabajos[0]);
const otros = computed(() => d.value?.trabajos.slice(1, 7) ?? []);
const atencion = computed(() => (d.value?.conteo_estados.sin_estado ?? 0) + (d.value?.conteo_estados.revision ?? 0));

async function abrirEjemplo() {
  try {
    const { id } = await api.post<{ id: string }>("/api/trabajos/ejemplo-csm");
    router.push(`/cursos/${id}/asistente`);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}
</script>

<template>
  <EstadoCarga v-if="!d" :cargando="cargando" :error="error" @reintentar="recargar()" />
  <div v-else class="space-y-14">
    <!-- Portada: la del manual de RiskMann. Siempre negra, en los dos temas: es la firma de la marca. -->
    <section class="relative isolate overflow-hidden rounded-3xl border border-[#272725] bg-[#020202] text-white">
      <!-- El caballero con los anillos cian y dorado (manual de identidad, modo oscuro) -->
      <img src="/marca/banco/caballero-anillos.webp" alt="" aria-hidden="true"
           class="absolute inset-y-0 right-0 -z-10 h-full w-full object-cover object-[70%_30%] opacity-90 sm:w-[70%]
                  [mask-image:linear-gradient(to_left,black_45%,transparent_100%)]" />
      <div class="absolute inset-0 -z-10 bg-gradient-to-t from-[#020202] via-transparent to-transparent sm:hidden" />
      <div class="grid grid-cols-[minmax(0,1fr)] items-end gap-8 px-6 py-10 sm:px-10 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:py-16">
        <div>
          <p class="text-sm font-semibold tracking-[0.2em] text-[#C8951A] uppercase">Estudio de video · RiskMann</p>
          <h1 class="mt-4 text-4xl leading-[1.08] font-bold sm:text-5xl">
            Convierte tu presentación en un <span class="text-[#C8951A]">curso en video</span>
          </h1>
          <p class="mt-5 max-w-xl text-lg text-white/75">Sube tu PowerPoint, elige la marca y la voz, y el estudio arma un video por módulo con tu propio guion.</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink to="/cursos/nuevo"
              class="inline-flex items-center gap-2 rounded-xl bg-[#C8951A] px-6 py-3.5 text-base font-bold text-[#020202] shadow-lg shadow-[#C8951A]/20 transition hover:-translate-y-px hover:brightness-110">
              <Upload class="size-5" /> Crear un curso
            </RouterLink>
            <button v-if="d.ejemplo_disponible" @click="abrirEjemplo"
              class="inline-flex items-center gap-2 rounded-xl border border-[#06C7FB]/50 px-6 py-3.5 text-base font-semibold text-white transition hover:bg-[#06C7FB]/10">
              <Sparkles class="size-5 text-[#06C7FB]" /> Ver un ejemplo
            </button>
          </div>
        </div>
        <!-- Lo que sale: un video de ejemplo con la marca RiskMann -->
        <div class="relative ml-auto hidden w-full max-w-xs lg:block" aria-hidden="true">
          <div class="rotate-[-2deg] shadow-2xl shadow-black/60 ring-1 ring-[#C8951A]/40 transition duration-500 hover:rotate-0 rounded-xl">
            <VistaPreviaVideo titulo="Módulo 1 · El conductor como actor vial" subtitulo="Conducir es una operación de alto riesgo que se desarrolla en un entorno cambiante."
                              :numero="1" :segundos="147" :marca="catalogo?.marcas.riskmann" foto="via-cabina.webp" />
          </div>
          <p class="mt-3 text-right text-xs text-white/60">Así se ve cada video</p>
        </div>
      </div>
    </section>

    <!-- Continúa donde quedaste -->
    <section v-if="reciente" aria-labelledby="t-reciente">
      <h2 id="t-reciente" class="mb-4 text-xl font-bold">Continúa donde quedaste</h2>
      <RouterLink :to="`/cursos/${reciente.id}`"
        class="tarjeta group grid grid-cols-[minmax(0,1fr)] overflow-hidden rounded-2xl transition hover:border-acento hover:shadow-lg sm:grid-cols-[280px_minmax(0,1fr)]">
        <div class="p-3 sm:p-4">
          <VistaPreviaVideo :titulo="reciente.nombre" :segundos="reciente.segundos" :marca="catalogo?.marcas[reciente.marca]" />
        </div>
        <div class="flex flex-col justify-center gap-2 p-5 sm:pl-2">
          <p class="text-xs font-semibold text-suave">{{ catalogo?.marcas[reciente.marca]?.nombre_corto }} · {{ fecha(reciente.creado) }}</p>
          <p class="text-2xl font-bold group-hover:text-acento">{{ reciente.nombre }}</p>
          <p class="text-suave">{{ cuenta(reciente.laminas, "diapositiva") }} → {{ cuenta(reciente.videos, "video") }} · {{ mmss(reciente.segundos) }} min</p>
          <span class="mt-2 inline-flex items-center gap-2 font-semibold text-acento">Abrir el curso <ArrowRight class="size-4 transition group-hover:translate-x-1" /></span>
        </div>
      </RouterLink>
    </section>

    <!-- Cómo funciona -->
    <section aria-labelledby="t-como">
      <h2 id="t-como" class="mb-5 text-xl font-bold">Así de fácil</h2>
      <ol class="grid grid-cols-[minmax(0,1fr)] gap-4 md:grid-cols-3">
        <li v-for="(p, i) in [
          { icono: Upload, foto: 'capacitaciones.webp', titulo: 'Sube tu PowerPoint', texto: 'Con el guion escrito en las notas del orador de cada diapositiva.' },
          { icono: Palette, foto: 'casco.webp', titulo: 'Elige marca y voz', texto: 'Colores, logo y una voz profesional. Puedes escuchar cada voz antes.' },
          { icono: Clapperboard, foto: 'seguridad-vial.webp', titulo: 'Recibe tus videos', texto: 'Un video por módulo, en horizontal o vertical, con preguntas de evaluación.' },
        ]" :key="i" class="tarjeta overflow-hidden rounded-2xl">
          <!-- Foto del banco de RiskMann -->
          <div class="relative h-36 overflow-hidden">
            <img :src="`/marca/banco/${p.foto}`" alt="" class="h-full w-full object-cover transition duration-700 hover:scale-105" loading="lazy" />
            <div class="absolute inset-0 bg-gradient-to-t from-[#020202]/70 to-transparent" />
            <span class="absolute bottom-3 left-4 grid size-10 place-items-center rounded-xl bg-[#C8951A] text-[#020202] shadow-lg">
              <component :is="p.icono" class="size-5" />
            </span>
            <span class="absolute right-4 bottom-2 text-4xl font-bold text-white/80" aria-hidden="true">{{ i + 1 }}</span>
          </div>
          <div class="p-5">
            <p class="text-lg font-bold">{{ p.titulo }}</p>
            <p class="mt-1 text-sm text-suave">{{ p.texto }}</p>
          </div>
        </li>
      </ol>
    </section>

    <!-- Más cursos -->
    <section v-if="otros.length" aria-labelledby="t-cursos">
      <div class="mb-4 flex items-center justify-between gap-4">
        <h2 id="t-cursos" class="text-xl font-bold">Tus otros cursos</h2>
        <RouterLink to="/cursos" class="inline-flex items-center gap-1 text-sm font-semibold text-acento hover:underline">Ver todos <ArrowRight class="size-4" /></RouterLink>
      </div>
      <div class="grid grid-cols-[minmax(0,1fr)] gap-4 md:grid-cols-2 xl:grid-cols-3">
        <TarjetaCurso v-for="t in otros" :key="t.id" :curso="t" />
      </div>
    </section>

    <!-- Para el equipo de producción -->
    <section aria-labelledby="t-equipo" class="rounded-3xl border border-borde bg-superficie-2 p-6 sm:p-8">
      <h2 id="t-equipo" class="text-lg font-bold">Para el equipo de producción</h2>
      <p class="mt-1 text-sm text-suave">El seguimiento de los videos ya hechos para las cuatro marcas.</p>
      <div class="mt-5 grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-3">
        <RouterLink to="/videos?estado=final" class="tarjeta flex items-center gap-3 rounded-xl p-4 transition hover:border-acento">
          <CircleCheck class="size-5 text-exito" /><span><span class="cifra block text-xl">{{ d.conteo_estados.final ?? 0 }}</span><span class="text-sm text-suave">videos entregados</span></span>
        </RouterLink>
        <RouterLink to="/videos?atencion=1" class="tarjeta flex items-center gap-3 rounded-xl p-4 transition hover:border-acento">
          <Film class="size-5 text-aviso" /><span><span class="cifra block text-xl">{{ atencion }}</span><span class="text-sm text-suave">necesitan atención</span></span>
        </RouterLink>
        <RouterLink to="/pendientes" class="tarjeta flex items-center gap-3 rounded-xl p-4 transition hover:border-acento">
          <Bell class="size-5 text-acento" /><span><span class="cifra block text-xl">{{ d.pendientes_abiertos }}</span><span class="text-sm text-suave">pendientes con marcas</span></span>
        </RouterLink>
      </div>
      <p class="mt-6 mb-3 text-sm font-semibold">Piezas de marketing ya hechas</p>
      <div class="grid grid-cols-[minmax(0,1fr)] gap-3 md:grid-cols-3">
        <RouterLink v-for="c in d.casos" :key="c.id" :to="`/casos/${c.id}`" class="tarjeta group flex gap-3 rounded-xl p-3 transition hover:border-acento">
          <video v-if="c.portada" :src="`/media/entregables/${c.portada}#t=3`" muted playsinline preload="metadata" aria-hidden="true"
                 class="aspect-[9/16] w-14 shrink-0 rounded-lg bg-black object-cover" />
          <span class="min-w-0 py-0.5">
            <span class="block text-sm font-bold group-hover:text-acento">{{ c.titulo }}</span>
            <span class="mt-0.5 line-clamp-2 text-xs text-suave">{{ c.resumen }}</span>
          </span>
        </RouterLink>
      </div>
    </section>

    <p v-if="!d.repositorio_conectado" class="rounded-xl bg-aviso-fondo p-4 text-sm text-aviso">
      La carpeta de videos no está conectada: no se verán videos, logos ni el ejemplo. Revisa <code>config.local.json</code>.
    </p>
  </div>
</template>
