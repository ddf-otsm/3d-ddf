#!/usr/bin/env blender --background --python
"""
Text to 3D Proof of Concept

Creates a 3D extruded text object from a string input.
Run with: blender --background --python text_to_3d_poc.py -- "YOUR TEXT"
"""
import sys
import bpy
from pathlib import Path


def clear_scene():
    """Remove all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def create_text_3d(text: str, font_size: float = 1.0, extrude_depth: float = 0.3):
    """
    Create a 3D extruded text object.
    
    Args:
        text: Text to convert to 3D
        font_size: Size of the text
        extrude_depth: Depth of extrusion
        
    Returns:
        The created text object
    """
    # Create text object
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = f"Text_{text[:10]}"
    
    # Configure text data
    text_data = text_obj.data
    text_data.body = text
    text_data.size = font_size
    text_data.extrude = extrude_depth
    text_data.bevel_depth = 0.01
    text_data.bevel_resolution = 2
    
    # Center alignment
    text_data.align_x = 'CENTER'
    text_data.align_y = 'CENTER'
    
    return text_obj


def apply_material(obj, color=(0.8, 0.2, 0.1), metallic=0.8, roughness=0.2):
    """
    Apply a PBR material to the object.
    
    Args:
        obj: Object to apply material to
        color: RGB color tuple
        metallic: Metallic value (0-1)
        roughness: Roughness value (0-1)
    """
    # Create material
    mat = bpy.data.materials.new(name=f"Material_{obj.name}")
    mat.use_nodes = True
    
    # Get nodes
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    # Create output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    # Link nodes
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def setup_camera_and_lighting():
    """Set up camera and lighting for the scene."""
    # Add camera
    bpy.ops.object.camera_add(location=(0, -5, 2))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0)  # Point at origin
    bpy.context.scene.camera = camera
    
    # Add key light
    bpy.ops.object.light_add(type='AREA', location=(3, -3, 5))
    key_light = bpy.context.active_object
    key_light.data.energy = 500
    key_light.data.size = 5
    
    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 200
    fill_light.data.size = 3
    
    # Add rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 2, 3))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 300
    rim_light.data.size = 2


def configure_render_settings(output_path: Path, resolution=(1920, 1080), samples=128):
    """Configure render settings."""
    scene = bpy.context.scene
    
    # Render engine
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    
    # Resolution
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    
    # Output
    scene.render.filepath = str(output_path)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'


def export_model(obj, output_path: Path, format='OBJ'):
    """
    Export the 3D model.
    
    Args:
        obj: Object to export
        output_path: Path for export file
        format: Export format (OBJ, FBX, GLTF)
    """
    # Select only the text object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    if format == 'OBJ':
        bpy.ops.wm.obj_export(
            filepath=str(output_path),
            export_selected_objects=True,
            export_materials=True
        )
    elif format == 'GLTF':
        bpy.ops.export_scene.gltf(
            filepath=str(output_path),
            use_selection=True,
            export_format='GLB'
        )


def main():
    """Main execution function."""
    # Parse arguments
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
    else:
        argv = []
    
    # Get text input
    if len(argv) > 0:
        text = argv[0]
    else:
        text = "DADOSFERA"
    
    print(f"\n{'='*70}")
    print(f"TEXT TO 3D POC")
    print(f"{'='*70}")
    print(f"Input text: {text}")
    print(f"{'='*70}\n")
    
    # Clear scene
    clear_scene()
    
    # Create 3D text
    print("Creating 3D text object...")
    text_obj = create_text_3d(text, font_size=1.0, extrude_depth=0.3)
    
    # Apply material
    print("Applying material...")
    apply_material(text_obj, color=(0.8, 0.2, 0.1), metallic=0.8, roughness=0.2)
    
    # Setup scene
    print("Setting up camera and lighting...")
    setup_camera_and_lighting()
    
    # Configure rendering
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    render_path = output_dir / f"text_3d_{text[:10].lower()}.png"
    print(f"Configuring render to: {render_path}")
    configure_render_settings(render_path, samples=128)
    
    # Export model
    export_path = output_dir / f"text_3d_{text[:10].lower()}.obj"
    print(f"Exporting model to: {export_path}")
    export_model(text_obj, export_path, format='OBJ')
    
    # Render
    print("Rendering...")
    bpy.ops.render.render(write_still=True)
    
    print(f"\n{'='*70}")
    print(f"✅ SUCCESS!")
    print(f"{'='*70}")
    print(f"Render: {render_path}")
    print(f"Model:  {export_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()



