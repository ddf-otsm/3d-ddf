#!/usr/bin/env python3
"""
Explosion rendering script for 3D-DDF.
Integrates with render_service.py for batch rendering and auto-encoding.
"""

from scripts.explosions.presets import get_preset_config
from scripts.explosions.config import ExplosionConfig
import sys
import argparse
from pathlib import Path
import json

# Conditional import for bpy (only if in Blender)
try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False
    bpy = None

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock render_main if not available
try:
    from scripts.render_service import main as render_main
except ImportError:
    def render_main(**kwargs):
        print("Mock render (Blender not available)")
        return True


def load_config(config_path: str) -> dict:
    """Load explosion config from JSON."""
    with open(config_path, 'r') as f:
        return json.load(f)


def render_explosions(
        blend_file: str,
        output_dir: str,
        config_path: str = None,
        **render_args):
    """
    Render explosion scene with config.

    Args:
        blend_file: Path to .blend file
        output_dir: Render output directory
        config_path: Optional JSON config
        render_args: Passed to render_service
    """
    print(f"🎬 Rendering explosions from {blend_file}")

    if config_path:
        config_data = load_config(config_path)
        # Apply config if needed (e.g., re-integrate)
        print(f"📋 Loaded config: {config_path}")

    # Use render_service for actual rendering
    # Note: actual call needs adjustment for subprocess
    render_args['blend_file'] = blend_file
    render_args['output_dir'] = output_dir
    render_args['engine'] = render_args.get('engine', 'CYCLES')
    render_args['quality'] = render_args.get('quality', 'production')

    # Call render_service (simulate or actual)
    if IN_BLENDER:
        # In Blender: run as script
        render_main(**render_args)
    else:
        # Outside: subprocess call
        from subprocess import run
        blender_cmd = [
            "${BLENDER}/Contents/MacOS/Blender",
            blend_file,
            "--background",
            "-o", f"{output_dir}/####",
            "-f", render_args.get('frames', '1-240'),
            "-P", "scripts/render_service.py",
            "--",
            f"--engine {render_args['engine']}",
            f"--quality {render_args['quality']}",
            f"--materials photorealistic"
        ]
        result = run(blender_cmd, check=True)
        if result.returncode == 0:
            print("✅ Render completed via subprocess")

    # Auto-encode video
    encode_frames_to_video(
        output_dir, f"{output_dir}/../exports/{Path(blend_file).stem}_explosions.mp4")


def encode_frames_to_video(frames_dir: str, output_video: str):
    """Encode PNG frames to MP4 using ffmpeg."""
    from subprocess import run
    ffmpeg_cmd = [
        "ffmpeg",
        "-framerate", "24",
        "-i", f"{frames_dir}/%04d.png",
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    result = run(ffmpeg_cmd, check=True)
    print(f"✅ Encoded video: {output_video}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render explosions")
    parser.add_argument("blend_file", help="Path to .blend file")
    parser.add_argument(
        "--output",
        default="renders/explosions",
        help="Output directory")
    parser.add_argument("--config", help="JSON config path")
    parser.add_argument("--frames", default="1-240", help="Frame range")
    parser.add_argument("--engine", default="CYCLES", choices=["CYCLES", "EEVEE"])
    parser.add_argument(
        "--quality",
        default="production",
        choices=[
            "draft",
            "preview",
            "production",
            "final"])

    args = parser.parse_args()

    render_explosions(
        args.blend_file,
        args.output,
        args.config,
        frames=args.frames,
        engine=args.engine,
        quality=args.quality
    )
