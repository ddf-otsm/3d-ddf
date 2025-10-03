#!/usr/bin/env python3
"""Save the explosion test scene"""

import bpy

# Save the explosion test scene
bpy.ops.wm.save_as_mainfile(
    filepath="/Users/luismartins/local_repos/3d-ddf/projects/explosion-test/blender_files/explosion_test_scene.blend")

print("✅ Explosion test scene saved!")
print("File: explosion_test_scene.blend")
print("Location: projects/explosion-test/blender_files/")
