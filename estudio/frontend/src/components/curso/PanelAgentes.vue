<script setup lang="ts">
// Los agentes de un paso del curso: ejecutarlos, ver su avance y aceptar o descartar sus propuestas.
import { computed, onUnmounted, ref, watch } from "vue";
import { Bot, Check, CircleAlert, LoaderCircle, Play, Sparkles, X } from "lucide-vue-next";
import { api } from "../../api";
import { avisar } from "../../composables/avisos";
import type { AgentesCurso, Propuesta, TrabajoCompleto } from "../../tipos";

const props = defineProps<{ trabajo: string; donde: string; solo?: string[] }>();
const emit = defineEmits<{ actualizado: [TrabajoCompleto] }>();

const datos = ref<AgentesCurso | null>(null);
let temporizador: ReturnType<typeof setTimeout> | undefined;

const agentes = computed(() => (datos.value?.agentes ?? []).filter((a) => a.donde === props.donde && (!props.solo || props.solo.includes(a.id))));
const trabajando = (id: string) => ["en_cola", "produciendo"].includes(datos.value?.estados[id]?.estado ?? "");
const pendientes = (id: string) => (datos.value?.propuestas ?? []).filter((p) => p.agente === id && p.estado === "pendiente");

async function consultar() {
  clearTimeout(temporizador);
  const antes = agentes.value.filter((a) => trabajando(a.id)).map((a) => a.id);
  try {
    datos.value = await api.get<AgentesCurso>(`/api/trabajos/${props.trabajo}/agentes`);
  } catch { /* se reintenta */ }
  for (const id of antes) {
    const e = datos.value?.estados[id];
    if (e?.estado === "listo") avisar(`${nombre(id)}: ${e.propuestas ?? 0} propuestas${e.con_ia ? " con IA" : " con reglas"}.`);
    if (e?.estado === "error") avisar(e.mensaje ?? "El agente falló", "error");
  }
  if (agentes.value.some((a) => trabajando(a.id))) temporizador = setTimeout(consultar, 2500);
}
watch(() => props.trabajo, consultar, { immediate: true });
onUnmounted(() => clearTimeout(temporizador));

const nombre = (id: string) => datos.value?.agentes.find((a) => a.id === id)?.nombre ?? id;

async function ejecutar(id: string) {
  try {
    datos.value = await api.post<AgentesCurso>(`/api/trabajos/${props.trabajo}/agentes/${id}`);
    temporizador = setTimeout(consultar, 1200);
  } catch (e) {
    avisar((e as Error).message, "error");
  }
}

const resolviendo = ref<string | null>(null);
async function resolver(p: Propuesta, accion: "aceptar" | "descartar") {
  resolviendo.value = p.id;
  try {
    const r = await api.post<TrabajoCompleto & AgentesCurso>(`/api/trabajos/${props.trabajo}/propuestas/${p.id}/${accion}`);
    datos.value = { agentes: r.agentes, estados: r.estados, propuestas: r.propuestas };
    emit("actualizado", { trabajo: r.trabajo, resumen: r.resumen });
  } catch (e) {
    avisar((e as Error).message, "error");
  } finally {
    resolviendo.value = null;
  }
}

async function aceptarTodas(id: string) {
  for (const p of pendientes(id)) await resolver(p, "aceptar");
}

/** Muestra un valor de propuesta como texto legible. */
function legible(x: unknown): string {
  if (x === null || x === undefined) return "—";
  if (typeof x === "string") return x;
  const o = x as Record<string, unknown>;
  if ("titulo" in o && "vinetas" in o) return [o.titulo, ...((o.vinetas as string[]) ?? []).map((v) => `• ${v}`)].join("\n");
  if ("notas" in o) return (o.notas as string) || "(sin narración)";
  if ("resumen" in o) return o.resumen as string;
  if ("plantilla" in o) return `Estilo: ${o.plantilla ?? "el del curso"}`;
  if ("pregunta" in o) return `${o.tipo}: ${o.pregunta}`;
  if ("preguntas" in o) return (o.preguntas as { enunciado: string; correcta: string }[]).map((q, i) => `${i + 1}. ${q.enunciado}\n   ✓ ${q.correcta}`).join("\n");
  if ("coincidencia" in o) return `Coincide el ${o.coincidencia} %` + ((o.faltan as string[]).length ? `\nNo se oyó: ${(o.faltan as string[]).join(" · ")}` : "");
  if ("alt" in o) return `${o.tipo === "contenido" ? "Contenido" : "No es contenido (" + o.tipo + ")"}\nTexto alternativo: ${o.alt}`;
  if ("descripcion" in o) return [o.titulo, "", o.descripcion, "", `Etiquetas: ${(o.etiquetas as string[]).join(", ")}`, "", ...((o.historias as string[]) ?? []).map((h) => `Historia: ${h}`)].join("\n");
  return JSON.stringify(x, null, 1);
}
</script>

<template>
  <section v-if="agentes.length" class="tarjeta p-5" aria-label="Agentes">
    <h3 class="flex items-center gap-2 font-bold"><Bot class="size-5 text-acento" /> Agentes de este paso</h3>
    <p class="mt-1 mb-4 text-sm text-suave">Proponen; tú decides. Nada cambia hasta que aceptes.</p>

    <div v-for="a in agentes" :key="a.id" class="border-t border-borde py-4 first-of-type:border-t-0 first-of-type:pt-0">
      <div class="flex flex-wrap items-center gap-3">
        <div class="min-w-0 flex-1">
          <strong class="text-sm">{{ a.nombre }}</strong>
          <span class="ml-2 rounded-full px-2 py-0.5 text-[11px] font-semibold"
                :class="a.con_ia ? 'bg-acento-suave text-acento' : 'bg-superficie-2 text-suave'">
            <template v-if="a.con_ia"><Sparkles class="inline size-3" /> {{ a.modelo }}</template>
            <template v-else-if="a.modelo">{{ a.necesita_ia ? "necesita Ollama" : "sin IA: reglas" }}</template>
            <template v-else>sin IA</template>
          </span>
          <span class="block text-xs text-suave">{{ a.que }}</span>
        </div>
        <template v-if="trabajando(a.id)">
          <span class="flex items-center gap-2 text-xs text-suave"><LoaderCircle class="size-4 animate-spin text-acento" />
            {{ datos?.estados[a.id]?.paso ?? "En la cola…" }}</span>
        </template>
        <button v-else class="boton-secundario !py-1.5 text-sm" :disabled="!a.activo || (a.necesita_ia && !a.con_ia)"
                :title="!a.activo ? 'Desactivado en Configuración' : a.necesita_ia && !a.con_ia ? 'Necesita Ollama con su modelo' : ''"
                @click="ejecutar(a.id)"><Play class="size-4" /> {{ pendientes(a.id).length ? "Volver a proponer" : "Proponer" }}</button>
      </div>
      <p v-if="datos?.estados[a.id]?.estado === 'error'" class="mt-2 flex items-start gap-2 text-sm text-error">
        <CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ datos.estados[a.id]?.mensaje }}</p>

      <!-- Propuestas pendientes -->
      <ul v-if="pendientes(a.id).length" class="mt-3 space-y-3">
        <li v-for="p in pendientes(a.id)" :key="p.id" class="rounded-lg border border-borde p-3">
          <div class="flex flex-wrap items-start gap-2">
            <div class="min-w-0 flex-1">
              <strong class="block text-sm">{{ p.titulo }}</strong>
              <span class="text-xs text-suave">{{ p.razon }} · {{ p.hecha_con === "reglas" ? "reglas" : p.hecha_con }}</span>
            </div>
            <div class="flex gap-1">
              <button v-if="a.acepta" class="boton-primario !px-3 !py-1.5 text-xs" :disabled="resolviendo === p.id" @click="resolver(p, 'aceptar')">
                <Check class="size-3.5" /> {{ a.id === "verificador" ? "Fuente revisada" : "Aceptar" }}</button>
              <button class="boton-fantasma !px-3 !py-1.5 text-xs" :disabled="resolviendo === p.id" @click="resolver(p, 'descartar')">
                <X class="size-3.5" /> {{ a.acepta ? "Descartar" : "Listo" }}</button>
            </div>
          </div>
          <div class="mt-2 grid gap-2 text-sm" :class="p.antes ? 'sm:grid-cols-2' : ''">
            <div v-if="p.antes" class="rounded-md bg-superficie-2 p-2">
              <span class="mb-1 block text-[11px] font-semibold text-suave uppercase">Ahora</span>
              <p class="whitespace-pre-line">{{ legible(p.antes) }}</p>
            </div>
            <div class="rounded-md bg-acento-suave/60 p-2">
              <span class="mb-1 block text-[11px] font-semibold text-acento uppercase">{{ p.antes ? "Propuesta" : "Detalle" }}</span>
              <p class="whitespace-pre-line">{{ legible(p.despues) }}</p>
            </div>
          </div>
        </li>
        <li v-if="a.acepta && pendientes(a.id).length > 1" class="text-right">
          <button class="boton-fantasma text-xs" @click="aceptarTodas(a.id)"><Check class="size-3.5" /> Aceptar las {{ pendientes(a.id).length }}</button>
        </li>
      </ul>
    </div>
  </section>
</template>
