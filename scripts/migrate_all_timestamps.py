#!/usr/bin/env python3
"""
Comprehensive Timestamp Migration

Migrates ALL project files and folders to timestamp-first naming convention:
- Report files (.txt)
- Log files (.log)
- Blend backup files (.blend)
- Export folders
- Any other timestamped artifacts
"""

import re
from pathlib import Path
from datetime import datetime
import sys

def extract_timestamp_from_filename(filename: str) -> tuple[str, str, str] | None:
    """
    Extract timestamp and description from various filename patterns.
    Returns (date, time, description) or None
    """
    # Remove extension for processing
    base = Path(filename).stem
    ext = Path(filename).suffix
    
    # Pattern 1: description_YYYYMMDD_HHMMSS (reports)
    pattern1 = re.compile(r'^(.+?)_(\d{8})_(\d{6})$')
    match = pattern1.match(base)
    if match:
        desc, date, time = match.groups()
        return (date, time[:4], desc)  # Use only HHMM
    
    # Pattern 2: description_YYYYMMDD_HHMM
    pattern2 = re.compile(r'^(.+?)_(\d{8})_(\d{4})$')
    match = pattern2.match(base)
    if match:
        desc, date, time = match.groups()
        return (date, time, desc)
    
    # Pattern 3: description_YYYYMMDD (no time)
    pattern3 = re.compile(r'^(.+?)_(\d{8})$')
    match = pattern3.match(base)
    if match:
        desc, date = match.groups()
        return (date, "0000", desc)
    
    # Pattern 4: Unix timestamp (dadosfera_alpha_1759251060)
    pattern4 = re.compile(r'^(.+?)_(\d{10})$')
    match = pattern4.match(base)
    if match:
        desc, unix_ts = match.groups()
        try:
            dt = datetime.fromtimestamp(int(unix_ts))
            return (dt.strftime('%Y%m%d'), dt.strftime('%H%M'), desc)
        except:
            pass
    
    return None


def get_item_timestamp(path: Path) -> tuple[str, str]:
    """Get timestamp from file/folder modification time."""
    mtime = path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return (dt.strftime('%Y%m%d'), dt.strftime('%H%M'))


def migrate_item(path: Path, dry_run: bool = True) -> tuple[Path | None, str]:
    """
    Migrate a file or folder to timestamp-first naming.
    Returns (new_path, status_message)
    """
    name = path.name
    
    # Check if already in correct format
    if re.match(r'^\d{8}_\d{4}_', name):
        return (None, f"✓ Already correct: {name}")
    
    # Try to extract timestamp
    extracted = extract_timestamp_from_filename(name)
    
    if extracted:
        date, time, desc = extracted
        # Clean description
        desc = re.sub(r'[^a-z0-9_.-]', '_', desc.lower())
        desc = re.sub(r'_+', '_', desc).strip('_')
        
        # Preserve extension for files
        if path.is_file():
            ext = path.suffix
            new_name = f"{date}_{time}_{desc}{ext}"
        else:
            new_name = f"{date}_{time}_{desc}"
    else:
        # Use modification time
        date, time = get_item_timestamp(path)
        desc = re.sub(r'[^a-z0-9_.-]', '_', name.lower())
        desc = re.sub(r'_+', '_', desc).strip('_')
        
        # Remove extension from description if it's a file
        if path.is_file():
            desc = Path(desc).stem
            ext = path.suffix
            new_name = f"{date}_{time}_{desc}{ext}"
        else:
            new_name = f"{date}_{time}_{desc}"
    
    new_path = path.parent / new_name
    
    # Check for conflicts
    if new_path.exists():
        return (None, f"⚠ Conflict: {name} -> {new_name} (destination exists)")
    
    if dry_run:
        return (new_path, f"Would rename: {name} -> {new_name}")
    else:
        path.rename(new_path)
        return (new_path, f"✓ Renamed: {name} -> {new_name}")


def find_items_to_migrate(repo_root: Path) -> dict[str, list[Path]]:
    """Find all files and folders that need migration."""
    items: dict[str, list[Path]] = {
        'reports': [],
        'logs': [],
        'blend_backups': [],
        'export_folders': [],
        'other': []
    }
    
    # Find report files
    reports_dir = repo_root / 'reports'
    if reports_dir.exists():
        for file in reports_dir.glob('*.txt'):
            if not re.match(r'^\d{8}_\d{4}_', file.name):
                items['reports'].append(file)
    
    # Find log files
    logs_dir = repo_root / 'logs'
    if logs_dir.exists():
        for file in logs_dir.glob('*.log'):
            if not re.match(r'^\d{8}_\d{4}_', file.name):
                items['logs'].append(file)
    
    # Find blend backup files with timestamps
    for blend_file in repo_root.glob('**/*.blend'):
        if '_backup_' in blend_file.name and not re.match(r'^\d{8}_\d{4}_', blend_file.name):
            items['blend_backups'].append(blend_file)
    
    # Find export folders with timestamps at end
    for export_dir in repo_root.glob('**/exports/*'):
        if export_dir.is_dir() and re.search(r'_\d{8}$', export_dir.name):
            if not re.match(r'^\d{8}_\d{4}_', export_dir.name):
                items['export_folders'].append(export_dir)
    
    return items


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate all timestamps to timestamp-first format")
    parser.add_argument('--execute', action='store_true',
                       help='Actually perform renames (default is dry-run)')
    parser.add_argument('--path', type=str, default='.',
                       help='Repository root path (default: current directory)')
    parser.add_argument('--category', choices=['reports', 'logs', 'blend_backups', 'export_folders', 'all'],
                       default='all', help='Category to migrate (default: all)')
    args = parser.parse_args()
    
    repo_root = Path(args.path).resolve()
    dry_run = not args.execute
    
    print("\n" + "=" * 70)
    print("📋 COMPREHENSIVE TIMESTAMP MIGRATION")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'EXECUTE (will rename)'}")
    print(f"Repository: {repo_root}")
    print(f"Category: {args.category}")
    print("=" * 70 + "\n")
    
    # Find all items
    items = find_items_to_migrate(repo_root)
    
    # Filter by category
    if args.category != 'all':
        items = {args.category: items[args.category]}
    
    # Count total items
    total = sum(len(v) for v in items.values())
    
    if total == 0:
        print("✅ No items found that need migration!")
        return 0
    
    print(f"Found {total} items to check:\n")
    
    # Show summary
    for category, item_list in items.items():
        if item_list:
            print(f"📁 {category.upper()}: {len(item_list)} items")
    print()
    
    # Migrate each category
    migrated = 0
    skipped = 0
    conflicts = 0
    
    for category, item_list in items.items():
        if not item_list:
            continue
            
        print(f"\n{'='*70}")
        print(f"📁 {category.upper()}")
        print('='*70 + "\n")
        
        for item in sorted(item_list):
            new_path, message = migrate_item(item, dry_run=dry_run)
            print(message)
            
            if new_path is not None:
                if not dry_run:
                    migrated += 1
            elif "Already correct" in message:
                skipped += 1
            elif "Conflict" in message:
                conflicts += 1
    
    print("\n" + "=" * 70)
    if dry_run:
        print(f"📊 Would migrate: {total - skipped} items")
        print(f"   Already correct: {skipped}")
        print(f"   Conflicts: {conflicts}")
        print("\n💡 Run with --execute to perform actual renames")
    else:
        print(f"✅ Migration complete!")
        print(f"   Migrated: {migrated} items")
        print(f"   Skipped: {skipped}")
        print(f"   Conflicts: {conflicts}")
    print("=" * 70 + "\n")
    
    return 0 if conflicts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
