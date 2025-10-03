"""
Unit tests for validate_json.py
Tests JSON validation functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
import json
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# Mock jsonschema module
class MockValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class MockJsonschema:
    ValidationError = MockValidationError
    def validate(instance, schema):
        pass

sys.modules['jsonschema'] = MockJsonschema()
sys.modules['jsonschema.exceptions'] = MockJsonschema()

from validate_json import JSONError, find_json_files, validate_json_syntax, validate_json_schema, validate_metadata_consistency, validate_all_json, print_results


class TestJSONError(unittest.TestCase):
    """Test JSONError class functionality."""

    def test_json_error_creation(self):
        """Test creating JSONError objects."""
        error = JSONError("test/file.json", "Invalid JSON syntax")

        self.assertEqual(error.file, "test/file.json")
        self.assertEqual(error.issue, "Invalid JSON syntax")

    def test_json_error_string_representation(self):
        """Test string representation of JSONError."""
        error = JSONError("test/file.json", "Invalid JSON syntax")
        error_str = str(error)

        self.assertIn("test/file.json", error_str)
        self.assertIn("Invalid JSON syntax", error_str)


class TestFindJsonFiles(unittest.TestCase):
    """Test find_json_files function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_find_json_files_empty_directory(self):
        """Test finding JSON files in empty directory."""
        json_files = find_json_files(self.repo_root)

        # Should return empty list
        self.assertEqual(len(json_files), 0)

    def test_find_json_files_with_json_files(self):
        """Test finding JSON files when they exist."""
        # Create some JSON files
        json_file1 = self.repo_root / "config.json"
        json_file1.write_text('{"test": "data"}')

        json_file2 = self.repo_root / "data.json"
        json_file2.write_text('{"more": "data"}')

        # Create non-JSON file
        txt_file = self.repo_root / "readme.txt"
        txt_file.write_text("Not JSON")

        json_files = find_json_files(self.repo_root)

        # Should find only JSON files
        self.assertEqual(len(json_files), 2)
        json_filenames = [f.name for f in json_files]
        self.assertIn("config.json", json_filenames)
        self.assertIn("data.json", json_filenames)

    def test_find_json_files_excludes_git_directory(self):
        """Test that .git directory is excluded."""
        # Create .git directory with JSON file
        git_dir = self.repo_root / ".git"
        git_dir.mkdir()

        git_json = git_dir / "config.json"
        git_json.write_text('{"git": "config"}')

        # Create regular JSON file
        regular_json = self.repo_root / "regular.json"
        regular_json.write_text('{"regular": "config"}')

        json_files = find_json_files(self.repo_root)

        # Should only find the regular JSON file
        self.assertEqual(len(json_files), 1)
        self.assertEqual(json_files[0].name, "regular.json")

    def test_find_json_files_excludes_pycache_directory(self):
        """Test that __pycache__ directory is excluded."""
        # Create __pycache__ directory with JSON file
        pycache_dir = self.repo_root / "__pycache__"
        pycache_dir.mkdir()

        pycache_json = pycache_dir / "module.json"
        pycache_json.write_text('{"cache": "data"}')

        # Create regular JSON file
        regular_json = self.repo_root / "regular.json"
        regular_json.write_text('{"regular": "data"}')

        json_files = find_json_files(self.repo_root)

        # Should only find the regular JSON file
        self.assertEqual(len(json_files), 1)
        self.assertEqual(json_files[0].name, "regular.json")


class TestValidateJsonSyntax(unittest.TestCase):
    """Test validate_json_syntax function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_json_syntax_valid_json(self):
        """Test validation of valid JSON."""
        test_file = Path(self.temp_dir.name) / "valid.json"
        test_file.write_text('{"valid": "json", "number": 42}')

        error = validate_json_syntax(test_file)

        # Should return None for valid JSON
        self.assertIsNone(error)

    def test_validate_json_syntax_invalid_json(self):
        """Test validation of invalid JSON."""
        test_file = Path(self.temp_dir.name) / "invalid.json"
        test_file.write_text('{"invalid": "json"')  # Missing closing brace

        error = validate_json_syntax(test_file)

        # Should return error message
        self.assertIsNotNone(error)
        self.assertIn("Invalid JSON syntax", error)

    def test_validate_json_syntax_empty_file(self):
        """Test validation of empty file."""
        test_file = Path(self.temp_dir.name) / "empty.json"
        test_file.touch()

        error = validate_json_syntax(test_file)

        # Should handle empty file gracefully
        self.assertIsNotNone(error)

    def test_validate_json_syntax_nonexistent_file(self):
        """Test validation of nonexistent file."""
        test_file = Path(self.temp_dir.name) / "nonexistent.json"

        error = validate_json_syntax(test_file)

        # Should return error for nonexistent file
        self.assertIsNotNone(error)
        self.assertIn("Error reading file", error)


class TestValidateJsonSchema(unittest.TestCase):
    """Test validate_json_schema function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_json_schema_no_schema(self):
        """Test validation when no schema file exists."""
        test_file = Path(self.temp_dir.name) / "data.json"
        test_file.write_text('{"test": "data"}')

        error = validate_json_schema(test_file, Path(self.temp_dir.name))

        # Should return None when no schema exists
        self.assertIsNone(error)

    def test_validate_json_schema_valid_schema(self):
        """Test validation with valid schema."""
        # Create schema file
        schema_file = Path(self.temp_dir.name) / "data.schema.json"
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }
        schema_file.write_text(json.dumps(schema))

        # Create data file
        data_file = Path(self.temp_dir.name) / "data.json"
        data = {"name": "John", "age": 30}
        data_file.write_text(json.dumps(data))

        error = validate_json_schema(data_file, Path(self.temp_dir.name))

        # Should pass validation
        self.assertIsNone(error)

    def test_validate_json_schema_invalid_schema(self):
        """Test validation with invalid schema."""
        # Create schema file
        schema_file = Path(self.temp_dir.name) / "data.schema.json"
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name", "age"]  # Requires age but data doesn't have it
        }
        schema_file.write_text(json.dumps(schema))

        # Create data file without required field
        data_file = Path(self.temp_dir.name) / "data.json"
        data = {"name": "John"}  # Missing required "age" field
        data_file.write_text(json.dumps(data))

        error = validate_json_schema(data_file, Path(self.temp_dir.name))

        # Should fail validation
        self.assertIsNotNone(error)
        self.assertIn("Schema validation failed", error)


class TestValidateMetadataConsistency(unittest.TestCase):
    """Test validate_metadata_consistency function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_metadata_consistency_non_metadata_file(self):
        """Test validation of non-metadata JSON file."""
        test_file = Path(self.temp_dir.name) / "config.json"
        test_file.write_text('{"config": "data"}')

        error = validate_metadata_consistency(test_file)

        # Should return None for non-metadata files
        self.assertIsNone(error)

    def test_validate_metadata_consistency_valid_metadata(self):
        """Test validation of valid metadata."""
        # Create exports directory and files
        exports_dir = Path(self.temp_dir.name) / "exports"
        exports_dir.mkdir()

        # Create metadata file
        metadata_file = exports_dir / "metadata.json"
        metadata = {
            "exports": [
                {
                    "filename": "project_alpha_20250101_1080p_final.mp4",
                    "version": "alpha",
                    "quality": "1080p"
                }
            ]
        }
        metadata_file.write_text(json.dumps(metadata))

        # Create the referenced file
        video_file = exports_dir / "project_alpha_20250101_1080p_final.mp4"
        video_file.write_text("video content")

        error = validate_metadata_consistency(metadata_file)

        # Should pass validation
        self.assertIsNone(error)

    def test_validate_metadata_consistency_missing_exports(self):
        """Test validation when exports field is missing."""
        test_file = Path(self.temp_dir.name) / "metadata.json"
        metadata = {"name": "Test Project"}  # Missing exports field
        test_file.write_text(json.dumps(metadata))

        error = validate_metadata_consistency(test_file)

        # Should detect missing exports field
        self.assertIsNotNone(error)
        self.assertIn("Missing 'exports' field", error)

    def test_validate_metadata_consistency_missing_file(self):
        """Test validation when referenced file doesn't exist."""
        # Create metadata file
        metadata_file = Path(self.temp_dir.name) / "metadata.json"
        metadata = {
            "exports": [
                {
                    "filename": "missing_file.mp4",
                    "version": "alpha",
                    "quality": "1080p"
                }
            ]
        }
        metadata_file.write_text(json.dumps(metadata))

        error = validate_metadata_consistency(metadata_file)

        # Should detect missing file
        self.assertIsNotNone(error)
        self.assertIn("Referenced file does not exist", error)


class TestValidateAllJson(unittest.TestCase):
    """Test validate_all_json function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_all_json_empty_directory(self):
        """Test validation of empty directory."""
        errors = validate_all_json(self.repo_root)

        # Should have no errors
        self.assertEqual(len(errors), 0)

    def test_validate_all_json_mixed_files(self):
        """Test validation with mix of valid and invalid JSON files."""
        # Create valid JSON file
        valid_file = self.repo_root / "valid.json"
        valid_file.write_text('{"valid": "json"}')

        # Create invalid JSON file
        invalid_file = self.repo_root / "invalid.json"
        invalid_file.write_text('{"invalid": "json"')  # Missing closing brace

        errors = validate_all_json(self.repo_root)

        # Should detect the invalid JSON file
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid JSON syntax", errors[0].issue)


class TestPrintResults(unittest.TestCase):
    """Test print_results function."""

    def test_print_results_no_errors(self):
        """Test print_results with no errors."""
        errors = []

        # Should return True (success)
        result = print_results(errors)
        self.assertTrue(result)

    def test_print_results_with_errors(self):
        """Test print_results with errors."""
        errors = [
            JSONError("file1.json", "Invalid JSON"),
            JSONError("file2.json", "Missing field")
        ]

        # Should return False (failure)
        result = print_results(errors)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
