"""Carga todos los agentes (cada módulo se registra al importarse)."""

from motor.agentes import director, entrega, revision, textos  # noqa: F401
from motor.agentes.base import REGISTRO, ErrorAgente, aceptar, aceptar_todas, descartar, ejecutar, estado_agentes  # noqa: F401
