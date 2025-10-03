"""
Integration tests for explosion system.
Tests the complete explosion creation workflow without requiring Blender.
"""

import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import sys

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from explosions.config import ExplosionConfig, QualityPreset
from explosions.materials import ExplosionMaterials


class TestExplosionIntegration(unittest.TestCase):
    """Test integration between explosion components."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = ExplosionConfig(
            name="Test_Explosion",
            location=(0.0, 0.0, 0.0),
            quality_preset=QualityPreset.MEDIUM
        )

    def test_config_and_materials_integration(self):
        """Test that config and materials work together."""
        # Create materials manager
        materials = ExplosionMaterials()

        # Test that materials can be created for different types
        fire_mat = materials.get_material("fire", "test_fire")
        smoke_mat = materials.get_material("smoke", "test_smoke")
        debris_mat = materials.get_material("debris", "test_debris")

        # Materials should be created and cached
        self.assertIsNotNone(fire_mat)
        self.assertIsNotNone(smoke_mat)
        self.assertIsNotNone(debris_mat)

        # Test caching - same material should be returned
        fire_mat2 = materials.get_material("fire", "test_fire")
        self.assertEqual(fire_mat, fire_mat2)

    def test_material_creation_without_blender(self):
        """Test material creation when Blender is not available."""
        materials = ExplosionMaterials()

        # Create a fire material
        result = materials.create_fire_material("test_fire", 1.0)

        # Should return a mock material when Blender is not available
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Explosion_Fire_test_fire")

    def test_config_validation(self):
        """Test that configuration validation works correctly."""
        # Test valid config
        valid_config = ExplosionConfig(
            name="Valid_Test",
            fire_particle_count=10,
            debris_particle_count=5,
            duration=60
        )
        self.assertEqual(valid_config.fire_particle_count, 10)
        self.assertEqual(valid_config.debris_particle_count, 5)

        # Test edge cases
        edge_config = ExplosionConfig(
            fire_particle_count=0,
            debris_particle_count=0,
            duration=1
        )
        self.assertEqual(edge_config.fire_particle_count, 0)
        self.assertEqual(edge_config.debris_particle_count, 0)

    def test_quality_preset_integration(self):
        """Test that quality presets work correctly across the system."""
        presets = [QualityPreset.QUICK, QualityPreset.MEDIUM, QualityPreset.HIGH]

        for preset in presets:
            config = ExplosionConfig(quality_preset=preset)

            # Each preset should have different settings
            if preset == QualityPreset.QUICK:
                self.assertEqual(config.render_samples, 128)
                self.assertEqual(config.fire_particle_count, 10)
            elif preset == QualityPreset.MEDIUM:
                self.assertEqual(config.render_samples, 256)
                self.assertEqual(config.fire_particle_count, 20)
            elif preset == QualityPreset.HIGH:
                self.assertEqual(config.render_samples, 512)
                self.assertEqual(config.fire_particle_count, 30)

    def test_explosion_workflow_simulation(self):
        """Simulate a complete explosion creation workflow."""
        # Step 1: Create configuration
        config = ExplosionConfig(
            name="Workflow_Test",
            location=(1.0, 2.0, 3.0),
            quality_preset=QualityPreset.MEDIUM
        )

        # Step 2: Initialize materials manager
        materials = ExplosionMaterials()

        # Step 3: Create materials for different components
        fire_mat = materials.create_fire_material("workflow_fire", 0.8)
        smoke_mat = materials.create_smoke_material("workflow_smoke", 0.7)
        debris_mat = materials.create_debris_material("workflow_debris")

        # Step 4: Verify all components are ready
        self.assertIsNotNone(fire_mat)
        self.assertIsNotNone(smoke_mat)
        self.assertIsNotNone(debris_mat)

        # Step 5: Verify configuration is valid for the workflow
        self.assertEqual(config.name, "Workflow_Test")
        self.assertEqual(config.location, (1.0, 2.0, 3.0))
        self.assertEqual(config.quality_preset, QualityPreset.MEDIUM)


class TestExplosionPerformance(unittest.TestCase):
    """Test performance aspects of the explosion system."""

    def test_config_creation_performance(self):
        """Test that config creation is fast."""
        import time

        start_time = time.time()
        for i in range(100):
            config = ExplosionConfig(
                name=f"Perf_Test_{i}",
                location=(i, i, i),
                quality_preset=QualityPreset.MEDIUM
            )
        end_time = time.time()

        # Should be able to create 100 configs in under 0.1 seconds
        self.assertLess(end_time - start_time, 0.1)

    def test_material_creation_performance(self):
        """Test that material creation is reasonably fast."""
        import time

        materials = ExplosionMaterials()

        start_time = time.time()
        for i in range(10):
            fire_mat = materials.create_fire_material(f"perf_fire_{i}", 1.0)
            smoke_mat = materials.create_smoke_material(f"perf_smoke_{i}", 0.8)
            debris_mat = materials.create_debris_material(f"perf_debris_{i}")
        end_time = time.time()

        # Should be able to create 30 materials in under 0.5 seconds
        self.assertLess(end_time - start_time, 0.5)


class TestExplosionErrorHandling(unittest.TestCase):
    """Test error handling in the explosion system."""

    def test_invalid_material_type(self):
        """Test handling of invalid material types."""
        materials = ExplosionMaterials()

        # Should return None for invalid material type
        result = materials.get_material("invalid_type", "test")
        self.assertIsNone(result)

    def test_config_with_extreme_values(self):
        """Test that extreme configuration values are handled gracefully."""
        # Test with very large numbers
        extreme_config = ExplosionConfig(
            fire_particle_count=10000,
            debris_particle_count=5000,
            duration=100000,
            render_samples=10000
        )

        # Should not crash and should store the values
        self.assertEqual(extreme_config.fire_particle_count, 10000)
        self.assertEqual(extreme_config.debris_particle_count, 5000)
        self.assertEqual(extreme_config.duration, 100000)
        self.assertEqual(extreme_config.render_samples, 10000)


if __name__ == '__main__':
    unittest.main()
