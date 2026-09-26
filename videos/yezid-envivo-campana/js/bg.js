// Fondo Three.js — «mesh gradient» líquido y orgánico: seis puntos de color que derivan
// sobre un campo deformado con ruido, mezclados por distancia inversa (así se construye un
// mesh gradient), con la paleta de la campaña. No hay reloj propio: render(t) recibe el
// tiempo del timeline de GSAP, así que el mismo fotograma sale igual en preview y en render.
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

export const BG_MODES = ["malla"];

// Lo que animan los timelines:
//   energia → el verde FEGIR gana espacio y el líquido corre más (urgencia)
//   pulso   → destello amarillo pálido en los golpes (cifra, fecha, botón)
//   coral   → tiñe el destello con el coral del botón del correo (solo en el CTA)
//   warp    → cuánto se retuerce el líquido
//   zoom    → respiración de cámara
export const bgState = { energia: 0, pulso: 0, coral: 0, warp: 0, zoom: 1 };

const frag = /* glsl */ `
precision highp float;
uniform float uTime, uEnergia, uPulso, uCoral, uWarp, uZoom;
varying vec2 vUv;

const vec3 PETROLEO = vec3(0.000, 0.122, 0.149);   // #001f26  correo
const vec3 PROFUNDO = vec3(0.086, 0.188, 0.184);   // #16302f  pieza aprobada
const vec3 VERDE    = vec3(0.200, 0.400, 0.400);   // #336666  manual
const vec3 FEGIR    = vec3(0.271, 0.627, 0.208);   // #45a035  brief
const vec3 PALIDO   = vec3(0.945, 0.925, 0.690);   // #f1ecb0  brief
const vec3 OLIVA    = vec3(0.502, 0.502, 0.290);   // #80804a  manual
const vec3 CORAL    = vec3(0.941, 0.431, 0.286);   // #f06e49  botón del correo

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
float fbm(vec2 p){ float f=0.0, a=0.5; mat2 r=mat2(1.6,1.2,-1.2,1.6); for(int i=0;i<4;i++){ f+=a*noise(p); p=r*p; a*=0.5; } return f; }

// punto de color que deriva en una curva de Lissajous
vec2 pt(float t, float ax, float ay, float fx, float fy, float ph){ return vec2(0.5 + ax*sin(t*fx + ph), 0.5 + ay*cos(t*fy + ph*1.3)); }

void main(){
  float t = uTime * (0.16 + 0.22*uEnergia);
  vec2 uv = (vUv - 0.5) * uZoom + 0.5;
  // deformación líquida del espacio antes de mezclar
  vec2 q = uv * vec2(1.0, 1.78);
  vec2 w = vec2(fbm(q*1.3 + vec2(0.0, t*0.6)), fbm(q*1.3 + vec2(4.1, -t*0.5)));
  uv += (0.10 + 0.10*uWarp) * w;

  vec2 P[6]; vec3 C[6];
  P[0] = pt(t, 0.38, 0.30, 0.50, 0.40, 0.0);  C[0] = PROFUNDO;
  P[1] = pt(t, 0.42, 0.38, 0.37, 0.53, 2.1);  C[1] = VERDE;
  P[2] = pt(t, 0.30, 0.42, 0.61, 0.33, 4.2);  C[2] = mix(VERDE, FEGIR, 0.35 + 0.55*uEnergia);
  P[3] = pt(t, 0.44, 0.26, 0.29, 0.47, 1.1);  C[3] = PETROLEO;
  P[4] = pt(t, 0.35, 0.40, 0.43, 0.59, 3.3);  C[4] = mix(OLIVA, FEGIR, 0.3 + 0.4*uEnergia) * 0.8;
  P[5] = pt(t, 0.40, 0.34, 0.55, 0.31, 5.0);  C[5] = PETROLEO;

  vec3 acc = vec3(0.0); float ws = 0.0;
  for (int i = 0; i < 6; i++) {
    vec2 d = (uv - P[i]) * vec2(1.0, 1.78);
    float wi = 1.0 / pow(dot(d, d) + 0.02, 1.6);
    acc += C[i] * wi; ws += wi;
  }
  vec3 col = acc / ws;

  // destellos sutiles en amarillo pálido donde el líquido «brilla»
  float brillo = smoothstep(0.35, 0.75, fbm(q*2.2 + w*1.5 + t*0.3));
  col += PALIDO * brillo * 0.07;
  // mantiene todo oscuro: el texto blanco y el pálido siempre ganan contraste
  col *= 0.62 + 0.18*uEnergia;
  // destello de golpe
  col += mix(PALIDO, CORAL, uCoral) * uPulso * 0.28;

  vec2 v = vUv - 0.5; col *= 1.0 - 1.05*dot(v, v);   // viñeta
  gl_FragColor = vec4(col, 1.0);
}`;

export function createBackground(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(540, 960, false);   // se estira por CSS a 1080×1920: el gradiente es suave
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uniforms = { uTime: { value: 0 }, uEnergia: { value: 0 }, uPulso: { value: 0 }, uCoral: { value: 0 },
                     uWarp: { value: 0 }, uZoom: { value: 1 } };
  const mat = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
    fragmentShader: frag,
  });
  scene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat));
  return {
    render(time, seed = 0) {
      uniforms.uTime.value = time + seed;
      uniforms.uEnergia.value = bgState.energia;
      uniforms.uPulso.value = bgState.pulso;
      uniforms.uCoral.value = bgState.coral;
      uniforms.uWarp.value = bgState.warp;
      uniforms.uZoom.value = bgState.zoom;
      renderer.render(scene, camera);
    },
  };
}
