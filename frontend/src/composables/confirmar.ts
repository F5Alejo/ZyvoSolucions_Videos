import { reactive } from "vue";

interface Pregunta {
  titulo: string;
  texto?: string;
  aceptar?: string;
  peligro?: boolean;
}

export const dialogo = reactive({
  abierto: false,
  titulo: "",
  texto: "",
  aceptar: "Aceptar",
  peligro: false,
  responder: (_: boolean) => {},
});

/** Pregunta antes de algo que no se deshace. Devuelve true si la persona acepta. */
export function confirmar(p: Pregunta): Promise<boolean> {
  return new Promise((resolver) => {
    Object.assign(dialogo, {
      abierto: true,
      titulo: p.titulo,
      texto: p.texto ?? "",
      aceptar: p.aceptar ?? "Aceptar",
      peligro: p.peligro ?? false,
      responder: (si: boolean) => {
        dialogo.abierto = false;
        resolver(si);
      },
    });
  });
}
