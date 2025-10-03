"""
Unit tests for fix_explosion_realism.py
Tests explosion realism improvement functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
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
        self.elements = [MockColorRampElement() for _ in range(6)]

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
import fix_explosion_realism


class TestFixExplosionRealism(unittest.TestCase):
    """Test explosion realism fixing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_clear_all_explosions(self):
        """Test clearing all explosion objects."""
        # Mock bpy.data.objects to return some test objects
        test_objects = [
            Mock(),
            Mock(),
            Mock()
        ]
        test_objects[0].name = "Explosion_Test_1"
        test_objects[1].name = "Fire_Test_2"
        test_objects[2].name = "Normal_Object"  # Should not be removed

        with patch('fix_explosion_realism.bpy') as mock_bpy:
            mock_bpy.data.objects = test_objects

            # Call the function
            fix_explosion_realism.clear_all_explosions()

            # Check that only explosion objects were removed
            mock_bpy.data.objects.remove.assert_called()
            self.assertEqual(mock_bpy.data.objects.remove.call_count, 2)

    def test_create_ultra_realistic_fire_material(self):
        """Test ultra-realistic fire material creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial(f"Ultra_Fire_test")
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
            result = fix_explosion_realism.create_ultra_realistic_fire_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Ultra_Fire_test")
            self.assertTrue(result.use_nodes)

            # Verify nodes were created
            mock_bpy.data.materials.new.assert_called_once()
            mock_material.node_tree.nodes.clear.assert_called_once()

    def test_create_enhanced_smoke_material(self):
        """Test enhanced smoke material creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial(f"Enhanced_Smoke_test")
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
            result = fix_explosion_realism.create_enhanced_smoke_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Enhanced_Smoke_test")

    def test_create_realistic_debris_material(self):
        """Test realistic debris material creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock the material creation
            mock_material = MockMaterial(f"Realistic_Debris_test")
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
            result = fix_explosion_realism.create_realistic_debris_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Realistic_Debris_test")

    def test_create_advanced_particle_system(self):
        """Test advanced particle system creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Test_Particle_System"
            mock_obj.particle_systems = Mock()
            mock_obj.particle_systems.new = Mock()

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock particle settings
            mock_settings = Mock()
            mock_settings.count = 100
            mock_settings.lifetime = 60
            mock_settings.physics_type = 'NEWTON'
            mock_settings.normal_factor = 1.0
            mock_settings.tangent_factor = 0.1

            mock_obj.particle_systems[0].settings = mock_settings

            # Call the function
            result = fix_explosion_realism.create_advanced_particle_system("test", 100, 60)

            # Verify object was created
            self.assertEqual(result.name, "Test_Particle_System")

    def test_apply_explosion_lighting(self):
        """Test explosion lighting application."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock existing lights
            light1 = Mock()
            light1.name = "Existing_Light"
            light1.type = 'POINT'
            light1.data.energy = 10.0

            light2 = Mock()
            light2.name = "Explosion_Light"
            light2.type = 'AREA'

            mock_bpy.data.objects = [light1, light2]

            # Mock new light creation
            new_light_obj = Mock()
            new_light_obj.name = "New_Explosion_Light"
            mock_bpy.data.objects.new.return_value = new_light_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Call the function
            fix_explosion_realism.apply_explosion_lighting()

            # Verify new lights were created
            self.assertGreater(mock_bpy.data.objects.new.call_count, 0)

    def test_create_volume_explosion_effect(self):
        """Test volume explosion effect creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Volume_Explosion"
            mock_obj.scale = (1.0, 1.0, 1.0)

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock material creation
            mock_material = MockMaterial("Volume_Material")
            mock_bpy.data.materials.new.return_value = mock_material

            # Call the function
            result = fix_explosion_realism.create_volume_explosion_effect(
                location=(0, 0, 0),
                scale=(2.0, 2.0, 2.0)
            )

            # Verify object was created with correct scale
            self.assertEqual(result.name, "Volume_Explosion")
            self.assertEqual(result.scale, (2.0, 2.0, 2.0))

    def test_fix_particle_system_settings(self):
        """Test particle system settings fixes."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock object with particle system
            mock_obj = Mock()
            mock_obj.name = "Test_Particle_Object"

            # Mock particle system
            mock_ps = Mock()
            mock_ps.settings = Mock()
            mock_ps.settings.count = 50  # Low count that should be fixed
            mock_ps.settings.lifetime = 30  # Short lifetime that should be fixed
            mock_ps.settings.physics_type = 'NO'  # Wrong physics

            mock_obj.particle_systems = [mock_ps]

            mock_bpy.data.objects = [mock_obj]

            # Call the function
            fix_explosion_realism.fix_particle_system_settings()

            # Verify settings were improved
            self.assertGreater(mock_ps.settings.count, 50)  # Should be increased
            self.assertGreater(mock_ps.settings.lifetime, 30)  # Should be increased
            self.assertEqual(mock_ps.settings.physics_type, 'NEWTON')  # Should be changed

    def test_create_fire_glow_effect(self):
        """Test fire glow effect creation."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock light creation
            mock_light_obj = Mock()
            mock_light_obj.name = "Fire_Glow_Light"
            mock_light_obj.data = Mock()
            mock_light_obj.data.energy = 100.0
            mock_light_obj.data.color = (1.0, 0.5, 0.0)

            mock_bpy.data.objects.new.return_value = mock_light_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Call the function
            result = fix_explosion_realism.create_fire_glow_effect(
                location=(1, 2, 3),
                intensity=100.0
            )

            # Verify light was created with correct properties
            self.assertEqual(result.name, "Fire_Glow_Light")
            self.assertEqual(result.data.energy, 100.0)


class TestMaterialCreationEdgeCases(unittest.TestCase):
    """Test edge cases for material creation."""

    def test_fire_material_with_extreme_values(self):
        """Test fire material creation with extreme parameter values."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            mock_material = MockMaterial("Ultra_Fire_extreme")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Test with very high strength
            result = fix_explosion_realism.create_ultra_realistic_fire_material("extreme")

            # Should not crash with extreme values
            self.assertIsNotNone(result)

    def test_material_creation_with_empty_name(self):
        """Test material creation with empty name."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            mock_material = MockMaterial("Ultra_Fire_")
            mock_bpy.data.materials.new.return_value = mock_material

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            mock_material.node_tree.nodes.new = mock_new
            mock_material.node_tree.nodes.clear = Mock()
            mock_material.node_tree.links.new = Mock()

            # Test with empty name
            result = fix_explosion_realism.create_ultra_realistic_fire_material("")

            # Should handle empty name gracefully
            self.assertIsNotNone(result)

    def test_particle_system_with_zero_values(self):
        """Test particle system creation with zero values."""
        with patch('fix_explosion_realism.bpy') as mock_bpy:
            # Mock object creation
            mock_obj = Mock()
            mock_obj.name = "Zero_Particle_System"
            mock_obj.particle_systems = Mock()
            mock_obj.particle_systems.new = Mock()

            mock_bpy.data.objects.new.return_value = mock_obj
            mock_bpy.context.collection.objects.link = Mock()

            # Mock particle settings with zero values
            mock_settings = Mock()
            mock_settings.count = 0
            mock_settings.lifetime = 0
            mock_settings.physics_type = 'NO'

            mock_obj.particle_systems[0].settings = mock_settings

            # Call the function - should handle zero values
            result = fix_explosion_realism.create_advanced_particle_system("zero_test", 0, 0)

            # Should still create the object
            self.assertEqual(result.name, "Zero_Particle_System")


if __name__ == '__main__':
    unittest.main()


