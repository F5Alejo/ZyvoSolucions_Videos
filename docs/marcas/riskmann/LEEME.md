# Material de marca — fuente de verdad

Los dos PDF de este directorio son **la fuente oficial** de la identidad
RiskMann. Vienen del Drive del equipo, enlazado en el issue #3:
`drive.google.com/drive/folders/1aVqnKAcIEWEn-Bvrcdb48Twe6yoSMip0`
→ carpeta «Manuales de Identidad».

Están **dentro del repo a propósito**. Antes vivían solo en Drive: se leían una
vez, sus valores se transcribían a mano al `frame.md` de un proyecto y a partir
de ahí nadie podía verificar nada sin volver a Drive. Cualquier pieza nueva se
contrasta contra estos archivos, no contra lo que hizo la pieza anterior.

## Para leerlos como imagen (recomendado)

`pdftotext` extrae las cadenas pero **pierde el diseño**: los swatches de color,
las proporciones del isotipo y los ejemplos de uso incorrecto son imágenes. Para
verlos hace falta `pdftoppm`, que este equipo no tiene todavía:

```
winget install --id oschwartz10612.Poppler -e
```

Ya instalado (`oschwartz10612.Poppler`). El binario **no queda en el PATH** que
winget anuncia; vive en:
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*\poppler-*\Libraryin`

El PDF es **una sola pagina de 2200 x 10269 pt**, asi que hay que trocearla en
bandas para leerla:

```bash
pdftoppm -png -r 70 -x 0 -y <desplazamiento> -W 2139 -H 1660 manual.pdf banda
```

## Lo que solo se ve mirando las paginas

Esto no lo da `pdftotext` y es justo lo que define el aire de la marca:

- **El caballero es fotografia real**, no ilustracion: cota de malla, yelmo,
  espada y escudo, en monocromo casi negro, iluminacion baja y dramatica.
- Alrededor del caballero hay **dos anillos concentricos**: uno grueso en cian
  `#06c7fb` y otro fino en dorado `#c8951a`. Es un motivo propio de la marca,
  una lente o portal que enmarca al sujeto.
- **La tipografia mezcla pesos dentro de una misma frase**: Bold en las palabras
  que cargan el mensaje y Light en los conectores.
  «RiskMann **es una** solucion digital **para gestionar** riesgos **de forma**
  simple, segura **y** conforme **a la** normativa.»
  Es un recurso de enfasis de la marca, no una licencia tipografica.
- El lockup del logo lleva **«by SOFU»** bajo el nombre.

## Lo que fija el manual

**Paleta general**

| Hex | Uso que indica el manual |
| --- | --- |
| `#020202` | Fondo principal |
| `#c8951a` | Toques de prestigio y detalles |
| `#06c7fb` | Detalles decorativos, gráficos acento |
| `#272725` | Separadores, fondos secundarios |

**Paleta del isotipo**

| Hex | Uso que indica el manual |
| --- | --- |
| `#333366` | Círculos del isotipo, elementos tecnológicos |
| `#FF3333` | Énfasis, alertas, botones |
| `#26367D` | Color institucional secundario o de soporte |
| `#FFFFFF` | Contraste, espacios negativos |

**Tipografía:** Dubai Bold para títulos, Dubai Regular para cuerpo.

**Estilo visual declarado** — esto no es decoración, es la dirección creativa
que el manual pide y que la v1 no usó:

> «Inspirado en las figuras de los caballeros medievales, transmiten una imagen
> de defensa, integridad y compromiso frente a los riesgos empresariales.»

- El caballero = el rol protector de la marca: firme, preparado y ético.
- Azul oscuro = profesionalismo y confianza · Negro = elegancia y autoridad ·
  Gris claro = neutralidad · Dorado = prestigio y valor.
- Fotografía e ilustración: **escudos, armaduras, metáforas de protección y
  estrategia**.
- Diseño: limpio, ordenado, con énfasis en estructuras sólidas.

**Reglas duras del isotipo** (el manual las ilustra como usos incorrectos):
área de reserva libre alrededor, no deformar, no recolorear, no aplicar
opacidad, no girar, no ocultar, no poner nada encima, no reinterpretarlo.
Solo se usa el archivo oficial.

## Advertencia sobre `riskmann-hud`

La receta congelada `riskmann-hud`, que heredan los proyectos nuevos según
`CLAUDE.md`, **no corresponde a este manual**. Se detectó al producir
`riskmann-consulta-pesv-vertical` y esa pieza se construyó contra el manual, no
contra la receta. Está sin resolver: o se corrige la receta, o se deja de
recomendar en el arranque de proyectos nuevos.
