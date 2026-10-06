"""Errores con código, severidad y cómo recuperarse.

Cada falla del motor se clasifica con un código estable (`TTS_002`, `RENDER_001`…) para poder
contar patrones, un mensaje dicho para la persona (nunca un *traceback*) y una recuperación
sugerida. El detalle técnico va al registro del curso (`motor/logs.py`), no a la interfaz.
"""

import subprocess

SEVERIDADES = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")

# código → (severidad, mensaje para la persona, recuperación)
CODIGOS = {
    "PPTX_001": ("HIGH", "No pudimos leer la presentación.", "REVISAR_ARCHIVO"),
    "SPEC_001": ("HIGH", "El plan del video no es válido.", "REVISAR_CURSO"),
    "TTS_001": ("HIGH", "La voz elegida no se puede usar en este equipo.", "ELEGIR_OTRA_VOZ"),
    "TTS_002": ("MEDIUM", "El servicio de voz no respondió.", "REINTENTAR"),
    "AI_001": ("LOW", "La IA local no respondió; se usaron reglas.", "NINGUNA"),
    "RENDER_001": ("HIGH", "No pudimos dibujar una escena.", "REINTENTAR"),
    "AUDIO_001": ("HIGH", "No pudimos mezclar el audio.", "REINTENTAR"),
    "VIDEO_001": ("HIGH", "No pudimos armar el video.", "REINTENTAR"),
    "QA_001": ("MEDIUM", "El control de calidad encontró un problema.", "REVISAR_QA"),
    "MOTOR_001": ("CRITICAL", "Algo salió mal al producir el video.", "DIAGNOSTICO"),
}

# Qué código lleva una falla de cada etapa cuando no hay uno más preciso.
POR_ETAPA = {"plan": "SPEC_001", "voz": "TTS_002", "direccion": "SPEC_001", "escenas": "RENDER_001", "audio": "AUDIO_001",
             "unir": "VIDEO_001", "subtitulos": "VIDEO_001", "qa": "QA_001"}


class ErrorZyvo(RuntimeError):
    """Una falla ya clasificada. `str(e)` es el mensaje para la persona."""

    def __init__(self, codigo: str, mensaje: str | None = None, etapa: str | None = None, transitorio: bool = False):
        self.codigo = codigo
        self.severidad, defecto, self.recuperacion = CODIGOS[codigo]
        self.etapa = etapa
        self.transitorio = transitorio
        super().__init__(mensaje or defecto)

    def como_dict(self) -> dict:
        return {"codigo": self.codigo, "severidad": self.severidad, "recuperacion": self.recuperacion,
                "etapa": self.etapa, "mensaje": str(self)}


def transitorio(e: BaseException) -> bool:
    """Si vale la pena reintentar: la red, un servicio caído o el navegador que se cerró.

    Un error de la persona (falta la clave) o uno que se repetiría igual (ffmpeg con datos malos)
    no se reintenta.
    """
    if isinstance(e, ErrorZyvo):
        return e.transitorio
    try:
        import httpx
        if isinstance(e, httpx.TransportError):
            return True
        if isinstance(e, httpx.HTTPStatusError):
            return e.response.status_code == 429 or e.response.status_code >= 500
    except ImportError:
        pass
    try:
        from playwright.sync_api import Error as ErrorPlaywright
        if isinstance(e, ErrorPlaywright):
            return True
    except ImportError:
        pass
    return isinstance(e, (TimeoutError, ConnectionError))


def clasificar(e: BaseException, etapa: str) -> ErrorZyvo:
    """Convierte cualquier excepción de una etapa en un ErrorZyvo con su código."""
    if isinstance(e, ErrorZyvo):
        e.etapa = e.etapa or etapa
        return e
    from motor.voz import VozNoDisponible
    if isinstance(e, VozNoDisponible):
        return ErrorZyvo("TTS_001", str(e), etapa)
    from motor.videospec import VideoSpecInvalido
    if isinstance(e, VideoSpecInvalido):
        return ErrorZyvo("SPEC_001", str(e), etapa)
    pasajero = transitorio(e)
    if etapa in POR_ETAPA and (pasajero or isinstance(e, (subprocess.CalledProcessError, OSError))):
        return ErrorZyvo(POR_ETAPA[etapa], None, etapa, pasajero)
    return ErrorZyvo("MOTOR_001", None, etapa)
