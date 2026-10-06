"""VideoSpec: el contrato entre el curso, la IA, la voz, las escenas y el render.

Un VideoSpec describe **un video** de principio a fin con datos, no con código: qué escenas
tiene, qué dice la voz en cada una, cómo entra y sale cada elemento, qué cámara y qué transición
usa, y con qué formato y audio se entrega. El render solo lee el VideoSpec.

Tiene dos momentos (la duración depende de la voz, y no se conoce hasta generarla):

    videospec.plan.json   `construir()`: duraciones **estimadas**; sale en segundos y sin costo
    videospec.json        `resolver()`:  cada frase con su audio, y cada escena en cuadros exactos

Todo valor de catálogo (animación, cámara, transición, fps, formato) se valida. Lo que no está en
el catálogo no se ejecuta: `sanear()` lo cambia por el de por defecto y deja el aviso
`INVALID_EFFECT` en `avisos`.
"""

import hashlib
import json
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from app import configuracion, datos, extractor, taller
from motor import catalogo, escenas, estilos, normalizar, recursos, sfx
from motor.escenas import animacion

VERSION = 1
FPS_PERMITIDOS = (25, 30, 60)
MUDA = 3.0  # una lámina sin narración (no debería pasar: el taller lo marca)


class VideoSpecInvalido(ValueError):
    """El VideoSpec no cumple el contrato (esquema, catálogo o coherencia)."""


# ── El contrato ──────────────────────────────────────────────────────────────

class Frase(BaseModel):
    texto: str                       # lo que se lee en los subtítulos (tal cual el guion)
    texto_voz: str                   # lo que dice la voz (cifras y normas en palabras)
    audio: str | None = None         # WAV de 48 kHz (en la caché de voz)
    inicio: float | None = None      # segundo del video en que empieza
    duracion: float | None = None


class Efecto(BaseModel):
    id: str                          # del catálogo de motor/sfx.py
    desfase: float = 0.0             # segundos desde que empieza la escena
    volumen: float = sfx.VOLUMEN_DEFECTO
    inicio: float | None = None      # segundo del video (cuando está resuelto)

    @field_validator("id")
    @classmethod
    def _id(cls, v):
        if v not in sfx.CATALOGO:
            raise ValueError(f"el efecto de sonido «{v}» no está en el catálogo")
        return v

    @field_validator("volumen")
    @classmethod
    def _volumen(cls, v):
        if v > sfx.VOLUMEN_MAXIMO:
            raise ValueError(f"un efecto no puede sonar a más de {sfx.VOLUMEN_MAXIMO:g} dB: taparía la voz")
        return v


TOMAS = ("clip", "foto", "lamina", "marca")   # de dónde sale el fondo de un momento
ESTILOS_BEAT = ("cajas", "termino", "cifra")


class Toma(BaseModel):
    tipo: str                        # clip o foto del banco de la empresa, imagen de la lámina, o fondo de marca
    archivo: str | None = None       # ruta absoluta (None en «marca»)
    desde: float = 0.0               # segundo del clip en que empieza la toma
    id: str | None = None            # id en el banco de medios (motor/banco)

    @field_validator("tipo")
    @classmethod
    def _tipo(cls, v):
        if v not in TOMAS:
            raise ValueError(f"la toma «{v}» no existe")
        return v


class Beat(BaseModel):
    """Un momento del video: lo que se ve mientras la voz dice una frase (o un trozo de ella)."""
    inicio: float                    # segundos desde que empieza la escena
    fin: float
    texto: str                       # 1 a 6 palabras en pantalla, sacadas de lo que dice la voz
    resaltado: list[int] = []        # índices de las palabras resaltadas (color de acento)
    etiqueta: str | None = None      # rótulo corto encima del texto («MODELADO 3D»)
    estilo: str = "cajas"            # cómo entra el texto (ESTILOS_BEAT)
    toma: Toma = Toma(tipo="marca")
    palabras: list[float] = []       # segundo (desde la escena) en que la voz dice cada palabra

    @field_validator("estilo")
    @classmethod
    def _estilo(cls, v):
        if v not in ESTILOS_BEAT:
            raise ValueError(f"el estilo de texto «{v}» no existe")
        return v

    @model_validator(mode="after")
    def _coherencia(self):
        n = len(self.texto.split())
        if not 1 <= n <= 8:
            raise ValueError(f"«{self.texto}»: en pantalla van de 1 a 8 palabras")
        if self.fin <= self.inicio:
            raise ValueError(f"«{self.texto}»: termina antes de empezar")
        if self.palabras and len(self.palabras) != n:
            raise ValueError(f"«{self.texto}»: tiene {n} palabras y {len(self.palabras)} tiempos")
        if any(not 0 <= i < n for i in self.resaltado):
            raise ValueError(f"«{self.texto}»: resalta una palabra que no está")
        return self


class Escena(BaseModel):
    id: str
    lamina: int
    indice: int
    vista: dict                      # lo que se ve: tipo, título, viñetas, imagen (motor/escenas.vista)
    animacion: dict                  # entradas y salidas ya resueltas (motor/escenas/animacion.plan)
    entrada: float                   # segundos que tarda en entrar todo
    salida: float                    # segundos antes del final en que empieza a salir
    narracion: list[Frase]
    camara: str = catalogo.CAMARA_DEFECTO
    transicion: str = catalogo.TRANSICION_DEFECTO
    sfx: list[Efecto] = []
    duracion_estimada: float
    inicio: float | None = None
    cuadros: int | None = None
    beats: list[Beat] = []           # la dirección visual (motor/direccion.py), para el renderer HyperFrames

    @field_validator("camara")
    @classmethod
    def _camara(cls, v):
        if v not in catalogo.CAMARA:
            raise ValueError(f"la cámara «{v}» no está en el catálogo")
        return v

    @field_validator("transicion")
    @classmethod
    def _transicion(cls, v):
        if v not in catalogo.TRANSICION:
            raise ValueError(f"la transición «{v}» no está en el catálogo")
        return v

    @field_validator("animacion")
    @classmethod
    def _animacion(cls, v):
        if v.get("plantilla") not in animacion.plantillas():
            raise ValueError(f"la plantilla de animación «{v.get('plantilla')}» no existe")
        animacion.validar_elementos(v.get("elementos") or {}, completo=True)
        return v


class Video(BaseModel):
    formato: str
    ancho: int                       # el lienzo en el que se diseña la escena
    alto: int
    escala: float = 1.0              # 2/3 para 720p
    fps: int
    crf: str
    preset: str
    subtitulos_quemados: bool = False

    @field_validator("formato")
    @classmethod
    def _formato(cls, v):
        if v not in escenas.FORMATOS:
            raise ValueError(f"el formato «{v}» no existe")
        return v

    @field_validator("fps")
    @classmethod
    def _fps(cls, v):
        if v not in FPS_PERMITIDOS:
            raise ValueError(f"{v} fps no está permitido")
        return v

    @property
    def ancho_real(self) -> int:
        return round(self.ancho * self.escala)

    @property
    def alto_real(self) -> int:
        return round(self.alto * self.escala)


class Audio(BaseModel):
    lufs: float
    musica: str | None = None        # nombre del archivo en datos/musica/
    musica_volumen: float = -22.0
    musica_elegida_por: str | None = None   # "configuración" o "estilo" (el director de música)


class Tiempos(BaseModel):
    entrada: float                   # la escena entra antes que la voz
    pausa: float                     # entre frases
    salida: float                    # respiro al final de la lámina


class Voz(BaseModel):
    id: str
    nombre: str
    proveedor: str
    solo_borrador: bool = False


class VideoSpec(BaseModel):
    version: int = VERSION
    trabajo: str
    clave: str
    titulo: str
    curso: str
    marca: str
    firma: str                       # lo que produjo el video (motor/produccion.firma)
    voz: Voz
    video: Video
    audio: Audio
    tiempos: Tiempos
    estilo: dict                     # colores, nombre y logo de la marca para la escena
    estilo_video: str | None = None  # el estilo elegido (motor/estilos.py), si hay
    escenas: list[Escena] = Field(min_length=1)
    avisos: list[str] = []
    resuelto: bool = False
    duracion: float | None = None    # segundos reales (cuando está resuelto)

    @model_validator(mode="after")
    def _coherencia(self):
        if self.version != VERSION:
            raise ValueError(f"VideoSpec v{self.version}: este motor entiende la v{VERSION}")
        ids = [e.id for e in self.escenas]
        if len(set(ids)) != len(ids):
            raise ValueError("hay escenas con el mismo id")
        if self.resuelto:
            for e in self.escenas:
                if not e.cuadros or e.cuadros <= 0 or e.inicio is None:
                    raise ValueError(f"{e.id}: sin duración en cuadros")
                if any(f.audio is None or f.inicio is None for f in e.narracion):
                    raise ValueError(f"{e.id}: hay frases sin audio")
        elif any(e.duracion_estimada <= 0 for e in self.escenas):
            raise ValueError("hay escenas sin duración")
        return self

    def guardar(self, ruta: Path) -> None:
        tmp = ruta.with_suffix(".tmp")
        tmp.write_text(self.model_dump_json(indent=1), encoding="utf-8")
        tmp.replace(ruta)


def validar(datos_spec: dict) -> VideoSpec:
    try:
        return VideoSpec.model_validate(datos_spec)
    except ValidationError as e:
        primero = e.errors()[0]
        donde = ".".join(str(x) for x in primero["loc"])
        raise VideoSpecInvalido(f"VideoSpec inválido en {donde or 'la raíz'}: {primero['msg']}") from e


def leer(ruta: Path) -> VideoSpec:
    return validar(json.loads(ruta.read_text(encoding="utf-8")))


def sanear(d: dict) -> tuple[dict, list[str]]:
    """Cambia por el de por defecto todo valor de cámara o transición fuera del catálogo.

    Para lo que propone un agente o lo que llega de un archivo editado a mano: nada fuera del
    catálogo se ejecuta. Devuelve el dict corregido y los avisos `INVALID_EFFECT`.
    """
    avisos = []
    for e in d.get("escenas", []):
        for campo, cat, defecto in (("camara", catalogo.CAMARA, catalogo.CAMARA_DEFECTO),
                                    ("transicion", catalogo.TRANSICION, catalogo.TRANSICION_DEFECTO)):
            if e.get(campo, defecto) not in cat:
                avisos.append(f"INVALID_EFFECT: {e.get('id')}: {campo} «{e[campo]}» no existe; se usa «{defecto}»")
                e[campo] = defecto
    d["avisos"] = list(d.get("avisos", [])) + avisos
    return d, avisos


# ── Construir el plan ────────────────────────────────────────────────────────

def _escena_opciones(t: dict, n: int) -> dict:
    """Cámara y transición de una lámina: las del curso, y encima las de esa lámina."""
    escena = t.get("escena") or {}
    propia = (escena.get("laminas") or {}).get(str(n)) or {}
    return {"camara": propia.get("camara") or escena.get("camara") or catalogo.CAMARA_DEFECTO,
            "transicion": propia.get("transicion") or escena.get("transicion") or catalogo.TRANSICION_DEFECTO}


def construir(t: dict, clave: str, firma: str, formato: str = "16:9") -> VideoSpec:
    """El plan del video `clave`: escenas, narración, animación y ajustes, con duraciones estimadas."""
    r = taller.resumen(t)
    video = next((v for v in r["videos"] if v["clave"] == clave), None)
    if video is None:
        raise VideoSpecInvalido(f"El trabajo no tiene un video «{clave}»")
    marca = datos.marcas()[t["marca"]]
    voz = next(v for v in taller.voces() if v["id"] == t["voz"])
    conf = configuracion.para_trabajo(t)
    cv, ca, ct = conf["video"], conf["audio"], conf["tiempos"]
    crf, preset = configuracion.CALIDADES[cv["calidad"]]
    ancho, alto = escenas.FORMATOS[formato]
    media = recursos.media(t)
    laminas = video["laminas_detalle"]

    lista, avisos = [], []
    for i, l in enumerate(laminas):
        v = escenas.vista(l, i, len(laminas), video["titulo"], media, t["nombre"])
        p = animacion.plan(t, l["n"])
        ent, sal = animacion.duraciones(p, v)
        narracion = [Frase(texto=f, texto_voz=normalizar.para_voz(f, marca.get("pronunciacion")))
                     for f in l["frases"]]
        habla = sum(len(f.texto_voz.split()) / extractor.PALABRAS_POR_SEGUNDO for f in narracion)
        estimada = (ct["entrada"] + habla + ct["pausa"] * max(0, len(narracion) - 1) + max(ct["salida"], sal + 0.3)
                    if narracion else max(MUDA, ent + sal + 1.0))
        lista.append({"id": f"escena-{i + 1:03d}", "lamina": l["n"], "indice": i, "vista": v, "animacion": p,
                      "entrada": ent, "salida": sal, "narracion": [f.model_dump() for f in narracion],
                      "duracion_estimada": round(estimada, 3), **_escena_opciones(t, l["n"])})
        if not narracion:
            avisos.append(f"{lista[-1]['id']}: la lámina {l['n']} no tiene narración")

    estilo_video = estilos.del_curso(t)
    efectos = sfx.dirigir([{"transicion_previa": lista[i - 1]["transicion"] if i else None} for i in range(len(lista))],
                          (estilo_video or {}).get("sfx"))
    for e, propios in zip(lista, efectos):
        e["sfx"] = propios
    musica, elegida_por = ca["musica"], "configuración" if ca["musica"] else None
    if musica is None and estilo_video and ca.get("musica_estilo", True):
        musica = estilos.elegir_musica(estilo_video.get("musica"), configuracion.pistas())
        elegida_por = "estilo" if musica else None

    d = {"trabajo": t["id"], "clave": clave, "titulo": video["titulo"], "curso": t["nombre"], "marca": t["marca"],
         "firma": firma, "voz": {k: voz.get(k) for k in ("id", "nombre", "proveedor")} | {"solo_borrador": bool(voz.get("solo_borrador"))},
         "video": {"formato": formato, "ancho": ancho, "alto": alto, "escala": configuracion.RESOLUCIONES[cv["resolucion"]],
                   "fps": int(cv["fps"]), "crf": crf, "preset": preset, "subtitulos_quemados": bool(cv["subtitulos_quemados"])},
         "audio": {"lufs": ca["lufs"], "musica": musica, "musica_volumen": ca["musica_volumen"],
                   "musica_elegida_por": elegida_por},
         "estilo_video": (estilo_video or {}).get("id"),
         "tiempos": ct, "estilo": escenas.estilo(marca, recursos.logo(marca)), "escenas": lista, "avisos": avisos}
    d, _ = sanear(d)
    return validar(d)


# ── Resolver: la voz y los cuadros exactos ───────────────────────────────────

def cuadros(segundos: float, fps: int) -> int:
    return max(1, round(segundos * fps))


def resolver(spec: VideoSpec, generar: Callable[[str], Path], duracion_de: Callable[[Path], float],
             avisar: Callable[[str, float], None] = lambda paso, x: None) -> VideoSpec:
    """Genera (o toma de la caché) el audio de cada frase y fija la línea de tiempo en cuadros exactos.

    `generar(texto_voz)` devuelve el WAV de la frase; `duracion_de(wav)` sus segundos. La imagen y la
    voz no se pueden separar: cada escena dura un número entero de cuadros y la siguiente empieza
    justo ahí.
    """
    d = spec.model_dump()
    tiempos, fps = spec.tiempos, spec.video.fps
    total = sum(len(e["narracion"]) for e in d["escenas"]) or 1
    hechas, t0 = 0, 0.0
    for e in d["escenas"]:
        frases = e["narracion"]
        dur = tiempos.entrada + max(tiempos.salida, e["salida"] + 0.3) if frases else max(MUDA, e["entrada"] + e["salida"] + 1.0)
        cursor = t0 + tiempos.entrada
        for i, f in enumerate(frases):
            avisar(f"Voz: frase {hechas + 1} de {total}", hechas / total)
            wav = generar(f["texto_voz"])
            largo = duracion_de(wav)
            f.update(audio=str(wav), inicio=round(cursor, 6), duracion=round(largo, 6))
            extra = largo + (tiempos.pausa if i < len(frases) - 1 else 0)
            cursor += extra
            dur += extra
            hechas += 1
        e["cuadros"] = cuadros(dur, fps)
        e["inicio"] = round(t0, 6)
        for x in e.get("sfx", []):
            x["inicio"] = round(t0 + x["desfase"], 6)
        t0 += e["cuadros"] / fps
    d.update(resuelto=True, duracion=round(t0, 6))
    return validar(d)


def linea_de_tiempo(spec: VideoSpec) -> dict:
    """Las pistas del video para dibujarlas: escenas, voz, música, efectos y subtítulos.

    Con un VideoSpec resuelto, los tiempos son los reales; con un plan, se estiman con la velocidad
    de lectura medida (`extractor.PALABRAS_POR_SEGUNDO`).
    """
    escenas_, voz, efectos, t0 = [], [], [], 0.0
    fps = spec.video.fps
    for e in spec.escenas:
        inicio = e.inicio if spec.resuelto else t0
        dura = e.cuadros / fps if spec.resuelto else e.duracion_estimada
        escenas_.append({"id": e.id, "lamina": e.lamina, "titulo": e.vista.get("titulo"), "tipo": e.vista.get("tipo"),
                         "inicio": round(inicio, 2), "duracion": round(dura, 2), "camara": e.camara,
                         "transicion": e.transicion, "plantilla": e.animacion.get("plantilla")})
        cursor = inicio + spec.tiempos.entrada
        for f in e.narracion:
            a = f.inicio if spec.resuelto else cursor
            d = f.duracion if spec.resuelto else len(f.texto_voz.split()) / extractor.PALABRAS_POR_SEGUNDO
            voz.append({"escena": e.id, "inicio": round(a, 2), "fin": round(a + d, 2), "texto": f.texto})
            cursor = a + d + spec.tiempos.pausa
        for x in e.sfx:
            efectos.append({"escena": e.id, "id": x.id, "nombre": sfx.CATALOGO[x.id],
                            "inicio": round(x.inicio if spec.resuelto else inicio + x.desfase, 2)})
        t0 = inicio + dura
    total = spec.duracion if spec.resuelto else t0
    musica = [{"inicio": 0.0, "fin": round(total, 2), "archivo": spec.audio.musica}] if spec.audio.musica else []
    return {"clave": spec.clave, "titulo": spec.titulo, "resuelto": spec.resuelto, "duracion": round(total, 2),
            "formato": spec.video.formato, "pistas": {"escenas": escenas_, "voz": voz, "musica": musica, "sfx": efectos,
                                                       "subtitulos": voz}}


def huella(*partes) -> str:
    """Un hash corto y estable de lo que se le pase (para la caché de escenas)."""
    texto = json.dumps(partes, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:20]
