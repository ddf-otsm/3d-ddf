#!/usr/bin/env python3
"""
Create realistic explosions using Mantaflow smoke simulation
This will replace the simple keyframe spheres with physics-based smoke/fire
"""

import bpy
import bmesh
from mathutils import Vector


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


def create_explosion_domain(location, size=4.0):
    """Create a Mantaflow domain for smoke simulation"""
    print(f"   Creating explosion domain at {location}")

    # Create cube for domain
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    domain = bpy.context.active_object
    domain.name = f"Explosion_Domain_{len([o for o in bpy.data.objects if o.name.startswith('Explosion_Domain')])}"

    # Set up as Mantaflow domain
    domain.modifiers.new(name="Fluid", type='FLUID_SIMULATION')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'

    # Configure domain settings
    fluid = domain.modifiers["Fluid"]
    fluid.domain_settings.domain_type = 'GAS'
    fluid.domain_settings.collision_extents = 'FULL'
    fluid.domain_settings.use_adaptive_domain = True
    fluid.domain_settings.use_high_resolution = True
    fluid.domain_settings.resolution_max = 64  # Start with lower res for speed

    # Smoke settings
    fluid.domain_settings.use_dissolve = True
    fluid.domain_settings.dissolve_speed = 1.0
    fluid.domain_settings.use_density = True
    fluid.domain_settings.use_reacting = True
    fluid.domain_settings.temp_max = 2.0
    fluid.domain_settings.temp_min = 0.0

    # Material for smoke
    smoke_mat = bpy.data.materials.new(name=f"Smoke_{domain.name}")
    smoke_mat.use_nodes = True
    nodes = smoke_mat.node_tree.nodes
    links = smoke_mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add volume shader
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)

    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (0, 0)

    # Configure volume shader for smoke
    volume.inputs['Density'].default_value = 0.5
    volume.inputs['Color'].default_value = (0.8, 0.3, 0.1, 1.0)  # Orange smoke
    volume.inputs['Emission Strength'].default_value = 2.0
    volume.inputs['Emission Color'].default_value = (
        1.0, 0.4, 0.1, 1.0)  # Bright orange

    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Assign material
    domain.data.materials.append(smoke_mat)

    return domain


def create_explosion_source(location, domain):
    """Create a Mantaflow flow object for explosion source"""
    print(f"   Creating explosion source at {location}")

    # Create small sphere for source
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=location)
    source = bpy.context.active_object
    source.name = f"Explosion_Source_{len([o for o in bpy.data.objects if o.name.startswith('Explosion_Source')])}"

    # Set up as Mantaflow flow
    source.modifiers.new(name="Fluid", type='FLUID_SIMULATION')
    source.modifiers["Fluid"].fluid_type = 'FLOW'

    # Configure flow settings
    fluid = source.modifiers["Fluid"]
    fluid.flow_settings.flow_type = 'SMOKE'
    fluid.flow_settings.smoke_flow_type = 'BOTH'
    fluid.flow_settings.smoke_flow_source = 'DENSITY'
    fluid.flow_settings.smoke_flow_behavior = 'INFLOW'

    # Explosion parameters
    fluid.flow_settings.smoke_color = (1.0, 0.3, 0.1, 1.0)  # Orange
    fluid.flow_settings.temperature = 2.0
    fluid.flow_settings.density = 1.0
    fluid.flow_settings.smoke_flow_velocity = 5.0

    # Make invisible
    source.hide_render = True
    source.hide_viewport = True

    return source


def create_explosion_animation(source, start_frame, duration=20):
    """Animate the explosion source"""
    print(f"   Animating explosion from frame {start_frame}")

    # Keyframe the source to appear and disappear
    source.hide_viewport = True
    source.hide_render = True

    # Start hidden
    source.keyframe_insert(data_path="hide_viewport", frame=start_frame - 1)
    source.keyframe_insert(data_path="hide_render", frame=start_frame - 1)

    # Appear at start frame
    source.hide_viewport = False
    source.hide_render = False
    source.keyframe_insert(data_path="hide_viewport", frame=start_frame)
    source.keyframe_insert(data_path="hide_render", frame=start_frame)

    # Disappear after duration
    source.hide_viewport = True
    source.hide_render = True
    source.keyframe_insert(data_path="hide_viewport", frame=start_frame + duration)
    source.keyframe_insert(data_path="hide_render", frame=start_frame + duration)


def create_realistic_explosions():
    """Create realistic explosions with Mantaflow"""
    print("\n" + "=" * 80)
    print("🔥 CREATING REALISTIC EXPLOSIONS")
    print("=" * 80 + "\n")

    # Clear old explosions
    clear_existing_explosions()

    # Explosion locations and timing (from original scene)
    explosion_data = [
        {"location": (4.14, 2.42, 4.70), "start_frame": 140, "name": "Explosion_0"},
        {"location": (5.13, -3.71, 3.09), "start_frame": 97, "name": "Explosion_1"},
        {"location": (0.60, -6.07, 3.62), "start_frame": 125, "name": "Explosion_2"},
        {"location": (0.73, 4.27, 1.30), "start_frame": 91, "name": "Explosion_3"},
        {"location": (-1.54, 5.11, 4.25), "start_frame": 89, "name": "Explosion_4"},
        {"location": (3.95, 5.50, 3.69), "start_frame": 138, "name": "Explosion_5"},
        {"location": (-2.93, -4.02, 2.20), "start_frame": 56, "name": "Explosion_6"},
        {"location": (2.50, -3.20, 4.84), "start_frame": 183, "name": "Explosion_7"},
    ]

    domains = []
    sources = []

    for i, exp_data in enumerate(explosion_data):
        print(f"\nCreating explosion {i + 1}/8: {exp_data['name']}")

        # Create domain
        domain = create_explosion_domain(exp_data["location"], size=6.0)
        domains.append(domain)

        # Create source
        source = create_explosion_source(exp_data["location"], domain)
        sources.append(source)

        # Animate source
        create_explosion_animation(source, exp_data["start_frame"], duration=15)

        print(f"   ✅ Explosion {i + 1} created")

    print(f"\n✅ Created {len(domains)} explosion domains and {len(sources)} sources")
    print("\n⚠️  IMPORTANT: You need to bake the simulation for realistic results!")
    print("   Go to: Physics Properties > Fluid > Bake")
    print("   This will take 10-30 minutes depending on resolution")
    print("   Higher resolution = more realistic but slower")


def setup_volume_rendering():
    """Configure scene for volume rendering"""
    print("\n🎨 Setting up volume rendering...")

    # Enable volume rendering in Cycles
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.volume_bounces = 4
        scene.cycles.volume_step_size = 0.1
        print("   ✅ Volume rendering enabled in Cycles")
    else:
        print("   ⚠️  Switch to Cycles for best volume rendering")


if __name__ == "__main__":
    print("🔥 REALISTIC EXPLOSIONS SETUP")
    print("This will replace simple spheres with Mantaflow smoke simulation")
    print("Warning: This requires baking simulation (10-30 minutes)")
    print()

    create_realistic_explosions()
    setup_volume_rendering()

    print("\n" + "=" * 80)
    print("🎬 NEXT STEPS:")
    print("=" * 80)
    print("1. Go to Physics Properties > Fluid")
    print("2. Click 'Bake' for each explosion domain")
    print("3. Wait 10-30 minutes for simulation")
    print("4. Render to see realistic smoke/fire!")
    print("\nThis is much more realistic than simple spheres! 🔥")
