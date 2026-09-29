// Lo que devuelve la API (app/main.py). Si cambia allá, cambia aquí.

export type Estado = "sin_estado" | "borrador" | "revision" | "aprobado" | "final" | "archivado";
export type Familia = "A" | "B";

export interface Color { hex: string; nombre: string; capa?: string }
export interface Item { texto: string; hecho: boolean }
export interface Fuente { fuente: string; tipo: string; donde: string; url?: string | null }

export interface Marca {
  id: string;
  nombre: string;
  nombre_corto: string;
  que_es: string;
  dominio: string | null;
  responsable: string | null;
  fuente_ficha: string;
  revisada: string;
  paleta: Color[];
  paleta_fuente: string;
  capas_paleta?: Record<string, { titulo: string; fuente: string; uso: string }>;
  tipografia: string;
  voz: string;
  cta: string | null;
  contradicciones: string[];
  hallazgos?: { fecha: string; texto: string }[];
  fuentes: Fuente[];
  pendientes: Item[];
  pedir_al_cliente: Item[];
  logo?: { archivo: string; fondo: "claro" | "oscuro" };
  logo_url: string | null;
}

export interface Voz {
  id: string;
  nombre: string;
  descripcion: string;
  proveedor: string;
  voice_id: string | null;
  muestra_url: string | null;
  /** Lo que falta para producir con esta voz (modelo, clave…); null si ya se puede. */
  falta: string | null;
  /** Su licencia no permite entregar: los videos salen con sello «BORRADOR». */
  solo_borrador?: boolean;
}

export interface Catalogo {
  estados: Record<Estado, string>;
  familias: Record<Familia, string>;
  formatos: Record<string, string>;
  marcas: Record<string, Marca>;
  voces: Voz[];
  pendientes_abiertos: number;
}

export interface Entregable { archivo: string; nota: string; existe?: boolean }
export interface Cambio { fecha: string; de: Estado; a: Estado; quien: string; nota: string }

export interface Proyecto {
  id: string;
  titulo: string;
  marca: string;
  familia: Familia;
  formato: string;
  duracion: string | null;
  estado: Estado;
  estado_original: string;
  donde: string | null;
  nota?: string;
  aprobado_por?: string;
  aprobado_el?: string;
  historial?: Cambio[];
  carpetas?: string[];
  entregables?: Entregable[];
  carpetas_detalle?: { nombre: string; existe: boolean; meta: Record<string, string> | null }[];
  entregables_detalle?: (Entregable & { existe: boolean })[];
}

export interface Lamina {
  n: number;
  formas: Record<string, string[]>;
  notas: string;
  frases: string[];
  foto: string | null;
  icono: string | null;
  titulo: string;
  segundos: number;
  citas: string[];
  fuente_narracion?: string;
}

export interface VideoPlan { clave: string; titulo: string; laminas: number[]; segundos: number; frases: number }
export interface Chequeo { ok: boolean | null; titulo: string; detalle: string }
export interface Pregunta { enunciado: string; correcta: string; distractores: string[]; fuente: string }
export interface Banco { nombre: string | null; grupos: { clave: string; titulo: string; tema: string; preguntas: Pregunta[] }[] }

export interface Trabajo {
  id: string;
  nombre: string;
  creado: string;
  origen: { tipo: "pptx" | "ejemplo"; archivo: string; bytes?: number; nota?: string };
  marca: string;
  voz: string;
  formatos: string[];
  laminas: Lamina[];
  videos: { clave: string; titulo: string; laminas: number[] }[];
  excluidas: Record<string, string>;
  banco: Banco | null;
}

export interface Resumen {
  videos: VideoPlan[];
  segundos: number;
  frases: number;
  palabras: number;
  normativas: { lamina: number; citas: string[] }[];
  chequeos: Chequeo[];
  preguntas: number;
  sin_uso: number[];
}

export interface TrabajoCompleto { trabajo: Trabajo; resumen: Resumen }

/** El motor (GET /api/trabajos/:id/produccion). */
export type EstadoRender = "en_cola" | "produciendo" | "listo" | "error";

export interface InformeRender {
  video: string;
  titulo: string;
  creado: string;
  marca: string;
  voz: string;
  borrador: boolean;
  duracion: number;
  chequeos: Chequeo[];
}

export interface VideoRender {
  estado: EstadoRender;
  paso: string | null;
  progreso: number | null;
  mensaje: string | null;
  informe: InformeRender | null;
  /** Se produjo con otra marca o voz que la elegida ahora. */
  desactualizado: boolean;
  archivos: { mp4: string; vtt: string; srt: string } | null;
}

export interface Produccion {
  voz_falta: string | null;
  voz_borrador: boolean;
  videos: Record<string, VideoRender | null>;
}

export interface TrabajoFila {
  id: string;
  nombre: string;
  creado: string;
  origen: Trabajo["origen"];
  marca: string;
  voz: string;
  videos: number;
  laminas: number;
  segundos: number;
}

export interface Inicio {
  cifras_ejemplo: { laminas: number; videos: number; minutos: number; frases: number; preguntas: number; palabras: number } | null;
  ejemplo_disponible: boolean;
  trabajos: TrabajoFila[];
  casos: { id: string; titulo: string; resumen: string; marca: string; portada: string | null; total_videos: number }[];
  conteo_estados: Partial<Record<Estado, number>>;
  total_videos: number;
  pendientes_abiertos: number;
  repositorio_conectado: boolean;
}

export interface Caso {
  id: string;
  titulo: string;
  resumen: string;
  marca: string;
  entra: { tipo: string; texto: string; url?: string }[];
  motor: string[];
  salida: Proyecto[];
  videos: (Entregable & { existe: boolean })[];
  documento_url: string | null;
}
