"""
Phase 1 Configuration Settings
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent.parent
INTEGRATION_DIR = Path(__file__).parent.parent
ASSETS_DIR = INTEGRATION_DIR / "assets"

# Platform configurations
PLATFORMS = {
    "opengameart": {
        "name": "OpenGameArt.org",
        "base_url": "https://opengameart.org",
        "api_url": "https://opengameart.org/api",
        "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds"],
        "license": "CC0, CC-BY, CC-BY-SA",
        "complexity": 1,
        "requires_auth": False
    },
    "free3d": {
        "name": "Free3D",
        "base_url": "https://free3d.com",
        "supported_formats": [".blend", ".fbx", ".obj", ".3ds", ".max"],
        "license": "Various free licenses",
        "complexity": 1,
        "requires_auth": False
    }
}

# Asset directories
ASSET_DIRECTORIES = {
    "opengameart": ASSETS_DIR / "opengameart",
    "free3d": ASSETS_DIR / "free3d",
    "imported": ASSETS_DIR / "imported",
    "exports": ASSETS_DIR / "exports"
}

# Blender settings
BLENDER_SETTINGS = {
    "default_scale": 1.0,
    "import_scale": 0.01,  # Scale down from cm to m
    "material_prefix": "Phase1_",
    "collection_prefix": "Phase1_"
}

# Workflow settings
WORKFLOW_SETTINGS = {
    "max_assets_per_search": 10,
    "default_search_terms": ["character", "weapon", "environment", "vehicle"],
    "supported_file_extensions": [".blend", ".fbx", ".obj", ".dae", ".3ds", ".max"],
    "backup_enabled": True,
    "log_level": "INFO"
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": INTEGRATION_DIR / "logs" / "phase1.log",
            "mode": "a"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

