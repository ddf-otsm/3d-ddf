#!/usr/bin/env python3
"""
Enhanced Dadosfera Scene with Metallic Materials and Atomic Bomb Explosions

Creates a high-quality dadosfera scene with:
- Metallic text materials (chrome/gold finish)
- Realistic atomic bomb-style explosions
- Enhanced particle systems with fire, smoke, and debris
- Professional lighting and camera work
- Production-ready rendering settings
"""

import bpy
import bmesh
from mathutils import Vector
import random
import time

def clear_scene():
    """Clear existing scene objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    print("🧹 Scene cleared")

def create_metallic_text_material():
    """Create a realistic metallic material for text"""
    mat = bpy.data.materials.new(name="Metallic_Chrome")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Metallic settings
    bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1.0)  # Slight blue tint
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metallic
    bsdf.inputs['Roughness'].default_value = 0.1  # Very shiny
    bsdf.inputs['Specular IOR Level'].default_value = 0.9
    
    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_gold_text_material():
    """Create a gold metallic material"""
    mat = bpy.data.materials.new(name="Metallic_Gold")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Gold settings
    bsdf.inputs['Base Color'].default_value = (1.0, 0.7, 0.2, 1.0)  # Gold color
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.05  # Very shiny gold
    bsdf.inputs['Specular IOR Level'].default_value = 0.9
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_dadosfera_text():
    """Create the main dadosfera text with metallic materials"""
    # Create text
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = "Dadosfera_Text"
    
    # Set text content
    text_obj.data.body = "DADOSFERA"
    text_obj.data.size = 2.0
    # Use default font
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.convert(target='MESH')
    
    # Add metallic material
    chrome_mat = create_metallic_text_material()
    text_obj.data.materials.append(chrome_mat)
    
    # Add slight animation
    text_obj.keyframe_insert(data_path="location", frame=1)
    text_obj.location.z = 0.2
    text_obj.keyframe_insert(data_path="location", frame=60)
    text_obj.location.z = 0
    text_obj.keyframe_insert(data_path="location", frame=120)
    
    print("✨ Created metallic dadosfera text")
    return text_obj

def create_atomic_fire_material():
    """Create realistic fire material for atomic explosion"""
    mat = bpy.data.materials.new(name="Atomic_Fire")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Emission shader for fire
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Color'].default_value = (1.0, 0.3, 0.1, 1.0)  # Orange fire
    emission.inputs['Strength'].default_value = 10.0
    
    # Add color ramp for fire gradient
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-200, 0)
    color_ramp.color_ramp.elements[0].color = (1.0, 0.1, 0.0, 1.0)  # Red
    color_ramp.color_ramp.elements[1].color = (1.0, 0.8, 0.0, 1.0)  # Yellow
    
    # Noise texture for fire variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 10.0
    
    # Geometry node for position
    geometry = nodes.new('ShaderNodeNewGeometry')
    geometry.location = (-600, 0)
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    links.new(geometry.outputs['Position'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    return mat

def create_atomic_smoke_material():
    """Create realistic smoke material for atomic explosion"""
    mat = bpy.data.materials.new(name="Atomic_Smoke")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    # Principled Volume for smoke
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (0, 0)
    volume.inputs['Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray smoke
    volume.inputs['Density'].default_value = 0.5
    volume.inputs['Anisotropy'].default_value = 0.8
    
    # Noise for smoke variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-200, 0)
    noise.inputs['Scale'].default_value = 2.0
    noise.inputs['Detail'].default_value = 5.0
    
    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    links.new(noise.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])
    
    return mat

def create_atomic_explosion(location, start_frame, scale=1.0):
    """Create a realistic atomic bomb explosion"""
    print(f"💥 Creating atomic explosion at {location}")
    
    # Create explosion emitter
    bpy.ops.mesh.primitive_ico_sphere_add(location=location, subdivisions=2)
    emitter = bpy.context.active_object
    emitter.scale = (0.1, 0.1, 0.1)
    emitter.name = f"Atomic_Explosion_{start_frame}"
    
    # Add particle system for fire
    bpy.ops.object.particle_system_add()
    ps = emitter.particle_systems[0]
    ps.name = f"Atomic_Fire_{start_frame}"
    
    settings = ps.settings
    settings.type = 'EMITTER'
    settings.count = int(2000 * scale)  # Massive particle count
    settings.frame_start = start_frame
    settings.frame_end = start_frame + 3  # Short burst
    settings.lifetime = 60  # Long-lasting fire
    settings.lifetime_random = 0.8
    
    # Explosion physics
    settings.physics_type = 'NEWTON'
    settings.mass = 0.05
    settings.normal_factor = 15.0 * scale  # Massive outward force
    settings.factor_random = 0.9
    settings.angular_velocity_factor = 5.0
    
    # No gravity for atomic explosion
    settings.effector_weights.gravity = 0.0
    settings.effector_weights.all = 1.0
    
    # Render settings
    settings.render_type = 'HALO'
    settings.particle_size = 0.2 * scale
    settings.size_random = 0.8
    
    # Apply fire material
    fire_mat = create_atomic_fire_material()
    emitter.data.materials.append(fire_mat)
    
    # Create smoke volume
    bpy.ops.mesh.primitive_cube_add(location=location)
    smoke_obj = bpy.context.active_object
    smoke_obj.scale = (2.0 * scale, 2.0 * scale, 2.0 * scale)
    smoke_obj.name = f"Atomic_Smoke_{start_frame}"
    
    # Add smoke material
    smoke_mat = create_atomic_smoke_material()
    smoke_obj.data.materials.append(smoke_mat)
    
    # Animate smoke expansion
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame)
    smoke_obj.scale = (0.1, 0.1, 0.1)
    smoke_obj.keyframe_insert(data_path="scale", frame=start_frame + 30)
    smoke_obj.scale = (3.0 * scale, 3.0 * scale, 3.0 * scale)
    
    # Animate smoke opacity
    smoke_obj.keyframe_insert(data_path="hide_render", frame=start_frame)
    smoke_obj.hide_render = True
    smoke_obj.keyframe_insert(data_path="hide_render", frame=start_frame + 5)
    smoke_obj.hide_render = False
    smoke_obj.keyframe_insert(data_path="hide_render", frame=start_frame + 60)
    smoke_obj.hide_render = True
    
    return [emitter, smoke_obj]

def create_debris_particles(location, start_frame, scale=1.0):
    """Create debris particles for atomic explosion"""
    bpy.ops.mesh.primitive_ico_sphere_add(location=location)
    debris_emitter = bpy.context.active_object
    debris_emitter.scale = (0.05, 0.05, 0.05)
    debris_emitter.name = f"Atomic_Debris_{start_frame}"
    
    # Add particle system
    bpy.ops.object.particle_system_add()
    ps = debris_emitter.particle_systems[0]
    ps.name = f"Atomic_Debris_Particles_{start_frame}"
    
    settings = ps.settings
    settings.type = 'EMITTER'
    settings.count = int(500 * scale)
    settings.frame_start = start_frame
    settings.frame_end = start_frame + 2
    settings.lifetime = 120  # Long debris lifetime
    settings.lifetime_random = 0.7
    
    # Debris physics
    settings.physics_type = 'NEWTON'
    settings.mass = 0.2
    settings.normal_factor = 8.0 * scale
    settings.factor_random = 0.8
    settings.angular_velocity_factor = 3.0
    
    # Gravity affects debris
    settings.effector_weights.gravity = 0.5
    
    # Render as objects
    settings.render_type = 'OBJECT'
    settings.particle_size = 0.1 * scale
    settings.size_random = 0.6
    
    # Create debris material
    debris_mat = bpy.data.materials.new(name=f"Debris_{start_frame}")
    debris_mat.use_nodes = True
    nodes = debris_mat.node_tree.nodes
    links = debris_mat.node_tree.links
    
    nodes.clear()
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.3, 0.2, 0.1, 1.0)  # Dark brown
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.7
    
    output = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    debris_emitter.data.materials.append(debris_mat)
    
    return debris_emitter

def setup_atomic_lighting():
    """Set up dramatic lighting for atomic explosion"""
    # Clear existing lights
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
    bpy.ops.object.delete()
    
    # Add sun light for overall illumination
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.name = "Atomic_Sun"
    sun.data.energy = 5.0
    sun.data.color = (1.0, 0.9, 0.7)  # Warm sunlight
    
    # Add point light for explosion illumination
    bpy.ops.object.light_add(type='POINT', location=(0, 0, 2))
    explosion_light = bpy.context.active_object
    explosion_light.name = "Atomic_Explosion_Light"
    explosion_light.data.energy = 50.0
    explosion_light.data.color = (1.0, 0.5, 0.2)  # Orange explosion light
    
    # Animate explosion light
    explosion_light.data.energy = 0.0
    explosion_light.data.keyframe_insert(data_path="energy", frame=1)
    explosion_light.data.energy = 100.0
    explosion_light.data.keyframe_insert(data_path="energy", frame=100)
    explosion_light.data.energy = 0.0
    explosion_light.data.keyframe_insert(data_path="energy", frame=120)
    
    print("💡 Set up atomic explosion lighting")

def setup_camera():
    """Set up cinematic camera for atomic explosion"""
    # Clear existing cameras
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':
            obj.select_set(True)
    bpy.ops.object.delete()
    
    # Add camera
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.name = "Atomic_Camera"
    
    # Point camera at text
    camera.rotation_euler = (1.1, 0, 0.785)  # Angled view
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Add slight camera shake for explosion
    camera.keyframe_insert(data_path="location", frame=1)
    camera.location = (8, -8, 6)
    camera.keyframe_insert(data_path="location", frame=100)
    camera.location = (8.2, -8.1, 6.1)  # Slight shake
    camera.keyframe_insert(data_path="location", frame=120)
    camera.location = (8, -8, 6)
    
    print("📹 Set up cinematic camera")

def create_enhanced_dadosfera_atomic():
    """Create the complete enhanced dadosfera scene with atomic explosions"""
    print("\n" + "=" * 80)
    print("☢️  CREATING ENHANCED DADOSFERA WITH ATOMIC EXPLOSIONS")
    print("=" * 80 + "\n")
    
    # Clear scene
    clear_scene()
    
    # Create metallic text
    text_obj = create_dadosfera_text()
    
    # Set up lighting
    setup_atomic_lighting()
    
    # Set up camera
    setup_camera()
    
    # Create atomic explosions at strategic points
    explosion_locations = [
        (3, 2, 1.5),    # Top right
        (-2, -3, 1.0),  # Bottom left
        (0, 4, 2.0),    # Top center
        (-3, 1, 1.2),   # Left side
        (2, -2, 1.8),   # Bottom right
    ]
    
    explosion_timings = [80, 100, 120, 140, 160]
    
    all_objects = []
    
    for i, (location, start_frame) in enumerate(zip(explosion_locations, explosion_timings)):
        print(f"💥 Creating atomic explosion {i+1}/5 at frame {start_frame}")
        
        # Create main explosion
        explosion_objects = create_atomic_explosion(location, start_frame, scale=1.0 + i*0.2)
        all_objects.extend(explosion_objects)
        
        # Create debris
        debris = create_debris_particles(location, start_frame, scale=0.8 + i*0.1)
        all_objects.append(debris)
    
    # Set up rendering
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 512  # High quality
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    
    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Frame range
    scene.frame_start = 1
    scene.frame_end = 240  # 10 seconds at 24fps
    
    # Output settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = '/Users/luismartins/local_repos/3d-ddf/projects/dadosfera/renders/atomic_dadosfera_frame_'
    
    print(f"\n✅ Enhanced Dadosfera with Atomic Explosions created!")
    print(f"   • Metallic chrome text with realistic reflections")
    print(f"   • {len(explosion_locations)} atomic bomb-style explosions")
    print(f"   • 2000+ particles per explosion")
    print(f"   • Realistic fire, smoke, and debris")
    print(f"   • Cinematic camera work")
    print(f"   • Production-quality rendering (512 samples)")
    print(f"\n🎬 Ready for final render!")

if __name__ == "__main__":
    create_enhanced_dadosfera_atomic()
