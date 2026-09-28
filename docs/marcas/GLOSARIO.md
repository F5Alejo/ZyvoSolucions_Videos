# Glosario

> Términos del negocio y de la producción que aparecen en el repositorio. Si una palabra
> se usa en dos sentidos, aquí se dice cuál es cuál. Añadir en orden alfabético.

## Del negocio

| Término | Significado | Fuente / nota |
| --- | --- | --- |
| **BIC** | Sociedad de Beneficio e Interés Colectivo (figura jurídica colombiana) | SOFU es «empresa BIC» (guion de SOFU) |
| **En Vivo** | Conversatorio en línea y gratuito del Dr. Yezid Ricaurte; el del PESV es el sábado 3 de octubre a las 10:00 a. m. | Página del evento en `yezidricaurte.com` |
| **Informe de autogestión** | Informe del PESV que se reporta; el En Vivo enseña a generarlo «con un solo clic» | Copy de la campaña del En Vivo |
| **PESV** | Plan Estratégico de Seguridad Vial | En locución se deletrea: `P-E-S-V` o «pe e ese ve» |
| **Resolución 20223040040595 de 2022** | Norma citada en la landing de inspecciones (paso 16) | `riskmann.com/inspecciones-gratis/` |
| **SMMLV** | Salario mínimo mensual legal vigente | Aparece en cifras de sanciones («500 SMMLV») |
| **SST** | Seguridad y Salud en el Trabajo | Servicio de SOFU |
| **Umbral de vehículos** | A partir de cuántos vehículos se exige el PESV. ⚠ La landing dice 11 y también 10 | PLAYBOOK §9 |

## De la producción

| Término | Significado |
| --- | --- |
| **Composición** | Un archivo HTML de HyperFrames con su timeline; `index.html` es la raíz y `compositions/` guarda las subcomposiciones |
| **Curso generado** | Curso producido por plantillas a partir de `curso.json` (moto, csm) |
| **Determinismo** | El render busca cada fotograma por tiempo y siempre da lo mismo: sin `Math.random`, `Date.now` ni `repeat:-1` |
| **Ducking** | Bajar la música automáticamente cuando habla la voz (`musica` en `mezcla.py`) |
| **Familia A / B** | A: cursos generados por plantillas. B: piezas de marketing a medida (`PLATAFORMA.md` §3.1) |
| **Ficha de marca** | Documento por marca en `docs/marcas/<marca>/ficha.md` |
| **Hoja de contactos** | Imagen con varios fotogramas del video para revisarlo sin verlo entero |
| **HyperFrames** | Framework de HeyGen que convierte HTML + GSAP en MP4; el motor principal del repo |
| **Lienzo propio** | Piezas hechas en HTML + GSAP + Three.js con su propio `render.mjs` (puppeteer), sin HyperFrames |
| **LUFS** | Medida de volumen percibido; −14 LUFS para redes, −16 en los módulos |
| **Muestra** | Los primeros ~15 s con sonido, para aprobar la dirección antes de producir todo |
| **Receta** (`riskmann-hud`) | Identidad visual congelada para reutilizar; ⚠ la de RiskMann no coincide con el manual |
| **Studio** | Editor visual de HyperFrames (`npx hyperframes preview`) |
| **Tiempo muerto** | Tramo en que la imagen casi no cambia; se mide con diferencia entre fotogramas (PLAYBOOK §6.4) |
| **Variante A/B/C** | Versiones de audio de una misma pieza (A: voz + efectos + música) |
