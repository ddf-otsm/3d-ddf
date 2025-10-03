# Explosion Creation Guide

## Overview
The 3D-DDF explosion system uses a hybrid approach combining particle systems for fire and debris with volume shaders for smoke. This provides realistic explosions without the need for time-consuming physics baking. The system supports multiple quality presets and is fully configurable via JSON.

Key Features:
- **Hybrid Rendering**: Particles + Volumes for balanced performance/quality
- **Quality Presets**: Quick (testing), Medium (production), High (final renders)
- **Multiple Explosions**: Up to 8 simultaneous explosions with independent timing
- **Material Library**: Pre-built fire, smoke, and debris materials
- **Animation System**: Automatic keyframing for explosion lifecycle
- **GPU Optimized**: Designed for M3 Max with MetalRT acceleration

## Prerequisites
- Blender 4.5.3+ (installed via `/Applications/Blender.app`)
- Python 3.10+ with required packages (see `integrations/requirements.txt`)
- Access to the 3D-DDF workspace

## Step-by-Step Guide

### 1. Setup
1. Navigate to the project root: `cd /Users/luismartins/local_repos/3d-ddf`
2. Activate the environment: `source integrations/env.final` (or equivalent)
3. Open Blender: `/Applications/Blender.app/Contents/MacOS/Blender`

### 2. Load Scene
- For testing: Open `projects/explosion-test/blender_files/hybrid_quick_test.blend`
- For production: Open `projects/dadosfera/blender_files/dadosfera_animation_v2_hybrid_explosions.blend`

### 3. Create Explosions
Use the production script for automated creation:

```bash
cd /Users/luismartins/local_repos/3d-ddf
/Applications/Blender.app/Contents/MacOS/Blender your_scene.blend --background --python scripts/explosions/integrate_with_main_project.py
```

This will:
- Clear existing explosion objects
- Create 5 configured explosions (title, action, background)
- Apply materials and animations
- Save as `v2_hybrid_explosions.blend`

### 4. Configure Explosions
Edit `projects/dadosfera/config/explosion_config.json` to customize:

**Parameters Reference**:
- `id`: Unique identifier (string)
- `name`: Explosion name prefix (string, e.g., "Dadosfera_Title_Explosion")
- `location`: [x, y, z] position in world coordinates (array of floats)
- `start_frame`: Animation start frame (integer, default 1)
- `duration`: Explosion length in frames (integer, default 60)
- `intensity`: Scale factor for particles/volume (float 0.0-2.0, default 1.0)
- `quality_preset`: "quick", "medium", "high" (string)
- `fire_particles`: Number of fire particles (integer, 10-50)
- `debris_particles`: Number of debris particles (integer, 5-20)
- `color_bias`: Fire color variation ("orange", "red", "yellow", "blue", "green") (string)

**Render Settings**:
- `quality`: Overall render quality (string)
- `samples`: Cycles samples per pixel (integer, 128-512)
- `resolution`: [width, height] (array, default [1920, 1080])
- `engine`: "CYCLES" or "EEVEE" (string, default "CYCLES")

Example for a single large explosion:
```json
{
  "explosions": [
    {
      "id": "big_boom",
      "name": "Large_Explosion",
      "location": [0, 0, 2],
      "start_frame": 50,
      "duration": 120,
      "intensity": 1.5,
      "quality_preset": "high",
      "fire_particles": 40,
      "debris_particles": 20,
      "color_bias": "red"
    }
  ],
  "render_settings": {
    "quality": "high",
    "samples": 512,
    "resolution": [1920, 1080]
  }
}
```

### 5. Render Explosions
Use the unified render service:

```bash
cd /Users/luismartins/local_repos/3d-ddf
/Applications/Blender.app/Contents/MacOS/Blender your_scene.blend --background \
  -o "projects/dadosfera/renders/my_render/####" \
  -f 1-240 \
  -P scripts/render_service.py \
  -- --engine CYCLES --quality production --materials photorealistic
```

- **Quality Options**: `draft` (32 samples, fast), `preview` (64), `production` (128), `final` (256)
- **Materials**: `default`, `photorealistic` (recommended), `clay` (lighting test)
- **Output**: PNG frames + automatic MP4 encoding

### 6. Video Encoding
The render service auto-encodes videos:
- Codec: H.264 (CRF 18 for high quality)
- FPS: 24 (matches animation)
- Output: `projects/dadosfera/exports/scene_name.mp4`

Manual encoding if needed:
```bash
cd /Users/luismartins/local_repos/3d-ddf
scripts/encode_frames_to_video.sh projects/dadosfera/renders/my_render/ projects/dadosfera/exports/my_video.mp4
```

## Integration with Dadosfera Project
1. Load `dadosfera_animation_v2_hybrid_explosions.blend`
2. Verify explosions: Play animation (frames 1-240)
3. Adjust timing via JSON and re-run integration script
4. Render full sequence: Use `--start 1 --end 240` for 10-second video
5. Key explosion timings:
   - Frame 1: Title explosion (high quality, center)
   - Frame 60: Background #1 (quick, left)
   - Frame 120: Action #1 (medium, left)
   - Frame 180: Action #2 (medium, right)
   - Frame 200: Background #2 (quick, right)

## Troubleshooting
- **Black Smoke**: Increase `smoke_density` to 0.9 in materials.py or config
- **Slow Rendering**: Use `EEVEE` engine or reduce `fire_particles` to 15
- **Memory Errors**: Lower `render_samples` to 128; ensure GPU is selected in Blender preferences
- **No Explosions Visible**: Check frame range; ensure `start_frame` aligns with camera path
- **Particle Clumping**: Increase `fire_velocity` to 2.5 in config
- **Color Issues**: Adjust `color_bias` or `fire_color_temperature` (0.0=hot red, 1.0=white)

Common Fixes:
- Clear cache: `bpy.ops.wm.read_factory_settings(use_empty=True)`
- Reset materials: Re-run `ExplosionMaterials()` in Blender console
- Validate config: Use `python scripts/explosions/config.py` to test JSON parsing

## Performance Tips
- **Target**: <15s/frame on M3 Max
- **Optimizations**: Enable MetalRT in Blender > Preferences > System
- **LOD**: Distant explosions auto-reduce particles (built into script)
- **Batch Render**: Use `--background` mode for headless rendering

## Version History
- v1.0: Initial hybrid system (Oct 2, 2025)
- v1.1: JSON config support
- v1.5-beta: Full Dadosfera integration

For issues, check `logs/` or contact the 3D-DDF team.
