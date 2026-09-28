# RiskMann · Módulo Capacitaciones — promo vertical (39 s)

**Fuente única:** la landing `riskmann.com/capacitaciones` (captura del 26-sep-2026). Cada
frase de la voz lleva su fuente en `GUION` de `tools/construir.py` y en `tools/tiempos-voz.json`.

**Identidad: la de la landing**, no la del manual (`docs/marcas/riskmann/`), por decisión del cliente
(26-sep): negro `#040404`, dorado `#AC841D`, Montserrat + Open Sans (los `.woff2` van en
`assets/fonts/`). Logo oficial `riskmann_logo_blanco.png` sobre negro y
`riskmann_logo_color.png` sobre el certificado blanco, **sin filtros**. QR oficial
`assets/qr/qr-app-riskmann-com.svg` → `https://app.riskmann.com/entrada` (el mismo destino
que el QR del brochure).

7 escenas, una sub-composición cada una: gancho · papel y Word · armas el curso · tu gente
lo toma · califica sola + certificado · el registro + Excel · cierre (gratis hasta el
1-ene-2027, botón, QR). Fondo persistente en `compositions/fondo.html`.

```bash
python tools/construir.py voz          # Carlos, eleven_multilingual_v2, speed 1.05, semilla fija
python tools/construir.py musica       # cama y efectos (ElevenLabs sound-generation), una vez
python tools/construir.py construir    # index.html + compositions/ desde los tiempos reales
npx hyperframes preview
```

Los tiempos salen de la voz: cada escena entra 0,30 s antes de su frase y sale 0,35 s
**después** de que la frase termina (el script lo comprueba con `assert`).
`construir` reescribe `index.html` y `compositions/`.
