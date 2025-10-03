"""
Phase 2 Configuration Settings
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent.parent
INTEGRATION_DIR = Path(__file__).parent.parent
ASSETS_DIR = INTEGRATION_DIR / "assets"

# Platform configurations
PLATFORMS = {
    "sketchfab": {
        "name": "Sketchfab",
        "base_url": "https://sketchfab.com",
        "api_url": "https://api.sketchfab.com/v3",
        "supported_formats": [".gltf", ".glb", ".blend", ".fbx", ".obj", ".dae"],
        "license": "Various licenses",
        "complexity": 2,
        "requires_auth": True,
        "auth_type": "api_key",
        "rate_limit": 1000
    },
    "clara": {
        "name": "Clara.io",
        "base_url": "https://clara.io",
        "api_url": "https://clara.io/api",
        "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds"],
        "license": "Various licenses",
        "complexity": 2,
        "requires_auth": True,
        "auth_type": "oauth",
        "rate_limit": 500
    }
}

# Asset directories
ASSET_DIRECTORIES = {
    "sketchfab": ASSETS_DIR / "sketchfab",
    "clara": ASSETS_DIR / "clara",
    "imported": ASSETS_DIR / "imported",
    "exports": ASSETS_DIR / "exports"
}

# Blender settings
BLENDER_SETTINGS = {
    "default_scale": 1.0,
    "import_scale": 0.01,  # Scale down from cm to m
    "material_prefix": "Phase2_",
    "collection_prefix": "Phase2_",
    "advanced_lighting": True,
    "use_cycles": True
}

# Workflow settings
WORKFLOW_SETTINGS = {
    "max_assets_per_search": 10,
    "default_search_terms": ["character", "weapon", "environment", "vehicle", "architecture"],
    "supported_file_extensions": [".gltf", ".glb", ".blend", ".fbx", ".obj", ".dae", ".3ds"],
    "backup_enabled": True,
    "log_level": "INFO",
    "auth_required": True
}

# Authentication settings
AUTH_SETTINGS = {
    "sketchfab": {
        "api_key_env": "SKETCHFAB_API_KEY",
        "api_key_file": "sketchfab_api_key.txt",
        "required": True
    },
    "clara": {
        "token_env": "CLARA_IO_TOKEN",
        "token_file": "clara_io_token.txt",
        "required": True
    }
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
            "filename": INTEGRATION_DIR / "logs" / "phase2.log",
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
