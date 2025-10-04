"""Main FastAPI application for Logo to 3D service."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

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
# Minimal UI for quick testing: simple HTML form to submit a name
@app.get("/", response_class=HTMLResponse)
async def index_page():
    return """
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Logo to 3D - Quick Demo</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
    form { display: flex; gap: 0.5rem; }
    input, button { padding: 0.6rem 0.8rem; font-size: 1rem; }
    .result { margin-top: 1rem; }
  </style>
  <script>
    async function submitForm(event) {
      event.preventDefault();
      const name = document.getElementById('name').value.trim();
      if (!name) { alert('Please enter a name.'); return; }
      const res = await fetch('/api/v1/text-to-3d', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: name })
      });
      const data = await res.json();
      document.getElementById('result').textContent = JSON.stringify(data, null, 2);
    }
  </script>
  </head>
<body>
  <h1>Logo to 3D - Quick Demo</h1>
  <p>Type a name; the server will generate a basic 3D model and trigger a Blender render pipeline.</p>
  <form onsubmit=\"submitForm(event)\">
    <input id=\"name\" name=\"name\" placeholder=\"Enter name (e.g., Dadosfera)\" />
    <button type=\"submit\">Generate</button>
  </form>
  <pre class=\"result\" id=\"result\"></pre>
</body>
</html>
"""


