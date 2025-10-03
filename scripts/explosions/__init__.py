"""
Explosion creation utilities for 3D-DDF project.
"""

# Import configuration and materials (always available)
from .config import ExplosionConfig, QualityPreset, DEFAULT_CONFIGS
from .materials import ExplosionMaterials

# Conditionally import Blender-dependent modules
try:
    import bpy
    BLENDER_AVAILABLE = True
    from .create_production_explosion import (
        create_explosion_sequence,
        clear_existing_explosions,
        create_fire_particles,
        create_debris_particles,
        create_smoke_volume,
        animate_explosion,
        create_explosion_from_preset,
        create_quick_explosion,
        create_medium_explosion,
        create_high_explosion
    )

    __all__ = [
        'create_explosion_sequence',
        'clear_existing_explosions',
        'create_fire_particles',
        'create_debris_particles',
        'create_smoke_volume',
        'animate_explosion',
        'create_explosion_from_preset',
        'create_quick_explosion',
        'create_medium_explosion',
        'create_high_explosion',
        'ExplosionConfig',
        'QualityPreset',
        'DEFAULT_CONFIGS',
        'ExplosionMaterials'
    ]

except ImportError:
    BLENDER_AVAILABLE = False
    # Define stub functions that raise informative errors

    def _blender_not_available(*args, **kwargs):
        raise ImportError(
            "Blender Python API (bpy) is not available. "
            "Install Blender or run this in a Blender environment."
        )

    create_explosion_sequence = _blender_not_available
    clear_existing_explosions = _blender_not_available
    create_fire_particles = _blender_not_available
    create_debris_particles = _blender_not_available
    create_smoke_volume = _blender_not_available
    animate_explosion = _blender_not_available
    create_explosion_from_preset = _blender_not_available
    create_quick_explosion = _blender_not_available
    create_medium_explosion = _blender_not_available
    create_high_explosion = _blender_not_available

    __all__ = [
        'ExplosionConfig',
        'QualityPreset',
        'DEFAULT_CONFIGS',
        'ExplosionMaterials'
    ]
