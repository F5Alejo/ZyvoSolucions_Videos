// Asegurar que el objeto global para HyperFrames exista
window.__timelines = window.__timelines || {};

// 1. Inicializar la visibilidad por defecto de las escenas
gsap.set("#scene-intro", { autoAlpha: 1 });
gsap.set("#scene-modules", { autoAlpha: 0 });
gsap.set("#scene-cta", { autoAlpha: 0 });

// 2. Crear la línea de tiempo principal (pausada por defecto para HyperFrames)
const tl = gsap.timeline({ paused: true });

// 3. Registrar la línea de tiempo con la clave de composición que coincide con 'data-composition-id'
window.__timelines["video-presentacion"] = tl;

  // --- ANIMACIONES ESCENA 1: INTRODUCCIÓN (0s - 3s) ---
  tl.fromTo("#scene-intro .logo-wrapper", 
    { scale: 0.8, opacity: 0 }, 
    { scale: 1, opacity: 1, duration: 1.2, ease: "back.out(1.5)" }, 
    0.2
  );
  
  tl.fromTo("#scene-intro .intro-title", 
    { y: 40, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 1.0, ease: "power3.out" }, 
    0.6
  );

  tl.fromTo("#scene-intro .intro-subtitle", 
    { y: 30, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 1.0, ease: "power3.out" }, 
    0.8
  );

  // Transición de Escena 1 a Escena 2 (Ocultar Escena 1)
  tl.to("#scene-intro", { autoAlpha: 0, duration: 0.5 }, 2.5);


  // --- ANIMACIONES ESCENA 2: MÓDULOS DE RIESGO (3s - 7.5s) ---
  // Mostrar contenedor de la escena 2
  tl.to("#scene-modules", { autoAlpha: 1, duration: 0.5 }, 3.0);

  // Animación del encabezado de módulos
  tl.fromTo("#scene-modules .scene-header h2", 
    { y: -30, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 0.8, ease: "power2.out" }, 
    3.2
  );
  
  tl.fromTo("#scene-modules .header-line", 
    { scaleX: 0 }, 
    { scaleX: 1, duration: 0.6, ease: "power2.out" }, 
    3.5
  );

  // Animación secuencial (stagger) de las tarjetas de módulos
  tl.fromTo("#scene-modules .module-card", 
    { y: 60, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: "power3.out" }, 
    3.6
  );

  // Animación de los submódulos (píldoras) con stagger y elasticidad de entrada
  tl.fromTo("#scene-modules .submodule-pill",
    { y: 20, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.7, stagger: 0.08, ease: "back.out(1.2)" },
    4.2
  );

  // Transición de Escena 2 a Escena 3 (Ocultar Escena 2)
  tl.to("#scene-modules", { autoAlpha: 0, duration: 0.5 }, 7.0);


  // --- ANIMACIONES ESCENA 3: LLAMADA A LA ACCIÓN (7.5s - 12s) ---
  // Mostrar contenedor de la escena 3
  tl.to("#scene-cta", { autoAlpha: 1, duration: 0.5 }, 7.5);

  // Animación del celular (mockup móvil)
  tl.fromTo("#scene-cta .phone-mockup", 
    { x: -150, opacity: 0, scale: 0.85, rotate: -3 }, 
    { x: 0, opacity: 1, scale: 1, rotate: 0, duration: 1.2, ease: "power4.out" }, 
    7.8
  );

  // Revelación deslizante de la captura de pantalla del login dentro del mockup
  tl.fromTo("#scene-cta .phone-screen", 
    { y: 60, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 1.2, ease: "power3.out" }, 
    8.4
  );

  // Animación de los textos a la derecha (Badge, título, párrafo, botones)
  tl.fromTo("#scene-cta .badge", 
    { scale: 0.7, opacity: 0 }, 
    { scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.5)" }, 
    8.2
  );

  tl.fromTo("#scene-cta .cta-text h2", 
    { y: 40, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }, 
    8.5
  );

  tl.fromTo("#scene-cta .cta-text p", 
    { y: 30, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }, 
    8.7
  );

  tl.fromTo("#scene-cta .cta-buttons", 
    { y: 30, opacity: 0 }, 
    { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }, 
    8.9
  );

  // Guardar referencias globales en window para interactuar con los botones de desarrollo
  window.goToScene = (sceneNum) => {
    const times = { 1: 0, 2: 3.0, 3: 7.5 };
    tl.seek(times[sceneNum]).pause();
    updatePlayPauseButton();
  };

  window.togglePlay = () => {
    if (tl.paused()) {
      tl.play();
    } else {
      tl.pause();
    }
    updatePlayPauseButton();
  };

  function updatePlayPauseButton() {
    const btn = document.getElementById("btn-play-pause");
    if (btn) {
      btn.textContent = tl.paused() ? "Play" : "Pause";
      // Añadir estilo distintivo cuando esté activo
      if (!tl.paused()) {
        btn.style.background = "#E6423C";
        btn.style.borderColor = "#E6423C";
      } else {
        btn.style.background = "rgba(255, 255, 255, 0.08)";
        btn.style.borderColor = "rgba(255, 255, 255, 0.12)";
      }
    }
  }

  // Actualizar indicador de tiempo dinámicamente
  tl.eventCallback("onUpdate", () => {
    const timeSpan = document.getElementById("playhead-time");
    if (timeSpan) {
      timeSpan.textContent = `Tiempo: ${tl.time().toFixed(1)}s / ${tl.duration().toFixed(1)}s`;
    }
    updatePlayPauseButton();
  });

  // Para poder probar la animación en el navegador sin el CLI de HyperFrames:
  // Si no se detecta la ejecución dentro de HyperFrames (o si deseas probar localmente),
  // podemos hacer que la animación se reproduzca automáticamente.
  if (!window.location.search.includes("hyperframes")) {
    tl.play();
  }
