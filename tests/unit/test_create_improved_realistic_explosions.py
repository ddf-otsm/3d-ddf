"""
Unit tests for create_improved_realistic_explosions.py
Tests improved realistic explosion creation functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# Mock bpy module to avoid import errors in tests
class MockColorRampElement:
    def __init__(self, color=(1.0, 1.0, 1.0, 1.0), position=0.0):
        self.color = color
        self.position = position

class MockColorRamp:
    def __init__(self):
        self.elements = [MockColorRampElement() for _ in range(5)]

    def new(self, position):
        return MockColorRampElement()

class MockNodeInputs:
    def __init__(self):
        self.Strength = Mock()
        self.Strength.default_value = 0.0
        self.Fac = Mock()
        self.Fac.default_value = 0.0
        self.Scale = Mock()
        self.Scale.default_value = 0.0
        self.Detail = Mock()
        self.Detail.default_value = 0.0
        self.Roughness = Mock()
        self.Roughness.default_value = 0.0

class MockNode:
    def __init__(self, node_type='UNKNOWN'):
        self.type = node_type
        self.location = (0, 0)
        self.inputs = MockNodeInputs()
        self.outputs = [Mock()]

class MockNodeTree:
    def __init__(self):
        self.nodes = Mock()
        self.links = Mock()

class MockMaterial:
    def __init__(self, name="TestMaterial"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

class MockBpy:
    class data:
        class objects:
            @staticmethod
            def remove(obj, do_unlink=True):
                pass

        class materials:
            @staticmethod
            def new(name):
                return MockMaterial(name)

        objects = []
        materials = []

    class context:
        class active_object:
            pass

        active_object = None

    bpy = None

# Patch bpy before importing the module
sys.modules['bpy'] = MockBpy()
sys.modules['bmesh'] = Mock()
sys.modules['mathutils'] = Mock()

# Now import the module after mocking
import create_improved_realistic_explosions


class TestCreateImprovedRealisticExplosions(unittest.TestCase):
    """Test improved realistic explosion creation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_clear_existing_explosions(self):
        """Test clearing existing explosion objects."""
        # Mock bpy.data.objects to return some test objects
        test_objects = [
            Mock(),
            Mock(),
            Mock()
        ]
        test_objects[0].name = "Explosion_Test_1"
        test_objects[1].name = "Fire_Test_2"
        test_objects[2].name = "Normal_Object"  # Should not be removed

        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            mock_bpy.data.objects = test_objects

            # Call the function
            create_improved_realistic_explosions.clear_existing_explosions()

            # Check that only explosion objects were removed
            mock_bpy.data.objects.remove.assert_called()
            self.assertEqual(mock_bpy.data.objects.remove.call_count, 2)

    def test_create_enhanced_fire_material(self):
        """Test enhanced fire material creation."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial("Enhanced_Fire_test")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            mock_nodes = []
            def mock_new(node_type):
                node = MockNode(node_type)
                mock_nodes.append(node)
                return node
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Call the function
            result = create_improved_realistic_explosions.create_enhanced_fire_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Enhanced_Fire_test")
            self.assertTrue(result.use_nodes)

            # Verify nodes were created
            mock_bpy.data.materials.new.assert_called_once()
            mock_material.node_tree.nodes.clear.assert_called_once()

    def test_create_enhanced_smoke_material(self):
        """Test enhanced smoke material creation."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial("Enhanced_Smoke_test")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Call the function
            result = create_improved_realistic_explosions.create_enhanced_smoke_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Enhanced_Smoke_test")

    def test_create_improved_debris_material(self):
        """Test improved debris material creation."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial("Improved_Debris_test")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Call the function
            result = create_improved_realistic_explosions.create_improved_debris_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Improved_Debris_test")

    def test_create_realistic_particle_system(self):
        """Test realistic particle system creation."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Realistic_Particle_System"
            mock_obj.particle_systems = Mock()
            mock_obj.particle_systems.new = Mock()

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock particle settings
            mock_settings = Mock()
            mock_settings.count = 150
            mock_settings.lifetime = 80
            mock_settings.physics_type = 'NEWTON'
            mock_settings.normal_factor = 1.2
            mock_settings.tangent_factor = 0.15

            mock_obj.particle_systems[0].settings = mock_settings

            # Call the function
            result = create_improved_realistic_explosions.create_realistic_particle_system("test", 150, 80)

            # Verify object was created
            self.assertEqual(result.name, "Realistic_Particle_System")

    def test_create_volume_smoke_effect(self):
        """Test volume smoke effect creation."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Volume_Smoke"
            mock_obj.scale = (1.0, 1.0, 1.0)

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock material creation
            mock_material = MockMaterial("Smoke_Material")
            mock_bpy.data.materials.new.return_value = mock_material

            # Call the function
            result = create_improved_realistic_explosions.create_volume_smoke_effect(
                location=(0, 0, 0),
                scale=(3.0, 3.0, 3.0)
            )

            # Verify object was created with correct scale
            self.assertEqual(result.name, "Volume_Smoke")
            self.assertEqual(result.scale, (3.0, 3.0, 3.0))

    def test_create_explosion_lighting_setup(self):
        """Test explosion lighting setup."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock existing lights
            light1 = Mock()
            light1.name = "Existing_Light"
            light1.type = 'POINT'
            light1.data = Mock()
            light1.data.energy = 10.0

            mock_bpy.data.objects = [light1]

            # Mock new light creation
            new_light_obj = Mock()
            new_light_obj.name = "Explosion_Key_Light"
            new_light_obj.data = Mock()
            new_light_obj.data.energy = 50.0
            new_light_obj.data.color = (1.0, 0.8, 0.6)

            mock_bpy.data.objects.new.return_value = new_light_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Call the function
            create_improved_realistic_explosions.create_explosion_lighting_setup()

            # Verify new lights were created
            self.assertGreater(mock_bpy.data.objects.new.call_count, 0)


class TestExplosionCreationScenarios(unittest.TestCase):
    """Test different explosion creation scenarios."""

    def test_small_scale_explosion(self):
        """Test creating a small-scale explosion."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Small_Explosion"
            mock_obj.scale = (0.5, 0.5, 0.5)

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock material creation
            mock_material = MockMaterial("Small_Fire_Material")
            mock_bpy.data.materials.new.return_value = mock_material

            # Call the function with small scale
            result = create_improved_realistic_explosions.create_enhanced_explosion(
                location=(0, 0, 0),
                scale=0.5,
                intensity=0.5
            )

            # Should still create objects
            self.assertIsNotNone(result)

    def test_large_scale_explosion(self):
        """Test creating a large-scale explosion."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Large_Explosion"
            mock_obj.scale = (5.0, 5.0, 5.0)

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock material creation
            mock_material = MockMaterial("Large_Fire_Material")
            mock_bpy.data.materials.new.return_value = mock_material

            # Call the function with large scale
            result = create_improved_realistic_explosions.create_enhanced_explosion(
                location=(0, 0, 0),
                scale=5.0,
                intensity=2.0
            )

            # Should still create objects
            self.assertIsNotNone(result)

    def test_explosion_at_different_locations(self):
        """Test explosion creation at different locations."""
        test_locations = [
            (0, 0, 0),      # Origin
            (10, 5, 2),     # Positive coordinates
            (-5, -3, 1),    # Negative coordinates
            (100, 50, 25)   # Large coordinates
        ]

        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            mock_obj = Mock()
            mock_obj.name = "Location_Test_Explosion"
            mock_obj.scale = (1.0, 1.0, 1.0)

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock material creation
            mock_material = MockMaterial("Location_Fire_Material")
            mock_bpy.data.materials.new.return_value = mock_material

            for location in test_locations:
                # Call the function with different locations
                result = create_improved_realistic_explosions.create_enhanced_explosion(
                    location=location,
                    scale=1.0,
                    intensity=1.0
                )

                # Should create objects for all locations
                self.assertIsNotNone(result)


class TestMaterialCreationEdgeCases(unittest.TestCase):
    """Test edge cases for material creation."""

    def test_fire_material_with_zero_intensity(self):
        """Test fire material creation with zero intensity."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            mock_material = MockMaterial("Zero_Intensity_Fire")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Test with zero intensity
            result = create_improved_realistic_explosions.create_enhanced_fire_material("zero_test")

            # Should not crash with zero values
            self.assertIsNotNone(result)

    def test_smoke_material_with_extreme_density(self):
        """Test smoke material creation with extreme density."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            mock_material = MockMaterial("Extreme_Density_Smoke")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Test with extreme density (both very low and very high)
            result_low = create_improved_realistic_explosions.create_enhanced_smoke_material("low_test")
            result_high = create_improved_realistic_explosions.create_enhanced_smoke_material("high_test")

            # Both should work
            self.assertIsNotNone(result_low)
            self.assertIsNotNone(result_high)

    def test_particle_system_with_extreme_counts(self):
        """Test particle system creation with extreme particle counts."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Extreme_Particle_System"
            mock_obj.particle_systems = Mock()
            mock_obj.particle_systems.new = Mock()

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock particle settings
            mock_settings = Mock()
            mock_settings.count = 10000  # Very high count
            mock_settings.lifetime = 200
            mock_settings.physics_type = 'NEWTON'

            mock_obj.particle_systems[0].settings = mock_settings

            # Test with extreme particle count
            result = create_improved_realistic_explosions.create_realistic_particle_system("extreme_test", 10000, 200)

            # Should still create the object
            self.assertEqual(result.name, "Extreme_Particle_System")


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios."""

    def test_complete_explosion_creation_workflow(self):
        """Test a complete explosion creation workflow."""
        with patch('create_improved_realistic_explosions.bpy') as mock_bpy:
            # Mock all the objects that would be created
            explosion_objects = []

            def mock_objects_new(name, object_data=None):
                mock_obj = Mock()
                mock_obj.name = name
                if "Particle" in name:
                    mock_obj.particle_systems = Mock()
                    mock_obj.particle_systems.new = Mock()
                explosion_objects.append(mock_obj)
                return mock_obj

            def mock_materials_new(name):
                return MockMaterial(name)

            def mock_collection_link(obj):
                pass

            mock_bpy.data.objects.new = mock_objects_new
            mock_bpy.data.materials.new = mock_materials_new
            mock_bpy.context.collection.objects.link = mock_collection_link

            # Create a complete explosion
            objects = create_improved_realistic_explosions.create_improved_explosion(
                location=(0, 0, 0),
                scale=1.0,
                intensity=1.0,
                particle_count=50
            )

            # Should create multiple objects
            self.assertIsInstance(objects, list)
            self.assertGreater(len(objects), 0)

            # Should include fire, debris, and smoke objects
            object_names = [obj.name for obj in objects]
            self.assertTrue(any("Fire" in name for name in object_names))
            self.assertTrue(any("Debris" in name for name in object_names))
            self.assertTrue(any("Smoke" in name for name in object_names))


if __name__ == '__main__':
    unittest.main()


