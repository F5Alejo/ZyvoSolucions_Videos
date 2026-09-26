// ════════════════════════════════════════════════════════════════════════════
//  CONFIGURACIÓN DE LA CAMPAÑA — el único archivo que hay que tocar para
//  cambiar textos. Una misma composición sirve para las tres etapas:
//     ?v=pocos    «Faltan pocos días…»   (acompaña el correo de reserva)
//     ?v=manana   «Es mañana»            (recordatorio de 24 h)
//     ?v=hoy      «Es hoy»               (día de la transmisión)
//
//  Marcado de texto:  *palabra*  → Bold (palabra clave)   ·  resto → Regular
//                     _palabra_  → Bold en amarillo pálido (un solo acento por frase)
//
//  Fuentes de cada dato: los tres correos de notificaciones@yezidricaurte.com
//  (Documentos_contexto/correos-en-vivo-pesv/) y el brief del cliente para la
//  frase de valor. Nada más entra en pantalla.
// ════════════════════════════════════════════════════════════════════════════

// Colores: yezidricaurte.com + manual de marca Yezid Ricaurte. Es un video de la
// página del Dr. Yezid, no de FEGIR. PROHIBIDO EL ROJO (y el coral #f06e49 de la web).
export const COLORES = {
  fondo: "#001f26",       // petróleo de yezidricaurte.com y de los correos
  verdeYezid: "#336666",  // verde profundo del manual: botón principal («avanzar»)
  dorado: "#d2b96a",      // dorado de yezidricaurte.com: filetes y borde del botón
  palido: "#f1ecb0",      // acentos, destellos, estados hover
};

// Tiempos por defecto (s). Con la locución de ElevenLabs se reemplazan por los
// de /v1/text-to-speech/{voz}/with-timestamps: cada golpe visual cuelga de aquí.
const TIEMPOS = { foto: 0.15, titular: 0.45, bajada: 1.9, fecha: 4.3, pasos: 5.3, cta: 8.0, fin: 12.0 };

export const CAMPANA = {
  pocos: {
    nombre: "Faltan pocos días",
    archivo: "01-Faltan-pocos-dias",
    titular: "Faltan _pocos días…_",
    bajada: "Aprende a *dominar el reporte PESV* y *blinda tu empresa* en _un solo día._",
    fecha: { dia: "Sábado 03 de octubre", hora: "10:00 a. m.", zona: "Hora Colombia" },
    pasos: ["Únete al *grupo oficial de WhatsApp*", "Crea tu cuenta en *app.riskmann.com*"],
    boton: "Crea tu cuenta",
    sub: "app.riskmann.com/registrarse",
    tiempos: { ...TIEMPOS },
  },
  manana: {
    nombre: "Es mañana",
    archivo: "02-Es-manana",
    titular: "Es _mañana._",
    bajada: "Aprende a *dominar el reporte PESV* y *blinda tu empresa* en _un solo día._",
    fecha: { dia: "Mañana · sábado 03 de octubre", hora: "10:00 a. m.", zona: "Hora Colombia" },
    pasos: ["Los enlaces llegan por el *grupo oficial de WhatsApp*", "Ten lista tu cuenta en *app.riskmann.com*"],
    boton: "Entrar al grupo de WhatsApp",
    sub: "Mañana · 10:00 a. m. (Hora Colombia)",
    tiempos: { ...TIEMPOS },
  },
  hoy: {
    nombre: "Es hoy",
    archivo: "03-Es-hoy",
    titular: "Es _hoy._",
    bajada: "Hoy aprendes a *dominar el reporte PESV* y a *blindar tu empresa* en _un solo día._",
    fecha: { dia: "Hoy · sábado 03 de octubre", hora: "10:00 a. m.", zona: "Hora Colombia" },
    pasos: ["Transmisión por *Instagram, TikTok y YouTube*", "Ten abierta tu cuenta en *app.riskmann.com*"],
    boton: "Ir al grupo de WhatsApp",
    sub: "Los enlaces, en el grupo oficial",
    tiempos: { ...TIEMPOS },
  },
};

// Texto común a las tres etapas
export const COMUN = {
  evento: "En Vivo PESV",
  subEvento: "Informe de Autogestión",
  persona: "Dr. Yezid Ricaurte",
  rol: "Abogado · Consultor · Conferencista",
  web: "yezidricaurte.com",
};
