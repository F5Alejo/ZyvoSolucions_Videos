# Hallazgos: lo aprendido para no repetirlo

Problemas reales que aparecieron al construir el estudio, su causa y cómo se resolvieron. El detalle
de cada uno, con su fecha, está en la [bitácora](bitacora.md).

## Audio y voz

| Problema | Causa | Solución |
|---|---|---|
| El volumen quedaba en -15,2 LUFS en vez de -14 | `loudnorm` en modo `linear` pasa a modo dinámico cuando la ganancia choca con el límite de picos, y se queda corto | Ganancia lineal más `alimiter` a -2 dBFS, repitiendo hasta quedar a ±0,3 LUFS (`motor/audio.py`) |
| El MP4 sonaba ~3 dB más fuerte que la pista medida | Duplicar un canal mono en estéreo suma ~3 dB a la sonoridad | Se pasa a estéreo **antes** de medir y normalizar |
| La voz Piper davefx parecía libre | Sus datos en español son CC0, pero se afinó a partir de `en_US-lessac`, cuya licencia (Blizzard 2013) prohíbe el uso comercial | Piper queda **solo para borradores** (sello «BORRADOR»); la voz gratuita para entregar es Kokoro (Apache 2.0). Revisar con el cliente el módulo PESV M01 |
| La voz leía mal cifras, leyes y siglas | Los modelos de voz no saben leer «Ley 1503 de 2011», «30 %» o «SMMLV» | `motor/normalizar.py` las pasa a palabras con las convenciones de Colombia (punto para miles, coma para decimales) |
| El Revisor de voz daba un falso 73 % | Whisper escribe «1503» y el guion dice «mil quinientos tres» | La transcripción pasa por la misma normalización antes de comparar |
| faster-whisper fallaba al leer el MP4 | Incompatibilidad con la versión de PyAV («unexpected keyword argument 'metadata_errors'») | El audio se decodifica con ffmpeg (16 kHz, mono) y se pasa como muestras |

## Render y escenas

| Problema | Causa | Solución |
|---|---|---|
| Subtítulos quemados fallaban en Windows | El filtro `subtitles` de ffmpeg no acepta bien rutas con «C:» | Se trabaja con archivos copiados a una carpeta temporal y rutas relativas (`cwd`) |
| La salida de una animación pisaba la entrada | Con dos animaciones `both` en el mismo elemento, la salida aplicaba su estado antes de tiempo | Entrada con `fill-mode: both` y salida con `forwards` |
| El fondo y el logo parpadeaban entre láminas | Entraban y salían en cada escena | Solo entran en la primera escena del video y solo salen en la última |
| Un render de 40 s de lámina sería lento | Dibujar cada cuadro con Chromium es caro | Se dibujan cuadro a cuadro solo la entrada y la salida; ffmpeg sostiene lo del medio |
| «Pantalla negra» en una lámina oscura con poco texto | `blackdetect` cuenta como negro un cuadro con más del 98 % de píxeles oscuros, y el fondo de RiskMann es #020202 | `pic_th=0.999`: solo un cuadro negro entero cuenta |
| La plantilla vertical dejaba el texto arriba y angosto | En columna, `.texto` con `flex: 1` crece hacia abajo y `align-items: center` lo encoge | En vertical, `.texto` sin `flex` y a todo el ancho; `.cuerpo` con `align-items: stretch` |
| Un zoom centrado recortaba la barra de avance | El zoom corta lo mismo arriba que abajo | La cámara mantiene fijo el borde de abajo (`y=ih-ih/zoom`) |
| Un enlace duro habría cambiado las versiones viejas | ffmpeg escribía el MP4 nuevo encima del mismo archivo | El MP4 se arma en `tmp/` y reemplaza al anterior con `replace` |
| El título repetido en la portada | El video toma su nombre de la primera lámina | La portada usa el nombre del curso como antetítulo |

## Interfaz (Vue)

| Problema | Causa | Solución |
|---|---|---|
| «#<Object> could not be cloned» | `structuredClone` no copia los objetos reactivos de Vue (Proxy) | `clonar()` por JSON en `frontend/src/utils.ts` |
| La vista previa no cargaba la fuente | El iframe aislado (`sandbox`) tiene origen «null» y el navegador bloquea la fuente por CORS | La ruta de la fuente (pública, OFL) responde `Access-Control-Allow-Origin: *` |
| La tarjeta del video salía angosta | Una regla CSS posterior con la misma especificidad la pisaba | Más especificidad (`.videos-plan.salida-videos`). Hoy la interfaz es Tailwind |
| Escalar el iframe con CSS no era confiable | Dividir unidades (`100cqw / 1920px`) no lo soportan todos los navegadores | `ResizeObserver` calcula la escala |
| Aviso de paquete obsoleto | `lucide-vue-next` está obsoleto | Se migró a `@lucide/vue` |
| Las miniaturas de los estilos salían vacías | Un `height` en % dentro de una grilla con filas automáticas da 0 | Alturas con `padding-top` en %, que va contra el ancho |
| Los subtítulos se veían dos veces | Quemados en la imagen y la pista VTT activa por defecto en `<video>` | La pista `<track>` sin `default` |

## Agentes e IA local

| Problema | Causa | Solución |
|---|---|---|
| El Redactor tardaba 79 s en 2 láminas | Con `keep_alive: 0`, Ollama recargaba el modelo en cada pregunta | El modelo queda cargado 2 min mientras trabaja el agente y se descarga al terminar (`ollama.descargar`) |
| Un modelo pequeño puede inventar cifras | Al «mejorar» un texto cambia un 30 % por un 40 % | `motor/agentes/guardas.py` descarta toda propuesta con cifras o normas que no están en la lámina |
| La guarda contaba dos veces la misma cifra | La marcaba como cifra y como norma | Una norma solo se marca si sus números ya estaban pero cambió su nombre («Decreto 1503» donde decía «Ley 1503») |
| No caben un render y un modelo a la vez | 8 GB de RAM: Chromium más un modelo de 4 B | Agentes y renders comparten una sola cola |

## Git, instalación y CI

| Problema | Causa | Solución |
|---|---|---|
| `main` ya no tenía ancestro común con la rama | El commit inicial fue reescrito con un *force push* | `git rebase --onto <nuevo> <viejo>` antes de unir |
| `instalar.ps1` con tildes dañadas | Windows PowerShell 5.1 lee como ANSI un archivo sin BOM | Se guarda en UTF-8 **con BOM** |
| `instalar.ps1` quedó con `\r\r\n` | Una conversión doble de saltos de línea | Se corrigió, y `.gitattributes` fija `*.ps1` en CRLF |
| Scripts largos en línea fallaban en Bash | «unexpected EOF» con muchas comillas mezcladas | Los scripts largos se guardan en un archivo temporal y se ejecutan desde ahí |
| Tildes dañadas al probar con Playwright desde la terminal | La codificación de los argumentos en Git Bash | Buscar por valores sin tilde (`input[value=cinetica]`) |
| Actions se colgó 20 min instalando ffmpeg | `apt-get` esperando un mirror | ffmpeg estático de johnvansickle.com; `apt` solo de respaldo con tiempo límite |
| Aviso de Node 20 obsoleto en Actions | Las acciones en v4 corren en Node 20 | `checkout`, `setup-python` y `setup-node` en v7, `cache` en v6 y `upload-artifact` en v7 |
| `ubuntu-latest` cambia a Ubuntu 26 el 19-oct-2026 | Una imagen que cambia sola puede romper las pruebas sin aviso | `runs-on: ubuntu-24.04` fijo; se sube a mano cuando se pruebe |
| Aviso de Starlette en las pruebas | Su cliente de pruebas con `httpx` está obsoleto | Se instala `httpx2`, que Starlette usa si está (`import httpx2 as httpx`) |
| Dependabot abría un PR por paquete de pip | Subía el mínimo (`>=`) aunque el rango ya admitía la versión nueva | `versioning-strategy: increase-if-necessary` |
| Los PR de Dependabot no se probaban | «Pruebas» solo se activaba con PR hacia `main` | También con PR hacia `Alejodev` |
| TypeScript 7 rompe `vue-tsc` | `ERR_PACKAGE_PATH_NOT_EXPORTED` (`./lib/tsc`) | Dependabot ignora las versiones mayores de TypeScript hasta que `vue-tsc` las soporte |
| El servidor local se apagaba solo | Las tareas en segundo plano del asistente tienen un tiempo máximo | El servidor se lanza en su propia ventana de PowerShell |
| `instalar.ps1` se quedaba esperando la clave sin ventana | `Read-Host` no falla cuando no hay quien escriba: espera para siempre | Solo pregunta si la sesión es interactiva y la entrada no está redirigida |
| Un commit dejó Actions en rojo tras mover un fixture | Se quitó `ORIGEN` de `test_motor.py`, que importan otras pruebas, y solo se corrió un subconjunto | Correr **todas** las pruebas después del último cambio |

## Despliegue

| Hallazgo | Por qué importa |
|---|---|
| **Vercel no puede correr el motor**: funciones de ~250 MB, disco de solo lectura, tiempo límite y sin tareas en segundo plano | Vercel sirve solo para la interfaz; el motor necesita un servidor con disco y CPU. Ver [`plan-nube.md`](plan-nube.md) |
| Vercel Hobby no permite uso comercial | Para un servicio con clientes: Vercel Pro, Cloudflare Pages o servir la interfaz desde la API |
| Las pruebas no necesitan claves | Usan una voz de prueba y Ollama simulado, así que la clave de ElevenLabs no va a los *secrets* de GitHub |
