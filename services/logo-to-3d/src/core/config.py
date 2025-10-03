"""Core configuration for the Logo to 3D service."""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = "Logo to 3D Service"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENV")

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")

    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost/logo3d",
        env="DATABASE_URL"
    )

    # Redis/Celery
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    celery_broker_url: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/1", env="CELERY_RESULT_BACKEND")

    # File storage
    upload_dir: Path = Field(default=Path("./data/uploads"))
    output_dir: Path = Field(default=Path("./data/outputs"))
    temp_dir: Path = Field(default=Path("./data/temp"))
    fonts_dir: Path = Field(default=Path("./fonts"))

    # Blender settings
    blender_executable: Optional[str] = Field(default=None, env="BLENDER_EXECUTABLE")
    blender_timeout: int = Field(default=300, env="BLENDER_TIMEOUT")  # seconds

    # Processing limits
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    max_processing_time: int = Field(default=300, env="MAX_PROCESSING_TIME")  # seconds
    max_concurrent_jobs: int = Field(default=5, env="MAX_CONCURRENT_JOBS")

    # Font settings
    default_font: str = Field(default="Liberation Sans")
    supported_fonts: List[str] = Field(default_factory=lambda: [
        "Liberation Sans", "Liberation Serif", "Liberation Mono",
        "DejaVu Sans", "DejaVu Serif", "DejaVu Sans Mono",
        "Arial", "Helvetica", "Verdana", "Tahoma"
    ])

    # Material settings
    default_material: str = Field(default="plastic")
    supported_materials: List[str] = Field(default_factory=lambda: [
        "plastic", "metal", "glass", "wood", "fabric", "ceramic"
    ])

    # Processing defaults
    default_extrude_depth: float = Field(default=0.1)
    default_bevel_depth: float = Field(default=0.01)
    default_resolution: int = Field(default=12)

    # Export settings
    default_export_formats: List[str] = Field(default_factory=lambda: ["obj", "gltf"])
    supported_export_formats: List[str] = Field(default_factory=lambda: [
        "obj", "fbx", "gltf", "glb", "stl", "ply", "x3d", "usd"
    ])

    # Security
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    api_key_required: bool = Field(default=False, env="API_KEY_REQUIRED")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @computed_field
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    def create_directories(self) -> None:
        """Create necessary directories."""
        directories = [
            self.upload_dir,
            self.output_dir,
            self.temp_dir,
            self.fonts_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def init_settings() -> Settings:
    """Initialize and return application settings."""
    settings.create_directories()
    return settings

