<script setup lang="ts">
// Los ajustes de producción (video, tiempos, audio, curso completo). Se usa en Configuración
// (lo global) y en cada curso (lo propio). Edita una copia: quien lo usa decide cuándo guardar.
import { computed } from "vue";
import type { AjustesVideo, OpcionesConfig, PistaMusica } from "../tipos";

const modelo = defineModel<AjustesVideo>({ required: true });
const props = defineProps<{ opciones: OpcionesConfig; musica: PistaMusica[]; base?: AjustesVideo }>();

type Lista = { valor: string | number; texto: string }[];
const lista = (clave: string) => (props.opciones[clave] as Lista) ?? [];
const rango = (clave: string) => props.opciones[clave] as { min: number; max: number };

/** En un curso, marca lo que cambia respecto a la configuración global. */
function cambiado(grupo: keyof AjustesVideo, clave: string): boolean {
  if (!props.base) return false;
  const a = (modelo.value[grupo] as Record<string, unknown>)[clave];
  const b = (props.base[grupo] as Record<string, unknown>)[clave];
  return JSON.stringify(a) !== JSON.stringify(b);
}

const TIEMPOS = [
  { clave: "entrada", titulo: "Antes de la voz", ayuda: "Lo que tarda en entrar la lámina antes de que hable la voz" },
  { clave: "pausa", titulo: "Entre frases", ayuda: "Silencio entre frases de la misma lámina" },
  { clave: "salida", titulo: "Respiro final", ayuda: "Lo que queda la lámina después de la última frase" },
] as const;

const musicaElegida = computed(() => props.musica.find((m) => m.archivo === modelo.value.audio.musica));
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-2">
    <!-- Video -->
    <fieldset class="tarjeta space-y-4 p-5">
      <legend class="sr-only">Video</legend>
      <h3 class="font-bold">Video</h3>
      <label class="block">
        <span class="etiqueta-campo">Resolución <span v-if="cambiado('video', 'resolucion')" class="marca-cambio">cambiado</span></span>
        <select v-model="modelo.video.resolucion" class="campo">
          <option v-for="o in lista('video.resolucion')" :key="o.valor" :value="o.valor">{{ o.texto }}</option>
        </select>
      </label>
      <label class="block">
        <span class="etiqueta-campo">Cuadros por segundo <span v-if="cambiado('video', 'fps')" class="marca-cambio">cambiado</span></span>
        <select v-model.number="modelo.video.fps" class="campo">
          <option v-for="o in lista('video.fps')" :key="o.valor" :value="o.valor">{{ o.texto }}</option>
        </select>
      </label>
      <label class="block">
        <span class="etiqueta-campo">Calidad <span v-if="cambiado('video', 'calidad')" class="marca-cambio">cambiado</span></span>
        <select v-model="modelo.video.calidad" class="campo">
          <option v-for="o in lista('video.calidad')" :key="o.valor" :value="o.valor">{{ o.texto }}</option>
        </select>
      </label>
      <label class="flex items-start gap-3">
        <input v-model="modelo.video.subtitulos_quemados" type="checkbox" class="mt-1 size-4 accent-[var(--c-acento)]" />
        <span><span class="block text-sm font-medium">Subtítulos dentro de la imagen
          <span v-if="cambiado('video', 'subtitulos_quemados')" class="marca-cambio">cambiado</span></span>
          <span class="block text-xs text-suave">Para redes, donde se ve sin sonido. El VTT y el SRT salen igual.</span></span>
      </label>
    </fieldset>

    <!-- Tiempos -->
    <fieldset class="tarjeta space-y-4 p-5">
      <legend class="sr-only">Tiempos</legend>
      <h3 class="font-bold">Ritmo de cada lámina</h3>
      <label v-for="x in TIEMPOS" :key="x.clave" class="block">
        <span class="etiqueta-campo flex justify-between">
          <span>{{ x.titulo }} <span v-if="cambiado('tiempos', x.clave)" class="marca-cambio">cambiado</span></span>
          <span class="tabular-nums text-suave">{{ modelo.tiempos[x.clave].toFixed(2).replace(".", ",") }} s</span>
        </span>
        <input v-model.number="modelo.tiempos[x.clave]" type="range" step="0.05"
               :min="rango(`tiempos.${x.clave}`)?.min" :max="rango(`tiempos.${x.clave}`)?.max"
               class="w-full accent-[var(--c-acento)]" :aria-describedby="`ayuda-${x.clave}`" />
        <span :id="`ayuda-${x.clave}`" class="text-xs text-suave">{{ x.ayuda }}</span>
      </label>
    </fieldset>

    <!-- Audio -->
    <fieldset class="tarjeta space-y-4 p-5">
      <legend class="sr-only">Audio</legend>
      <h3 class="font-bold">Audio</h3>
      <label class="block">
        <span class="etiqueta-campo">Volumen final <span v-if="cambiado('audio', 'lufs')" class="marca-cambio">cambiado</span></span>
        <select v-model.number="modelo.audio.lufs" class="campo">
          <option v-for="o in lista('audio.lufs')" :key="o.valor" :value="o.valor">{{ o.texto }}</option>
        </select>
      </label>
      <label class="block">
        <span class="etiqueta-campo">Música de fondo <span v-if="cambiado('audio', 'musica')" class="marca-cambio">cambiado</span></span>
        <select v-model="modelo.audio.musica" class="campo">
          <option :value="null">Sin música</option>
          <option v-for="m in musica" :key="m.archivo" :value="m.archivo">{{ m.archivo }}</option>
        </select>
        <span v-if="musicaElegida" class="mt-1 block text-xs text-suave">Licencia: {{ musicaElegida.licencia ?? "sin registrar" }}</span>
        <span v-else-if="!musica.length" class="mt-1 block text-xs text-suave">Sube pistas en Configuración → Música.</span>
      </label>
      <label v-if="modelo.audio.musica" class="block">
        <span class="etiqueta-campo flex justify-between">
          <span>Volumen de la música <span v-if="cambiado('audio', 'musica_volumen')" class="marca-cambio">cambiado</span></span>
          <span class="tabular-nums text-suave">{{ modelo.audio.musica_volumen }} dB</span>
        </span>
        <input v-model.number="modelo.audio.musica_volumen" type="range" step="1"
               :min="rango('audio.musica_volumen')?.min" :max="rango('audio.musica_volumen')?.max" class="w-full accent-[var(--c-acento)]" />
        <span class="text-xs text-suave">Baja sola ~10 dB más mientras habla la voz.</span>
      </label>
    </fieldset>

    <!-- Curso completo -->
    <fieldset class="tarjeta space-y-4 p-5">
      <legend class="sr-only">Curso completo</legend>
      <h3 class="font-bold">Curso completo en un solo MP4</h3>
      <label class="flex items-start gap-3">
        <input v-model="modelo.completo.tarjetas" type="checkbox" class="mt-1 size-4 accent-[var(--c-acento)]" />
        <span><span class="block text-sm font-medium">Tarjeta con el título de cada video
          <span v-if="cambiado('completo', 'tarjetas')" class="marca-cambio">cambiado</span></span>
          <span class="block text-xs text-suave">Separa un video del siguiente dentro del MP4 completo.</span></span>
      </label>
      <label v-if="modelo.completo.tarjetas" class="block">
        <span class="etiqueta-campo flex justify-between"><span>Duración de la tarjeta</span>
          <span class="tabular-nums text-suave">{{ modelo.completo.duracion_tarjeta.toFixed(1).replace(".", ",") }} s</span></span>
        <input v-model.number="modelo.completo.duracion_tarjeta" type="range" step="0.5"
               :min="rango('completo.duracion_tarjeta')?.min" :max="rango('completo.duracion_tarjeta')?.max" class="w-full accent-[var(--c-acento)]" />
      </label>
      <label class="flex items-start gap-3">
        <input v-model="modelo.completo.capitulos" type="checkbox" class="mt-1 size-4 accent-[var(--c-acento)]" />
        <span><span class="block text-sm font-medium">Capítulos
          <span v-if="cambiado('completo', 'capitulos')" class="marca-cambio">cambiado</span></span>
          <span class="block text-xs text-suave">Dentro del MP4 y en capitulos.txt para pegar en YouTube.</span></span>
      </label>
    </fieldset>
  </div>
</template>

<style scoped>
@reference "../estilos.css";
.marca-cambio {
  @apply ml-1 rounded-full bg-acento-suave px-2 py-0.5 text-[11px] font-semibold text-acento;
}
</style>
