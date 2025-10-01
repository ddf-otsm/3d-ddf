#!/usr/bin/env python3
"""
Dadosfera Animation Renderer
Supports both EEVEE (fast) and CYCLES (photorealistic)
Runs in background mode for maximum performance
"""

import bpy
import sys
import os
import time
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get engine from command line argument or default to CYCLES
ENGINE = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] in ['EEVEE', 'CYCLES', 'BLENDER_EEVEE_NEXT'] else 'CYCLES'

# Output configuration
PROJECT_ROOT = Path("/Users/luismartins/local_repos/3d-ddf")
FRAMES_DIR = PROJECT_ROOT / "projects/dadosfera/renders/frames_cycles" if ENGINE == 'CYCLES' else PROJECT_ROOT / "projects/dadosfera/renders/frames_eevee"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = PROJECT_ROOT / "render_logs" / f"render_{ENGINE.lower()}_{int(time.time())}.log"
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
log(f"DADOSFERA RENDER - {ENGINE} MODE")
log("=" * 70)

# ============================================================================
# SCENE SETUP
# ============================================================================

scene = bpy.context.scene

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

# ============================================================================
# ENGINE-SPECIFIC SETTINGS
# ============================================================================

if ENGINE == 'CYCLES':
    log("\n🎨 CYCLES - Photorealistic Mode")
    log("-" * 70)
    
    # Set Cycles engine
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
            log(f"   GPU: {device.name}")
    
    # Quality settings
    scene.cycles.samples = 128  # Good quality, reasonable speed
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.01
    
    # Performance optimizations for background render
    scene.cycles.use_progressive_refine = False  # Faster for animation
    scene.cycles.tile_size = 2048  # Larger tiles for GPU
    
    log(f"   Samples: {scene.cycles.samples}")
    log(f"   Denoising: OpenImageDenoise")
    log(f"   Adaptive sampling: Enabled")
    log(f"   Expected: ~3-5 sec/frame (GPU)")
    
elif ENGINE in ['EEVEE', 'BLENDER_EEVEE_NEXT']:
    log("\n⚡ EEVEE - Fast Mode")
    log("-" * 70)
    
    # Set EEVEE engine
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    
    # EEVEE settings (already optimized)
    log(f"   GPU: Automatic (Metal)")
    log(f"   Expected: ~1 sec/frame (GPU)")

else:
    log(f"❌ Unknown engine: {ENGINE}")
    sys.exit(1)

# ============================================================================
# COLOR MANAGEMENT
# ============================================================================

scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'
scene.sequencer_colorspace_settings.name = 'sRGB'

log("\n🎨 Color Management:")
log(f"   View Transform: {scene.view_settings.view_transform}")
log(f"   Look: {scene.view_settings.look}")

# ============================================================================
# DISABLE VIEWPORT FOR BACKGROUND RENDERING
# ============================================================================

# Disable viewport updates to save performance
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Disable viewport shading updates
                    space.shading.type = 'SOLID'
                    log("✅ Viewport display disabled for performance")

# ============================================================================
# RENDER HANDLERS
# ============================================================================

# Clear existing handlers
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
    log(f"   Output: {FRAMES_DIR}")
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
    
    # Track frame time for next ETA calculation
    if len(frame_times) > 0:
        frame_times.append(frame_time - frame_times[-1])
    else:
        frame_times.append(2.0)  # Default estimate
    
    # Keep only last 10 frame times for rolling average
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
    log(f"   Frames rendered: {scene.frame_end - scene.frame_start + 1}")
    log(f"   Output: {FRAMES_DIR}")
    log("")
    log("🎬 Next step: Encode frames to video")
    log(f"   Run: bash scripts/encode_frames_to_video.sh")

@bpy.app.handlers.persistent
def on_render_cancel(scene):
    log("")
    log("❌ RENDER CANCELLED")
    log(f"   Stopped at frame: {scene.frame_current}")

bpy.app.handlers.render_pre.append(on_render_init)
bpy.app.handlers.render_post.append(on_frame_post)
bpy.app.handlers.render_complete.append(on_render_complete)
bpy.app.handlers.render_cancel.append(on_render_cancel)

log("✅ Render handlers configured")

# ============================================================================
# START BACKGROUND RENDER
# ============================================================================

log("\n" + "=" * 70)
log("⚙️  STARTING BACKGROUND RENDER (no viewport updates)")
log("=" * 70)
log(f"Log file: {LOG_FILE}")
log("")

# Render animation in background mode
# This prevents viewport updates and maximizes performance
try:
    bpy.ops.render.render('EXEC_DEFAULT', animation=True, write_still=True)
except Exception as e:
    log(f"❌ Render error: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log("\n🎉 Script execution complete!")

