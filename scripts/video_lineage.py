#!/usr/bin/env python3
"""
Video Lineage Investigator

Traces the complete lineage of rendered videos back to their source:
- Render settings (quality, samples, resolution)
- Source blend file
- Project and description
- Render time and duration
- File relationships (frames → video)

Usage:
  python3 scripts/video_lineage.py [video_path]  # Single video
  python3 scripts/video_lineage.py --project dadosfera  # All videos in project
  python3 scripts/video_lineage.py --all  # All videos in all projects

Output includes:
  - Render metadata from JSON
  - Frame range and duration
  - Quality settings used
  - Source blend file and path
  - Render performance metrics
  - File relationships
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime
import argparse
import sys


def parse_timestamp_from_filename(filename: str) -> tuple[str, str] | None:
    """
    Parse YYYYMMDD_HHMM timestamp from filename.
    Returns (date, time) or None if format doesn't match.
    """
    pattern = re.compile(r'(\d{8})_(\d{4})_')
    match = pattern.search(filename)
    if match:
        date, time = match.groups()
        return (date, time)
    return None


def find_render_directory(repo_root: Path, timestamp: str) -> Path | None:
    """
    Find the render directory matching the timestamp.
    Searches in projects/*/renders/YYYYMMDD_HHMM_* directories.
    """
    # Pattern: YYYYMMDD_HHMM_description
    timestamp_pattern = re.compile(f'{timestamp[:8]}_{timestamp[9:13]}_')
    
    for renders_dir in repo_root.glob('projects/*/renders'):
        for render_dir in renders_dir.glob('*'):
            if render_dir.is_dir() and timestamp_pattern.search(render_dir.name):
                return render_dir
    return None


def load_render_metadata(render_dir: Path) -> Dict[str, Any] | None:
    """
    Load render_metadata.json from render directory.
    Returns the metadata dictionary or None if not found.
    """
    metadata_path = render_dir / 'render_metadata.json'
    if not metadata_path.exists():
        return None
    
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def find_matching_video(render_metadata: Dict[str, Any], exports_root: Path) -> Path | None:
    """
    Find the corresponding video file in exports directory.
    Matches on timestamp and description.
    """
    timestamp = render_metadata['timestamp']
    description = render_metadata['description'] if 'description' in render_metadata else ''
    quality = render_metadata['quality_preset']
    resolution = render_metadata['quality_settings']['resolution_y']
    
    video_pattern = f'{timestamp}_{description}_{quality}_{resolution}p.mp4'
    
    # Try exact match first
    video_path = exports_root / video_pattern
    if video_path.exists():
        return video_path
    
    # Try with project name
    project = render_metadata.get('project', '')
    if project:
        video_pattern = f'{timestamp}_{project}_{quality}_{resolution}p.mp4'
        video_path = exports_root / video_pattern
        if video_path.exists():
            return video_path
    
    # Fallback: search by timestamp
    for video_file in exports_root.glob(f'{timestamp}*.mp4'):
        return video_path
    
    return None


def print_video_lineage(video_path: Path) -> None:
    """
    Print complete lineage for a specific video file.
    """
    video_file = Path(video_path)
    if not video_file.exists():
        print(f"❌ Video not found: {video_path}")
        return
    
    print(f"\n📊 VIDEO LINEAGE: {video_file.name}")
    print("=" * 60)
    
    # Parse timestamp from filename
    timestamp = parse_timestamp_from_filename(video_file.name)
    if not timestamp:
        print(f"⚠️  Could not parse timestamp from filename: {video_file.name}")
        print(f"   File size: {video_file.stat().st_size / (1024*1024):.1f} MB")
        print(f"   Modified: {datetime.fromtimestamp(video_file.stat().st_mtime):%Y-%m-%d %H:%M}")
        return
    
    date, time = timestamp
    print(f"Timestamp: {date} {time}")
    
    # Find project from path
    project = None
    for proj in ['dadosfera', 'explosion-test']:
        if proj in str(video_file.parent):
            project = proj
            break
    print(f"Project: {project or 'unknown'}")
    
    # Find render directory
    full_timestamp = f"{date}_{time}"
    render_dir = find_render_directory(video_file.parent.parent, full_timestamp)
    if not render_dir:
        print(f"⚠️  Could not find matching render directory for {timestamp}")
        return
    
    print(f"Render directory: {render_dir.name}")
    
    # Load metadata
    metadata = load_render_metadata(render_dir)
    if not metadata:
        print(f"⚠️  No render_metadata.json found in {render_dir.name}")
        return
    
    # Print metadata
    print(f"\n📋 Render Metadata:")
    print(f"   Source blend file: {Path(metadata['blend_file']).name}")
    print(f"   Quality preset: {metadata.get('quality_preset', 'unknown')}")
    print(f"   Samples: {metadata['quality_settings'].get('samples', 'unknown')}")
    print(f"   Resolution: {metadata['quality_settings'].get('resolution_x', 'unknown')}x{metadata['quality_settings'].get('resolution_y', 'unknown')}")
    print(f"   Frame range: {metadata['frame_range'][0]}-{metadata['frame_range'][1]} ({metadata['frame_range'][1] - metadata['frame_range'][0] + 1} frames)")
    print(f"   Duration: {metadata.get('duration_seconds', 'unknown'):.2f}s")
    print(f"   FPS: {metadata.get('fps', 'unknown')}")
    print(f"   Render time: {metadata.get('render_duration_minutes', 'unknown'):.1f} minutes")
    print(f"   Average: {metadata.get('average_seconds_per_frame', 'unknown'):.1f}s per frame")
    print(f"   Engine: Cycles (Metal GPU)")
    print(f"   Denoising: {metadata['quality_settings'].get('denoising', False)}")
    
    # Check if video matches metadata
    expected_video = find_matching_video(metadata, video_file.parent)
    if expected_video and expected_video == video_file:
        print(f"   ✅ Video matches render metadata")
    else:
        print(f"   ⚠️  Video may not match render metadata")
        if expected_video:
            print(f"      Expected: {expected_video.name}")
    
    print(f"\n📁 Frame Directory:")
    frame_count = len(list(render_dir.glob('frame_*.png')))
    print(f"   {render_dir}")
    print(f"   Frames present: {frame_count}")
    
    print(f"\n🎬 Video File:")
    size_mb = video_file.stat().st_size / (1024*1024)
    print(f"   {video_file}")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   Modified: {datetime.fromtimestamp(video_file.stat().st_mtime):%Y-%m-%d %H:%M}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Investigate video lineage and render settings")
    parser.add_argument('video', nargs='?', type=str,
                       help='Path to video file (optional)')
    parser.add_argument('--project', type=str,
                       help='Project to scan (e.g., dadosfera, explosion-test)')
    parser.add_argument('--all', action='store_true',
                       help='Show lineage for all videos in all projects')
    args = parser.parse_args()
    
    repo_root = Path('.').resolve()
    
    if args.video:
        # Single video lookup
        video_path = repo_root / args.video
        print_video_lineage(video_path)
    elif args.project:
        # Project-specific
        exports_dir = repo_root / f'projects/{args.project}/exports'
        if not exports_dir.exists():
            print(f"❌ Project exports directory not found: {exports_dir}")
            return 1
        
        videos = sorted(exports_dir.glob('*.mp4'))
        if not videos:
            print(f"❌ No videos found in {exports_dir}")
            return 0
        
        print(f"📊 {args.project.upper()} VIDEO LINEAGE REPORT")
        print(f"Found {len(videos)} videos:\n")
        
        for video in videos:
            print(f"\n--- {video.name} ---")
            print_video_lineage(video)
        
        print(f"\n📊 SUMMARY: {len(videos)} videos traced")
    elif args.all:
        # All projects
        print("📊 ALL PROJECT VIDEO LINEAGE REPORT")
        print(f"Scanning {repo_root}\n")
        
        total_videos = 0
        for project in ['dadosfera', 'explosion-test']:
            exports_dir = repo_root / f'projects/{project}/exports'
            if not exports_dir.exists():
                continue
                
            videos = sorted(exports_dir.glob('*.mp4'))
            if videos:
                print(f"\n{'='*60}")
                print(f"{project.upper()} - {len(videos)} videos")
                print('='*60)
                
                for video in videos:
                    print(f"\n--- {video.name} ---")
                    print_video_lineage(video)
                
                total_videos += len(videos)
                print()
        
        print(f"\n🏆 COMPLETE LINEAGE REPORT")
        print(f"Total videos traced: {total_videos}")
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
