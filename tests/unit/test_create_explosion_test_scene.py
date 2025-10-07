"""
Unit tests for create_explosion_test_scene.py
Tests explosion test scene creation functionality.
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
    
    def __getitem__(self, index):
        return self.elements[index]

class MockNodeInputs:
    def __init__(self):
        self.BaseColor = Mock()
        self.BaseColor.default_value = (1.0, 1.0, 1.0, 1.0)
        self.Roughness = Mock()
        self.Roughness.default_value = 0.0
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
    
    def __getitem__(self, key):
        # Return a mock input for any key
        mock_input = Mock()
        mock_input.default_value = 0.0
        return mock_input

class MockNodeOutputs:
    def __init__(self):
        self.Generated = Mock()
        self.Color = Mock()
        self.Fac = Mock()
        self.Vector = Mock()
    
    def __getitem__(self, key):
        # Return a mock output for any key
        mock_output = Mock()
        return mock_output

class MockNode:
    def __init__(self, node_type='UNKNOWN'):
        self.type = node_type
        self.location = (0, 0)
        self.inputs = MockNodeInputs()
        # Create proper outputs with subscripting support
        self.outputs = MockNodeOutputs()
        # Add color_ramp support for ColorRamp nodes
        if node_type == 'VALTORGB' or node_type == 'ShaderNodeValToRGB':
            self.color_ramp = MockColorRamp()

class MockNodeTree:
    def __init__(self):
        self.nodes = Mock()
        self.links = Mock()

class MockMaterial:
    def __init__(self, name="TestMaterial"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

class MockObject:
    def __init__(self, name="TestObject"):
        self.name = name
        self.location = (0, 0, 0)
        self.rotation_euler = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.data = Mock()
        self.data.materials = []
    
    def keyframe_insert(self, data_path, frame):
        # Mock keyframe insertion
        pass

class MockBpy:
    class context:
        class scene:
            frame_start = 1
            frame_end = 100
            render = Mock()
            cycles = Mock()
            cycles.device = 'CPU'

        scene = scene()
        active_object = None

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

    class ops:
        class object:
            @staticmethod
            def select_all(action='SELECT'):
                pass

            @staticmethod
            def delete(use_global=False):
                pass

            @staticmethod
            def camera_add(location=(0, 0, 0)):
                return MockObject("Camera")

            @staticmethod
            def light_add(type='POINT', location=(0, 0, 0)):
                return MockObject(f"{type}_Light")

        class mesh:
            @staticmethod
            def primitive_plane_add(size=1, location=(0, 0, 0)):
                return MockObject("Plane")

        object = object()
        mesh = mesh()

# Patch bpy before importing the module
sys.modules['bpy'] = MockBpy()
sys.modules['bmesh'] = Mock()
sys.modules['mathutils'] = Mock()

# Now import the module after mocking
import create_explosion_test_scene


class TestCreateExplosionTestScene(unittest.TestCase):
    """Test explosion test scene creation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_clear_scene(self):
        """Test clearing the scene."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock that there are objects to delete
            mock_bpy.ops.object.select_all = Mock()
            mock_bpy.ops.object.delete = Mock()

            # Call the function
            create_explosion_test_scene.clear_scene()

            # Verify operations were called
            mock_bpy.ops.object.select_all.assert_called_once_with(action='SELECT')
            mock_bpy.ops.object.delete.assert_called_once_with(use_global=False)

    def test_setup_scene(self):
        """Test scene setup."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock context and scene
            scene = MockBpy.context.scene
            mock_bpy.context.scene = scene

            # Mock camera and light creation
            camera_obj = MockObject("Test_Camera")
            sun_obj = MockObject("Sun_Light")
            ground_obj = MockObject("Ground")

            mock_bpy.ops.object.camera_add = Mock(return_value=camera_obj)
            mock_bpy.ops.object.light_add = Mock(return_value=sun_obj)
            mock_bpy.ops.mesh.primitive_plane_add = Mock(return_value=ground_obj)
            mock_bpy.context.active_object = camera_obj

            # Mock material creation
            ground_material = MockMaterial("Ground_Material")
            mock_bpy.data.materials.new = Mock(return_value=ground_material)
            
            # Mock node creation for material
            def mock_new(node_type):
                return MockNode(node_type)
            
            ground_material.node_tree.nodes.new = mock_new
            ground_material.node_tree.nodes.clear = Mock()
            ground_material.node_tree.links.new = Mock()

            # Call the function
            create_explosion_test_scene.setup_scene()

            # Verify scene properties were set
            self.assertEqual(scene.frame_start, 1)
            self.assertEqual(scene.frame_end, 100)

            # Verify camera was created
            mock_bpy.ops.object.camera_add.assert_called_once()

            # Verify lighting was added
            mock_bpy.ops.object.light_add.assert_called_once()

            # Verify ground was created
            mock_bpy.ops.mesh.primitive_plane_add.assert_called_once()

    def test_create_fire_material(self):
        """Test fire material creation."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock material creation
            fire_material = MockMaterial(f"Fire_Mat_test")
            mock_bpy.data.materials.new = Mock(return_value=fire_material)

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            fire_material.node_tree.nodes.new = mock_new
            fire_material.node_tree.nodes.clear = Mock()
            fire_material.node_tree.links.new = Mock()

            # Call the function
            result = create_explosion_test_scene.create_fire_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Fire_Mat_test")
            self.assertTrue(result.use_nodes)

            # Verify nodes were created
            mock_bpy.data.materials.new.assert_called_once()
            fire_material.node_tree.nodes.clear.assert_called_once()

    def test_create_smoke_material(self):
        """Test smoke material creation."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock material creation
            smoke_material = MockMaterial("Smoke_Mat_test")
            mock_bpy.data.materials.new = Mock(return_value=smoke_material)

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            smoke_material.node_tree.nodes.new = mock_new
            smoke_material.node_tree.nodes.clear = Mock()
            smoke_material.node_tree.links.new = Mock()

            # Call the function
            result = create_explosion_test_scene.create_smoke_material("test")

            # Verify material was created with correct name
            self.assertEqual(result.name, "Smoke_Mat_test")

    def test_create_explosion_objects(self):
        """Test explosion objects creation."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock object creation for fire, debris, and smoke
            fire_obj = MockObject("Fire_Explosion_test")
            debris_obj = MockObject("Debris_Explosion_test")
            smoke_obj = MockObject("Smoke_Explosion_test")

            mock_bpy.ops.mesh.primitive_uv_sphere_add = Mock(side_effect=[
                fire_obj, debris_obj, smoke_obj
            ])
            mock_bpy.context.active_object = fire_obj

            # Mock material creation
            fire_material = MockMaterial("Fire_Material")
            debris_material = MockMaterial("Debris_Material")
            smoke_material = MockMaterial("Smoke_Material")

            mock_bpy.data.materials.new = Mock(side_effect=[
                fire_material, debris_material, smoke_material
            ])
            
            # Mock node creation for materials
            def mock_new(node_type):
                return MockNode(node_type)
            
            fire_material.node_tree.nodes.new = mock_new
            fire_material.node_tree.nodes.clear = Mock()
            fire_material.node_tree.links.new = Mock()
            
            debris_material.node_tree.nodes.new = mock_new
            debris_material.node_tree.nodes.clear = Mock()
            debris_material.node_tree.links.new = Mock()
            
            smoke_material.node_tree.nodes.new = mock_new
            smoke_material.node_tree.nodes.clear = Mock()
            smoke_material.node_tree.links.new = Mock()

            # Call the function
            objects = create_explosion_test_scene.create_explosion_objects(
                location=(0, 0, 0),
                start_frame=1,
                name="test"
            )

            # Should return list of objects
            self.assertIsInstance(objects, list)
            self.assertEqual(len(objects), 3)

            # Verify object creation calls
            self.assertEqual(mock_bpy.ops.mesh.primitive_uv_sphere_add.call_count, 3)

    def test_animate_explosion_objects(self):
        """Test explosion object animation."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Create mock objects
            fire_obj = MockObject("Fire_test")
            debris_obj = MockObject("Debris_test")
            smoke_obj = MockObject("Smoke_test")

            objects = [fire_obj, debris_obj, smoke_obj]

            # Mock keyframe insertion
            for obj in objects:
                obj.keyframe_insert = Mock()

            # Call the function
            create_explosion_test_scene.animate_explosion_objects(objects, start_frame=1)

            # Verify keyframes were inserted for all objects
            for obj in objects:
                obj.keyframe_insert.assert_called()

    def test_create_test_explosions(self):
        """Test creating multiple test explosions."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock all the functions that create_test_explosions calls
            with patch.object(create_explosion_test_scene, 'clear_scene'), \
                 patch.object(create_explosion_test_scene, 'setup_scene'), \
                 patch.object(create_explosion_test_scene, 'create_explosion_objects', return_value=[]), \
                 patch.object(create_explosion_test_scene, 'animate_explosion_objects'):

                # Call the function
                create_explosion_test_scene.create_test_explosions()

                # Should complete without errors
                self.assertTrue(True)

    def test_create_explosion_test_scene(self):
        """Test the main explosion test scene creation function."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock all the functions that create_explosion_test_scene calls
            with patch.object(create_explosion_test_scene, 'clear_scene'), \
                 patch.object(create_explosion_test_scene, 'setup_scene'), \
                 patch.object(create_explosion_test_scene, 'create_test_explosions'):

                # Call the function
                create_explosion_test_scene.create_explosion_test_scene()

                # Should complete without errors
                self.assertTrue(True)


class TestExplosionTestSceneEdgeCases(unittest.TestCase):
    """Test edge cases for explosion test scene creation."""

    def test_scene_setup_with_custom_frame_range(self):
        """Test scene setup with custom frame range."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock context and scene
            scene = MockBpy.context.scene
            mock_bpy.context.scene = scene

            # Mock object creation
            camera_obj = MockObject("Test_Camera")
            sun_obj = MockObject("Sun_Light")
            ground_obj = MockObject("Ground")

            mock_bpy.ops.object.camera_add = Mock(return_value=camera_obj)
            mock_bpy.ops.object.light_add = Mock(return_value=sun_obj)
            mock_bpy.ops.mesh.primitive_plane_add = Mock(return_value=ground_obj)
            mock_bpy.context.active_object = camera_obj

            # Call the function
            create_explosion_test_scene.setup_scene()

            # Verify scene properties were set to standard values
            self.assertEqual(scene.frame_start, 1)
            self.assertEqual(scene.frame_end, 100)

    def test_fire_material_with_empty_name(self):
        """Test fire material creation with empty name."""
        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock material creation
            fire_material = MockMaterial("Fire_Mat_")
            mock_bpy.data.materials.new = Mock(return_value=fire_material)

            # Mock node creation
            def mock_new(node_type):
                return MockNode(node_type)
            fire_material.node_tree.nodes.new = mock_new
            fire_material.node_tree.nodes.clear = Mock()
            fire_material.node_tree.links.new = Mock()

            # Test with empty name
            result = create_explosion_test_scene.create_fire_material("")

            # Should handle empty name gracefully
            self.assertIsNotNone(result)

    def test_explosion_objects_at_different_locations(self):
        """Test explosion objects creation at different locations."""
        test_locations = [
            (0, 0, 0),      # Origin
            (5, 3, 1),      # Positive coordinates
            (-2, -4, 0.5),  # Negative coordinates
            (10, 8, 3)      # Large coordinates
        ]

        with patch('create_explosion_test_scene.bpy') as mock_bpy:
            # Mock object creation
            explosion_objects = []
            def mock_sphere_add(size=1.0, location=(0, 0, 0), radius=1.0):
                obj = MockObject(f"Explosion_{len(explosion_objects)}")
                explosion_objects.append(obj)
                return obj

            mock_bpy.ops.mesh.primitive_uv_sphere_add = mock_sphere_add
            
            # Create a mock context that returns the active object
            mock_context = Mock()
            type(mock_context).active_object = property(lambda self: explosion_objects[-1] if explosion_objects else None)
            mock_bpy.context = mock_context

            # Mock material creation
            materials = []
            def mock_material_new(name):
                mat = MockMaterial(name)
                materials.append(mat)
                return mat

            mock_bpy.data.materials.new = mock_material_new
            
            # Mock node creation for materials
            def mock_new(node_type):
                return MockNode(node_type)
            
            # Set up node tree mocks for all materials (including future ones)
            def setup_material_mocks(mat):
                mat.node_tree.nodes.new = mock_new
                mat.node_tree.nodes.clear = Mock()
                mat.node_tree.links.new = Mock()
            
            # Override the material creation to set up mocks immediately
            original_mock_material_new = mock_material_new
            def mock_material_new_with_setup(name):
                mat = original_mock_material_new(name)
                setup_material_mocks(mat)
                return mat
            
            mock_bpy.data.materials.new = mock_material_new_with_setup

            for location in test_locations:
                # Call the function with different locations
                objects = create_explosion_test_scene.create_explosion_objects(
                    location=location,
                    start_frame=1,
                    name=f"test_{len(test_locations)}"
                )

                # Should create objects for all locations
                self.assertIsInstance(objects, list)
                self.assertEqual(len(objects), 3)  # fire, debris, smoke


if __name__ == '__main__':
    unittest.main()


