#!/usr/bin/env python3
"""
Dadosfera Photorealistic Render
Loads the saved scene, applies photorealistic materials, and renders with CYCLES
"""

import bpy
import sys
import os
import time
from pathlib import Path

# ============================================================================
# LOAD SCENE
# ============================================================================
print("="*70)
print("LOADING DADOSFERA SCENE")
print("="*70)

blend_file = "/Users/luismartins/local_repos/3d-ddf/Untitled.blend"
if not os.path.exists(blend_file):
    print(f"❌ ERROR: Scene file not found: {blend_file}")
    sys.exit(1)

# Clear current scene
bpy.ops.wm.read_homefile(use_empty=True)

# Load the dadosfera scene
bpy.ops.wm.open_mainfile(filepath=blend_file)
print(f"✅ Loaded scene: {blend_file}")

scene = bpy.context.scene
print(f"   Objects in scene: {len(scene.objects)}")
for obj in scene.objects:
    print(f"      - {obj.name} ({obj.type})")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get engine from command line argument or default to CYCLES
ENGINE = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] in ['EEVEE', 'CYCLES', 'BLENDER_EEVEE_NEXT'] else 'CYCLES'

# Output configuration
PROJECT_ROOT = Path("/Users/luismartins/local_repos/3d-ddf")
FRAMES_DIR = PROJECT_ROOT / "projects/dadosfera/renders/frames_cycles_photorealistic"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = PROJECT_ROOT / "render_logs" / f"render_photorealistic_{int(time.time())}.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# ============================================================================
# LOGGING
# ============================================================================

def log(message):
    """Write to log file and print"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line, end="")

log("=" * 70)
log(f"DADOSFERA PHOTOREALISTIC RENDER - {ENGINE}")
log("=" * 70)

# ============================================================================
# APPLY PHOTOREALISTIC MATERIALS
# ============================================================================

log("\n🎨 APPLYING PHOTOREALISTIC MATERIALS")
log("-" * 70)

# Switch to Cycles
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
        log(f"   GPU: {device.name}")

# Quality settings
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

log(f"   Samples: {scene.cycles.samples}")
log(f"   Denoising: OpenImageDenoise")

# 1. REALISTIC FLOOR MATERIAL
ground = bpy.data.objects.get('Ground_Plane')
if ground:
    ground.data.materials.clear()
    
    floor_mat = bpy.data.materials.new(name="Polished_Floor")
    floor_mat.use_nodes = True
    nodes = floor_mat.node_tree.nodes
    links = floor_mat.node_tree.links
    
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Polished dark surface
    bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.15, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.15
    bsdf.inputs['Specular IOR Level'].default_value = 0.6
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    ground.data.materials.append(floor_mat)
    
    log("   ✅ Polished floor material")

# 2. CHROME CYAN TEXT
dadosfera = bpy.data.objects.get('Dadosfera_Text')
if dadosfera:
    dadosfera.data.materials.clear()
    
    chrome_mat = bpy.data.materials.new(name="Chrome_Cyan")
    chrome_mat.use_nodes = True
    nodes = chrome_mat.node_tree.nodes
    links = chrome_mat.node_tree.links
    
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Chrome properties
    bsdf.inputs['Base Color'].default_value = (0.7, 0.9, 1.0, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.05
    bsdf.inputs['Specular IOR Level'].default_value = 1.0
    bsdf.inputs['Coat Weight'].default_value = 0.5
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    dadosfera.data.materials.append(chrome_mat)
    
    log("   ✅ Chrome cyan text")

# 3. GLOWING RED EXPLOSIONS
explosion_count = 0
for obj in scene.objects:
    if obj.name.startswith('Explosion_'):
        obj.data.materials.clear()
        
        explosion_mat = bpy.data.materials.new(name=f"Explosion_{explosion_count}")
        explosion_mat.use_nodes = True
        nodes = explosion_mat.node_tree.nodes
        links = explosion_mat.node_tree.links
        
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        
        emission.inputs['Color'].default_value = (1.0, 0.1, 0.0, 1.0)
        emission.inputs['Strength'].default_value = 20.0
        
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        obj.data.materials.append(explosion_mat)
        
        explosion_count += 1

if explosion_count > 0:
    log(f"   ✅ {explosion_count} glowing explosions")

# 4. ENHANCE LIGHTS
for obj in scene.objects:
    if obj.type == 'LIGHT':
        obj.data.energy *= 2.0

log("   ✅ Enhanced lighting\n")

# ============================================================================
# SCENE SETUP
# ============================================================================

# Frame range
scene.frame_start = 1
scene.frame_end = 240

# Resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Output settings
scene.render.filepath = str(FRAMES_DIR / "frame_")
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15

log(f"Output directory: {FRAMES_DIR}")
log(f"Frame range: {scene.frame_start}-{scene.frame_end}")
log(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

# Color management
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'

log(f"\n🎨 Color: {scene.view_settings.view_transform} / {scene.view_settings.look}")

# ============================================================================
# RENDER HANDLERS
# ============================================================================

bpy.app.handlers.render_pre.clear()
bpy.app.handlers.render_post.clear()
bpy.app.handlers.render_complete.clear()
bpy.app.handlers.render_cancel.clear()

render_start_time = None
frame_times = []

@bpy.app.handlers.persistent
def on_render_init(scene):
    global render_start_time
    render_start_time = time.time()
    log(f"\n🚀 RENDER STARTED")
    log(f"   Engine: {ENGINE}")
    log(f"   Frames: {scene.frame_start}-{scene.frame_end}")
    log("")

@bpy.app.handlers.persistent
def on_frame_post(scene):
    global frame_times
    frame_time = time.time()
    
    current = scene.frame_current
    total = scene.frame_end - scene.frame_start + 1
    progress = ((current - scene.frame_start + 1) / total) * 100
    
    # Calculate ETA
    if len(frame_times) > 0:
        avg_time = sum(frame_times) / len(frame_times)
        remaining_frames = scene.frame_end - current
        eta_seconds = remaining_frames * avg_time
        eta_minutes = eta_seconds / 60
        eta_str = f", ETA: {eta_minutes:.1f}min"
    else:
        eta_str = ""
    
    log(f"Frame {current:04d}/{scene.frame_end} ({progress:.1f}%){eta_str}")
    
    # Track frame time
    if len(frame_times) > 0:
        frame_times.append(frame_time - frame_times[-1])
    else:
        frame_times.append(4.0)  # Estimate
    
    if len(frame_times) > 10:
        frame_times.pop(0)

@bpy.app.handlers.persistent
def on_render_complete(scene):
    total_time = time.time() - render_start_time
    minutes = total_time / 60
    avg_frame_time = total_time / (scene.frame_end - scene.frame_start + 1)
    
    log("")
    log("=" * 70)
    log("✅ RENDER COMPLETE!")
    log("=" * 70)
    log(f"   Total time: {minutes:.1f} minutes")
    log(f"   Avg per frame: {avg_frame_time:.2f} seconds")
    log(f"   Output: {FRAMES_DIR}")

@bpy.app.handlers.persistent
def on_render_cancel(scene):
    log(f"\n❌ RENDER CANCELLED at frame {scene.frame_current}")

bpy.app.handlers.render_pre.append(on_render_init)
bpy.app.handlers.render_post.append(on_frame_post)
bpy.app.handlers.render_complete.append(on_render_complete)
bpy.app.handlers.render_cancel.append(on_render_cancel)

# ============================================================================
# START RENDER
# ============================================================================

log("\n" + "=" * 70)
log("⚙️  STARTING PHOTOREALISTIC CYCLES RENDER")
log("=" * 70)
log(f"Log file: {LOG_FILE}\n")

try:
    bpy.ops.render.render('EXEC_DEFAULT', animation=True, write_still=True)
except Exception as e:
    log(f"❌ Render error: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("\n🎉 Render complete!")

