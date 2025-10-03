"""
Unit tests for explosion creation system.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from explosions.config import ExplosionConfig, QualityPreset
from explosions.create_production_explosion import (
    clear_existing_explosions,
    create_explosion_sequence,
    BLENDER_AVAILABLE
)


class TestExplosionCreation(unittest.TestCase):
    """Test explosion creation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = ExplosionConfig(
            name="Test_Explosion",
            location=(0.0, 0.0, 0.0),
            quality_preset=QualityPreset.MEDIUM
        )

    def test_clear_existing_explosions_without_blender(self):
        """Test clearing explosions when Blender is not available."""
        # Should not raise an exception
        try:
            clear_existing_explosions()
        except Exception as e:
            self.fail(f"clear_existing_explosions() raised {type(e).__name__} unexpectedly")

    def test_create_explosion_sequence_without_blender(self):
        """Test explosion sequence creation when Blender is not available."""
        result = create_explosion_sequence(self.test_config)

        # Should return simulated object names
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Check that expected object types are included
        object_names = [obj for obj in result if isinstance(obj, str)]
        self.assertTrue(any("Fire" in name for name in object_names))
        self.assertTrue(any("Debris" in name for name in object_names))
        self.assertTrue(any("Smoke" in name for name in object_names))

    def test_explosion_sequence_with_custom_config(self):
        """Test explosion creation with custom configuration."""
        custom_config = ExplosionConfig(
            name="Custom_Test",
            location=(1.0, 2.0, 3.0),
            fire_particle_count=50,
            debris_particle_count=25,
            duration=120
        )

        result = create_explosion_sequence(custom_config)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_explosion_sequence_different_quality_presets(self):
        """Test explosion creation with different quality presets."""
        presets = [QualityPreset.QUICK, QualityPreset.MEDIUM, QualityPreset.HIGH]

        for preset in presets:
            config = ExplosionConfig(quality_preset=preset, name=f"Test_{preset.value}")
            result = create_explosion_sequence(config)

            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_blender_availability_detection(self):
        """Test Blender availability detection."""
        # This should be a boolean
        self.assertIsInstance(BLENDER_AVAILABLE, bool)

    def test_explosion_config_validation(self):
        """Test that explosion creation validates configuration."""
        # Test with minimal config
        minimal_config = ExplosionConfig(
            name="Minimal",
            fire_particle_count=1,
            debris_particle_count=1,
            duration=1
        )

        result = create_explosion_sequence(minimal_config)
        self.assertIsInstance(result, list)

    def test_multiple_explosion_creations(self):
        """Test creating multiple explosions in sequence."""
        configs = [
            ExplosionConfig(name="Explosion_1", quality_preset=QualityPreset.QUICK),
            ExplosionConfig(name="Explosion_2", quality_preset=QualityPreset.MEDIUM),
            ExplosionConfig(name="Explosion_3", quality_preset=QualityPreset.HIGH)
        ]

        all_objects = []
        for config in configs:
            objects = create_explosion_sequence(config)
            all_objects.extend(objects)

        self.assertGreater(len(all_objects), 0)

        # Each explosion should have multiple objects
        self.assertGreaterEqual(len(all_objects), len(configs) * 3)


class TestExplosionCreationEdgeCases(unittest.TestCase):
    """Test edge cases for explosion creation."""

    def test_zero_particle_config(self):
        """Test explosion creation with zero particles."""
        zero_config = ExplosionConfig(
            name="Zero_Test",
            fire_particle_count=0,
            debris_particle_count=0,
            duration=1
        )

        result = create_explosion_sequence(zero_config)
        self.assertIsInstance(result, list)
        # Should still return some objects (smoke volume, etc.)

    def test_negative_coordinates(self):
        """Test explosion creation with negative coordinates."""
        negative_config = ExplosionConfig(
            name="Negative_Test",
            location=(-10.0, -20.0, -30.0)
        )

        result = create_explosion_sequence(negative_config)
        self.assertIsInstance(result, list)

    def test_very_large_explosion(self):
        """Test explosion creation with very large scale."""
        large_config = ExplosionConfig(
            name="Large_Test",
            location=(0.0, 0.0, 0.0),
            fire_particle_count=1000,
            debris_particle_count=500,
            duration=1000
        )

        result = create_explosion_sequence(large_config)
        self.assertIsInstance(result, list)

    def test_very_small_explosion(self):
        """Test explosion creation with very small scale."""
        small_config = ExplosionConfig(
            name="Small_Test",
            location=(0.0, 0.0, 0.0),
            fire_particle_count=1,
            debris_particle_count=1,
            duration=1
        )

        result = create_explosion_sequence(small_config)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()


