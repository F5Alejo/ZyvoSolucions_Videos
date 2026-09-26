// V2: fondo sólido, el color de yezidricaurte.com (--color-brand-black-blue: #001217).
// Sin partículas ni líquido: el movimiento lo ponen las imágenes de cada bloque (ads.js).
// Se conserva la misma interfaz (bgState, render) para no tocar el resto del motor.
export const BG_MODES = ["solido"];
export const bgState = { energia: 0, pulso: 0, coral: 0, warp: 0, zoom: 1 };

export function createBackground(canvas) {
  canvas.style.display = "none";
  return { render() {} };
}
