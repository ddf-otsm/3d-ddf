"""
Unit tests for validation scripts.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from validate_taxonomy import ValidationError, validate_documentation, validate_export_naming
from validate_docs import validate_documentation as validate_docs_docs
from validate_links import LinkError, validate_links


class TestValidationError(unittest.TestCase):
    """Test ValidationError class."""

    def test_validation_error_creation(self):
        """Test creating ValidationError objects."""
        error = ValidationError("test_path", "test_message", "test_fix")

        self.assertEqual(error.path, "test_path")
        self.assertEqual(error.message, "test_message")
        self.assertEqual(error.fix, "test_fix")

    def test_validation_error_string_representation(self):
        """Test string representation of ValidationError."""
        error = ValidationError("test_path", "test_message", "test_fix")
        error_str = str(error)

        self.assertIn("test_path", error_str)
        self.assertIn("test_message", error_str)
        self.assertIn("test_fix", error_str)

    def test_validation_error_without_fix(self):
        """Test ValidationError without fix message."""
        error = ValidationError("test_path", "test_message")
        error_str = str(error)

        self.assertIn("test_path", error_str)
        self.assertIn("test_message", error_str)
        self.assertNotIn("💡 Fix:", error_str)


class TestTaxonomyValidation(unittest.TestCase):
    """Test taxonomy validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_documentation_empty_directory(self):
        """Test validation on empty directory."""
        errors = validate_documentation(self.repo_root)

        # Should find missing docs directory
        self.assertTrue(any("docs/" in str(error) for error in errors))

    def test_validate_documentation_with_proper_structure(self):
        """Test validation with proper documentation structure."""
        # Create proper docs structure
        docs_dir = self.repo_root / "docs"
        docs_dir.mkdir()
        (docs_dir / "project").mkdir()
        (docs_dir / "guides").mkdir()
        (docs_dir / "setup").mkdir()

        # Create a valid README.md in root
        (self.repo_root / "README.md").write_text("# Test Project")

        errors = validate_documentation(self.repo_root)

        # Should not have structure errors
        structure_errors = [e for e in errors if "does not exist" in str(e)]
        self.assertEqual(len(structure_errors), 0)

    def test_validate_export_naming_no_exports(self):
        """Test export naming validation with no export files."""
        errors = validate_export_naming(self.repo_root)

        # Should not have errors if no files to validate
        self.assertEqual(len(errors), 0)

    def test_validate_export_naming_with_project_structure(self):
        """Test export naming validation with project structure."""
        # Create project directory with export file
        project_dir = self.repo_root / "projects" / "test_project"
        project_dir.mkdir(parents=True)

        # Create an export file that follows naming convention
        export_file = project_dir / "test_project_alpha_20250101_1080p_final.mp4"
        export_file.parent.mkdir(parents=True, exist_ok=True)
        export_file.touch()

        errors = validate_export_naming(self.repo_root)

        # Should not have naming errors for properly named file
        naming_errors = [e for e in errors if "naming convention" in str(e)]
        self.assertEqual(len(naming_errors), 0)


class TestLinkValidation(unittest.TestCase):
    """Test link validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_link_error_creation(self):
        """Test creating LinkError objects."""
        error = LinkError("test_path", 10, "test_url", "test_message")

        self.assertEqual(error.file, "test_path")
        self.assertEqual(error.line, 10)
        self.assertEqual(error.link, "test_url")
        self.assertEqual(error.issue, "test_message")

    def test_validate_links_no_markdown_files(self):
        """Test link validation with no markdown files."""
        errors = validate_links(self.repo_root)

        # Should not have errors if no files to check
        self.assertEqual(len(errors), 0)

    def test_validate_links_with_markdown_structure(self):
        """Test link validation with markdown files."""
        # Create docs structure
        docs_dir = self.repo_root / "docs"
        docs_dir.mkdir()

        # Create a markdown file
        md_file = docs_dir / "test.md"
        md_file.write_text("# Test Document\n\n[Valid Link](test.md)")

        errors = validate_links(self.repo_root)

        # Should not have link errors for valid relative links
        self.assertEqual(len(errors), 0)


class TestDocsValidation(unittest.TestCase):
    """Test documentation validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_validate_docs_empty_directory(self):
        """Test docs validation on empty directory."""
        errors, info = validate_docs_docs(self.repo_root)

        # Should find missing docs directory
        self.assertTrue(any("docs/" in str(error) for error in errors))

    def test_validate_docs_with_valid_structure(self):
        """Test docs validation with valid structure."""
        # Create proper docs structure
        docs_dir = self.repo_root / "docs"
        docs_dir.mkdir()
        (docs_dir / "project").mkdir()
        (docs_dir / "guides").mkdir()
        (docs_dir / "setup").mkdir()

        # Create valid root markdown files
        valid_files = ["README.md", "QUICKSTART.md", "LICENSE.md", "CONTRIBUTING.md"]
        for filename in valid_files:
            (self.repo_root / filename).write_text(f"# {filename}")

        errors, info = validate_docs_docs(self.repo_root)

        # Should not have structure errors
        structure_errors = [e for e in errors if "does not exist" in str(e)]
        self.assertEqual(len(structure_errors), 0)


if __name__ == '__main__':
    unittest.main()
