# Renders Directory - Agent Guide

## Content Summary
This directory contains rendered output from Blender, including:
- **Video files**: MP4, AVI, MOV formats (final rendered animations)
- **Image sequences**: PNG, JPG frame sequences from renders
- **Subdirectories**: Organized by project or render type (e.g., `explosions/`)

## File Naming Convention
- Videos: `{project}_{timestamp}.mp4` or `{project}_final.mp4`
- Frame sequences: `frame_####.png` (zero-padded frame numbers)
- Subdirectories: `{project_name}_{date}_{description}/`

## Purpose
Stores final render outputs from Blender scenes. These files are ignored by `.cursorignore` due to their large size, but can be accessed when needed for analysis, verification, or processing.

## Finding Files

```bash
# List all video files in renders/
find /Users/luismartins/local_repos/3d-ddf/renders -name "*.mp4" -o -name "*.avi" -o -name "*.mov"

# List all subdirectories
ls -d /Users/luismartins/local_repos/3d-ddf/renders/*/

# Find the most recent video
find /Users/luismartins/local_repos/3d-ddf/renders -name "*.mp4" -exec ls -t {} + | head -1

# Count frame sequences in a directory
find /Users/luismartins/local_repos/3d-ddf/renders/explosions -name "*.png" | wc -l

# Get video file info (requires ffprobe)
ffprobe -v quiet -print_format json -show_format -show_streams {video_file}
```

## Common Operations

### Accessing a Specific Video
```bash
# Read video metadata directly by absolute path
ffprobe "/Users/luismartins/local_repos/3d-ddf/renders/explosions/my_render.mp4"
```

### Working with Frame Sequences
```bash
# List frames in order
ls -1v /Users/luismartins/local_repos/3d-ddf/renders/explosions/frame_*.png

# Check frame count
ls -1 /Users/luismartins/local_repos/3d-ddf/renders/explosions/frame_*.png | wc -l
```

## Subdirectories
- `explosions/`: Explosion effect renders and tests (see `explosions/AGENTS.md`)

## Dependencies
- Related scripts: `scripts/render_service.py`, `scripts/create_explosion_video.py`
- Configuration: `pytest.ini`, project-specific render settings
- Source scenes: `.blend` files in project directories
