#!/usr/bin/env python3
"""
Migrate Export File Names to Taxonomy Standard

Renames export MP4 files to follow the YYYYMMDD_HHMM_description format.
Extracts timestamps and metadata from existing filenames.
"""

import re
from pathlib import Path
from datetime import datetime
import sys

def extract_metadata_from_filename(filename: str) -> tuple[str, str, str] | None:
    """
    Extract timestamp and description from export filename.
    Returns (date, time, description) or None
    
    Handles patterns like:
    - dadosfera_stable_20251002_1080p_cycles.mp4
    - dadosfera_alpha_20250930_1080p_partial_8sec.mp4
    - dadosfera_CYCLES_preview_20251002_2042.mp4
    """
    # Remove .mp4 extension
    base = filename.replace('.mp4', '')
    
    # Pattern 1: project_description_YYYYMMDD_HHMM (e.g., dadosfera_CYCLES_preview_20251002_2042)
    pattern1 = re.compile(r'^([a-z]+)_(.+?)_(\d{8})_(\d{4})$')
    match = pattern1.match(base)
    if match:
        project, desc, date, time = match.groups()
        return (date, time, f"{project}_{desc}")
    
    # Pattern 2: project_version_YYYYMMDD_quality_type (e.g., dadosfera_stable_20251002_1080p_cycles)
    pattern2 = re.compile(r'^([a-z]+)_([a-z]+)_(\d{8})_(.+)$')
    match = pattern2.match(base)
    if match:
        project, version, date, rest = match.groups()
        return (date, "0000", f"{project}_{version}_{rest}")
    
    # Pattern 3: project_YYYYMMDD_HHMM (e.g., dadosfera_20251002_2125)
    pattern3 = re.compile(r'^([a-z]+)_(\d{8})_(\d{4})$')
    match = pattern3.match(base)
    if match:
        project, date, time = match.groups()
        return (date, time, project)
    
    return None


def get_file_timestamp(file_path: Path) -> tuple[str, str]:
    """Get timestamp from file's modification time."""
    mtime = file_path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return (dt.strftime('%Y%m%d'), dt.strftime('%H%M'))


def migrate_export_file(file_path: Path, dry_run: bool = True) -> tuple[Path | None, str]:
    """
    Migrate a single export file to new naming convention.
    Returns (new_path, status_message)
    """
    filename = file_path.name
    
    # Skip non-MP4 files and special files
    if not filename.endswith('.mp4'):
        return (None, f"⊘ Skipped: {filename} (not an MP4)")
    
    if filename in ['README.md', '.DS_Store']:
        return (None, f"⊘ Skipped: {filename} (special file)")
    
    # Try to extract metadata from filename
    extracted = extract_metadata_from_filename(filename)
    
    if extracted:
        date, time, desc = extracted
        # Clean description
        desc = re.sub(r'[^a-z0-9_-]', '_', desc.lower())
        desc = re.sub(r'_+', '_', desc).strip('_')
        new_name = f"{date}_{time}_{desc}.mp4"
    else:
        # Use file modification time as fallback
        date, time = get_file_timestamp(file_path)
        # Clean filename for description
        desc = re.sub(r'[^a-z0-9_-]', '_', filename.replace('.mp4', '').lower())
        desc = re.sub(r'_+', '_', desc).strip('_')
        new_name = f"{date}_{time}_{desc}.mp4"
    
    # Check if already in correct format
    pattern = re.compile(r'^\d{8}_\d{4}_.+\.mp4$')
    if pattern.match(filename):
        return (None, f"✓ Already correct: {filename}")
    
    new_path = file_path.parent / new_name
    
    # Check for conflicts
    if new_path.exists():
        return (None, f"⚠ Conflict: {filename} -> {new_name} (destination exists)")
    
    if dry_run:
        return (new_path, f"Would rename: {filename} -> {new_name}")
    else:
        file_path.rename(new_path)
        return (new_path, f"✓ Renamed: {filename} -> {new_name}")


def main():
    """Main migration function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate export files to taxonomy standard")
    parser.add_argument('--execute', action='store_true', 
                       help='Actually perform renames (default is dry-run)')
    parser.add_argument('--path', type=str, default='.',
                       help='Repository root path (default: current directory)')
    parser.add_argument('--exports-dir', type=str, default='projects/dadosfera/exports',
                       help='Exports directory relative to repo root')
    args = parser.parse_args()
    
    repo_root = Path(args.path).resolve()
    exports_dir = repo_root / args.exports_dir
    dry_run = not args.execute
    
    if not exports_dir.exists():
        print(f"❌ Export directory not found: {exports_dir}")
        return 1
    
    print("\n" + "=" * 70)
    print("🎬 Export File Name Migration")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'EXECUTE (will rename)'}")
    print(f"Export directory: {exports_dir}")
    print("=" * 70 + "\n")
    
    # Find all export files
    export_files = sorted(exports_dir.glob("*.mp4"))
    
    if not export_files:
        print("✅ No MP4 files found to migrate.")
        return 0
    
    print(f"Found {len(export_files)} export files to check:\n")
    
    migrated = 0
    skipped = 0
    conflicts = 0
    
    for file_path in export_files:
        new_path, message = migrate_export_file(file_path, dry_run=dry_run)
        print(message)
        
        if new_path is not None and not dry_run:
            migrated += 1
        elif "Already correct" in message:
            skipped += 1
        elif "Conflict" in message:
            conflicts += 1
    
    print("\n" + "=" * 70)
    if dry_run:
        print(f"📊 Would migrate: {len(export_files) - skipped} files")
        print(f"   Already correct: {skipped}")
        print(f"   Conflicts: {conflicts}")
        print("\n💡 Run with --execute to perform actual renames")
    else:
        print(f"✅ Migration complete!")
        print(f"   Migrated: {migrated} files")
        print(f"   Skipped: {skipped}")
        print(f"   Conflicts: {conflicts}")
    print("=" * 70 + "\n")
    
    return 0 if conflicts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
