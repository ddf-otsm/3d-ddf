#!/usr/bin/env python3
"""
Create a focused explosion test scene
This scene contains only explosion effects for validation
"""

import bpy
import bmesh
from mathutils import Vector
import random


def clear_scene():
    """Clear the default scene"""
    print("🗑️  Clearing default scene...")

    # Select all objects
    bpy.ops.object.select_all(action='SELECT')

    # Delete all objects
    bpy.ops.object.delete(use_global=False)

    print("   ✅ Scene cleared")


def setup_scene():
    """Setup basic scene for explosion testing"""
    print("\n🎬 Setting up test scene...")

    # Set frame range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 100

    # Set resolution
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # Set render engine to Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'

    # Add camera
    bpy.ops.object.camera_add(location=(5, -5, 3))
    camera = bpy.context.active_object
    camera.name = "Test_Camera"

    # Point camera at origin
    camera.rotation_euler = (1.1, 0, 0.785)

    # Add basic lighting
    bpy.ops.object.light_add(type='SUN', location=(2, 2, 5))
    sun = bpy.context.active_object
    sun.name = "Sun_Light"
    sun.data.energy = 3.0

    # Add ground plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
    ground = bpy.context.active_object
    ground.name = "Ground"

    # Simple ground material
    ground_mat = bpy.data.materials.new(name="Ground_Material")
    ground_mat.use_nodes = True
    nodes = ground_mat.node_tree.nodes
    links = ground_mat.node_tree.links

    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')

    bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    ground.data.materials.append(ground_mat)

    print("   ✅ Scene setup complete")


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


def create_test_explosions():
    """Create test explosions at different positions and times"""
    print("\n🔥 Creating test explosions...")

    # Test explosion data - spread across the scene
    explosion_data = [
        {"location": (0, 0, 1), "start_frame": 10, "name": "Center"},
        {"location": (3, 0, 1), "start_frame": 20, "name": "Right"},
        {"location": (-3, 0, 1), "start_frame": 30, "name": "Left"},
        {"location": (0, 3, 1), "start_frame": 40, "name": "Front"},
        {"location": (0, -3, 1), "start_frame": 50, "name": "Back"},
        {"location": (2, 2, 2), "start_frame": 60, "name": "High"},
        {"location": (-2, -2, 0.5), "start_frame": 70, "name": "Low"},
        {"location": (0, 0, 3), "start_frame": 80, "name": "Top"},
    ]

    all_objects = []

    for i, exp_data in enumerate(explosion_data):
        print(f"\nCreating test explosion {i + 1}/8: {exp_data['name']}")

        # Create explosion objects
        objects = create_explosion_objects(
            exp_data["location"],
            exp_data["start_frame"],
            exp_data["name"]
        )

        all_objects.extend(objects)
        print(f"   ✅ Test explosion {i + 1} created with {len(objects)} objects")

    print(f"\n✅ Created {len(all_objects)} explosion objects total")
    return all_objects


def create_explosion_test_scene():
    """Create the complete explosion test scene"""
    print("\n" + "=" * 80)
    print("🔥 CREATING EXPLOSION TEST SCENE")
    print("=" * 80 + "\n")

    # Clear and setup scene
    clear_scene()
    setup_scene()

    # Create test explosions
    objects = create_test_explosions()

    print("\n" + "=" * 80)
    print("🎬 EXPLOSION TEST SCENE READY!")
    print("=" * 80)
    print(f"Total explosion objects: {len(objects)}")
    print("Scene contains:")
    print("• 8 test explosions at different positions")
    print("• Each explosion has 3 layers (Fire Core + Fire Shell + Smoke)")
    print("• Explosions at frames: 10, 20, 30, 40, 50, 60, 70, 80")
    print("• 100 frame animation (4 seconds at 25fps)")
    print("• Ground plane and basic lighting")
    print("• Camera positioned for good viewing")
    print("\nReady for explosion validation! 🔥")


if __name__ == "__main__":
    print("🔥 EXPLOSION TEST SCENE CREATOR")
    print("This creates a focused scene for testing explosion effects")
    print()

    create_explosion_test_scene()

    print("\n" + "=" * 80)
    print("🎬 NEXT STEPS:")
    print("=" * 80)
    print("1. Save this scene as explosion test")
    print("2. Render a few frames to validate explosions")
    print("3. If approved, apply to main project")
    print("4. If not, iterate on explosion design")
    print("\nPerfect for focused explosion testing! 🔥")
