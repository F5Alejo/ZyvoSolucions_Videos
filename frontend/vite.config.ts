/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// En desarrollo, la API y los archivos los sirve FastAPI (puerto 8765).
const API = "http://localhost:8765";

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: { port: 5173, proxy: { "/api": API, "/media": API } },
  test: { environment: "jsdom" },
});
