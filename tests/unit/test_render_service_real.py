"""
Unit tests for render_service.py (real module)
Tests actual render service functionality with proper bpy mocking.
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
class MockRenderEngine:
    def __init__(self):
        self.cycles = Mock()
        self.cycles.samples = 128
        self.eevee = Mock()
        self.eevee.samples = 64

class MockScene:
    def __init__(self):
        self.render = Mock()
        self.render.engine = 'CYCLES'
        self.render.resolution_percentage = 100
        self.frame_start = 1
        self.frame_end = 240
        self.render.filepath = "/tmp/output"
        self.render.image_settings = Mock()
        self.render.image_settings.file_format = 'PNG'

class MockBpy:
    class context:
        class scene:
            pass
        scene = MockScene()

    class data:
        class scenes:
            @staticmethod
            def new(name):
                return MockScene()

    bpy = None

# Patch bpy before importing the module
sys.modules['bpy'] = MockBpy()

# Now import the module after mocking
import render_service


class TestRenderServiceReal(unittest.TestCase):
    """Test real render service functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_quality_presets_configuration(self):
        """Test that quality presets are properly configured."""
        # Test that all expected presets exist
        expected_presets = ['draft', 'preview', 'production', 'final']
        for preset in expected_presets:
            self.assertIn(preset, render_service.QUALITY_PRESETS)

        # Test preset values
        draft = render_service.QUALITY_PRESETS['draft']
        self.assertEqual(draft['samples'], 32)
        self.assertEqual(draft['resolution_percentage'], 50)

        production = render_service.QUALITY_PRESETS['production']
        self.assertEqual(production['samples'], 128)
        self.assertEqual(production['resolution_percentage'], 100)

        final = render_service.QUALITY_PRESETS['final']
        self.assertEqual(final['samples'], 256)
        self.assertEqual(final['resolution_percentage'], 100)

    def test_material_styles_configuration(self):
        """Test that material styles are properly configured."""
        expected_styles = ['default', 'photorealistic', 'clay']
        for style in expected_styles:
            self.assertIn(style, render_service.MATERIAL_STYLES)

    def test_parse_args_with_defaults(self):
        """Test argument parsing with default values."""
        args = render_service.parse_args([])

        self.assertEqual(args.engine, 'CYCLES')
        self.assertEqual(args.quality, 'production')
        self.assertEqual(args.materials, 'photorealistic')
        self.assertEqual(args.start, 1)
        self.assertEqual(args.end, 240)
        self.assertIsNone(args.output_name)

    def test_parse_args_with_custom_values(self):
        """Test argument parsing with custom values."""
        test_args = [
            '--engine', 'EEVEE',
            '--quality', 'draft',
            '--materials', 'clay',
            '--start', '10',
            '--end', '50',
            '--output-name', 'custom_output'
        ]

        args = render_service.parse_args(test_args)

        self.assertEqual(args.engine, 'EEVEE')
        self.assertEqual(args.quality, 'draft')
        self.assertEqual(args.materials, 'clay')
        self.assertEqual(args.start, 10)
        self.assertEqual(args.end, 50)
        self.assertEqual(args.output_name, 'custom_output')

    def test_apply_quality_preset_draft(self):
        """Test applying draft quality preset."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock scene
            scene = MockScene()
            mock_bpy.context.scene = scene

            # Apply draft preset
            render_service.apply_quality_preset('draft')

            # Check that scene settings were updated for draft
            self.assertEqual(scene.render.resolution_percentage, 50)
            # Engine should remain CYCLES for draft

    def test_apply_quality_preset_final(self):
        """Test applying final quality preset."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock scene
            scene = MockScene()
            mock_bpy.context.scene = scene

            # Apply final preset
            render_service.apply_quality_preset('final')

            # Check that scene settings were updated for final
            self.assertEqual(scene.render.resolution_percentage, 100)

    def test_apply_material_style_photorealistic(self):
        """Test applying photorealistic material style."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock scene objects
            mock_obj1 = Mock()
            mock_obj1.name = "TestObject1"
            mock_obj1.data = Mock()
            mock_obj1.data.materials = [Mock()]

            mock_obj2 = Mock()
            mock_obj2.name = "TestObject2"
            mock_obj2.data = Mock()
            mock_obj2.data.materials = [Mock()]

            mock_bpy.data.objects = [mock_obj1, mock_obj2]

            # Apply photorealistic style
            render_service.apply_material_style('photorealistic')

            # Should not crash (materials would be modified in real implementation)
            self.assertTrue(True)

    def test_apply_material_style_clay(self):
        """Test applying clay material style."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock scene objects
            mock_obj = Mock()
            mock_obj.name = "TestObject"
            mock_obj.data = Mock()
            mock_obj.data.materials = [Mock()]

            mock_bpy.data.objects = [mock_obj]

            # Apply clay style
            render_service.apply_material_style('clay')

            # Should not crash
            self.assertTrue(True)

    def test_setup_output_path_with_timestamp(self):
        """Test output path setup with timestamp."""
        output_dir = Path(self.temp_dir.name) / "renders"
        output_dir.mkdir()

        # Test without custom name (should use timestamp)
        result1 = render_service.setup_output_path(output_dir=str(output_dir))

        # Test with custom name
        result2 = render_service.setup_output_path(
            output_dir=str(output_dir),
            custom_name="custom_render"
        )

        # Both should be valid paths
        self.assertTrue(os.path.exists(os.path.dirname(result1)) or result1.startswith(str(output_dir)))
        self.assertIn("custom_render", result2)

    def test_setup_output_path_with_frame_number(self):
        """Test output path setup with frame number."""
        output_dir = Path(self.temp_dir.name) / "renders"
        output_dir.mkdir()

        result = render_service.setup_output_path(
            output_dir=str(output_dir),
            custom_name="test_output",
            frame_number=25
        )

        # Should include frame number in path
        self.assertIn("25", result)

    def test_validate_frame_range_valid(self):
        """Test frame range validation with valid ranges."""
        # Test valid frame range
        self.assertTrue(render_service.validate_frame_range(1, 100))
        self.assertTrue(render_service.validate_frame_range(10, 20))

    def test_validate_frame_range_invalid(self):
        """Test frame range validation with invalid ranges."""
        # Test invalid frame ranges
        self.assertFalse(render_service.validate_frame_range(100, 1))  # End before start
        self.assertFalse(render_service.validate_frame_range(-1, 100))  # Negative start
        self.assertFalse(render_service.validate_frame_range(1, 0))     # Zero end
        self.assertFalse(render_service.validate_frame_range(0, 0))     # Zero range

    def test_calculate_render_time_estimate_different_presets(self):
        """Test render time estimation for different presets."""
        frame_count = 100

        # Test different quality presets
        estimate_draft = render_service.calculate_render_time_estimate(
            frame_count=frame_count,
            quality_preset='draft'
        )

        estimate_production = render_service.calculate_render_time_estimate(
            frame_count=frame_count,
            quality_preset='production'
        )

        estimate_final = render_service.calculate_render_time_estimate(
            frame_count=frame_count,
            quality_preset='final'
        )

        # Higher quality should take longer
        self.assertLess(estimate_draft, estimate_production)
        self.assertLess(estimate_production, estimate_final)

        # All should be positive numbers
        self.assertGreater(estimate_draft, 0)
        self.assertGreater(estimate_production, 0)
        self.assertGreater(estimate_final, 0)

    def test_calculate_render_time_estimate_different_frame_counts(self):
        """Test render time estimation for different frame counts."""
        # Test different frame counts with same quality
        estimate_small = render_service.calculate_render_time_estimate(
            frame_count=10,
            quality_preset='production'
        )

        estimate_medium = render_service.calculate_render_time_estimate(
            frame_count=100,
            quality_preset='production'
        )

        estimate_large = render_service.calculate_render_time_estimate(
            frame_count=1000,
            quality_preset='production'
        )

        # More frames should take longer
        self.assertLess(estimate_small, estimate_medium)
        self.assertLess(estimate_medium, estimate_large)

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        # Should have a main function
        self.assertTrue(hasattr(render_service, 'main'))
        self.assertTrue(callable(render_service.main))


class TestRenderServiceIntegration(unittest.TestCase):
    """Test render service integration scenarios."""

    def test_full_render_pipeline_simulation(self):
        """Test a complete render pipeline simulation."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock scene
            scene = MockScene()
            mock_bpy.context.scene = scene

            # Mock scene objects
            mock_obj1 = Mock()
            mock_obj1.name = "TestObject1"
            mock_obj1.data = Mock()
            mock_obj1.data.materials = [Mock()]

            mock_obj2 = Mock()
            mock_obj2.name = "TestObject2"
            mock_obj2.data = Mock()
            mock_obj2.data.materials = [Mock()]

            mock_bpy.data.objects = [mock_obj1, mock_obj2]

            # Simulate full pipeline with different arguments
            test_cases = [
                ['--quality', 'draft', '--materials', 'default'],
                ['--quality', 'preview', '--materials', 'photorealistic'],
                ['--quality', 'production', '--materials', 'clay'],
                ['--quality', 'final', '--engine', 'EEVEE']
            ]

            for args in test_cases:
                parsed_args = render_service.parse_args(args)

                # Apply settings (should not crash)
                render_service.apply_quality_preset(parsed_args.quality)
                render_service.apply_material_style(parsed_args.materials)

                # Should complete without errors
                self.assertTrue(True)

    def test_error_handling_invalid_arguments(self):
        """Test error handling for invalid arguments."""
        # Test invalid quality preset
        with self.assertRaises(SystemExit):
            render_service.parse_args(['--quality', 'invalid_quality'])

        # Test invalid engine
        with self.assertRaises(SystemExit):
            render_service.parse_args(['--engine', 'INVALID_ENGINE'])

        # Test invalid material style
        with self.assertRaises(SystemExit):
            render_service.parse_args(['--materials', 'invalid_style'])


class TestRenderServiceEdgeCases(unittest.TestCase):
    """Test edge cases for render service."""

    def test_zero_frame_range_handling(self):
        """Test handling of zero-length frame range."""
        # Should handle gracefully without crashing
        estimate = render_service.calculate_render_time_estimate(
            frame_count=0,
            quality_preset='production'
        )

        # Should return some value (may be 0 or a minimum)
        self.assertIsInstance(estimate, (int, float))

    def test_negative_frame_numbers(self):
        """Test handling of negative frame numbers."""
        # Should be handled gracefully
        self.assertFalse(render_service.validate_frame_range(-10, 100))
        self.assertFalse(render_service.validate_frame_range(1, -10))

    def test_very_large_frame_counts(self):
        """Test with very large frame counts."""
        # Should handle large numbers without overflow
        estimate = render_service.calculate_render_time_estimate(
            frame_count=100000,
            quality_preset='final'
        )

        # Should return a reasonable estimate
        self.assertIsInstance(estimate, (int, float))
        self.assertGreater(estimate, 0)

    def test_material_style_with_no_objects(self):
        """Test material style application with no objects in scene."""
        with patch('render_service.bpy') as mock_bpy:
            # Mock empty scene
            mock_bpy.data.objects = []

            # Apply material style
            render_service.apply_material_style('photorealistic')

            # Should not crash even with no objects
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


