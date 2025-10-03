#!/usr/bin/env python3
"""
Create improved explosions using multiple mesh objects with realistic materials
This is much better than simple spheres but doesn't require complex simulation
"""

import bpy
import bmesh
from mathutils import Vector
import random


def clear_existing_explosions():
    """Remove the old simple explosion spheres"""
    print("🗑️  Removing old simple explosion spheres...")

    objects_to_remove = []
    for obj in bpy.data.objects:
        if obj.name.startswith('Explosion_'):
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"   Removed {len(objects_to_remove)} old explosion objects")


def create_fire_material(name):
    """Create a realistic fire material"""
    mat = bpy.data.materials.new(name=f"Fire_Mat_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Add emission shader
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (400, 0)

    # Add color ramp for fire gradient
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 0)

    # Fire colors: red -> orange -> yellow -> white
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 0.8, 1.0)  # White

    # Add noise for fire variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.7

    # Add mapping for animation
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 0)
    mapping.inputs['Location'].default_value = (0, 0, 0)

    # Add coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (-400, 0)

    # Connect nodes
    links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    # High emission strength
    emission.inputs['Strength'].default_value = 8.0

    return mat


def create_smoke_material(name):
    """Create a smoke material"""
    mat = bpy.data.materials.new(name=f"Smoke_Mat_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Add emission for glow
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (200, 0)

    # Smoke color
    emission.inputs['Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
    emission.inputs['Strength'].default_value = 2.0

    # Add noise for smoke variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 3.0

    # Connect
    links.new(noise.outputs['Fac'], emission.inputs['Strength'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def create_explosion_objects(location, start_frame, name):
    """Create multiple objects for a realistic explosion"""
    print(f"   Creating explosion objects at {location}")

    objects = []

    # Create fire core (small, bright)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=location)
    fire_core = bpy.context.active_object
    fire_core.name = f"Explosion_Fire_{name}"
    objects.append(fire_core)

    # Create fire shell (medium, expanding)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=location)
    fire_shell = bpy.context.active_object
    fire_shell.name = f"Explosion_Shell_{name}"
    objects.append(fire_shell)

    # Create smoke cloud (large, expanding)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=location)
    smoke_cloud = bpy.context.active_object
    smoke_cloud.name = f"Explosion_Smoke_{name}"
    objects.append(smoke_cloud)

    # Create materials
    fire_mat = create_fire_material(name)
    smoke_mat = create_smoke_material(name)

    # Assign materials
    fire_core.data.materials.append(fire_mat)
    fire_shell.data.materials.append(fire_mat)
    smoke_cloud.data.materials.append(smoke_mat)

    # Animate explosion
    animate_explosion_objects(objects, start_frame)

    return objects


def animate_explosion_objects(objects, start_frame):
    """Animate the explosion objects"""
    fire_core, fire_shell, smoke_cloud = objects

    # Start hidden
    for obj in objects:
        obj.scale = (0.0, 0.0, 0.0)
        obj.keyframe_insert(data_path="scale", frame=start_frame - 1)

    # Explosion sequence
    # Frame 0: Fire core appears
    fire_core.scale = (1.0, 1.0, 1.0)
    fire_core.keyframe_insert(data_path="scale", frame=start_frame)

    # Frame 2: Fire shell appears
    fire_shell.scale = (1.0, 1.0, 1.0)
    fire_shell.keyframe_insert(data_path="scale", frame=start_frame + 2)

    # Frame 4: Smoke cloud appears
    smoke_cloud.scale = (1.0, 1.0, 1.0)
    smoke_cloud.keyframe_insert(data_path="scale", frame=start_frame + 4)

    # Expansion phase
    # Frame 8: All objects expand
    fire_core.scale = (2.0, 2.0, 2.0)
    fire_core.keyframe_insert(data_path="scale", frame=start_frame + 8)

    fire_shell.scale = (3.0, 3.0, 3.0)
    fire_shell.keyframe_insert(data_path="scale", frame=start_frame + 8)

    smoke_cloud.scale = (4.0, 4.0, 4.0)
    smoke_cloud.keyframe_insert(data_path="scale", frame=start_frame + 8)

    # Fade out phase
    # Frame 15: Fire core fades
    fire_core.scale = (0.5, 0.5, 0.5)
    fire_core.keyframe_insert(data_path="scale", frame=start_frame + 15)

    # Frame 20: Fire shell fades
    fire_shell.scale = (0.3, 0.3, 0.3)
    fire_shell.keyframe_insert(data_path="scale", frame=start_frame + 20)

    # Frame 25: All disappear
    for obj in objects:
        obj.scale = (0.0, 0.0, 0.0)
        obj.keyframe_insert(data_path="scale", frame=start_frame + 25)

    # Add some rotation for dynamic effect
    for obj in objects:
        obj.rotation_euler = (0, 0, 0)
        obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)

        obj.rotation_euler = (
            random.uniform(
                0, 6.28), random.uniform(
                0, 6.28), random.uniform(
                0, 6.28))
        obj.keyframe_insert(data_path="rotation_euler", frame=start_frame + 25)


def create_improved_explosions():
    """Create improved explosions with multiple objects"""
    print("\n" + "=" * 80)
    print("🔥 CREATING IMPROVED EXPLOSIONS")
    print("=" * 80 + "\n")

    # Clear old explosions
    clear_existing_explosions()

    # Explosion data
    explosion_data = [
        {"location": (4.14, 2.42, 4.70), "start_frame": 140, "name": "0"},
        {"location": (5.13, -3.71, 3.09), "start_frame": 97, "name": "1"},
        {"location": (0.60, -6.07, 3.62), "start_frame": 125, "name": "2"},
        {"location": (0.73, 4.27, 1.30), "start_frame": 91, "name": "3"},
        {"location": (-1.54, 5.11, 4.25), "start_frame": 89, "name": "4"},
        {"location": (3.95, 5.50, 3.69), "start_frame": 138, "name": "5"},
        {"location": (-2.93, -4.02, 2.20), "start_frame": 56, "name": "6"},
        {"location": (2.50, -3.20, 4.84), "start_frame": 183, "name": "7"},
    ]

    all_objects = []

    for i, exp_data in enumerate(explosion_data):
        print(f"\nCreating explosion {i + 1}/8: {exp_data['name']}")

        # Create explosion objects
        objects = create_explosion_objects(
            exp_data["location"],
            exp_data["start_frame"],
            exp_data["name"]
        )

        all_objects.extend(objects)
        print(f"   ✅ Explosion {i + 1} created with {len(objects)} objects")

    print(f"\n✅ Created {len(all_objects)} explosion objects total")
    print("\n🎬 These explosions will have:")
    print("   • Fire core (bright, small)")
    print("   • Fire shell (expanding)")
    print("   • Smoke cloud (large, dissipating)")
    print("   • Realistic fire colors (red -> orange -> yellow)")
    print("   • Dynamic scaling and rotation")
    print("   • No simulation baking required!")
    print("\nMuch more realistic than simple yellow spheres! 🔥")


if __name__ == "__main__":
    print("🔥 IMPROVED EXPLOSIONS")
    print("This creates multi-layered explosions with realistic materials")
    print("Much better than simple spheres!")
    print()

    create_improved_explosions()

    print("\n" + "=" * 80)
    print("🎬 READY TO RENDER!")
    print("=" * 80)
    print("These explosions will render immediately with:")
    print("• Multi-layered fire and smoke")
    print("• Realistic fire colors and gradients")
    print("• Dynamic scaling and rotation")
    print("• No simulation baking needed!")
    print("\nMuch better than simple yellow spheres! 🔥")
