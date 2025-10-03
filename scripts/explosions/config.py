"""
Configuration classes for explosion creation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Optional

try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False


class QualityPreset(Enum):
    """Quality presets for explosion rendering."""

    QUICK = "quick"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ExplosionConfig:
    """Configuration for explosion creation."""

    # Basic parameters
    name: str = "Explosion"
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    start_frame: int = 1
    duration: int = 60

    # Quality settings
    quality_preset: QualityPreset = QualityPreset.MEDIUM

    # Fire particle settings
    fire_particle_count: int = 20
    fire_lifetime: float = 3.0
    fire_velocity: float = 2.0
    fire_scale: float = 1.0

    # Debris particle settings
    debris_particle_count: int = 10
    debris_lifetime: float = 5.0
    debris_velocity: float = 3.0
    debris_scale: float = 0.5

    # Smoke volume settings
    smoke_density: float = 0.8
    smoke_scale: Tuple[float, float, float] = (3.0, 3.0, 3.0)

    # Material settings
    fire_color_temperature: float = 1.0  # 0.0 = red, 1.0 = white
    smoke_color: Tuple[float, float, float, float] = (0.2, 0.2, 0.2, 0.8)

    # Render settings
    render_samples: int = 256
    render_resolution: Tuple[int, int] = (1920, 1080)

    # Animation settings
    camera_shake_intensity: float = 0.5
    camera_shake_frames: int = 10

    def __post_init__(self):
        """Apply quality preset settings."""
        if self.quality_preset == QualityPreset.QUICK:
            self.render_samples = 128
            self.fire_particle_count = 10
            self.debris_particle_count = 5
        elif self.quality_preset == QualityPreset.HIGH:
            self.render_samples = 512
            self.fire_particle_count = 30
            self.debris_particle_count = 15

    @classmethod
    def from_preset(cls, preset: QualityPreset, **kwargs) -> 'ExplosionConfig':
        """Create config from quality preset."""
        return cls(quality_preset=preset, **kwargs)


# Default configurations
DEFAULT_CONFIGS = {
    QualityPreset.QUICK: ExplosionConfig(quality_preset=QualityPreset.QUICK),
    QualityPreset.MEDIUM: ExplosionConfig(quality_preset=QualityPreset.MEDIUM),
    QualityPreset.HIGH: ExplosionConfig(quality_preset=QualityPreset.HIGH),
}
