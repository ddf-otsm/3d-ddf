import bpy
print('Testing cylinder creation:')
try:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2)
    print("✓ primitive_cylinder_add with radius/depth works")
except Exception as e:
    print(f"✗ primitive_cylinder_add failed: {e}")

try:
    bpy.ops.mesh.primitive_cylinder_add(size=0.2)
    print("✓ primitive_cylinder_add with size works")
except Exception as e:
    print(f"✗ primitive_cylinder_add with size failed: {e}")
