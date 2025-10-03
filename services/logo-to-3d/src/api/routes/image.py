"""Image to 3D API routes."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/image-to-3d")
async def create_image_to_3d_job():
    """Convert image to 3D model - not yet implemented."""
    raise HTTPException(
        status_code=501,
        detail="Image to 3D conversion not yet implemented. Check back in Week 3!"
    )

