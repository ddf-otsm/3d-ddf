#!/usr/bin/env python3
"""
Fix explosion realism issues
This script addresses the most common problems that make explosions look fake
"""

import bpy
import bmesh
import random
from mathutils import Vector
import math


def clear_all_explosions():
    """Remove all existing explosion objects"""
    print("🗑️  Clearing all explosion objects...")

    objects_to_remove = []
    for obj in bpy.data.objects:
        if (obj.name.startswith('Explosion_')
                or obj.name.startswith('Fire_')
                or obj.name.startswith('Debris_')
                or obj.name.startswith('Smoke_')
                or obj.name.startswith('Enhanced_')):
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"   Removed {len(objects_to_remove)} objects")


def create_ultra_realistic_fire_material(name):
    """Create ultra-realistic fire material"""
    mat = bpy.data.materials.new(name=f"Ultra_Fire_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1000, 0)

    # Emission
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (800, 0)
    emission.inputs['Strength'].default_value = 50.0  # Very bright

    # Color ramp with realistic fire colors
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (600, 0)

    # Realistic fire color gradient
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[0].position = 0.0

    color_ramp.color_ramp.elements.new(0.15)
    color_ramp.color_ramp.elements[1].color = (1.0, 0.2, 0.0, 1.0)  # Red-orange
    color_ramp.color_ramp.elements[1].position = 0.15

    color_ramp.color_ramp.elements.new(0.35)
    color_ramp.color_ramp.elements[2].color = (1.0, 0.4, 0.0, 1.0)  # Orange
    color_ramp.color_ramp.elements[2].position = 0.35

    color_ramp.color_ramp.elements.new(0.55)
    color_ramp.color_ramp.elements[3].color = (1.0, 0.6, 0.0, 1.0)  # Orange-yellow
    color_ramp.color_ramp.elements[3].position = 0.55

    color_ramp.color_ramp.elements.new(0.75)
    color_ramp.color_ramp.elements[4].color = (1.0, 0.8, 0.2, 1.0)  # Yellow-orange
    color_ramp.color_ramp.elements[4].position = 0.75

    color_ramp.color_ramp.elements[5].color = (1.0, 1.0, 0.9, 1.0)  # White
    color_ramp.color_ramp.elements[5].position = 1.0

    # Multiple noise layers for complex fire
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (200, 200)
    noise1.inputs['Scale'].default_value = 20.0
    noise1.inputs['Detail'].default_value = 8.0
    noise1.inputs['Roughness'].default_value = 0.9

    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (200, 0)
    noise2.inputs['Scale'].default_value = 8.0
    noise2.inputs['Detail'].default_value = 6.0
    noise2.inputs['Roughness'].default_value = 0.7

    noise3 = nodes.new('ShaderNodeTexNoise')
    noise3.location = (200, -200)
    noise3.inputs['Scale'].default_value = 4.0
    noise3.inputs['Detail'].default_value = 4.0
    noise3.inputs['Roughness'].default_value = 0.5

    # Mix noise layers
    mix1 = nodes.new('ShaderNodeMix')
    mix1.location = (400, 100)
    mix1.data_type = 'FLOAT'
    mix1.inputs['Factor'].default_value = 0.6

    mix2 = nodes.new('ShaderNodeMix')
    mix2.location = (600, 0)
    mix2.data_type = 'FLOAT'
    mix2.inputs['Factor'].default_value = 0.4

    # Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (0, 0)

    # Time for animation
    time = nodes.new('ShaderNodeValue')
    time.location = (0, -300)
    time.outputs[0].default_value = 0.0

    # Connect
    links.new(coord.outputs['Generated'], noise1.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise2.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise3.inputs['Vector'])

    links.new(noise1.outputs['Fac'], mix1.inputs['A'])
    links.new(noise2.outputs['Fac'], mix1.inputs['B'])
    links.new(mix1.outputs['Result'], mix2.inputs['A'])
    links.new(noise3.outputs['Fac'], mix2.inputs['B'])

    links.new(mix2.outputs['Result'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def create_ultra_realistic_smoke_material(name):
    """Create ultra-realistic smoke material"""
    mat = bpy.data.materials.new(name=f"Ultra_Smoke_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Volume Principled
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (600, 0)
    volume.inputs['Density'].default_value = 0.6
    volume.inputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark
    volume.inputs['Emission Strength'].default_value = 2.0
    volume.inputs['Emission Color'].default_value = (0.6, 0.3, 0.1, 1.0)  # Orange glow

    # Multiple noise for complex smoke
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (200, 200)
    noise1.inputs['Scale'].default_value = 8.0
    noise1.inputs['Detail'].default_value = 6.0

    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (200, 0)
    noise2.inputs['Scale'].default_value = 4.0
    noise2.inputs['Detail'].default_value = 4.0

    noise3 = nodes.new('ShaderNodeTexNoise')
    noise3.location = (200, -200)
    noise3.inputs['Scale'].default_value = 2.0
    noise3.inputs['Detail'].default_value = 2.0

    # Mix noise
    mix1 = nodes.new('ShaderNodeMix')
    mix1.location = (400, 100)
    mix1.data_type = 'FLOAT'
    mix1.inputs['Factor'].default_value = 0.5

    mix2 = nodes.new('ShaderNodeMix')
    mix2.location = (600, 0)
    mix2.data_type = 'FLOAT'
    mix2.inputs['Factor'].default_value = 0.3

    # Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (0, 0)

    # Connect
    links.new(coord.outputs['Generated'], noise1.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise2.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise3.inputs['Vector'])

    links.new(noise1.outputs['Fac'], mix1.inputs['A'])
    links.new(noise2.outputs['Fac'], mix1.inputs['B'])
    links.new(mix1.outputs['Result'], mix2.inputs['A'])
    links.new(noise3.outputs['Fac'], mix2.inputs['B'])

    links.new(mix2.outputs['Result'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    return mat


def create_ultra_realistic_debris_material(name):
    """Create ultra-realistic debris material"""
    mat = bpy.data.materials.new(name=f"Ultra_Debris_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    bsdf.inputs['Base Color'].default_value = (0.15, 0.1, 0.05, 1.0)  # Dark brown
    bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Metallic'].default_value = 0.05

    # Emission for glowing effect
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (600, 200)
    emission.inputs['Color'].default_value = (0.8, 0.3, 0.1, 1.0)  # Orange glow
    emission.inputs['Strength'].default_value = 3.0

    # Mix emission and BSDF
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (700, 0)
    mix.inputs['Fac'].default_value = 0.4  # 40% emission, 60% surface

    # Connect
    links.new(bsdf.outputs['BSDF'], mix.inputs['Shader'])
    links.new(emission.outputs['Emission'], mix.inputs['Shader_001'])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    return mat


def create_ultra_realistic_fire_particles(location, start_frame, count=50):
    """Create ultra-realistic fire particles"""
    fire_objects = []

    for i in range(count):
        # More complex distribution
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0.05, 1.5)
        height = random.uniform(0, 1.0)

        # Spherical distribution with more variation
        x = location[0] + radius * math.cos(angle) * random.uniform(0.3, 1.2)
        y = location[1] + radius * math.sin(angle) * random.uniform(0.3, 1.2)
        z = location[2] + height

        # Create fire particle
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(x, y, z))
        fire_obj = bpy.context.active_object
        fire_obj.name = f"Ultra_Fire_{i}"

        # Ultra-realistic material
        fire_mat = create_ultra_realistic_fire_material(f"Fire_{i}")
        fire_obj.data.materials.append(fire_mat)

        # Complex animation
        fire_obj.scale = (0.0, 0.0, 0.0)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame - 1)

        # Quick burst
        fire_obj.scale = (1.5, 1.5, 1.5)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame + 1)

        # Expand outward with realistic physics
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        velocity = random.uniform(2.5, 5.0)

        # Parabolic motion with more frames
        for t in range(0, 30, 1):
            frame = start_frame + t
            time_factor = t / 30.0

            # Horizontal movement
            new_x = x + direction.x * velocity * time_factor
            new_y = y + direction.y * velocity * time_factor

            # Vertical movement with gravity
            gravity = -0.6 * time_factor * time_factor
            new_z = z + direction.z * velocity * time_factor + gravity

            fire_obj.location = (new_x, new_y, new_z)
            fire_obj.keyframe_insert(data_path="location", frame=frame)

            # Scale animation with more variation
            scale_factor = (1.0 - time_factor * 0.9) * random.uniform(0.8, 1.2)
            fire_obj.scale = (scale_factor, scale_factor, scale_factor)
            fire_obj.keyframe_insert(data_path="scale", frame=frame)

        fire_objects.append(fire_obj)

    return fire_objects


def create_ultra_realistic_debris_particles(location, start_frame, count=30):
    """Create ultra-realistic debris particles"""
    debris_objects = []

    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0.1, 2.0)

        x = location[0] + radius * math.cos(angle)
        y = location[1] + radius * math.sin(angle)
        z = location[2] + random.uniform(0, 0.8)

        # Create debris with random shape and size
        if random.random() < 0.4:
            bpy.ops.mesh.primitive_cube_add(
                size=random.uniform(
                    0.1, 0.3), location=(
                    x, y, z))
        elif random.random() < 0.7:
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=random.uniform(
                    0.05, 0.2), location=(
                    x, y, z))
        else:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=random.uniform(
                    0.05, 0.15), depth=random.uniform(
                    0.1, 0.3), location=(
                    x, y, z))

        debris_obj = bpy.context.active_object
        debris_obj.name = f"Ultra_Debris_{i}"

        # Random rotation
        debris_obj.rotation_euler = (
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi)
        )

        # Ultra-realistic material
        debris_mat = create_ultra_realistic_debris_material(f"Debris_{i}")
        debris_obj.data.materials.append(debris_mat)

        # Physics-like animation
        debris_obj.scale = (0.0, 0.0, 0.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame)

        # Appear
        debris_obj.scale = (1.0, 1.0, 1.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame + 2)

        # Trajectory with gravity
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        velocity = random.uniform(2.0, 4.0)

        for t in range(0, 60, 2):
            frame = start_frame + t
            time_factor = t / 60.0

            # Horizontal movement
            new_x = x + direction.x * velocity * time_factor
            new_y = y + direction.y * velocity * time_factor

            # Vertical with gravity
            gravity = -1.0 * time_factor * time_factor
            new_z = z + direction.z * velocity * time_factor + gravity

            debris_obj.location = (new_x, new_y, new_z)
            debris_obj.keyframe_insert(data_path="location", frame=frame)

            # Rotation
            debris_obj.rotation_euler = (
                debris_obj.rotation_euler[0] + 0.3,
                debris_obj.rotation_euler[1] + 0.3,
                debris_obj.rotation_euler[2] + 0.3
            )
            debris_obj.keyframe_insert(data_path="rotation_euler", frame=frame)

        debris_objects.append(debris_obj)

    return debris_objects


def create_ultra_realistic_smoke_volume(location, start_frame):
    """Create ultra-realistic smoke volume"""
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    smoke_obj = bpy.context.active_object
    smoke_obj.name = "Ultra_Smoke_Volume"

    # Ultra-realistic material
    smoke_mat = create_ultra_realistic_smoke_material("Smoke")
    smoke_obj.data.materials.append(smoke_mat)

    # Realistic smoke animation
    smoke_obj.scale = (0.1, 0.1, 0.1)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Initial burst
    smoke_obj.scale = (1.2, 1.2, 1.2)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 3)

    # Expansion
    smoke_obj.scale = (3.0, 3.0, 3.0)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 15)

    # Rise and spread
    smoke_obj.location = (location[0], location[1], location[2] + 1.5)
    smoke_obj.scale = (5.0, 5.0, 4.0)
    smoke_obj.keyframe_insert(data_path="location", frame=start_frame + 30)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 30)

    # Final dissipation
    smoke_obj.location = (location[0], location[1], location[2] + 3.0)
    smoke_obj.scale = (8.0, 8.0, 6.0)
    smoke_obj.keyframe_insert(data_path="location", frame=start_frame + 100)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 100)

    return smoke_obj


def setup_ultra_realistic_lighting():
    """Setup ultra-realistic lighting for explosions"""
    print("💡 Setting up ultra-realistic lighting...")

    # Main light
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 15))
    sun = bpy.context.active_object
    sun.name = "Main_Sun"
    sun.data.energy = 5.0
    sun.data.color = (1.0, 0.95, 0.8)  # Warm white

    # Fire glow light
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 2))
    fire_light = bpy.context.active_object
    fire_light.name = "Fire_Glow"
    fire_light.data.energy = 100.0
    fire_light.data.color = (1.0, 0.4, 0.1)  # Orange
    fire_light.data.cutoff_distance = 10.0

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 8))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 20.0
    rim_light.data.color = (0.8, 0.9, 1.0)  # Cool white
    rim_light.data.size = 2.0

    print("   ✅ Added main sun, fire glow, and rim lighting")


def setup_ultra_realistic_rendering():
    """Setup ultra-realistic rendering settings"""
    print("🎬 Setting up ultra-realistic rendering...")

    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 512  # High quality
    scene.cycles.volume_bounces = 12  # High quality volumes
    scene.cycles.volume_step_size = 0.02  # High quality volumes
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPTIX'  # Best denoiser

    # Enable all features
    scene.cycles.feature_set = 'EXPERIMENTAL'

    print("   ✅ Ultra-realistic rendering settings applied")


def create_ultra_realistic_explosion(location=(0, 0, 1.5), start_frame=10):
    """Create ultra-realistic explosion with all improvements"""
    print(f"\n🔥 Creating ultra-realistic explosion at {location}, frame {start_frame}")

    # Create all components
    fire_objs = create_ultra_realistic_fire_particles(location, start_frame, count=60)
    print(f"   ✅ Created {len(fire_objs)} ultra-realistic fire particles")

    debris_objs = create_ultra_realistic_debris_particles(
        location, start_frame + 2, count=40)
    print(f"   ✅ Created {len(debris_objs)} ultra-realistic debris particles")

    smoke_obj = create_ultra_realistic_smoke_volume(location, start_frame + 5)
    print(f"   ✅ Created ultra-realistic smoke volume")

    return fire_objs + debris_objs + [smoke_obj]


def main():
    print("=" * 80)
    print("🔥 ULTRA-REALISTIC EXPLOSION FIXER")
    print("=" * 80)
    print("This script fixes common realism issues:")
    print("- Better fire materials with realistic color gradients")
    print("- Enhanced smoke with multiple noise layers")
    print("- Physics-based particle motion")
    print("- Ultra-realistic lighting setup")
    print("- High-quality rendering settings")
    print()

    clear_all_explosions()
    setup_ultra_realistic_lighting()
    setup_ultra_realistic_rendering()

    # Create ultra-realistic explosion
    create_ultra_realistic_explosion()

    # Save scene
    bpy.ops.wm.save_as_mainfile(
        filepath="${PROJECT_ROOT}/projects/explosion-test/blender_files/ultra_realistic_explosion.blend")
    print("✅ Ultra-realistic scene saved")

    print("\n" + "=" * 80)
    print("✅ ULTRA-REALISTIC EXPLOSIONS CREATED!")
    print("=" * 80)
    print("Improvements made:")
    print("1. Ultra-realistic fire materials with complex color gradients")
    print("2. Enhanced smoke with multiple noise layers")
    print("3. Physics-based particle motion with gravity")
    print("4. Ultra-realistic lighting (main + fire glow + rim)")
    print("5. High-quality rendering settings (512 samples, 12 volume bounces)")
    print("6. More particles (60 fire + 40 debris)")
    print("7. Complex animation with realistic physics")
    print()
    print("This should look much more realistic! 🔥")


if __name__ == "__main__":
    main()
