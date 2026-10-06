# Pruebas

```sh
python -m pytest                 # 117 pruebas: API, motor, agentes y videos reales (~3,5 min)
cd frontend && npm run typecheck # tipos de TypeScript
cd frontend && npm test          # Vitest: utilidades, flujo /crear y componentes (18)
ruff check .                     # estilo de Python
```

Las pruebas de video necesitan **ffmpeg** y **Chromium** (`python -m playwright install chromium`);
sin ellos se saltan. No necesitan claves ni modelos: usan una voz de prueba (un tono con la duración
que tendría la frase) y Ollama simulado.

## Por niveles

| Nivel | Archivos | Qué cubre |
|---|---|---|
| Unidad | `test_videospec.py`, `test_robustez.py`, `test_proveedores.py`, `test_animaciones.py`, `test_configuracion.py` | Contrato y validación del VideoSpec, errores, reintentos, permisos de agentes, catálogos, configuración |
| Integración | `test_analisis.py`, `test_escena.py`, `test_estilos_audio.py`, `test_versiones.py`, `test_agentes.py`, `test_taller.py` | PPTX → análisis, cámara y formatos, estilos, música y efectos, versiones y regeneración selectiva |
| Punta a punta | `test_e2e.py`, `test_motor.py` | Un PPTX con de todo → MP4 válidos, completo con capítulos y ZIP, por la API y la cola |

## Los PPTX de prueba

`tests/fixtures/` (simple, images, tables, long_text, notes, empty_slide, mixed_content) se generan
con `python scripts/generar_fixtures.py`: son reproducibles y no traen material de clientes. Si cambia
el script, se vuelven a generar y se suben con el cambio.

## Regla de no regresión

Antes y después de tocar el motor: **todas** las pruebas. Si algo que funcionaba se rompe, se arregla
eso antes de seguir. (Una vez se corrió solo una parte después del último cambio y Actions quedó en
rojo: ver `hallazgos.md`.) GitHub Actions corre todo en cada push a `develop` y `main`, y en todos los pull request.
