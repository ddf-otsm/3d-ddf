#!/usr/bin/env python3
"""
Proof of Concept: Text to 3D Conversion

This script demonstrates basic text-to-3D conversion using Blender.
Run with: blender --background --python poc_text_to_3d.py

Requirements:
- Blender 4.2+
- Python dependencies installed
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Main POC function."""
    print("Logo to 3D Service - Proof of Concept")
    print("=" * 50)

    try:
        # Import Blender modules
        import bpy

        # Clear scene
        bpy.ops.wm.read_homefile(use_empty=True)

        # Create a simple text object
        bpy.ops.object.text_add(location=(0, 0, 0))
        text_obj = bpy.context.active_object

        # Set text properties
        text_obj.data.body = "TEST"
        text_obj.data.size = 1.0
        text_obj.data.font = bpy.data.fonts.load("//fonts/LiberationSans-Regular.ttf")  # Placeholder

        # Convert text to mesh
        bpy.ops.object.convert(target='MESH')

        # Add extrusion
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, 0.1)}
        )
        bpy.ops.object.mode_set(mode='OBJECT')

        # Export to OBJ
        output_path = Path("./data/temp/test_output.obj")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        bpy.ops.export_scene.obj(
            filepath=str(output_path),
            use_selection=True,
            use_materials=False,
            use_triangles=False,
            use_uvs=False,
            use_normals=True
        )

        print(f"✅ Success! Exported to: {output_path}")
        print(f"File size: {output_path.stat().st_size} bytes")

        # Clean up
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this script with Blender:")
        print("blender --background --python poc_text_to_3d.py")
        return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("🎉 POC completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

