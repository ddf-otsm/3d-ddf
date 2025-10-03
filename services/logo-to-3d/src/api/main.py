"""Main FastAPI application for Logo to 3D service."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..core.config import init_settings, settings
from ..core.exceptions import LogoTo3DException
from ..core.logging import setup_logging
from .routes import text, image, jobs, assets


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    # Startup
    setup_logging()
    init_settings()

    yield

    # Shutdown
    # Add cleanup logic here if needed


# Create FastAPI application
app = FastAPI(
    title="Logo to 3D Service",
    description="Convert company logos and text into professional 3D models",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(LogoTo3DException)
async def logo_to_3d_exception_handler(request: Request, exc: LogoTo3DException):
    """Handle LogoTo3D custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": {"error": str(exc)} if settings.debug else {},
            }
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "logo-to-3d"}


# API information endpoint
@app.get("/api/v1/status")
async def api_status():
    """Get API status and capabilities."""
    return {
        "service": "Logo to 3D Service",
        "version": "0.1.0",
        "status": "planning",
        "capabilities": {
            "text_to_3d": False,  # Not yet implemented
            "image_to_3d": False, # Not yet implemented
            "supported_fonts": settings.supported_fonts,
            "supported_formats": settings.supported_export_formats,
            "supported_materials": settings.supported_materials,
        }
    }


# Include routers
app.include_router(
    text.router,
    prefix="/api/v1",
    tags=["text"],
)

app.include_router(
    image.router,
    prefix="/api/v1",
    tags=["image"],
)

app.include_router(
    jobs.router,
    prefix="/api/v1",
    tags=["jobs"],
)

app.include_router(
    assets.router,
    prefix="/api/v1",
    tags=["assets"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )

