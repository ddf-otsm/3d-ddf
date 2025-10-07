#!/usr/bin/env blender --background --python
"""
Integrate Text with Explosions

Creates a complete scene with 3D text and explosion effects.
This is the integration script for the dadosfera project.

Run with: blender --background --python integrate_text_with_explosions.py -- "TEXT"
"""
import sys
import bpy
from pathlib import Path


def clear_scene():
    """Remove all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def create_text_3d(text: str, font_size: float = 1.0, extrude_depth: float = 0.3):
    """Create a 3D extruded text object."""
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = f"Text_{text[:10]}"
    
    text_data = text_obj.data
    text_data.body = text
    text_data.size = font_size
    text_data.extrude = extrude_depth
    text_data.bevel_depth = 0.01
    text_data.bevel_resolution = 2
    text_data.align_x = 'CENTER'
    text_data.align_y = 'CENTER'
    
    return text_obj


def apply_material(obj, color=(0.8, 0.2, 0.1), metallic=0.8, roughness=0.2):
    """Apply a PBR material to the object."""
    mat = bpy.data.materials.new(name=f"Material_{obj.name}")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def create_simple_explosion(location, frame_start, scale=1.0):
    """
    Create a simple explosion effect using particle system.
    
    Args:
        location: (x, y, z) tuple for explosion position
        frame_start: Frame when explosion starts
        scale: Scale of the explosion
    """
    # Create emitter
    bpy.ops.mesh.primitive_ico_sphere_add(location=location, subdivisions=1, size=0.1)
    emitter = bpy.context.active_object
    emitter.name = f"Explosion_Emitter_{frame_start}"
    
    # Add particle system
    bpy.ops.object.particle_system_add()
    ps = emitter.particle_systems[0]
    ps_settings = ps.settings
    
    # Configure particles
    ps_settings.count = 100 * scale
    ps_settings.frame_start = frame_start
    ps_settings.frame_end = frame_start + 1
    ps_settings.lifetime = 30
    ps_settings.lifetime_random = 0.3
    
    # Physics
    ps_settings.normal_factor = 2.0
    ps_settings.factor_random = 0.5
    ps_settings.physics_type = 'NEWTON'
    ps_settings.mass = 0.5
    ps_settings.use_die_on_collision = False
    
    # Render
    ps_settings.render_type = 'HALO'
    ps_settings.particle_size = 0.05 * scale
    ps_settings.size_random = 0.5
    
    # Create material for particles
    mat = bpy.data.materials.new(name=f"Explosion_Mat_{frame_start}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # Emission shader for fire effect
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 0.3, 0.1, 1.0)  # Orange fire
    emission.inputs['Strength'].default_value = 5.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    if emitter.data.materials:
        emitter.data.materials[0] = mat
    else:
        emitter.data.materials.append(mat)
    
    return emitter


def setup_camera_and_lighting():
    """Set up camera and lighting for the scene."""
    # Camera
    bpy.ops.object.camera_add(location=(0, -6, 2.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.15, 0, 0)
    bpy.context.scene.camera = camera
    
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(4, -4, 6))
    key_light = bpy.context.active_object
    key_light.data.energy = 600
    key_light.data.size = 6
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-4, -3, 4))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 250
    fill_light.data.size = 4
    
    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 3, 4))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 400
    rim_light.data.size = 3


def configure_animation(total_frames=120):
    """Configure animation settings."""
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.frame_current = 1
    scene.render.fps = 24


def configure_render_settings(output_path: Path, resolution=(1920, 1080), samples=128):
    """Configure render settings."""
    scene = bpy.context.scene
    
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.device = 'GPU' if bpy.context.preferences.addons.get('cycles') else 'CPU'
    
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    
    scene.render.filepath = str(output_path)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'


def main():
    """Main execution function."""
    # Parse arguments
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
    else:
        argv = []
    
    text = argv[0] if len(argv) > 0 else "DADOSFERA"
    
    print(f"\n{'='*70}")
    print(f"TEXT + EXPLOSIONS INTEGRATION")
    print(f"{'='*70}")
    print(f"Text: {text}")
    print(f"{'='*70}\n")
    
    # Clear scene
    clear_scene()
    
    # Create 3D text
    print("Creating 3D text...")
    text_obj = create_text_3d(text, font_size=1.2, extrude_depth=0.4)
    apply_material(text_obj, color=(0.1, 0.3, 0.8), metallic=0.9, roughness=0.1)
    
    # Setup camera and lighting
    print("Setting up camera and lighting...")
    setup_camera_and_lighting()
    
    # Configure animation
    print("Configuring animation...")
    configure_animation(total_frames=120)
    
    # Add explosions at different times and positions
    print("Adding explosions...")
    explosion_configs = [
        {'location': (-2, 1, 0.5), 'frame': 30, 'scale': 1.2},
        {'location': (2, 1, 0.5), 'frame': 45, 'scale': 1.0},
        {'location': (0, 2, 1.0), 'frame': 60, 'scale': 1.5},
        {'location': (-1.5, -1, 0.3), 'frame': 75, 'scale': 0.8},
        {'location': (1.5, -1, 0.3), 'frame': 90, 'scale': 0.8},
    ]
    
    for config in explosion_configs:
        create_simple_explosion(
            location=config['location'],
            frame_start=config['frame'],
            scale=config['scale']
        )
    
    # Configure output
    output_dir = Path(__file__).parent.parent / "projects" / "dadosfera" / "renders" / "integration_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Render a few keyframes
    print("Rendering keyframes...")
    keyframes = [1, 30, 45, 60, 75, 90, 120]
    
    for frame in keyframes:
        bpy.context.scene.frame_set(frame)
        output_path = output_dir / f"frame_{frame:04d}.png"
        configure_render_settings(output_path, samples=64)  # Lower samples for speed
        print(f"  Rendering frame {frame}...")
        bpy.ops.render.render(write_still=True)
    
    print(f"\n{'='*70}")
    print(f"✅ INTEGRATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Output: {output_dir}")
    print(f"Frames rendered: {len(keyframes)}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()



