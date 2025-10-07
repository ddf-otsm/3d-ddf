# Explosion Test Project

## Overview
This project contains test scenes, renders, and exports for developing and validating the 3D-DDF explosion system. It includes various explosion test scenarios, rendering experiments, and showcases of the explosion technology.

## Project Structure

```
explosion-test/
├── blender_files/          # Blender scene files for testing explosion techniques
│   ├── explosion_test_scene.blend
│   ├── hybrid_quick_test.blend
│   └── realistic_explosion_test.blend
├── exports/                # Final video exports following project taxonomy
│   ├── explosion_test_alpha_20251002_1080p_showcase.mp4  # Latest showcase demo
│   ├── frames_showcase_20251002/                         # Frame exports
│   └── README.md           # Export documentation and metadata
├── renders/                # Rendered output from explosion tests
│   ├── hybrid_test_20251002_0017/     # Hybrid particle+volume tests
│   ├── multilayer_test_20251001_2158/ # Multi-layer rendering tests
│   ├── realistic_test_20251001_2218/  # Realistic explosion tests
│   └── README.md          # Render batch documentation
├── logs/                   # Render logs and system logs
│   └── render_*.log
└── RENDER_BATCHES.md      # Historical render batches and results
```

## Recent Exports

### 🎬 Latest Showcase (October 2, 2025)
- **File**: `explosion_test_alpha_20251002_1080p_showcase.mp4`
- **Duration**: 3.1 seconds
- **Resolution**: 1920×1080 (Full HD)
- **Features**:
  - 4 explosions with different quality presets
  - 112 explosion objects (particles, debris, smoke)
  - Professional lighting and cinematic camera
  - Cycles renderer with GPU acceleration
  - Real-time denoising for clean output

### 📊 Technical Specifications
| Feature | Details |
|---------|---------|
| **Explosions** | 4 (quick, medium, high quality) |
| **Objects** | 112 (particles, debris, smoke volumes) |
| **Render Engine** | Cycles (GPU accelerated) |
| **Samples** | 256 (production quality) |
| **Denoising** | OIDN/Optix |
| **File Size** | 249KB (efficient H.264) |

## Current Status
- **✅ Production Ready**: Explosion system validated and tested
- **✅ 100% Test Pass Rate**: All non-Blender tests passing
- **🔄 Active Development**: Performance optimization and user feedback
- **📚 Documentation Complete**: Comprehensive guides and examples

## Development Focus
- **Core System**: Hybrid particle + volume explosion rendering
- **Quality Presets**: Quick (10 particles), Medium (20 particles), High (30 particles)
- **Performance**: LOD optimization for distant explosions
- **Integration**: Seamless integration with main 3D-DDF projects

## Related Documentation
- [📋 Explosion System Overview](../../scripts/explosions/README.md)
- [🎯 Active Plans](../../docs/plans/active/explosion-development-roadmap.md)
- [🧪 Test Results](../../docs/project/test_pass_summary_20251002.md)
- [📖 Explosion Creation Guide](../../docs/guides/explosion-creation.md)
- [⚙️ Configuration Guide](../../scripts/explosions/config.py)

## Usage Examples

### Create Explosion Video
```bash
# In Blender
python scripts/create_explosion_video.py --quality production --duration 150

# Command line (requires Blender in PATH)
blender --background --python scripts/create_explosion_video.py --
```

### Test Explosion System
```bash
# Run all tests
pytest tests/ -v -m "not blender"

# Run explosion-specific tests
pytest tests/explosions/ -v
```

### Analyze Explosions
```bash
# Analyze current explosion objects
python scripts/analyze_explosion_realism.py

# Check explosion configuration
python scripts/check_explosion_objects.py
```

## Version History

| Version | Date | Description |
|---------|------|-------------|
| **alpha** | 2025-10-02 | Initial showcase release with 4 explosion types |
| **beta** | TBD | Performance optimizations and user feedback |
| **stable** | TBD | Production-ready with full documentation |

## Contact
- **Lead Developer**: Visual Effects Team
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: See `docs/` for comprehensive guides


