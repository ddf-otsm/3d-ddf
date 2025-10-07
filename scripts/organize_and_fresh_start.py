#!/usr/bin/env python3
"""
Organize blend files and create fresh baseline scenes
Run this after user approves the fresh start approach
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Dynamic project root detection: use env var if provided; otherwise walk up to repo root
def _detect_project_root() -> Path:
    start = Path(__file__).resolve()
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    # Fallback: assume this file lives under <repo>/scripts/
    return Path(__file__).resolve().parent.parent

PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", str(_detect_project_root())))

def organize_dadosfera():
    """Archive old dadosfera files"""
    print("\n🗂️  Organizing Dadosfera files...")
    
    base = PROJECT_ROOT / "projects/dadosfera/blender_files"
    archive_dir = base / "archived/v1_original"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_archive = [
        base / "active/dadosfera_animation_v1.blend",
        base / "archive/dadosfera_animation_v1_improved_explosions.blend",
    ]
    
    for file in files_to_archive:
        if file.exists():
            dest = archive_dir / file.name
            print(f"  Moving: {file.name} → archived/v1_original/")
            shutil.move(str(file), str(dest))
    
    # Move backups
    backup_src = base / "backups"
    if backup_src.exists():
        for backup in backup_src.glob("*.blend"):
            dest = archive_dir / backup.name
            print(f"  Moving: {backup.name} → archived/v1_original/")
            shutil.move(str(backup), str(dest))
    
    print("  ✓ Dadosfera files archived")

def organize_explosion_test():
    """Archive old explosion test files"""
    print("\n🗂️  Organizing Explosion-Test files...")
    
    base = PROJECT_ROOT / "projects/explosion-test/blender_files"
    archive_dir = base / "archived/geometry_tests"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_archive = [
        base / "active/ultra_realistic_explosion_refined.blend",
        base / "hybrid_quick_test.blend",
    ]
    
    for file in files_to_archive:
        if file.exists():
            dest = archive_dir / file.name
            print(f"  Moving: {file.name} → archived/geometry_tests/")
            shutil.move(str(file), str(dest))
    
    # Move archived tests
    archive_src = base / "archive"
    if archive_src.exists():
        for test in archive_src.glob("*.blend"):
            dest = archive_dir / test.name
            print(f"  Moving: {test.name} → archived/geometry_tests/")
            shutil.move(str(test), str(dest))
    
    print("  ✓ Explosion-Test files archived")

def create_readme_files():
    """Create README files explaining the organization"""
    print("\n📝 Creating README files...")
    
    # Dadosfera archived README
    dadosfera_readme = PROJECT_ROOT / "projects/dadosfera/blender_files/archived/v1_original/README.md"
    dadosfera_readme.write_text(f"""# Archived V1 Files

**Archived on**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Reason**: Starting fresh with improved approach

## Files Archived

These files represented the first attempt at the Dadosfera animation, but had several issues:
- Simple geometry-based "explosions" (not real particle systems)
- Checker texture floor (not professional looking)
- Basic lighting setup

## What Was Learned

✓ Initial composition and camera angles  
✓ Dadosfera text/logo 3D model  
✓ Animation timing basics  
✗ Explosion approach was too simple  
✗ Materials needed improvement  
✗ Lighting needed professional setup  

## New Approach (V2)

See `../active/dadosfera_v2_clean.blend` for the fresh start with:
- Real particle-based explosions
- Professional PBR materials
- Studio-quality lighting
- Clean, optimized scene structure
""")
    
    # Explosion-test archived README
    explosion_readme = PROJECT_ROOT / "projects/explosion-test/blender_files/archived/geometry_tests/README.md"
    explosion_readme.write_text(f"""# Archived Geometry Test Files

**Archived on**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Reason**: These files used simple geometry, not real particle systems

## Files Archived

All these files attempted to create explosions using geometry with emission shaders:
- `ultra_realistic_explosion_refined.blend` - Most developed version
- `hybrid_quick_test.blend` - Minimal test setup
- `explosion_test_scene.blend` - Early test
- `realistic_explosion_test.blend` - Iteration
- `ultra_realistic_explosion*.blend` - Various attempts

## Why This Approach Failed

❌ Geometry-based explosions don't look realistic  
❌ No volumetric fire/smoke simulation  
❌ No proper physics or turbulence  
❌ Static appearance, not dynamic  

## New Approach

See `../active/particle_explosion_v1.blend` for the fresh start with:
- Quick Smoke particle emitter
- Fire + Smoke domain with proper settings
- Volumetric rendering
- Realistic physics simulation
- Optimized for production rendering
""")
    
    print(f"  ✓ Created archived/v1_original/README.md")
    print(f"  ✓ Created archived/geometry_tests/README.md")

def create_placeholder_active_files():
    """Create placeholder files for the new active files"""
    print("\n📄 Creating placeholder markers...")
    
    # Dadosfera active placeholder
    dadosfera_active = PROJECT_ROOT / "projects/dadosfera/blender_files/active/CREATE_dadosfera_v2_clean.txt"
    dadosfera_active.write_text("""# Create: dadosfera_v2_clean.blend

This file should be created with:

1. Dadosfera 3D text/logo (clean import)
2. Professional metallic/glass material
3. Studio floor (concrete or similar PBR texture)
4. 3-point lighting + HDRI environment
5. Proper camera setup
6. NO explosion objects yet (add those later from explosion-test)

Estimated time: 2-3 hours

See BLEND_FILE_ORGANIZATION.md for detailed steps.
""")
    
    # Explosion-test active placeholder
    explosion_active = PROJECT_ROOT / "projects/explosion-test/blender_files/active/CREATE_particle_explosion_v1.txt"
    explosion_active.write_text("""# Create: particle_explosion_v1.blend

This file should be created with:

1. Quick Smoke particle emitter
2. Fire + Smoke domain configuration
3. Volumetric material setup
4. Proper resolution settings for baking
5. Test render to validate realism

Estimated time: 3-4 hours

See BLEND_FILE_ORGANIZATION.md for detailed steps.

References:
- Blender Quick Smoke tutorial
- Volumetric rendering best practices
- Production optimization for smoke sims
""")
    
    print(f"  ✓ Created active/CREATE_dadosfera_v2_clean.txt")
    print(f"  ✓ Created active/CREATE_particle_explosion_v1.txt")

def main():
    print("=" * 60)
    print("BLEND FILE ORGANIZATION & FRESH START")
    print("=" * 60)
    
    # Check if we should proceed
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-y", "--yes", action="store_true", help="Run non-interactively and proceed without prompt")
    args, _ = parser.parse_known_args()

    print("\n⚠️  This will:")
    print("  1. Move all current active files to archived/")
    print("  2. Clear active/ folders")
    print("  3. Create placeholder files for new baseline scenes")
    print("\nOriginal files will be preserved in archived/ folders.")

    if not args.yes and os.environ.get("ORGANIZE_ASSUME_YES", "").lower() not in ("1", "true", "yes", "y"):
        response = input("\n🤔 Proceed? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("\n❌ Cancelled. No changes made.")
            return
    else:
        print("\n✅ Proceeding non-interactively")
    
    # Execute organization
    organize_dadosfera()
    organize_explosion_test()
    create_readme_files()
    create_placeholder_active_files()
    
    print("\n" + "=" * 60)
    print("✅ ORGANIZATION COMPLETE!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("  1. Review archived files in:")
    print("     - projects/dadosfera/blender_files/archived/v1_original/")
    print("     - projects/explosion-test/blender_files/archived/geometry_tests/")
    print("\n  2. Create fresh baseline scenes:")
    print("     - dadosfera_v2_clean.blend")
    print("     - particle_explosion_v1.blend")
    print("\n  3. Follow implementation plan in:")
    print("     projects/BLEND_FILE_ORGANIZATION.md")
    print("\n🎬 Ready to start fresh with proper approach!")

if __name__ == "__main__":
    main()
