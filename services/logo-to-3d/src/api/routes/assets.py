"""Assets API routes - fonts, materials, presets."""

from typing import List

from fastapi import APIRouter

from ...core.config import settings

router = APIRouter()


@router.get("/fonts")
async def list_fonts() -> List[str]:
    """List all available fonts."""
    # TODO: Implement font manager
    return settings.supported_fonts


@router.get("/materials")
async def list_materials() -> List[str]:
    """List all available material presets."""
    return settings.supported_materials


@router.get("/formats")
async def list_formats() -> List[str]:
    """List all supported export formats."""
    return settings.supported_export_formats
