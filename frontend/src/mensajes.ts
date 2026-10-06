// Los textos de Zyvo que ve la persona, en un solo lugar para poder cambiarlos sin tocar las pantallas.
// Regla: lenguaje humano, nada técnico (ni «render», ni «TTS», ni códigos). Pocos emojis.

export const MENSAJES = {
  subir: {
    titulo: "Crea un video desde tu PPTX",
    zona: "Arrastra tu PPTX aquí",
    o: "o selecciona un archivo",
    limite: "Hasta 200 MB",
    cargada: "✨ ¡Presentación cargada!",
    noEsPptx: (nombre: string) => `«${nombre}» no es un PPTX. Ábrelo en PowerPoint y guárdalo como .pptx.`,
    muyGrande: (nombre: string, tam: string) => `«${nombre}» pesa ${tam}: el máximo es 200 MB.`,
  },
  analizar: {
    titulo: "Analizando tu presentación…",
    pasos: ["Leyendo diapositivas", "Detectando contenido", "Identificando imágenes", "Preparando estructura"],
    listo: "🔍 Ya entendimos tu presentación.",
  },
  estilo: { titulo: "¿Cómo quieres que se vea tu video?", ayuda: "Puedes cambiarlo después, escena por escena." },
  voz: {
    titulo: "Elige cómo quieres que suene tu video",
    escuchar: "Escuchar",
    noDisponible: "Necesita configuración",
    borrador: "Solo para pruebas internas",
  },
  opciones: { titulo: "Últimos detalles", avanzado: "Configuración avanzada" },
  generar: {
    boton: "✨ Crear mi video",
    enCurso: "🎬 Estamos dando vida a tus diapositivas…",
    enCola: "Tu video está en la fila. Empieza en cuanto termine el anterior.",
    problema: "⚠️ Encontramos un problema y estamos intentando solucionarlo.",
    fallo: "No pudimos terminar tu video.",
  },
  listo: { titulo: "🎉 ¡Tu video está listo!", varios: (n: number) => `${n} videos listos para ver y descargar.` },
  editor: { titulo: "Editar escena por escena", ayuda: "Cambia lo que quieras y regenera solo esa escena." },
} as const;

/** Formatos en lenguaje humano (el usuario no tiene por qué saber qué es 16:9). */
export const FORMATOS_HUMANOS: Record<string, { titulo: string; uso: string }> = {
  "16:9": { titulo: "Presentación", uso: "YouTube, computador y proyector" },
  "9:16": { titulo: "Vertical", uso: "TikTok, Reels y Shorts" },
  "1:1": { titulo: "Cuadrado", uso: "Publicaciones en redes" },
  "4:5": { titulo: "Instagram", uso: "Feed de Instagram" },
};

/** Qué hacer ante cada recuperación que sugiere el motor (motor/errores.py). */
export const RECUPERACIONES: Record<string, { texto: string; accion?: "voz" | "reintentar" | "curso" | "diagnostico" }> = {
  ELEGIR_OTRA_VOZ: { texto: "Elige otra voz y vuelve a crear el video.", accion: "voz" },
  REINTENTAR: { texto: "Suele ser algo pasajero. Inténtalo de nuevo.", accion: "reintentar" },
  REVISAR_CURSO: { texto: "Revisa el contenido de la presentación.", accion: "curso" },
  REVISAR_ARCHIVO: { texto: "Prueba con otro archivo o guárdalo de nuevo desde PowerPoint." },
  DIAGNOSTICO: { texto: "Si se repite, abre el modo diagnóstico y comparte el detalle.", accion: "diagnostico" },
};
