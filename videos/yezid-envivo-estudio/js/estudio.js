// «Estudio virtual»: fondo sólido verde profundo (degradado radial muy sutil) y, encima,
// UNA de dos piezas 3D intencionales — nunca fluidos ni partículas al azar:
//   escudo : escudo geométrico de cristal con aristas doradas + anillo de datos (por defecto)
//   plexus : red geométrica fina, lenta y tenue («análisis de datos y conexiones»)
// Sin reloj propio: todo sale del tiempo t del timeline → seek-safe y determinista.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

// Lo que animan los timelines: pulso (destello) · zoom (0→1, cámara hacia adelante en el CTA)
export const estado = { pulso: 0, zoom: 0 };

const W = 1080, H = 1920;
const DORADO = new THREE.Color("#d2b96a"), PALIDO = new THREE.Color("#f1ecb0"), VERDE = new THREE.Color("#4f8f7f");

const fragFondo = /* glsl */ `
precision highp float;
uniform float uPulso;
varying vec2 vUv;
void main(){
  vec2 d = (vUv - vec2(0.5, 0.58)) * vec2(1.0, 1.7778);
  float r = clamp(length(d) / 1.05, 0.0, 1.0);
  vec3 centro = vec3(26.0, 59.0, 59.0) / 255.0;   // #1A3B3B
  vec3 borde  = vec3(15.0, 42.0, 42.0) / 255.0;   // #0F2A2A
  vec3 col = mix(centro, borde, smoothstep(0.0, 1.0, r));
  col += vec3(0.945, 0.925, 0.69) * uPulso * 0.07 * (1.0 - r);
  gl_FragColor = vec4(col, 1.0);
}`;

function mulberry32(a) {
  return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

// ── pieza 1 · escudo de cristal + anillo de datos ──
function crearEscudo(escena) {
  const s = new THREE.Shape();
  s.moveTo(0, 1.25);
  s.lineTo(1.02, 0.92);
  s.lineTo(1.02, 0.05);
  s.quadraticCurveTo(0.98, -0.78, 0, -1.3);
  s.quadraticCurveTo(-0.98, -0.78, -1.02, 0.05);
  s.lineTo(-1.02, 0.92);
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, { depth: 0.22, bevelEnabled: true, bevelThickness: 0.06,
    bevelSize: 0.05, bevelSegments: 5, curveSegments: 48 });
  geo.center();
  const cristal = new THREE.MeshPhysicalMaterial({
    color: 0x6fa89b, metalness: 0.15, roughness: 0.06, transmission: 0.85, thickness: 0.8, ior: 1.5,
    clearcoat: 1, clearcoatRoughness: 0.02, transparent: true, opacity: 0.8, envMapIntensity: 2.6,
    emissive: 0x0f2a2a, emissiveIntensity: 0.2, specularIntensity: 1, specularColor: 0xf1ecb0,
  });
  const escudo = new THREE.Mesh(geo, cristal);
  const aristas = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 28),
    new THREE.LineBasicMaterial({ color: DORADO, transparent: true, opacity: 0.75 }));
  // escudo interior: la «capa de protección», solo el contorno
  const pts = s.getPoints(64).map((p) => new THREE.Vector3(p.x * 0.7, p.y * 0.7 + 0.0, 0.2));
  const interior = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts),
    new THREE.LineBasicMaterial({ color: PALIDO, transparent: true, opacity: 0.45 }));
  interior.position.y = 0.0; interior.geometry.center(); interior.position.z = 0.2;

  // anillo de datos: toro metálico dorado con tres nodos que orbitan
  const R = 1.45;
  const anillo = new THREE.Mesh(new THREE.TorusGeometry(R, 0.018, 24, 256),
    new THREE.MeshStandardMaterial({ color: DORADO, metalness: 1, roughness: 0.25, emissive: DORADO, emissiveIntensity: 0.15 }));
  anillo.rotation.x = Math.PI / 2.4;
  const anillo2 = new THREE.Mesh(new THREE.TorusGeometry(R * 1.14, 0.007, 16, 256),
    new THREE.MeshBasicMaterial({ color: PALIDO, transparent: true, opacity: 0.35 }));
  anillo2.rotation.x = Math.PI / 2.1; anillo2.rotation.y = 0.35;
  const nodos = [0, 1, 2].map(() => new THREE.Mesh(new THREE.SphereGeometry(0.045, 24, 16),
    new THREE.MeshBasicMaterial({ color: PALIDO })));

  const grupo = new THREE.Group();
  grupo.add(escudo, aristas, interior, anillo, anillo2, ...nodos);
  // a la derecha de la foto: foto (la persona) + escudo (la seguridad), lado a lado
  const X = 0.82, Y = 1.55;
  grupo.position.set(X, Y, 0);
  grupo.scale.setScalar(0.72);
  escena.add(grupo);

  return (t) => {
    grupo.rotation.y = t * 0.24;                        // rotación perpetua en Y
    grupo.rotation.x = 0.1 * Math.sin(t * 0.35);
    grupo.position.y = Y + 0.06 * Math.sin(t * 0.5);    // también respira
    anillo.rotation.z = t * 0.18;
    nodos.forEach((n, i) => {                           // los nodos corren sobre el anillo
      const a = t * 0.55 + (i * Math.PI * 2) / 3, r = R;
      const v = new THREE.Vector3(Math.cos(a) * r, Math.sin(a) * r, 0).applyEuler(anillo.rotation);
      n.position.copy(v);
    });
    aristas.material.opacity = 0.6 + 0.35 * estado.pulso;
  };
}

// ── pieza 2 · red geométrica (plexus) lenta y tenue ──
function crearPlexus(escena) {
  const N = 130, ENLACE = 0.8, MAX = 900;
  const rnd = mulberry32(11);
  const base = [], fase = [];
  for (let i = 0; i < N; i++) {
    base.push(new THREE.Vector3((rnd() - 0.5) * 5.2, (rnd() - 0.5) * 9.4, (rnd() - 0.5) * 2.4));
    fase.push([rnd() * 6.28, rnd() * 6.28, rnd() * 6.28]);
  }
  const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
  const gP = new THREE.BufferGeometry();
  gP.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  gP.setAttribute("color", new THREE.BufferAttribute(col, 3));
  for (let i = 0; i < N; i++) (i % 3 ? VERDE : DORADO).toArray(col, i * 3);
  const c = document.createElement("canvas"); c.width = c.height = 64;      // punto redondo y suave
  const g = c.getContext("2d"), rg = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  rg.addColorStop(0, "#fff"); rg.addColorStop(0.4, "rgba(255,255,255,0.8)"); rg.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = rg; g.fillRect(0, 0, 64, 64);
  const puntos = new THREE.Points(gP, new THREE.PointsMaterial({ size: 0.075, vertexColors: true, transparent: true,
    opacity: 0.55, depthWrite: false, map: new THREE.CanvasTexture(c) }));
  const lp = new Float32Array(MAX * 6), lc = new Float32Array(MAX * 6);
  const gL = new THREE.BufferGeometry();
  gL.setAttribute("position", new THREE.BufferAttribute(lp, 3));
  gL.setAttribute("color", new THREE.BufferAttribute(lc, 3));
  const lineas = new THREE.LineSegments(gL, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true,
    opacity: 1, depthWrite: false, blending: THREE.AdditiveBlending }));
  const grupo = new THREE.Group(); grupo.add(lineas, puntos); escena.add(grupo);
  const p = Array.from({ length: N }, () => new THREE.Vector3());

  return (t) => {
    const v = 0.18;                                      // extrema lentitud
    for (let i = 0; i < N; i++) {
      const b = base[i], f = fase[i];
      p[i].set(b.x + 0.12 * Math.sin(t * v + f[0]), b.y + 0.12 * Math.sin(t * v * 0.8 + f[1]), b.z + 0.1 * Math.sin(t * v * 0.9 + f[2]));
      p[i].toArray(pos, i * 3);
    }
    gP.attributes.position.needsUpdate = true;
    let k = 0;
    for (let i = 0; i < N && k < MAX; i++) for (let j = i + 1; j < N && k < MAX; j++) {
      const d = p[i].distanceTo(p[j]);
      if (d < ENLACE) {
        const a = (1 - d / ENLACE) * (0.22 + 0.25 * estado.pulso);
        const c = (i + j) % 4 === 0 ? DORADO : VERDE;
        p[i].toArray(lp, k * 6); p[j].toArray(lp, k * 6 + 3);
        lc.set([c.r * a, c.g * a, c.b * a, c.r * a, c.g * a, c.b * a], k * 6); k++;
      }
    }
    gL.setDrawRange(0, k * 2);
    gL.attributes.position.needsUpdate = true; gL.attributes.color.needsUpdate = true;
    grupo.rotation.y = t * 0.03;                         // gira con extrema lentitud
  };
}

export function crearEstudio(canvas, modo = "escudo") {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.autoClear = false;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const escenaF = new THREE.Scene(), camF = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uF = { uPulso: { value: 0 } };
  escenaF.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ uniforms: uF,
    fragmentShader: fragFondo, depthTest: false, depthWrite: false, toneMapped: false,
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }" })));

  const escena = new THREE.Scene();
  escena.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 50);
  escena.add(new THREE.AmbientLight(0xffffff, 0.35));
  const clave = new THREE.DirectionalLight(0xf1ecb0, 1.6); clave.position.set(-3, 4, 5); escena.add(clave);
  const contra = new THREE.PointLight(0xd2b96a, 18, 20); contra.position.set(3, -1, -3); escena.add(contra);

  const animar = modo === "plexus" ? crearPlexus(escena) : crearEscudo(escena);

  return {
    render(t) {
      animar(t);
      cam.position.set(0, 0, 9.2 - 1.3 * estado.zoom);   // zoom-in sutil en el CTA
      cam.lookAt(0.35 * estado.zoom, 0.6 * estado.zoom, 0);   // el zoom se acerca al escudo
      uF.uPulso.value = estado.pulso;
      renderer.clear();
      renderer.render(escenaF, camF);
      renderer.clearDepth();
      renderer.render(escena, cam);
    },
  };
}
