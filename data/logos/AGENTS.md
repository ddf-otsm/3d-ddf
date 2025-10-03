# Data/Logos Directory - Agent Guide

## Content Summary
This directory contains logo image files used as input for 3D transformations:
- **PNG files**: Logo images with transparency
- **SVG files**: Vector logo files (if any)
- **Various formats**: JPG, GIF, etc.

## Current Files
- `Logo Dadosfera Colorida sem Slogan.png` - Dadosfera colored logo without slogan (221KB)

## File Naming Convention
- Descriptive names indicating the brand and version
- Typically: `Logo {Brand} {Variant}.{ext}`

## Purpose
Stores source logo images that are processed by the logo-to-3D service and used in various 3D projects. These files are ignored by `.cursorignore` because they are binary image files that don't need to be indexed for code context.

## Finding Files

```bash
# List all logo files
ls -lh /Users/luismartins/local_repos/3d-ddf/data/logos/

# Find specific image types
find /Users/luismartins/local_repos/3d-ddf/data/logos -name "*.png" -o -name "*.svg"

# Get image dimensions (requires ImageMagick)
identify "/Users/luismartins/local_repos/3d-ddf/data/logos/Logo Dadosfera Colorida sem Slogan.png"

# List with file sizes
ls -lhS /Users/luismartins/local_repos/3d-ddf/data/logos/
```

## Common Operations

### Accessing a Logo File
```bash
# Read file info directly by absolute path
file "/Users/luismartins/local_repos/3d-ddf/data/logos/Logo Dadosfera Colorida sem Slogan.png"

# Get detailed image information (requires ImageMagick)
identify -verbose "/Users/luismartins/local_repos/3d-ddf/data/logos/Logo Dadosfera Colorida sem Slogan.png"

# Get basic dimensions with sips (macOS)
sips -g pixelHeight -g pixelWidth "/Users/luismartins/local_repos/3d-ddf/data/logos/Logo Dadosfera Colorida sem Slogan.png"
```

### Processing Logos
The logo-to-3D service processes these files. See:
- `services/logo-to-3d/` - Logo to 3D conversion service
- `projects/dadosfera/` - Dadosfera project using the logo

## Dependencies
- Related service: `services/logo-to-3d/`
- Related projects: `projects/dadosfera/`
- Scripts that may reference logos: Check `scripts/` directory
