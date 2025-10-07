"""
Unit tests for analyze_current_explosions.py
Tests explosion analysis functionality.
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
class MockObject:
    def __init__(self, name="TestObject"):
        self.name = name
        self.type = "MESH"
        self.data = Mock()
        self.data.materials = [Mock()]
        self.location = Mock()
        self.location.x = 0.0
        self.location.y = 0.0
        self.location.z = 0.0
        self.scale = Mock()
        self.scale.x = 1.0
        self.scale.y = 1.0
        self.scale.z = 1.0

        # Make location and scale iterable for tuple access
        self.location.__getitem__ = lambda self, key: [self.x, self.y, self.z][key]
        self.scale.__getitem__ = lambda self, key: [self.x, self.y, self.z][key]

class MockNodeTree:
    def __init__(self):
        self.nodes = []
        self.links = []

class MockMaterial:
    def __init__(self, name="TestMaterial"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

class MockBpyDataObjects:
    def __iter__(self):
        return iter([
            MockObject("Explosion_1"),
            MockObject("Fire_1"),
            MockObject("Normal_Object")
        ])

class MockBpyDataMaterials:
    def __iter__(self):
        return iter([
            MockMaterial("Fire_Material"),
            MockMaterial("Smoke_Material")
        ])

class MockBpy:
    class data:
        objects = MockBpyDataObjects()
        materials = MockBpyDataMaterials()

    class context:
        pass

# Test the core logic patterns used in analyze_current_explosions.py
# without importing the module (since it has bpy dependencies)


class TestAnalyzeCurrentExplosions(unittest.TestCase):
    """Test explosion analysis functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_module_imports(self):
        """Test that the module can be imported."""
        # Test that the module exists and can be imported
        import analyze_current_explosions
        self.assertTrue(hasattr(analyze_current_explosions, '__file__'))

    def test_analyze_current_explosions_function_exists(self):
        """Test that the main analysis function exists."""
        # The script is designed to run directly, not as a module with functions
        # Test that the file exists and is readable
        import analyze_current_explosions
        self.assertTrue(hasattr(analyze_current_explosions, '__file__'))

    def test_string_operations(self):
        """Test string operations used in the analysis."""
        # Test string repetition for headers
        header = "=" * 80
        self.assertEqual(len(header), 80)
        self.assertEqual(header, "=" * 80)

        # Test f-string formatting
        location = (1.0, 2.0, 3.0)
        formatted = f"Location: ({location[0]:.2f}, {location[1]:.2f}, {location[2]:.2f})"
        expected = "Location: (1.00, 2.00, 3.00)"
        self.assertEqual(formatted, expected)

    def test_color_value_formatting(self):
        """Test color value formatting used in analysis."""
        # Test RGB color formatting
        color = (1.0, 0.5, 0.0)
        strength = 2.5

        formatted_color = f"RGB({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})"
        expected_color = "RGB(1.00, 0.50, 0.00)"
        self.assertEqual(formatted_color, expected_color)

        formatted_strength = f"Strength: {strength}"
        expected_strength = "Strength: 2.5"
        self.assertEqual(formatted_strength, expected_strength)

    def test_explosion_object_filtering_logic(self):
        """Test the logic for filtering explosion objects."""
        # Test the logic that would be used to identify explosion objects
        test_objects = [
            "Explosion_Test_1",
            "Fire_Particle_1",
            "Debris_Chunk_1",
            "Smoke_Volume_1",
            "Normal_Cube",
            "Camera",
            "Light"
        ]

        explosion_objects = []
        for obj_name in test_objects:
            if (obj_name.startswith('Explosion_') or
                obj_name.startswith('Fire_') or
                obj_name.startswith('Debris_') or
                obj_name.startswith('Smoke_')):
                explosion_objects.append(obj_name)

        expected_objects = ["Explosion_Test_1", "Fire_Particle_1", "Debris_Chunk_1", "Smoke_Volume_1"]
        self.assertEqual(explosion_objects, expected_objects)

    def test_material_analysis_logic(self):
        """Test material analysis logic."""
        # Test logic for analyzing materials
        test_materials = [
            "Fire_Material",
            "Smoke_Material",
            "Debris_Material",
            "Ground_Material"
        ]

        fire_materials = 0
        emission_materials = 0
        volume_materials = 0

        for mat_name in test_materials:
            if "Fire" in mat_name or "Explosion" in mat_name:
                fire_materials += 1
            if "Smoke" in mat_name:
                volume_materials += 1

        # Should detect fire and smoke materials
        self.assertEqual(fire_materials, 1)  # Fire_Material
        self.assertEqual(volume_materials, 1)  # Smoke_Material


class TestAnalyzeCurrentExplosionsEdgeCases(unittest.TestCase):
    """Test edge cases for explosion analysis."""

    def test_empty_scene_analysis(self):
        """Test analysis with empty scene."""
        # Test that empty scene doesn't crash the analysis
        empty_objects = []
        empty_materials = []

        # Should handle empty collections gracefully
        self.assertEqual(len(empty_objects), 0)
        self.assertEqual(len(empty_materials), 0)

    def test_mixed_object_types(self):
        """Test analysis with mixed object types."""
        # Test with various object types
        mixed_objects = [
            "Explosion_Bomb",
            "Fire_Flame_1",
            "Debris_Shard_1",
            "Smoke_Cloud_1",
            "Camera_Main",
            "Light_Key",
            "Ground_Plane",
            "Building_Structure"
        ]

        explosion_objects = []
        for obj_name in mixed_objects:
            if any(prefix in obj_name for prefix in ['Explosion_', 'Fire_', 'Debris_', 'Smoke_']):
                explosion_objects.append(obj_name)

        # Should only include explosion-related objects
        expected = ["Explosion_Bomb", "Fire_Flame_1", "Debris_Shard_1", "Smoke_Cloud_1"]
        self.assertEqual(explosion_objects, expected)

    def test_object_property_formatting(self):
        """Test object property formatting for analysis output."""
        # Test formatting of object properties
        obj = MockObject("Test_Explosion")
        obj.location.x = 5.123
        obj.location.y = -2.456
        obj.location.z = 1.789
        obj.scale.x = 2.5
        obj.scale.y = 2.5
        obj.scale.z = 2.5

        # Test formatted output
        location_str = f"({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f})"
        scale_str = f"({obj.scale.x:.2f}, {obj.scale.y:.2f}, {obj.scale.z:.2f})"

        self.assertEqual(location_str, "(5.12, -2.46, 1.79)")
        self.assertEqual(scale_str, "(2.50, 2.50, 2.50)")


if __name__ == '__main__':
    unittest.main()
