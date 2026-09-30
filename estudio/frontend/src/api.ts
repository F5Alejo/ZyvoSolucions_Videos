// Cliente de la API. Los errores llegan como Error con el mensaje que da el servidor.

async function pedir<T>(metodo: string, url: string, cuerpo?: unknown): Promise<T> {
  let r: Response;
  try {
    r = await fetch(url, {
      method: metodo,
      headers: cuerpo === undefined ? {} : { "Content-Type": "application/json" },
      body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
    });
  } catch {
    throw new Error("No hay conexión con el servidor. ¿Está encendido?");
  }
  if (r.status === 204) return undefined as T;
  const datos = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(mensajeDeError(datos, r.status));
  return datos as T;
}

function mensajeDeError(datos: { detail?: unknown }, estado: number): string {
  const d = datos.detail;
  if (typeof d === "string") return d;
  if (Array.isArray(d)) return "Faltan datos o no son válidos.";
  return estado === 404 ? "No encontramos lo que buscas." : "Algo salió mal en el servidor.";
}

export const api = {
  get: <T>(url: string) => pedir<T>("GET", url),
  post: <T>(url: string, cuerpo?: unknown) => pedir<T>("POST", url, cuerpo ?? {}),
  patch: <T>(url: string, cuerpo: unknown) => pedir<T>("PATCH", url, cuerpo),
  delete: (url: string) => pedir<void>("DELETE", url),
};

/** Sube un archivo mostrando el progreso (fetch todavía no informa el avance de la subida). */
export function subir<T>(url: string, datos: FormData, alAvanzar: (fraccion: number) => void): Promise<T> {
  return new Promise((resolver, rechazar) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.upload.onprogress = (e) => e.lengthComputable && alAvanzar(e.loaded / e.total);
    xhr.onerror = () => rechazar(new Error("No hay conexión con el servidor. ¿Está encendido?"));
    xhr.onload = () => {
      let cuerpo: { detail?: unknown } = {};
      try { cuerpo = JSON.parse(xhr.responseText); } catch { /* respuesta vacía */ }
      if (xhr.status >= 200 && xhr.status < 300) resolver(cuerpo as T);
      else rechazar(new Error(mensajeDeError(cuerpo, xhr.status)));
    };
    xhr.send(datos);
  });
}
