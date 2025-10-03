"""
Unit tests for validate_file_sizes.py
Tests file size validation functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from validate_file_sizes import SizeIssue, get_file_size_mb, check_file_sizes, print_results


class TestSizeIssue(unittest.TestCase):
    """Test SizeIssue class functionality."""

    def test_size_issue_creation(self):
        """Test creating SizeIssue objects."""
        issue = SizeIssue("test/file.mp4", 150.5, "error", "File too large")

        self.assertEqual(issue.file, "test/file.mp4")
        self.assertEqual(issue.size_mb, 150.5)
        self.assertEqual(issue.issue_type, "error")
        self.assertEqual(issue.message, "File too large")

    def test_size_issue_string_representation(self):
        """Test string representation of SizeIssue."""
        issue = SizeIssue("test/file.mp4", 150.5, "error", "File too large")
        issue_str = str(issue)

        self.assertIn("test/file.mp4", issue_str)
        self.assertIn("150.50 MB", issue_str)
        self.assertIn("File too large", issue_str)

    def test_size_issue_warning_string_representation(self):
        """Test string representation of warning SizeIssue."""
        issue = SizeIssue("test/file.mp4", 75.2, "warning", "File is large")
        issue_str = str(issue)

        self.assertIn("⚠️", issue_str)  # Should have warning emoji
        self.assertIn("test/file.mp4", issue_str)


class TestGetFileSizeMb(unittest.TestCase):
    """Test get_file_size_mb function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_get_file_size_mb_small_file(self):
        """Test getting size of small file."""
        # Create a test file with known size
        test_file = Path(self.temp_dir.name) / "test.txt"
        test_content = "Hello, World!"  # 13 bytes
        test_file.write_text(test_content)

        size_mb = get_file_size_mb(test_file)

        # Should be very small (less than 1MB)
        self.assertLess(size_mb, 1.0)
        self.assertGreater(size_mb, 0.0)

    def test_get_file_size_mb_larger_file(self):
        """Test getting size of larger file."""
        # Create a test file with 1MB content
        test_file = Path(self.temp_dir.name) / "large_file.txt"
        test_content = "x" * (1024 * 1024)  # 1MB of content
        test_file.write_text(test_content)

        size_mb = get_file_size_mb(test_file)

        # Should be approximately 1MB
        self.assertAlmostEqual(size_mb, 1.0, places=2)

    def test_get_file_size_mb_empty_file(self):
        """Test getting size of empty file."""
        # Create an empty file
        test_file = Path(self.temp_dir.name) / "empty.txt"
        test_file.touch()

        size_mb = get_file_size_mb(test_file)

        # Should be 0 MB
        self.assertEqual(size_mb, 0.0)


class TestCheckFileSizes(unittest.TestCase):
    """Test check_file_sizes function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_check_file_sizes_empty_directory(self):
        """Test checking file sizes in empty directory."""
        issues, stats = check_file_sizes(self.repo_root)

        # Should have no issues and proper stats
        self.assertEqual(len(issues), 0)
        self.assertEqual(stats["total_files"], 0)
        self.assertEqual(stats["total_size_mb"], 0.0)
        self.assertEqual(stats["large_files"], 0)
        self.assertEqual(stats["empty_files"], 0)

    def test_check_file_sizes_with_small_files(self):
        """Test checking file sizes with small files."""
        # Create some small files
        small_file = self.repo_root / "small.mp4"
        small_file.write_text("small content")

        small_png = self.repo_root / "small.png"
        small_png.write_text("small image content")

        issues, stats = check_file_sizes(self.repo_root)

        # Should have no issues for small files
        self.assertEqual(len(issues), 0)
        self.assertEqual(stats["total_files"], 2)
        self.assertGreater(stats["total_size_mb"], 0)

    def test_check_file_sizes_with_large_files(self):
        """Test checking file sizes with large files."""
        # Create files of different sizes
        small_file = self.repo_root / "small.mp4"
        small_file.write_text("small content")

        # Create a file larger than 50MB (warning threshold)
        large_file = self.repo_root / "large.mp4"
        large_content = "x" * (60 * 1024 * 1024)  # 60MB
        large_file.write_text(large_content)

        # Create a file larger than 100MB (error threshold)
        huge_file = self.repo_root / "huge.mp4"
        huge_content = "x" * (120 * 1024 * 1024)  # 120MB
        huge_file.write_text(huge_content)

        issues, stats = check_file_sizes(self.repo_root)

        # Should detect large files
        self.assertGreater(len(issues), 0)
        self.assertEqual(stats["total_files"], 3)
        self.assertEqual(stats["large_files"], 2)  # Both large and huge files

        # Should have one error (huge file) and one warning (large file)
        error_issues = [i for i in issues if i.issue_type == "error"]
        warning_issues = [i for i in issues if i.issue_type == "warning"]

        self.assertEqual(len(error_issues), 1)
        self.assertEqual(len(warning_issues), 1)

    def test_check_file_sizes_with_empty_file(self):
        """Test checking file sizes with empty file."""
        # Create an empty file
        empty_file = self.repo_root / "empty.mp4"
        empty_file.touch()

        issues, stats = check_file_sizes(self.repo_root)

        # Should detect empty file
        self.assertEqual(len(issues), 1)
        self.assertEqual(stats["total_files"], 1)
        self.assertEqual(stats["empty_files"], 1)

        # Should be an error
        self.assertEqual(issues[0].issue_type, "error")
        self.assertIn("empty", issues[0].message.lower())

    def test_check_file_sizes_excludes_git_directory(self):
        """Test that .git directory is excluded."""
        # Create .git directory with files
        git_dir = self.repo_root / ".git"
        git_dir.mkdir()

        git_file = git_dir / "config"
        git_file.write_text("git config content")

        # Create regular files
        regular_file = self.repo_root / "regular.mp4"
        regular_file.write_text("regular content")

        issues, stats = check_file_sizes(self.repo_root)

        # Should only count the regular file, not git files
        self.assertEqual(stats["total_files"], 1)
        self.assertEqual(len(issues), 0)

    def test_check_file_sizes_excludes_pycache_directory(self):
        """Test that __pycache__ directory is excluded."""
        # Create __pycache__ directory with files
        pycache_dir = self.repo_root / "__pycache__"
        pycache_dir.mkdir()

        pycache_file = pycache_dir / "module.pyc"
        pycache_file.write_text("compiled python")

        # Create regular files
        regular_file = self.repo_root / "regular.mp4"
        regular_file.write_text("regular content")

        issues, stats = check_file_sizes(self.repo_root)

        # Should only count the regular file, not pycache files
        self.assertEqual(stats["total_files"], 1)
        self.assertEqual(len(issues), 0)


class TestPrintResults(unittest.TestCase):
    """Test print_results function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_print_results_no_issues(self):
        """Test print_results with no issues."""
        issues = []
        stats = {
            "total_files": 10,
            "total_size_mb": 25.5,
            "large_files": 0,
            "empty_files": 0
        }

        # Should return True (success)
        result = print_results(issues, stats)
        self.assertTrue(result)

    def test_print_results_with_warnings_only(self):
        """Test print_results with warnings only."""
        issues = [
            SizeIssue("large_file.mp4", 75.2, "warning", "File is large")
        ]
        stats = {
            "total_files": 10,
            "total_size_mb": 100.5,
            "large_files": 1,
            "empty_files": 0
        }

        # Should return True (warnings don't fail)
        result = print_results(issues, stats)
        self.assertTrue(result)

    def test_print_results_with_errors(self):
        """Test print_results with errors."""
        issues = [
            SizeIssue("empty_file.mp4", 0.0, "error", "File is empty"),
            SizeIssue("huge_file.mp4", 150.5, "error", "File is very large")
        ]
        stats = {
            "total_files": 10,
            "total_size_mb": 200.5,
            "large_files": 1,
            "empty_files": 1
        }

        # Should return False (errors cause failure)
        result = print_results(issues, stats)
        self.assertFalse(result)

    def test_print_results_mixed_issues(self):
        """Test print_results with mixed errors and warnings."""
        issues = [
            SizeIssue("empty_file.mp4", 0.0, "error", "File is empty"),
            SizeIssue("large_file.mp4", 75.2, "warning", "File is large"),
            SizeIssue("huge_file.mp4", 150.5, "error", "File is very large")
        ]
        stats = {
            "total_files": 10,
            "total_size_mb": 250.7,
            "large_files": 2,
            "empty_files": 1
        }

        # Should return False (errors cause failure)
        result = print_results(issues, stats)
        self.assertFalse(result)


class TestFileSizeValidationEdgeCases(unittest.TestCase):
    """Test edge cases for file size validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_file_size_boundary_values(self):
        """Test file size validation at boundary values."""
        # Test files at exact boundary values
        warning_boundary_file = self.repo_root / "warning_boundary.mp4"
        warning_boundary_file.write_text("x" * (50 * 1024 * 1024))  # Exactly 50MB

        error_boundary_file = self.repo_root / "error_boundary.mp4"
        error_boundary_file.write_text("x" * (100 * 1024 * 1024))  # Exactly 100MB

        issues, stats = check_file_sizes(self.repo_root)

        # Should detect both files as issues
        self.assertEqual(stats["total_files"], 2)
        self.assertEqual(stats["large_files"], 2)

    def test_file_size_with_special_characters(self):
        """Test file size validation with files having special characters in names."""
        # Create file with special characters
        special_file = self.repo_root / "special_@#$%^&()_file.mp4"
        special_file.write_text("special content")

        issues, stats = check_file_sizes(self.repo_root)

        # Should handle special characters gracefully
        self.assertEqual(stats["total_files"], 1)
        self.assertEqual(len(issues), 0)

    def test_file_size_with_unicode_names(self):
        """Test file size validation with unicode file names."""
        # Create file with unicode name
        unicode_file = self.repo_root / "测试文件.mp4"
        unicode_file.write_text("unicode content")

        issues, stats = check_file_sizes(self.repo_root)

        # Should handle unicode names gracefully
        self.assertEqual(stats["total_files"], 1)
        self.assertEqual(len(issues), 0)

    def test_multiple_large_files(self):
        """Test handling multiple large files."""
        # Create several large files
        large_files = []
        for i in range(5):
            large_file = self.repo_root / f"large_file_{i}.mp4"
            large_content = "x" * (75 * 1024 * 1024)  # 75MB each
            large_file.write_text(large_content)
            large_files.append(large_file)

        issues, stats = check_file_sizes(self.repo_root)

        # Should detect all large files
        self.assertEqual(stats["total_files"], 5)
        self.assertEqual(stats["large_files"], 5)
        self.assertEqual(len(issues), 5)

        # All should be warnings (75MB > 50MB but < 100MB)
        for issue in issues:
            self.assertEqual(issue.issue_type, "warning")


if __name__ == '__main__':
    unittest.main()


