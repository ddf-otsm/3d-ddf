"""Text to 3D API routes."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/text-to-3d")
async def create_text_to_3d_job():
    """Convert text to 3D model - not yet implemented."""
    raise HTTPException(
        status_code=501,
        detail="Text to 3D conversion not yet implemented. Check back in Week 2!"
    )

