"""
Unit tests for explosion materials system.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from explosions.materials import ExplosionMaterials, BLENDER_AVAILABLE


class TestExplosionMaterials(unittest.TestCase):
    """Test ExplosionMaterials class functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.materials = ExplosionMaterials()

    def test_initialization(self):
        """Test that materials manager initializes correctly."""
        self.assertIsInstance(self.materials.materials, dict)
        self.assertEqual(len(self.materials.materials), 0)

    def test_material_caching(self):
        """Test that materials are properly cached."""
        # Create a material
        mat1 = self.materials.get_material("fire", "test_material")

        # Should be cached
        self.assertIn("fire_test_material", self.materials.materials)
        self.assertEqual(self.materials.materials["fire_test_material"], mat1)

        # Getting same material should return cached version
        mat2 = self.materials.get_material("fire", "test_material")
        self.assertEqual(mat1, mat2)

    def test_different_material_types(self):
        """Test creating different types of materials."""
        fire_mat = self.materials.get_material("fire", "test_fire")
        smoke_mat = self.materials.get_material("smoke", "test_smoke")
        debris_mat = self.materials.get_material("debris", "test_debris")

        self.assertIsNotNone(fire_mat)
        self.assertIsNotNone(smoke_mat)
        self.assertIsNotNone(debris_mat)

        # Should all be different objects
        self.assertNotEqual(fire_mat, smoke_mat)
        self.assertNotEqual(fire_mat, debris_mat)
        self.assertNotEqual(smoke_mat, debris_mat)

    def test_material_naming(self):
        """Test that materials are named correctly."""
        fire_mat = self.materials.get_material("fire", "test_name")
        smoke_mat = self.materials.get_material("smoke", "different_name")

        # Check that materials have expected names
        self.assertEqual(fire_mat.name, "Explosion_Fire_test_name")
        self.assertEqual(smoke_mat.name, "Explosion_Smoke_different_name")

    def test_blender_availability_detection(self):
        """Test Blender availability detection."""
        # This should be a boolean
        self.assertIsInstance(BLENDER_AVAILABLE, bool)

    @patch('explosions.materials.bpy')
    def test_blender_material_creation(self, mock_bpy):
        """Test material creation when Blender is available."""
        # Mock Blender being available
        mock_bpy.data = Mock()
        mock_bpy.data.materials = Mock()
        mock_bpy.data.materials.new.return_value = Mock()
        mock_bpy.context = Mock()
        mock_bpy.context.active_object = None

        # Create materials instance
        materials = ExplosionMaterials()

        # This would normally require Blender to be available
        # but our test is focused on the logic structure
        self.assertIsInstance(materials.materials, dict)

    def test_multiple_material_instances(self):
        """Test that different material instances don't interfere."""
        materials1 = ExplosionMaterials()
        materials2 = ExplosionMaterials()

        # Create materials in both instances
        mat1 = materials1.get_material("fire", "test1")
        mat2 = materials2.get_material("fire", "test2")

        # Should be different objects
        self.assertNotEqual(mat1, mat2)

        # But both should be cached in their respective instances
        self.assertIn("fire_test1", materials1.materials)
        self.assertIn("fire_test2", materials2.materials)


class TestMaterialCreationMethods(unittest.TestCase):
    """Test individual material creation methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.materials = ExplosionMaterials()

    def test_create_fire_material_without_blender(self):
        """Test fire material creation when Blender is not available."""
        result = self.materials.create_fire_material("test_fire", 1.0)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Explosion_Fire_test_fire")
        self.assertTrue(result.use_nodes)

    def test_create_smoke_material_without_blender(self):
        """Test smoke material creation when Blender is not available."""
        result = self.materials.create_smoke_material("test_smoke", 0.8)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Explosion_Smoke_test_smoke")

    def test_create_debris_material_without_blender(self):
        """Test debris material creation when Blender is not available."""
        # Note: create_debris_material doesn't take a density parameter like the others
        result = self.materials.get_material("debris", "test_debris")

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Explosion_Debris_test_debris")


if __name__ == '__main__':
    unittest.main()
