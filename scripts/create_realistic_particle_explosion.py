#!/usr/bin/env python3
"""
Create a realistic explosion using particle systems and volume rendering
This will be much more realistic than simple spheres
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


def create_explosion_particle_system(location, start_frame):
    """Create a realistic particle explosion"""
    print(f"   Creating particle explosion at {location}")

    # Create empty object as emitter
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    emitter = bpy.context.active_object
    emitter.name = "Explosion_Emitter"

    # Add particle system
    bpy.ops.object.particle_system_add()
    ps = emitter.particle_systems[0]
    ps.name = "Explosion_Particles"

    # Configure particle settings
    settings = ps.settings
    settings.type = 'HAIR'
    settings.render_type = 'HALO'
    settings.emit_from = 'VOLUME'
    settings.distribution = 'RAND'

    # Explosion timing
    settings.frame_start = start_frame
    settings.frame_end = start_frame + 5  # Short burst
    settings.lifetime = 30  # Particles live for 30 frames
    settings.lifetime_random = 0.5

    # Explosion behavior
    settings.count = 1000  # Number of particles
    settings.size = 0.05
    settings.size_random = 0.8
    settings.angular_velocity_factor = 3.0

    # Physics
    settings.physics_type = 'NEWTONIAN'
    settings.mass = 0.1
    settings.brownian_factor = 2.0

    # Force fields for explosion
    settings.effector_weights.gravity = 0.0  # No gravity
    settings.effector_weights.all = 1.0

    # Velocity
    settings.normal_factor = 8.0  # Explode outward
    settings.factor_random = 0.8
    settings.angular_velocity_factor = 3.0

    # Create realistic fire material
    create_fire_particle_material(emitter)

    return emitter


def create_fire_particle_material(emitter):
    """Create realistic fire material for particles"""
    mat = bpy.data.materials.new(name="Fire_Particle_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Add emission shader
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (200, 0)

    # Add color ramp for fire gradient
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 0)

    # Fire colors: red -> orange -> yellow -> white
    color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 0.8, 1.0)  # White

    # Add noise for fire variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.7

    # Connect nodes
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    # High emission strength for bright explosion
    emission.inputs['Strength'].default_value = 15.0

    # Assign material
    emitter.data.materials.append(mat)


def create_smoke_volume(location, start_frame):
    """Create a smoke volume for the explosion"""
    print(f"   Creating smoke volume at {location}")

    # Create cube for smoke volume
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=location)
    smoke_volume = bpy.context.active_object
    smoke_volume.name = "Explosion_Smoke"

    # Scale animation for expanding smoke
    smoke_volume.scale = (0.1, 0.1, 0.1)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame)

    smoke_volume.scale = (3.0, 3.0, 3.0)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame + 15)

    smoke_volume.scale = (5.0, 5.0, 5.0)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame + 30)

    # Fade out
    smoke_volume.hide_viewport = True
    smoke_volume.hide_render = True
    smoke_volume.keyframe_insert(data_path="hide_viewport", frame=start_frame + 50)
    smoke_volume.keyframe_insert(data_path="hide_render", frame=start_frame + 50)

    # Smoke material
    create_smoke_volume_material(smoke_volume)

    return smoke_volume


def create_smoke_volume_material(obj):
    """Create smoke material with volume shader"""
    mat = bpy.data.materials.new(name="Smoke_Volume_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Add volume shader
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (200, 0)

    # Configure for smoke
    volume.inputs['Density'].default_value = 0.2
    volume.inputs['Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray smoke
    volume.inputs['Emission Strength'].default_value = 0.5
    volume.inputs['Emission Color'].default_value = (0.8, 0.4, 0.1, 1.0)  # Orange glow

    # Add noise for smoke variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 3.0

    # Connect noise to density
    links.new(noise.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Assign material
    obj.data.materials.append(mat)


def create_realistic_explosion():
    """Create the complete realistic explosion scene"""
    print("\n" + "=" * 80)
    print("🔥 CREATING REALISTIC PARTICLE EXPLOSION")
    print("=" * 80 + "\n")

    # Clear and setup scene
    clear_scene()
    setup_scene()

    # Create explosion at center
    emitter = create_explosion_particle_system((0, 0, 1), 10)
    smoke = create_smoke_volume((0, 0, 1), 10)

    print("\n" + "=" * 80)
    print("🎬 REALISTIC EXPLOSION READY!")
    print("=" * 80)
    print("This explosion uses:")
    print("• 1000+ particles for realistic fire")
    print("• Volume rendering for smoke")
    print("• Realistic fire colors and materials")
    print("• Dynamic scaling and animation")
    print("\nThis will be MUCH more realistic than simple spheres! 🔥")


if __name__ == "__main__":
    print("🔥 REALISTIC PARTICLE EXPLOSION")
    print("This creates a particle-based explosion with volume rendering")
    print("Much more realistic than simple spheres!")
    print()

    create_realistic_explosion()

    print("\n" + "=" * 80)
    print("🎬 READY TO RENDER!")
    print("=" * 80)
    print("This explosion will render immediately with:")
    print("• Realistic particle effects")
    print("• Fire and smoke colors")
    print("• Dynamic expansion")
    print("• No simulation baking needed!")
    print("\nMuch better than simple spheres! 🔥")
