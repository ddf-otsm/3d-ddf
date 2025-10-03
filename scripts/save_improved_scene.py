#!/usr/bin/env python3
"""Save the scene with improved explosions"""

import bpy

# Save the updated scene
bpy.ops.wm.save_as_mainfile(
    filepath="/Users/luismartins/local_repos/3d-ddf/projects/dadosfera/blender_files/dadosfera_animation_v1_improved_explosions.blend")

print("✅ Scene saved with improved explosions")
print("File: dadosfera_animation_v1_improved_explosions.blend")

# Count explosion objects
explosion_count = 0
for obj in bpy.data.objects:
    if obj.name.startswith('Explosion_'):
        explosion_count += 1

print(f"Total explosion objects: {explosion_count}")
print("Each explosion now has 3 layers: Fire Core + Fire Shell + Smoke Cloud")
print("Much more realistic than simple yellow spheres! 🔥")
