# Plan de nube: llevar el estudio a un servicio escalable

> **Estado (2026-10-01): siguiente etapa, todavía no se ejecuta.** Primero se terminó GitHub Actions
> (pruebas, estilo, secretos, Dependabot, instalador en Windows y protección de `main`). Este plan
> se retoma cuando el usuario lo indique.

Decisiones del usuario: **primero el equipo, después SaaS** (la arquitectura queda pensada para
clientes externos), y **la prueba se monta con todo gratis**. Para cómo funciona hoy, ver
[`arquitectura-anterior.md`](arquitectura-anterior.md).

## 1. ¿Sirve tal como está para dar el servicio?

**Para el equipo en un solo servidor:** casi. Le faltan HTTPS, inicio de sesión y copias de
seguridad, y se resuelven sin tocar el código (Fase 1).

**Para clientes externos (SaaS): no.**

| Hoy | Problema para un servicio |
|---|---|
| Datos en JSON escritos sin bloqueo | Dos personas guardando a la vez pueden pisarse |
| Cola en memoria (`motor/cola.py`, un hilo) | Se pierde al reiniciar; un solo worker que comparte la máquina con la API |
| Videos, PPTX y caché en el disco local | No escala a varias máquinas; las copias de seguridad son manuales |
| Sin usuarios | Cualquiera con la URL ve el material de clientes y gasta los créditos de ElevenLabs |
| Marcas globales | No hay separación por empresa |
| Una sola clave de ElevenLabs, sin medir el consumo | No hay cuotas ni cobro por uso |
| Ollama en el mismo equipo | Un modelo de 4 B más Chromium no caben juntos en 8 GB |

**Capacidad:** un worker de 4 vCPU produce unos 15 a 20 minutos de video por hora (render de
~1,5 a 2 veces la duración, de a uno).

## 2. Arquitectura objetivo: cuatro piezas

| Pieza | Qué es | Dónde puede correr |
|---|---|---|
| `frontend` | Vue compilado (estático) | Lo sirve la API, o una CDN (Cloudflare Pages, Vercel) |
| `api` | FastAPI liviana: recibe, guarda, encola y responde. **No renderiza** | Cualquier contenedor pequeño |
| `worker-motor` | ffmpeg, Chromium y Kokoro: produce los videos | El servidor; más servidores para crecer |
| `worker-ia` | Ollama y Whisper: los agentes | El PC del equipo con GPU, o una GPU en la nube |

```
Navegador ──HTTPS──> Caddy ──> api ──> PostgreSQL
                                │  └─> almacenamiento S3 (Cloudflare R2)
                                └─ encola ──> Redis
                                               ▲  (los workers PIDEN trabajo: conexión de salida, sin túnel)
                        worker-motor ──────────┤
                        worker-ia (PC con GPU, por Tailscale)
```

- **La clave para escalar:** los workers *piden* trabajo a la cola. El motor puede correr en
  cualquier máquina que llegue a Redis, PostgreSQL y R2, **sin túnel ni puertos abiertos**. Para
  crecer, se encienden más workers.
- **El túnel** (Cloudflare Tunnel) queda solo para demostraciones rápidas desde el PC.
- **Mismo repositorio, cuatro imágenes Docker.** El primer paso hacia la nube es que GitHub Actions
  construya y publique esas imágenes en GHCR.

## 3. Herramientas

| Necesidad | Herramienta | Costo para la prueba |
|---|---|---|
| Servidor | **Oracle Cloud Always Free**: VM ARM de hasta 4 OCPU y 24 GB | 0 |
| Despliegue | **Docker Compose** y **Caddy** (HTTPS automático) | 0 |
| Cola | **Redis** con **RQ** (reemplaza el hilo de `motor/cola.py` con la misma interfaz `encolar` y `estado`) | 0 |
| Base de datos | **PostgreSQL** con SQLAlchemy y Alembic (en la VM; o Neon/Supabase gratis) | 0 |
| Archivos | **Cloudflare R2** (10 GB gratis, sin costo por descarga) | 0 |
| Dominio | **DuckDNS** (subdominio gratis) o un dominio propio en Cloudflare | 0 |
| Acceso del equipo | **Cloudflare Access** (gratis hasta 50 usuarios) | 0 |
| Red privada (PC con GPU como worker de IA) | **Tailscale** | 0 |
| Errores y caídas | **Sentry** (capa gratuita) y **Uptime Kuma** | 0 |
| CI/CD | **GitHub Actions** con **GHCR** (ya existe el flujo de pruebas) | 0 |
| Copias | `pg_dump` cada noche a R2 | 0 |

**No sirven para el motor** (poca RAM o se duermen): las capas gratuitas de Render, Koyeb, Railway
y Fly, y las funciones de Vercel.

## 4. Fases

**Fase 1a. Prueba 100 % gratis**
1. Crear la cuenta de Oracle Cloud (pide tarjeta solo para verificar) y la VM ARM. Si no hay cupo en la región, reintentar o cambiar de región.
2. Instalar Docker y Compose; escribir `Dockerfile` y `docker-compose.yml` (caddy, api, worker, redis, postgres).
3. Configurar el subdominio en DuckDNS, el HTTPS con Caddy y Cloudflare Access delante.
4. Copias nocturnas a R2.
5. Entornos: `main` en producción y `develop` en pruebas (otro subdominio), con despliegue desde Actions.

**Fase 1b. Servidor pagado** (≤ 30 USD al mes, cuando la prueba funcione): Hetzner CPX31 o
similar, con la misma configuración.

**Fase 2. Listo para SaaS** (cambios de código en ramas `feature/*` hacia `develop`)
1. Redis con RQ y un worker en un proceso aparte; la API ya no renderiza.
2. PostgreSQL: organizaciones, usuarios, cursos, videos, trabajos, propuestas y configuración por empresa; migrar los JSON.
3. Capa de almacenamiento (disco local o R2) con enlaces firmados.
4. Inicio de sesión con empresas y roles (Supabase Auth, Clerk o uno propio). Las marcas y las claves de ElevenLabs pasan a ser de cada empresa, cifradas.
5. Medir minutos de video y caracteres de voz por empresa, con cuotas.
6. Proveedor de IA configurable: Ollama propio o una API externa **con política de no entrenar con los datos** y acuerdo de tratamiento.

**Fase 3. Escalar:** más workers (otro servidor, o Fly Machines, Cloud Run Jobs o Modal por
trabajo), GPU por segundos para IA y Whisper, interfaz en una CDN, y cobro (Stripe, Wompi o Mercado Pago).

## 5. Lo que GitHub Actions no puede probar

En Actions no hay GPU, ni 8 GB libres, ni claves:
- Ollama con modelos reales;
- ElevenLabs real;
- el rendimiento real.

Se cubren con las pruebas simuladas (voz de prueba y Ollama simulado) y con una **prueba de humo
manual** en el equipo o en el servidor después de cada despliegue.

## 6. Decisiones pendientes

- El dominio (DuckDNS gratis o uno propio).
- El proveedor de IA para clientes externos.
- Supabase Auth, Clerk o un inicio de sesión propio.
- La pasarela de pago.
- La región del servidor (latencia desde Colombia frente a cupo disponible).
