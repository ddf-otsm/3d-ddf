# Dadosfera Project Structure

## Directory Organization

```
projects/dadosfera/
├── blender_files/              # Blender scene files
│   └── dadosfera_animation_v1.blend
│
├── renders/                    # Rendered output frames
│   ├── frames_cycles_photorealistic/  # High-quality CYCLES renders
│   ├── frames_cycles/                 # Standard CYCLES renders
│   └── frames_eevee/                  # Fast EEVEE renders
│
├── exports/                    # Final encoded videos
│   ├── dadosfera_CYCLES_PHOTOREALISTIC_*.mp4
│   ├── dadosfera_alpha_*.mp4
│   └── dadosfera_deprecated_*.mp4
│
└── documentation/              # Project documentation
    └── PROJECT_SUMMARY.md
```

## File Naming Conventions

### Blender Files
- **Format**: `{project}_{type}_v{version}.blend`
- **Example**: `dadosfera_animation_v1.blend`

### Rendered Frames
- **Location**: `renders/frames_{engine}_{variant}/`
- **Format**: `frame_{####}.png`
- **Example**: `frames_cycles_photorealistic/frame_0120.png`

### Video Exports
- **Format**: `{project}_{variant}_{date}_{quality}_{type}.mp4`
- **Examples**:
  - `dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4`
  - `dadosfera_alpha_20250930_1080p_partial_8sec.mp4`
  - `dadosfera_deprecated_20250930_720p_preview.mp4`

## Render Scripts

### Quick Start
```bash
# Photorealistic CYCLES render (recommended)
bash scripts/render_photorealistic.sh CYCLES

# Fast EEVEE preview
bash scripts/render_photorealistic.sh EEVEE

# Encode frames to video
bash scripts/encode_frames_to_video.sh cycles_photorealistic
```

### Script Locations
- `scripts/render_photorealistic.sh` - Main render orchestration
- `scripts/apply_photorealistic_and_render.py` - Material setup + rendering
- `scripts/encode_frames_to_video.sh` - FFmpeg video encoding

## Scene Details

### Animation Specifications
- **Duration**: 10 seconds (240 frames @ 24fps)
- **Resolution**: 1920x1080 (Full HD)
- **Camera**: Helicopter orbit around text
- **Effects**: Red circle explosions with emission glow

### Objects
- `Dadosfera_Text` - 3D extruded text with chrome material
- `Ground_Plane` - Polished dark floor with reflections
- `Explosion_*` - Animated red glowing circles
- `Helicopter_Camera` - Orbiting camera with keyframes

### Materials (Photorealistic)
- **Floor**: Polished dark surface (Roughness: 0.15)
- **Text**: Chrome cyan metal (Metallic: 1.0, Roughness: 0.05)
- **Explosions**: Bright emission (Strength: 30.0)

## Render Profiles

### CYCLES Photorealistic
- **Samples**: 128
- **Denoising**: OpenImageDenoise
- **GPU**: Apple M3 Max (Metal)
- **Speed**: ~4 seconds/frame
- **Total time**: ~16 minutes for 240 frames

### EEVEE Fast
- **Quality**: Good
- **GPU**: Automatic (Metal)
- **Speed**: ~1 second/frame
- **Total time**: ~4 minutes for 240 frames

## Version History

### v1 (Current)
- Initial animation with helicopter camera
- Photorealistic CYCLES materials
- Red explosion effects
- 10-second loop (240 frames)

## Next Steps

1. **Review render quality**: Check `dadosfera_CYCLES_PHOTOREALISTIC_*.mp4`
2. **Iterate materials**: Adjust roughness, metallic values if needed
3. **Add more effects**: Particles, motion blur, depth of field
4. **Optimize**: Reduce samples for faster iteration
5. **Final render**: High-quality 4K version for production

## Troubleshooting

### Issue: Render shows only a cube
**Solution**: Ensure `render_photorealistic.sh` loads the correct scene file:
```bash
SCENE_FILE="projects/dadosfera/blender_files/dadosfera_animation_v1.blend"
```

### Issue: Materials not showing
**Solution**: Use CYCLES engine, not viewport render. Check `apply_photorealistic_and_render.py` sets:
```python
scene.render.engine = 'CYCLES'
```

### Issue: Slow render
**Solution**: Reduce samples in `apply_photorealistic_and_render.py`:
```python
scene.cycles.samples = 64  # Instead of 128
```

## References

- **Target URL**: `dadosfera.alpha.dadosfera.info`
- **Release**: ALPHA (partial render, 8 seconds)
- **Documentation**: `documentation/PROJECT_SUMMARY.md`

