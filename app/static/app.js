// Mejoras de uso. Todo funciona sin este archivo: aquí solo se hace más cómodo.
(() => {
  "use strict";
  const $ = (sel, raiz = document) => raiz.querySelector(sel);
  const $$ = (sel, raiz = document) => [...raiz.querySelectorAll(sel)];

  // ── Avisos flotantes ──────────────────────────────────────────────
  const zonaAvisos = $("#avisos");
  function avisar(texto, tipo = "ok") {
    if (!zonaAvisos) return;
    const div = document.createElement("div");
    div.className = `aviso-flotante ${tipo}`;
    div.setAttribute("role", tipo === "error" ? "alert" : "status");
    div.textContent = (tipo === "ok" ? "✓ " : "⚠ ") + texto;
    zonaAvisos.append(div);
    setTimeout(() => div.classList.add("saliendo"), 3500);
    setTimeout(() => div.remove(), 4000);
  }
  $$(".aviso-flotante").forEach((a) => {
    setTimeout(() => a.classList.add("saliendo"), 4000);
    setTimeout(() => a.remove(), 4500);
  });
  // Quita ?ok= de la dirección para que recargar no repita el aviso.
  if (location.search.includes("ok=")) {
    const url = new URL(location.href);
    url.searchParams.delete("ok");
    history.replaceState(null, "", url.pathname + url.search + url.hash);
  }

  // ── Confirmar antes de algo que no se deshace ─────────────────────
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-confirmar]");
    if (b && !confirm(b.dataset.confirmar)) ev.preventDefault();
  });
  $$("form[data-confirmar]").forEach((f) =>
    f.addEventListener("submit", (ev) => { if (!confirm(f.dataset.confirmar)) ev.preventDefault(); }));

  // ── «Cargando…» al enviar algo que tarda ──────────────────────────
  $$("form[data-cargando]").forEach((f) =>
    f.addEventListener("submit", (ev) => {
      if (ev.defaultPrevented || !f.checkValidity()) return;
      $$("button", f).forEach((b) => (b.disabled = true));
      const capa = document.createElement("div");
      capa.className = "cargando";
      capa.setAttribute("role", "status");
      capa.innerHTML = '<span class="girando" aria-hidden="true"></span><span></span>';
      capa.lastChild.textContent = f.dataset.cargando;
      document.body.append(capa);
    }));

  // ── Zona para soltar el PPTX ──────────────────────────────────────
  const zona = $("#zona");
  if (zona) {
    const input = $(".zona-input", zona);
    const rotulo = $(".zona-archivo", zona);
    const mb = (n) => (n / 1048576).toFixed(1).replace(".", ",") + " MB";
    const mostrar = () => {
      const f = input.files[0];
      zona.classList.toggle("con-archivo", !!f);
      zona.classList.remove("zona-error");
      if (!f) { rotulo.hidden = true; return; }
      rotulo.hidden = false;
      if (!f.name.toLowerCase().endsWith(".pptx")) {
        zona.classList.add("zona-error");
        rotulo.textContent = `«${f.name}» no es un PPTX. Guárdalo desde PowerPoint como .pptx.`;
        input.value = "";
        return;
      }
      if (f.size > 200 * 1048576) {
        zona.classList.add("zona-error");
        rotulo.textContent = `«${f.name}» pesa ${mb(f.size)}: el máximo es 200 MB.`;
        input.value = "";
        return;
      }
      rotulo.textContent = `✓ ${f.name} · ${mb(f.size)}`;
    };
    input.addEventListener("change", mostrar);
    ["dragenter", "dragover"].forEach((e) => zona.addEventListener(e, (ev) => { ev.preventDefault(); zona.classList.add("encima"); }));
    ["dragleave", "drop"].forEach((e) => zona.addEventListener(e, () => zona.classList.remove("encima")));
    zona.addEventListener("drop", (ev) => {
      ev.preventDefault();
      if (ev.dataTransfer.files.length) { input.files = ev.dataTransfer.files; mostrar(); }
    });
  }

  // ── Guardado automático de marca, voz y formatos ─────────────────
  $$("form[data-autoguardar]").forEach((f) => {
    const estado = $("[data-estado-guardado]", f);
    let ultimoBueno = new FormData(f);
    const restaurar = (datos) => $$("input", f).forEach((i) => {
      i.checked = datos.getAll(i.name).includes(i.value);
    });
    f.addEventListener("change", async (ev) => {
      if (!ev.target.matches("input")) return;
      const datos = new FormData(f);
      estado.textContent = "Guardando…";
      try {
        const r = await fetch(f.action, { method: "POST", body: datos, headers: { Accept: "application/json" } });
        const j = await r.json();
        if (!j.ok) throw new Error(j.mensaje);
        ultimoBueno = datos;
        estado.textContent = "✓ Guardado";
        actualizarResumen(f);
      } catch (e) {
        restaurar(ultimoBueno);
        estado.textContent = "";
        avisar(e.message || "No se pudo guardar. Revisa la conexión.", "error");
      }
    });
  });
  function actualizarResumen(f) {
    const marca = $("input[name=marca]:checked", f);
    const voz = $("input[name=voz]:checked", f);
    const resumen = $("[data-resumen-ajustes]");
    if (resumen && marca && voz) resumen.textContent = `${marca.dataset.nombre} · ${voz.dataset.nombre}`;
    const plan = $("[data-videos-plan]");
    if (plan && marca) { plan.style.setProperty("--c1", marca.dataset.c1); plan.style.setProperty("--c2", marca.dataset.c2); }
  }

  // Una sola muestra de voz sonando a la vez.
  document.addEventListener("play", (ev) => {
    $$("audio, video").forEach((m) => { if (m !== ev.target) m.pause(); });
  }, true);

  // ── Filtros que se aplican solos ──────────────────────────────────
  $$("form[data-autoenviar] select").forEach((s) => s.addEventListener("change", () => s.form.submit()));

  // ── Buscar dentro de una tabla ────────────────────────────────────
  const buscador = $("[data-filtrar-tabla]");
  const tabla = $("table[data-filtrable]");
  if (buscador && tabla) {
    const conteo = $("[data-conteo-tabla]");
    const filas = $$("tbody tr[data-href]", tabla);
    buscador.addEventListener("input", () => {
      const q = normalizar(buscador.value);
      let visibles = 0;
      filas.forEach((tr) => {
        const ok = !q || normalizar(tr.textContent).includes(q);
        tr.hidden = !ok;
        visibles += ok;
      });
      conteo.textContent = q ? (visibles ? `${visibles} de ${filas.length} videos` : "Ningún video coincide con la búsqueda.") : "";
    });
  }
  function normalizar(t) { return t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim(); }

  // Filas de tabla que se abren con un clic en cualquier parte.
  document.addEventListener("click", (ev) => {
    const tr = ev.target.closest("tr[data-href]");
    if (tr && !ev.target.closest("a, button, input")) location.href = tr.dataset.href;
  });

  // ── Recordar el nombre de quien decide ────────────────────────────
  $$("[data-recordar]").forEach((i) => {
    const clave = "estudio." + i.dataset.recordar;
    try { if (!i.value) i.value = localStorage.getItem(clave) || ""; } catch (_) {}
    i.form.addEventListener("submit", () => { try { localStorage.setItem(clave, i.value.trim()); } catch (_) {} });
  });

  // ── Barra de pasos: marca el paso que se está viendo ──────────────
  const barra = $(".pasos-barra");
  if (barra && "IntersectionObserver" in window) {
    const enlaces = new Map($$("a[data-paso]", barra).map((a) => [a.dataset.paso, a]));
    const obs = new IntersectionObserver((entradas) => {
      entradas.forEach((e) => {
        if (!e.isIntersecting) return;
        enlaces.forEach((a) => a.removeAttribute("aria-current"));
        enlaces.get(e.target.id)?.setAttribute("aria-current", "step");
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    $$("section.paso").forEach((s) => obs.observe(s));
  }

  // ── Herramientas del guion: buscar, solo lo marcado, abrir todo ───
  const herramientas = $("[data-guion-herramientas]");
  const guion = $("[data-guion]");
  if (herramientas && guion) {
    herramientas.hidden = false;
    const buscar = $("[data-guion-buscar]", herramientas);
    const soloMarcas = $("[data-guion-solo-marcas]", herramientas);
    const conteo = $("[data-guion-conteo]", herramientas);
    const videos = $$("details.video-guion", guion);
    const filtrar = () => {
      const q = normalizar(buscar.value);
      const marcas = soloMarcas.checked;
      let laminas = 0;
      videos.forEach((d) => {
        let alguna = false;
        $$(".lamina", d).forEach((l) => {
          const ok = (!q || normalizar(l.textContent).includes(q)) && (!marcas || $("mark", l));
          l.hidden = !ok;
          if (ok) { alguna = true; laminas++; }
        });
        const filtrando = q || marcas;
        d.hidden = filtrando && !alguna;
        if (filtrando) d.open = alguna;
      });
      conteo.textContent = q || marcas ? `${laminas} láminas` : "";
    };
    buscar.addEventListener("input", filtrar);
    soloMarcas.addEventListener("change", filtrar);
    $("[data-guion-abrir]", herramientas).addEventListener("click", () => videos.forEach((d) => (d.open = !d.hidden)));
    $("[data-guion-cerrar]", herramientas).addEventListener("click", () => videos.forEach((d) => (d.open = false)));
  }

  // ── Menú de marcas: se cierra al hacer clic fuera o con Escape ────
  const menu = $("details.menu");
  if (menu) {
    document.addEventListener("click", (ev) => { if (!menu.contains(ev.target)) menu.open = false; });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") menu.open = false; });
  }
})();
