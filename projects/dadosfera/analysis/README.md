# Dadosfera Analysis Directory

This directory contains analysis files, comparisons, and debugging materials for the Dadosfera project.

## Directory Structure

```
analysis/
├── render_comparison_20251004/   ← Oct 2 vs Oct 4 render comparison
│   ├── *_video_frame1.jpg        ← Frames extracted from videos
│   ├── *_RENDER_frame1.png       ← Original render PNGs
│   └── COMPARISON_NOTES.md       ← Analysis notes
└── README.md                     ← This file
```

## Purpose

This directory stores:
- **Render Comparisons**: Side-by-side comparisons to debug quality regressions
- **Analysis Notes**: Documented findings from visual inspections
- **Reference Images**: Key frames for quality benchmarking
- **Debug Materials**: Any troubleshooting artifacts

## Subdirectories

### `render_comparison_20251004/`
**Created**: 2025-10-04  
**Purpose**: Compare Oct 2 "good" render vs Oct 4 "bad" renders to identify regression

**Files**:
- Oct 2 renders (baseline "good" quality)
- Oct 4 renders with checkered floor issue
- Oct 4 renders with no floor (failed fix attempt)
- Detailed comparison notes

**Status**: Under review - awaiting user feedback on visual differences

---

## Usage

When creating new analysis subdirectories, use the format:
```
analysis/[type]_[description]_YYYYMMDD/
```

Examples:
- `render_comparison_20251004/`
- `material_test_metallic_20251005/`
- `lighting_setup_comparison_20251006/`

Each subdirectory should contain:
1. Source files (images, data, etc.)
2. A README.md or notes file documenting the analysis
3. Any scripts or tools used for the analysis

---

**Note**: This directory is gitignored for large media files. Use `.gitkeep` or small reference images in git, store full-res files locally.
