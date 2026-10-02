// Del estado técnico del motor a lo que entiende una persona: pasos, porcentaje y qué hacer si falla.
import type { FaseMotor, Produccion, VideoRender } from "./tipos";

export interface PasoGeneracion { id: string; texto: string; estado: "hecho" | "actual" | "pendiente" }

/** Los pasos que ve la persona, en orden, y desde qué fase del motor cuenta cada uno como empezado. */
const PASOS: { id: string; texto: string; fases: FaseMotor[] }[] = [
  { id: "escenas", texto: "Preparando escenas", fases: ["SCRIPTING", "SCRIPT_READY"] },
  { id: "voz", texto: "Generando narración", fases: ["GENERATING_AUDIO", "AUDIO_READY"] },
  { id: "animacion", texto: "Aplicando animaciones", fases: ["BUILDING_SCENES", "SCENES_READY"] },
  { id: "audio", texto: "Mezclando audio", fases: [] },
  { id: "video", texto: "Renderizando video", fases: ["RENDERING", "RENDERED"] },
  { id: "calidad", texto: "Revisando calidad", fases: ["QA_RUNNING", "QA_PASSED", "QA_FAILED"] },
];

function indice(v: VideoRender | null | undefined): number {
  if (!v) return -1;
  if (v.estado === "listo" || v.fase === "COMPLETED") return PASOS.length;
  if (!v.fase || v.fase === "QUEUED") return v.estado === "produciendo" ? 0 : -1;
  // «Mezclando el audio» es parte de RENDERING en el motor: se distingue por el texto del paso.
  if (v.fase === "RENDERING" && (v.paso ?? "").toLowerCase().includes("audio")) return 3;
  const i = PASOS.findIndex((p) => p.fases.includes(v.fase as FaseMotor));
  return i < 0 ? 0 : i;
}

/** Los pasos de un video: los anteriores hechos, el actual marcado, el resto pendiente. */
export function pasos(v: VideoRender | null | undefined): PasoGeneracion[] {
  const actual = indice(v);
  return PASOS.map((p, i) => ({ id: p.id, texto: p.texto, estado: i < actual ? "hecho" : i === actual ? "actual" : "pendiente" }));
}

const enCurso = (v: VideoRender | null | undefined) => v?.estado === "en_cola" || v?.estado === "produciendo";

/** Resumen de todo el curso: porcentaje (0-100), si sigue produciendo, si terminó y el video que va. */
export function resumen(p: Produccion | null) {
  const videos = Object.entries(p?.videos ?? {});
  if (!p || !videos.length) return { porcentaje: 0, produciendo: false, listo: false, error: null as VideoRender | null, actual: null as VideoRender | null };
  const valor = (v: VideoRender | null) => (v?.estado === "listo" ? 1 : enCurso(v) ? (v?.progreso ?? 0) : 0);
  const porcentaje = Math.round((100 * videos.reduce((s, [, v]) => s + valor(v), 0)) / videos.length);
  const error = videos.map(([, v]) => v).find((v) => v?.estado === "error") ?? null;
  const actual = videos.map(([, v]) => v).find((v) => v?.estado === "produciendo") ??
    videos.map(([, v]) => v).find((v) => v?.estado === "en_cola") ?? null;
  const produciendo = videos.some(([, v]) => enCurso(v)) || enCurso(p.completo as VideoRender | null);
  const listo = videos.every(([, v]) => v?.estado === "listo" && !v.desactualizado);
  return { porcentaje, produciendo, listo, error, actual };
}

/** Un mensaje técnico nunca llega tal cual: sin trazas, rutas ni códigos de salida. */
export function mensajeHumano(texto: string | null | undefined): string {
  const t = (texto ?? "").trim();
  if (!t || /traceback|exited with|errno|subprocess|jsondecode|\.py\b|[A-Z]:\\/i.test(t)) {
    return "Algo salió mal al crear el video.";
  }
  return t;
}
