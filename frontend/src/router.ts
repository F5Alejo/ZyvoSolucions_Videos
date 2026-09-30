import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: (a, b, guardada) => guardada ?? (a.path === b.path ? undefined : { top: 0 }),
  routes: [
    { path: "/", name: "inicio", component: () => import("./views/InicioView.vue"), meta: { titulo: "Inicio" } },
    { path: "/cursos", name: "cursos", component: () => import("./views/CursosView.vue"), meta: { titulo: "Cursos" } },
    { path: "/cursos/nuevo", name: "crear", component: () => import("./views/CrearCursoView.vue"), meta: { titulo: "Crear curso" } },
    { path: "/cursos/:id", name: "curso", component: () => import("./views/CursoView.vue"), props: true, meta: { titulo: "Curso" } },
    { path: "/videos", name: "videos", component: () => import("./views/VideosView.vue"), meta: { titulo: "Videos" } },
    { path: "/videos/:id", name: "video", component: () => import("./views/VideoView.vue"), props: true, meta: { titulo: "Video" } },
    { path: "/marcas/:id", name: "marca", component: () => import("./views/MarcaView.vue"), props: true, meta: { titulo: "Marca" } },
    { path: "/pendientes", name: "pendientes", component: () => import("./views/PendientesView.vue"), meta: { titulo: "Pendientes" } },
    { path: "/configuracion", name: "configuracion", component: () => import("./views/ConfiguracionView.vue"), meta: { titulo: "Configuración" } },
    { path: "/casos/:id", name: "caso", component: () => import("./views/CasoView.vue"), props: true, meta: { titulo: "Pieza de marketing" } },
    { path: "/:resto(.*)*", name: "no-encontrado", component: () => import("./views/NoEncontradoView.vue"), meta: { titulo: "No encontrado" } },
  ],
});

router.afterEach((a) => {
  document.title = `${(a.meta.titulo as string) ?? "Estudio"} · Estudio de video RiskMann`;
});

export default router;
