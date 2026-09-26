// Fondo WebGL: gradiente líquido muy sutil + red de puntos conectados en 3D
// («gestión de datos / seguridad»). Sin reloj propio: todo sale del tiempo t del
// timeline de GSAP, así que cualquier fotograma se puede buscar y sale idéntico.
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

// Lo que animan los timelines:
//   energia → velocidad y densidad de enlaces · pulso → destello en los golpes
//   calma   → el gradiente se aclara hacia el verde del manual
export const fondoEstado = { energia: 0.4, pulso: 0, calma: 0 };

const W = 1080, H = 1920;
const N = 110;           // nodos
const ENLACE = 0.62;     // distancia máxima para unir dos nodos
const MAX_LINEAS = 900;

// PRNG determinista: la misma red en preview y en render
function mulberry32(a) {
  return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

const fragGradiente = /* glsl */ `
precision highp float;
uniform float uT, uPulso, uCalma;
varying vec2 vUv;
const vec3 FONDO = vec3(0.0, 0.122, 0.149);   // #001f26
const vec3 YEZID = vec3(0.2, 0.4, 0.4);       // #336666
const vec3 TEAL = vec3(0.004, 0.271, 0.329);  // #014554 (yezidricaurte.com)
const vec3 PALIDO = vec3(0.945, 0.925, 0.690);// #f1ecb0
float blob(vec2 uv, vec2 c, float r){ vec2 d = (uv - c) * vec2(1.0, 1.7778); return exp(-dot(d,d) / (r*r)); }
void main(){
  vec2 uv = vUv;
  vec3 col = FONDO;
  // tres manchas que derivan despacio: el «mesh gradient»
  vec2 c1 = vec2(0.25 + 0.08*sin(uT*0.21), 0.72 + 0.05*cos(uT*0.17));
  vec2 c2 = vec2(0.80 + 0.06*cos(uT*0.19), 0.40 + 0.07*sin(uT*0.23));
  vec2 c3 = vec2(0.50 + 0.10*sin(uT*0.13 + 1.3), 0.12 + 0.04*sin(uT*0.29));
  col += YEZID * blob(uv, c1, 0.55) * (0.55 + 0.25*uCalma);
  col += TEAL * blob(uv, c2, 0.45) * 0.55;
  col += PALIDO * blob(uv, c3, 0.35) * 0.05;
  col += PALIDO * uPulso * 0.10 * blob(uv, vec2(0.5, 0.35), 0.8);
  vec2 v = uv - 0.5; col *= 1.0 - 0.9*dot(v, v);   // viñeta
  gl_FragColor = vec4(col, 1.0);
}`;

function texturaPunto() {
  const c = document.createElement("canvas"); c.width = c.height = 64;
  const g = c.getContext("2d"); const r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(0.35, "rgba(255,255,255,0.85)");
  r.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = r; g.fillRect(0, 0, 64, 64);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export function crearFondo(canvas, semilla = 7) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.autoClear = false;

  // capa 1 · gradiente
  const escenaG = new THREE.Scene();
  const camG = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uG = { uT: { value: 0 }, uPulso: { value: 0 }, uCalma: { value: 0 } };
  escenaG.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({
    uniforms: uG, fragmentShader: fragGradiente, depthWrite: false, depthTest: false,
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
  })));

  // capa 2 · red de nodos en 3D
  const escenaR = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(42, W / H, 0.1, 20);
  cam.position.set(0, 0, 4.2);
  const rnd = mulberry32(semilla);
  const base = [], fase = [], amp = [];
  for (let i = 0; i < N; i++) {
    base.push(new THREE.Vector3((rnd() - 0.5) * 3.0, (rnd() - 0.5) * 5.4, (rnd() - 0.5) * 1.8));
    fase.push([rnd() * 6.28, rnd() * 6.28, rnd() * 6.28]);
    amp.push(0.06 + rnd() * 0.12);
  }
  const pos = new Float32Array(N * 3);
  const gPuntos = new THREE.BufferGeometry();
  gPuntos.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const matPuntos = new THREE.PointsMaterial({ size: 0.055, map: texturaPunto(), color: 0xf1ecb0, transparent: true,
    opacity: 0.75, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
  const puntos = new THREE.Points(gPuntos, matPuntos);

  const lpos = new Float32Array(MAX_LINEAS * 6), lcol = new Float32Array(MAX_LINEAS * 6);
  const gLineas = new THREE.BufferGeometry();
  gLineas.setAttribute("position", new THREE.BufferAttribute(lpos, 3));
  gLineas.setAttribute("color", new THREE.BufferAttribute(lcol, 3));
  const lineas = new THREE.LineSegments(gLineas, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true,
    opacity: 1, depthWrite: false, blending: THREE.AdditiveBlending }));
  const grupo = new THREE.Group(); grupo.add(lineas, puntos); escenaR.add(grupo);

  const dorado = new THREE.Color("#d2b96a"), palido = new THREE.Color("#f1ecb0"), yez = new THREE.Color("#336666");
  const p = Array.from({ length: N }, () => new THREE.Vector3());

  return {
    render(t) {
      const e = fondoEstado.energia, pu = fondoEstado.pulso;
      const vel = 0.35 + 0.9 * e;
      for (let i = 0; i < N; i++) {
        const b = base[i], f = fase[i], a = amp[i];
        p[i].set(b.x + a * Math.sin(t * vel * 0.9 + f[0]), b.y + a * Math.sin(t * vel * 0.7 + f[1]),
                 b.z + a * Math.sin(t * vel * 0.8 + f[2]));
        pos.set([p[i].x, p[i].y, p[i].z], i * 3);
      }
      gPuntos.attributes.position.needsUpdate = true;
      let k = 0;
      const lim = ENLACE * (0.85 + 0.3 * e);
      for (let i = 0; i < N && k < MAX_LINEAS; i++) for (let j = i + 1; j < N && k < MAX_LINEAS; j++) {
        const d = p[i].distanceTo(p[j]);
        if (d < lim) {
          const a = (1 - d / lim) * (0.30 + 0.45 * pu);
          const c = (i + j) % 7 === 0 ? palido : ((i + j) % 3 === 0 ? dorado : yez);
          lpos.set([p[i].x, p[i].y, p[i].z, p[j].x, p[j].y, p[j].z], k * 6);
          lcol.set([c.r * a, c.g * a, c.b * a, c.r * a, c.g * a, c.b * a], k * 6);
          k++;
        }
      }
      gLineas.setDrawRange(0, k * 2);
      gLineas.attributes.position.needsUpdate = true; gLineas.attributes.color.needsUpdate = true;
      matPuntos.opacity = 0.55 + 0.35 * pu + 0.15 * e;
      // la cámara deriva: rotación lenta de la red, nunca quieta
      grupo.rotation.y = 0.18 * Math.sin(t * 0.12);
      grupo.rotation.x = 0.08 * Math.sin(t * 0.09 + 1.0);
      grupo.position.y = -0.15 + 0.05 * t;

      uG.uT.value = t; uG.uPulso.value = pu; uG.uCalma.value = fondoEstado.calma;
      renderer.clear();
      renderer.render(escenaG, camG);
      renderer.clearDepth();          // el plano del gradiente no debe tapar la red
      renderer.render(escenaR, cam);
    },
  };
}
