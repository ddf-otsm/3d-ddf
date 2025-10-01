#!/usr/bin/env python3
"""
Apply Photorealistic Materials and Render
Called by render_photorealistic.sh with the scene already loaded
"""

import bpy
import sys
import time
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get engine from command line
ENGINE = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] in ['EEVEE', 'CYCLES', 'BLENDER_EEVEE_NEXT'] else 'CYCLES'

PROJECT_ROOT = Path("/Users/luismartins/local_repos/3d-ddf")
FRAMES_DIR = PROJECT_ROOT / "projects/dadosfera/renders/frames_cycles_photorealistic"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene

print("\n" + "="*70)
print(f"DADOSFERA PHOTOREALISTIC RENDER - {ENGINE}")
print("="*70)
print(f"\n📋 Scene loaded: {bpy.data.filepath}")
print(f"   Objects: {len(scene.objects)}")
for obj in list(scene.objects)[:10]:  # Show first 10
    print(f"      - {obj.name} ({obj.type})")
if len(scene.objects) > 10:
    print(f"      ... and {len(scene.objects) - 10} more")

# ============================================================================
# APPLY PHOTOREALISTIC MATERIALS
# ============================================================================

print("\n🎨 APPLYING PHOTOREALISTIC MATERIALS")
print("-"*70)

# Switch to CYCLES
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'

# GPU configuration
preferences = bpy.context.preferences
cycles_prefs = preferences.addons['cycles'].preferences
cycles_prefs.compute_device_type = 'METAL'
cycles_prefs.get_devices()

gpu_count = 0
for device in cycles_prefs.devices:
    if device.type == 'METAL':
        device.use = True
        gpu_count += 1
        print(f"   ✅ GPU: {device.name}")

if gpu_count == 0:
    print("   ⚠️  WARNING: No Metal GPU found, will use CPU")

# Quality settings for photorealism
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01
scene.cycles.use_progressive_refine = False
scene.cycles.tile_size = 2048

print(f"   Samples: {scene.cycles.samples}")
print(f"   Denoising: OpenImageDenoise")
print(f"   Adaptive sampling: Enabled")

# ============================================================================
# MATERIAL APPLICATION
# ============================================================================

material_count = {'floor': 0, 'text': 0, 'explosions': 0}

# 1. POLISHED FLOOR
ground = bpy.data.objects.get('Ground_Plane')
if ground and ground.data:
    # Clear existing materials
    ground.data.materials.clear()
    
    # Create polished floor material
    floor_mat = bpy.data.materials.new(name="Polished_Floor_Photorealistic")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    links = floor_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Dark polished floor with subtle reflections
    bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.15, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.15  # Shiny
    bsdf.inputs['Specular IOR Level'].default_value = 0.6
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    ground.data.materials.append(floor_mat)
    material_count['floor'] = 1
    print("   ✅ Polished floor material")

# 2. CHROME CYAN TEXT
dadosfera = bpy.data.objects.get('Dadosfera_Text')
if dadosfera and dadosfera.data:
    dadosfera.data.materials.clear()
    
    chrome_mat = bpy.data.materials.new(name="Chrome_Cyan_Photorealistic")
    chrome_mat.use_nodes = True
    nodes = chrome_mat.node_tree.nodes
    links = chrome_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    # Chrome metal with cyan tint
    bsdf.inputs['Base Color'].default_value = (0.7, 0.9, 1.0, 1.0)  # Cyan
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metal
    bsdf.inputs['Roughness'].default_value = 0.05  # Very shiny
    bsdf.inputs['Specular IOR Level'].default_value = 1.0
    bsdf.inputs['Coat Weight'].default_value = 0.5  # Clear coat
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    dadosfera.data.materials.append(chrome_mat)
    material_count['text'] = 1
    print("   ✅ Chrome cyan text")

# 3. GLOWING EXPLOSIONS
for obj in scene.objects:
    if obj.name.startswith('Explosion_') and obj.type == 'MESH' and obj.data:
        obj.data.materials.clear()
        
        explosion_mat = bpy.data.materials.new(name=f"Explosion_Glow_{material_count['explosions']}")
        explosion_mat.use_nodes = True
        nodes = explosion_mat.node_tree.nodes
        links = explosion_mat.node_tree.links
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (0, 0)
        
        # Bright red-orange glow
        emission.inputs['Color'].default_value = (1.0, 0.15, 0.0, 1.0)
        emission.inputs['Strength'].default_value = 30.0  # Very bright
        
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        obj.data.materials.append(explosion_mat)
        material_count['explosions'] += 1

if material_count['explosions'] > 0:
    print(f"   ✅ {material_count['explosions']} glowing explosions")

# 4. ENHANCE LIGHTING
light_count = 0
for obj in scene.objects:
    if obj.type == 'LIGHT':
        obj.data.energy *= 2.0
        light_count += 1

if light_count > 0:
    print(f"   ✅ Enhanced {light_count} lights")

print(f"\n✅ Materials applied:")
print(f"   - Floor: {material_count['floor']}")
print(f"   - Text: {material_count['text']}")
print(f"   - Explosions: {material_count['explosions']}")

# ============================================================================
# RENDER SETTINGS
# ============================================================================

print("\n⚙️  RENDER SETTINGS")
print("-"*70)

# Frame range
scene.frame_start = 1
scene.frame_end = 240

# Resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Output
scene.render.filepath = str(FRAMES_DIR / "frame_")
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15

# Color management
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

print(f"   Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
print(f"   Frames: {scene.frame_start}-{scene.frame_end}")
print(f"   Color: {scene.view_settings.view_transform} / {scene.view_settings.look}")
print(f"   Output: {FRAMES_DIR}")

# ============================================================================
# RENDER PROGRESS TRACKING
# ============================================================================

render_start_time = None
frame_times = []

@bpy.app.handlers.persistent
def on_render_init(dummy):
    global render_start_time
    render_start_time = time.time()
    print("\n" + "="*70)
    print("🚀 RENDER STARTED")
    print("="*70)
    print("")

@bpy.app.handlers.persistent
def on_frame_post(dummy):
    global frame_times
    
    current = scene.frame_current
    total = scene.frame_end - scene.frame_start + 1
    progress = ((current - scene.frame_start + 1) / total) * 100
    
    # Calculate ETA
    if len(frame_times) > 0:
        avg_time = sum(frame_times[-10:]) / len(frame_times[-10:])
        remaining = scene.frame_end - current
        eta_sec = remaining * avg_time
        eta_min = eta_sec / 60
        eta_str = f", ETA: {eta_min:.1f}min ({avg_time:.1f}s/frame)"
    else:
        eta_str = ""
    
    print(f"✅ Frame {current:04d}/{scene.frame_end} ({progress:.1f}%){eta_str}")
    
    # Track frame time
    if render_start_time:
        frame_times.append(time.time() - render_start_time)

@bpy.app.handlers.persistent
def on_render_complete(dummy):
    if render_start_time:
        total_time = time.time() - render_start_time
        minutes = total_time / 60
        avg_time = total_time / (scene.frame_end - scene.frame_start + 1)
        
        print("\n" + "="*70)
        print("✅ RENDER COMPLETE!")
        print("="*70)
        print(f"   Total time: {minutes:.1f} minutes ({total_time:.0f} seconds)")
        print(f"   Avg per frame: {avg_time:.2f} seconds")
        print(f"   Frames: {scene.frame_end - scene.frame_start + 1}")
        print(f"   Output: {FRAMES_DIR}")
        print("")

@bpy.app.handlers.persistent
def on_render_cancel(dummy):
    print(f"\n❌ RENDER CANCELLED at frame {scene.frame_current}")

# Clear and set handlers
bpy.app.handlers.render_pre.clear()
bpy.app.handlers.render_post.clear()
bpy.app.handlers.render_complete.clear()
bpy.app.handlers.render_cancel.clear()

bpy.app.handlers.render_pre.append(on_render_init)
bpy.app.handlers.render_post.append(on_frame_post)
bpy.app.handlers.render_complete.append(on_render_complete)
bpy.app.handlers.render_cancel.append(on_render_cancel)

# ============================================================================
# START RENDER
# ============================================================================

print("\n" + "="*70)
print("▶️  STARTING BACKGROUND RENDER")
print("="*70)
print("")

try:
    bpy.ops.render.render('EXEC_DEFAULT', animation=True, write_still=True)
except Exception as e:
    print(f"\n❌ RENDER ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 Render script execution complete!")

