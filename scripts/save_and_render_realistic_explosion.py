#!/usr/bin/env python3
"""Save and render the realistic explosion scene"""

import bpy

# Save the realistic explosion scene
bpy.ops.wm.save_as_mainfile(
    filepath="${PROJECT_ROOT}/projects/explosion-test/blender_files/realistic_explosion_test.blend")

print("✅ Realistic explosion scene saved!")
print("File: realistic_explosion_test.blend")

# Set up render
scene = bpy.context.scene
scene.frame_set(20)  # Frame with explosion

# Set active camera
camera = bpy.data.objects.get("Test_Camera")
if camera:
    scene.camera = camera
    print("✅ Camera set as active")
else:
    print("❌ No camera found!")

# Set output path
scene.render.filepath = "${PROJECT_ROOT}/projects/explosion-test/renders/realistic_explosion_frame_020"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Render
bpy.ops.render.render(write_still=True)
print("✅ Rendered realistic explosion test frame!")
