# How to Run Explosion Validation Renders

**Quick Guide**: Execute validation renders for explosion integration testing

---

## 🎯 What This Does

Renders 10 strategic keyframes to validate:
- ✅ Visual quality across explosion sequence
- ✅ Performance metrics (render time, memory)
- ✅ Integration with main project scenes

---

## 🚀 Quick Start (3 Steps)

### Step 1: Ensure Blender is Available

```bash
# Check Blender is in PATH or set environment variable
$BLENDER --version
# OR
/Applications/Blender.app/Contents/MacOS/Blender --version
```

**Set environment variable** (recommended):
```bash
export BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
# OR add to .env file
echo 'BLENDER=/Applications/Blender.app/Contents/MacOS/Blender' >> .env
```

---

### Step 2: Run Validation Renders

```bash
cd ${PROJECT_ROOT}  # e.g., ~/local_repos/3d-ddf

# Option A: Render all 10 validation keyframes (recommended)
python3 scripts/explosions/render_validation_keyframes.py \
  projects/explosion-test/blender_files/explosion_test_scene.blend

# Option B: Custom output directory
python3 scripts/explosions/render_validation_keyframes.py \
  projects/explosion-test/blender_files/explosion_test_scene.blend \
  --output projects/explosion-test/renders/validation_20251003

# Option C: Quick test (render subset of frames)
python3 scripts/explosions/render_validation_keyframes.py \
  projects/explosion-test/blender_files/explosion_test_scene.blend \
  --frames 1 50 110 200 300
```

**Expected Duration**: ~3-4 minutes per frame = 30-40 minutes total for 10 frames

---

### Step 3: Review Results

**Check output directory**:
```bash
# Default location
ls -lh projects/explosion-test/renders/validation_*/

# You should see:
# - frame_0001.png through frame_0300.png (10 frames)
# - frame_XXXX_meta.json (metadata for each frame)
# - validation_results.json (summary report)
```

**Review summary**:
```bash
# View summary report
cat projects/explosion-test/renders/validation_*/validation_results.json
```

---

## 📊 What Gets Rendered

| Frame | Time (sec) | Event | Expected Result |
|-------|------------|-------|-----------------|
| 1 | 0.04 | Scene start | Clean slate, no explosions |
| 50 | 2.08 | First explosion trigger | Initial fire particles visible |
| 75 | 3.13 | First explosion peak | Full fire + debris, smoke starting |
| 110 | 4.58 | Second explosion trigger | First fading, second starting |
| 140 | 5.83 | Mid-sequence | Multiple explosions overlapping |
| 170 | 7.08 | Third explosion peak | Complex particle interactions |
| 200 | 8.33 | Late sequence | Older explosions dissipating |
| 230 | 9.58 | Final explosion | Last explosion at peak |
| 270 | 11.25 | Wind-down | All explosions in decay phase |
| 300 | 12.5 | Sequence end | Final smoke trails, embers |

---

## 🎨 Quality Settings

**Validation renders use**:
- **Samples**: 256 (medium quality, balanced speed/quality)
- **Resolution**: 1920x1080 (1080p)
- **Engine**: Cycles
- **Device**: GPU (if available)

---

## 📝 Output Files

### Frame Images
- **Format**: PNG
- **Naming**: `frame_0001.png`, `frame_0050.png`, etc.
- **Size**: ~2-5MB per frame

### Metadata Files
Each frame gets a `_meta.json` file with:
```json
{
  "frame": 50,
  "render_time": 15.3,
  "samples": 256,
  "resolution": [1920, 1080],
  "timestamp": "2025-10-03 14:30:15"
}
```

### Summary Report
`validation_results.json`:
```json
{
  "summary": {
    "total_frames": 10,
    "successful": 10,
    "failed": 0,
    "success_rate": 1.0,
    "avg_render_time": 16.2,
    "total_time": 162.5
  },
  "results": [ ... ]
}
```

---

## ✅ Success Criteria

**Validation passes if**:
- ✅ ≥8/10 frames render successfully (80% success rate)
- ✅ Average render time ≤20 seconds per frame
- ✅ Peak memory usage ≤4GB (check Activity Monitor)
- ✅ No critical visual artifacts (fireflies, clipping)
- ✅ Visual quality rated ≥4.0/5

See: `projects/explosion-test/VALIDATION_CHECKLIST.md`

---

## 🔧 Troubleshooting

### "Blender not found"
```bash
# Option 1: Set BLENDER environment variable
export BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"

# Option 2: Add to PATH
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"

# Option 3: Use .env file
echo 'BLENDER=/Applications/Blender.app/Contents/MacOS/Blender' >> .env
```

### "Blend file not found"
```bash
# Make sure you're in project root
cd ~/local_repos/3d-ddf

# Check if blend file exists
ls -lh projects/explosion-test/blender_files/*.blend
```

### Render takes too long (>30s per frame)
- CPU/GPU may be under load from other processes
- Consider closing other apps
- Use quick test with fewer frames: `--frames 1 50 110`

### Out of memory
- Close other applications
- Reduce samples: edit VALIDATION_QUALITY in script (256 → 128)
- Monitor memory: Activity Monitor → Memory tab

---

## 🎬 Next Steps After Validation

**If validation passes** (≥80% success rate):
1. ✅ Update `VALIDATION_CHECKLIST.md` with results
2. 🎥 Create sample video (see below)
3. 🚀 Proceed with integration into dadosfera project

**If validation fails** (<80% success rate):
1. 📊 Review error messages in terminal
2. 🔍 Check individual frame metadata for issues
3. 🐛 Debug specific frames that failed
4. 🔄 Re-run validation after fixes

---

## 🎥 Create Sample Video (After Validation)

```bash
cd projects/explosion-test/renders/validation_20251003

# High quality encode (recommended)
ffmpeg -framerate 24 -i frame_%04d.png \
  -c:v libx264 -preset slow -crf 18 \
  -pix_fmt yuv420p \
  explosion_validation_sample_1080p.mp4

# Quick preview
ffmpeg -framerate 24 -i frame_%04d.png \
  -c:v libx264 -preset fast -crf 23 \
  -pix_fmt yuv420p \
  explosion_validation_preview.mp4
```

**Note**: Only 10 keyframes = ~0.4 second video (not smooth, just validation)

For full animation, render all frames 1-300 using render_service.py

---

## 📚 Related Documentation

- **Validation Checklist**: `projects/explosion-test/VALIDATION_CHECKLIST.md`
- **Explosion Roadmap**: `docs/plans/active/explosion-development-roadmap.md`
- **Render Service**: `projects/dadosfera/RENDER_SERVICE.md`
- **Script Source**: `scripts/explosions/render_validation_keyframes.py`

---

## 🆘 Need Help?

1. Check `VALIDATION_CHECKLIST.md` for detailed criteria
2. Review `validation_results.json` for specific errors
3. Inspect individual `frame_XXXX_meta.json` files
4. Check Blender console output for warnings

---

**Last Updated**: 2025-10-03  
**Tested On**: macOS (Blender 4.5.3 LTS)  
**Estimated Time**: 30-40 minutes for full validation
