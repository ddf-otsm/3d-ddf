#!/usr/bin/env python3
"""
Clean Production Scene

Removes test/debug elements from a Blender scene to prepare for production rendering:
- Hides or removes ground planes/test geometry
- Validates material assignments
- Checks camera setup
- Removes debug objects
- Saves cleaned version with timestamp backup

Usage:
  blender scene.blend --background --python clean_production_scene.py -- --output cleaned_scene.blend
"""

import bpy
import sys
from datetime import datetime
from pathlib import Path

# Test objects to remove or hide (case-insensitive)
TEST_OBJECT_PATTERNS = [
    'ground_plane',
    'test_',
    'debug_',
    'temp_',
    'placeholder_',
]

# Materials that should not be on main objects
FORBIDDEN_MATERIALS = [
    'Crystal_Glass',  # Should only be on Crystal_Core
]

def find_test_objects():
    """Find objects that match test patterns."""
    test_objects = []
    for obj in bpy.data.objects:
        obj_name_lower = obj.name.lower()
        for pattern in TEST_OBJECT_PATTERNS:
            if pattern in obj_name_lower:
                test_objects.append(obj)
                break
    return test_objects

def validate_materials():
    """Check for materials applied to wrong objects."""
    issues = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        if not obj.data.materials:
            continue
        
        for mat_slot in obj.data.materials:
            if not mat_slot:
                continue
            
            # Check if Crystal_Glass is on non-core objects
            if mat_slot.name == 'Crystal_Glass' and 'Crystal_Core' not in obj.name:
                issues.append(f"❌ {obj.name} has Crystal_Glass material (should only be on Crystal_Core)")
    
    return issues

def validate_camera():
    """Check camera setup."""
    issues = []
    
    camera = bpy.data.objects.get('Camera')
    if not camera:
        issues.append("❌ No camera found in scene")
        return issues
    
    # Check if camera is active
    if bpy.context.scene.camera != camera:
        issues.append("⚠️  Camera exists but is not set as active")
    
    # Check camera location (should be looking at origin area)
    loc = camera.location
    if loc.z < 0:
        issues.append(f"⚠️  Camera Z position is negative: {loc.z:.2f}")
    
    return issues

def hide_ground_plane():
    """Hide ground plane for rendering."""
    ground = bpy.data.objects.get('Ground_Plane')
    if ground:
        ground.hide_render = True
        ground.hide_viewport = True
        print(f"✓ Hidden Ground_Plane from render and viewport")
        return True
    return False

def clean_scene(dry_run=False):
    """Clean the scene of test elements."""
    print("\n" + "="*60)
    print("🧹 SCENE CLEANING REPORT")
    print("="*60)
    
    # Find test objects
    print("\n📦 Checking for test objects...")
    test_objects = find_test_objects()
    if test_objects:
        print(f"Found {len(test_objects)} test objects:")
        for obj in test_objects:
            print(f"  - {obj.name}")
            if not dry_run:
                if obj.name == 'Ground_Plane':
                    obj.hide_render = True
                    obj.hide_viewport = True
                    print(f"    → Hidden from render")
                else:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    print(f"    → Removed")
    else:
        print("  ✓ No test objects found")
    
    # Validate materials
    print("\n🎨 Checking material assignments...")
    material_issues = validate_materials()
    if material_issues:
        for issue in material_issues:
            print(f"  {issue}")
    else:
        print("  ✓ All materials correctly assigned")
    
    # Validate camera
    print("\n📷 Checking camera setup...")
    camera_issues = validate_camera()
    if camera_issues:
        for issue in camera_issues:
            print(f"  {issue}")
    else:
        print("  ✓ Camera setup correct")
    
    # Summary
    print("\n" + "="*60)
    total_issues = len(test_objects) + len(material_issues) + len(camera_issues)
    if total_issues == 0:
        print("✅ Scene is production-ready!")
    else:
        print(f"⚠️  Found {total_issues} issues")
        if dry_run:
            print("   (Dry run - no changes made)")
        else:
            print("   (Changes applied)")
    print("="*60 + "\n")
    
    return total_issues

def main():
    """Main execution."""
    import argparse
    
    # Parse args after "--"
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, help='Output blend file path')
    parser.add_argument('--dry-run', action='store_true', help='Check only, do not modify')
    args = parser.parse_args(argv)
    
    # Clean the scene
    issues_found = clean_scene(dry_run=args.dry_run)
    
    # Save if output specified and not dry run
    if args.output and not args.dry_run:
        output_path = Path(args.output)
        
        # Create backup of original if output is same as input
        current_file = Path(bpy.data.filepath)
        if output_path.resolve() == current_file.resolve():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = current_file.parent / f"{timestamp}_{current_file.stem}_backup.blend"
            print(f"Creating backup: {backup_path.name}")
            bpy.ops.wm.save_as_mainfile(filepath=str(backup_path), copy=True)
        
        # Save cleaned version
        print(f"Saving cleaned scene: {output_path}")
        bpy.ops.wm.save_as_mainfile(filepath=str(output_path))
        print("✓ Saved successfully")
    
    # Exit with error code if issues found
    sys.exit(0 if issues_found == 0 else 1)

if __name__ == "__main__":
    main()

