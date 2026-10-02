"""De punta a punta, como lo hace la interfaz: PPTX → análisis → estilo → voz → crear → MP4 válidos."""

import json
import subprocess
from pathlib import Path

import pytest

from tests.test_motor import VozDePrueba, hay_ffmpeg

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _ffprobe(ruta: Path) -> dict:
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_chapters",
                                      "-of", "json", str(ruta)], capture_output=True, text=True, check=True).stdout)


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_un_pptx_con_de_todo_sale_como_videos_validos(datos_copia, monkeypatch):
    pytest.importorskip("playwright")
    from fastapi.testclient import TestClient

    from app.main import app
    from motor import cola, voz
    monkeypatch.setitem(voz.PROVEEDORES, "Kokoro", VozDePrueba)
    monkeypatch.setattr(voz, "disponible", lambda v: None)
    c = TestClient(app)

    # Subir y analizar
    r = c.post("/api/trabajos", files={"archivo": ("mixto.pptx", (FIXTURES / "mixed_content.pptx").read_bytes())},
               data={"nombre": "Curso mixto"})
    assert r.status_code == 201
    id_ = r.json()["id"]
    analisis = c.get(f"/api/trabajos/{id_}/analisis").json()
    assert analisis["laminas"] == 9 and analisis["tablas"] and analisis["graficos"]

    # Estilo, voz y formato como en el flujo /crear
    assert c.put(f"/api/trabajos/{id_}/estilo", json={"estilo": "corporativo", "con_formato": False}).status_code == 200
    d = c.patch(f"/api/trabajos/{id_}", json={"marca": "riskmann", "voz": "kokoro-dora", "formatos": ["16:9"]}).json()
    claves = [v["clave"] for v in d["trabajo"]["videos"]]

    # Crear todo (y el completo si hay varios videos)
    c.post(f"/api/trabajos/{id_}/producir-todo?completo={'true' if len(claves) > 1 else 'false'}")
    cola.esperar()
    p = c.get(f"/api/trabajos/{id_}/produccion").json()
    salida = datos_copia / "trabajos" / id_ / "salida"
    muda = next(x["lamina"] for x in analisis["titulos"] if x["lamina"] in analisis["sin_notas"])
    for clave in claves:
        v = p["videos"][clave]
        assert v["estado"] == "listo" and v["fase"] == "COMPLETED", v
        fallas = {x["id"] for x in v["informe"]["chequeos"] if x["ok"] is False}
        con_muda = muda in next(x["laminas"] for x in d["trabajo"]["videos"] if x["clave"] == clave)
        # La lámina sin notas queda en silencio: el control de calidad lo marca (y solo eso).
        assert fallas == ({"silencios"} if con_muda else set()), v["informe"]["chequeos"]
        if con_muda:
            assert [b["bug"] for b in v["informe"]["bugs"]] == ["AUDIO_003"]
        info = _ffprobe(salida / clave / f"{clave}.mp4")
        tipos = {s["codec_type"]: s for s in info["streams"]}
        assert tipos["video"]["codec_name"] == "h264" and tipos["audio"]["codec_name"] == "aac"
        assert float(info["format"]["duration"]) > 3
        assert (salida / clave / "versiones" / "v001" / "video.mp4").exists()
        linea = c.get(f"/api/trabajos/{id_}/linea/{clave}").json()
        assert linea["resuelto"] and {e["transicion"] for e in linea["pistas"]["escenas"]} == {"fundido"}
    if len(claves) > 1:
        assert p["completo"]["estado"] == "listo"
        assert len(_ffprobe(salida / "completo" / "completo.mp4")["chapters"]) >= len(claves)

    # Exportar: el ZIP trae los videos y su manifiesto
    r = c.get(f"/api/trabajos/{id_}/paquete.zip")
    assert r.status_code == 200 and r.headers["content-type"] == "application/zip"


@pytest.mark.skipif(not hay_ffmpeg, reason="hace falta ffmpeg")
def test_una_pantalla_negra_de_verdad_se_detecta_y_una_lamina_oscura_no(tmp_path):
    from motor import qa
    for nombre, filtro, esperado in [("negro", "color=black:s=640x360:d=3", False),
                                     ("oscura", "color=0x020202:s=640x360:d=3,drawbox=x=40:y=150:w=120:h=30:color=white:t=fill", True)]:
        mp4 = tmp_path / f"{nombre}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", filtro, "-f", "lavfi", "-i", "sine=d=3",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(mp4)], check=True)
        negros = next(c for c in qa.revisar(mp4, 640, 360, 3, 3, 25) if c["id"] == "negros")
        assert negros["ok"] is esperado, (nombre, negros)
