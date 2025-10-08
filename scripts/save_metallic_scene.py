#!/usr/bin/env python3
"""
Save Metallic Dadosfera Scene

This script creates the metallic scene and saves it to a blend file.
"""

import bpy
import os
from pathlib import Path

def clear_scene():
    """Clear the scene of all objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_metallic_dadosfera_scene():
    """Create the Dadosfera scene with metallic materials."""
    print("🎬 Creating Dadosfera with Metallic Materials...")
    
    # Clear scene
    clear_scene()
    
    # Create 3D text "DADOSFERA"
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = "Dadosfera_Text"
    text_obj.data.body = "DADOSFERA"
    text_obj.data.size = 2.0
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.convert(target='MESH')
    
    # Add solidify modifier for thickness
    solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.15
    
    # Create professional metallic material
    metallic_mat = bpy.data.materials.new(name="Dadosfera_Chrome_Metallic")
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
    
    # Set metallic properties for chrome-like appearance
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.95, 1.0)  # Slightly blue-white
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metallic
    bsdf.inputs['Roughness'].default_value = 0.05  # Very shiny
    bsdf.inputs['Specular IOR Level'].default_value = 1.0
    bsdf.inputs['Coat Weight'].default_value = 0.8  # Clear coat for extra shine
    
    # Assign material
    text_obj.data.materials.append(metallic_mat)
    
    # Create studio floor
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    
    # Create floor material
    floor_mat = bpy.data.materials.new(name="Studio_Floor_Reflective")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    links = floor_mat.node_tree.links
    
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Dark reflective floor
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark grey
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.1  # Very reflective
    bsdf.inputs['Specular IOR Level'].default_value = 0.9
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    floor.data.materials.append(floor_mat)
    
    # Add professional lighting
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 5.0
    key_light.data.color = (1.0, 0.95, 0.8)  # Warm white
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 8))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 2.0
    fill_light.data.size = 5.0
    fill_light.data.color = (0.8, 0.9, 1.0)  # Cool white
    
    # Rim light
    bpy.ops.object.light_add(type='SPOT', location=(0, -8, 6))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 3.0
    rim_light.data.spot_size = 0.5
    rim_light.data.color = (1.0, 0.8, 0.6)  # Warm rim
    
    # Add camera
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.name = "Main_Camera"
    camera.rotation_euler = (1.1, 0, 0.785)  # Angled view
    
    # Set camera as active
    bpy.context.scene.camera = camera
    
    # Set render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 512
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Enable denoising
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    
    print("✅ Created metallic Dadosfera scene with professional lighting")

def save_scene():
    """Save the scene to a blend file."""
    # Get project root
    project_root = Path(__file__).resolve().parent.parent
    
    # Create output directory
    output_dir = project_root / "projects/dadosfera/blender_files/active"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save blend file
    blend_file = output_dir / "dadosfera_metallic_materials.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))
    
    print(f"✅ Scene saved to: {blend_file}")

def main():
    """Main execution function."""
    print("=" * 70)
    print("🎬 DADOSFERA METALLIC MATERIAL SETUP & SAVE")
    print("=" * 70)
    
    create_metallic_dadosfera_scene()
    save_scene()
    
    print("\n" + "=" * 70)
    print("✅ METALLIC SCENE SAVED!")
    print("=" * 70)

if __name__ == '__main__':
    main()
