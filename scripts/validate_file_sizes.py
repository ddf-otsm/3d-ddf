#!/usr/bin/env python3
"""
File Size Validator

Checks for large files, empty files, and tracks size trends.
"""

import sys
from pathlib import Path
from typing import List, Tuple


class SizeIssue:
    def __init__(self, file: str, size_mb: float, issue_type: str, message: str):
        self.file = file
        self.size_mb = size_mb
        self.issue_type = issue_type
        self.message = message

    def __str__(self):
        emoji = "⚠️" if self.issue_type == "warning" else "❌"
        return f"{emoji} {self.file} ({self.size_mb:.2f} MB)\n   {self.message}"


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB."""
    return file_path.stat().st_size / (1024 * 1024)


def check_file_sizes(repo_root: Path) -> Tuple[List[SizeIssue], dict]:
    """Check all files for size issues."""
    issues = []
    stats = {
        "total_files": 0,
        "total_size_mb": 0.0,
        "large_files": 0,
        "empty_files": 0,
    }

    # Patterns to check
    patterns = ["**/*.mp4", "**/*.blend", "**/*.png", "**/*.jpg", "**/*.pdf"]

    # Exclude directories
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}

    print("📊 Checking file sizes...\n")

    for pattern in patterns:
        for file_path in repo_root.glob(pattern):
            # Skip excluded directories
            if any(ex in file_path.parts for ex in exclude_dirs):
                continue

            rel_path = file_path.relative_to(repo_root)
            size_mb = get_file_size_mb(file_path)

            stats["total_files"] += 1
            stats["total_size_mb"] += size_mb

            # Check for empty files
            if size_mb == 0:
                stats["empty_files"] += 1
                issues.append(SizeIssue(
                    str(rel_path),
                    size_mb,
                    "error",
                    "File is empty"
                ))

            # Check for large files (>50MB warning, >100MB error)
            elif size_mb > 100:
                stats["large_files"] += 1
                issues.append(SizeIssue(
                    str(rel_path),
                    size_mb,
                    "error",
                    "File is very large (>100MB). Consider compression or Git LFS."
                ))
            elif size_mb > 50:
                stats["large_files"] += 1
                issues.append(SizeIssue(
                    str(rel_path),
                    size_mb,
                    "warning",
                    "File is large (>50MB). Consider compression or Git LFS."
                ))

    return issues, stats


def print_results(issues: List[SizeIssue], stats: dict) -> bool:
    """Print validation results."""
    print("\n" + "=" * 70)
    print("📊 File Size Validation Results")
    print("=" * 70 + "\n")

    # Print statistics
    print(f"📈 Statistics:")
    print(f"   Total files checked: {stats['total_files']}")
    print(f"   Total size: {stats['total_size_mb']:.2f} MB")
    print(f"   Large files (>50MB): {stats['large_files']}")
    print(f"   Empty files: {stats['empty_files']}")
    print()

    if not issues:
        print("✅ All file sizes are reasonable!")
        print("=" * 70)
        return True

    # Separate errors and warnings
    errors = [i for i in issues if i.issue_type == "error"]
    warnings = [i for i in issues if i.issue_type == "warning"]

    if errors:
        print(f"Found {len(errors)} error(s):\n")
        for error in errors:
            print(error)
            print()

    if warnings:
        print(f"Found {len(warnings)} warning(s):\n")
        for warning in warnings:
            print(warning)
            print()

    print("=" * 70)
    if errors:
        print("❌ Validation FAILED")
    else:
        print("⚠️  Validation PASSED with warnings")
    print("=" * 70)

    return len(errors) == 0


def main():
    """Main validation function."""
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    issues, stats = check_file_sizes(repo_root)
    success = print_results(issues, stats)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
