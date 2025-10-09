#!/usr/bin/env python3
"""
Production Render Script - Multi-Project Support

Renders any project's animation with Cycles engine and Metal GPU optimization.
Automatically exports with timestamp-first naming convention.

Supported Projects:
  - dadosfera: Main 3D logo animation project (10s, 240 frames)
  - explosion-test: Explosion effects validation project (variable duration)

Usage:
  # Preview render (quick quality check)
  python3 scripts/render_production.py dadosfera --quality preview --frames 1 48

  # Full production render
  python3 scripts/render_production.py dadosfera --quality production

  # Custom frame range
  python3 scripts/render_production.py explosion-test --quality draft --frames 1 120

Quality Presets:
  - draft: 64 samples @ 720p (fastest, ~20-30 min full render)
  - preview: 128 samples @ 1080p (medium, ~40-60 min full render)  
  - production: 256 samples @ 1080p (high quality, ~60-90 min full render)
  - final: 512 samples @ 1080p (highest quality, ~120-180 min full render)

Features:
  - Metal GPU optimization (M3 Max)
  - Cycles rendering engine
  - AI denoising
  - Automatic video encoding (FFmpeg)
  - JSON metadata tracking
  - Timestamp-first naming (YYYYMMDD_HHMM_description)
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json
import time

# Project configurations
PROJECTS = {
    'dadosfera': {
        'blend_file': 'projects/dadosfera/blender_files/active/dadosfera_metallic_materials.blend',
        'renders_dir': 'projects/dadosfera/renders',
        'exports_dir': 'projects/dadosfera/exports',
        'default_frames': (1, 240),
        'fps': 24,
        'description': 'Main 3D logo animation with metallic materials'
    },
    'explosion-test': {
        'blend_file': 'projects/explosion-test/blender_files/archived/geometry_tests/hybrid_quick_test.blend',
        'renders_dir': 'projects/explosion-test/renders',
        'exports_dir': 'projects/explosion-test/exports',
        'default_frames': (1, 120),
        'fps': 24,
        'description': 'Explosion effects validation and testing'
    }
}

# Quality presets
QUALITY_PRESETS = {
    'draft': {
        'samples': 64,
        'resolution_x': 1280,
        'resolution_y': 720,
        'denoising': True,
        'description': 'Draft quality for quick preview'
    },
    'preview': {
        'samples': 128,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'denoising': True,
        'description': 'Preview quality for validation'
    },
    'production': {
        'samples': 256,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'denoising': True,
        'description': 'Production quality for final output'
    },
    'final': {
        'samples': 512,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'denoising': True,
        'description': 'Maximum quality for final delivery'
    }
}


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).resolve().parent.parent


def get_blender_executable():
    """Get the Blender executable path."""
    # macOS default locations
    possible_paths = [
        Path("/Applications/Blender.app/Contents/MacOS/Blender"),
        Path("${BLENDER}/Contents/MacOS/Blender"),
        Path("~/Applications/Blender.app/Contents/MacOS/Blender").expanduser()
    ]

    for blender_path in possible_paths:
        if blender_path.exists():
            return str(blender_path)

    # Check PATH
    result = subprocess.run(['which', 'blender'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()

    raise FileNotFoundError("Blender executable not found. Install Blender or add to PATH.")


def create_render_script(quality_preset: dict, output_path: str, frame_start: int, frame_end: int, project_name: str):
    """
    Create Blender Python script for rendering with Metal GPU optimization.
    
    Args:
        quality_preset: Quality settings dict
        output_path: Directory for rendered frames
        frame_start: First frame to render
        frame_end: Last frame to render  
        project_name: Name of the project being rendered
    
    Returns:
        str: Path to temporary render script
    """
    script_content = f'''
import bpy
import time

# Get scene
scene = bpy.context.scene

# Configure Cycles with Metal GPU
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = {quality_preset['samples']}

# Enable Metal GPU on macOS
preferences = bpy.context.preferences
cycles_preferences = preferences.addons['cycles'].preferences
cycles_preferences.compute_device_type = 'METAL'

# Get Metal devices
cycles_preferences.get_devices()
for device in cycles_preferences.devices:
    if device.type == 'METAL':
        device.use = True
        print(f"✓ Enabled Metal GPU: {{device.name}}")

# Resolution
scene.render.resolution_x = {quality_preset['resolution_x']}
scene.render.resolution_y = {quality_preset['resolution_y']}
scene.render.resolution_percentage = 100

# Denoising
if {quality_preset['denoising']}:
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# Output settings
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '{output_path}/frame_'
scene.render.use_file_extension = True

# Frame range
scene.frame_start = {frame_start}
scene.frame_end = {frame_end}

# Print settings
print("\\n" + "=" * 70)
print("🎬 PRODUCTION RENDER: {project_name.upper()}")
print("=" * 70)
print(f"Engine: CYCLES (Metal GPU)")
print(f"Samples: {quality_preset['samples']}")
print(f"Resolution: {quality_preset['resolution_x']}x{quality_preset['resolution_y']}")
print(f"Frames: {{scene.frame_start}}-{{scene.frame_end}} ({{scene.frame_end - scene.frame_start + 1}} frames)")
print(f"FPS: {{scene.render.fps}}")
print(f"Duration: {{(scene.frame_end - scene.frame_start + 1) / scene.render.fps:.2f}}s")
print(f"Denoising: {{scene.cycles.use_denoising}}")
print(f"Output: {output_path}")
print("=" * 70 + "\\n")

# Render
start_time = time.time()
bpy.ops.render.render(animation=True)
elapsed = time.time() - start_time

print("\\n" + "=" * 70)
print(f"✅ Render complete!")
print(f"   Total time: {{elapsed / 60:.1f}} minutes")
print(f"   Average: {{elapsed / (scene.frame_end - scene.frame_start + 1):.1f}}s per frame")
print("=" * 70 + "\\n")
'''
    
    # Write to temp file
    project_root = get_project_root()
    temp_script = project_root / 'scripts' / f'_temp_{project_name}_render.py'
    temp_script.write_text(script_content)
    
    return str(temp_script)


def encode_video(frames_dir: Path, output_video: Path, fps: int = 24):
    """
    Encode rendered frames to MP4 using FFmpeg.
    
    Args:
        frames_dir: Directory containing PNG frames
        output_video: Output MP4 file path
        fps: Frames per second (default: 24)
    
    Returns:
        bool: True if encoding succeeded, False otherwise
    """
    print(f"\n🎬 Encoding video: {output_video.name}")
    
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output
        '-framerate', str(fps),
        '-i', str(frames_dir / 'frame_%04d.png'),
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',  # High quality (0-51, lower is better)
        '-pix_fmt', 'yuv420p',
        str(output_video)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Video encoded: {output_video}")
        
        # Get file size
        size_mb = output_video.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.1f} MB")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Video encoding failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg not found. Install with: brew install ffmpeg")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Production render script with multi-project support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview render for dadosfera (2 seconds)
  %(prog)s dadosfera --quality preview --frames 1 48

  # Full production render for explosion-test
  %(prog)s explosion-test --quality production

  # Draft quality, custom description
  %(prog)s dadosfera --quality draft --description "test_v2"
        """
    )
    
    parser.add_argument('project', choices=PROJECTS.keys(),
                       help='Project to render')
    parser.add_argument('--quality', choices=QUALITY_PRESETS.keys(), default='production',
                       help='Quality preset (default: production)')
    parser.add_argument('--frames', type=int, nargs=2, metavar=('START', 'END'),
                       help='Frame range (default: project-specific)')
    parser.add_argument('--no-encode', action='store_true',
                       help='Skip video encoding (render frames only)')
    parser.add_argument('--description', type=str,
                       help='Custom description for output filename (auto-generated if not provided)')
    args = parser.parse_args()
    
    project_root = get_project_root()
    project_config = PROJECTS[args.project]
    
    # Get blend file
    blend_file = project_root / project_config['blend_file']
    if not blend_file.exists():
        print(f"❌ Blend file not found: {blend_file}")
        print(f"   Expected: {project_config['blend_file']}")
        return 1
    
    # Pre-render validation: Check scene for test elements
    print("🔍 Running pre-render validation...")
    validation_script = project_root / 'scripts/clean_production_scene.py'
    blender_exe = get_blender_executable()
    validation_cmd = [
        blender_exe,
        str(blend_file),
        '--background',
        '--python', str(validation_script),
        '--',
        '--dry-run'
    ]
    
    validation_result = subprocess.run(validation_cmd, capture_output=True, text=True)
    
    if validation_result.returncode != 0:
        print("⚠️  Scene validation warnings detected:")
        print(validation_result.stdout)
        print("\n❓ Scene has issues but may still be renderable.")
        print("   Consider running: blender <scene> --background --python scripts/clean_production_scene.py -- --output <scene>")
    else:
        print("✅ Scene validation passed")
    
    # Get quality preset
    quality = QUALITY_PRESETS[args.quality]
    
    # Determine frame range
    frame_start, frame_end = args.frames if args.frames else project_config['default_frames']
    frame_count = frame_end - frame_start + 1
    duration_seconds = frame_count / project_config['fps']
    
    # Generate description
    if args.description:
        description = args.description
    else:
        description = f"{args.project}_{args.quality}"
    
    # Create output directory with timestamp-first naming
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_dir = project_root / project_config['renders_dir'] / f'{timestamp}_production_{description}'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 70)
    print(f"🎬 PRODUCTION RENDER: {args.project.upper()}")
    print("=" * 70)
    print(f"Project: {args.project}")
    print(f"Description: {project_config['description']}")
    print(f"Blend file: {blend_file.name}")
    print(f"Quality: {args.quality} ({quality['description']})")
    print(f"Samples: {quality['samples']}")
    print(f"Resolution: {quality['resolution_x']}x{quality['resolution_y']}")
    print(f"Frames: {frame_start}-{frame_end} ({frame_count} frames)")
    print(f"Duration: {duration_seconds:.2f}s @ {project_config['fps']} FPS")
    print(f"Output: {output_dir}")
    print("=" * 70 + "\n")
    
    # Estimate render time
    est_per_frame = {
        'draft': 5,
        'preview': 10,
        'production': 20,
        'final': 45
    }
    estimated_minutes = (frame_count * est_per_frame[args.quality]) / 60
    print(f"⏱️  Estimated render time: {estimated_minutes:.1f} minutes")
    print(f"   (Based on ~{est_per_frame[args.quality]}s per frame average)\n")
    
    # Save render metadata
    metadata = {
        'timestamp': timestamp,
        'project': args.project,
        'project_description': project_config['description'],
        'blend_file': str(blend_file),
        'quality_preset': args.quality,
        'quality_settings': quality,
        'frame_range': [frame_start, frame_end],
        'frame_count': frame_count,
        'duration_seconds': duration_seconds,
        'fps': project_config['fps'],
        'output_directory': str(output_dir),
        'render_start': datetime.now().isoformat()
    }
    
    metadata_file = output_dir / 'render_metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Create render script
    render_script = create_render_script(quality, str(output_dir), frame_start, frame_end, args.project)
    
    # Get Blender executable
    try:
        blender = get_blender_executable()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    
    # Build command
    cmd = [
        blender,
        str(blend_file),
        '--background',
        '--python', render_script
    ]
    
    # Execute render
    print(f"🚀 Starting Blender render...\n")
    start_time = time.time()
    
    try:
        subprocess.run(cmd, check=True)
        elapsed = time.time() - start_time
        
        # Update metadata
        metadata['render_end'] = datetime.now().isoformat()
        metadata['render_duration_seconds'] = elapsed
        metadata['render_duration_minutes'] = elapsed / 60
        metadata['average_seconds_per_frame'] = elapsed / frame_count
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Render complete! ({elapsed / 60:.1f} minutes)")
        print(f"   Average: {elapsed / frame_count:.1f}s per frame")
        
        # Encode video
        if not args.no_encode:
            exports_dir = project_root / project_config['exports_dir']
            exports_dir.mkdir(parents=True, exist_ok=True)
            
            # Project taxonomy naming: project_version_date_quality_type
            # Use 'alpha' as default version for new renders
            version = "alpha"
            type_suffix = args.description if args.description else args.quality
            video_name = f"{args.project}_{version}_{timestamp.split('_')[0]}_{quality['resolution_y']}p_{type_suffix}.mp4"
            output_video = exports_dir / video_name
            
            if encode_video(output_dir, output_video, project_config['fps']):
                metadata['output_video'] = str(output_video)
                metadata['video_size_mb'] = output_video.stat().st_size / (1024 * 1024)
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ PRODUCTION RENDER COMPLETE!")
        print("=" * 70)
        print(f"Project: {args.project}")
        print(f"Frames: {output_dir}")
        if not args.no_encode and 'output_video' in metadata:
            print(f"Video: {Path(metadata['output_video']).name}")
            print(f"Size: {metadata['video_size_mb']:.1f} MB")
        print("=" * 70 + "\n")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Render failed: {e}")
        return 1
    except KeyboardInterrupt:
        print(f"\n⚠️  Render interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
