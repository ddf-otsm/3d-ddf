#!/usr/bin/env python3
"""
Refine explosion animations for better realism
This script enhances particle animations with more realistic physics,
turbulence, and timing adjustments
"""

import bpy
import bmesh
from mathutils import Vector, Euler
import random
import math


def add_turbulence_to_particles():
    """Add turbulence and secondary motion to fire particles"""
    print("🌪️ Adding turbulence and secondary motion to particles...")

    enhanced_count = 0

    for obj in bpy.data.objects:
        if obj.name.startswith("Ultra_Fire_"):
            # Add slight random rotation for more natural fire movement
            if not obj.animation_data or not obj.animation_data.action:
                continue

            # Add turbulence keyframes to existing animation
            for fcurve in obj.animation_data.action.fcurves:
                if 'location' in fcurve.data_path:
                    # Add small turbulence to position
                    for keyframe in fcurve.keyframe_points:
                        frame = keyframe.co[0]
                        current_value = keyframe.co[1]

                        # Add small random turbulence (0.1-0.3 units)
                        turbulence = random.uniform(-0.2, 0.2)
                        keyframe.co[1] = current_value + turbulence

            # Add subtle rotation animation
            obj.rotation_euler = (0, 0, random.uniform(-0.5, 0.5))
            obj.keyframe_insert(data_path="rotation_euler", frame=obj.animation_data.action.frame_range[0])

            # Rotate slightly over time
            rotation_frames = [10, 20, 30, 40]
            for frame in rotation_frames:
                if frame <= obj.animation_data.action.frame_range[1]:
                    rotation_z = random.uniform(-1.0, 1.0)
                    obj.rotation_euler = (obj.rotation_euler[0], obj.rotation_euler[1], rotation_z)
                    obj.keyframe_insert(data_path="rotation_euler", frame=frame)

            enhanced_count += 1

    print(f"   Enhanced {enhanced_count} fire particles with turbulence")
    return enhanced_count


def improve_debris_physics():
    """Improve debris physics with better trajectories and bouncing"""
    print("🏀 Improving debris physics and trajectories...")

    enhanced_count = 0

    for obj in bpy.data.objects:
        if obj.name.startswith("Ultra_Debris_"):
            if not obj.animation_data or not obj.animation_data.action:
                continue

            # Add more realistic bouncing for some debris
            if random.random() < 0.3:  # 30% of debris will bounce
                # Find location keyframes
                location_curves = {}
                for fcurve in obj.animation_data.action.fcurves:
                    if 'location' in fcurve.data_path:
                        axis = fcurve.data_path.split('.')[-1]  # x, y, or z
                        location_curves[axis] = fcurve

                if 'z' in location_curves:  # Add bounce to vertical motion
                    z_curve = location_curves['z']

                    # Add a bounce keyframe around frame 40-50
                    bounce_frame = random.randint(40, 50)
                    bounce_height = random.uniform(0.5, 1.5)

                    # Create bounce keyframe
                    obj.location.z = bounce_height
                    obj.keyframe_insert(data_path="location", frame=bounce_frame)

                    # Add slight horizontal movement during bounce
                    if random.random() < 0.5:
                        bounce_x = obj.location.x + random.uniform(-0.3, 0.3)
                        bounce_y = obj.location.y + random.uniform(-0.3, 0.3)
                        obj.location.x = bounce_x
                        obj.location.y = bounce_y
                        obj.keyframe_insert(data_path="location", frame=bounce_frame)

            # Add more realistic rotation (tumbling)
            rotation_frames = [15, 25, 35, 45, 55]
            for frame in rotation_frames:
                if frame <= obj.animation_data.action.frame_range[1]:
                    # Add random tumbling rotation
                    rot_x = random.uniform(-2.0, 2.0)
                    rot_y = random.uniform(-2.0, 2.0)
                    rot_z = random.uniform(-3.0, 3.0)

                    obj.rotation_euler = (rot_x, rot_y, rot_z)
                    obj.keyframe_insert(data_path="rotation_euler", frame=frame)

            enhanced_count += 1

    print(f"   Enhanced {enhanced_count} debris objects with better physics")
    return enhanced_count


def add_smoke_dynamics():
    """Add more dynamic smoke movement and behavior"""
    print("💨 Enhancing smoke dynamics...")

    smoke_obj = None
    for obj in bpy.data.objects:
        if obj.name.startswith("Ultra_Smoke"):
            smoke_obj = obj
            break

    if smoke_obj and smoke_obj.animation_data and smoke_obj.animation_data.action:
        print("   Found smoke object - enhancing dynamics")

        # Add more complex smoke movement
        base_frames = [15, 25, 35, 45, 55]

        for frame in base_frames:
            if frame <= smoke_obj.animation_data.action.frame_range[1]:
                # Add swirling motion to smoke
                swirl_x = smoke_obj.location.x + random.uniform(-0.8, 0.8)
                swirl_y = smoke_obj.location.y + random.uniform(-0.8, 0.8)
                swirl_z = smoke_obj.location.z + random.uniform(0.2, 0.8)

                smoke_obj.location = (swirl_x, swirl_y, swirl_z)

                # Add scale variation for more natural smoke
                current_scale = smoke_obj.scale
                scale_variation = random.uniform(0.9, 1.1)
                smoke_obj.scale = (
                    current_scale[0] * scale_variation,
                    current_scale[1] * scale_variation,
                    current_scale[2] * scale_variation * random.uniform(0.8, 1.2)  # More variation in height
                )

                smoke_obj.keyframe_insert(data_path="location", frame=frame)
                smoke_obj.keyframe_insert(data_path="scale", frame=frame)

        print("   ✅ Enhanced smoke with dynamic movement and scaling")
        return True

    print("   ⚠️  No smoke object found or no animation data")
    return False


def add_timing_variations():
    """Add slight timing variations for more natural explosion sequence"""
    print("⏰ Adding timing variations for more natural sequence...")

    # Slightly offset the start times of different particle groups
    fire_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Ultra_Fire_")]
    debris_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Ultra_Debris_")]

    # Add slight delays to fire particles (0-2 frames)
    for obj in fire_objects[:20]:  # First 20 fire particles
        if obj.animation_data and obj.animation_data.action:
            # Shift all keyframes by small random amount
            delay = random.uniform(0, 2)
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.co[0] += delay

    # Add larger delays to debris (2-5 frames)
    for obj in debris_objects[:15]:  # First 15 debris objects
        if obj.animation_data and obj.animation_data.action:
            delay = random.uniform(2, 5)
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.co[0] += delay

    print("   ✅ Added timing variations to particle groups")
    return True


def optimize_keyframes():
    """Optimize keyframe data for better performance and smoother animation"""
    print("🔧 Optimizing keyframe data...")

    total_objects = 0
    optimized_objects = 0

    for obj in bpy.data.objects:
        if obj.name.startswith(("Ultra_Fire_", "Ultra_Debris_", "Ultra_Smoke_")):
            total_objects += 1

            if obj.animation_data and obj.animation_data.action:
                # Simplify keyframes by removing redundant ones
                for fcurve in obj.animation_data.action.fcurves:
                    keyframes = fcurve.keyframe_points

                    # Remove keyframes that are too close in value (redundant)
                    to_remove = []
                    for i in range(1, len(keyframes) - 1):
                        prev_val = keyframes[i-1].co[1]
                        curr_val = keyframes[i].co[1]
                        next_val = keyframes[i+1].co[1]

                        # If current keyframe is very close to both neighbors, remove it
                        if abs(curr_val - prev_val) < 0.01 and abs(curr_val - next_val) < 0.01:
                            to_remove.append(i)

                    # Remove from end to start to maintain indices
                    for i in reversed(to_remove):
                        keyframes.remove(keyframes[i])

                optimized_objects += 1

    print(f"   Optimized keyframes for {optimized_objects}/{total_objects} objects")
    return optimized_objects


def add_camera_shake():
    """Add subtle camera shake for more dramatic explosion effect"""
    print("📹 Adding subtle camera shake...")

    camera = bpy.context.scene.camera
    if not camera:
        print("   ⚠️  No camera found - cannot add camera shake")
        return False

    # Add very subtle camera shake during explosion
    shake_frames = [12, 15, 18, 22, 28]

    for frame in shake_frames:
        # Very subtle shake (0.02-0.05 units)
        shake_x = random.uniform(-0.03, 0.03)
        shake_y = random.uniform(-0.03, 0.03)
        shake_z = random.uniform(-0.02, 0.02)

        camera.location = (
            camera.location[0] + shake_x,
            camera.location[1] + shake_y,
            camera.location[2] + shake_z
        )

        # Add slight rotation shake
        shake_rot_x = random.uniform(-0.01, 0.01)
        shake_rot_y = random.uniform(-0.01, 0.01)
        shake_rot_z = random.uniform(-0.02, 0.02)

        camera.rotation_euler = (
            camera.rotation_euler[0] + shake_rot_x,
            camera.rotation_euler[1] + shake_rot_y,
            camera.rotation_euler[2] + shake_rot_z
        )

        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Return camera to original position gradually
    original_location = camera.location.copy()
    original_rotation = camera.rotation_euler.copy()

    camera.location = original_location
    camera.rotation_euler = original_rotation
    camera.keyframe_insert(data_path="location", frame=35)
    camera.keyframe_insert(data_path="rotation_euler", frame=35)

    print("   ✅ Added subtle camera shake during explosion")
    return True


def create_animation_report():
    """Create a report on animation improvements"""
    print("\n🎬 ANIMATION REFINEMENT REPORT")
    print("=" * 40)

    # Count animated objects
    fire_count = len([obj for obj in bpy.data.objects if obj.name.startswith("Ultra_Fire_")])
    debris_count = len([obj for obj in bpy.data.objects if obj.name.startswith("Ultra_Debris_")])
    smoke_count = len([obj for obj in bpy.data.objects if obj.name.startswith("Ultra_Smoke_")])

    print(f"Fire Particles: {fire_count}")
    print(f"Debris Objects: {debris_count}")
    print(f"Smoke Objects: {smoke_count}")

    # Animation improvements summary
    improvements = [
        "✅ Added turbulence to fire particles",
        "✅ Enhanced debris physics with bouncing",
        "✅ Improved smoke dynamics and movement",
        "✅ Added timing variations for natural sequence",
        "✅ Optimized keyframe data for performance",
        "✅ Added subtle camera shake effect"
    ]

    print("\n🎯 Animation Improvements:")
    for improvement in improvements:
        print(f"   {improvement}")

    print("\n🎯 Expected Results:")
    print("   • More realistic particle movement")
    print("   • Better explosion timing and sequence")
    print("   • Enhanced visual drama with camera shake")
    print("   • Smoother animations with optimized keyframes")
    print("   • More natural smoke and debris behavior")

    return True


def save_refined_scene():
    """Save the animation-refined scene"""
    output_path = "${PROJECT_ROOT}/projects/explosion-test/blender_files/ultra_realistic_explosion_refined.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"💾 Saved refined scene: {output_path}")
    return output_path


def main():
    print("🎬 ANIMATION REFINEMENT FOR ULTRA-REALISTIC EXPLOSIONS")
    print("=" * 60)
    print("This script enhances particle animations with more realistic physics,")
    print("turbulence, timing variations, and camera effects.")
    print()

    # Check if we're in the right scene
    if not bpy.data.filepath or "ultra_realistic_explosion" not in bpy.data.filepath:
        print("⚠️  Warning: Not in ultra_realistic_explosion scene")
        print("   Please open the ultra-realistic explosion scene first")
        return

    print("🎯 Starting animation refinement process...")

    # Apply refinements
    turbulence_added = add_turbulence_to_particles()
    physics_improved = improve_debris_physics()
    smoke_enhanced = add_smoke_dynamics()
    timing_added = add_timing_variations()
    keyframes_optimized = optimize_keyframes()
    camera_shake_added = add_camera_shake()

    # Create report
    create_animation_report()

    # Save refined scene
    saved_path = save_refined_scene()

    print("\n" + "=" * 60)
    print("✅ ANIMATION REFINEMENT COMPLETE!")
    print("=" * 60)
    print("Refinements applied:")
    print(f"   • {turbulence_added} fire particles enhanced with turbulence")
    print(f"   • {physics_improved} debris objects improved with physics")
    print(f"   • {'✅' if smoke_enhanced else '❌'} smoke dynamics enhanced")
    print(f"   • {'✅' if timing_added else '❌'} timing variations added")
    print(f"   • {keyframes_optimized} objects had keyframes optimized")
    print(f"   • {'✅' if camera_shake_added else '❌'} camera shake added")
    print(f"   • Refined scene saved to: {saved_path}")
    print("\n🎯 Enhanced Realism Features:")
    print("   • Turbulent fire particle movement")
    print("   • Bouncing debris with realistic trajectories")
    print("   • Dynamic smoke swirling and scaling")
    print("   • Natural timing variations")
    print("   • Subtle camera shake for drama")
    print("   • Optimized keyframe performance")


if __name__ == "__main__":
    main()
