
import bpy
import time

# Get scene
scene = bpy.context.scene

# Configure Cycles with Metal GPU
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = 512

# Enable Metal GPU on macOS
preferences = bpy.context.preferences
cycles_preferences = preferences.addons['cycles'].preferences
cycles_preferences.compute_device_type = 'METAL'

# Get Metal devices
cycles_preferences.get_devices()
for device in cycles_preferences.devices:
    if device.type == 'METAL':
        device.use = True
        print(f"✓ Enabled Metal GPU: {device.name}")

# Resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Denoising
if True:
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Output settings
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/Users/luismartins/local_repos/3d-ddf/projects/dadosfera/renders/20251009_1008_production_atomic_metallic/frame_'
scene.render.use_file_extension = True

# Frame range
scene.frame_start = 1
scene.frame_end = 240

# Print settings
print("\n" + "=" * 70)
print("🎬 PRODUCTION RENDER: DADOSFERA")
print("=" * 70)
print(f"Engine: CYCLES (Metal GPU)")
print(f"Samples: 512")
print(f"Resolution: 1920x1080")
print(f"Frames: {scene.frame_start}-{scene.frame_end} ({scene.frame_end - scene.frame_start + 1} frames)")
print(f"FPS: {scene.render.fps}")
print(f"Duration: {(scene.frame_end - scene.frame_start + 1) / scene.render.fps:.2f}s")
print(f"Denoising: {scene.cycles.use_denoising}")
print(f"Output: /Users/luismartins/local_repos/3d-ddf/projects/dadosfera/renders/20251009_1008_production_atomic_metallic")
print("=" * 70 + "\n")

# Render
start_time = time.time()
bpy.ops.render.render(animation=True)
elapsed = time.time() - start_time

print("\n" + "=" * 70)
print(f"✅ Render complete!")
print(f"   Total time: {elapsed / 60:.1f} minutes")
print(f"   Average: {elapsed / (scene.frame_end - scene.frame_start + 1):.1f}s per frame")
print("=" * 70 + "\n")
