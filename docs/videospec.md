# VideoSpec: el plano de un video

El VideoSpec describe **un video** con datos: qué escenas tiene, qué dice la voz en cada una, cómo
entra y sale cada elemento, qué cámara y qué transición usa y con qué formato y audio se entrega.
El render solo lee el VideoSpec. La IA nunca escribe código de video: a lo sumo propone valores
que luego se validan contra el catálogo.

Código: [`motor/videospec.py`](../motor/videospec.py). Catálogos: [`motor/catalogo.py`](../motor/catalogo.py)
(cámara y transiciones) y [`motor/escenas/efectos.py`](../motor/escenas/efectos.py) (animaciones).

## Dos momentos

| Archivo | Lo escribe | Qué tiene |
|---|---|---|
| `salida/<clave>/videospec.plan.json` | `videospec.construir()` | El plan: escenas, narración, animación, ajustes. Duraciones **estimadas**. Tarda segundos |
| `salida/<clave>/videospec.json` | `videospec.resolver()` | El mismo plan con el audio de cada frase y cada escena en **cuadros exactos** |

La duración depende de la voz y no se sabe hasta generarla: por eso hay dos.

## Forma (versión 1)

```json
{
  "version": 1,
  "trabajo": "seguridad-vial-a1b2c3", "clave": "v01", "titulo": "Riesgo vial", "curso": "Seguridad vial",
  "marca": "riskmann", "firma": "9f2c…",
  "voz": {"id": "kokoro-dora", "nombre": "Dora · Kokoro", "proveedor": "Kokoro", "solo_borrador": false},
  "video": {"formato": "16:9", "ancho": 1920, "alto": 1080, "escala": 1.0, "fps": 30,
            "crf": "18", "preset": "medium", "subtitulos_quemados": false},
  "audio": {"lufs": -14, "musica": null, "musica_volumen": -22},
  "tiempos": {"entrada": 1.0, "pausa": 0.35, "salida": 1.3},
  "estilo": {"fondo": "#020202", "acento": "#C8951A", "…": "…"},
  "escenas": [{
    "id": "escena-001", "lamina": 1, "indice": 0,
    "vista": {"tipo": "portada", "titulo": "Riesgo vial", "vinetas": ["…"], "imagen": null},
    "animacion": {"plantilla": "dinamica", "elementos": {"titulo": {"entrada": {…}, "salida": {…}}}},
    "entrada": 1.1, "salida": 0.6,
    "narracion": [{"texto": "Lo exige la Ley 1503 de 2011.",
                   "texto_voz": "Lo exige la Ley mil quinientos tres de dos mil once.",
                   "audio": "…/cache/voz/ab12….wav", "inicio": 1.0, "duracion": 2.4}],
    "camara": "estatica", "transicion": "corte",
    "duracion_estimada": 6.2, "inicio": 0.0, "cuadros": 186
  }],
  "avisos": [], "resuelto": true, "duracion": 12.4
}
```

`texto` es lo que sale en los subtítulos (igual al guion); `texto_voz` es lo que dice la voz, con
cifras, leyes y siglas en palabras (`motor/normalizar.py`).

## Validación

Antes de usarse, todo VideoSpec pasa por `videospec.validar()`:

1. **Esquema** (Pydantic): tipos y campos obligatorios.
2. **Catálogo**: plantilla y efectos de animación, cámara, transición, formato y fps (25, 30 o 60).
3. **Coherencia**: al menos una escena, ids únicos, duraciones mayores que cero y, si está resuelto,
   cada escena en cuadros y cada frase con su audio.

Si algo falla se lanza `VideoSpecInvalido` con el lugar exacto. Para lo que llega de un agente o de
un archivo editado a mano, `videospec.sanear()` cambia cada cámara o transición desconocida por la
de por defecto y deja el aviso `INVALID_EFFECT: …` en `avisos`. Nunca se ejecuta lo desconocido.

## Versiones

`version` sube cuando cambia el contrato de forma incompatible. Un motor solo acepta la versión
que entiende, así un proyecto viejo no se dibuja mal en silencio.
