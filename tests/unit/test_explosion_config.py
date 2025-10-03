"""
Unit tests for explosion configuration system.
"""

import unittest
from scripts.explosions.config import ExplosionConfig, QualityPreset, DEFAULT_CONFIGS


class TestQualityPreset(unittest.TestCase):
    """Test QualityPreset enum functionality."""

    def test_quality_preset_values(self):
        """Test that quality presets have correct values."""
        self.assertEqual(QualityPreset.QUICK.value, "quick")
        self.assertEqual(QualityPreset.MEDIUM.value, "medium")
        self.assertEqual(QualityPreset.HIGH.value, "high")

    def test_quality_preset_enum_members(self):
        """Test that all expected preset members exist."""
        self.assertTrue(hasattr(QualityPreset, 'QUICK'))
        self.assertTrue(hasattr(QualityPreset, 'MEDIUM'))
        self.assertTrue(hasattr(QualityPreset, 'HIGH'))


class TestExplosionConfig(unittest.TestCase):
    """Test ExplosionConfig dataclass functionality."""

    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = ExplosionConfig()

        self.assertEqual(config.name, "Explosion")
        self.assertEqual(config.location, (0.0, 0.0, 0.0))
        self.assertEqual(config.start_frame, 1)
        self.assertEqual(config.duration, 60)
        self.assertEqual(config.quality_preset, QualityPreset.MEDIUM)

    def test_custom_config_creation(self):
        """Test creating config with custom values."""
        config = ExplosionConfig(
            name="Custom_Explosion",
            location=(1.0, 2.0, 3.0),
            start_frame=10,
            duration=120,
            quality_preset=QualityPreset.HIGH
        )

        self.assertEqual(config.name, "Custom_Explosion")
        self.assertEqual(config.location, (1.0, 2.0, 3.0))
        self.assertEqual(config.start_frame, 10)
        self.assertEqual(config.duration, 120)
        self.assertEqual(config.quality_preset, QualityPreset.HIGH)

    def test_quality_preset_application(self):
        """Test that quality presets are applied correctly."""
        # Test quick preset
        quick_config = ExplosionConfig(quality_preset=QualityPreset.QUICK)
        self.assertEqual(quick_config.render_samples, 128)
        self.assertEqual(quick_config.fire_particle_count, 10)
        self.assertEqual(quick_config.debris_particle_count, 5)

        # Test high preset
        high_config = ExplosionConfig(quality_preset=QualityPreset.HIGH)
        self.assertEqual(high_config.render_samples, 512)
        self.assertEqual(high_config.fire_particle_count, 30)
        self.assertEqual(high_config.debris_particle_count, 15)

        # Test medium preset (default)
        medium_config = ExplosionConfig(quality_preset=QualityPreset.MEDIUM)
        self.assertEqual(medium_config.render_samples, 256)
        self.assertEqual(medium_config.fire_particle_count, 20)
        self.assertEqual(medium_config.debris_particle_count, 10)

    def test_from_preset_method(self):
        """Test creating config from preset class method."""
        config = ExplosionConfig.from_preset(
            QualityPreset.HIGH,
            name="High_Quality_Test",
            location=(5.0, 5.0, 5.0)
        )

        self.assertEqual(config.quality_preset, QualityPreset.HIGH)
        self.assertEqual(config.name, "High_Quality_Test")
        self.assertEqual(config.location, (5.0, 5.0, 5.0))
        self.assertEqual(config.render_samples, 512)

    def test_default_configs(self):
        """Test that default configurations are properly set up."""
        self.assertIn(QualityPreset.QUICK, DEFAULT_CONFIGS)
        self.assertIn(QualityPreset.MEDIUM, DEFAULT_CONFIGS)
        self.assertIn(QualityPreset.HIGH, DEFAULT_CONFIGS)

        # Test that default configs have correct presets
        self.assertEqual(DEFAULT_CONFIGS[QualityPreset.QUICK].quality_preset, QualityPreset.QUICK)
        self.assertEqual(DEFAULT_CONFIGS[QualityPreset.MEDIUM].quality_preset, QualityPreset.MEDIUM)
        self.assertEqual(DEFAULT_CONFIGS[QualityPreset.HIGH].quality_preset, QualityPreset.HIGH)


class TestExplosionConfigValidation(unittest.TestCase):
    """Test ExplosionConfig validation and edge cases."""

    def test_invalid_particle_counts(self):
        """Test that config handles edge cases properly."""
        # Zero particles should be allowed (for testing)
        config = ExplosionConfig(fire_particle_count=0, debris_particle_count=0)
        self.assertEqual(config.fire_particle_count, 0)
        self.assertEqual(config.debris_particle_count, 0)

    def test_negative_values(self):
        """Test that negative values are handled appropriately."""
        # Negative duration should be allowed (though not practical)
        config = ExplosionConfig(duration=-10)
        self.assertEqual(config.duration, -10)

    def test_large_values(self):
        """Test that large values don't cause issues."""
        config = ExplosionConfig(
            fire_particle_count=1000,
            debris_particle_count=500,
            duration=10000
        )
        self.assertEqual(config.fire_particle_count, 1000)
        self.assertEqual(config.debris_particle_count, 500)
        self.assertEqual(config.duration, 10000)


if __name__ == '__main__':
    unittest.main()


