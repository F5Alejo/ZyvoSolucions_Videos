# FEGIR · recordatorios del En Vivo PESV (3 videos)

Uno por correo de la secuencia de la campaña (`Documentos_contexto/correos-en-vivo-pesv`,
fuera del repo): **1-pocos-dias** (correo de reserva), **2-manana**, **3-hoy**.
Vertical 9:16, 15–19 s, identidad FEGIR heredada de `videos/fegir-envivo/` (aprobado).

- **Solo FEGIR.** Del correo se toman la estructura y los datos del evento (sábado 3 de
  octubre, 10:00 a. m., grupo oficial de WhatsApp con el texto literal del botón,
  cuenta en app.riskmann.com, Instagram · TikTok · YouTube). Nada de la marca de Yezid.
- «Faltan pocos días» en vez de «18 días»: sirve el día que se envíe.
- El cierre usa la toma **aprobada** del video principal («FEGIR… tu seguridad,
  nuestra prioridad»), leída de `../fegir-envivo/assets/mezcla/voz-6.wav`.

## Comandos

```bash
python serie.py voz                          # las 4 frases de cada video (semilla fija)
python serie.py voz 1-pocos-dias:2 2-manana:2    # regenera SOLO esas frases
python serie.py construir                    # escribe index.html + compositions/ de los tres
cd 1-pocos-dias && npx hyperframes preview   # Studio
```

`construir` **reescribe** los tres proyectos: lo editado a mano en el Studio se pierde.
Para cambiar textos o frases, edita la lista `SERIE` de `serie.py`.

Entregas y notas: `ENTREGABLES-VIDEO/fegir-recordatorios/LEEME.txt` (fuera del repo).
