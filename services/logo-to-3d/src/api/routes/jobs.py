"""Job management API routes."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status - not yet implemented."""
    raise HTTPException(
        status_code=501,
        detail="Job management not yet implemented. Check back in Week 3!"
    )


@router.get("/jobs/{job_id}/download")
async def download_job_result(job_id: str):
    """Download job result - not yet implemented."""
    raise HTTPException(
        status_code=501,
        detail="Job downloads not yet implemented. Check back in Week 3!"
    )

