#!/usr/bin/env python3
"""
Demo script: Complete text-to-3D conversion pipeline

This script demonstrates the complete pipeline from text input to 3D output.
Run with: python scripts/demo_text_to_3d.py

Note: Requires Blender to be installed for actual 3D processing.
"""

import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from core.config import settings
from core.blender_server import get_blender_server
from text_processor.renderer import get_text_renderer


def main():
    """Demonstrate the complete text-to-3D pipeline."""
    print("🚀 Logo to 3D Service - Text to 3D Demo")
    print("=" * 50)

    try:
        # Initialize components
        print("📋 Initializing components...")
        text_renderer = get_text_renderer()
        blender_server = get_blender_server()

        print(f"✅ Text renderer ready")
        print(f"✅ Blender server ready (temp dir: {blender_server.temp_dir})")

        # Step 1: Render text to SVG
        print("\n📝 Step 1: Rendering text to SVG...")
        text_input = "HELLO\nWORLD"
        font_name = settings.default_font
        font_size = 1.0

        print(f"   Text: {repr(text_input)}")
        print(f"   Font: {font_name}")
        print(f"   Size: {font_size}")

        svg_content = text_renderer.render_text_to_svg(
            text_input,
            font_name=font_name,
            font_size=font_size
        )

        print(f"   Generated SVG ({len(svg_content)} characters)")

        # Save SVG
        svg_path = blender_server.temp_dir / "demo_text.svg"
        with open(svg_path, 'w') as f:
            f.write(svg_content)

        print(f"   Saved SVG to: {svg_path}")

        # Step 2: Create Blender operations
        print("\n🔧 Step 2: Creating Blender operations...")

        operations = [
            {
                "type": "import_svg",
                "params": {"svg_path": str(svg_path)}
            },
            {
                "type": "extrude_mesh",
                "params": {
                    "depth": 0.1,
                    "bevel_depth": 0.01,
                    "resolution": 12
                }
            },
            {
                "type": "apply_material",
                "params": {
                    "name": "DemoMaterial",
                    "base_color": [0.2, 0.6, 1.0, 1.0]  # Blue color
                }
            },
            {
                "type": "setup_lighting",
                "params": {}
            }
        ]

        # Generate outputs in multiple formats
        output_base = blender_server.temp_dir / "demo_output"
        formats = ["obj", "gltf", "fbx"]

        for fmt in formats:
            operations.append({
                "type": "export_mesh",
                "params": {
                    "format": fmt,
                    "output_path": f"{output_base}.{fmt}"
                }
            })

        print(f"   Created {len(operations)} operations")
        print(f"   Will export to: {', '.join(formats)}")

        # Step 3: Generate and execute Blender script
        print("\n🎬 Step 3: Generating Blender script...")

        script_path = blender_server.create_blender_script(operations)
        print(f"   Script generated: {script_path}")

        # Show script preview
        with open(script_path) as f:
            lines = f.readlines()[:20]  # First 20 lines
            print("   Script preview:")
            for i, line in enumerate(lines, 1):
                print("2d")
            if len(lines) == 20:
                print("      ... (truncated)")

        # Step 4: Execute in Blender (if available)
        print("\n🏃 Step 4: Executing in Blender...")

        if blender_server.is_blender_available():
            print("   Blender is available, processing...")

            try:
                result = blender_server.process_request(script_path, timeout=60)

                if result["success"]:
                    print("   ✅ Processing completed successfully!")

                    # Check for output files
                    print("   📁 Output files:")
                    for fmt in formats:
                        output_file = Path(f"{output_base}.{fmt}")
                        if output_file.exists():
                            size = output_file.stat().st_size
                            print(f"      ✅ {output_file.name} ({size} bytes)")
                        else:
                            print(f"      ❌ {output_file.name} (not found)")

                else:
                    print(f"   ❌ Processing failed: {result.get('stderr', 'Unknown error')}")
                    return 1

            except Exception as e:
                print(f"   ❌ Processing error: {e}")
                return 1

        else:
            print("   ⚠️  Blender not available - skipping actual processing")
            print(f"   📄 Script would be executed: {script_path}")
            print("   💡 To run with actual Blender, install Blender and ensure it's in PATH")

        # Step 5: Summary
        print("\n🎉 Demo completed!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"   • Text input: {repr(text_input)}")
        print(f"   • Font: {font_name}")
        print(f"   • Generated SVG: {len(svg_content)} characters")
        print(f"   • Blender operations: {len(operations)}")
        print(f"   • Output formats: {', '.join(formats)}")
        print(f"   • Temp directory: {blender_server.temp_dir}")

        if blender_server.is_blender_available():
            blender_version = blender_server.get_blender_version()
            print(f"   • Blender version: {blender_version}")
        else:
            print("   • Blender: Not available")

        print("\n💡 Next steps:")
        print("   1. Install Blender (if not already installed)")
        print("   2. Run: blender --background --python scripts/poc_text_to_3d.py")
        print("   3. Integrate with Dadosfera logo processing")
        print("   4. Add REST API endpoints")

        # Cleanup
        blender_server.cleanup()

        return 0

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

