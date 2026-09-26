// ════════════════════════════════════════════════════════════════════════════
//  «ESTUDIO VIRTUAL» · En Vivo PESV — Informe de Autogestión (yezidricaurte.com)
//  El único archivo que hay que tocar para cambiar textos, colores o tiempos.
//
//     ?v=v1   Faltan pocos días   (acompaña el correo de reserva)
//     ?v=v2   Es mañana           (recordatorio de 24 h)
//     ?v=v3   Es hoy              (día de la transmisión)
//     &fondo=escudo | plexus      (estudio 3D sólido · red geométrica sutil)
//
//  Marcado:  *texto* → Bold   ·   _texto_ → Bold dorado (un acento por frase)
// ════════════════════════════════════════════════════════════════════════════

// Paleta: verde profundo de Yezid Ricaurte para el estudio, dorado y crema de
// yezidricaurte.com para acentos. PROHIBIDO EL ROJO (y el coral de la web).
export const COLORES = {
  fondoCentro: "#1A3B3B",  // estudio: centro del degradado radial
  fondoBorde: "#0F2A2A",   // estudio: bordes
  dorado: "#d2b96a",       // yezidricaurte.com
  palido: "#f1ecb0",       // destellos
  verde: "#45a035",        // SOLO si se elige boton: "verde" (los prompts lo piden; el cliente
                           // aclaró que el video es de yezidricaurte.com, no de FEGIR)
};

// «cristal-dorado»: cristal transparente con borde y resplandor dorado (por defecto)
// «verde»         : botón sólido #45a035
export const BOTON = "cristal-dorado";

// Sincronización con la voz. Con la locución real de ElevenLabs estos segundos
// se reemplazan por los de /v1/text-to-speech/{voz}/with-timestamps.
export const videoTimestamps = {
  v1: { hook: 0.5, valor: 4.0, cta: 8.5 },
  v2: { hook: 0.4, valor: 3.4, cta: 8.0 },
  v3: { hook: 0.4, valor: 3.0, cta: 7.6 },
};

// Guiones para ElevenLabs (Carlos · eleven_multilingual_v2). Ingeniería de
// puntuación con lo YA MEDIDO en este repo (ENTREGABLES-VIDEO/prueba-puntuacion):
//   · «…» da 0.64 s de pausa real; el guion largo «—» da 0.57 s → pausas con «…»
//   · las comillas no son un mecanismo del modelo (puede leerlas como cita) → no
//   · P-E-S-V deletreado: la sigla pasa de 0.49 a 0.95 s y se entiende
//   · «vivo» nunca cierra frase: el modelo se come la «o» y suena «vip»
export const GUIONES = {
  v1: "Faltan pocos días… para dominar el P-E-S-V. Blinda tu empresa… en un solo día. ¡Regístrate ahora!",
  v2: "La oportunidad es mañana… A las diez de la mañana, hora Colombia. ¡Entra al grupo de WhatsApp!",
  v3: "Llegó el día… Estamos en vivo, ¡únete ahora mismo!",
};

export const VIDEOS = {
  v1: {
    nombre: "Faltan pocos días",
    archivo: "01-Faltan-pocos-dias",
    titular: "Faltan pocos días…",
    subtitulo: "Aprende a *dominar el reporte PESV* y *blinda tu empresa* en _un solo día._",
    info: [["Sábado", "03 de octubre"], ["Hora", "10:00 a. m. (Col)"]],
    boton: "Crea tu cuenta",
    sub: "app.riskmann.com/registrarse",
  },
  v2: {
    nombre: "Es mañana",
    archivo: "02-Es-manana",
    titular: "La oportunidad es mañana",
    subtitulo: "Los enlaces llegan por el *grupo oficial de WhatsApp*. Ten lista tu cuenta en _app.riskmann.com._",
    info: [["Mañana", "03 de octubre"], ["Hora", "10:00 a. m. (Col)"]],
    boton: "Entrar al grupo de WhatsApp",
    sub: "Grupo oficial del En Vivo",
  },
  v3: {
    nombre: "Es hoy",
    archivo: "03-Es-hoy",
    titular: "Llegó el día",
    subtitulo: "Transmisión por *Instagram, TikTok y YouTube*. Los enlaces, en el _grupo oficial._",
    info: [["Hoy", "10:00 a. m."], ["Estado", "En vivo"]],
    enVivo: true,
    boton: "Ir al grupo de WhatsApp",
    sub: "Ten abierta tu cuenta en app.riskmann.com",
  },
};

export const COMUN = {
  evento: "En Vivo PESV",
  subEvento: "Informe de Autogestión",
  persona: "Dr. Yezid Ricaurte",
  rol: "Abogado · Consultor · Conferencista",
  web: "yezidricaurte.com",
  foto: "yezid-photo.png",   // recorte sin fondo, en la raíz del proyecto
};
