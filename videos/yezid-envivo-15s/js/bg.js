// Escena 3D de fondo (Three.js): «análisis de datos y seguridad».
//   · túnel de partículas que viaja hacia la cámara
//   · rayos de datos (líneas que se estiran con la velocidad)
//   · anillos wireframe que marcan el paso del túnel
//   · mallas geométricas oscuras (icosaedros wireframe) que giran al fondo
// Paleta: ambiente #336666 / #80804a, destellos #45a035, acentos #f1ecb0.
//
// Determinista: todo es función del tiempo del timeline. La distancia recorrida se integra
// desde 0 sobre una curva de velocidad fija (setVelocidad), así que buscar el segundo 11.5
// da exactamente el mismo fotograma que llegar reproduciendo.
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

export const BG_MODES = ["tunel"];
export const bgState = { fov: 0, roll: 0, brillo: 0 };   // los anima el timeline (golpes de cámara)

const C = {
  verde: new THREE.Color("#336666"), tierra: new THREE.Color("#80804a"),
  fegir: new THREE.Color("#45a035"), palido: new THREE.Color("#f1ecb0"),
  fondo: new THREE.Color("#021417"),
};
const LARGO = 260;        // largo del túnel (se repite)
const RND = (() => { let s = 20261003; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); })();

function colorPaleta() {
  const r = RND();
  return r < 0.55 ? C.verde : r < 0.75 ? C.tierra : r < 0.93 ? C.fegir : C.palido;
}

const vertPuntos = /* glsl */ `
  uniform float uViaje, uLargo, uTam;
  attribute vec3 color; attribute float tam;
  varying vec3 vColor; varying float vNiebla;
  void main(){
    vec3 p = position;
    p.z = mod(p.z + uViaje, uLargo) - uLargo;          // el túnel se repite sin costura
    vec4 mv = modelViewMatrix * vec4(p, 1.0);
    gl_Position = projectionMatrix * mv;
    gl_PointSize = tam * uTam * (300.0 / -mv.z);
    vColor = color;
    vNiebla = smoothstep(uLargo * 0.95, 8.0, -mv.z);   // 0 lejos · 1 cerca
  }`;
const fragPuntos = /* glsl */ `
  varying vec3 vColor; varying float vNiebla;
  void main(){
    vec2 c = gl_PointCoord - 0.5; float d = length(c);
    float a = smoothstep(0.5, 0.0, d);
    gl_FragColor = vec4(vColor * (0.6 + 1.4 * a), a * vNiebla);
  }`;
const vertRayos = /* glsl */ `
  uniform float uViaje, uLargo, uEstela;
  attribute vec3 color; attribute float cola;
  varying vec3 vColor; varying float vA;
  void main(){
    vec3 p = position;
    p.z = mod(p.z + uViaje, uLargo) - uLargo - cola * uEstela;   // la cola se estira con la velocidad
    vec4 mv = modelViewMatrix * vec4(p, 1.0);
    gl_Position = projectionMatrix * mv;
    vColor = color;
    vA = (1.0 - cola) * smoothstep(uLargo * 0.9, 10.0, -mv.z);
  }`;
const fragRayos = /* glsl */ `
  varying vec3 vColor; varying float vA;
  void main(){ gl_FragColor = vec4(vColor * 1.6, vA * 0.9); }`;

export function createBackground(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(1080, 1920, false);
  renderer.setClearColor(C.fondo, 1);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(C.fondo, 0.012);
  const camera = new THREE.PerspectiveCamera(70, 1080 / 1920, 0.1, 400);

  // ── partículas del túnel ──
  const N = 6500, pos = new Float32Array(N * 3), col = new Float32Array(N * 3), tam = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const a = RND() * Math.PI * 2, r = 2.2 + Math.pow(RND(), 0.6) * 9;
    pos.set([Math.cos(a) * r, Math.sin(a) * r * 1.35, -RND() * LARGO], i * 3);
    const c = colorPaleta(); col.set([c.r, c.g, c.b], i * 3);
    tam[i] = c === C.palido ? 2.6 : 0.8 + RND() * 1.6;
  }
  const gP = new THREE.BufferGeometry();
  gP.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  gP.setAttribute("color", new THREE.BufferAttribute(col, 3));
  gP.setAttribute("tam", new THREE.BufferAttribute(tam, 1));
  const uP = { uViaje: { value: 0 }, uLargo: { value: LARGO }, uTam: { value: 1 } };
  const puntos = new THREE.Points(gP, new THREE.ShaderMaterial({
    uniforms: uP, vertexShader: vertPuntos, fragmentShader: fragPuntos,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  puntos.frustumCulled = false;
  scene.add(puntos);

  // ── rayos de datos ──
  const R = 420, pr = new Float32Array(R * 6), cr = new Float32Array(R * 6), co = new Float32Array(R * 2);
  for (let i = 0; i < R; i++) {
    const a = RND() * Math.PI * 2, r = 3 + RND() * 7, z = -RND() * LARGO;
    const x = Math.cos(a) * r, y = Math.sin(a) * r * 1.35;
    pr.set([x, y, z, x, y, z], i * 6);
    const c = RND() < 0.6 ? C.fegir : RND() < 0.5 ? C.palido : C.verde;
    cr.set([c.r, c.g, c.b, c.r, c.g, c.b], i * 6);
    co.set([0, 1], i * 2);
  }
  const gR = new THREE.BufferGeometry();
  gR.setAttribute("position", new THREE.BufferAttribute(pr, 3));
  gR.setAttribute("color", new THREE.BufferAttribute(cr, 3));
  gR.setAttribute("cola", new THREE.BufferAttribute(co, 1));
  const uR = { uViaje: { value: 0 }, uLargo: { value: LARGO }, uEstela: { value: 2 } };
  const rayos = new THREE.LineSegments(gR, new THREE.ShaderMaterial({
    uniforms: uR, vertexShader: vertRayos, fragmentShader: fragRayos,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  rayos.frustumCulled = false;
  scene.add(rayos);

  // ── anillos wireframe del túnel ──
  const anillos = [];
  const matAnillo = new THREE.LineBasicMaterial({ color: C.verde, transparent: true, opacity: 0.35 });
  const geoAnillo = new THREE.EdgesGeometry(new THREE.CylinderGeometry(10.5, 10.5, 0.01, 6, 1, true));
  for (let i = 0; i < 12; i++) {
    const m = new THREE.LineSegments(geoAnillo, matAnillo);
    m.rotation.x = Math.PI / 2; m.scale.y = 1; m.userData.z0 = -(i / 12) * LARGO;
    anillos.push(m); scene.add(m);
  }

  // ── mallas oscuras al fondo ──
  const mallas = [];
  const matMalla = new THREE.MeshBasicMaterial({ color: C.tierra, wireframe: true, transparent: true, opacity: 0.22 });
  [[-7, 6, -70, 7], [8, -8, -110, 9], [-5, -10, -160, 6], [6, 9, -210, 8]].forEach(([x, y, z, s], i) => {
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(s, 1), i % 2 ? matMalla : matMalla.clone());
    if (!(i % 2)) m.material.color = C.verde;
    m.position.set(x, y, z); m.userData = { z0: z, gira: 0.08 + i * 0.03 };
    mallas.push(m); scene.add(m);
  });

  // ── curva de velocidad (unidades/s) y su integral ──
  let claves = [[0, 10], [15, 10]];
  const velocidad = (t) => {
    for (let i = 1; i < claves.length; i++) {
      const [t0, v0] = claves[i - 1], [t1, v1] = claves[i];
      if (t <= t1) { const k = (t - t0) / Math.max(1e-6, t1 - t0); const e = k * k * (3 - 2 * k); return v0 + (v1 - v0) * e; }
    }
    return claves[claves.length - 1][1];
  };
  const viaje = (t) => { let s = 0; const dt = 1 / 120; for (let x = 0; x < t; x += dt) s += velocidad(Math.min(x, t)) * Math.min(dt, t - x); return s; };

  return {
    setVelocidad(k) { claves = k; },
    render(t) {
      const v = velocidad(t), d = viaje(t);
      uP.uViaje.value = d; uR.uViaje.value = d;
      uR.uEstela.value = 0.6 + v * 0.22;                       // a más velocidad, rayos más largos
      uP.uTam.value = 1 + bgState.brillo * 0.8;
      anillos.forEach((m) => { m.position.z = ((m.userData.z0 + d) % LARGO + LARGO) % LARGO - LARGO; m.rotation.y = t * 0.15; });
      mallas.forEach((m) => {
        m.position.z = ((m.userData.z0 + d * 0.35) % LARGO + LARGO) % LARGO - LARGO;
        m.rotation.x = t * m.userData.gira; m.rotation.y = t * m.userData.gira * 1.3;
      });
      // paralaje continuo de cámara + golpes del timeline
      camera.position.set(Math.sin(t * 0.55) * 0.9, Math.cos(t * 0.43) * 0.7, 6);
      camera.lookAt(Math.sin(t * 0.3) * 0.6, Math.cos(t * 0.37) * 0.5, -30);
      camera.rotation.z += Math.sin(t * 0.25) * 0.05 + bgState.roll;
      camera.fov = 70 + Math.min(18, v * 0.18) + bgState.fov;   // la velocidad abre el lente
      camera.updateProjectionMatrix();
      renderer.render(scene, camera);
    },
  };
}
