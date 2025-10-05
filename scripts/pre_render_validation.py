#!/usr/bin/env python3
"""
Pre-Render Validation

Validates a Blender scene before rendering to catch issues early:
- Test/debug objects that shouldn't be visible
- Material assignments
- Camera setup and framing
- Lighting configuration
- Render settings
- Scene integrity

Usage:
  blender scene.blend --background --python pre_render_validation.py

Exit Codes:
  0 = Scene is production-ready
  1 = Warnings found (proceed with caution)
  2 = Errors found (do not render)
"""

import bpy
import sys

def check_test_objects():
    """Check for test/debug objects that should not be rendered."""
    issues = []
    warnings = []
    
    test_patterns = ['test_', 'debug_', 'temp_', 'placeholder_']
    
    for obj in bpy.data.objects:
        obj_name_lower = obj.name.lower()
        
        # Check for test patterns
        for pattern in test_patterns:
            if pattern in obj_name_lower:
                if obj.hide_render:
                    warnings.append(f"⚠️  Test object exists but hidden: {obj.name}")
                else:
                    issues.append(f"❌ Test object visible in render: {obj.name}")
                break
        
        # Check for Ground_Plane
        if obj_name_lower == 'ground_plane':
            if not obj.hide_render:
                issues.append(f"❌ Ground_Plane is visible in render")
            else:
                warnings.append(f"✓ Ground_Plane correctly hidden")
    
    return issues, warnings

def check_materials():
    """Validate material assignments."""
    issues = []
    warnings = []
    
    # Check for objects without materials
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        if not obj.data.materials:
            if obj.visible_camera:
                warnings.append(f"⚠️  Object visible but has no material: {obj.name}")
    
    # Check for specific material misuse
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or not obj.data.materials:
            continue
        
        for mat_slot in obj.data.materials:
            if not mat_slot:
                continue
            
            # Crystal_Glass should only be on Crystal_Core
            if mat_slot.name == 'Crystal_Glass' and 'Crystal_Core' not in obj.name:
                issues.append(f"❌ {obj.name} has Crystal_Glass material (wrong object)")
    
    return issues, warnings

def check_camera():
    """Validate camera setup."""
    issues = []
    warnings = []
    
    camera = bpy.context.scene.camera
    
    if not camera:
        issues.append("❌ No active camera in scene")
        return issues, warnings
    
    # Check camera location
    loc = camera.location
    if loc.z < 0:
        warnings.append(f"⚠️  Camera Z below 0: {loc.z:.2f}")
    
    # Check if camera can see main objects
    scene_objects = [obj for obj in bpy.data.objects 
                    if obj.type == 'MESH' and 'dadosfera' in obj.name.lower()]
    
    if not scene_objects:
        warnings.append("⚠️  No main objects found in scene")
    
    return issues, warnings

def check_render_settings():
    """Validate render settings."""
    issues = []
    warnings = []
    
    scene = bpy.context.scene
    
    # Check render engine
    if scene.render.engine != 'CYCLES':
        warnings.append(f"⚠️  Render engine is {scene.render.engine}, expected CYCLES")
    
    # Check resolution
    if scene.render.resolution_x < 1920 or scene.render.resolution_y < 1080:
        warnings.append(f"⚠️  Low resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
    
    # Check samples
    if scene.cycles.samples < 64:
        warnings.append(f"⚠️  Low sample count: {scene.cycles.samples}")
    
    # Check output format
    if scene.render.image_settings.file_format not in ['PNG', 'OPEN_EXR']:
        warnings.append(f"⚠️  Output format: {scene.render.image_settings.file_format}")
    
    return issues, warnings

def check_scene_integrity():
    """Check overall scene integrity."""
    issues = []
    warnings = []
    
    # Check for missing dependencies
    if bpy.data.is_dirty:
        warnings.append("⚠️  Scene has unsaved changes")
    
    # Check for broken links
    broken_images = [img for img in bpy.data.images if img.filepath and not img.packed_file]
    if broken_images:
        for img in broken_images[:3]:  # Show first 3
            warnings.append(f"⚠️  External image: {img.name}")
    
    return issues, warnings

def main():
    """Run all validation checks."""
    print("\n" + "="*60)
    print("🔍 PRE-RENDER VALIDATION")
    print("="*60)
    print(f"Blend file: {bpy.data.filepath}")
    print()
    
    all_issues = []
    all_warnings = []
    
    # Run all checks
    checks = [
        ("Test Objects", check_test_objects),
        ("Materials", check_materials),
        ("Camera", check_camera),
        ("Render Settings", check_render_settings),
        ("Scene Integrity", check_scene_integrity),
    ]
    
    for check_name, check_func in checks:
        print(f"📋 Checking {check_name}...")
        issues, warnings = check_func()
        
        if issues:
            all_issues.extend(issues)
            for issue in issues:
                print(f"   {issue}")
        
        if warnings:
            all_warnings.extend(warnings)
            for warning in warnings:
                print(f"   {warning}")
        
        if not issues and not warnings:
            print(f"   ✓ {check_name} OK")
        
        print()
    
    # Summary
    print("="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    print(f"Errors: {len(all_issues)}")
    print(f"Warnings: {len(all_warnings)}")
    
    if len(all_issues) > 0:
        print("\n❌ VALIDATION FAILED - DO NOT RENDER")
        print("Fix the errors above before rendering")
        exit_code = 2
    elif len(all_warnings) > 0:
        print("\n⚠️  VALIDATION PASSED WITH WARNINGS")
        print("Review warnings, but safe to render")
        exit_code = 1
    else:
        print("\n✅ VALIDATION PASSED - READY TO RENDER")
        exit_code = 0
    
    print("="*60 + "\n")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
