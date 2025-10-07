#!/usr/bin/env python3
"""
Create improved realistic explosions with better materials and physics
This addresses the "not realistic enough" issue with enhanced effects
"""

import bpy
import bmesh
import random
from mathutils import Vector
import math


def clear_existing_explosions():
    """Remove old explosion objects"""
    print("🗑️  Removing old explosion objects...")

    objects_to_remove = []
    for obj in bpy.data.objects:
        if (obj.name.startswith('Explosion_')
                or obj.name.startswith('Fire_')
                or obj.name.startswith('Debris_')
                or obj.name.startswith('Smoke_')):
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"   Removed {len(objects_to_remove)} old objects")


def create_enhanced_fire_material(name):
    """Create more realistic fire material with better color gradients"""
    mat = bpy.data.materials.new(name=f"Enhanced_Fire_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Emission
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (600, 0)
    emission.inputs['Strength'].default_value = 25.0  # Much brighter

    # Color ramp for fire colors
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (400, 0)

    # More realistic fire colors
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[0].position = 0.0

    # Add more color stops for realistic fire
    color_ramp.color_ramp.elements.new(0.2)
    color_ramp.color_ramp.elements[1].color = (1.0, 0.3, 0.0, 1.0)  # Orange-red
    color_ramp.color_ramp.elements[1].position = 0.2

    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[2].color = (1.0, 0.6, 0.0, 1.0)  # Orange
    color_ramp.color_ramp.elements[2].position = 0.5

    color_ramp.color_ramp.elements.new(0.8)
    color_ramp.color_ramp.elements[3].color = (1.0, 0.9, 0.3, 1.0)  # Yellow-orange
    color_ramp.color_ramp.elements[3].position = 0.8

    color_ramp.color_ramp.elements[4].color = (1.0, 1.0, 0.8, 1.0)  # White
    color_ramp.color_ramp.elements[4].position = 1.0

    # Multiple noise layers for more complex fire
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (200, 100)
    noise1.inputs['Scale'].default_value = 15.0
    noise1.inputs['Detail'].default_value = 6.0
    noise1.inputs['Roughness'].default_value = 0.8

    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (200, -100)
    noise2.inputs['Scale'].default_value = 8.0
    noise2.inputs['Detail'].default_value = 4.0
    noise2.inputs['Roughness'].default_value = 0.6

    # Mix the noise layers
    mix = nodes.new('ShaderNodeMix')
    mix.location = (400, 0)
    mix.data_type = 'FLOAT'
    mix.inputs['Fac'].default_value = 0.7

    # Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (0, 0)

    # Time for animation
    time = nodes.new('ShaderNodeValue')
    time.location = (0, -200)
    time.outputs[0].default_value = 0.0

    # Connect
    links.new(coord.outputs['Generated'], noise1.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise2.inputs['Vector'])
    links.new(noise1.outputs['Fac'], mix.inputs['A'])
    links.new(noise2.outputs['Fac'], mix.inputs['B'])
    links.new(mix.outputs['Result'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def create_enhanced_smoke_material(name):
    """Create more realistic smoke material"""
    mat = bpy.data.materials.new(name=f"Enhanced_Smoke_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Volume Principled
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (400, 0)
    volume.inputs['Density'].default_value = 0.4
    volume.inputs['Color'].default_value = (0.15, 0.15, 0.15, 1.0)  # Darker smoke
    volume.inputs['Emission Strength'].default_value = 1.5
    volume.inputs['Emission Color'].default_value = (0.8, 0.4, 0.2, 1.0)  # Orange glow

    # Multiple noise for complex smoke
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (200, 100)
    noise1.inputs['Scale'].default_value = 6.0
    noise1.inputs['Detail'].default_value = 4.0

    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (200, -100)
    noise2.inputs['Scale'].default_value = 12.0
    noise2.inputs['Detail'].default_value = 2.0

    # Mix noise
    mix = nodes.new('ShaderNodeMix')
    mix.location = (400, 0)
    mix.data_type = 'FLOAT'
    mix.inputs['Fac'].default_value = 0.6

    # Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (0, 0)

    # Connect
    links.new(coord.outputs['Generated'], noise1.inputs['Vector'])
    links.new(coord.outputs['Generated'], noise2.inputs['Vector'])
    links.new(noise1.outputs['Fac'], mix.inputs['A'])
    links.new(noise2.outputs['Fac'], mix.inputs['B'])
    links.new(mix.outputs['Result'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    return mat


def create_enhanced_debris_material(name):
    """Create more realistic debris material"""
    mat = bpy.data.materials.new(name=f"Enhanced_Debris_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.15, 0.1, 1.0)  # Dark brown
    bsdf.inputs['Roughness'].default_value = 0.9
    bsdf.inputs['Metallic'].default_value = 0.1

    # Emission for glowing effect
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (400, 200)
    emission.inputs['Color'].default_value = (0.8, 0.3, 0.1, 1.0)  # Orange glow
    emission.inputs['Strength'].default_value = 2.0

    # Mix emission and BSDF
    mix = nodes.new('ShaderNodeMix')
    mix.location = (500, 0)
    mix.data_type = 'SHADER'
    mix.inputs['Fac'].default_value = 0.3  # 30% emission, 70% surface

    # Connect
    links.new(bsdf.outputs['BSDF'], mix.inputs['A'])
    links.new(emission.outputs['Emission'], mix.inputs['B'])
    links.new(mix.outputs['Result'], output.inputs['Surface'])

    return mat


def create_enhanced_fire_particles(location, start_frame, count=20):
    """Create enhanced fire particles with better physics"""
    fire_objects = []

    for i in range(count):
        # More random distribution
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0.1, 1.2)
        height = random.uniform(0, 0.8)

        # Spherical distribution
        x = location[0] + radius * math.cos(angle) * random.uniform(0.5, 1.0)
        y = location[1] + radius * math.sin(angle) * random.uniform(0.5, 1.0)
        z = location[2] + height

        # Create fire particle
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x, y, z))
        fire_obj = bpy.context.active_object
        fire_obj.name = f"Enhanced_Fire_{i}"

        # Enhanced material
        fire_mat = create_enhanced_fire_material(f"Fire_{i}")
        fire_obj.data.materials.append(fire_mat)

        # More complex animation
        fire_obj.scale = (0.0, 0.0, 0.0)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame - 1)

        # Quick burst
        fire_obj.scale = (1.2, 1.2, 1.2)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame + 1)

        # Expand outward with physics-like motion
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        velocity = random.uniform(2.0, 4.0)

        # Parabolic motion
        for t in range(0, 20, 2):
            frame = start_frame + t
            time_factor = t / 20.0

            # Horizontal movement
            new_x = x + direction.x * velocity * time_factor
            new_y = y + direction.y * velocity * time_factor

            # Vertical movement with gravity
            gravity = -0.5 * time_factor * time_factor
            new_z = z + direction.z * velocity * time_factor + gravity

            fire_obj.location = (new_x, new_y, new_z)
            fire_obj.keyframe_insert(data_path="location", frame=frame)

            # Scale animation
            scale_factor = 1.0 - time_factor * 0.8
            fire_obj.scale = (scale_factor, scale_factor, scale_factor)
            fire_obj.keyframe_insert(data_path="scale", frame=frame)

        fire_objects.append(fire_obj)

    return fire_objects


def create_enhanced_debris_particles(location, start_frame, count=15):
    """Create enhanced debris with better physics"""
    debris_objects = []

    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0.2, 1.5)

        x = location[0] + radius * math.cos(angle)
        y = location[1] + radius * math.sin(angle)
        z = location[2] + random.uniform(0, 0.5)

        # Create debris with random shape
        if random.random() < 0.5:
            bpy.ops.mesh.primitive_cube_add(size=0.15, location=(x, y, z))
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x, y, z))

        debris_obj = bpy.context.active_object
        debris_obj.name = f"Enhanced_Debris_{i}"

        # Random rotation
        debris_obj.rotation_euler = (
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi),
            random.uniform(0, 2 * math.pi)
        )

        # Enhanced material
        debris_mat = create_enhanced_debris_material(f"Debris_{i}")
        debris_obj.data.materials.append(debris_mat)

        # Physics-like animation
        debris_obj.scale = (0.0, 0.0, 0.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame)

        # Appear
        debris_obj.scale = (1.0, 1.0, 1.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame + 3)

        # Trajectory with gravity
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        velocity = random.uniform(1.5, 3.0)

        for t in range(0, 40, 2):
            frame = start_frame + t
            time_factor = t / 40.0

            # Horizontal movement
            new_x = x + direction.x * velocity * time_factor
            new_y = y + direction.y * velocity * time_factor

            # Vertical with gravity
            gravity = -0.8 * time_factor * time_factor
            new_z = z + direction.z * velocity * time_factor + gravity

            debris_obj.location = (new_x, new_y, new_z)
            debris_obj.keyframe_insert(data_path="location", frame=frame)

            # Rotation
            debris_obj.rotation_euler = (
                debris_obj.rotation_euler[0] + 0.2,
                debris_obj.rotation_euler[1] + 0.2,
                debris_obj.rotation_euler[2] + 0.2
            )
            debris_obj.keyframe_insert(data_path="rotation_euler", frame=frame)

        debris_objects.append(debris_obj)

    return debris_objects


def create_enhanced_smoke_volume(location, start_frame):
    """Create enhanced smoke volume with better animation"""
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=location)
    smoke_obj = bpy.context.active_object
    smoke_obj.name = "Enhanced_Smoke_Volume"

    # Enhanced material
    smoke_mat = create_enhanced_smoke_material("Smoke")
    smoke_obj.data.materials.append(smoke_mat)

    # More realistic smoke animation
    smoke_obj.scale = (0.1, 0.1, 0.1)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Initial burst
    smoke_obj.scale = (1.0, 1.0, 1.0)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 5)

    # Expansion
    smoke_obj.scale = (2.5, 2.5, 2.5)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 20)

    # Rise and spread
    smoke_obj.location = (location[0], location[1], location[2] + 1.0)
    smoke_obj.scale = (4.0, 4.0, 3.0)
    smoke_obj.keyframe_insert(data_path="location", frame=start_frame + 40)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 40)

    # Final dissipation
    smoke_obj.location = (location[0], location[1], location[2] + 2.0)
    smoke_obj.scale = (6.0, 6.0, 4.0)
    smoke_obj.keyframe_insert(data_path="location", frame=start_frame + 80)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 80)

    return smoke_obj


def create_enhanced_explosion(location=(0, 0, 1.5), start_frame=10):
    """Create enhanced explosion with all improvements"""
    print(f"\n🔥 Creating enhanced explosion at {location}, frame {start_frame}")

    # Create all components
    fire_objs = create_enhanced_fire_particles(location, start_frame, count=25)
    print(f"   ✅ Created {len(fire_objs)} enhanced fire particles")

    debris_objs = create_enhanced_debris_particles(location, start_frame + 2, count=20)
    print(f"   ✅ Created {len(debris_objs)} enhanced debris particles")

    smoke_obj = create_enhanced_smoke_volume(location, start_frame + 5)
    print(f"   ✅ Created enhanced smoke volume")

    return fire_objs + debris_objs + [smoke_obj]


def setup_enhanced_rendering():
    """Setup enhanced rendering settings"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 256  # Higher quality
    scene.cycles.volume_bounces = 8  # Better volume rendering
    scene.cycles.volume_step_size = 0.05  # Higher quality volumes
    scene.cycles.use_denoising = True  # Reduce noise

    print("✅ Enhanced rendering settings applied")


def main():
    print("=" * 80)
    print("🔥 ENHANCED REALISTIC EXPLOSIONS")
    print("=" * 80)
    print("Improvements:")
    print("- Better fire materials with color gradients")
    print("- Enhanced smoke with multiple noise layers")
    print("- Physics-based particle motion")
    print("- Higher quality rendering settings")
    print()

    clear_existing_explosions()
    setup_enhanced_rendering()

    # Create enhanced explosion
    create_enhanced_explosion()

    # Save scene
    bpy.ops.wm.save_as_mainfile(
        filepath="${PROJECT_ROOT}/projects/explosion-test/blender_files/enhanced_realistic_explosion.blend")
    print("✅ Enhanced scene saved")

    print("\n" + "=" * 80)
    print("✅ ENHANCED EXPLOSIONS CREATED!")
    print("=" * 80)
    print("Improvements made:")
    print("1. Better fire materials with realistic color gradients")
    print("2. Enhanced smoke with multiple noise layers")
    print("3. Physics-based particle motion with gravity")
    print("4. Higher quality rendering settings")
    print("5. More realistic debris materials")
    print()
    print("Next: Render to see the improved explosions! 🔥")


if __name__ == "__main__":
    main()
