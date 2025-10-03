# Render Service Consolidation

## Problem

Before consolidation, the project had:

❌ **5 different render scripts** doing similar things:
- `scripts/render_dadosfera.py`
- `scripts/render_dadosfera_from_file.py`
- `scripts/render_photorealistic.sh`
- `scripts/apply_photorealistic_and_render.py`
- `scripts/setup_photorealistic_render.py`

❌ **3+ output directories** with inconsistent naming:
- `renders/frames_cycles/`
- `renders/frames_cycles_photorealistic/`
- `renders/frames_eevee/`

❌ **Scattered logic**:
- Material application in multiple places
- Duplicate render setup code
- No standardized parameters
- Difficult to maintain

## Solution

✅ **Single unified render service** with parameters:

### Architecture

```
scripts/
├── render.sh              # Simple CLI wrapper (production, preview, quick, etc.)
└── render_service.py      # Core unified service with all logic

scripts/deprecated/        # Old scripts moved here
└── ...
```

### One Service, Multiple Configurations

**Single point of control**: `render_service.py`

**Configurable via parameters**:
- `--engine`: CYCLES | EEVEE
- `--quality`: draft | preview | production | final
- `--materials`: default | photorealistic | clay
- `--start` / `--end`: Frame range
- `--output-name`: Custom naming
- `--gpu` / `--no-gpu`: GPU control

### Consistent Output

**Pattern**: `renders/{engine}_{quality}_{materials}_{timestamp}/`

**Examples**:
- `renders/cycles_production_photorealistic_20251001_1430/`
- `renders/eevee_draft_default_20251001_1445/`
- `renders/cycles_final_photorealistic_20251001_1500/`

## Usage

### Before (Scattered)

```bash
# Different scripts for different purposes
bash scripts/render_photorealistic.sh CYCLES
python scripts/render_dadosfera.py EEVEE
# Output goes to inconsistent directories
```

### After (Unified)

```bash
# One command, different parameters
bash scripts/render.sh production      # CYCLES production photorealistic
bash scripts/render.sh preview         # CYCLES preview photorealistic
bash scripts/render.sh quick           # EEVEE draft default
bash scripts/render.sh EEVEE draft     # Manual configuration
bash scripts/render.sh CYCLES production photorealistic --start 60 --end 120
```

## Benefits

### 1. Maintainability
- **Single source of truth** for render logic
- Changes in one place affect all render modes
- Easy to add new quality presets or material styles

### 2. Consistency
- **Standardized naming** for all outputs
- Same code paths = predictable results
- Easier to compare renders

### 3. Flexibility
- **Parameterized** for all use cases
- Easy to create custom configurations
- No need to create new scripts

### 4. Documentation
- **One place to document** all render options
- Clear parameter definitions
- Examples for common workflows

## Migration Guide

| Old Command | New Command |
|-------------|-------------|
| `bash scripts/render_photorealistic.sh CYCLES` | `bash scripts/render.sh production` |
| `python scripts/render_dadosfera.py EEVEE` | `bash scripts/render.sh EEVEE production` |
| Custom frame directory setup | `--output-name custom_name` |

## Quality Presets

| Preset | Samples | Resolution | Speed | Use Case |
|--------|---------|------------|-------|----------|
| **draft** | 32 | 50% | ⚡⚡⚡ Fast | Quick iteration |
| **preview** | 64 | 75% | ⚡⚡ Medium | Animation review |
| **production** ⭐ | 128 | 100% | ⚡ Slow | **Final delivery** |
| **final** | 256 | 100% | 🐌 Very slow | Maximum quality |

## Material Styles

| Style | Description |
|-------|-------------|
| **default** | Use existing scene materials as-is |
| **photorealistic** ⭐ | Chrome text, polished floor, glowing explosions (recommended) |
| **clay** | Simple matte for lighting tests |

## Output Organization

### Old Structure (Messy)
```
renders/
├── frames/              # What is this?
├── frames_alpha/        # What render config?
├── frames_cycles/       # Basic cycles?
├── frames_cycles_photorealistic/  # Different from above?
└── frames_eevee/        # Which quality?
```

### New Structure (Clear)
```
renders/
├── cycles_production_photorealistic_20251001_1430/  # Self-documenting!
├── cycles_preview_photorealistic_20251001_1445/
├── eevee_draft_default_20251001_1500/
└── cycles_final_photorealistic_20251001_1530/
```

## Testing

### Test Execution

```bash
# Quick 5-frame test
$ bash scripts/render.sh quick --start 120 --end 125

============================================================================
DADOSFERA RENDER SERVICE
============================================================================

📁 Scene:     .../dadosfera_animation_v1.blend
🎨 Engine:    EEVEE
⚙️  Quality:   draft
🎭 Materials: default
📌 Options:   --start 120 --end 125

✅ RENDER COMPLETE!

📂 Check: projects/dadosfera/renders/eevee_draft_default_20251001_1839/
```

**Result**: ✅ 5 frames rendered in 3 seconds

## Next Steps

### Recommended Workflow

1. **Test**: `bash scripts/render.sh quick --start 1 --end 10`
2. **Preview**: `bash scripts/render.sh preview`
3. **Production**: `bash scripts/render.sh production` ⭐
4. **Encode**: `ffmpeg -framerate 24 -i frame_%04d.png output.mp4`

### Cleanup Old Renders

```bash
# Move old scattered renders to archive
mkdir -p archive/renders_old
mv renders/frames* archive/renders_old/

# Keep only new organized renders
ls renders/  # Should show: {engine}_{quality}_{materials}_{timestamp}/
```

## Summary

### Before
- ❌ 5 different scripts
- ❌ 3+ inconsistent output directories
- ❌ Duplicate code and logic
- ❌ Difficult to maintain and extend

### After
- ✅ 1 unified service (`render_service.py`)
- ✅ 1 simple wrapper (`render.sh`)
- ✅ Consistent, self-documenting output naming
- ✅ Easy to maintain, extend, and use
- ✅ Production-ready with logging and error handling

**Result**: Centralized, professional render pipeline ready for production use.

---

**See**: `projects/dadosfera/RENDER_SERVICE.md` for complete usage documentation.

