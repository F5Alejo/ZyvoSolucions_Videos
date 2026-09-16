---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "Descubre en 1 minuto si tu empresa está obligada a implementar el PESV — RiskMann te lo dice gratis"
angle: "Invitación a consulta gratuita: la duda del PESV resuelta en un formulario"
destination: social
aspect: "16:9"
format: 1920x1080
length: 45
language: es
audience: "Gerencia / HSEQ de empresas con flota de vehículos o conductores a cargo, que no saben si el PESV les aplica"
style_preset: riskmann-manual-oficial
capture: https://riskmann.com/consulta-pesv/
---

## Intent

Video de marketing para A/B testing en redes sociales de RiskMann (issue
JTFernandez/riskmann2-marketing-videos#3, ref. AR-2026-09-15-10-00-AM). Invita a las
empresas colombianas a consultar gratis si el PESV (Plan Estratégico de Seguridad Vial)
les aplica. Tono: urgencia informativa, no alarmista — la empresa puede no saberlo y
exponerse a sanción sin culpa. Cierre en la consulta gratuita, no en la venta directa de
la plataforma.

## Assets

- assets/public/riskmann_logo_blanco.png — logo oficial, único archivo permitido para el
  lockup completo en el cierre de marca.
- assets/public/riskmann_icono_blanco.png — isotipo oficial, para usos reducidos.
- assets/fonts/DUBAI-REGULAR.TTF, DUBAI-BOLD.TTF, DUBAI-MEDIUM.TTF, DUBAI-LIGHT.TTF —
  tipografía oficial de marca según el manual real, copiada desde las fuentes del sistema
  (C:\Windows\Fonts\). Reemplaza a Montserrat, que no está en el manual.
- capture/ — captura real de https://riskmann.com/consulta-pesv/ (copia, cifras, CTAs).
  Usar SOLO como fuente de contenido/texto, nunca de estilo visual (ver Notes).
- assets/graficas.mp4, assets/estadisticas.mp4 — grabaciones reales de UI de la
  plataforma (mismas usadas en riskmann-sala-de-control), para los planos de
  feature_showcase de automatización/ahorro de tiempo. La landing capturada no trae
  screenshots de producto (es una página de captación de leads, no la app).
- assets/seguridad_vial_icono_conductores.webp, _vehiculos.webp, _mantenimientos.webp,
  _siniestralidad_vial.webp, assets/inicio_icono_seguridad_vial.webp — iconos oficiales
  del módulo Seguridad Vial (el módulo real de la plataforma bajo el que vive el PESV).
- assets/riskmann_logo_blanco.png, assets/riskmann_icono_blanco.png — copias planas de
  los archivos oficiales de logo, listas para referenciar en HTML.

## Customizations

- Ritmo de revelado de texto autosuficiente sin narración: cada cue de texto en pantalla
  debe comunicar el beat completo por sí solo, porque el video se entrega en 3 mezclas de
  audio (ver Notes) y dos de ellas no llevan voz.

## Notes

- **Identidad: manual oficial, NO el recipe `riskmann-hud`.** Verificado el 2026-09-16
  contra `RiskMann Manual-de-identidad.pdf` y su versión Modo Oscuro (Google Drive →
  RiskMann-by-SOFU → Manuales de Identidad): el recipe `riskmann-hud` que usa el resto de
  la serie (Montserrat, `bg` #051427 azul marino, `primary` #E6423C rojo, `accent-2`
  #8E8FC4 lavanda) **no corresponde al manual real**. El manual documenta Dubai
  (Bold/Regular) y la paleta `#020202` / `#FF3333` / `#333366` / `#26367D` / `#336699` /
  `#c8951a` / `#06c7fb` / `#999999`. Por instrucción explícita del cliente, este proyecto
  usa un `frame.md` bespoke construido desde cero con esos valores reales (ver
  `frame.md` → "Nota de origen" para la tabla completa hex → rol). La discrepancia en los
  videos anteriores de la serie queda reportada aparte, sin corregir retroactivamente
  aquí. La landing capturada usa además su propio Inter/#5C8AFF — tampoco se usa para
  diseño, solo como fuente de contenido/texto (ver `capture/extracted/tokens.json`).
  Fuentes Dubai (.ttf) ya copiadas a `assets/fonts/` desde el sistema (Windows las trae
  instaladas junto con Office).
- **Trazabilidad estricta.** Ninguna cifra o afirmación entra si no está literal en
  `capture/extracted/visible-text.txt`. Cifras ya verificadas ahí: 11+ vehículos o 2+
  conductores obligan (art. 12 Ley 1503 de 2011, mod. Ley 2050 de 2020); 24 pasos del
  ciclo PESV (Resolución 20223040040595 de 2022), niveles Básica 18-20 / Estándar 22 /
  Avanzada 24; multa hasta 500 SMMLV (~$650.000.000 COP, Ley 1562 de 2012); auditoría
  interna mínima 1 vez/año; RiskMann reduce hasta 70% el tiempo de gestión documental.
  CTAs reales de la página: "Consultar ahora", "Valida si te aplica el PESV", "Descubre si
  te aplica el PESV". No usar ninguna cifra o frase que no esté en ese archivo.
- **Sin figuras humanas dibujadas** (manual de marca §0.2) — solo fotografía real si se
  necesita gente en pantalla, o ninguna.
- **Logo solo con archivo oficial**, nunca redibujado ni re-letrado (§0.1).
- **Estructura BAB reducida de 6 planos, ~45s, planos de 7-8s** (PRODUCCION-VIDEOS.md
  §3.1): hook (duda concreta) → product_intro (se arma el logo, se nombra RiskMann) →
  feature_showcase x2 (automatización de tareas / ahorro de tiempo, con las cifras reales)
  → benefit_highlight (qué cambia, solo frases aprobadas) → branding (logo, cierre). El
  motivo estructural de panel es `panel-frame` (marcas de esquina, ver frame.md), no la
  retícula HUD del recipe anterior.
- **Entrega final en 3 mezclas de audio** (particularidad de este video, se resuelve
  DESPUÉS de este workflow con `tools/mezcla.py`, fuera del alcance de esta skill): A) voz
  ElevenLabs + SFX + música, B) SFX + música sin voz, C) solo música. Para este workflow:
  generar SCRIPT.md y narración asumiendo que la Versión A (completa) es la referencia.
- Zona libre inferior 17%, densidad ≥40% del elemento principal, curvas `power3` sin
  rebote (§5 reglas técnicas duras).
