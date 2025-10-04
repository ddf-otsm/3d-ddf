#!/usr/bin/env python3
"""
Migrate Render Folder Names to Taxonomy Standard

Renames render output folders to follow the YYYYMMDD_HHMM_description format.
Uses file modification times as fallback when timestamp isn't in folder name.
"""

import re
from pathlib import Path
from datetime import datetime
import sys

def extract_timestamp_from_name(folder_name: str) -> tuple[str, str, str] | None:
    """
    Extract timestamp and description from folder name.
    Returns (date, time, description) or None
    """
    # Pattern: anything_YYYYMMDD_HHMM
    pattern1 = re.compile(r'(.+?)_(\d{8})_(\d{4})$')
    match = pattern1.match(folder_name)
    if match:
        desc, date, time = match.groups()
        return (date, time, desc)
    
    # Pattern: anything_YYYYMMDD
    pattern2 = re.compile(r'(.+?)_(\d{8})$')
    match = pattern2.match(folder_name)
    if match:
        desc, date = match.groups()
        return (date, "0000", desc)
    
    return None


def get_folder_timestamp(folder_path: Path) -> tuple[str, str]:
    """Get timestamp from folder's modification time."""
    mtime = folder_path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return (dt.strftime('%Y%m%d'), dt.strftime('%H%M'))


def migrate_folder(folder_path: Path, dry_run: bool = True) -> tuple[Path | None, str]:
    """
    Migrate a single folder to new naming convention.
    Returns (new_path, status_message)
    """
    folder_name = folder_path.name
    
    # Try to extract timestamp from name
    extracted = extract_timestamp_from_name(folder_name)
    
    if extracted:
        date, time, desc = extracted
        new_name = f"{date}_{time}_{desc}"
    else:
        # Use folder modification time
        date, time = get_folder_timestamp(folder_path)
        # Clean description (remove invalid chars)
        desc = re.sub(r'[^a-z0-9_-]', '_', folder_name.lower())
        desc = re.sub(r'_+', '_', desc).strip('_')
        new_name = f"{date}_{time}_{desc}"
    
    # Check if already in correct format
    if folder_name == new_name:
        return (None, f"✓ Already correct: {folder_name}")
    
    new_path = folder_path.parent / new_name
    
    # Check for conflicts
    if new_path.exists():
        return (None, f"⚠ Conflict: {folder_name} -> {new_name} (destination exists)")
    
    if dry_run:
        return (new_path, f"Would rename: {folder_name} -> {new_name}")
    else:
        folder_path.rename(new_path)
        return (new_path, f"✓ Renamed: {folder_name} -> {new_name}")


def main():
    """Main migration function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate render folders to taxonomy standard")
    parser.add_argument('--execute', action='store_true', 
                       help='Actually perform renames (default is dry-run)')
    parser.add_argument('--path', type=str, default='.',
                       help='Repository root path (default: current directory)')
    args = parser.parse_args()
    
    repo_root = Path(args.path).resolve()
    dry_run = not args.execute
    
    print("\n" + "=" * 70)
    print("📁 Render Folder Name Migration")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'EXECUTE (will rename)'}")
    print(f"Repository: {repo_root}")
    print("=" * 70 + "\n")
    
    # Find all render directories
    folders_to_migrate = []
    for renders_dir in repo_root.glob("**/renders"):
        if not renders_dir.is_dir():
            continue
            
        for folder in sorted(renders_dir.iterdir()):
            if not folder.is_dir():
                continue
            folders_to_migrate.append(folder)
    
    if not folders_to_migrate:
        print("✅ No folders found to migrate.")
        return 0
    
    print(f"Found {len(folders_to_migrate)} folders to check:\n")
    
    migrated = 0
    skipped = 0
    conflicts = 0
    
    for folder in folders_to_migrate:
        new_path, message = migrate_folder(folder, dry_run=dry_run)
        print(message)
        
        if new_path is not None and not dry_run:
            migrated += 1
        elif "Already correct" in message:
            skipped += 1
        elif "Conflict" in message:
            conflicts += 1
    
    print("\n" + "=" * 70)
    if dry_run:
        print(f"📊 Would migrate: {migrated} folders")
        print(f"   Already correct: {skipped}")
        print(f"   Conflicts: {conflicts}")
        print("\n💡 Run with --execute to perform actual renames")
    else:
        print(f"✅ Migration complete!")
        print(f"   Migrated: {migrated} folders")
        print(f"   Skipped: {skipped}")
        print(f"   Conflicts: {conflicts}")
    print("=" * 70 + "\n")
    
    return 0 if conflicts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
