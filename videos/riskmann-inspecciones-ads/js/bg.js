// Fondo Three.js con la paleta del manual oficial (frame.md de riskmann-consulta-pesv-vertical).
// No hay reloj propio: el tiempo que recibe render() es el del timeline de GSAP, así que el
// fondo es seek-safe y el mismo fotograma sale igual en preview que en render.
//
// Cinco fondos, un solo shader (?bg=<nombre>):
//   liquido     mesh gradient líquido (V1)
//   aurora      cortinas de luz verticales
//   topografico curvas de nivel que respiran (mapa / terreno)
//   carretera   piso en perspectiva con carriles que avanzan hacia la cámara
//   bokeh       luces de tráfico desenfocadas (faros dorados, stops rojos)
//   solido      negro plano #040404, el fondo de la landing (var(--black)); no reacciona
//   azul        azul marino plano de la landing (#1a2744, --blue-navy) con retícula de puntos,
//               rayado diagonal tenue y los dos halos del hero de la landing (V3)
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

export const BG_MODES = ["liquido", "aurora", "topografico", "carretera", "bokeh", "solido", "azul"];

// Estado que los timelines animan (reacción del fondo a la línea de tiempo).
//   heat  → tensión roja (#FF3333): SOLO peligro/problema
//   calm  → alivio cian (#06c7fb) en la solución
//   pulse → destello puntual en los golpes
//   gold  → tiñe el destello de dorado (llamados a la acción, V2)
//   warp  → agitación / velocidad del fondo
//   zoom  → escala del campo (respiración de cámara)
export const bgState = { heat: 0, calm: 0, pulse: 0, gold: 0, warp: 0, zoom: 1 };

const frag = /* glsl */ `
precision highp float;
uniform float uTime, uHeat, uCalm, uPulse, uGold, uWarp, uZoom, uMode;
uniform vec2 uRes;
varying vec2 vUv;

const vec3 BG    = vec3(0.008);                 // #020202
const vec3 NAVY  = vec3(0.149, 0.212, 0.490);   // #26367D
const vec3 TECH  = vec3(0.200, 0.200, 0.400);   // #333366
const vec3 STEEL = vec3(0.200, 0.400, 0.600);   // #336699
const vec3 RED   = vec3(1.000, 0.200, 0.200);   // #FF3333
const vec3 CYAN  = vec3(0.024, 0.780, 0.984);   // #06c7fb
const vec3 GOLD  = vec3(0.784, 0.584, 0.102);   // #c8951a

vec2 hash(vec2 p){ p = vec2(dot(p,vec2(127.1,311.7)), dot(p,vec2(269.5,183.3))); return -1.0+2.0*fract(sin(p)*43758.5453); }
float noise(vec2 p){
  const float K1 = 0.366025404; const float K2 = 0.211324865;
  vec2 i = floor(p + (p.x+p.y)*K1); vec2 a = p - i + (i.x+i.y)*K2;
  float m = step(a.y,a.x); vec2 o = vec2(m,1.0-m);
  vec2 b = a - o + K2; vec2 c = a - 1.0 + 2.0*K2;
  vec3 h = max(0.5-vec3(dot(a,a), dot(b,b), dot(c,c)), 0.0);
  vec3 n = h*h*h*h*vec3(dot(a,hash(i)), dot(b,hash(i+o)), dot(c,hash(i+1.0)));
  return dot(n, vec3(70.0));
}
float fbm(vec2 p){ float f=0.0, a=0.5; mat2 r=mat2(1.6,1.2,-1.2,1.6); for(int i=0;i<5;i++){ f+=a*noise(p); p=r*p; a*=0.5; } return 0.5+0.5*f; }

// ── 0 · líquido ──
vec3 liquido(vec2 p, float t){
  t *= 0.11;
  vec2 q = vec2(fbm(p + vec2(0.0, t)), fbm(p + vec2(5.2, 1.3) - t));
  vec2 r = vec2(fbm(p + (3.0+uWarp)*q + vec2(1.7, 9.2) + 1.4*t), fbm(p + (3.0+uWarp)*q + vec2(8.3, 2.8) - 1.2*t));
  float f = fbm(p + (2.4 + 1.5*uWarp) * r);
  vec3 col = mix(BG, TECH, smoothstep(0.25, 0.85, f));
  col = mix(col, NAVY, 0.85*smoothstep(0.35, 0.95, length(q)));
  col = mix(col, STEEL, 0.45*smoothstep(0.55, 1.0, r.x));
  col = mix(col, RED*0.85, uHeat * 0.55 * smoothstep(0.45, 1.0, f*r.y*1.6));
  col = mix(col, CYAN*0.75, uCalm * 0.40 * smoothstep(0.5, 1.0, r.x*f*1.5));
  col *= 0.35 + 0.55*f*f;
  col += 0.06 * pow(smoothstep(0.6, 1.0, f), 3.0);
  return col;
}

// ── 1 · aurora ──
vec3 aurora(vec2 uv, float t){
  vec3 col = mix(vec3(0.006,0.008,0.02), vec3(0.02,0.03,0.07), uv.y);
  for (int i = 0; i < 4; i++) {
    float fi = float(i);
    float sp = 0.5 + 0.6*uWarp;
    float x = uv.x + 0.16*sin(uv.y*2.6 + t*0.45*sp + fi*1.9) + 0.07*sin(uv.y*6.3 - t*0.7*sp + fi*2.3);
    float center = 0.14 + 0.24*fi;
    float band = exp(-pow((x - center)*(5.5 + 1.5*fi), 2.0));
    float rays = 0.55 + 0.45*noise(vec2(x*38.0, t*0.25 + fi*3.1));
    float fall = smoothstep(-0.05, 0.75, uv.y) * smoothstep(1.1, 0.45, uv.y);
    vec3 c = i == 0 ? NAVY*1.6 : (i == 1 ? STEEL*1.3 : (i == 2 ? TECH*1.8 : GOLD*0.7));
    c = mix(c, RED, uHeat * (i == 3 ? 0.2 : 0.55));
    c = mix(c, CYAN, uCalm * (i == 1 ? 0.8 : 0.35));
    col += c * band * rays * fall * 0.95;
  }
  col += NAVY * 0.25 * smoothstep(0.4, 0.0, uv.y);
  return col;
}

// ── 2 · topográfico ──
vec3 topografico(vec2 p, float t){
  float f = fbm(p*0.9 + vec2(t*0.035, -t*0.025)) + 0.35*fbm(p*2.1 - t*0.05) * (0.6 + uWarp);
  float v = f * 12.0;
  float d = abs(fract(v - 0.5) - 0.5) / fwidth(v);
  float line = 1.0 - clamp(d, 0.0, 1.0);
  float idx = floor(v + 0.5);
  float major = step(4.5, mod(idx, 5.0));
  vec3 base = mix(BG, NAVY*0.5, smoothstep(0.2, 0.9, f));
  vec3 lc = mix(STEEL*0.75, GOLD*0.95, major);
  lc = mix(lc, RED, uHeat*0.6);
  lc = mix(lc, CYAN, uCalm*0.7*(1.0 - major));
  float glow = 0.35 + 0.65*smoothstep(0.3, 0.9, fbm(p*0.6 + t*0.02));
  return base + lc * line * (0.6 + 0.45*major) * glow;
}

// ── 3 · carretera ──
vec3 carretera(vec2 uv, float t){
  float hz = 0.60;                       // horizonte
  vec3 sky = mix(NAVY*0.30, BG, smoothstep(hz, 1.0, uv.y));
  sky += mix(STEEL*0.5, RED*0.8, uHeat) * exp(-abs(uv.y - hz)*14.0) * 0.8;
  sky += CYAN * uCalm * exp(-abs(uv.y - hz)*10.0) * 0.35;
  if (uv.y >= hz) return sky;
  float depth = 0.32 / (hz - uv.y);
  float x = (uv.x - 0.5) * depth * 2.2;
  float z = depth + t * (1.6 + 3.0*uWarp);
  float fw = fwidth(x);
  float lanes = 0.0;
  for (int i = -2; i <= 2; i++) {                        // divisiones de carril, discontinuas
    float lx = float(i) * 1.1;
    float dash = step(0.45, fract(z*0.35));
    lanes += (1.0 - smoothstep(0.0, fw*1.5 + 0.02, abs(x - lx))) * dash * (i == 0 ? 0.0 : 1.0);
  }
  float edges = 1.0 - smoothstep(0.0, fw*1.5 + 0.03, abs(abs(x) - 2.9));   // bordes continuos
  float cross = 1.0 - smoothstep(0.0, fwidth(z)*1.5, abs(fract(z*0.25) - 0.5) - 0.48);
  float fade = exp(-depth*0.12);
  vec3 floorC = mix(BG, TECH*0.35, fade);
  vec3 lc = mix(GOLD, RED, uHeat*0.7);
  lc = mix(lc, CYAN, uCalm*0.6);
  vec3 col = floorC + lc * lanes * fade * 0.9 + mix(STEEL, CYAN, uCalm) * edges * fade * 0.9 + STEEL * cross * fade * 0.12;
  col += sky * smoothstep(hz - 0.04, hz, uv.y);
  return col;
}

// ── 6 · azul: plano, con diseño de bajo contraste ──
vec3 azul(vec2 uv, float t){
  vec3 base = vec3(26.0, 39.0, 68.0) / 255.0;                    // #1a2744 --blue-navy
  vec2 asp = vec2(1.0, 1920.0/1080.0);
  // los dos halos del hero de riskmann.com (.hero::before), respirando despacio
  vec2 c1 = vec2(0.78, 0.58 + 0.02*sin(t*0.3)); vec2 c2 = vec2(0.15, 0.78);
  float h1 = exp(-dot((uv - c1)*asp, (uv - c1)*asp) * 3.2);
  float h2 = exp(-dot((uv - c2)*asp, (uv - c2)*asp) * 4.5);
  vec3 halo1 = mix(NAVY, RED*0.55, uHeat*0.6); halo1 = mix(halo1, CYAN*0.5, uCalm*0.5);
  vec3 col = base + (halo1 - base*0.5) * h1 * 0.45 + GOLD * h2 * 0.10;
  // retícula de puntos: 40 px en el lienzo 1080×1920, deriva hacia arriba muy lenta
  vec2 g = uv * vec2(1080.0, 1920.0) / 40.0 + vec2(0.0, t*0.12);
  float d = length(fract(g) - 0.5);
  float w = fwidth(d) * 1.2;
  float dots = 1.0 - smoothstep(0.075 - w, 0.075 + w, d);
  col += vec3(0.55, 0.65, 0.85) * dots * 0.075;
  // rayado diagonal ancho, casi imperceptible
  float diag = 0.5 + 0.5*sin((uv.x + uv.y*1.78) * 55.0);
  col += vec3(0.013, 0.017, 0.027) * smoothstep(0.6, 1.0, diag);
  // barrido de luz diagonal cada ~6 s
  float sweep = fract(t / 6.0) * 2.6 - 0.8;
  col += vec3(0.05, 0.06, 0.09) * exp(-pow((uv.x + (1.0 - uv.y)*0.6 - sweep) * 7.0, 2.0));
  return col;
}

// ── 4 · bokeh ──
vec3 bokeh(vec2 p, float t){
  vec3 col = mix(vec3(0.01,0.012,0.03), NAVY*0.18, smoothstep(-1.2, 1.2, p.y));
  for (int L = 0; L < 3; L++) {
    float fl = float(L);
    float sc = 1.6 + fl*1.4;
    vec2 q = p*sc + vec2(t*(0.10 + 0.06*fl)*(1.0 + 2.0*uWarp), fl*7.3 + sin(t*0.2 + fl)*0.2);
    vec2 id = floor(q); vec2 f = fract(q) - 0.5;
    vec2 h = hash(id + fl*13.1) * 0.5 + 0.5;
    vec2 o = (h - 0.5) * 0.45;
    float r = 0.16 + 0.18*h.x;
    float d = length(f - o);
    float soft = 0.03 + 0.05*fl;
    float disc = smoothstep(r, r - soft, d) * (0.55 + 0.45*smoothstep(r*0.3, r, d));
    float on = step(0.42, h.y);
    vec3 c = h.x < 0.34 ? GOLD : (h.x < 0.62 ? STEEL : RED*(0.35 + 0.65*uHeat));
    c = mix(c, CYAN, uCalm * step(0.34, h.x) * 0.7);
    float tw = 0.75 + 0.25*sin(t*1.3 + h.y*40.0);
    col += c * disc * on * tw * (0.42 - 0.1*fl);
  }
  return col;
}

void main(){
  // sólido: el color exacto de la landing, sin viñeta ni destellos
  if (uMode > 4.5 && uMode < 5.5) { gl_FragColor = vec4(vec3(4.0/255.0), 1.0); return; }
  vec2 p = (vUv-0.5) * vec2(uRes.x/uRes.y, 1.0) * 2.2 * uZoom;
  vec2 uvz = (vUv - 0.5) * uZoom + 0.5;
  vec3 col;
  if (uMode < 0.5)      col = liquido(p, uTime);
  else if (uMode < 1.5) col = aurora(uvz, uTime);
  else if (uMode < 2.5) col = topografico(p, uTime);
  else if (uMode < 3.5) col = carretera(uvz, uTime);
  else if (uMode < 4.5) col = bokeh(p, uTime);
  else                  col = azul(vUv, uTime);

  vec3 flashC = mix(vec3(0.45,0.10,0.10), vec3(0.10,0.35,0.45), uCalm);
  flashC = mix(flashC, GOLD*0.55, uGold);
  col += uPulse * flashC * 0.8;

  vec2 v = vUv - 0.5; col *= 1.0 - 1.15*dot(v, v);   // viñeta
  gl_FragColor = vec4(col, 1.0);
}`;

export function createBackground(canvas, mode = "liquido") {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true });
  // 540×960 internos, estirados por CSS a 1080×1920: cabe en máquinas modestas.
  renderer.setPixelRatio(1);
  renderer.setSize(540, 960, false);
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uniforms = {
    uTime: { value: 0 }, uHeat: { value: 0 }, uCalm: { value: 0 }, uPulse: { value: 0 }, uGold: { value: 0 },
    uWarp: { value: 0 }, uZoom: { value: 1 }, uMode: { value: Math.max(0, BG_MODES.indexOf(mode)) },
    uRes: { value: new THREE.Vector2(1080, 1920) },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
    fragmentShader: frag,
  });
  scene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat));

  return {
    render(time, seed = 0) {
      uniforms.uTime.value = time + seed;
      uniforms.uHeat.value = bgState.heat;
      uniforms.uCalm.value = bgState.calm;
      uniforms.uPulse.value = bgState.pulse;
      uniforms.uGold.value = bgState.gold;
      uniforms.uWarp.value = bgState.warp;
      uniforms.uZoom.value = bgState.zoom;
      renderer.render(scene, camera);
    },
  };
}
