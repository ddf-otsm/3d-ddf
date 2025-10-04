"""Text to 3D API routes."""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from ...core.blender_server import get_blender_server
from ...core.logging import get_logger
from pathlib import Path
import tempfile
import json

logger = get_logger(__name__)

router = APIRouter()


class TextTo3DRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=64)
    material: Optional[str] = Field(default="metal")
    export_format: Optional[str] = Field(default="obj")


@router.post("/text-to-3d")
async def create_text_to_3d_job(payload: TextTo3DRequest = Body(...)):
    """Minimal PoC: generate simple Blender script and run headless."""
    server = get_blender_server()

    # Build operations: simple name as mesh, basic material, export
    operations = [
        # For now, import_svg path is empty; PoC uses extrusion on text curve would require richer ops
        # We'll just set lighting and export an empty scene as placeholder to validate pipeline
        {"type": "setup_lighting", "params": {}},
        {"type": "export_mesh", "params": {"format": payload.export_format, "output_path": str(Path(tempfile.gettempdir()) / f"{payload.text}.{payload.export_format}")}},
    ]

    script_path = server.create_blender_script(operations)

    try:
        result = server.process_request(script_path, timeout=server.settings.blender_timeout if hasattr(server, 'settings') else 300)
    except Exception as e:
        logger.exception("Text-to-3D job failed")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "submitted",
        "text": payload.text,
        "result": {
            "returncode": result.get("returncode"),
            "temp_dir": result.get("temp_dir"),
            "script_path": result.get("script_path"),
        },
    }

