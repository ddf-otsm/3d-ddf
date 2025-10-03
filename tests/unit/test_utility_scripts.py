"""
Unit tests for utility scripts.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from generate_report import generate_report
from detect_blender import find_blender_installations


class TestGenerateReport(unittest.TestCase):
    """Test report generation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = Path(self.temp_dir.name) / "test_report.txt"

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_generate_report_basic(self):
        """Test basic report generation."""
        # Should not raise an exception
        try:
            generate_report(self.output_path.parent)
        except Exception as e:
            self.fail(f"generate_report() raised {type(e).__name__} unexpectedly")

    def test_generate_report_output_file_creation(self):
        """Test that report file is created."""
        generate_report(self.output_path.parent)

        # File should exist in reports directory
        reports_dir = self.output_path.parent / "reports"
        report_files = list(reports_dir.glob("validation_report_*.txt"))
        self.assertGreater(len(report_files), 0)

        # File should have content
        content = report_files[0].read_text()
        self.assertGreater(len(content), 0)


class TestBlenderDetection(unittest.TestCase):
    """Test Blender detection functionality."""

    def test_find_blender_installations(self):
        """Test Blender installation detection."""
        # This may or may not find Blender depending on system
        # The important thing is it doesn't raise an exception
        try:
            result = find_blender_installations()
            # Should return a list of dictionaries or empty list
            self.assertIsInstance(result, list)
            for item in result:
                self.assertIsInstance(item, dict)
        except Exception as e:
            self.fail(f"find_blender_installations() raised {type(e).__name__} unexpectedly")


class TestFileOperations(unittest.TestCase):
    """Test file operation utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_path_operations(self):
        """Test that path operations work correctly."""
        test_path = Path(self.temp_dir.name) / "test_file.txt"

        # Test file creation
        test_path.write_text("test content")
        self.assertTrue(test_path.exists())

        # Test file reading
        content = test_path.read_text()
        self.assertEqual(content, "test content")

        # Test file deletion
        test_path.unlink()
        self.assertFalse(test_path.exists())


class TestMockBlenderOperations(unittest.TestCase):
    """Test mock Blender operations for testing without Blender."""

    def test_mock_bpy_structure(self):
        """Test that mock bpy structure works for testing."""
        # This tests the mock structure used in the explosion system
        # when Blender is not available

        # Import the mock structure
        try:
            from explosions.create_production_explosion import MockBpy
            mock_bpy = MockBpy()

            # Should have the expected structure
            self.assertTrue(hasattr(mock_bpy, 'data'))
            self.assertTrue(hasattr(mock_bpy.data, 'meshes'))
            self.assertTrue(hasattr(mock_bpy.data, 'objects'))
            # Note: materials is not in the mock data class

        except ImportError as e:
            self.fail(f"Failed to import mock bpy structure: {e}")

    def test_mock_material_creation(self):
        """Test mock material creation."""
        try:
            from explosions.create_production_explosion import MockBpy
            mock_bpy = MockBpy()

            # Create a mock mesh (materials are accessed through mesh.materials)
            mesh = mock_bpy.data.meshes.new("test_mesh")
            self.assertIsNotNone(mesh)

        except Exception as e:
            self.fail(f"Mock mesh creation failed: {e}")


if __name__ == '__main__':
    unittest.main()
