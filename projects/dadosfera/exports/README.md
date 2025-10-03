# Dadosfera Animation Exports

## Naming Convention

All files follow this standard format:

```
{project}_{version}_{date}_{quality}_{type}.mp4
```

**Components:**
- `{project}`: Project name (dadosfera)
- `{version}`: Release version (alpha, beta, deprecated)
- `{date}`: Creation date (YYYYMMDD)
- `{quality}`: Resolution (1080p, 720p, 360p, 270p)
- `{type}`: Render type/purpose (partial, test, viewport, etc.)

## Current Files

### ✅ Stable Release (Production)

**`dadosfera_stable_20251001_1080p_final.mp4`** (9.1 MB)
- **Status**: ✅ **PRODUCTION RELEASE**
- **Quality**: Full HD 1920x1080
- **Duration**: 10 seconds (240 frames)
- **Render**: Cycles photorealistic production quality
- **Engine**: Cycles (256 samples, OpenImageDenoise)
- **Features**:
  - ✅ Photorealistic materials and lighting
  - ✅ Motion blur and volumetrics
  - ✅ Complete animation (all 240 frames)
  - ✅ Production-grade quality
- **Deploy**: Ready for `3d-ddf.dadosfera.info`
- **Render Time**: ~90 minutes

### ✅ Alpha Releases

**`dadosfera_alpha_20251001_1080p_preview.mp4`** (291 KB)
- **Status**: Preview render
- **Quality**: Full HD 1920x1080
- **Duration**: 10 seconds (240 frames)
- **Render**: Cycles photorealistic (128 samples)
- **Purpose**: Alpha preview/testing
- **Render Time**: ~26 minutes

**`dadosfera_alpha_20250930_1080p_partial_8sec.mp4`** (3.6 MB)
- **Status**: Archived alpha release
- **Quality**: Full HD 1920x1080
- **Duration**: ~8 seconds (194 frames)
- **Render**: EEVEE_NEXT with materials
- **Features**:
  - ✅ Cyan metallic dadosfera text with glow
  - ✅ Glass crystal with refraction
  - ✅ Red explosions with bright emission
  - ✅ Gold/copper/silver metallic reflections
  - ✅ Professional lighting and shadows
- **Notes**: Missing final 46 frames (frames 195-240)

### ⚠️ Deprecated Files (Old Renders)

These are **viewport captures** without proper material rendering:

**`dadosfera_deprecated_20250930_1080p_viewport_nomat.mp4`** (7.7 MB)
- Resolution: 1920x1080
- Issue: Viewport capture, materials NOT rendered
- Render: OpenGL viewport only

**`dadosfera_deprecated_20250930_1080p_viewport1.mp4`** (4.0 MB)
- Resolution: 1920x1080
- Issue: Viewport capture, materials NOT rendered

**`dadosfera_deprecated_20250930_1080p_viewport2.mp4`** (3.1 MB)
- Resolution: 1920x1080
- Issue: Viewport capture, materials NOT rendered

**`dadosfera_deprecated_20250930_720p_preview.mp4`** (3.8 MB)
- Resolution: 1280x720
- Issue: Viewport capture, materials NOT rendered

**`dadosfera_deprecated_20250930_360p_test.mp4`** (727 KB)
- Resolution: 640x360
- Purpose: Camera test

**`dadosfera_deprecated_20250930_360p_viewport.mp4`** (535 KB)
- Resolution: 640x360
- Purpose: Quick viewport test

**`dadosfera_deprecated_20250930_270p_test.mp4`** (1.1 MB)
- Resolution: 480x270
- Purpose: Ultra-fast test

## Render Method Comparison

| Type | Method | Materials | Quality | Use Case |
|------|--------|-----------|---------|----------|
| **Alpha** | EEVEE PNG sequence → FFmpeg | ✅ Yes | High | Production |
| **Deprecated** | OpenGL viewport capture | ❌ No | Low | Testing only |

## Why Deprecated Files Don't Work

The deprecated files used `bpy.ops.render.opengl()` which:
- ❌ Captures viewport appearance only
- ❌ Doesn't render materials properly
- ❌ Missing reflections, refractions, emission
- ❌ No proper lighting calculation
- ✅ Fast but unusable for production

## Correct Rendering Workflow

The alpha release uses the proper workflow:

1. **Render to PNG frames** with `bpy.ops.render.render(animation=True)`
2. Each frame is fully rendered with all materials
3. **Encode frames to video** with FFmpeg
4. Result: Production-quality output

## Metadata

All exports are documented in `metadata.json` with:
- Render settings (engine, samples, denoiser)
- File properties (size, resolution, fps)
- Features and status
- Blend file reference

## To-Do

- [x] ~~Render remaining 46 frames (195-240)~~ ✅ Complete
- [x] ~~Create complete 10-second version~~ ✅ Done
- [ ] Deploy stable version to production CDN
- [ ] Create beta version with enhanced features
- [ ] Generate 4K version for v2.5

## File Size Reference

- Partial 8 sec (194 frames): 3.6 MB
- Estimated full 10 sec (240 frames): ~4.5 MB
- Frame size: ~1.9 MB per PNG (with alpha channel)

## Deployment

**Alpha URL**: `https://3d-ddf.alpha.dadosfera.info/dadosfera_alpha_20250930_1080p_partial_8sec.mp4`

---

**Updated**: October 2, 2025  
**Project**: 3D-DDF  
**Version**: Stable 1.0  
**Metadata**: See `metadata.json` for complete export information
