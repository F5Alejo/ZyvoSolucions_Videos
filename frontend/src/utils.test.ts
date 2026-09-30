import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import TextoResaltado from "./components/TextoResaltado.vue";
import { contraste, cuenta, mmss, normalizar, resaltar, tintaLegible } from "./utils";

describe("color legible", () => {
  it("mide el contraste como WCAG", () => {
    expect(contraste("#000000", "#FFFFFF")).toBeCloseTo(21, 0);
    expect(contraste("#073D7A", "#F3F3F3")).toBeCloseTo(9.67, 1);   // medido para la app
  });

  it("descarta el color de marca que no se lee y cae a blanco o negro", () => {
    // Dr. Yezid: oliva #80804A sobre verde #336666 da 1,75:1 → ilegible.
    expect(contraste("#80804A", "#336666")).toBeLessThan(2);
    expect(tintaLegible("#336666", ["#80804A"])).toBe("#FFFFFF");
    // RiskMann: dorado #C8951A sobre #020202 sí se lee.
    expect(tintaLegible("#020202", ["#C8951A"])).toBe("#C8951A");
    // Fondo claro: texto oscuro.
    expect(tintaLegible("#F1ECB0")).toBe("#111111");
  });
});

describe("utilidades", () => {
  it("formatea minutos y segundos", () => {
    expect(mmss(125)).toBe("2:05");
    expect(mmss(2004.4)).toBe("33:24");
    expect(mmss(0)).toBe("0:00");
  });

  it("pone el plural solo cuando hace falta", () => {
    expect(cuenta(1, "video")).toBe("1 video");
    expect(cuenta(15, "video")).toBe("15 videos");
    expect(cuenta(2, "diapositiva sin voz", "diapositivas sin voz")).toBe("2 diapositivas sin voz");
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
