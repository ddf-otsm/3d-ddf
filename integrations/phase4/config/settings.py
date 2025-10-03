"""
Phase 4: Professional Marketplace Configuration
Settings for CGTrader, TurboSquid, and Unreal Marketplace integration
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Asset directories for Phase 4 platforms
ASSET_DIRECTORIES = {
    "cgtrader": str(ASSETS_DIR / "cgtrader"),
    "turbosquid": str(ASSETS_DIR / "turbosquid"),
    "unreal": str(ASSETS_DIR / "unreal"),
    "imported": str(ASSETS_DIR / "imported"),
    "exports": str(ASSETS_DIR / "exports")
}

# Platform configurations
PLATFORMS = {
    "cgtrader": {
        "name": "CGTrader",
        "base_url": "https://www.cgtrader.com",
        "api_url": "https://www.cgtrader.com/api",
        "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds", ".max", ".c4d"],
        "license": "Commercial License",
        "complexity": 4,
        "requires_auth": True,
        "auth_type": "api_key",
        "rate_limit": 500,
        "special_features": ["commercial_license", "high_poly", "professional_quality", "texture_packs"],
        "categories": ["Architecture", "Characters", "Vehicles", "Nature", "Furniture"],
        "quality_levels": ["Standard", "Premium", "Ultra"],
        "export_settings": {
            "scale_factor": 1.0,
            "apply_scale": True,
            "bake_animations": True,
            "optimize_meshes": True
        }
    },
    "turbosquid": {
        "name": "TurboSquid",
        "base_url": "https://www.turbosquid.com",
        "api_url": "https://www.turbosquid.com/api",
        "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds", ".max", ".c4d", ".ma"],
        "license": "Commercial License",
        "complexity": 4,
        "requires_auth": True,
        "auth_type": "api_key",
        "rate_limit": 300,
        "special_features": ["commercial_license", "industry_standard", "professional_quality", "rigged_models"],
        "categories": ["Architecture", "Characters", "Vehicles", "Nature", "Furniture"],
        "quality_levels": ["Standard", "Premium", "Ultra"],
        "export_settings": {
            "scale_factor": 1.0,
            "apply_scale": True,
            "bake_animations": True,
            "optimize_meshes": True
        }
    },
    "unreal": {
        "name": "Unreal Marketplace",
        "base_url": "https://www.unrealengine.com/marketplace",
        "api_url": "https://www.unrealengine.com/api",
        "supported_formats": [".fbx", ".obj", ".dae", ".abc"],
        "license": "Unreal Engine License",
        "complexity": 4,
        "requires_auth": True,
        "auth_type": "epic_id",
        "rate_limit": 200,
        "special_features": ["unreal_optimized", "real_time_ready", "professional_quality", "blueprint_ready"],
        "categories": ["Environment", "Characters", "Vehicles", "Props", "Effects"],
        "quality_levels": ["Standard", "Premium", "Ultra"],
        "export_settings": {
            "scale_factor": 0.01,  # Unreal uses cm
            "apply_scale": True,
            "bake_animations": True,
            "optimize_meshes": True
        }
    }
}

# Workflow settings
WORKFLOW_SETTINGS = {
    "max_assets_per_search": 5,
    "download_timeout": 600,  # 10 minutes
    "import_timeout": 300,    # 5 minutes
    "backup_enabled": True,
    "log_level": "INFO",
    "parallel_downloads": 2,
    "retry_attempts": 3,
    "retry_delay": 10  # seconds
}

# Professional marketplace specific settings
PROFESSIONAL_MARKETPLACE = {
    "quality_levels": {
        "standard": {
            "max_polygons": 25000,
            "max_texture_size": 2048,
            "max_materials": 5,
            "price_range": "$50-$200"
        },
        "premium": {
            "max_polygons": 50000,
            "max_texture_size": 4096,
            "max_materials": 8,
            "price_range": "$200-$500"
        },
        "ultra": {
            "max_polygons": 100000,
            "max_texture_size": 8192,
            "max_materials": 12,
            "price_range": "$500+"
        }
    },
    "licensing": {
        "commercial_license": {
            "description": "Full commercial usage rights",
            "restrictions": "None",
            "price_multiplier": 1.0
        },
        "extended_license": {
            "description": "Extended commercial usage rights",
            "restrictions": "None",
            "price_multiplier": 2.0
        },
        "exclusive_license": {
            "description": "Exclusive commercial usage rights",
            "restrictions": "Exclusive to buyer",
            "price_multiplier": 10.0
        }
    },
    "quality_standards": {
        "texture_quality": {
            "standard": "4K",
            "premium": "8K",
            "ultra": "16K"
        },
        "polygon_density": {
            "low": 1000,
            "medium": 10000,
            "high": 50000,
            "ultra": 100000
        },
        "material_complexity": {
            "simple": 3,
            "standard": 5,
            "complex": 8,
            "ultra": 12
        }
    }
}

# Export settings for different professional workflows
EXPORT_SETTINGS = {
    "cgtrader": {
        "format": "fbx",
        "scale_factor": 1.0,
        "apply_scale": True,
        "bake_animations": True,
        "optimize_meshes": True,
        "export_materials": True,
        "export_textures": True,
        "export_uvs": True,
        "export_normals": True
    },
    "turbosquid": {
        "format": "fbx",
        "scale_factor": 1.0,
        "apply_scale": True,
        "bake_animations": True,
        "optimize_meshes": True,
        "export_materials": True,
        "export_textures": True,
        "export_uvs": True,
        "export_normals": True
    },
    "unreal": {
        "format": "fbx",
        "scale_factor": 0.01,  # Unreal uses cm
        "apply_scale": True,
        "bake_animations": True,
        "optimize_meshes": True,
        "export_materials": True,
        "export_textures": True,
        "export_uvs": True,
        "export_normals": True,
        "unreal_optimized": True
    },
    "blender": {
        "format": "blend",
        "scale_factor": 1.0,
        "apply_scale": False,
        "bake_animations": False,
        "optimize_meshes": False,
        "export_materials": True,
        "export_textures": True,
        "export_uvs": True,
        "export_normals": True
    }
}

# Quality presets for professional work
QUALITY_PRESETS = {
    "draft": {
        "texture_resolution": 1024,
        "polygon_reduction": 0.3,
        "animation_fps": 24,
        "lighting": "basic",
        "use_case": "concept_art"
    },
    "preview": {
        "texture_resolution": 2048,
        "polygon_reduction": 0.6,
        "animation_fps": 30,
        "lighting": "standard",
        "use_case": "client_presentation"
    },
    "production": {
        "texture_resolution": 4096,
        "polygon_reduction": 0.8,
        "animation_fps": 30,
        "lighting": "advanced",
        "use_case": "final_production"
    },
    "cinematic": {
        "texture_resolution": 8192,
        "polygon_reduction": 1.0,
        "animation_fps": 60,
        "lighting": "cinematic",
        "use_case": "high_end_rendering"
    },
    "real_time": {
        "texture_resolution": 2048,
        "polygon_reduction": 0.5,
        "animation_fps": 60,
        "lighting": "real_time",
        "use_case": "game_engine"
    }
}

# File naming conventions for professional work
FILE_NAMING = {
    "asset_prefix": "Phase4",
    "separator": "_",
    "include_platform": True,
    "include_date": True,
    "include_quality": True,
    "include_license": True,
    "max_length": 60,
    "use_camel_case": False
}

# Professional workflow settings
PROFESSIONAL_WORKFLOW = {
    "version_control": True,
    "backup_frequency": "daily",
    "quality_checks": True,
    "license_validation": True,
    "metadata_tracking": True,
    "cost_tracking": True,
    "usage_analytics": True
}

# Logging configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(BASE_DIR / "phase4.log"),
    "max_size": 20971520,  # 20MB
    "backup_count": 10
}
