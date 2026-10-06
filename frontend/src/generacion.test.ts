import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import EstadoGeneracion from "./components/zyvo/EstadoGeneracion.vue";
import MensajeError from "./components/zyvo/MensajeError.vue";
import PasosProgreso from "./components/zyvo/PasosProgreso.vue";
import { mensajeHumano, pasos, resumen } from "./generacion";
import type { Produccion, VideoRender } from "./tipos";

const video = (x: Partial<VideoRender>): VideoRender => ({
  estado: "produciendo", paso: null, progreso: 0.3, mensaje: null, informe: null, desactualizado: false, archivos: null, ...x,
});

describe("del motor a pasos humanos", () => {
  it("marca hechos los pasos anteriores a la fase actual", () => {
    const p = pasos(video({ fase: "BUILDING_SCENES" }));
    expect(p.map((x) => x.estado)).toEqual(["hecho", "hecho", "actual", "pendiente", "pendiente", "pendiente"]);
    expect(p[2]!.texto).toBe("Aplicando animaciones");
  });

  it("distingue «Mezclando audio» dentro de la fase de render", () => {
    expect(pasos(video({ fase: "RENDERING", paso: "Mezclando el audio" })).find((x) => x.estado === "actual")!.id).toBe("audio");
    expect(pasos(video({ fase: "RENDERING", paso: "Quemando los subtítulos" })).find((x) => x.estado === "actual")!.id).toBe("video");
  });

  it("un video listo tiene todo hecho y uno en la fila nada empezado", () => {
    expect(pasos(video({ estado: "listo", fase: "COMPLETED" })).every((x) => x.estado === "hecho")).toBe(true);
    expect(pasos(video({ estado: "en_cola", fase: "QUEUED" })).every((x) => x.estado === "pendiente")).toBe(true);
  });

  it("resume el avance de todos los videos del curso", () => {
    const p = { videos: { v01: video({ estado: "listo" }), v02: video({ progreso: 0.5 }) }, completo: null } as unknown as Produccion;
    const r = resumen(p);
    expect(r.porcentaje).toBe(75);
    expect(r.produciendo).toBe(true);
    expect(r.listo).toBe(false);
    expect(resumen(null).porcentaje).toBe(0);
  });

  it("nunca muestra un mensaje técnico", () => {
    expect(mensajeHumano("Traceback (most recent call last): ...")).toBe("Algo salió mal al crear el video.");
    expect(mensajeHumano("FFmpeg exited with code 1")).toBe("Algo salió mal al crear el video.");
    expect(mensajeHumano("Falta la clave de ElevenLabs")).toBe("Falta la clave de ElevenLabs");
  });
});

describe("componentes del flujo", () => {
  it("los pasos dicen dónde está la persona", () => {
    const w = mount(PasosProgreso, { props: { pasos: [{ id: "a", texto: "Uno" }, { id: "b", texto: "Dos" }, { id: "c", texto: "Tres" }], actual: "b", hasta: 1 } });
    const botones = w.findAll("button");
    expect(botones[1]!.attributes("aria-current")).toBe("step");
    expect(botones[2]!.attributes("disabled")).toBeDefined();
  });

  it("la generación muestra el porcentaje y el paso actual", () => {
    const w = mount(EstadoGeneracion, { props: { video: video({ fase: "GENERATING_AUDIO" }), porcentaje: 42 } });
    expect(w.text()).toContain("42 %");
    expect(w.text()).toContain("Generando narración");
    expect(w.find('[role="progressbar"]').attributes("aria-valuenow")).toBe("42");
  });

  it("un error sugiere qué hacer, sin detalles técnicos", () => {
    const w = mount(MensajeError, { props: { mensaje: "subprocess failed: ffmpeg", recuperacion: "ELEGIR_OTRA_VOZ" } });
    expect(w.text()).not.toContain("subprocess");
    expect(w.text()).toContain("Elegir otra voz");
    expect(w.text()).not.toContain("Modo diagnóstico");  // solo aparece si hay a quién pedirle el registro
  });
});
