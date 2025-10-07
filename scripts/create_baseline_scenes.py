#!/usr/bin/env python3
"""
Create Baseline Scenes for Explosion Development

This script creates the baseline scenes needed for the explosion development roadmap:
1. dadosfera_v2_clean.blend - Clean Dadosfera scene with professional materials
2. particle_explosion_v1.blend - Particle explosion test scene

Usage:
  blender --background --python create_baseline_scenes.py -- --output-dadosfera /path/to/dadosfera_v2_clean.blend --output-explosion /path/to/particle_explosion_v1.blend
"""

import bpy
import bmesh
import sys
import argparse
from mathutils import Vector
from pathlib import Path

def clear_scene():
    """Clear the current scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Clear meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

def create_dadosfera_scene():
    """Create the clean Dadosfera baseline scene."""
    print("🎬 Creating Dadosfera v2 Clean Scene...")
    
    # Clear scene
    clear_scene()
    
    # Create 3D text "DADOSFERA"
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = "Dadosfera_Text"
    text_obj.data.body = "DADOSFERA"
    text_obj.data.size = 2.0
    text_obj.data.font = bpy.data.fonts.load("/System/Library/Fonts/Arial.ttf")  # Fallback to default
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.convert(target='MESH')
    
    # Add solidify modifier for thickness
    solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.1
    
    # Create professional metallic material
    metallic_mat = bpy.data.materials.new(name="Dadosfera_Metallic")
    metallic_mat.use_nodes = True
    nodes = metallic_mat.node_tree.nodes
    links = metallic_mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Connect nodes
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Set metallic properties
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.2
    bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1.0)  # Slightly blue metallic
    
    # Assign material
    text_obj.data.materials.append(metallic_mat)
    
    # Create studio floor
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    
    # Create floor material
    floor_mat = bpy.data.materials.new(name="Studio_Floor")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    links = floor_mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Connect nodes
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Set floor properties
    bsdf.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Dark gray
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Metallic'].default_value = 0.0
    
    # Assign material
    floor.data.materials.append(floor_mat)
    
    # Set up lighting
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 3.0
    key_light.data.color = (1.0, 0.95, 0.8)
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 5))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 1.0
    fill_light.data.color = (0.8, 0.9, 1.0)
    
    # Rim light
    bpy.ops.object.light_add(type='SPOT', location=(0, -8, 3))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 2.0
    rim_light.data.color = (1.0, 0.9, 0.7)
    
    # Set up camera
    bpy.ops.object.camera_add(location=(8, -8, 5))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (1.1, 0, 0.8)  # Look at text
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Set render settings
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    
    print("✅ Dadosfera v2 Clean Scene created successfully!")

def create_particle_explosion_scene():
    """Create the particle explosion test scene."""
    print("💥 Creating Particle Explosion Test Scene...")
    
    # Clear scene
    clear_scene()
    
    # Create emitter object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0, 0))
    emitter = bpy.context.active_object
    emitter.name = "Explosion_Emitter"
    
    # Add particle system
    bpy.ops.object.particle_system_add()
    ps = emitter.particle_systems[0]
    settings = ps.settings
    
    # Configure particle system for fire
    settings.type = 'EMITTER'
    settings.count = 1000
    settings.frame_start = 1
    settings.frame_end = 10
    settings.lifetime = 60
    settings.lifetime_random = 0.5
    settings.physics_type = 'NEWTON'
    settings.normal_factor = 2.0
    settings.tangent_factor = 0.1
    settings.factor_random = 0.5
    
    # Create fire material
    fire_mat = bpy.data.materials.new(name="Fire_Material")
    fire_mat.use_nodes = True
    nodes = fire_mat.node_tree.nodes
    links = fire_mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Emission shader
    emission = nodes.new(type='ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Color'].default_value = (1.0, 0.3, 0.0, 1.0)  # Orange fire
    emission.inputs['Strength'].default_value = 5.0
    
    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    emitter.data.materials.append(fire_mat)
    
    # Create smoke domain
    bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 2))
    domain = bpy.context.active_object
    domain.name = "Smoke_Domain"
    
    # Add smoke modifier
    smoke_mod = domain.modifiers.new(name="Smoke", type='SMOKE')
    smoke_mod.smoke_type = 'DOMAIN'
    smoke_mod.domain_settings.resolution_max = 64  # Low res for testing
    smoke_mod.domain_settings.alpha = 0.1
    smoke_mod.domain_settings.beta = 0.1
    
    # Create smoke material
    smoke_mat = bpy.data.materials.new(name="Smoke_Material")
    smoke_mat.use_nodes = True
    nodes = smoke_mat.node_tree.nodes
    links = smoke_mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Volume Scatter
    volume_scatter = nodes.new(type='ShaderNodeVolumeScatter')
    volume_scatter.location = (0, 0)
    volume_scatter.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # Gray smoke
    volume_scatter.inputs['Density'].default_value = 0.1
    
    # Add Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Connect nodes
    links.new(volume_scatter.outputs['Volume'], output.inputs['Volume'])
    
    # Assign material
    domain.data.materials.append(smoke_mat)
    
    # Set up camera
    bpy.ops.object.camera_add(location=(5, -5, 3))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (1.2, 0, 0.8)  # Look at explosion
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Set render settings
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # Lower samples for testing
    
    print("✅ Particle Explosion Test Scene created successfully!")

def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Create baseline scenes for explosion development')
    parser.add_argument('--output-dadosfera', type=str, help='Output path for Dadosfera scene')
    parser.add_argument('--output-explosion', type=str, help='Output path for explosion scene')
    parser.add_argument('--dadosfera-only', action='store_true', help='Create only Dadosfera scene')
    parser.add_argument('--explosion-only', action='store_true', help='Create only explosion scene')
    
    # Parse args after "--"
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    
    args = parser.parse_args(argv)
    
    # Create Dadosfera scene
    if not args.explosion_only:
        create_dadosfera_scene()
        if args.output_dadosfera:
            output_path = Path(args.output_dadosfera)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            bpy.ops.wm.save_as_mainfile(filepath=str(output_path))
            print(f"💾 Saved Dadosfera scene: {output_path}")
    
    # Create explosion scene
    if not args.dadosfera_only:
        create_particle_explosion_scene()
        if args.output_explosion:
            output_path = Path(args.output_explosion)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            bpy.ops.wm.save_as_mainfile(filepath=str(output_path))
            print(f"💾 Saved explosion scene: {output_path}")
    
    print("🎉 Baseline scenes creation complete!")

if __name__ == "__main__":
    main()
