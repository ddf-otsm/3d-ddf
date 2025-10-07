#!/usr/bin/env python3
"""
JSON Validator

Validates JSON syntax and schema compliance.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional
import jsonschema


class JSONError:
    def __init__(self, file: str, issue: str):
        self.file = file
        self.issue = issue

    def __str__(self):
        return f"❌ {self.file}\n   {self.issue}"


def find_json_files(repo_root: Path) -> List[Path]:
    """Find all JSON files."""
    json_files = []

    for pattern in ["**/*.json"]:
        json_files.extend(repo_root.glob(pattern))

    # Exclude certain directories
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv",
                    "blender-mcp"}

    filtered = []
    for f in json_files:
        if not any(ex in f.parts for ex in exclude_dirs):
            filtered.append(f)

    return sorted(filtered)


def validate_json_syntax(file_path: Path) -> Optional[str]:
    """Validate JSON syntax."""
    try:
        content = file_path.read_text(encoding='utf-8')
        json.loads(content)
        return None
    except json.JSONDecodeError as e:
        return f"Invalid JSON syntax: {e}"
    except Exception as e:
        return f"Error reading file: {e}"


def validate_json_schema(file_path: Path, repo_root: Path) -> Optional[str]:
    """Validate JSON against schema if available."""
    # Check if there's a corresponding schema file
    schema_file = file_path.parent / f"{file_path.stem}.schema.json"

    if not schema_file.exists():
        return None  # No schema, skip validation

    try:
        data = json.loads(file_path.read_text())
        schema = json.loads(schema_file.read_text())

        jsonschema.validate(instance=data, schema=schema)
        return None
    except jsonschema.exceptions.ValidationError as e:
        return f"Schema validation failed: {e.message}"
    except Exception as e:
        return f"Error validating schema: {e}"


def validate_metadata_consistency(file_path: Path) -> Optional[str]:
    """Validate export metadata.json specifically."""
    if file_path.name != "metadata.json":
        return None

    try:
        data = json.loads(file_path.read_text())

        # Check exports list
        if "exports" not in data:
            return "Missing 'exports' field"

        # Check each export
        exports_dir = file_path.parent
        for export in data["exports"]:
            filename = export.get("filename")
            if not filename:
                continue

            # Check if file exists
            file = exports_dir / filename
            if not file.exists():
                return f"Referenced file does not exist: {filename}"

            # Check filename matches metadata
            # New format: YYYYMMDD_HHMM_project_version_quality_descriptor.mp4
            # Old format: project_version_YYYYMMDD_quality_descriptor.mp4
            parts = filename.replace(".mp4", "").split("_")
            if len(parts) >= 5:
                meta_version = export.get("version")
                meta_quality = export.get("quality")
                
                # Detect format by checking if first part is a date (8 digits)
                if parts[0].isdigit() and len(parts[0]) == 8:
                    # New timestamp-first format: YYYYMMDD_HHMM_project_version_quality_...
                    version_idx = 3
                    quality_idx = 4
                else:
                    # Old format: project_version_YYYYMMDD_quality_...
                    version_idx = 1
                    quality_idx = 3

                if meta_version and len(parts) > version_idx and parts[version_idx] != meta_version:
                    return f"Version mismatch in {filename}: filename has '{parts[version_idx]}', metadata has '{meta_version}'"

                if meta_quality and len(parts) > quality_idx and parts[quality_idx] != meta_quality:
                    return f"Quality mismatch in {filename}: filename has '{parts[quality_idx]}', metadata has '{meta_quality}'"

        return None
    except Exception as e:
        return f"Error validating metadata: {e}"


def validate_all_json(repo_root: Path) -> List[JSONError]:
    """Validate all JSON files."""
    errors = []
    json_files = find_json_files(repo_root)

    print(f"📄 Checking {len(json_files)} JSON files...\n")

    for json_file in json_files:
        rel_path = json_file.relative_to(repo_root)

        # Check syntax
        syntax_error = validate_json_syntax(json_file)
        if syntax_error:
            errors.append(JSONError(str(rel_path), syntax_error))
            continue  # Skip further checks if syntax is invalid

        # Check schema
        schema_error = validate_json_schema(json_file, repo_root)
        if schema_error:
            errors.append(JSONError(str(rel_path), schema_error))

        # Check metadata consistency
        metadata_error = validate_metadata_consistency(json_file)
        if metadata_error:
            errors.append(JSONError(str(rel_path), metadata_error))

    return errors


def print_results(errors: List[JSONError]) -> bool:
    """Print validation results."""
    print("\n" + "=" * 70)
    print("📄 JSON Validation Results")
    print("=" * 70 + "\n")

    if not errors:
        print("✅ All JSON files are valid!")
        print("=" * 70)
        return True

    print(f"Found {len(errors)} issue(s):\n")
    for error in errors:
        print(error)
        print()

    print("=" * 70)
    print("❌ Validation FAILED")
    print("=" * 70)
    return False


def main():
    """Main validation function."""
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    errors = validate_all_json(repo_root)
    success = print_results(errors)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
