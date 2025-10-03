#!/usr/bin/env python3
"""
Create realistic explosions using particle systems (no baking required)
This is faster than Mantaflow but still looks much better than simple spheres
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


def create_explosion_particle_system(location, start_frame, name):
    """Create a particle system for realistic explosion"""
    print(f"   Creating particle explosion at {location}")

    # Create empty object as emitter
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    emitter = bpy.context.active_object
    emitter.name = f"Explosion_Emitter_{name}"

    # Add particle system
    bpy.ops.object.particle_system_add()
    if len(emitter.particle_systems) > 0:
        ps = emitter.particle_systems[0]
        ps.name = f"Explosion_Particles_{name}"
    else:
        print(f"   ⚠️  Failed to create particle system for {name}")
        return None

    # Configure particle settings
    settings = ps.settings
    settings.type = 'HAIR'
    settings.render_type = 'HALO'
    settings.emit_from = 'VOLUME'
    settings.distribution = 'RAND'

    # Explosion timing
    settings.frame_start = start_frame
    settings.frame_end = start_frame + 5  # Short burst
    settings.lifetime = 20  # Particles live for 20 frames
    settings.lifetime_random = 0.5

    # Explosion behavior
    settings.count = 500  # Number of particles
    settings.size = 0.1
    settings.size_random = 0.8
    settings.angular_velocity_factor = 2.0

    # Physics
    settings.physics_type = 'NEWTONIAN'
    settings.mass = 0.1
    settings.brownian_factor = 2.0

    # Force fields for explosion
    settings.effector_weights.gravity = 0.0  # No gravity
    settings.effector_weights.all = 1.0

    # Velocity
    settings.normal_factor = 5.0  # Explode outward
    settings.factor_random = 0.8
    settings.angular_velocity_factor = 3.0

    # Material for particles
    create_explosion_particle_material(emitter, name)

    return emitter


def create_explosion_particle_material(emitter, name):
    """Create material for explosion particles"""
    mat = bpy.data.materials.new(name=f"Explosion_Particle_Mat_{name}")
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

    # Add color ramp for fire colors
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 0)
    color_ramp.color_ramp.elements[0].color = (1.0, 0.1, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[1].color = (1.0, 0.8, 0.0, 1.0)  # Yellow

    # Add noise for variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 10.0

    # Connect nodes
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])

    # High emission strength for bright explosion
    emission.inputs['Strength'].default_value = 10.0

    # Assign material
    emitter.data.materials.append(mat)


def create_explosion_smoke_volume(location, start_frame, name):
    """Create a smoke volume for the explosion"""
    print(f"   Creating smoke volume at {location}")

    # Create cube for smoke volume
    bpy.ops.mesh.primitive_cube_add(size=3.0, location=location)
    smoke_volume = bpy.context.active_object
    smoke_volume.name = f"Explosion_Smoke_{name}"

    # Scale animation for expanding smoke
    smoke_volume.scale = (0.1, 0.1, 0.1)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame)

    smoke_volume.scale = (2.0, 2.0, 2.0)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame + 10)

    smoke_volume.scale = (3.0, 3.0, 3.0)
    smoke_volume.keyframe_insert(data_path="scale", frame=start_frame + 20)

    # Fade out
    smoke_volume.hide_viewport = True
    smoke_volume.hide_render = True
    smoke_volume.keyframe_insert(data_path="hide_viewport", frame=start_frame + 30)
    smoke_volume.keyframe_insert(data_path="hide_render", frame=start_frame + 30)

    # Smoke material
    create_smoke_material(smoke_volume, name)

    return smoke_volume


def create_smoke_material(obj, name):
    """Create smoke material with volume shader"""
    mat = bpy.data.materials.new(name=f"Smoke_Mat_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # Add volume shader
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (0, 0)

    # Configure for smoke
    volume.inputs['Density'].default_value = 0.3
    volume.inputs['Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray smoke
    volume.inputs['Emission Strength'].default_value = 0.5
    volume.inputs['Emission Color'].default_value = (0.8, 0.4, 0.1, 1.0)  # Orange glow

    # Add noise for smoke variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 3.0

    # Connect noise to density
    links.new(noise.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Assign material
    obj.data.materials.append(mat)


def create_realistic_particle_explosions():
    """Create realistic explosions using particle systems"""
    print("\n" + "=" * 80)
    print("🔥 CREATING REALISTIC PARTICLE EXPLOSIONS")
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

    for i, exp_data in enumerate(explosion_data):
        print(f"\nCreating explosion {i + 1}/8: {exp_data['name']}")

        # Create particle system
        emitter = create_explosion_particle_system(
            exp_data["location"],
            exp_data["start_frame"],
            exp_data["name"]
        )

        # Create smoke volume
        smoke = create_explosion_smoke_volume(
            exp_data["location"],
            exp_data["start_frame"],
            exp_data["name"]
        )

        print(f"   ✅ Explosion {i + 1} created with particles + smoke")

    print(f"\n✅ Created {len(explosion_data)} realistic explosions")
    print("\n🎬 These explosions will have:")
    print("   • 500+ particles per explosion")
    print("   • Fire colors (red to yellow)")
    print("   • Smoke volumes with realistic expansion")
    print("   • No baking required - renders immediately!")
    print("\nMuch more realistic than simple spheres! 🔥")


if __name__ == "__main__":
    print("🔥 REALISTIC PARTICLE EXPLOSIONS")
    print("This creates particle-based explosions (no baking required)")
    print("Much more realistic than simple spheres!")
    print()

    create_realistic_particle_explosions()

    print("\n" + "=" * 80)
    print("🎬 READY TO RENDER!")
    print("=" * 80)
    print("These explosions will render immediately with:")
    print("• Realistic particle effects")
    print("• Fire and smoke colors")
    print("• Dynamic expansion")
    print("• No simulation baking needed!")
    print("\nMuch better than simple yellow spheres! 🔥")
