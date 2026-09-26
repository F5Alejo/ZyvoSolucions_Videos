# RiskMann · Módulo Capacitaciones — serie de 4 anuncios (15–17 s)

Hermana de `../riskmann-capacitaciones-promo/`: misma fuente (la landing), identidad,
voz, música, efectos, logo y QR. `serie.py` **importa** las plantillas y la voz del promo
(`tools/construir.py`), así que un cambio de estilo allí llega a los cuatro al reconstruir.

| Carpeta | Idea | CTA (botón literal de la landing) |
| --- | --- | --- |
| `1-papel-vs-registro` | La lista en papel no alcanza → la plataforma guarda resultado, intentos y fecha | Quiero activar Capacitaciones |
| `2-cuatro-pasos` | Misma cuenta → los 4 pasos | Quiero empezar ahora |
| `3-certificado` | ¿Pero puedes demostrarlo? → el certificado | Quiero activar Capacitaciones |
| `4-gratis-2027` | Gratis hasta el 1-ene-2027 → ya tienes la cuenta | Activar ahora |

Estructura fija: gancho → valor → CTA (tres escenas, una frase cada una).

```bash
python serie.py voz          # solo lo que falte o cambie
python serie.py construir    # reescribe los cuatro proyectos
cd 1-papel-vs-registro && npx hyperframes preview
```

Ilustrativo (no son datos): «Colaborador 1/2/3», intentos y «dd/mm/aaaa» de la tabla del
anuncio 1; el curso «Capacitación para ciclistas» es el que muestra la landing.
