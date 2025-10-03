#!/usr/bin/env python3
"""
Add camera work for more dramatic explosion effects
This script adds camera shake, movement, and framing improvements
for cinematic explosion sequences
"""

import bpy
import bmesh
from mathutils import Vector, Euler
import random
import math


def add_camera_shake():
    """Add realistic camera shake during explosion"""
    print("📹 Adding camera shake for explosion drama...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot add camera shake")
        return False

    # Create keyframes for camera shake during explosion
    shake_frames = [
        (10, (0, 0, 0)),        # Start - no shake
        (12, (0.02, 0.01, 0)),  # Initial shake
        (14, (-0.03, -0.02, 0.01)),  # Build up
        (16, (0.04, 0.03, -0.02)),   # Peak shake
        (18, (-0.02, -0.01, 0.01)),  # Settle
        (20, (0.01, 0.005, 0)),      # Residual
        (25, (0, 0, 0)),        # Return to normal
    ]

    original_location = camera.location.copy()

    for frame, (shake_x, shake_y, shake_z) in shake_frames:
        camera.location = (
            original_location[0] + shake_x,
            original_location[1] + shake_y,
            original_location[2] + shake_z
        )
        camera.keyframe_insert(data_path="location", frame=frame)

    print("   ✅ Added camera shake animation")
    return True


def add_camera_movement():
    """Add subtle camera movement for dynamic framing"""
    print("🎬 Adding camera movement for dynamic framing...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot add camera movement")
        return False

    # Add subtle tracking movement
    movement_frames = [
        (1, (7.36, -6.93, 4.96)),     # Initial position
        (15, (7.4, -6.9, 5.0)),       # Slight pull back during explosion
        (30, (7.3, -6.95, 4.9)),      # Slight adjustment
        (45, (7.35, -6.92, 4.95)),    # Return close to original
    ]

    for frame, (x, y, z) in movement_frames:
        camera.location = (x, y, z)
        camera.keyframe_insert(data_path="location", frame=frame)

    print("   ✅ Added camera movement animation")
    return True


def add_camera_rotation():
    """Add subtle camera rotation for more dynamic feel"""
    print("🔄 Adding camera rotation for dynamic feel...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot add camera rotation")
        return False

    # Add very subtle rotation changes
    rotation_frames = [
        (1, (1.109, 0, 0.814)),      # Initial rotation
        (15, (1.115, 0.005, 0.81)),  # Slight tilt during explosion
        (30, (1.105, -0.003, 0.818)), # Opposite tilt
        (45, (1.11, 0, 0.815)),      # Return close to original
    ]

    for frame, (x, y, z) in rotation_frames:
        camera.rotation_euler = (x, y, z)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    print("   ✅ Added camera rotation animation")
    return True


def optimize_camera_settings():
    """Optimize camera settings for explosion rendering"""
    print("⚙️ Optimizing camera settings...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot optimize settings")
        return False

    # Set camera to optimal settings for explosion
    camera.data.clip_start = 0.1
    camera.data.clip_end = 100.0

    # Set field of view for dramatic effect (if perspective)
    if camera.data.type == 'PERSP':
        camera.data.angle = math.radians(45)  # 45-degree FOV

    print("   ✅ Optimized camera clip distances and FOV")
    return True


def add_dof_effect():
    """Add depth of field effect for more cinematic look"""
    print("🌟 Adding depth of field effect...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot add DOF")
        return False

    # Enable depth of field
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 8.0  # Focus on explosion area
    camera.data.dof.aperture_fstop = 2.8   # Moderate blur

    # Set focus object if explosion center exists
    explosion_center = Vector((0, 0, 1.5))
    # Create an empty at explosion center for focus target
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=explosion_center)
    focus_empty = bpy.context.active_object
    focus_empty.name = "Explosion_Focus_Target"

    camera.data.dof.focus_object = focus_empty

    print("   ✅ Added depth of field with focus on explosion")
    return True


def smooth_keyframes():
    """Smooth camera keyframes for more natural movement"""
    print("🎯 Smoothing camera keyframes...")

    camera = bpy.context.scene.camera
    if not camera or not camera.animation_data:
        print("   ⚠️  No camera animation data to smooth")
        return False

    # Set interpolation to bezier for smoother curves
    for fcurve in camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            # Adjust handles for smoother curves
            keyframe.handle_left_type = 'AUTO'
            keyframe.handle_right_type = 'AUTO'

    print("   ✅ Smoothed camera animation curves")
    return True


def create_camera_report():
    """Create a report on camera enhancements"""
    print("\n📷 CAMERA WORK ENHANCEMENT REPORT")
    print("=" * 40)

    camera = bpy.context.scene.camera
    if camera:
        print(f"Camera: {camera.name}")
        print(f"Type: {camera.data.type}")
        print(f"Location: {camera.location}")
        print(f"Rotation: {camera.rotation_euler}")
        print(f"FOV: {math.degrees(camera.data.angle):.1f}°")
        print(f"DOF Enabled: {camera.data.dof.use_dof}")
        if camera.data.dof.use_dof:
            print(f"Focus Distance: {camera.data.dof.focus_distance}")
            print(f"Aperture: f/{camera.data.dof.aperture_fstop}")

        # Count keyframes
        if camera.animation_data and camera.animation_data.action:
            location_keyframes = 0
            rotation_keyframes = 0
            for fcurve in camera.animation_data.action.fcurves:
                if 'location' in fcurve.data_path:
                    location_keyframes += len(fcurve.keyframe_points)
                elif 'rotation' in fcurve.data_path:
                    rotation_keyframes += len(fcurve.keyframe_points)

            print(f"Location Keyframes: {location_keyframes}")
            print(f"Rotation Keyframes: {rotation_keyframes}")
    else:
        print("No camera found in scene")

    enhancements = [
        "✅ Added realistic camera shake during explosion",
        "✅ Implemented dynamic camera movement",
        "✅ Added subtle camera rotation",
        "✅ Optimized camera settings for explosions",
        "✅ Enabled depth of field effect",
        "✅ Smoothed animation curves"
    ]

    print("\n🎯 Camera Enhancements:")
    for enhancement in enhancements:
        print(f"   {enhancement}")

    print("\n🎯 Expected Results:")
    print("   • More cinematic explosion presentation")
    print("   • Realistic camera shake from explosion force")
    print("   • Dynamic framing that follows the action")
    print("   • Enhanced depth perception with DOF")
    print("   • Smoother, more professional camera movement")
    print("   • Increased dramatic impact of explosion sequences")

    return True


def save_camera_enhanced_scene():
    """Save the camera-enhanced scene"""
    output_path = "/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/blender_files/ultra_realistic_explosion_camera.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"💾 Saved camera-enhanced scene: {output_path}")
    return output_path


def main():
    print("📷 CAMERA WORK ENHANCEMENT FOR ULTRA-REALISTIC EXPLOSIONS")
    print("=" * 60)
    print("This script adds camera shake, movement, and cinematic effects")
    print("for more dramatic and professional explosion sequences.")
    print()

    # Check if we're in the right scene
    if not bpy.data.filepath or "ultra_realistic_explosion" not in bpy.data.filepath:
        print("⚠️  Warning: Not in ultra_realistic_explosion scene")
        print("   Please open the enhanced explosion scene first")
        return

    print("🎯 Starting camera work enhancement process...")

    # Apply camera enhancements
    shake_added = add_camera_shake()
    movement_added = add_camera_movement()
    rotation_added = add_camera_rotation()
    settings_optimized = optimize_camera_settings()
    dof_added = add_dof_effect()
    keyframes_smoothed = smooth_keyframes()

    # Create report
    create_camera_report()

    # Save enhanced scene
    saved_path = save_camera_enhanced_scene()

    print("\n" + "=" * 60)
    print("✅ CAMERA WORK ENHANCEMENT COMPLETE!")
    print("=" * 60)
    print("Enhancements applied:")
    print(f"   • {'✅' if shake_added else '❌'} camera shake added")
    print(f"   • {'✅' if movement_added else '❌'} camera movement added")
    print(f"   • {'✅' if rotation_added else '❌'} camera rotation added")
    print(f"   • {'✅' if settings_optimized else '❌'} camera settings optimized")
    print(f"   • {'✅' if dof_added else '❌'} depth of field added")
    print(f"   • {'✅' if keyframes_smoothed else '❌'} keyframes smoothed")
    print(f"   • Camera-enhanced scene saved to: {saved_path}")
    print("\n🎯 Cinematic Effects Added:")
    print("   • Realistic camera shake from explosion impact")
    print("   • Dynamic camera movement following the action")
    print("   • Professional depth of field focus on explosion")
    print("   • Smooth bezier animation curves")
    print("   • Enhanced dramatic presentation")
    print("   • Cinematic explosion sequences ready for production")


if __name__ == "__main__":
    main()
