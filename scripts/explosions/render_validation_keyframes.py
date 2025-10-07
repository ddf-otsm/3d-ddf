#!/usr/bin/env python3
"""
Render validation keyframes for explosion integration testing.

This script renders 10 strategic keyframes to validate:
- Visual quality across the explosion sequence
- Performance metrics (render time, memory)
- Integration with main project scenes

Based on projects/explosion-test/VALIDATION_CHECKLIST.md
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Validation keyframes (as defined in VALIDATION_CHECKLIST.md)
VALIDATION_FRAMES = [1, 50, 75, 110, 140, 170, 200, 230, 270, 300]

# Quality settings for validation (medium quality)
VALIDATION_QUALITY = {
    'samples': 256,
    'resolution_x': 1920,
    'resolution_y': 1080,
    'engine': 'CYCLES',
    'device': 'GPU'
}


def get_blender_executable() -> str:
    """Get Blender executable path from environment or default."""
    blender_paths = [
        os.environ.get('BLENDER'),
        os.environ.get('BLENDER_EXECUTABLE'),
        '${BLENDER}/Contents/MacOS/Blender',  # macOS default
        '/usr/bin/blender',  # Linux default
        'blender'  # In PATH
    ]
    
    for path in blender_paths:
        if path and Path(path).exists():
            return path
    
    # Fallback: assume in PATH
    return 'blender'


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def create_render_script() -> str:
    """
    Create Blender Python script for rendering validation frames.
    Returns path to temporary script.
    """
    script_content = '''
import bpy
import sys
import json
import time
from pathlib import Path

# Get arguments passed after --
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Get args after --

frame_number = int(argv[0])
output_path = argv[1]
quality_json = argv[2]

# Load quality settings
with open(quality_json, 'r') as f:
    quality = json.load(f)

# Configure scene
scene = bpy.context.scene
scene.render.engine = quality['engine']
scene.cycles.device = quality['device']
scene.cycles.samples = quality['samples']
scene.render.resolution_x = quality['resolution_x']
scene.render.resolution_y = quality['resolution_y']
scene.render.resolution_percentage = 100

# Set output
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_path

# Set frame
scene.frame_set(frame_number)

# Render
print(f"\\n{'='*60}")
print(f"🎬 Rendering validation frame {frame_number}")
print(f"   Output: {output_path}")
print(f"   Samples: {quality['samples']}")
print(f"   Resolution: {quality['resolution_x']}x{quality['resolution_y']}")
print(f"{'='*60}\\n")

start_time = time.time()

try:
    bpy.ops.render.render(write_still=True)
    render_time = time.time() - start_time
    
    print(f"\\n{'='*60}")
    print(f"✅ Frame {frame_number} rendered successfully")
    print(f"   Time: {render_time:.2f}s")
    print(f"{'='*60}\\n")
    
    # Write metadata
    meta_path = output_path.replace('.png', '_meta.json')
    meta = {
        'frame': frame_number,
        'render_time': render_time,
        'samples': quality['samples'],
        'resolution': [quality['resolution_x'], quality['resolution_y']],
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
except Exception as e:
    print(f"\\n❌ Error rendering frame {frame_number}: {e}\\n")
    sys.exit(1)
'''
    
    # Write to temp file
    project_root = get_project_root()
    temp_script = project_root / 'scripts' / 'explosions' / '_temp_validation_render.py'
    temp_script.write_text(script_content)
    
    return str(temp_script)


def render_validation_frame(
    blend_file: Path,
    frame: int,
    output_dir: Path,
    quality_settings: Dict,
    render_script: str
) -> Dict:
    """
    Render a single validation frame.
    
    Returns metadata about the render (time, success, etc.)
    """
    # Create quality settings JSON
    quality_json = output_dir / 'quality_settings.json'
    with open(quality_json, 'w') as f:
        json.dump(quality_settings, f)
    
    # Output path
    output_path = output_dir / f'frame_{frame:04d}.png'
    
    # Get Blender executable
    blender = get_blender_executable()
    
    # Build command
    cmd = [
        blender,
        str(blend_file),
        '--background',
        '--python', render_script,
        '--',
        str(frame),
        str(output_path),
        str(quality_json)
    ]
    
    print(f"\n🚀 Starting render for frame {frame}...")
    print(f"   Command: {' '.join(cmd[:6])}...")
    
    # Execute
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            check=True,
            # Don't capture output so we can see Blender errors
            # capture_output=True,
            # text=True
        )
        
        elapsed = time.time() - start_time
        render_time = elapsed  # Use actual elapsed time
        
        return {
            'frame': frame,
            'success': True,
            'render_time': render_time or elapsed,
            'total_time': elapsed,
            'output': str(output_path),
            'error': None
        }
        
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        return {
            'frame': frame,
            'success': False,
            'render_time': None,
            'total_time': elapsed,
            'output': str(output_path),
            'error': str(e)
        }


def render_all_validation_frames(
    blend_file: Path,
    output_dir: Path,
    frames: Optional[List[int]] = None
):
    """
    Render all validation keyframes.
    """
    if frames is None:
        frames = VALIDATION_FRAMES
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create render script ONCE before all frames
    render_script = create_render_script()
    
    print(f"\n{'='*70}")
    print(f"🎬 EXPLOSION VALIDATION RENDER")
    print(f"{'='*70}")
    print(f"Blend file: {blend_file}")
    print(f"Output dir: {output_dir}")
    print(f"Frames to render: {frames}")
    print(f"Quality: {VALIDATION_QUALITY['samples']} samples, {VALIDATION_QUALITY['resolution_x']}x{VALIDATION_QUALITY['resolution_y']}")
    print(f"Render script: {render_script}")
    print(f"{'='*70}\n")
    
    # Render each frame
    results = []
    total_start = time.time()
    
    for i, frame in enumerate(frames, 1):
        print(f"\n📊 Progress: {i}/{len(frames)}")
        result = render_validation_frame(
            blend_file,
            frame,
            output_dir,
            VALIDATION_QUALITY,
            render_script
        )
        results.append(result)
        
        if result['success']:
            print(f"✅ Frame {frame}: {result['render_time']:.2f}s")
        else:
            print(f"❌ Frame {frame}: FAILED - {result['error']}")
    
    total_time = time.time() - total_start
    
    # Generate summary report
    success_count = sum(1 for r in results if r['success'])
    avg_render_time = sum(r['render_time'] for r in results if r['render_time']) / success_count if success_count > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"📊 VALIDATION RENDER SUMMARY")
    print(f"{'='*70}")
    print(f"Total frames: {len(frames)}")
    print(f"Successful: {success_count}/{len(frames)} ({success_count/len(frames)*100:.1f}%)")
    print(f"Failed: {len(frames) - success_count}")
    print(f"Average render time: {avg_render_time:.2f}s per frame")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Output directory: {output_dir}")
    print(f"{'='*70}\n")
    
    # Save results JSON
    results_file = output_dir / 'validation_results.json'
    results_data = {
        'timestamp': datetime.now().isoformat(),
        'blend_file': str(blend_file),
        'frames': frames,
        'quality': VALIDATION_QUALITY,
        'results': results,
        'summary': {
            'total_frames': len(frames),
            'successful': success_count,
            'failed': len(frames) - success_count,
            'success_rate': success_count / len(frames),
            'avg_render_time': avg_render_time,
            'total_time': total_time
        }
    }
    
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"💾 Results saved to: {results_file}\n")
    
    # Cleanup temp script
    temp_script = get_project_root() / 'scripts' / 'explosions' / '_temp_validation_render.py'
    if temp_script.exists():
        temp_script.unlink()
    
    # Return exit code based on success
    return 0 if success_count == len(frames) else 1


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Render validation keyframes for explosion integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Render all validation keyframes
  python scripts/explosions/render_validation_keyframes.py explosion_test.blend
  
  # Render to custom output directory
  python scripts/explosions/render_validation_keyframes.py explosion_test.blend --output renders/validation_20251003
  
  # Render subset of frames for quick test
  python scripts/explosions/render_validation_keyframes.py explosion_test.blend --frames 1 50 75
  
Environment Variables:
  BLENDER - Path to Blender executable
  PROJECT_ROOT - Project root directory
        '''
    )
    
    parser.add_argument(
        'blend_file',
        type=Path,
        help='Path to .blend file with explosion scene'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output directory (default: projects/explosion-test/renders/validation_YYYYMMDD_HHMM)'
    )
    
    parser.add_argument(
        '--frames',
        type=int,
        nargs='+',
        default=None,
        help=f'Specific frames to render (default: {VALIDATION_FRAMES})'
    )
    
    args = parser.parse_args()
    
    # Validate blend file exists
    if not args.blend_file.exists():
        print(f"❌ Error: Blend file not found: {args.blend_file}")
        sys.exit(1)
    
    # Determine output directory
    if args.output is None:
        project_root = get_project_root()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        # Use timestamp at FRONT (taxonomy standard)
        args.output = project_root / 'projects' / 'explosion-test' / 'renders' / f'{timestamp}_validation'
    
    # Render frames
    exit_code = render_all_validation_frames(
        args.blend_file,
        args.output,
        args.frames
    )
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
