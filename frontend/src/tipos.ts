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
  logo?: { archivo?: string; archivo_local?: string; fondo: "claro" | "oscuro" };
  logo_url: string | null;
  /** true si la registró una empresa desde el estudio; false en las marcas base. */
  registrada: boolean;
  voz_id?: string | null;
  creada?: string;
}

export interface EmpresaFila extends Marca { cursos: number; videos: number }

/** Lo que se envía al registrar o editar una empresa. */
export interface DatosEmpresa {
  nombre: string;
  nombre_corto: string;
  que_es: string;
  sitio_web: string;
  responsable: string;
  colores: string[];
  voz: string;
  cta: string;
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
  /** Tiene una edición propia (el original del PPTX no cambia). */
  editada?: boolean;
  notas_original?: string;
  pantalla?: { titulo: string | null; vinetas: string[] | null };
}

export interface VideoPlan { clave: string; titulo: string; laminas: number[]; segundos: number; frases: number }
export interface Chequeo {
  clave: "fuente" | "sin_notas" | "sin_uso" | "largos" | "normativas" | "marca";
  ok: boolean | null;
  titulo: string;
  detalle: string;
  ayuda: string;
}
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
  animacion?: { plantilla: string | null } | null;
  estilo?: string | null;
  escena?: EscenaCurso | null;
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
  fase?: FaseMotor | null;
  codigo?: string | null;
  recuperacion?: string | null;
  estado: EstadoRender;
  paso: string | null;
  progreso: number | null;
  mensaje: string | null;
  informe: InformeRender | null;
  /** Se produjo con otra marca o voz que la elegida ahora. */
  desactualizado: boolean;
  archivos: { mp4: string; vtt: string; srt: string } | null;
}

export interface CompletoRender extends Omit<VideoRender, "informe" | "archivos"> {
  informe: (Omit<InformeRender, "chequeos"> & { chequeos: Chequeo[]; capitulos: { inicio: number; titulo: string }[] }) | null;
  archivos: { mp4: string; vtt: string; srt: string; capitulos: string } | null;
}

export interface Produccion {
  voz_falta: string | null;
  voz_borrador: boolean;
  videos: Record<string, VideoRender | null>;
  completo: CompletoRender | null;
  listos: number;
  total: number;
  /** Videos que faltan o quedaron desactualizados («Título (sin producir)»). */
  pendientes: string[];
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

/** Configuración del estudio (GET /api/configuracion). */
export interface AjustesVideo {
  video: { resolucion: "1080p" | "720p"; fps: 25 | 30 | 60; calidad: "final" | "borrador"; subtitulos_quemados: boolean };
  tiempos: { entrada: number; pausa: number; salida: number };
  audio: { lufs: number; musica: string | null; musica_volumen: number; respaldo_voz?: boolean; musica_estilo?: boolean };
  completo: { tarjetas: boolean; duracion_tarjeta: number; capitulos: boolean };
}

export interface Configuracion extends AjustesVideo {
  cursos: { marca: string; voz: string; formatos: string[]; animacion: string };
  agentes: { url: string; modelo_texto: string; modelo_vision: string; activos: Record<string, boolean> };
}

export type OpcionesConfig = Record<string, { valor: string | number; texto: string }[] | { min: number; max: number }>;
export interface PistaMusica { archivo: string; licencia: string | null; fuente: string | null; energia?: string | null }

export interface RespuestaConfig {
  configuracion: Configuracion;
  opciones: OpcionesConfig;
  musica: PistaMusica[];
  por_curso: (keyof AjustesVideo)[];
}

/** Diagnóstico del equipo (GET /api/sistema). */
export interface Revision { ok: boolean; detalle: string; arreglo?: string | null }
export interface Sistema {
  ffmpeg: Revision;
  chromium: Revision;
  elevenlabs: Revision;
  voces: { id: string; nombre: string; proveedor: string; ok: boolean; detalle: string }[];
  ollama: Revision & { encendido: boolean; modelos: string[] };
  disco: Revision;
}

/** Animación (GET /api/animaciones y /api/trabajos/:id/animacion). */
export type Fase = "entrada" | "salida";
export interface PasoAnim { efecto: string; duracion: number; retardo: number; curva: string; escalonado: number }
export type ElementosAnim = Record<string, Record<Fase, PasoAnim>>;
export type AjustesAnim = Record<string, Partial<Record<Fase, Partial<PasoAnim>>>>;
export interface PlantillaAnim { id: string; nombre: string; descripcion: string; elementos: ElementosAnim; propia: boolean }
export interface AnimacionCurso {
  plantilla: string | null;
  ajustes: AjustesAnim;
  laminas: Record<string, { plantilla: string | null; ajustes: AjustesAnim }>;
}
export interface CatalogoAnim {
  plantillas: PlantillaAnim[];
  elementos: Record<string, { nombre: string; entrada: { id: string; nombre: string }[]; salida: { id: string; nombre: string }[] }>;
  curvas: { id: string; nombre: string }[];
  limites: Record<"duracion" | "retardo" | "escalonado", { min: number; max: number }>;
  continuos: string[];
}

/** Agentes (GET /api/trabajos/:id/agentes). */
export interface AgenteInfo {
  id: string;
  nombre: string;
  que: string;
  donde: "presentacion" | "guion" | "animacion" | "resultado";
  modelo: string | null;
  activo: boolean;
  con_ia: boolean;
  necesita_ia: boolean;
  acepta: boolean;
}
export interface Propuesta {
  id: string;
  agente: string;
  lamina: number | null;
  video: string | null;
  titulo: string;
  antes: unknown;
  despues: Record<string, unknown>;
  razon: string;
  estado: "pendiente" | "aceptada" | "descartada";
  hecha_con: string;
  creada: string;
}
export interface AgentesCurso {
  agentes: AgenteInfo[];
  estados: Record<string, { estado: EstadoRender; paso: string | null; progreso: number | null; mensaje: string | null;
    propuestas: number | null; con_ia: boolean | null } | null>;
  propuestas: Propuesta[];
}

/** Flujo creativo (/crear): análisis, estilos, escena, línea de tiempo y versiones. */
export interface Analisis {
  laminas: number;
  titulos: { lamina: number; titulo: string; seccion: string | null }[];
  con_notas: number;
  sin_notas: number[];
  imagenes: number[];
  tablas: number[];
  graficos: number[];
  vacias: number[];
  texto_largo: number[];
  palabras: number;
  minutos: number;
  videos: number;
  estructura: string;
  tema: string[];
  dificultad: string;
  puntos_importantes: { lamina: number; cita: string }[];
  avisos: string[];
}

export interface Estilo {
  id: string;
  nombre: string;
  icono: string;
  descripcion: string;
  animacion: string;
  camara: string;
  transicion: string;
  subtitulos_quemados: boolean;
  sfx: string | null;
  musica: string | null;
  formato: string;
  camara_nombre: string;
  transicion_nombre: string;
  musica_nombre: string | null;
}

export interface OpcionCatalogo { id: string; nombre: string }
export interface CatalogoEscena {
  camaras: OpcionCatalogo[];
  transiciones: OpcionCatalogo[];
  formatos: (OpcionCatalogo & { ancho: number; alto: number })[];
}

export interface EscenaCurso { camara?: string; transicion?: string; laminas?: Record<string, { camara?: string; transicion?: string }> }

export interface LineaDeTiempo {
  clave: string;
  titulo: string;
  resuelto: boolean;
  duracion: number;
  formato: string;
  pistas: {
    escenas: { id: string; lamina: number; titulo: string; tipo: string; inicio: number; duracion: number; camara: string;
      transicion: string; plantilla: string }[];
    voz: { escena: string; inicio: number; fin: number; texto: string }[];
    musica: { inicio: number; fin: number; archivo: string }[];
    sfx: { escena: string; id: string; nombre: string; inicio: number }[];
    subtitulos: { escena: string; inicio: number; fin: number; texto: string }[];
  };
}

export interface VersionVideo {
  version: string;
  numero: number;
  creado: string | null;
  voz: string | null;
  duracion: number | null;
  formato: string | null;
  fallas: number;
  bugs: number;
  avisos: string[];
  mp4: string;
}

/** Fases del motor mientras produce (produccion.FASES y la cola). */
export type FaseMotor = "QUEUED" | "SCRIPTING" | "SCRIPT_READY" | "GENERATING_AUDIO" | "AUDIO_READY" | "BUILDING_SCENES"
  | "SCENES_READY" | "RENDERING" | "RENDERED" | "QA_RUNNING" | "QA_PASSED" | "QA_FAILED" | "COMPLETED" | "FAILED";

export interface EventoRegistro {
  timestamp: string;
  stage: string;
  status: string;
  message: string;
  retry?: number;
  error_code?: string | null;
  severity?: string | null;
  recovery?: string | null;
  stacktrace?: string;
}
