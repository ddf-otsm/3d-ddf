# Rendering Guide

## Rendering Engines

### Cycles (Ray-traced, Photorealistic)

**Best for:**
- Final high-quality renders
- Realistic materials (glass, metal, emission)
- Complex lighting with caustics
- Still images and final animations

**Settings:**
- Samples: 128-512 (higher = better quality, slower)
- Device: GPU (Metal on Apple Silicon)
- Denoiser: OpenImageDenoise (AI-based)

**Render time:**
- ~30-60 seconds per frame on M3 Max @ 128 samples
- ~2-4 hours for 240-frame animation

### EEVEE (Real-time, Fast Preview)

**Best for:**
- Quick previews
- Animation testing
- Viewport rendering
- Fast iteration

**Settings:**
- Resolution: 1280x720 for previews
- Samples: 64-128
- Enable bloom for glowing effects

**Render time:**
- ~1-3 seconds per frame
- ~8-12 minutes for 240-frame animation

## Resolution Settings

| Purpose | Resolution | Aspect Ratio |
|---------|------------|--------------|
| Preview | 1280x720 | 16:9 |
| HD | 1920x1080 | 16:9 |
| 2K | 2560x1440 | 16:9 |
| 4K | 3840x2160 | 16:9 |
| Square (social) | 1080x1080 | 1:1 |

## Rendering Single Frames

### Via Cursor/MCP

Ask Cursor:
```
"Render the current frame at 1920x1080 with 128 samples"
```

### Via Blender Python

```python
import bpy
scene = bpy.context.scene

# Set frame
scene.frame_set(60)

# Configure render
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.cycles.samples = 128

# Render
bpy.ops.render.render(write_still=True)
```

## Rendering Animations

### Render Specific Frames

Ask Cursor:
```
"Render frames 1, 60, 120, 180, and 240 from the animation"
```

### Render Full Animation

```python
import bpy
scene = bpy.context.scene

# Set output path
scene.render.filepath = '/Users/luismartins/local_repos/3d-ddf/projects/my-project/renders/frames/frame_'

# Set format
scene.render.image_settings.file_format = 'PNG'

# Render animation
bpy.ops.render.render(animation=True)
```

### Fast Preview Animation (EEVEE)

```python
import bpy
scene = bpy.context.scene

# Switch to EEVEE
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Lower resolution for speed
scene.render.resolution_x = 1280
scene.render.resolution_y = 720

# Render animation
bpy.ops.render.render(animation=True)
```

## Exporting Videos

### Using FFmpeg

From rendered frame sequence:

```bash
# High quality MP4
ffmpeg -framerate 24 -i projects/my-project/renders/frames/frame_%03d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 \
  projects/my-project/exports/animation.mp4

# Lower quality for previews
ffmpeg -framerate 24 -i projects/my-project/renders/frames/frame_%03d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 23 \
  projects/my-project/exports/animation_preview.mp4

# Quick preview (fast encode)
ffmpeg -framerate 24 -i projects/my-project/renders/frames/frame_%03d.png \
  -c:v libx264 -preset ultrafast -crf 28 \
  projects/my-project/exports/animation_test.mp4
```

## Optimization Tips

### For Fast Previews
- Use EEVEE engine
- Lower resolution (720p)
- Reduce samples (64-128)
- Disable ray-tracing features
- Use simpler materials

### For Final Quality
- Use Cycles engine
- Full resolution (1080p or higher)
- Higher samples (256-512)
- Enable denoising
- Enable caustics for glass
- Use Metal GPU acceleration

### For Animations
1. **Test first**: Render a few key frames to check quality
2. **Preview animation**: Use EEVEE for full animation preview
3. **Optimize scene**: Remove unnecessary objects
4. **Batch render**: Render overnight for long animations
5. **Save incrementally**: Render in chunks if possible

## Quality Settings by Use Case

### Social Media Preview
- Engine: EEVEE
- Resolution: 1080x1080 or 1920x1080
- Samples: 64
- Time: Minutes

### Portfolio/Presentation
- Engine: Cycles
- Resolution: 1920x1080 or 2560x1440
- Samples: 256
- Time: Hours

### Professional/Commercial
- Engine: Cycles
- Resolution: 3840x2160 (4K)
- Samples: 512+
- Time: Many hours

## Performance Expectations

### Apple M3 Max (30 GPU cores)

| Setting | Time per Frame |
|---------|----------------|
| EEVEE 720p | 1-3 seconds |
| EEVEE 1080p | 2-5 seconds |
| Cycles 1080p @ 128 samples | 30-60 seconds |
| Cycles 1080p @ 256 samples | 1-2 minutes |
| Cycles 4K @ 256 samples | 4-8 minutes |
