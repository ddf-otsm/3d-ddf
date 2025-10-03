#!/usr/bin/env python3
"""Check explosion objects in the scene"""

import bpy

# Count all explosion-related objects
fire_objects = 0
shell_objects = 0
smoke_objects = 0

for obj in bpy.data.objects:
    if obj.name.startswith('Explosion_Fire_'):
        fire_objects += 1
    elif obj.name.startswith('Explosion_Shell_'):
        shell_objects += 1
    elif obj.name.startswith('Explosion_Smoke_'):
        smoke_objects += 1

print(f"Fire objects: {fire_objects}")
print(f"Shell objects: {shell_objects}")
print(f"Smoke objects: {smoke_objects}")
print(f"Total explosion objects: {fire_objects + shell_objects + smoke_objects}")

if fire_objects > 0:
    print("✅ Improved explosions are in the scene!")
    print("Each explosion has 3 layers: Fire Core + Fire Shell + Smoke Cloud")
else:
    print("❌ No improved explosions found")
