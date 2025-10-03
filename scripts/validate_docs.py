#!/usr/bin/env python3
"""
Documentation Structure Validator

Validates that documentation follows the project's taxonomy rules.
Can be used as a pre-commit hook or standalone validation script.

Rules:
1. No markdown files in root except: README.md, QUICKSTART.md,
   LICENSE.md, CONTRIBUTING.md
2. No documentation/ folder (use docs/ instead)
3. Project docs must be in docs/project/
4. Guides must be in docs/guides/
5. Setup docs must be in docs/setup/
6. Project-specific docs must be in projects/{name}/
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Allowed root-level markdown files
ALLOWED_ROOT_MD = {
    "README.md",
    "QUICKSTART.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
    ".md",  # Hidden markdown files
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


def validate_documentation(repo_root: Path) -> Tuple[List[ValidationError], List[str]]:
    """Validate documentation structure."""
    errors = []
    info = []

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
            "Create docs/ directory with project/, guides/, and setup/ subdirectories"
        ))
    else:
        # Check for expected subdirectories
        for expected_dir in EXPECTED_STRUCTURE["docs/"]:
            expected_path = docs_dir / expected_dir
            if not expected_path.exists():
                errors.append(ValidationError(
                    f"docs/{expected_dir}",
                    f"Expected subdirectory does not exist",
                    f"Create docs/{expected_dir}"
                ))

    # Check 4: Look for orphaned .md files in inappropriate locations
    for md_file in repo_root.rglob("*.md"):
        rel_path = md_file.relative_to(repo_root)
        path_parts = rel_path.parts

        # Skip allowed locations
        if path_parts[0] in ["docs", "projects", "tests", "blender-mcp", "scripts"]:
            continue
        if md_file.name in ALLOWED_ROOT_MD and len(path_parts) == 1:
            continue

        # Allow README.md in subdirectories (documentation for that component)
        if md_file.name == "README.md":
            continue

        # Check if it's in an unexpected location
        if len(path_parts) > 1:
            errors.append(ValidationError(
                str(rel_path),
                "Markdown file in unexpected location",
                "Move to appropriate docs/ subdirectory or projects/{name}/"
            ))

    # Info: Count documentation files
    if docs_dir.exists():
        doc_count = len(list(docs_dir.rglob("*.md")))
        info.append(f"✅ Found {doc_count} documentation files in docs/")

    return errors, info


def print_results(errors: List[ValidationError], info: List[str]):
    """Print validation results."""
    print("\n" + "=" * 70)
    print("📋 Documentation Structure Validation")
    print("=" * 70 + "\n")

    if info:
        for msg in info:
            print(msg)
        print()

    if errors:
        print(f"Found {len(errors)} issue(s):\n")
        for error in errors:
            print(error)
            print()
        print("=" * 70)
        print("❌ Validation FAILED")
        print("=" * 70)
        return False
    else:
        print("=" * 70)
        print("✅ Validation PASSED - Documentation structure is correct!")
        print("=" * 70)
        return True


def main():
    """Main validation function."""
    # Find repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    # Run validation
    errors, info = validate_documentation(repo_root)

    # Print results
    success = print_results(errors, info)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
