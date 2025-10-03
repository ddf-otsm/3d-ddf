# AGENTS.md - AI Agent Navigation Guide

This file helps AI agents navigate and work with content that may be excluded from direct indexing.

## Purpose
`AGENTS.md` files are placed in directories to help AI assistants understand folder contents even when files are ignored by `.cursorignore`. This allows agents to:
1. Discover what files exist using Unix tools
2. Selectively remove files from `.cursorignore` when needed
3. Understand the structure and purpose without loading all content

## How AI Agents Should Use This File

### Finding Files
```bash
# List all files in this directory
ls -la

# Find specific file types
find . -name "*.png" -o -name "*.mp4"

# Count files by type
find . -type f | sed 's/.*\.//' | sort | uniq -c
```

### Accessing Ignored Content
If you need to work with a specific ignored file:
1. Read this `AGENTS.md` to understand what's available
2. Use `find` or `ls` commands to locate the exact file
3. Read the specific file by absolute path (ignored files can still be read directly)
4. Or temporarily remove it from `.cursorignore` if extensive work is needed

### Template Structure
Each folder's `AGENTS.md` should include:
- **Content Summary**: What types of files are stored here
- **File Naming Convention**: How files are named
- **Purpose**: Why these files exist
- **Common Operations**: How to find or work with specific files
- **Dependencies**: Related files or folders

## Example AGENTS.md for a Renders Folder
```markdown
# Renders Folder - Agent Guide

## Content
- Image sequences: PNG frames numbered 0001-0250
- Video outputs: MP4 files (H.264 encoded)
- Metadata: JSON files with render settings

## Naming Convention
- Frames: `frame_NNNN.png` (e.g., `frame_0001.png`)
- Videos: `{project}_{date}_final.mp4`
- Metadata: `{project}_{date}_metadata.json`

## Finding Files
```bash
# List all video files
ls -1 *.mp4

# Find frame sequences
find . -name "frame_*.png" | sort

# Get latest render
ls -t *.mp4 | head -1
```

## Purpose
Contains final render outputs from Blender. Videos are ignored due to size but can be accessed by absolute path when needed for analysis.
```

## Root Directory Overview
This is the root `AGENTS.md` for the 3D-DDF project. See folder-specific `AGENTS.md` files in subdirectories for detailed content descriptions.
