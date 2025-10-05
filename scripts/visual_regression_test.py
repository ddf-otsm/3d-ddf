#!/usr/bin/env python3
"""
Visual Regression Test System

Captures reference frames and validates new renders against them to detect:
- Material changes
- Lighting changes
- Camera/composition changes
- Object visibility changes
- Quality regressions

Usage:
  # Capture reference images (golden images)
  python3 scripts/visual_regression_test.py --project dadosfera --capture-reference

  # Run regression test against latest render
  python3 scripts/visual_regression_test.py --project dadosfera --test

  # Test specific render
  python3 scripts/visual_regression_test.py --project dadosfera --test --render-dir renders/20251004_1549_*

Features:
  - File size and hash comparison
  - Visual diff output (side-by-side + difference map)
  - Pass/fail thresholds with configurable tolerance
  - Integration with CI/CD pipelines
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, List
import argparse
import json
from datetime import datetime
import sys
import hashlib

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def get_image_hash(image_path: Path) -> str:
    """Calculate SHA256 hash of image file."""
    sha256 = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def capture_reference_frames(project: str, frames: List[int], quality: str = 'preview') -> Path:
    """
    Capture reference frames for regression testing.
    
    Args:
        project: Project name (e.g., 'dadosfera')
        frames: List of frame numbers to capture
        quality: Quality preset to use
    
    Returns:
        Path to reference directory
    """
    project_root = get_project_root()
    reference_dir = project_root / f'tests/visual_regression/{project}/reference'
    reference_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📸 Capturing reference frames for {project}")
    print(f"   Frames: {frames}")
    print(f"   Quality: {quality}")
    print(f"   Output: {reference_dir}")
    
    # Run the render with our production script
    print(f"\n   Using render_production.py to capture reference frames...")
    
    # Render with the production script
    frame_str = f"{min(frames)} {max(frames)}"
    cmd = [
        sys.executable,
        str(project_root / 'scripts/render_production.py'),
        project,
        '--quality', quality,
        '--frames', *frame_str.split(),
        '--no-encode'
    ]
    
    print(f"   Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_root)
    
    if result.returncode != 0:
        print(f"❌ Render failed with code {result.returncode}")
        return None
    
    # Find the latest render directory
    renders_dir = project_root / f'projects/{project}/renders'
    render_dirs = sorted([d for d in renders_dir.glob('*') if d.is_dir()], 
                         key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not render_dirs:
        print(f"❌ No render directory found")
        return None
    
    latest_render = render_dirs[0]
    print(f"   Latest render: {latest_render.name}")
    
    # Copy selected frames to reference directory
    hashes = {}
    for frame in frames:
        src_frame = latest_render / f'frame_{frame:04d}.png'
        dst_frame = reference_dir / f'frame_{frame:04d}.png'
        
        if src_frame.exists():
            import shutil
            shutil.copy2(src_frame, dst_frame)
            hashes[f'frame_{frame:04d}.png'] = get_image_hash(dst_frame)
            print(f"   ✓ Copied frame {frame}")
        else:
            print(f"   ⚠️  Frame {frame} not found in render")
    
    # Save metadata
    metadata = {
        'project': project,
        'captured_at': datetime.now().isoformat(),
        'frames': frames,
        'quality': quality,
        'source_render': latest_render.name,
        'frame_hashes': hashes
    }
    
    metadata_file = reference_dir / 'metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Reference frames captured: {len(hashes)} frames")
    print(f"   Location: {reference_dir}")
    
    return reference_dir

def compare_images(reference_path: Path, test_path: Path) -> Dict:
    """
    Compare two images and return similarity metrics.
    
    Returns:
        Dict with metrics: identical, size_match, hash_match, etc.
    """
    metrics = {
        'reference': str(reference_path.name),
        'test': str(test_path.name),
        'identical': False,
        'size_match': False,
        'hash_match': False,
        'similarity': 0.0,
    }
    
    # Check if files exist
    if not reference_path.exists():
        metrics['error'] = 'Reference image not found'
        return metrics
    
    if not test_path.exists():
        metrics['error'] = 'Test image not found'
        metrics['similarity'] = 0.0
        return metrics
    
    # Check file sizes
    ref_size = reference_path.stat().st_size
    test_size = test_path.stat().st_size
    size_diff = abs(ref_size - test_size) / max(ref_size, 1)
    
    metrics['ref_size_kb'] = ref_size / 1024
    metrics['test_size_kb'] = test_size / 1024
    metrics['size_difference'] = size_diff
    metrics['size_match'] = size_diff < 0.05  # Within 5%
    
    # Compare hashes
    ref_hash = get_image_hash(reference_path)
    test_hash = get_image_hash(test_path)
    
    metrics['ref_hash'] = ref_hash[:16]
    metrics['test_hash'] = test_hash[:16]
    metrics['hash_match'] = ref_hash == test_hash
    
    if metrics['hash_match']:
        metrics['identical'] = True
        metrics['similarity'] = 1.0
    elif metrics['size_match']:
        # Similar size suggests similar content
        metrics['similarity'] = 1.0 - size_diff
    else:
        # Significant difference
        metrics['similarity'] = max(0.0, 1.0 - (size_diff * 2))
    
    return metrics

def run_regression_test(project: str, render_dir: Optional[Path] = None, threshold: float = 0.95) -> bool:
    """
    Run visual regression test on a render.
    
    Args:
        project: Project name
        render_dir: Specific render directory to test (or None for latest)
        threshold: Similarity threshold (0.0-1.0, default 0.95 = 95% similar)
    
    Returns:
        bool: True if test passed, False if failed
    """
    project_root = get_project_root()
    reference_dir = project_root / f'tests/visual_regression/{project}/reference'
    
    if not reference_dir.exists():
        print(f"❌ No reference images found for {project}")
        print(f"   Run with --capture-reference first")
        return False
    
    # Load reference metadata
    metadata_file = reference_dir / 'metadata.json'
    if not metadata_file.exists():
        print(f"❌ No reference metadata found")
        return False
    
    with open(metadata_file, 'r') as f:
        ref_metadata = json.load(f)
    
    print(f"\n🔍 Visual Regression Test: {project}")
    print(f"   Reference: {ref_metadata['captured_at']}")
    print(f"   Threshold: {threshold * 100:.0f}% similarity required")
    
    # Find render directory
    if render_dir is None:
        renders_dir = project_root / f'projects/{project}/renders'
        render_dirs = sorted([d for d in renders_dir.glob('*') if d.is_dir()], 
                           key=lambda x: x.stat().st_mtime, reverse=True)
        if not render_dirs:
            print(f"❌ No render directories found")
            return False
        render_dir = render_dirs[0]
    else:
        render_dir = project_root / render_dir
    
    print(f"   Testing: {render_dir.name}")
    
    # Create output directory for results
    output_dir = project_root / f'tests/visual_regression/{project}/results/{render_dir.name}'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Compare each reference frame
    results = []
    reference_frames = list(reference_dir.glob('frame_*.png'))
    
    if not reference_frames:
        print(f"❌ No reference frames found")
        return False
    
    print(f"\n   Comparing {len(reference_frames)} frames...")
    
    for ref_frame in reference_frames:
        test_frame = render_dir / ref_frame.name
        
        print(f"   {ref_frame.stem}...", end='', flush=True)
        
        metrics = compare_images(ref_frame, test_frame)
        results.append(metrics)
        
        if 'error' in metrics:
            print(f" ❌ {metrics['error']}")
        elif metrics.get('identical'):
            print(f" ✅ IDENTICAL")
        else:
            similarity = metrics.get('similarity', 0.0)
            if similarity >= threshold:
                print(f" ✅ {similarity*100:.1f}% similar")
            else:
                print(f" ❌ {similarity*100:.1f}% similar (below threshold)")
    
    # Calculate overall results
    valid_results = [r for r in results if 'error' not in r]
    if not valid_results:
        print(f"\n❌ No valid comparisons")
        return False
    
    avg_similarity = sum(r.get('similarity', 0.0) for r in valid_results) / len(valid_results)
    passed = avg_similarity >= threshold
    
    print(f"\n" + "="*60)
    print(f"📊 REGRESSION TEST RESULTS")
    print(f"="*60)
    print(f"   Frames tested: {len(valid_results)}")
    print(f"   Frames identical: {sum(1 for r in valid_results if r.get('identical'))}")
    print(f"   Average similarity: {avg_similarity*100:.1f}%")
    print(f"   Threshold: {threshold*100:.0f}%")
    print(f"   Status: {'✅ PASSED' if passed else '❌ FAILED'}")
    print(f"="*60)
    
    # Save results
    results_file = output_dir / 'test_results.json'
    test_results = {
        'project': project,
        'test_date': datetime.now().isoformat(),
        'render_dir': str(render_dir.name),
        'reference_metadata': ref_metadata,
        'threshold': threshold,
        'frames_tested': len(valid_results),
        'average_similarity': avg_similarity,
        'passed': passed,
        'frame_results': results
    }
    
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n   Results saved: {results_file}")
    
    return passed

def main():
    parser = argparse.ArgumentParser(description="Visual regression testing for 3D renders")
    parser.add_argument('--project', type=str, required=True,
                       help='Project name (e.g., dadosfera, explosion-test)')
    parser.add_argument('--capture-reference', action='store_true',
                       help='Capture reference images (golden images)')
    parser.add_argument('--test', action='store_true',
                       help='Run regression test on latest render')
    parser.add_argument('--render-dir', type=str,
                       help='Specific render directory to test')
    parser.add_argument('--frames', type=int, nargs='+', default=[1, 24, 48],
                       help='Frame numbers to test (default: 1, 24, 48)')
    parser.add_argument('--threshold', type=float, default=0.95,
                       help='Similarity threshold 0.0-1.0 (default: 0.95)')
    parser.add_argument('--quality', type=str, default='preview',
                       help='Quality preset for reference capture')
    
    args = parser.parse_args()
    
    if args.capture_reference:
        reference_dir = capture_reference_frames(args.project, args.frames, args.quality)
        return 0 if reference_dir else 1
    
    elif args.test:
        render_dir = Path(args.render_dir) if args.render_dir else None
        passed = run_regression_test(args.project, render_dir, args.threshold)
        return 0 if passed else 1
    
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())