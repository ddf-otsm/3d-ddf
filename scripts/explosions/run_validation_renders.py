#!/usr/bin/env python3
"""
Run validation renders for explosion system.

This script renders the 10 keyframes specified in the validation checklist
to verify explosion quality, performance, and integration.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime


# Validation keyframes from VALIDATION_CHECKLIST.md
VALIDATION_KEYFRAMES = [
    (1, "Scene start - no explosions visible"),
    (50, "First explosion trigger - initial fire particles"),
    (75, "First explosion peak - full fire + debris + smoke"),
    (110, "Second explosion trigger - first fading, second starting"),
    (140, "Mid-sequence - multiple explosions overlapping"),
    (170, "Third explosion peak - complex particle interactions"),
    (200, "Late sequence - older explosions dissipating"),
    (230, "Final explosion - last explosion at peak"),
    (270, "Wind-down - all explosions in decay phase"),
    (300, "Sequence end - final smoke trails and embers"),
]


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_blender_executable() -> str:
    """Get Blender executable path from environment or default."""
    import os
    blender = os.environ.get("BLENDER", "blender")
    return blender


def render_keyframe(
    blend_file: Path,
    frame: int,
    output_dir: Path,
    quality: str = "medium"
) -> bool:
    """
    Render a single keyframe.
    
    Args:
        blend_file: Path to .blend file
        frame: Frame number to render
        output_dir: Output directory for rendered frame
        quality: Quality preset (quick/medium/high)
        
    Returns:
        True if render succeeded, False otherwise
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"frame_{frame:04d}.png"
    
    blender = get_blender_executable()
    
    # Blender command to render single frame
    cmd = [
        blender,
        str(blend_file),
        "--background",
        "--frame-start", str(frame),
        "--frame-end", str(frame),
        "--render-output", str(output_file.with_suffix("")),
        "--render-format", "PNG",
        "--python-expr",
        f"import bpy; bpy.context.scene.render.resolution_x = 1920; "
        f"bpy.context.scene.render.resolution_y = 1080; "
        f"bpy.context.scene.cycles.samples = 256 if '{quality}' == 'medium' else 128",
        "--render-frame", str(frame),
    ]
    
    print(f"\n{'='*70}")
    print(f"Rendering frame {frame}...")
    print(f"Output: {output_file}")
    print(f"{'='*70}\n")
    
    start_time = datetime.now()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per frame
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Check for output file - Blender may create with different naming
        actual_output = None
        if output_file.exists():
            actual_output = output_file
        else:
            # Check for Blender's frame number format (e.g., frame_00010001.png)
            for possible_file in output_dir.glob(f"frame_*{frame:04d}*.png"):
                actual_output = possible_file
                break
        
        if result.returncode == 0 and actual_output and actual_output.exists():
            file_size_mb = actual_output.stat().st_size / (1024 * 1024)
            print(f"✅ Frame {frame} rendered successfully")
            print(f"   Duration: {duration:.1f}s")
            print(f"   File size: {file_size_mb:.2f} MB")
            print(f"   Output: {actual_output.name}")
            return True
        else:
            print(f"❌ Frame {frame} render failed")
            print(f"   Return code: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Frame {frame} render timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Frame {frame} render error: {e}")
        return False


def run_validation(
    blend_file: Path,
    output_dir: Path,
    quality: str = "medium",
    frames: list = None
) -> dict:
    """
    Run validation renders for specified keyframes.
    
    Args:
        blend_file: Path to .blend file
        output_dir: Output directory
        quality: Quality preset
        frames: List of frame numbers (or None for all validation frames)
        
    Returns:
        Dictionary with validation results
    """
    if frames is None:
        frames_to_render = [f[0] for f in VALIDATION_KEYFRAMES]
    else:
        frames_to_render = frames
    
    results = {
        "total": len(frames_to_render),
        "passed": 0,
        "failed": 0,
        "frames": {},
        "start_time": datetime.now(),
    }
    
    print(f"\n{'='*70}")
    print(f"EXPLOSION VALIDATION RENDER")
    print(f"{'='*70}")
    print(f"Blend file: {blend_file}")
    print(f"Output dir: {output_dir}")
    print(f"Quality: {quality}")
    print(f"Frames to render: {len(frames_to_render)}")
    print(f"{'='*70}\n")
    
    for frame_num in frames_to_render:
        success = render_keyframe(blend_file, frame_num, output_dir, quality)
        results["frames"][frame_num] = success
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    results["end_time"] = datetime.now()
    results["duration"] = (results["end_time"] - results["start_time"]).total_seconds()
    
    return results


def print_summary(results: dict):
    """Print validation summary."""
    print(f"\n{'='*70}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"Total frames: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print(f"Pass rate: {results['passed']/results['total']*100:.1f}%")
    print(f"Total duration: {results['duration']:.1f}s ({results['duration']/60:.1f} minutes)")
    
    if results['passed'] > 0:
        avg_time = results['duration'] / results['passed']
        print(f"Average time per frame: {avg_time:.1f}s")
    
    print(f"\nFrame-by-frame results:")
    for frame, success in results['frames'].items():
        status = "✅ PASS" if success else "❌ FAIL"
        desc = next((d[1] for d in VALIDATION_KEYFRAMES if d[0] == frame), "")
        print(f"  Frame {frame:3d}: {status} - {desc}")
    
    # Approval criteria check
    pass_rate = results['passed'] / results['total']
    print(f"\n{'='*70}")
    print(f"APPROVAL CRITERIA")
    print(f"{'='*70}")
    
    min_pass = pass_rate >= 0.8
    print(f"Minimum pass (≥80%): {'✅ PASS' if min_pass else '❌ FAIL'} ({pass_rate*100:.1f}%)")
    
    if results['passed'] > 0:
        avg_time = results['duration'] / results['passed']
        time_ok = avg_time <= 20
        print(f"Average render time (≤20s): {'✅ PASS' if time_ok else '❌ FAIL'} ({avg_time:.1f}s)")
    
    if min_pass:
        print(f"\n🎉 VALIDATION PASSED - Ready for integration!")
    else:
        print(f"\n⚠️  VALIDATION FAILED - Review and fix issues")
    
    print(f"{'='*70}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run explosion validation renders"
    )
    parser.add_argument(
        "--blend-file",
        type=Path,
        help="Path to .blend file (default: projects/explosion-test/blender_files/explosion_test_scene.blend)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: projects/explosion-test/renders/validation_YYYYMMDD_HHMM)"
    )
    parser.add_argument(
        "--quality",
        choices=["quick", "medium", "high"],
        default="medium",
        help="Render quality preset (default: medium)"
    )
    parser.add_argument(
        "--frames",
        type=int,
        nargs="+",
        help="Specific frames to render (default: all validation keyframes)"
    )
    
    args = parser.parse_args()
    
    # Set defaults
    project_root = get_project_root()
    
    if args.blend_file is None:
        args.blend_file = project_root / "projects" / "explosion-test" / "blender_files" / "explosion_test_scene.blend"
    
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        args.output_dir = project_root / "projects" / "explosion-test" / "renders" / f"validation_{timestamp}"
    
    # Validate blend file exists
    if not args.blend_file.exists():
        print(f"❌ Error: Blend file not found: {args.blend_file}")
        print(f"\nAvailable blend files:")
        blend_dir = args.blend_file.parent
        if blend_dir.exists():
            for f in blend_dir.glob("*.blend"):
                print(f"  - {f}")
        return 1
    
    # Run validation
    results = run_validation(
        args.blend_file,
        args.output_dir,
        args.quality,
        args.frames
    )
    
    # Print summary
    print_summary(results)
    
    # Return exit code based on results
    return 0 if results['passed'] / results['total'] >= 0.8 else 1


if __name__ == "__main__":
    sys.exit(main())
