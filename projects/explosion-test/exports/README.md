# Explosion Test Exports

This directory contains final video exports and frame sequences from explosion test renders. All files follow the project's standardized taxonomy naming convention.

## 📋 Export Naming Convention

All export files follow this format:
```
{project}_{version}_{date}_{quality}_{type}.{extension}
```

### Component Definitions

| Component | Description | Valid Values |
|-----------|-------------|--------------|
| **{project}** | Project identifier | `explosion-test` |
| **{version}** | Release version | `alpha`, `beta`, `stable`, `deprecated` |
| **{date}** | Creation date | `YYYYMMDD` format |
| **{quality}** | Resolution | `270p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `4k` |
| **{type}** | Export purpose | `final`, `partial`, `test`, `preview`, `viewport`, `showcase` |

## 🎬 Current Exports

### Latest Release (October 2, 2025)

#### Explosion Showcase Demo
- **File**: `explosion_test_alpha_20251002_1080p_showcase.mp4`
- **Size**: 249KB
- **Duration**: 3.1 seconds
- **Resolution**: 1920×1080 (Full HD)
- **Frame Rate**: 24fps
- **Codec**: H.264 (High Quality, CRF 18)

**Features Demonstrated**:
- ✅ 4 explosions with different quality presets
- ✅ 112 explosion objects (particles, debris, smoke)
- ✅ Professional lighting and cinematic camera movement
- ✅ Cycles renderer with GPU acceleration and denoising
- ✅ LOD (Level of Detail) optimization for performance

#### Frame Sequence
- **Directory**: `frames_showcase_20251002/`
- **Count**: 75 frames
- **Format**: PNG (1920×1080)
- **Total Size**: ~110MB

## 📊 Technical Specifications

| Specification | Value |
|---------------|-------|
| **Render Engine** | Cycles (GPU) |
| **Samples** | 256 (production quality) |
| **Denoising** | OIDN/Optix |
| **Lighting** | Sun + Point lights |
| **Camera** | Animated cinematic movement |
| **Quality Presets** | Quick (10 particles), Medium (20), High (30) |

## 🚀 Usage

### View Video Export
```bash
# Open video file
open projects/explosion-test/exports/explosion_test_alpha_20251002_1080p_showcase.mp4

# Or use VLC/Media Player
vlc projects/explosion-test/exports/explosion_test_alpha_20251002_1080p_showcase.mp4
```

### Examine Frames
```bash
# View individual frames
open projects/explosion-test/exports/frames_showcase_20251002/frame_0001.png

# Create contact sheet (requires ImageMagick)
montage projects/explosion-test/exports/frames_showcase_20251002/frame_*.png \
  -tile 8x -geometry +2+2 contact_sheet.png
```

### Re-encode Video (if needed)
```bash
# Re-encode with different settings
ffmpeg -i explosion_test_alpha_20251002_1080p_showcase.mp4 \
  -c:v libx264 -crf 20 -preset slow \
  explosion_test_alpha_20251002_1080p_showcase_high_quality.mp4
```

## 📈 Version History

| Version | Date | Description | Files |
|---------|------|-------------|-------|
| **alpha** | 2025-10-02 | Initial showcase release | 1 video + 75 frames |
| **beta** | TBD | Performance optimizations | TBD |
| **stable** | TBD | Production-ready exports | TBD |

## 🔗 Related Documentation

- [📖 Explosion Creation Guide](../../../docs/guides/explosion-creation.md)
- [🎯 Active Development Plans](../../../docs/plans/active/explosion-development-roadmap.md)
- [🧪 Test Results](../../../docs/project/test_pass_summary_20251002.md)
- [⚙️ Configuration Guide](../../../scripts/explosions/config.py)
- [📋 Project Overview](../README.md)

## 📝 Metadata

**Export Creation Script**: `scripts/create_explosion_video.py`  
**Validation**: All files pass `scripts/validate_taxonomy.py`  
**Quality**: Production-ready for integration testing

---
*Last Updated: October 2, 2025*

