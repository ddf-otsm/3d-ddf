#!/usr/bin/env python3
"""Test render a few frames of the explosion test scene"""

import bpy

# Set up render settings
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 100

# Set active camera
camera = bpy.data.objects.get("Test_Camera")
if camera:
    scene.camera = camera
    print("✅ Camera set as active")
else:
    print("❌ No camera found!")

# Set output path
scene.render.filepath = "/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/renders/explosion_test_"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Render a few key frames
test_frames = [10, 20, 30, 40, 50, 60, 70, 80, 90]

print("🎬 Rendering explosion test frames...")
print(f"Test frames: {test_frames}")

for frame in test_frames:
    scene.frame_set(frame)
    scene.render.filepath = f"/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/renders/explosion_test_frame_{
        frame:03d}"
    bpy.ops.render.render(write_still=True)
    print(f"   ✅ Rendered frame {frame}")

print(f"\n✅ Rendered {len(test_frames)} test frames")
print("Check: projects/explosion-test/renders/")
print("Review the explosions and approve if they look good!")
