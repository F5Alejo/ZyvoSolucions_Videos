import { ref } from "vue";

export type Tema = "oscuro" | "claro";
const CLAVE = "estudio.tema";

/** El tema de la página. Oscuro por defecto: es el del manual de RiskMann. index.html lo aplica antes de pintar. */
export const tema = ref<Tema>((document.documentElement.dataset.tema as Tema) || "oscuro");

export function cambiarTema(nuevo: Tema) {
  tema.value = nuevo;
  document.documentElement.dataset.tema = nuevo;
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content", nuevo === "oscuro" ? "#020202" : "#26367D");
  try { localStorage.setItem(CLAVE, nuevo); } catch { /* sin almacenamiento: vale para esta visita */ }
}
