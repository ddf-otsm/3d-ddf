"""
Phase 3: Game Development Configuration
Settings for Unity Asset Store and Adobe Mixamo integration
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Asset directories for Phase 3 platforms
ASSET_DIRECTORIES = {
    "unity": str(ASSETS_DIR / "unity"),
    "mixamo": str(ASSETS_DIR / "mixamo"),
    "imported": str(ASSETS_DIR / "imported"),
    "exports": str(ASSETS_DIR / "exports")
}

# Platform configurations
PLATFORMS = {
    "unity": {
        "name": "Unity Asset Store",
        "base_url": "https://assetstore.unity.com",
        "api_url": "https://assetstore.unity.com/api",
        "supported_formats": [".fbx", ".blend", ".obj", ".dae", ".3ds", ".max"],
        "license": "Unity Asset Store License",
        "complexity": 3,
        "requires_auth": True,
        "auth_type": "unity_id",
        "rate_limit": 2000,
        "special_features": ["game_ready", "optimized", "prefabs"],
        "categories": ["3D Models", "Characters", "Environments", "Vehicles", "Weapons"],
        "quality_levels": ["Free", "Standard", "Premium"],
        "export_settings": {
            "scale_factor": 1.0,
            "apply_scale": True,
            "bake_animations": True,
            "optimize_meshes": True
        }
    },
    "mixamo": {
        "name": "Adobe Mixamo",
        "base_url": "https://mixamo.com",
        "api_url": "https://mixamo.com/api",
        "supported_formats": [".fbx", ".bvh", ".dae"],
        "license": "Adobe License",
        "complexity": 3,
        "requires_auth": True,
        "auth_type": "adobe_id",
        "rate_limit": 1000,
        "special_features": ["character_animation", "auto_rigging", "motion_capture"],
        "categories": ["Locomotion", "Combat", "Idle", "Emotional", "Sports"],
        "character_types": ["humanoid", "creature", "robot"],
        "animation_settings": {
            "default_fps": 30,
            "bone_mapping": "mixamo_standard",
            "scale_factor": 0.01,  # Mixamo uses cm, Blender uses m
            "root_motion": True,
            "in_place": False
        }
    }
}

# Workflow settings
WORKFLOW_SETTINGS = {
    "max_assets_per_search": 10,
    "download_timeout": 300,  # 5 minutes
    "import_timeout": 120,    # 2 minutes
    "backup_enabled": True,
    "log_level": "INFO",
    "parallel_downloads": 3,
    "retry_attempts": 3,
    "retry_delay": 5  # seconds
}

# Game development specific settings
GAME_DEVELOPMENT = {
    "optimization_levels": {
        "mobile": {
            "max_polygons": 5000,
            "max_texture_size": 1024,
            "max_materials": 3,
            "lod_levels": 2
        },
        "console": {
            "max_polygons": 20000,
            "max_texture_size": 2048,
            "max_materials": 5,
            "lod_levels": 3
        },
        "pc": {
            "max_polygons": 50000,
            "max_texture_size": 4096,
            "max_materials": 8,
            "lod_levels": 4
        }
    },
    "character_rigging": {
        "standard_bones": [
            "Hips", "Spine", "Spine1", "Spine2", "Neck", "Head",
            "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
            "RightShoulder", "RightArm", "RightForeArm", "RightHand",
            "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase",
            "RightUpLeg", "RightLeg", "RightFoot", "RightToeBase"
        ],
        "facial_bones": [
            "Jaw", "LeftEye", "RightEye", "LeftEar", "RightEar"
        ],
        "finger_bones": [
            "LeftThumb1", "LeftThumb2", "LeftThumb3",
            "LeftIndex1", "LeftIndex2", "LeftIndex3",
            "LeftMiddle1", "LeftMiddle2", "LeftMiddle3",
            "LeftRing1", "LeftRing2", "LeftRing3",
            "LeftPinky1", "LeftPinky2", "LeftPinky3"
        ]
    },
    "animation_curves": {
        "locomotion": ["walk", "run", "jog", "sprint", "crouch_walk"],
        "combat": ["punch", "kick", "block", "dodge", "attack"],
        "idle": ["idle", "idle_2", "idle_3", "bored", "alert"],
        "emotional": ["happy", "sad", "angry", "surprised", "fearful"]
    }
}

# Export settings for different game engines
EXPORT_SETTINGS = {
    "unity": {
        "format": "fbx",
        "scale_factor": 1.0,
        "apply_scale": True,
        "bake_animations": True,
        "optimize_meshes": True,
        "export_materials": True,
        "export_textures": True
    },
    "unreal": {
        "format": "fbx",
        "scale_factor": 0.01,  # Unreal uses cm
        "apply_scale": True,
        "bake_animations": True,
        "optimize_meshes": True,
        "export_materials": True,
        "export_textures": True
    },
    "blender": {
        "format": "blend",
        "scale_factor": 1.0,
        "apply_scale": False,
        "bake_animations": False,
        "optimize_meshes": False,
        "export_materials": True,
        "export_textures": True
    }
}

# Quality presets
QUALITY_PRESETS = {
    "draft": {
        "texture_resolution": 512,
        "polygon_reduction": 0.5,
        "animation_fps": 15,
        "lighting": "basic"
    },
    "preview": {
        "texture_resolution": 1024,
        "polygon_reduction": 0.8,
        "animation_fps": 24,
        "lighting": "standard"
    },
    "production": {
        "texture_resolution": 2048,
        "polygon_reduction": 1.0,
        "animation_fps": 30,
        "lighting": "advanced"
    },
    "cinematic": {
        "texture_resolution": 4096,
        "polygon_reduction": 1.0,
        "animation_fps": 60,
        "lighting": "cinematic"
    }
}

# File naming conventions
FILE_NAMING = {
    "asset_prefix": "Phase3",
    "separator": "_",
    "include_platform": True,
    "include_date": True,
    "include_quality": True,
    "max_length": 50
}

# Logging configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(BASE_DIR / "phase3.log"),
    "max_size": 10485760,  # 10MB
    "backup_count": 5
}
