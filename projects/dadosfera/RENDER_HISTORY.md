# Dadosfera Render History

Complete history of all renders with settings, results, and learnings.

## Format

Each entry documents:
- **Date/Time** - When the render was done
- **Export File** - Output filename (following taxonomy)
- **Engine** - Render engine used
- **Settings** - Key render settings
- **Duration** - Render time
- **Result** - Success/issues
- **Notes** - Observations and learnings

---

## October 1, 2025

### Render #3: Production Photorealistic (FINAL)
**Time**: 21:21  
**File**: `dadosfera_stable_20251001_1080p_final.mp4`  
**Engine**: Cycles  
**Settings**:
- Resolution: 1920x1080 (Full HD)
- Samples: 256
- Denoiser: OpenImageDenoise
- Motion Blur: Enabled
- Volumetrics: Enabled
- Preset: Production Photorealistic

**Duration**: ~90 minutes (240 frames)  
**Result**: ✅ Success  
**Quality**: 10/10 - Production ready

**Notes**:
- Best quality render to date
- Full 10-second animation (240 frames)
- Photorealistic materials and lighting
- Ready for production deployment
- File size: 9.1 MB (excellent compression)

**Learnings**:
- Production preset worth the render time
- Motion blur adds significant realism
- Denoising works excellently at 256 samples
- M3 Max handles Cycles very well

---

### Render #2: Cycles Photorealistic Preview
**Time**: 14:09  
**File**: `dadosfera_alpha_20251001_1080p_preview.mp4`  
**Engine**: Cycles  
**Settings**:
- Resolution: 1920x1080 (Full HD)
- Samples: 128
- Denoiser: OpenImageDenoise
- Preset: Photorealistic (not production)

**Duration**: ~26 minutes (240 frames)  
**Result**: ✅ Success  
**Quality**: 8/10 - Good preview quality

**Notes**:
- Faster preview render for testing
- 128 samples sufficient for preview
- Much smaller file size (291 KB)
- Good for quick iterations

**Learnings**:
- 128 samples adequate for previews
- Denoising very effective even at lower samples
- Fast enough for iteration cycles

---

## September 30, 2025

### Render #1: EEVEE Alpha Partial
**Time**: Evening  
**File**: `dadosfera_alpha_20250930_1080p_partial_8sec.mp4`  
**Engine**: EEVEE_NEXT  
**Settings**:
- Resolution: 1920x1080 (Full HD)
- Samples: 64
- Real-time engine

**Duration**: ~8 minutes (194 frames)  
**Result**: ⚠️ Partial (stopped early)  
**Quality**: 7/10 - Good but incomplete

**Notes**:
- Missing final 46 frames (frames 195-240)
- Materials render correctly with EEVEE_NEXT
- Much faster than Cycles
- Good for initial alpha release

**Issues**:
- Render stopped before completion
- Had to encode partial sequence

**Learnings**:
- EEVEE_NEXT renders materials properly
- Need to monitor renders to completion
- Frame sequence approach works well

---

### Deprecated Viewport Captures
**Date**: September 30, 2025  
**Method**: OpenGL viewport capture  
**Result**: ❌ Unusable for production

**Files**:
- `dadosfera_deprecated_20250930_1080p_viewport_nomat.mp4` (7.7 MB)
- `dadosfera_deprecated_20250930_1080p_viewport1.mp4` (4.0 MB)
- `dadosfera_deprecated_20250930_1080p_viewport2.mp4` (3.1 MB)
- `dadosfera_deprecated_20250930_720p_preview.mp4` (3.8 MB)
- `dadosfera_deprecated_20250930_360p_test.mp4` (727 KB)
- `dadosfera_deprecated_20250930_360p_viewport.mp4` (535 KB)
- `dadosfera_deprecated_20250930_270p_test.mp4` (1.1 MB)

**Issues**:
- Materials not rendered (just viewport appearance)
- Missing reflections, refractions, emission
- No proper lighting calculation
- Only useful for camera testing

**Learnings**:
- Never use `bpy.ops.render.opengl()` for final output
- Always use proper render (`bpy.ops.render.render()`)
- Viewport capture only for quick camera tests

---

## Render Statistics

### Total Renders
- **Production**: 1
- **Preview/Test**: 2
- **Deprecated**: 7
- **Total**: 10

### Render Times
- **Cycles Production (256 samples)**: ~90 min
- **Cycles Preview (128 samples)**: ~26 min
- **EEVEE (64 samples)**: ~8 min
- **Viewport capture**: ~3-5 min

### Quality Progression
1. Viewport captures: 3/10 (unusable)
2. EEVEE partial: 7/10 (good)
3. Cycles preview: 8/10 (very good)
4. Cycles production: 10/10 (excellent)

### File Sizes
- Production (240 frames, Cycles): 9.1 MB
- Preview (240 frames, Cycles): 291 KB
- Partial (194 frames, EEVEE): 3.6 MB
- Viewport captures: 0.5-7.7 MB

---

## Best Practices Discovered

### Render Settings
1. **Cycles Production**: 256 samples minimum
2. **Cycles Preview**: 128 samples sufficient
3. **EEVEE**: 64 samples adequate
4. **Denoising**: Always enable (OpenImageDenoise)
5. **Motion Blur**: Enable for final renders only

### Workflow
1. Test camera with viewport capture
2. Preview with EEVEE (fast iteration)
3. Test lighting with Cycles 128 samples
4. Final render with Cycles 256+ samples
5. Monitor render progress to completion

### Hardware
- **M3 Max**: Excellent for Cycles
- **MetalRT**: Significant performance boost
- **30 GPU cores**: Fully utilized
- **VRAM**: ~4 GB typical usage

---

## Future Renders Planned

### v1.5 Beta (October 15, 2025)
- Engine: Cycles
- Samples: 256-512
- Features: Enhanced materials, HDRI lighting
- Target render time: ~60 min (optimized)

### v2.0 Stable (November 1, 2025)
- Engine: Cycles
- Samples: 512
- Features: Physics simulations, PBR textures
- Target render time: ~90-120 min

### v2.5 Enhanced (December 2025)
- Engine: Cycles
- Resolution: 4K (3840x2160)
- Samples: 512-1024
- Target render time: ~6 hours

---

**Last Updated**: October 2, 2025  
**Total Render Time**: ~124 minutes (production quality)  
**Next Planned Render**: v1.5 Beta
