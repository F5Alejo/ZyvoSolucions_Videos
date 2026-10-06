// El estado central del flujo creativo (/crear/:id): un solo lugar para el curso, su análisis,
// los estilos, la producción y la línea de tiempo. Las pantallas leen de aquí y piden cambios aquí.
import { computed, reactive } from "vue";
import { api } from "../api";
import { resumen as resumenProduccion } from "../generacion";
import type { Analisis, CatalogoEscena, EscenaCurso, Estilo, LineaDeTiempo, Produccion, TrabajoCompleto } from "../tipos";

interface Estado {
  id: string | null;
  datos: TrabajoCompleto | null;
  analisis: Analisis | null;
  estilos: Estilo[];
  escena: CatalogoEscena | null;
  produccion: Produccion | null;
  lineas: Record<string, LineaDeTiempo>;
  cargando: boolean;
  error: string | null;
}

export const proyecto = reactive<Estado>({
  id: null, datos: null, analisis: null, estilos: [], escena: null, produccion: null, lineas: {}, cargando: false, error: null,
});

export const trabajo = computed(() => proyecto.datos?.trabajo ?? null);
export const generacion = computed(() => resumenProduccion(proyecto.produccion));

let temporizador: ReturnType<typeof setTimeout> | undefined;

export async function abrir(id: string) {
  if (proyecto.id !== id) {
    detener();
    Object.assign(proyecto, { id, datos: null, analisis: null, produccion: null, lineas: {} });
  }
  proyecto.cargando = true;
  proyecto.error = null;
  try {
    const [datos, analisis, estilos, escena] = await Promise.all([
      api.get<TrabajoCompleto>(`/api/trabajos/${id}`),
      api.get<Analisis>(`/api/trabajos/${id}/analisis`),
      proyecto.estilos.length ? Promise.resolve(proyecto.estilos) : api.get<Estilo[]>("/api/estilos"),
      proyecto.escena ? Promise.resolve(proyecto.escena) : api.get<CatalogoEscena>("/api/catalogo/escena"),
    ]);
    Object.assign(proyecto, { datos, analisis, estilos, escena });
    await consultar();
  } catch (e) {
    proyecto.error = (e as Error).message;
  } finally {
    proyecto.cargando = false;
  }
}

function actualizar(d: TrabajoCompleto) {
  proyecto.datos = { trabajo: d.trabajo, resumen: d.resumen };
  proyecto.lineas = {}; // el plan cambió: la línea de tiempo se vuelve a pedir
}

export async function elegirEstilo(estilo: string) {
  actualizar(await api.put<TrabajoCompleto>(`/api/trabajos/${proyecto.id}/estilo`, { estilo, con_formato: false }));
}

export async function elegirVozYFormato(voz: string, formato: string) {
  const t = trabajo.value!;
  actualizar(await api.patch<TrabajoCompleto>(`/api/trabajos/${proyecto.id}`, { marca: t.marca, voz, formatos: [formato] }));
}

export async function fijarAjustes(ajustes: Record<string, Record<string, unknown>> | null) {
  actualizar(await api.put<TrabajoCompleto>(`/api/trabajos/${proyecto.id}/ajustes-video`, { ajustes }));
}

/** Cambia un solo ajuste de video del curso, sin perder los demás que ya tenía propios. */
export async function cambiarAjuste(grupo: string, clave: string, valor: unknown) {
  const { propios } = await api.get<{ propios: Record<string, Record<string, unknown>> }>(`/api/trabajos/${proyecto.id}/ajustes-video`);
  await fijarAjustes({ ...propios, [grupo]: { ...(propios[grupo] ?? {}), [clave]: valor } });
}

export async function restaurarLamina(n: number) {
  actualizar(await api.put<TrabajoCompleto>(`/api/trabajos/${proyecto.id}/laminas/${n}/edicion`, { cambios: null }));
}

export async function fijarEscena(escena: EscenaCurso) {
  actualizar(await api.put<TrabajoCompleto>(`/api/trabajos/${proyecto.id}/escena`, escena));
}

export async function editarNarracion(n: number, notas: string) {
  actualizar(await api.put<TrabajoCompleto>(`/api/trabajos/${proyecto.id}/laminas/${n}/edicion`, { cambios: { notas } }));
}

export async function lineaDeTiempo(clave: string): Promise<LineaDeTiempo> {
  proyecto.lineas[clave] ??= await api.get<LineaDeTiempo>(`/api/trabajos/${proyecto.id}/linea/${clave}`);
  return proyecto.lineas[clave]!;
}

/** Produce lo que falta (y el MP4 completo si el curso tiene varios videos). */
export async function generar() {
  const varios = (trabajo.value?.videos.length ?? 0) > 1;
  proyecto.produccion = await api.post<Produccion>(`/api/trabajos/${proyecto.id}/producir-todo?completo=${varios}`);
  vigilar();
}

export async function regenerar(clave: string, cambios: { escena?: number; voz?: boolean }) {
  proyecto.produccion = await api.post<Produccion>(`/api/trabajos/${proyecto.id}/regenerar/${clave}`, cambios);
  delete proyecto.lineas[clave];
  vigilar();
}

export async function consultar() {
  if (!proyecto.id) return;
  proyecto.produccion = await api.get<Produccion>(`/api/trabajos/${proyecto.id}/produccion`);
  if (generacion.value.produciendo) vigilar();
  else proyecto.lineas = {}; // terminó: los tiempos reales reemplazan a los estimados
}

function vigilar() {
  clearTimeout(temporizador);
  temporizador = setTimeout(() => consultar().catch(() => vigilar()), 2500);
}

export function detener() {
  clearTimeout(temporizador);
}
