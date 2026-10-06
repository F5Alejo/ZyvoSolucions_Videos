<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft, ArrowRight, Building2, CircleAlert, ImageUp, LoaderCircle, PartyPopper, Plus, Sparkles, Trash2, Upload, X } from "@lucide/vue";
import { api, enviarFormulario } from "../api";
import { avisar } from "../composables/avisos";
import { cargarCatalogo, catalogo } from "../composables/catalogo";
import EstadoCarga from "../components/EstadoCarga.vue";
import SelectorVoz from "../components/SelectorVoz.vue";
import VistaPreviaVideo from "../components/VistaPreviaVideo.vue";
import type { DatosEmpresa, Marca } from "../tipos";
import { contraste, mb } from "../utils";

/** Sin `id`: registrar una empresa nueva. Con `id`: editar una empresa registrada. */
const props = defineProps<{ id?: string }>();
const ruta = useRoute();
const router = useRouter();
const editando = computed(() => !!props.id);
const volver = computed(() => (typeof ruta.query.volver === "string" && ruta.query.volver.startsWith("/") ? ruta.query.volver : null));

const PASOS = [
  { id: "datos", titulo: "Tu empresa" },
  { id: "logo", titulo: "Logo" },
  { id: "colores", titulo: "Colores" },
  { id: "voz", titulo: "Voz y cierre" },
] as const;
const indice = ref(0);
const paso = computed(() => PASOS[indice.value]!.id);

const f = ref<DatosEmpresa>({ nombre: "", nombre_corto: "", que_es: "", sitio_web: "", responsable: "", colores: ["#26367D"], voz: "carlos", cta: "" });
const cortoTocado = ref(false);
watch(() => f.value.nombre, (n) => { if (!cortoTocado.value) f.value.nombre_corto = n.replace(/\s+(S\.?A\.?S\.?|S\.?A\.?|LTDA\.?|BIC)\b.*$/i, "").trim().slice(0, 24); });

// ── Cargar la empresa al editar ─────────────────────────────────────────────
const cargando = ref(false);
const errorCarga = ref<string | null>(null);
const logoActual = ref<string | null>(null);
async function cargar() {
  if (!props.id) return;
  cargando.value = true;
  errorCarga.value = null;
  try {
    const m = await api.get<Marca>(`/api/marcas/${props.id}`);
    if (!m.registrada) throw new Error("Esta es una de las marcas base del estudio: no se edita desde aquí.");
    f.value = {
      nombre: m.nombre, nombre_corto: m.nombre_corto, que_es: m.que_es === "Empresa registrada en el estudio" ? "" : m.que_es,
      sitio_web: m.dominio ?? "", responsable: m.responsable ?? "", colores: m.paleta.map((c) => c.hex),
      voz: m.voz_id ?? "carlos", cta: m.cta ?? "",
    };
    cortoTocado.value = true;
    logoActual.value = m.logo_url;
  } catch (e) {
    errorCarga.value = (e as Error).message;
  } finally {
    cargando.value = false;
  }
}
cargar();

// ── Logo ─────────────────────────────────────────────────────────────────────
const logo = ref<File | null>(null);
const logoUrl = ref<string | null>(null);
const logoFondo = ref<"claro" | "oscuro">("claro");
const sugeridos = ref<string[]>([]);
const leyendoLogo = ref(false);
const errorLogo = ref<string | null>(null);
const coloresTocados = ref(false);
const encima = ref(false);

async function elegirLogo(archivo: File | undefined) {
  errorLogo.value = null;
  if (!archivo) return;
  if (!/\.(png|jpe?g|webp)$/i.test(archivo.name)) {
    errorLogo.value = "El logo tiene que ser una imagen PNG, JPG o WebP. Si lo tienes en otro formato (SVG, PDF, AI), exporta una versión en PNG.";
    return;
  }
  if (archivo.size > 5 * 1024 * 1024) {
    errorLogo.value = `El logo pesa ${mb(archivo.size)} y el máximo es 5 MB.`;
    return;
  }
  if (logoUrl.value) URL.revokeObjectURL(logoUrl.value);
  logo.value = archivo;
  logoUrl.value = URL.createObjectURL(archivo);
  logoFondo.value = await fondoDelLogo(logoUrl.value);
  leyendoLogo.value = true;
  try {
    const datos = new FormData();
    datos.append("logo", archivo);
    const { colores } = await enviarFormulario<{ colores: string[] }>("POST", "/api/empresas/colores", datos);
    sugeridos.value = colores;
    if (colores.length && !coloresTocados.value) f.value.colores = colores.slice(0, 3);
  } catch (e) {
    errorLogo.value = (e as Error).message;
    quitarLogo();
  } finally {
    leyendoLogo.value = false;
  }
}

function quitarLogo() {
  if (logoUrl.value) URL.revokeObjectURL(logoUrl.value);
  logo.value = null;
  logoUrl.value = null;
  sugeridos.value = [];
}
onBeforeUnmount(() => { if (logoUrl.value) URL.revokeObjectURL(logoUrl.value); });

/** Si el logo es claro (por ejemplo, blanco), necesita fondo oscuro para verse. */
function fondoDelLogo(url: string): Promise<"claro" | "oscuro"> {
  return new Promise((resolver) => {
    const img = new Image();
    img.onload = () => {
      const lienzo = document.createElement("canvas");
      lienzo.width = 64; lienzo.height = 64;
      const ctx = lienzo.getContext("2d");
      if (!ctx) return resolver("claro");
      ctx.drawImage(img, 0, 0, 64, 64);
      const d = ctx.getImageData(0, 0, 64, 64).data;
      let suma = 0, n = 0;
      for (let i = 0; i < d.length; i += 4) if (d[i + 3]! > 200) { suma += 0.2126 * d[i]! + 0.7152 * d[i + 1]! + 0.0722 * d[i + 2]!; n++; }
      resolver(n && suma / n / 255 > 0.72 ? "oscuro" : "claro");
    };
    img.onerror = () => resolver("claro");
    img.src = url;
  });
}

// ── Colores ──────────────────────────────────────────────────────────────────
const NOMBRES = ["Principal", "Acento", "Complementario", "Apoyo", "Detalle", "Extra"];
function cambiarColor(i: number, valor: string) {
  coloresTocados.value = true;
  f.value.colores[i] = valor.toUpperCase();
}
function agregarColor(hex = "#C8951A") {
  if (f.value.colores.length >= 6 || f.value.colores.includes(hex.toUpperCase())) return;
  coloresTocados.value = true;
  f.value.colores.push(hex.toUpperCase());
}
function quitarColor(i: number) {
  if (f.value.colores.length <= 1) return;
  coloresTocados.value = true;
  f.value.colores.splice(i, 1);
}
const hexValido = (c: string) => /^#[0-9A-Fa-f]{6}$/.test(c);
const textoEnVideos = computed(() => {
  const c = f.value.colores[0] ?? "#000000";
  if (!hexValido(c)) return "";
  return contraste("#FFFFFF", c) >= contraste("#111111", c) ? "blanco" : "negro";
});

/** La empresa tal como se verá, para la vista previa en vivo. */
const marcaPrevia = computed<Marca>(() => ({
  id: "previa", nombre: f.value.nombre || "Tu empresa", nombre_corto: f.value.nombre_corto || f.value.nombre || "Tu empresa",
  que_es: f.value.que_es, dominio: f.value.sitio_web || null, responsable: null, fuente_ficha: "", revisada: "",
  paleta: f.value.colores.filter(hexValido).map((hex, i) => ({ hex, nombre: NOMBRES[i] ?? "" })), paleta_fuente: "",
  tipografia: "", voz: "", cta: f.value.cta || null, contradicciones: [], fuentes: [], pendientes: [], pedir_al_cliente: [],
  logo: { fondo: logoUrl.value ? logoFondo.value : "claro" }, logo_url: logoUrl.value ?? logoActual.value, registrada: true,
}));

// ── Avanzar y guardar ────────────────────────────────────────────────────────
const errorPaso = ref<string | null>(null);
function validar(): string | null {
  if (paso.value === "datos") {
    if (f.value.nombre.trim().length < 2) return "Escribe el nombre de la empresa.";
    if (f.value.nombre_corto.trim().length > 24) return "El nombre corto puede tener hasta 24 caracteres.";
  }
  if (paso.value === "colores") {
    if (!f.value.colores.length) return "Elige al menos el color principal.";
    if (f.value.colores.some((c) => !hexValido(c))) return "Hay un color que no es válido. Usa el formato #RRGGBB.";
  }
  return null;
}
function ir(delta: number) {
  errorPaso.value = delta > 0 ? validar() : null;
  if (errorPaso.value) return;
  indice.value = Math.min(Math.max(indice.value + delta, 0), PASOS.length - 1);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

const guardando = ref(false);
const lista = ref<Marca | null>(null);
async function guardar() {
  errorPaso.value = validar();
  if (errorPaso.value) return;
  guardando.value = true;
  try {
    const datos = new FormData();
    datos.append("datos", JSON.stringify(f.value));
    if (logo.value) datos.append("logo", logo.value);
    const m = editando.value
      ? await enviarFormulario<Marca>("PUT", `/api/empresas/${props.id}`, datos)
      : await enviarFormulario<Marca>("POST", "/api/empresas", datos);
    await cargarCatalogo(true);
    if (editando.value) {
      avisar("Cambios guardados.");
      router.push(`/marcas/${m.id}`);
    } else {
      lista.value = m;
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  } catch (e) {
    errorPaso.value = (e as Error).message;
  } finally {
    guardando.value = false;
  }
}

const vocesListas = computed(() => !!catalogo.value?.voces.length);
</script>

<template>
  <EstadoCarga v-if="cargando || errorCarga" :cargando="cargando" :error="errorCarga" @reintentar="cargar" />

  <!-- Registrada -->
  <div v-else-if="lista" class="mx-auto max-w-2xl py-6 text-center">
    <span class="mx-auto grid size-20 place-items-center rounded-full bg-exito-fondo text-exito"><PartyPopper class="size-10" /></span>
    <h1 class="mt-5 text-3xl font-bold">¡{{ lista.nombre_corto }} ya está registrada!</h1>
    <p class="mx-auto mt-2 max-w-md text-suave">Desde ahora aparece al elegir la marca de un curso, con sus colores y su logo.</p>
    <div class="mx-auto mt-8 max-w-sm"><VistaPreviaVideo titulo="Módulo 1 · Así se verán tus videos" :numero="1" :segundos="120" :marca="lista" /></div>
    <div class="mt-10 flex flex-wrap justify-center gap-3">
      <RouterLink v-if="volver" :to="volver" class="boton-primario px-6 py-3 text-base">Seguir con mi curso <ArrowRight class="size-4" /></RouterLink>
      <RouterLink v-else :to="`/cursos/nuevo?marca=${lista.id}`" class="boton-primario px-6 py-3 text-base"><Upload class="size-5" /> Crear un curso para {{ lista.nombre_corto }}</RouterLink>
      <RouterLink :to="`/marcas/${lista.id}`" class="boton-secundario px-6 py-3 text-base">Ver la empresa</RouterLink>
    </div>
  </div>

  <div v-else class="mx-auto max-w-5xl">
    <!-- Progreso -->
    <div class="mb-8">
      <div class="flex items-center justify-between text-sm">
        <p class="font-semibold text-suave">{{ editando ? "Editar empresa" : "Registrar empresa" }} · paso {{ indice + 1 }} de {{ PASOS.length }}</p>
        <RouterLink :to="volver ?? (editando ? `/marcas/${id}` : '/empresas')" class="text-suave hover:text-acento hover:underline">Cancelar</RouterLink>
      </div>
      <ol class="mt-3 flex gap-2" aria-label="Pasos">
        <li v-for="(p, i) in PASOS" :key="p.id" class="flex-1">
          <span class="block h-1.5 rounded-full transition-colors duration-500" :class="i <= indice ? 'bg-acento' : 'bg-borde'" />
          <span class="mt-1.5 hidden text-xs sm:block" :class="i === indice ? 'font-bold text-texto' : 'text-suave'">{{ p.titulo }}</span>
        </li>
      </ol>
    </div>

    <div class="grid grid-cols-[minmax(0,1fr)] gap-10 lg:grid-cols-[minmax(0,1fr)_300px]">
      <div>
        <!-- 1. Datos -->
        <section v-if="paso === 'datos'" aria-labelledby="t-datos" class="space-y-5">
          <div>
            <h1 id="t-datos" class="text-3xl font-bold">{{ editando ? "Los datos de la empresa" : "¿Cómo se llama tu empresa?" }}</h1>
            <p class="mt-2 text-suave">Con esto la reconocerás en el estudio. Solo el nombre es obligatorio.</p>
          </div>
          <div>
            <label for="nombre" class="etiqueta-campo">Nombre de la empresa</label>
            <input id="nombre" v-model="f.nombre" class="campo py-3 text-base" placeholder="Por ejemplo: Transportes del Llano S.A.S." autocomplete="organization" />
          </div>
          <div class="grid grid-cols-[minmax(0,1fr)] gap-5 sm:grid-cols-2">
            <div>
              <label for="corto" class="etiqueta-campo">Nombre corto <span class="font-normal text-suave">(así sale en el estudio)</span></label>
              <input id="corto" v-model="f.nombre_corto" maxlength="24" class="campo" placeholder="Transportes del Llano" @input="cortoTocado = true" />
            </div>
            <div>
              <label for="sitio" class="etiqueta-campo">Sitio web <span class="font-normal text-suave">(opcional)</span></label>
              <input id="sitio" v-model="f.sitio_web" class="campo" placeholder="miempresa.com" inputmode="url" autocomplete="url" />
            </div>
          </div>
          <div>
            <label for="que" class="etiqueta-campo">¿A qué se dedica? <span class="font-normal text-suave">(opcional)</span></label>
            <textarea id="que" v-model="f.que_es" rows="2" maxlength="200" class="campo" placeholder="Por ejemplo: transporte de carga por carretera en los Llanos Orientales" />
          </div>
          <div>
            <label for="resp" class="etiqueta-campo">Persona de contacto <span class="font-normal text-suave">(opcional)</span></label>
            <input id="resp" v-model="f.responsable" maxlength="80" class="campo" placeholder="Quien aprueba los videos de la empresa" autocomplete="name" />
          </div>
        </section>

        <!-- 2. Logo -->
        <section v-else-if="paso === 'logo'" aria-labelledby="t-logo" class="space-y-5">
          <div>
            <h1 id="t-logo" class="text-3xl font-bold">Sube el logo</h1>
            <p class="mt-2 text-suave">Con el logo proponemos los colores de la marca. Si no lo tienes a mano, puedes seguir sin él y agregarlo después.</p>
          </div>
          <div v-if="!logoUrl"
               class="relative rounded-3xl border-2 border-dashed px-6 py-12 text-center transition"
               :class="encima ? 'border-acento bg-acento-suave' : 'border-borde bg-superficie hover:border-acento'"
               @dragenter.prevent="encima = true" @dragover.prevent="encima = true" @dragleave.prevent="encima = false"
               @drop.prevent="encima = false; elegirLogo($event.dataTransfer?.files[0])">
            <input id="logo" type="file" accept="image/png,image/jpeg,image/webp" class="absolute inset-0 cursor-pointer opacity-0"
                   aria-describedby="logo-ayuda" @change="elegirLogo(($event.target as HTMLInputElement).files?.[0])" />
            <span class="mx-auto grid size-14 place-items-center rounded-2xl bg-acento text-sobre-acento"><ImageUp class="size-7" /></span>
            <p class="mt-4 text-lg font-bold">Arrastra aquí el logo</p>
            <p id="logo-ayuda" class="mt-1 text-sm text-suave">o haz clic para buscarlo · PNG, JPG o WebP hasta 5 MB · mejor con fondo transparente</p>
            <p v-if="editando && logoActual" class="mt-3 text-xs text-suave">Si no subes uno nuevo, se conserva el actual.</p>
          </div>
          <div v-else class="tarjeta rounded-2xl p-5">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex h-32 items-center justify-center rounded-xl border border-borde bg-white p-4"><img :src="logoUrl" alt="Logo sobre fondo blanco" class="max-h-full max-w-full object-contain" /></div>
              <div class="flex h-32 items-center justify-center rounded-xl border border-borde bg-[#0b0d0f] p-4"><img :src="logoUrl" alt="Logo sobre fondo oscuro" class="max-h-full max-w-full object-contain" /></div>
            </div>
            <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
              <p class="text-sm">
                <span class="font-semibold">{{ logo?.name }}</span>
                <span class="text-suave"> · {{ logoFondo === "oscuro" ? "se ve mejor sobre fondo oscuro" : "se ve bien sobre fondo claro" }}</span>
              </p>
              <button type="button" class="boton-fantasma" @click="quitarLogo"><X class="size-4" /> Cambiar logo</button>
            </div>
            <p v-if="leyendoLogo" class="mt-3 flex items-center gap-2 text-sm text-suave"><LoaderCircle class="size-4 animate-spin" /> Buscando los colores del logo…</p>
            <p v-else-if="sugeridos.length" class="mt-3 flex flex-wrap items-center gap-2 text-sm text-suave">
              <Sparkles class="size-4 text-acento" /> Colores del logo:
              <span v-for="c in sugeridos" :key="c" class="size-5 rounded-full ring-1 ring-borde" :style="{ background: c }" :title="c" />
            </p>
          </div>
          <p v-if="errorLogo" class="flex items-start gap-2 rounded-xl bg-error-fondo p-4 text-sm text-error" role="alert"><CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ errorLogo }}</p>
        </section>

        <!-- 3. Colores -->
        <section v-else-if="paso === 'colores'" aria-labelledby="t-colores" class="space-y-5">
          <div>
            <h1 id="t-colores" class="text-3xl font-bold">Los colores de la marca</h1>
            <p class="mt-2 text-suave">
              <template v-if="sugeridos.length && !coloresTocados">Los tomamos de tu logo. </template>
              El principal es el fondo de los videos; el acento, los detalles. La vista previa cambia en vivo.
            </p>
          </div>
          <ul class="space-y-3">
            <li v-for="(c, i) in f.colores" :key="i" class="tarjeta flex items-center gap-4 rounded-2xl p-3">
              <label class="relative size-14 shrink-0 cursor-pointer overflow-hidden rounded-xl ring-1 ring-borde" :style="{ background: hexValido(c) ? c : 'transparent' }">
                <input type="color" :value="hexValido(c) ? c.toLowerCase() : '#000000'" class="absolute inset-0 cursor-pointer opacity-0"
                       :aria-label="`Elegir el color ${NOMBRES[i]}`" @input="cambiarColor(i, ($event.target as HTMLInputElement).value)" />
              </label>
              <div class="min-w-0 flex-1">
                <p class="font-semibold">{{ NOMBRES[i] }}</p>
                <p class="text-xs text-suave">{{ i === 0 ? "Fondo de los videos" : i === 1 ? "Barras, rótulos y detalles" : "Para usar en las piezas" }}</p>
              </div>
              <input :value="c" maxlength="7" class="campo w-28 font-mono uppercase" :class="!hexValido(c) && 'border-error'"
                     :aria-label="`Código del color ${NOMBRES[i]}`" @input="cambiarColor(i, ($event.target as HTMLInputElement).value)" />
              <button v-if="f.colores.length > 1" type="button" class="boton-fantasma" :aria-label="`Quitar el color ${NOMBRES[i]}`" @click="quitarColor(i)"><Trash2 class="size-4" /></button>
            </li>
          </ul>
          <div class="flex flex-wrap items-center gap-3">
            <button v-if="f.colores.length < 6" type="button" class="boton-secundario" @click="agregarColor()"><Plus class="size-4" /> Agregar color</button>
            <template v-if="sugeridos.some((s) => !f.colores.includes(s))">
              <span class="text-sm text-suave">Del logo:</span>
              <button v-for="s in sugeridos.filter((x) => !f.colores.includes(x))" :key="s" type="button" @click="agregarColor(s)"
                      class="size-8 rounded-full ring-2 ring-borde transition hover:scale-110 hover:ring-acento" :style="{ background: s }" :aria-label="`Agregar ${s}`" :title="`Agregar ${s}`" />
            </template>
          </div>
          <p v-if="textoEnVideos" class="text-sm text-suave">Para que se lea, el texto de los videos irá en <strong class="text-texto">{{ textoEnVideos }}</strong> sobre el color principal.</p>
        </section>

        <!-- 4. Voz y cierre -->
        <section v-else aria-labelledby="t-voz" class="space-y-6">
          <div>
            <h1 id="t-voz" class="text-3xl font-bold">La voz y el cierre</h1>
            <p class="mt-2 text-suave">La voz que usarán sus cursos por defecto (se puede cambiar en cada curso) y lo que dicen al terminar.</p>
          </div>
          <SelectorVoz v-if="vocesListas" v-model="f.voz" />
          <div>
            <label for="cta" class="etiqueta-campo">¿Qué dice el final de los videos? <span class="font-normal text-suave">(opcional)</span></label>
            <input id="cta" v-model="f.cta" maxlength="160" class="campo py-3" :placeholder="`Por ejemplo: Conoce más en ${f.sitio_web || 'miempresa.com'}`" />
          </div>
        </section>

        <p v-if="errorPaso" class="mt-6 flex items-start gap-2 rounded-xl bg-error-fondo p-4 text-sm text-error" role="alert"><CircleAlert class="mt-0.5 size-4 shrink-0" /> {{ errorPaso }}</p>

        <!-- Navegación -->
        <div class="mt-10 flex items-center justify-between gap-3 border-t border-borde pt-6">
          <button v-if="indice > 0" type="button" class="boton-fantasma" @click="ir(-1)"><ArrowLeft class="size-4" /> Atrás</button>
          <span v-else />
          <button v-if="indice < PASOS.length - 1" type="button" class="boton-primario px-6 py-3 text-base" @click="ir(1)">
            {{ paso === "logo" && !logoUrl && !(editando && logoActual) ? "Seguir sin logo" : "Continuar" }} <ArrowRight class="size-4" />
          </button>
          <button v-else type="button" class="boton-primario px-6 py-3 text-base" :disabled="guardando" @click="guardar">
            <LoaderCircle v-if="guardando" class="size-5 animate-spin" /><Building2 v-else class="size-5" />
            {{ editando ? "Guardar cambios" : "Registrar empresa" }}
          </button>
        </div>
      </div>

      <!-- Vista previa en vivo -->
      <aside class="lg:sticky lg:top-6 lg:self-start" aria-label="Vista previa">
        <p class="mb-2 text-sm font-semibold text-suave">Así se verán sus videos</p>
        <VistaPreviaVideo :titulo="`Módulo 1 · Bienvenidos a ${marcaPrevia.nombre_corto}`" :subtitulo="f.que_es || undefined"
                          :numero="1" :segundos="120" :marca="marcaPrevia" />
        <div class="mt-3 flex h-3 overflow-hidden rounded-full ring-1 ring-borde" aria-hidden="true">
          <i v-for="c in marcaPrevia.paleta" :key="c.hex" class="flex-1" :style="{ background: c.hex }" />
        </div>
      </aside>
    </div>
  </div>
</template>
