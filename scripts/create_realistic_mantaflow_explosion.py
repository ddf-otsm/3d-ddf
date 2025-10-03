#!/usr/bin/env python3
"""
Create a TRULY realistic explosion using Mantaflow smoke simulation
This will be much more realistic than simple spheres
"""

import bpy
import bmesh
from mathutils import Vector


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


def create_mantaflow_explosion(location, start_frame):
    """Create a realistic explosion using Mantaflow"""
    print(f"   Creating Mantaflow explosion at {location}")

    # Create domain for smoke simulation
    bpy.ops.mesh.primitive_cube_add(size=4.0, location=location)
    domain = bpy.context.active_object
    domain.name = "Explosion_Domain"

    # Set up as Mantaflow domain
    domain.modifiers.new(name="Fluid", type='FLUID')
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

    # Create flow object (explosion source)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=location)
    source = bpy.context.active_object
    source.name = "Explosion_Source"

    # Set up as Mantaflow flow
    source.modifiers.new(name="Fluid", type='FLUID')
    source.modifiers["Fluid"].fluid_type = 'FLOW'

    # Configure flow settings
    flow_fluid = source.modifiers["Fluid"]
    flow_fluid.flow_settings.flow_type = 'SMOKE'
    flow_fluid.flow_settings.smoke_flow_type = 'BOTH'
    flow_fluid.flow_settings.smoke_flow_source = 'DENSITY'
    flow_fluid.flow_settings.smoke_flow_behavior = 'INFLOW'

    # Explosion parameters
    flow_fluid.flow_settings.smoke_color = (1.0, 0.3, 0.1, 1.0)  # Orange
    flow_fluid.flow_settings.temperature = 2.0
    flow_fluid.flow_settings.density = 1.0
    flow_fluid.flow_settings.smoke_flow_velocity = 5.0

    # Animate source to appear and disappear
    source.hide_viewport = True
    source.hide_render = True
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
    source.keyframe_insert(data_path="hide_viewport", frame=start_frame + 15)
    source.keyframe_insert(data_path="hide_render", frame=start_frame + 15)

    # Create realistic smoke material
    create_smoke_material(domain)

    return domain, source


def create_smoke_material(domain):
    """Create realistic smoke material with volume shader"""
    mat = bpy.data.materials.new(name="Realistic_Smoke")
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

    # Configure for realistic smoke
    volume.inputs['Density'].default_value = 0.3
    volume.inputs['Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray smoke
    volume.inputs['Emission Strength'].default_value = 1.0
    volume.inputs['Emission Color'].default_value = (1.0, 0.4, 0.1, 1.0)  # Orange glow

    # Add noise for smoke variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 3.0

    # Connect noise to density
    links.new(noise.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Assign material
    domain.data.materials.append(mat)


def create_realistic_explosion():
    """Create the complete realistic explosion scene"""
    print("\n" + "=" * 80)
    print("🔥 CREATING REALISTIC MANTAFLOW EXPLOSION")
    print("=" * 80 + "\n")

    # Clear and setup scene
    clear_scene()
    setup_scene()

    # Create Mantaflow explosion
    domain, source = create_mantaflow_explosion((0, 0, 1), 10)

    print("\n" + "=" * 80)
    print("🎬 REALISTIC EXPLOSION READY!")
    print("=" * 80)
    print("This explosion uses Mantaflow smoke simulation for realism!")
    print("\n⚠️  IMPORTANT: You need to bake the simulation!")
    print("1. Go to Physics Properties > Fluid")
    print("2. Click 'Bake' for the domain")
    print("3. Wait 5-10 minutes for simulation")
    print("4. Render to see realistic smoke/fire!")
    print("\nThis will be MUCH more realistic than simple spheres! 🔥")


if __name__ == "__main__":
    print("🔥 REALISTIC MANTAFLOW EXPLOSION")
    print("This creates a physics-based explosion with real smoke simulation")
    print("Much more realistic than simple spheres!")
    print()

    create_realistic_explosion()

    print("\n" + "=" * 80)
    print("🎬 NEXT STEPS:")
    print("=" * 80)
    print("1. Save this scene")
    print("2. Bake the Mantaflow simulation (5-10 minutes)")
    print("3. Render to see realistic fire and smoke!")
    print("4. This will look like a REAL explosion! 🔥")
