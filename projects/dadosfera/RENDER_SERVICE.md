# Dadosfera Render Service

## Overview

Centralized, parameterized render service for the Dadosfera project. Single unified script that handles all rendering scenarios with configurable parameters.

## Quick Start

```bash
# Navigate to project root
cd /Users/luismartins/local_repos/3d-ddf

# Quick draft (fastest - ~2 minutes)
bash scripts/render.sh quick

# Preview quality (~15 minutes)
bash scripts/render.sh preview

# Production quality (~45 minutes) - RECOMMENDED
bash scripts/render.sh production

# Final quality (~2 hours)
bash scripts/render.sh final
```

## Architecture

### Single Service, Multiple Parameters

**One Script**: `scripts/render_service.py`
**One Wrapper**: `scripts/render.sh`
**One Output Structure**: `projects/dadosfera/renders/{engine}_{quality}_{materials}_{timestamp}/`

### No More Duplicates

❌ **Old (scattered)**:
- `render_dadosfera.py`
- `render_dadosfera_from_file.py`
- `render_photorealistic.sh`
- `apply_photorealistic_and_render.py`
- Multiple output directories: `frames_cycles/`, `frames_cycles_photorealistic/`, `frames_eevee/`

✅ **New (centralized)**:
- `render_service.py` - Single unified service
- `render.sh` - Simple wrapper for common use cases
- Single output pattern: `renders/{config}_{timestamp}/`

## Parameters

### 1. Engine (`--engine`)

| Engine | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| `EEVEE` | ⚡⚡⚡ Fast | Good | Quick previews, drafts |
| `CYCLES` | 🐌 Slow | Excellent | Production, photorealism |

**Default**: `CYCLES`

### 2. Quality (`--quality`)

| Preset | Samples | Resolution | Time/Frame | Use Case |
|--------|---------|------------|------------|----------|
| `draft` | 32 | 50% | ~0.5s | Quick iteration |
| `preview` | 64 | 75% | ~2s | Review animation |
| `production` | 128 | 100% | ~10s | **Recommended for final** |
| `final` | 256 | 100% | ~20s | Maximum quality |

**Default**: `production`

### 3. Materials (`--materials`)

| Style | Description | Use Case |
|-------|-------------|----------|
| `default` | Scene materials as-is | Use existing setup |
| `photorealistic` | Chrome text, polished floor, glowing explosions | **Recommended** |
| `clay` | Simple matte materials | Lighting tests |

**Default**: `photorealistic`

### 4. Frame Range

```bash
# Render specific frames
bash scripts/render.sh CYCLES production --start 60 --end 120

# Single frame test
bash scripts/render.sh CYCLES production --start 120 --end 120
```

**Default**: `--start 1 --end 240` (full 10-second animation)

### 5. Output Name

```bash
# Custom output directory name
bash scripts/render.sh CYCLES production --output-name test_render_v2
```

**Default**: Auto-generated `{engine}_{quality}_{materials}_{timestamp}`

## Usage Examples

### Common Workflows

```bash
# 1. Quick check (30 seconds)
bash scripts/render.sh quick --start 1 --end 30

# 2. Preview full animation (15 minutes)
bash scripts/render.sh preview

# 3. Production render (45 minutes) ⭐ RECOMMENDED
bash scripts/render.sh production

# 4. Test single frame for quality
bash scripts/render.sh CYCLES production --start 120 --end 120

# 5. EEVEE fast preview (4 minutes)
bash scripts/render.sh EEVEE preview

# 6. Clay render for lighting (testing)
bash scripts/render.sh CYCLES preview clay
```

### Advanced Configuration

```bash
# Manual full control
bash scripts/render.sh CYCLES final photorealistic --start 1 --end 240

# Custom output name
bash scripts/render.sh CYCLES production --output-name final_render_v3

# Specific frame range with custom materials
bash scripts/render.sh CYCLES production default --start 100 --end 150
```

## Output Structure

```
projects/dadosfera/renders/
├── cycles_production_photorealistic_20251001_1430/
│   ├── frame_0001.png
│   ├── frame_0002.png
│   └── ...
├── cycles_final_photorealistic_20251001_1500/
├── eevee_draft_default_20251001_1445/
└── ...

render_logs/
├── render_20251001_1430.log
├── render_20251001_1500.log
└── ...
```

## Encode to Video

After rendering frames:

```bash
# Navigate to output directory
cd projects/dadosfera/renders/cycles_production_photorealistic_20251001_1430/

# Encode to H.264 video
ffmpeg -framerate 24 -i frame_%04d.png \
  -c:v libx264 -preset slow -crf 18 \
  -pix_fmt yuv420p -movflags +faststart \
  ../../exports/dadosfera_production_$(date +%Y%m%d).mp4
```

Or use the helper script:

```bash
# From project root
bash scripts/encode_frames_to_video.sh \
  projects/dadosfera/renders/cycles_production_photorealistic_20251001_1430 \
  projects/dadosfera/exports/dadosfera_production_20251001.mp4
```

## Performance Guide

### Render Times (240 frames @ 1920x1080)

| Configuration | Time/Frame | Total Time | File Size |
|---------------|------------|------------|-----------|
| EEVEE draft | 0.3s | ~2 min | ~100MB |
| EEVEE preview | 0.5s | ~4 min | ~300MB |
| CYCLES draft | 1s | ~4 min | ~200MB |
| CYCLES preview | 3s | ~15 min | ~500MB |
| **CYCLES production** ⭐ | **10s** | **~45 min** | **~900MB** |
| CYCLES final | 20s | ~2 hours | ~1.5GB |

**Hardware**: Apple M3 Max, Metal GPU

### Optimization Tips

1. **Test first**: Always render 1-5 frames first to verify settings
2. **Use draft for iteration**: Quick tests with `draft` quality
3. **Production for finals**: Use `production` quality (128 samples) for delivery
4. **Final only if needed**: `final` (256 samples) for extreme quality needs
5. **Frame range**: Render specific problematic frames separately

## Troubleshooting

### Issue: Render too slow
**Solution**: 
```bash
# Use lower quality
bash scripts/render.sh CYCLES preview

# Or reduce samples in render_service.py
```

### Issue: Need higher quality
**Solution**:
```bash
# Use final preset
bash scripts/render.sh final

# Or custom samples (edit render_service.py QUALITY_PRESETS)
```

### Issue: Materials not showing
**Solution**:
```bash
# Ensure using photorealistic materials
bash scripts/render.sh CYCLES production photorealistic
```

### Issue: Out of memory
**Solution**:
```bash
# Use lower resolution
bash scripts/render.sh CYCLES draft  # 50% resolution
```

## Integration with CI/CD

The render service can be automated:

```bash
#!/bin/bash
# Automated render pipeline

# 1. Render
bash scripts/render.sh production

# 2. Get latest render directory
RENDER_DIR=$(ls -td projects/dadosfera/renders/cycles_production_* | head -1)

# 3. Encode
bash scripts/encode_frames_to_video.sh "$RENDER_DIR" \
  projects/dadosfera/exports/dadosfera_auto_$(date +%Y%m%d).mp4

# 4. Upload (example)
# aws s3 cp projects/dadosfera/exports/*.mp4 s3://bucket/
```

## Development

### Adding New Quality Presets

Edit `scripts/render_service.py`:

```python
QUALITY_PRESETS = {
    'custom_high': {
        'samples': 512,
        'resolution_percentage': 100,
        'description': 'Ultra high quality'
    },
    # ...
}
```

### Adding New Material Styles

Edit `scripts/render_service.py`:

```python
MATERIAL_STYLES = {
    'glass': 'Transparent glass materials',
    # ...
}

# Then implement in RenderService._apply_glass_materials()
```

## Migration from Old Scripts

If you have old render commands:

| Old | New |
|-----|-----|
| `bash scripts/render_photorealistic.sh CYCLES` | `bash scripts/render.sh production` |
| `blender -b -P render_dadosfera.py -- EEVEE` | `bash scripts/render.sh EEVEE production` |
| Custom frame dirs | Auto-generated consistent naming |

## Summary

✅ **Single service** instead of multiple scattered scripts  
✅ **Parameterized** for all use cases (draft → final)  
✅ **Consistent naming** for outputs  
✅ **Simple CLI** with presets and manual control  
✅ **Production-ready** with logging and error handling  

**Recommended workflow**:
1. Test: `bash scripts/render.sh quick --start 1 --end 10`
2. Preview: `bash scripts/render.sh preview`
3. **Production**: `bash scripts/render.sh production` ⭐
4. Encode to video
5. Deliver

