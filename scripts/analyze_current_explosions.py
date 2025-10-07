#!/usr/bin/env python3
"""Analyze current explosion objects"""

import bpy

print("\n" + "=" * 80)
print("CURRENT EXPLOSION ANALYSIS")
print("=" * 80 + "\n")

# Check explosion objects
explosion_count = 0
for obj in bpy.data.objects:
    if obj.name.startswith('Explosion_'):
        explosion_count += 1
        print(f"Explosion {explosion_count}: {obj.name}")
        print(f"  Type: {obj.type}")
        print(f"  Location: ({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f})")
        print(f"  Scale: ({obj.scale.x:.2f}, {obj.scale.y:.2f}, {obj.scale.z:.2f})")

        # Check material
        if obj.data and obj.data.materials:
            mat = obj.data.materials[0]
            print(f"  Material: {mat.name}")
            if mat.use_nodes:
                nodes = mat.node_tree.nodes
                for node in nodes:
                    if node.type == 'EMISSION':
                        color = node.inputs['Color'].default_value
                        strength = node.inputs['Strength'].default_value
                        print(f"    Emission: RGB({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}), Strength: {strength}")
        print()

print(f"\nTotal explosions: {explosion_count}")
print("\nCurrent explosions are just simple UV spheres with emission materials.")
print("They look like glowing balls, not realistic explosions.")
print("\nTo make realistic explosions, we need:")
print("1. Mantaflow smoke simulation")
print("2. Fire/smoke materials")
print("3. Volume rendering")
print("4. Particle systems for debris")
