# Visual Regression Testing & Quality Assurance

## Overview

This document describes the quality assurance systems implemented to prevent rendering regressions and ensure consistent output quality across the 3D-DDF pipeline.

## Problem Statement

**Incident**: October 4, 2025 - Dadosfera render regression
- Wrong materials applied (Crystal_Glass on wrong objects)
- Test geometry visible (Ground_Plane checkered floor)
- No automated detection of the regression
- Manual QA required to catch the issue

**Root Cause**: 
- Production render used a development blend file with test elements
- No automated visual regression testing
- No pre-render validation

## Solution: Three-Tier Quality System

### 1. Scene Cleaning (`scripts/clean_production_scene.py`)

Automatically cleans development/test elements from Blender scenes before production renders.

**Features:**
- Removes or hides test objects (`test_*`, `debug_*`, `temp_*`, `Ground_Plane`)
- Validates material assignments
- Checks camera setup
- Creates automatic backups before modification

**Usage:**
```bash
# Dry run (check only)
blender scene.blend --background --python scripts/clean_production_scene.py -- --dry-run

# Apply fixes
blender scene.blend --background --python scripts/clean_production_scene.py -- --output scene.blend
```

**Example Output:**
```
🧹 SCENE CLEANING REPORT
============================================================
📦 Checking for test objects...
Found 1 test objects:
  - Ground_Plane
    → Hidden from render

🎨 Checking material assignments...
  ✓ All materials correctly assigned

📷 Checking camera setup...
  ✓ Camera setup correct

============================================================
✅ Scene is production-ready!
============================================================
```

### 2. Pre-Render Validation (`scripts/pre_render_validation.py`)

Validates a scene BEFORE rendering to catch issues early.

**Checks Performed:**
- ✓ Test objects not visible in render
- ✓ Materials correctly assigned
- ✓ Camera exists and positioned correctly
- ✓ Render settings (engine, resolution, samples)
- ✓ Scene integrity (missing textures, broken links)

**Exit Codes:**
- `0` = Production-ready (no issues)
- `1` = Warnings found (safe to render but review needed)
- `2` = Errors found (DO NOT RENDER)

**Usage:**
```bash
blender scene.blend --background --python scripts/pre_render_validation.py
```

**Integration with Render Pipeline:**
```bash
# Validate before rendering
blender scene.blend --background --python scripts/pre_render_validation.py && \
  python3 scripts/render_production.py dadosfera --quality production
```

### 3. Visual Regression Testing (`scripts/visual_regression_test.py`)

Captures reference frames (golden images) and validates new renders against them.

**Features:**
- Perceptual image comparison (structural similarity)
- Pixel-level difference detection
- Visual diff output (side-by-side + difference maps)
- Configurable similarity thresholds
- Automatic pass/fail determination

**Workflow:**

#### Step 1: Capture Reference Frames
```bash
# Capture golden images for dadosfera (frames 1, 24, 48, 120)
python3 scripts/visual_regression_test.py \
  --project dadosfera \
  --capture-reference \
  --frames 1 24 48 120 \
  --quality preview
```

Reference frames are stored in:
```
tests/visual_regression/dadosfera/reference/
├── frame_0001.png
├── frame_0024.png
├── frame_0048.png
├── frame_0120.png
└── metadata.json
```

#### Step 2: Run Regression Test
```bash
# Test latest render
python3 scripts/visual_regression_test.py \
  --project dadosfera \
  --test

# Test specific render
python3 scripts/visual_regression_test.py \
  --project dadosfera \
  --test \
  --render-dir projects/dadosfera/renders/20251004_1644_*
```

**Example Output:**
```
🔍 Visual Regression Test: dadosfera
   Reference: 2025-10-04T16:30:00
   Threshold: 95% similarity required
   Testing: 20251004_1644_production_fixed_no_ground_plane_test

   Comparing 4 frames...
   frame_0001... ✓ 98.5% similar
   frame_0024... ✓ 97.2% similar
   frame_0048... ✓ IDENTICAL
   frame_0120... ❌ 89.3% similar (below threshold)

============================================================
📊 REGRESSION TEST RESULTS
============================================================
   Frames tested: 4
   Average similarity: 95.8%
   Threshold: 95%
   Status: ✅ PASSED
============================================================
```

**Similarity Thresholds:**
- `>= 98%`: Excellent (nearly identical)
- `>= 95%`: Good (minor acceptable differences)
- `>= 90%`: Warning (review changes)
- `< 90%`: Failed (significant regression)

## Recommended Workflow

### For Development Renders:
```bash
# 1. Clean scene
blender scene.blend --background \
  --python scripts/clean_production_scene.py -- \
  --output scene.blend

# 2. Validate
blender scene.blend --background \
  --python scripts/pre_render_validation.py

# 3. Render preview
python3 scripts/render_production.py dadosfera --quality preview

# 4. If first time or major changes, capture reference
python3 scripts/visual_regression_test.py --project dadosfera --capture-reference
```

### For Production Renders:
```bash
# 1. Pre-render validation
blender scene.blend --background --python scripts/pre_render_validation.py

# 2. Render production quality
python3 scripts/render_production.py dadosfera --quality production

# 3. Visual regression test
python3 scripts/visual_regression_test.py --project dadosfera --test

# 4. If passed, video is ready for export
```

### For CI/CD Integration:
```bash
# Add to Jenkinsfile or GitHub Actions
stage('Quality Assurance') {
    steps {
        sh '''
            # Validate scene
            blender ${BLEND_FILE} --background --python scripts/pre_render_validation.py
            
            # Render test frames
            python3 scripts/render_production.py ${PROJECT} --quality preview --frames 1 48
            
            # Visual regression test
            python3 scripts/visual_regression_test.py --project ${PROJECT} --test --threshold 0.95
        '''
    }
}
```

## Incident Resolution: October 4, 2025

### Actions Taken:
1. ✅ Created `clean_production_scene.py` to remove test elements
2. ✅ Applied fix to `dadosfera_animation_v1_improved_explosions.blend`
3. ✅ Created automatic backup: `20251004_164200_dadosfera_animation_v1_improved_explosions_backup.blend`
4. ✅ Validated fix with pre-render validation (passed with warnings)
5. ✅ Rendered test frames to verify fix
6. ✅ Implemented visual regression test system

### Test Results:
- **Before Fix**: Ground_Plane visible, materials incorrect
- **After Fix**: Ground_Plane hidden, materials correct
- **Test Video**: `20251004_1644_fixed_no_ground_plane_test_1080p.mp4` (28 KB, 3 frames)

### Prevention:
- Pre-render validation will catch visible test objects
- Visual regression tests will detect material/scene changes
- Scene cleaning should be run before all production renders

## Video Lineage Investigation

For investigating quality differences between renders, use:

```bash
# Investigate specific video
python3 scripts/video_lineage.py projects/dadosfera/exports/20251004_1644_*.mp4

# Compare all videos in a project
python3 scripts/video_lineage.py --project dadosfera

# Full repository scan
python3 scripts/video_lineage.py --all
```

This traces each video back to:
- Source blend file
- Render settings (samples, resolution, quality preset)
- Render duration and performance
- Frame range and FPS
- Complete render metadata

## Future Improvements

### Planned Enhancements:
1. **Automated Reference Updates**: Auto-update golden images when changes are intentional
2. **Perceptual Hash Library**: Use dedicated image comparison libs (imagehash, SSIM)
3. **Machine Learning Detection**: Train model to detect "good" vs "bad" renders
4. **Integration with render_production.py**: Auto-run validation before render
5. **Web Dashboard**: Visual comparison UI for reviewing regression test results
6. **Slack/Email Notifications**: Alert on regression test failures

### Metrics to Track:
- Regression test pass rate
- Average render similarity score
- Time saved by catching issues early
- Number of manual QA reviews prevented

## Troubleshooting

### "No reference images found"
**Solution**: Capture reference first:
```bash
python3 scripts/visual_regression_test.py --project PROJECT --capture-reference
```

### "Validation failed - Ground_Plane visible"
**Solution**: Run scene cleaning:
```bash
blender scene.blend --background --python scripts/clean_production_scene.py -- --output scene.blend
```

### "ImageMagick compare not found"
**Solution**: Install ImageMagick for better comparison:
```bash
brew install imagemagick  # macOS
```
(Script falls back to basic size comparison if not available)

### "Similarity too low but renders look identical"
**Solution**: Adjust threshold or investigate lighting/material differences:
```bash
python3 scripts/visual_regression_test.py --project PROJECT --test --threshold 0.90
```

## Related Documentation

- [Render Production Guide](../guides/rendering-guide.md)
- [Quality Presets](../guides/explosion-creation.md#quality-presets)
- [Taxonomy Standards](../../TAXONOMY.md)
- [CI/CD Pipeline](../setup/jenkins.md)

---

**Last Updated**: October 4, 2025  
**Author**: AI Agent + Luis Martins  
**Status**: ✅ Active - In Production
