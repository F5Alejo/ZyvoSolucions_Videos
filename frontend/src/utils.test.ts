import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import TextoResaltado from "./components/TextoResaltado.vue";
import { cuenta, diferencias, fijarAjuste, mmss, normalizar, resaltar, resolverAnimacion } from "./utils";
import type { PlantillaAnim } from "./tipos";

describe("utilidades", () => {
  it("formatea minutos y segundos", () => {
    expect(mmss(125)).toBe("2:05");
    expect(mmss(2004.4)).toBe("33:24");
    expect(mmss(0)).toBe("0:00");
  });

  it("pone el plural solo cuando hace falta", () => {
    expect(cuenta(1, "video")).toBe("1 video");
    expect(cuenta(15, "video")).toBe("15 videos");
    expect(cuenta(2, "lámina muda", "láminas mudas")).toBe("2 láminas mudas");
  });

  it("busca sin importar tildes ni mayúsculas", () => {
    expect(normalizar("  Campaña del EN VIVO ")).toBe("campana del en vivo");
  });
});

describe("resaltar cifras y normas", () => {
  it("marca cada cita y deja el resto igual", () => {
    const trozos = resaltar("Lo exige la Ley 1503 de 2011: el 30 % ocurre en misión.", ["Ley 1503 de 2011", "30 %"]);
    expect(trozos.map((t) => t.texto).join("")).toBe("Lo exige la Ley 1503 de 2011: el 30 % ocurre en misión.");
    expect(trozos.filter((t) => t.marcado).map((t) => t.texto)).toEqual(["Ley 1503 de 2011", "30 %"]);
  });

  it("prefiere la cita más larga cuando se solapan", () => {
    const trozos = resaltar("Ley 1503 de 2011", ["Ley 1503", "Ley 1503 de 2011"]);
    expect(trozos).toEqual([{ texto: "Ley 1503 de 2011", marcado: true }]);
  });

  it("no rompe con caracteres especiales de expresiones regulares", () => {
    expect(resaltar("Cuesta $ 500.000 (aprox.)", ["$ 500.000"]).find((t) => t.marcado)?.texto).toBe("$ 500.000");
  });

  it("nunca interpreta el texto del cliente como HTML", () => {
    const w = mount(TextoResaltado, { props: { texto: "<img src=x onerror=alert(1)> el 30 %", citas: ["30 %"] } });
    expect(w.find("img").exists()).toBe(false);
    expect(w.text()).toContain("<img src=x onerror=alert(1)>");
    expect(w.find("mark").text()).toBe("30 %");
  });
});

describe("diferencias", () => {
  it("devuelve solo lo que cambia, por grupo", () => {
    const base = { video: { fps: 30, calidad: "final" }, audio: { lufs: -14, musica: null } };
    const nuevo = { video: { fps: 60, calidad: "final" }, audio: { lufs: -14, musica: null } };
    expect(diferencias(base, nuevo)).toEqual({ video: { fps: 60 } });
    expect(diferencias(base, structuredClone(base))).toEqual({});
  });
});

describe("animación por capas", () => {
  const paso = (efecto: string) => ({ efecto, duracion: 0.5, retardo: 0, curva: "suave", escalonado: 0 });
  const plantillas: PlantillaAnim[] = [
    { id: "sobria", nombre: "Sobria", descripcion: "", propia: false, elementos: { titulo: { entrada: paso("aparecer"), salida: paso("aparecer") } } },
    { id: "cinetica", nombre: "Cinética", descripcion: "", propia: false, elementos: { titulo: { entrada: paso("rebote"), salida: paso("desenfoque") } } },
  ];
  const vacia = { plantilla: null, ajustes: {}, laminas: {} };

  it("usa la plantilla por defecto, luego la del curso y luego la de la lámina", () => {
    expect(resolverAnimacion(plantillas, vacia, "sobria", null).plantilla).toBe("sobria");
    const a = { ...vacia, plantilla: "cinetica", laminas: { "3": { plantilla: "sobria", ajustes: {} } } };
    expect(resolverAnimacion(plantillas, a, "sobria", 1).plantilla).toBe("cinetica");
    expect(resolverAnimacion(plantillas, a, "sobria", 3).plantilla).toBe("sobria");
  });

  it("un ajuste va a su capa y no toca las demás", () => {
    let a = fijarAjuste(vacia, null, "titulo", "entrada", "duracion", 1.2);
    a = fijarAjuste(a, 2, "titulo", "salida", "efecto", "subir");
    expect(resolverAnimacion(plantillas, a, "sobria", 1).elementos.titulo!.entrada.duracion).toBe(1.2);
    expect(resolverAnimacion(plantillas, a, "sobria", 1).elementos.titulo!.salida.efecto).toBe("aparecer");
    expect(resolverAnimacion(plantillas, a, "sobria", 2).elementos.titulo!.salida.efecto).toBe("subir");
    expect(vacia.ajustes).toEqual({}); // no muta la original
  });
});
