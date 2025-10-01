#!/usr/bin/env python3
"""
Setup photorealistic rendering for dadosfera animation
Switches to Cycles for true photorealism
"""

import bpy
import math

scene = bpy.context.scene

print("🎨 SETTING UP PHOTOREALISTIC RENDER")
print("=" * 60)

# ============================================================================
# 1. SWITCH TO CYCLES FOR PHOTOREALISM
# ============================================================================
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'

# GPU settings
preferences = bpy.context.preferences
cycles_prefs = preferences.addons['cycles'].preferences
cycles_prefs.compute_device_type = 'METAL'
cycles_prefs.get_devices()
for device in cycles_prefs.devices:
    if device.type == 'METAL':
        device.use = True

# Quality settings
scene.cycles.samples = 128  # Good quality
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'

print("✅ Switched to CYCLES with GPU (Metal)")
print(f"   Samples: {scene.cycles.samples}")
print(f"   Denoising: Enabled")

# ============================================================================
# 2. IMPROVE GROUND PLANE - REALISTIC MATERIAL
# ============================================================================
ground = bpy.data.objects.get('Ground_Plane')
if ground:
    # Remove old material
    ground.data.materials.clear()
    
    # Create new realistic floor material
    floor_mat = bpy.data.materials.new(name="Realistic_Floor")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    links = floor_mat.node_tree.links
    
    nodes.clear()
    
    # Create nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Realistic floor properties - polished concrete/marble look
    bsdf.inputs['Base Color'].default_value = (0.15, 0.15, 0.18, 1.0)  # Dark grey
    bsdf.inputs['Metallic'].default_value = 0.0  # Not metallic
    bsdf.inputs['Roughness'].default_value = 0.2  # Slight shine
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    # Add subtle checker via mix for variation
    mix = nodes.new('ShaderNodeMixRGB')
    checker = nodes.new('ShaderNodeTexChecker')
    mapping = nodes.new('ShaderNodeMapping')
    texcoord = nodes.new('ShaderNodeTexCoord')
    
    checker.inputs['Scale'].default_value = 10.0
    checker.inputs['Color1'].default_value = (0.12, 0.12, 0.15, 1.0)
    checker.inputs['Color2'].default_value = (0.18, 0.18, 0.21, 1.0)
    
    mix.blend_type = 'MIX'
    mix.inputs['Fac'].default_value = 0.3  # Subtle variation
    
    # Link nodes
    links.new(texcoord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], mix.inputs['Color1'])
    links.new(bsdf.outputs[0].default_value, mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    ground.data.materials.append(floor_mat)
    print("✅ Created realistic floor material (polished surface)")

# ============================================================================
# 3. IMPROVE DADOSFERA TEXT - CHROME/GLASS HYBRID
# ============================================================================
dadosfera = bpy.data.objects.get('Dadosfera_Text')
if dadosfera:
    dadosfera.data.materials.clear()
    
    # Create stunning chrome material with cyan tint
    chrome_mat = bpy.data.materials.new(name="Chrome_Cyan")
    chrome_mat.use_nodes = True
    nodes = chrome_mat.node_tree.nodes
    links = chrome_mat.node_tree.links
    
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Chrome properties
    bsdf.inputs['Base Color'].default_value = (0.7, 0.9, 1.0, 1.0)  # Cyan tint
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metallic
    bsdf.inputs['Roughness'].default_value = 0.05  # Very shiny
    bsdf.inputs['Specular IOR Level'].default_value = 1.0
    bsdf.inputs['Coat Weight'].default_value = 0.5  # Clear coat for extra shine
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    dadosfera.data.materials.append(chrome_mat)
    print("✅ Created chrome cyan material for text")

# ============================================================================
# 4. IMPROVE LIGHTING - DRAMATIC HDRI + STUDIO LIGHTS
# ============================================================================

# World HDRI environment
world = bpy.data.worlds.get('World')
if not world:
    world = bpy.data.worlds.new("World")
    scene.world = world

world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links

nodes.clear()

output = nodes.new('ShaderNodeOutputWorld')
background = nodes.new('ShaderNodeBackground')

# Gradient background that looks good
gradient = nodes.new('ShaderNodeTexGradient')
color_ramp = nodes.new('ShaderNodeValToRGB')
mapping = nodes.new('ShaderNodeMapping')
texcoord = nodes.new('ShaderNodeTexCoord')

gradient.gradient_type = 'RADIAL'
color_ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.03, 1.0)  # Almost black
color_ramp.color_ramp.elements[1].color = (0.05, 0.08, 0.15, 1.0)  # Dark blue

background.inputs['Strength'].default_value = 0.5

links.new(texcoord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])
links.new(gradient.outputs['Color'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], background.inputs['Color'])
links.new(background.outputs['Background'], output.inputs['Surface'])

print("✅ Created atmospheric world environment")

# Enhance existing lights
for obj in scene.objects:
    if obj.type == 'LIGHT':
        # Make lights stronger for Cycles
        obj.data.energy *= 2.0
        print(f"✅ Enhanced {obj.name}: {obj.data.energy}W")

# ============================================================================
# 5. CAMERA SETTINGS FOR REALISM
# ============================================================================
camera = bpy.data.objects.get('Camera')
if camera:
    camera.data.lens = 50
    camera.data.sensor_width = 36
    # Enable depth of field for cinematic look
    camera.data.dof.use_dof = False  # Disable for now, can enable if needed
    print("✅ Camera configured for photorealism")

# ============================================================================
# 6. RENDER SETTINGS
# ============================================================================
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.film_transparent = False

# Color management for realism
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15

print("✅ Render settings configured")

print("\n" + "=" * 60)
print("🎬 PHOTOREALISTIC SETUP COMPLETE!")
print("=" * 60)
print("\n📊 Summary:")
print("   Engine: Cycles (GPU - Metal)")
print("   Samples: 128 with AI denoising")
print("   Floor: Realistic polished surface")
print("   Text: Chrome cyan metallic")
print("   Lighting: Enhanced studio setup")
print("   Color: Filmic High Contrast")
print("\n⏱️  Render time: ~3-5 seconds per frame")
print("   Total: ~12-20 minutes for 240 frames")
print("\n🚀 Ready to render photorealistic animation!")

