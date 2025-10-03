#!/usr/bin/env python3
"""
Quick test of hybrid explosion approach
Renders 5 key frames to validate concept before full implementation
"""

import bpy
import random
from mathutils import Vector


def clear_scene():
    """Clear the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def setup_scene():
    """Setup basic scene"""
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 60
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 128  # Lower for quick test

    # Add camera
    bpy.ops.object.camera_add(location=(6, -6, 4))
    camera = bpy.context.active_object
    camera.name = "Test_Camera"
    camera.rotation_euler = (1.1, 0, 0.785)
    scene.camera = camera

    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0

    # Add ground
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"

    # Ground material
    ground_mat = bpy.data.materials.new(name="Ground_Mat")
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


def create_fire_material(name):
    """Create fire material"""
    mat = bpy.data.materials.new(name=f"Fire_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Emission
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (400, 0)
    emission.inputs['Strength'].default_value = 12.0

    # Color ramp
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (200, 0)
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 0.8, 1.0)  # White

    # Noise
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 4.0

    # Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (-200, 0)

    # Connect
    links.new(coord.outputs['Generated'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def create_debris_material(name):
    """Create debris material"""
    mat = bpy.data.materials.new(name=f"Debris_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Emission
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (200, 0)
    emission.inputs['Color'].default_value = (0.3, 0.2, 0.1, 1.0)  # Dark
    emission.inputs['Strength'].default_value = 4.0

    # Connect
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    return mat


def create_smoke_material(name):
    """Create smoke volume material"""
    mat = bpy.data.materials.new(name=f"Smoke_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Volume Principled
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (200, 0)
    volume.inputs['Density'].default_value = 0.3
    volume.inputs['Color'].default_value = (0.25, 0.25, 0.25, 1.0)
    volume.inputs['Emission Strength'].default_value = 0.8
    volume.inputs['Emission Color'].default_value = (0.9, 0.5, 0.2, 1.0)

    # Noise
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 3.0

    # Connect
    links.new(noise.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    return mat


def create_fire_particles(location, start_frame):
    """Create fire particle system"""
    # Create multiple small spheres as fire particles
    fire_objects = []

    for i in range(10):  # Simplified: 10 fire elements instead of 600 particles
        angle = random.uniform(0, 6.28)
        radius = random.uniform(0.2, 0.8)
        height = random.uniform(0, 0.5)

        x = location[0] + radius * random.uniform(-1, 1)
        y = location[1] + radius * random.uniform(-1, 1)
        z = location[2] + height

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(x, y, z))
        fire_obj = bpy.context.active_object
        fire_obj.name = f"Fire_Particle_{i}"

        # Material
        fire_mat = create_fire_material(f"Fire_{i}")
        fire_obj.data.materials.append(fire_mat)

        # Animation
        fire_obj.scale = (0.0, 0.0, 0.0)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame - 1)

        # Appear
        fire_obj.scale = (1.0, 1.0, 1.0)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame + 2)

        # Expand and move outward
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        new_loc = (x + direction.x * 1.5, y + direction.y * 1.5, z + direction.z * 1.0)
        fire_obj.location = new_loc
        fire_obj.scale = (1.5, 1.5, 1.5)
        fire_obj.keyframe_insert(data_path="location", frame=start_frame + 10)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame + 10)

        # Fade
        fire_obj.scale = (0.1, 0.1, 0.1)
        fire_obj.keyframe_insert(data_path="scale", frame=start_frame + 20)

        fire_objects.append(fire_obj)

    return fire_objects


def create_debris_particles(location, start_frame):
    """Create debris particle system"""
    debris_objects = []

    for i in range(5):  # Simplified: 5 debris elements
        angle = random.uniform(0, 6.28)
        radius = random.uniform(0.3, 1.0)

        x = location[0] + radius * random.uniform(-1, 1)
        y = location[1] + radius * random.uniform(-1, 1)
        z = location[2] + random.uniform(0, 0.3)

        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x, y, z))
        debris_obj = bpy.context.active_object
        debris_obj.name = f"Debris_Particle_{i}"

        # Material
        debris_mat = create_debris_material(f"Debris_{i}")
        debris_obj.data.materials.append(debris_mat)

        # Animation
        debris_obj.scale = (0.0, 0.0, 0.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame)

        # Appear
        debris_obj.scale = (1.0, 1.0, 1.0)
        debris_obj.keyframe_insert(data_path="scale", frame=start_frame + 5)

        # Move and fall
        direction = Vector(
            (x - location[0],
             y - location[1],
             z - location[2])).normalized()
        new_loc = (x + direction.x * 2.0, y + direction.y * 2.0, z + 0.5 - 0.5)  # Arc
        debris_obj.location = new_loc
        debris_obj.keyframe_insert(data_path="location", frame=start_frame + 30)

        debris_objects.append(debris_obj)

    return debris_objects


def create_smoke_volume(location, start_frame):
    """Create smoke volume"""
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    smoke_obj = bpy.context.active_object
    smoke_obj.name = "Smoke_Volume"

    # Material
    smoke_mat = create_smoke_material("Smoke")
    smoke_obj.data.materials.append(smoke_mat)

    # Animation
    smoke_obj.scale = (0.1, 0.1, 0.1)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame)

    smoke_obj.scale = (1.5, 1.5, 1.5)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 15)

    smoke_obj.scale = (3.5, 3.5, 3.5)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 40)

    smoke_obj.scale = (4.5, 4.5, 4.5)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 60)

    return smoke_obj


def create_hybrid_explosion(location=(0, 0, 1.5), start_frame=10):
    """Create complete hybrid explosion"""
    print(f"\n🔥 Creating hybrid explosion at {location}, frame {start_frame}")

    fire_objs = create_fire_particles(location, start_frame)
    print(f"   ✅ Created {len(fire_objs)} fire elements")

    debris_objs = create_debris_particles(location, start_frame + 3)
    print(f"   ✅ Created {len(debris_objs)} debris elements")

    smoke_obj = create_smoke_volume(location, start_frame + 8)
    print(f"   ✅ Created smoke volume")

    return fire_objs + debris_objs + [smoke_obj]


def render_test_frames():
    """Render 5 key frames"""
    scene = bpy.context.scene

    # Test frames: initial, burst, expansion, smoke, dissipation
    test_frames = [1, 15, 25, 40, 60]

    print("\n🎬 Rendering test frames...")
    for frame in test_frames:
        scene.frame_set(frame)
        scene.render.filepath = f"/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/renders/hybrid_quick_test_frame_{
            frame:03d}"
        bpy.ops.render.render(write_still=True)
        print(f"   ✅ Rendered frame {frame}")


def main():
    print("=" * 80)
    print("🔥 HYBRID EXPLOSION QUICK TEST")
    print("=" * 80)
    print("Testing: Particles + Volume approach")
    print("Frames: 5 key frames (1, 15, 25, 40, 60)")
    print("Quality: Lower samples for speed (128)")
    print()

    clear_scene()
    print("✅ Scene cleared")

    setup_scene()
    print("✅ Scene setup complete")

    create_hybrid_explosion()
    print("✅ Hybrid explosion created")

    # Save scene
    bpy.ops.wm.save_as_mainfile(
        filepath="/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/blender_files/hybrid_quick_test.blend")
    print("✅ Scene saved: hybrid_quick_test.blend")

    render_test_frames()

    print("\n" + "=" * 80)
    print("✅ HYBRID EXPLOSION QUICK TEST COMPLETE!")
    print("=" * 80)
    print("Check renders in: projects/explosion-test/renders/")
    print("Files: hybrid_quick_test_frame_*.png")
    print()
    print("Next steps:")
    print("1. Review the 5 rendered frames")
    print("2. Assess visual quality")
    print("3. Decide on render complexity level")
    print("4. Proceed with full implementation if approved")


if __name__ == "__main__":
    main()
