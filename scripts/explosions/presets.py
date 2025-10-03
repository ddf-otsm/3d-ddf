"""
Explosion presets library for 3D-DDF system.
Provides pre-configured explosion types for quick setup.
"""

from typing import Dict, Any
from .config import ExplosionConfig, QualityPreset

PRESETS: Dict[str, Dict[str, Any]] = {
    "small_explosion": {
        "name": "Small_Explosion",
        "fire_particles": 10,
        "debris_particles": 5,
        "duration": 30,
        "intensity": 0.7,
        "quality_preset": QualityPreset.QUICK,
        "color_bias": "orange",
        "description": "Quick burst, minimal debris - ideal for background effects"
    },
    "medium_explosion": {
        "name": "Medium_Explosion",
        "fire_particles": 20,
        "debris_particles": 10,
        "duration": 60,
        "intensity": 1.0,
        "quality_preset": QualityPreset.MEDIUM,
        "color_bias": "red",
        "description": "Standard explosion - balanced for action sequences"
    },
    "large_explosion": {
        "name": "Large_Explosion",
        "fire_particles": 40,
        "debris_particles": 20,
        "duration": 120,
        "intensity": 1.5,
        "quality_preset": QualityPreset.HIGH,
        "color_bias": "yellow",
        "description": "Massive, long-lasting - for major impacts"
    },
    "fireball": {
        "name": "Fireball",
        "fire_particles": 30,
        "debris_particles": 2,
        "duration": 45,
        "intensity": 1.2,
        "quality_preset": QualityPreset.MEDIUM,
        "color_bias": "orange",
        "description": "Heavy fire, minimal smoke - pure combustion effect"
    },
    "dusty_explosion": {
        "name": "Dusty_Explosion",
        "fire_particles": 8,
        "debris_particles": 15,
        "duration": 90,
        "intensity": 0.8,
        "quality_preset": QualityPreset.MEDIUM,
        "color_bias": "gray",
        "description": "Heavy smoke/debris, minimal fire - dust cloud simulation"
    },
    "aerial_explosion": {
        "name": "Aerial_Explosion",
        "fire_particles": 25,
        "debris_particles": 8,
        "duration": 50,
        "intensity": 1.1,
        "quality_preset": QualityPreset.MEDIUM,
        "color_bias": "blue",
        "description": "No ground interaction - mid-air burst"
    },
    "ground_impact": {
        "name": "Ground_Impact",
        "fire_particles": 15,
        "debris_particles": 25,
        "duration": 75,
        "intensity": 1.3,
        "quality_preset": QualityPreset.HIGH,
        "color_bias": "brown",
        "description": "Heavy debris and dust cloud - surface explosion"
    }
}


def get_preset_config(
        preset_name: str,
        location: tuple = (
            0.0,
            0.0,
            0.0),
        start_frame: int = 1) -> ExplosionConfig:
    """
    Get an ExplosionConfig from a preset.

    Args:
        preset_name: Name of the preset
        location: Explosion position
        start_frame: Start frame for animation

    Returns:
        Configured ExplosionConfig
    """
    if preset_name not in PRESETS:
        raise ValueError(
            f"Unknown preset: {preset_name}. Available: {list(PRESETS.keys())}")

    preset = PRESETS[preset_name]
    config = ExplosionConfig(
        name=preset["name"],
        location=location,
        start_frame=start_frame,
        duration=preset["duration"],
        quality_preset=preset["quality_preset"],
        fire_particle_count=preset["fire_particles"],
        debris_particle_count=preset["debris_particles"],
        # Add intensity and color_bias if supported in config
    )
    print(f"🔥 Loaded preset: {preset_name} - {preset['description']}")
    return config


# Example usage in integration:
# config = get_preset_config("medium_explosion", location=(2, 2, 1), start_frame=50)
