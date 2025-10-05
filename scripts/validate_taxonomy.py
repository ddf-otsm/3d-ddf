#!/usr/bin/env python3
"""
Complete Taxonomy Validator

Validates project taxonomy including:
1. Documentation structure (docs/)
2. Export file naming conventions
3. Project structure consistency

Can be used as a pre-commit hook or standalone validation script.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# ============================================================================
# DOCUMENTATION RULES
# ============================================================================

# Allowed root-level markdown files
ALLOWED_ROOT_MD = {
    "README.md",
    "QUICKSTART.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",  # Standard for project changelogs
    "AGENTS.md",  # AI navigation guide
}

# Disallowed directory names
DISALLOWED_DIRS = {
    "documentation",  # Use docs/ instead
    "doc",            # Use docs/ instead
}

# Expected documentation structure
EXPECTED_STRUCTURE = {
    "docs/": ["project/", "guides/", "setup/"],
}

# ============================================================================
# EXPORT NAMING RULES
# ============================================================================

# Export naming pattern: {project}_{version}_{date}_{quality}_{type}.mp4
EXPORT_PATTERN = re.compile(
    r'^(?P<project>[a-z]+)_'
    r'(?P<version>[a-z]+)_'
    r'(?P<date>\d{8})_'
    r'(?P<quality>\d+p)_'
    r'(?P<type>[a-z0-9_]+)'
    r'\.mp4$'
)

# Valid component values
VALID_VERSIONS = {"alpha", "beta", "stable", "deprecated", "rc"}
VALID_QUALITIES = {"270p", "360p", "480p", "720p", "1080p", "1440p", "4k"}

# Exceptions (files that don't follow the pattern but are allowed)
EXPORT_EXCEPTIONS = {
    "README.md",
    ".rename_mapping.txt",

    # Legacy export files - kept for historical reference
    "20250930_0000_dadosfera_deprecated_1080p_viewport_nomat.mp4",
    "20250930_0000_dadosfera_deprecated_1080p_viewport1.mp4",
    "20250930_0000_dadosfera_deprecated_1080p_viewport2.mp4",
    "20251004_1549_dadosfera_preview_1080p.mp4",
    "20251001_0000_dadosfera_stable_1080p_final.mp4",
    "20251001_0000_dadosfera_alpha_1080p_preview.mp4",
    "20251002_0000_dadosfera_stable_1080p_final.mp4",
    "20250930_0000_dadosfera_deprecated_270p_test.mp4",
    "20251002_0000_dadosfera_stable_1080p_cycles.mp4",
    "20250930_0000_dadosfera_deprecated_360p_test.mp4",
    "20251004_1644_fixed_no_ground_plane_test_1080p.mp4",
    "20251002_0000_dadosfera_alpha_1080p_preview.mp4",
    "20250930_0000_dadosfera_alpha_1080p_partial_8sec.mp4",
    "20250930_0000_dadosfera_deprecated_360p_viewport.mp4",
    "20251002_0000_dadosfera_beta_1080p_cycles.mp4",
    "20250930_0000_dadosfera_deprecated_720p_preview.mp4",
    "20251004_1549_explosion-test_preview_1080p.mp4",
    "20251002_1152_explosion-test_alpha_20251002_1080p_final.mp4",

    # Additional legacy files that don't follow the pattern
    "dadosfera_20251002_2125.mp4",  # Legacy export before taxonomy enforcement
    "dadosfera_CYCLES_preview_20251002_2042.mp4",  # Internal preview render
    "explosion-test_alpha_20251002_1080p_final.mp4",  # Test file with project name containing dash
}


class ValidationError:
    def __init__(self, path: str, message: str, fix: str = ""):
        self.path = path
        self.message = message
        self.fix = fix

    def __str__(self):
        result = f"❌ {self.path}\n   {self.message}"
        if self.fix:
            result += f"\n   💡 Fix: {self.fix}"
        return result


def validate_documentation(repo_root: Path) -> List[ValidationError]:
    """Validate documentation structure."""
    errors = []

    # Check 1: No unauthorized markdown files in root
    for md_file in repo_root.glob("*.md"):
        if md_file.name not in ALLOWED_ROOT_MD:
            errors.append(ValidationError(
                str(md_file.relative_to(repo_root)),
                "Documentation file in root directory",
                f"Move to docs/project/{md_file.name.lower().replace('_', '-')}"
            ))

    # Check 2: No disallowed directories
    for disallowed in DISALLOWED_DIRS:
        disallowed_path = repo_root / disallowed
        if disallowed_path.exists():
            errors.append(ValidationError(
                str(disallowed_path.relative_to(repo_root)),
                f"Disallowed directory '{disallowed}/' exists",
                f"Move contents to docs/ and remove {disallowed}/"
            ))

    # Check 3: Verify docs/ structure exists
    docs_dir = repo_root / "docs"
    if not docs_dir.exists():
        errors.append(ValidationError(
            "docs/",
            "Documentation directory does not exist",
            "Create docs/ with project/, guides/, and setup/ subdirectories"
        ))
    else:
        # Check for expected subdirectories
        for expected_dir in EXPECTED_STRUCTURE["docs/"]:
            expected_path = docs_dir / expected_dir
            if not expected_path.exists():
                errors.append(ValidationError(
                    f"docs/{expected_dir}",
                    "Expected subdirectory does not exist",
                    f"Create docs/{expected_dir}"
                ))

    # Check 4: Look for orphaned .md files in inappropriate locations
    for md_file in repo_root.rglob("*.md"):
        rel_path = md_file.relative_to(repo_root)
        path_parts = rel_path.parts

        # Skip venv directories and other excluded paths
        if any(part in ["venv", ".venv", "env", ".env", "node_modules", "__pycache__"]
               for part in path_parts):
            continue

        # Skip AGENTS.md files anywhere
        if md_file.name == "AGENTS.md":
            continue

        # Skip allowed locations
        if path_parts[0] in ["docs", "projects", "tests", "blender-mcp",
                             "scripts"]:
            continue
        if md_file.name in ALLOWED_ROOT_MD and len(path_parts) == 1:
            continue

        # Allow README.md in subdirectories
        if md_file.name == "README.md":
            continue

        # Check if it's in an unexpected location
        if len(path_parts) > 1:
            errors.append(ValidationError(
                str(rel_path),
                "Markdown file in unexpected location",
                "Move to appropriate docs/ subdirectory or projects/{name}/"
            ))

    return errors


def validate_export_naming(repo_root: Path) -> List[ValidationError]:
    """Validate export file naming conventions."""
    errors = []

    # Find all export directories
    exports_dirs = list(repo_root.glob("projects/*/exports"))

    for exports_dir in exports_dirs:
        project_name = exports_dir.parent.name

        for export_file in exports_dir.iterdir():
            # Skip directories and exceptions
            if export_file.is_dir():
                continue
            if export_file.name in EXPORT_EXCEPTIONS:
                continue

            # Only check .mp4 files
            if not export_file.name.endswith('.mp4'):
                continue

            # Check if filename matches pattern
            match = EXPORT_PATTERN.match(export_file.name)

            if not match:
                rel_path = export_file.relative_to(repo_root)
                errors.append(ValidationError(
                    str(rel_path),
                    "Export file does not follow naming convention",
                    f"Rename to: {project_name}_<version>_<YYYYMMDD>_<quality>_<type>.mp4"
                    f"\n   Example: {project_name}_alpha_20251002_1080p_final.mp4"
                ))
                continue

            # Validate components
            groups = match.groupdict()

            # Check project name matches directory
            if groups['project'] != project_name:
                rel_path = export_file.relative_to(repo_root)
                errors.append(ValidationError(
                    str(rel_path),
                    f"Project name '{groups['project']}' doesn't match "
                    f"directory '{project_name}'",
                    f"Rename to start with '{project_name}_'"
                ))

            # Check version is valid
            if groups['version'] not in VALID_VERSIONS:
                rel_path = export_file.relative_to(repo_root)
                errors.append(ValidationError(
                    str(rel_path),
                    f"Invalid version '{groups['version']}'",
                    f"Use one of: {', '.join(sorted(VALID_VERSIONS))}"
                ))

            # Check quality is valid
            if groups['quality'] not in VALID_QUALITIES:
                rel_path = export_file.relative_to(repo_root)
                errors.append(ValidationError(
                    str(rel_path),
                    f"Invalid quality '{groups['quality']}'",
                    f"Use one of: {', '.join(sorted(VALID_QUALITIES))}"
                ))

            # Validate date format (basic check)
            try:
                date_str = groups['date']
                year = int(date_str[0:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
                if not (2020 <= year <= 2030
                        and 1 <= month <= 12
                        and 1 <= day <= 31):
                    raise ValueError("Invalid date")
            except (ValueError, IndexError):
                rel_path = export_file.relative_to(repo_root)
                errors.append(ValidationError(
                    str(rel_path),
                    f"Invalid date '{groups['date']}'",
                    "Date must be in YYYYMMDD format"
                ))

    return errors


def print_results(doc_errors: List[ValidationError],
                  export_errors: List[ValidationError],
                  doc_count: int) -> bool:
    """Print validation results."""
    print("\n" + "=" * 70)
    print("📋 Project Taxonomy Validation")
    print("=" * 70 + "\n")

    all_errors = doc_errors + export_errors

    if doc_count > 0:
        print(f"✅ Found {doc_count} documentation files in docs/")

    if not all_errors:
        print("\n" + "=" * 70)
        print("✅ Validation PASSED - All taxonomy rules followed!")
        print("=" * 70)
        return True

    print(f"\nFound {len(all_errors)} issue(s):\n")

    if doc_errors:
        print("📄 Documentation Issues:")
        print("-" * 70)
        for error in doc_errors:
            print(error)
            print()

    if export_errors:
        print("🎬 Export Naming Issues:")
        print("-" * 70)
        for error in export_errors:
            print(error)
            print()

    print("=" * 70)
    print("❌ Validation FAILED")
    print("=" * 70)
    return False


def main():
    """Main validation function."""
    # Find repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    # Run validations
    doc_errors = validate_documentation(repo_root)
    export_errors = validate_export_naming(repo_root)

    # Count documentation files
    docs_dir = repo_root / "docs"
    doc_count = len(list(docs_dir.rglob("*.md"))) if docs_dir.exists() else 0

    # Print results
    success = print_results(doc_errors, export_errors, doc_count)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
