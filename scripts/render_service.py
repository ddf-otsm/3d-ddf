#!/usr/bin/env python3
"""
Unified Dadosfera Render Service
Single centralized renderer with multiple execution parameters
"""

import bpy
import sys
import time
import argparse
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# ============================================================================
# CONFIGURATION PRESETS
# ============================================================================

QUALITY_PRESETS = {
    'draft': {
        'samples': 32,
        'resolution_percentage': 50,
        'description': 'Fast draft (32 samples, 50% res)'
    },
    'preview': {
        'samples': 64,
        'resolution_percentage': 75,
        'description': 'Quick preview (64 samples, 75% res)'
    },
    'production': {
        'samples': 128,
        'resolution_percentage': 100,
        'description': 'High quality (128 samples, 100% res)'
    },
    'final': {
        'samples': 256,
        'resolution_percentage': 100,
        'description': 'Maximum quality (256 samples, 100% res)'
    }
}

MATERIAL_STYLES = {
    'default': 'Use existing scene materials',
    'photorealistic': 'Apply photorealistic CYCLES materials',
    'clay': 'Simple matte clay materials for lighting tests'
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Dadosfera Unified Render Service',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick draft preview with EEVEE
  blender scene.blend -b -P render_service.py -- --engine EEVEE --quality draft

  # Production photorealistic render
  blender scene.blend -b -P render_service.py -- --engine CYCLES --quality production --materials photorealistic

  # Custom frame range
  blender scene.blend -b -P render_service.py -- --engine CYCLES --quality preview --start 1 --end 120
        """
    )

    parser.add_argument('--engine',
                        choices=['CYCLES', 'EEVEE'],
                        default='CYCLES',
                        help='Render engine (default: CYCLES)')

    parser.add_argument('--quality',
                        choices=list(QUALITY_PRESETS.keys()),
                        default='production',
                        help='Quality preset (default: production)')

    parser.add_argument('--materials',
                        choices=list(MATERIAL_STYLES.keys()),
                        default='photorealistic',
                        help='Material style (default: photorealistic)')

    parser.add_argument('--start',
                        type=int,
                        default=1,
                        help='Start frame (default: 1)')

    parser.add_argument('--end',
                        type=int,
                        default=240,
                        help='End frame (default: 240)')

    parser.add_argument('--output-name',
                        type=str,
                        default=None,
                        help='Custom output name (default: auto-generated)')

    parser.add_argument('--gpu',
                        action='store_true',
                        default=True,
                        help='Use GPU rendering (default: True)')

    # Parse only after '--'
    argv = sys.argv
    if '--' in argv:
        argv = argv[argv.index('--') + 1:]
    else:
        argv = []

    return parser.parse_args(argv)

# ============================================================================
# RENDER SERVICE CLASS
# ============================================================================


class RenderService:
    """Centralized render service with configurable parameters"""

    def __init__(self, args):
        self.args = args
        self.scene = bpy.context.scene
        self.project_root = Path("/Users/luismartins/local_repos/3d-ddf")

        # Generate timestamp FIRST for proper taxonomy
        timestamp = time.strftime("%Y%m%d_%H%M")
        
        # Determine project name from blend file or output_name
        if args.output_name and 'explosion' in args.output_name.lower():
            self.project_name = "explosion_test"
            project_dir = "explosion-test"
        else:
            self.project_name = "dadosfera"
            project_dir = "dadosfera"
        
        # Generate output folder name: {timestamp}_{engine}_{quality}_{materials}
        if args.output_name:
            output_name = args.output_name
        else:
            output_name = f"{timestamp}_{args.engine.lower()}_{args.quality}_{args.materials}"
        
        self.output_dir = self.project_root / f"projects/{project_dir}/renders" / output_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set exports directory based on project
        self.exports_dir = self.project_root / f"projects/{project_dir}/exports"
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        
        # Log file: {timestamp}_render.log
        self.log_file = self.project_root / "logs" / f"{timestamp}_render.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.timestamp = timestamp
        self.start_time = None
        self.frame_times = []

    def log(self, message: str):
        """Write to log file and print"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(line)
        print(line, end="")

    def setup_render_engine(self):
        """Configure the render engine"""
        self.log("\n" + "=" * 70)
        self.log(f"🎨 RENDER ENGINE: {self.args.engine}")
        self.log("=" * 70)

        if self.args.engine == 'CYCLES':
            self.scene.render.engine = 'CYCLES'
            self.scene.cycles.device = 'GPU' if self.args.gpu else 'CPU'

            if self.args.gpu:
                # Configure GPU
                preferences = bpy.context.preferences
                cycles_prefs = preferences.addons['cycles'].preferences
                cycles_prefs.compute_device_type = 'METAL'

                # Enable MetalRT hardware ray-tracing (M3+ optimization)
                if hasattr(cycles_prefs, 'metal_rt'):
                    cycles_prefs.metal_rt = 'ON'
                    self.log(f"   ✅ MetalRT: Enabled (Hardware ray-tracing)")

                cycles_prefs.get_devices()

                gpu_count = 0
                for device in cycles_prefs.devices:
                    if device.type == 'METAL':
                        device.use = True
                        gpu_count += 1
                        self.log(f"   ✅ GPU: {device.name}")

                if gpu_count == 0:
                    self.log("   ⚠️  WARNING: No Metal GPU found, using CPU")

            # Quality settings
            quality = QUALITY_PRESETS[self.args.quality]
            self.scene.cycles.samples = quality['samples']
            self.scene.cycles.use_denoising = True
            self.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
            self.scene.cycles.use_adaptive_sampling = True
            self.scene.cycles.adaptive_threshold = 0.01
            self.scene.cycles.tile_size = 2048

            # Performance optimizations
            self.scene.render.use_persistent_data = True  # Reuse data between frames

            self.log(f"   Samples: {quality['samples']}")
            self.log(f"   Denoising: OpenImageDenoise")
            self.log(f"   Persistent data: Enabled (faster animation)")

        else:  # EEVEE
            self.scene.render.engine = 'BLENDER_EEVEE_NEXT'
            self.log(f"   GPU: Automatic (Metal)")

    def apply_materials(self):
        """Apply material style"""
        if self.args.materials == 'default':
            self.log("\n✅ Using existing scene materials")
            return

        self.log(f"\n🎨 APPLYING {self.args.materials.upper()} MATERIALS")
        self.log("-" * 70)

        if self.args.materials == 'photorealistic':
            self._apply_photorealistic_materials()
        elif self.args.materials == 'clay':
            self._apply_clay_materials()

    def _apply_photorealistic_materials(self):
        """Apply photorealistic materials"""
        material_count = {'floor': 0, 'text': 0, 'explosions': 0}

        # Floor
        ground = bpy.data.objects.get('Ground_Plane')
        if ground and ground.data:
            ground.data.materials.clear()
            floor_mat = bpy.data.materials.new(name="Polished_Floor")
            floor_mat.use_nodes = True
            nodes = floor_mat.node_tree.nodes
            links = floor_mat.node_tree.links
            nodes.clear()

            output = nodes.new('ShaderNodeOutputMaterial')
            bsdf = nodes.new('ShaderNodeBsdfPrincipled')

            bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.15, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Roughness'].default_value = 0.15
            bsdf.inputs['Specular IOR Level'].default_value = 0.6

            links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            ground.data.materials.append(floor_mat)
            material_count['floor'] = 1

        # Text
        dadosfera = bpy.data.objects.get('Dadosfera_Text')
        if dadosfera and dadosfera.data:
            dadosfera.data.materials.clear()
            chrome_mat = bpy.data.materials.new(name="Chrome_Cyan")
            chrome_mat.use_nodes = True
            nodes = chrome_mat.node_tree.nodes
            links = chrome_mat.node_tree.links
            nodes.clear()

            output = nodes.new('ShaderNodeOutputMaterial')
            bsdf = nodes.new('ShaderNodeBsdfPrincipled')

            bsdf.inputs['Base Color'].default_value = (0.7, 0.9, 1.0, 1.0)
            bsdf.inputs['Metallic'].default_value = 1.0
            bsdf.inputs['Roughness'].default_value = 0.05
            bsdf.inputs['Specular IOR Level'].default_value = 1.0
            bsdf.inputs['Coat Weight'].default_value = 0.5

            links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            dadosfera.data.materials.append(chrome_mat)
            material_count['text'] = 1

        # Explosions
        for obj in self.scene.objects:
            if obj.name.startswith('Explosion_') and obj.type == 'MESH' and obj.data:
                obj.data.materials.clear()
                explosion_mat = bpy.data.materials.new(
                    name=f"Explosion_Glow_{material_count['explosions']}")
                explosion_mat.use_nodes = True
                nodes = explosion_mat.node_tree.nodes
                links = explosion_mat.node_tree.links
                nodes.clear()

                output = nodes.new('ShaderNodeOutputMaterial')
                emission = nodes.new('ShaderNodeEmission')

                emission.inputs['Color'].default_value = (1.0, 0.15, 0.0, 1.0)
                emission.inputs['Strength'].default_value = 30.0

                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                obj.data.materials.append(explosion_mat)
                material_count['explosions'] += 1

        # Enhance lights
        for obj in self.scene.objects:
            if obj.type == 'LIGHT':
                obj.data.energy *= 2.0

        self.log(
            f"   ✅ Floor: {material_count['floor']}, Text: {material_count['text']}, Explosions: {material_count['explosions']}")

    def _apply_clay_materials(self):
        """Apply simple matte clay materials"""
        clay_mat = bpy.data.materials.new(name="Clay_Material")
        clay_mat.use_nodes = True
        nodes = clay_mat.node_tree.nodes
        links = clay_mat.node_tree.links
        nodes.clear()

        output = nodes.new('ShaderNodeOutputMaterial')
        bsdf = nodes.new('ShaderNodeBsdfDiffuse')
        bsdf.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)

        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        # Apply to all mesh objects
        count = 0
        for obj in self.scene.objects:
            if obj.type == 'MESH' and obj.data:
                obj.data.materials.clear()
                obj.data.materials.append(clay_mat)
                count += 1

        self.log(f"   ✅ Applied clay material to {count} objects")

    def setup_output(self):
        """Configure output settings"""
        self.log("\n⚙️  OUTPUT SETTINGS")
        self.log("-" * 70)

        # Frame range
        self.scene.frame_start = self.args.start
        self.scene.frame_end = self.args.end

        # Resolution
        quality = QUALITY_PRESETS[self.args.quality]
        self.scene.render.resolution_x = 1920
        self.scene.render.resolution_y = 1080
        self.scene.render.resolution_percentage = quality['resolution_percentage']

        # Output path
        self.scene.render.filepath = str(self.output_dir / "frame_")
        self.scene.render.image_settings.file_format = 'PNG'
        self.scene.render.image_settings.color_mode = 'RGBA'
        self.scene.render.image_settings.compression = 15

        # Color management
        self.scene.view_settings.view_transform = 'Filmic'
        self.scene.view_settings.look = 'High Contrast'

        self.log(
            f"   Resolution: {self.scene.render.resolution_x}x{self.scene.render.resolution_y} @ {quality['resolution_percentage']}%")
        self.log(f"   Frames: {self.args.start}-{self.args.end}")
        self.log(f"   Output: {self.output_dir}")
        self.log(f"   Color: Filmic / High Contrast")

    def setup_handlers(self):
        """Setup render progress handlers"""

        @bpy.app.handlers.persistent
        def on_render_init(dummy):
            self.start_time = time.time()
            self.log("\n" + "=" * 70)
            self.log("🚀 RENDER STARTED")
            self.log("=" * 70)

        @bpy.app.handlers.persistent
        def on_frame_post(dummy):
            current = self.scene.frame_current
            total = self.scene.frame_end - self.scene.frame_start + 1
            progress = ((current - self.scene.frame_start + 1) / total) * 100

            # Calculate ETA
            if len(self.frame_times) > 0:
                avg_time = sum(self.frame_times[-10:]) / len(self.frame_times[-10:])
                remaining = self.scene.frame_end - current
                eta_min = (remaining * avg_time) / 60
                eta_str = f", ETA: {eta_min:.1f}min ({avg_time:.1f}s/frame)"
            else:
                eta_str = ""

            self.log(
                f"✅ Frame {current:04d}/{self.scene.frame_end} ({progress:.1f}%){eta_str}")

            if self.start_time:
                self.frame_times.append(time.time() - self.start_time)

        @bpy.app.handlers.persistent
        def on_render_complete(dummy):
            if self.start_time:
                total_time = time.time() - self.start_time
                minutes = total_time / 60
                avg_time = total_time / \
                    (self.scene.frame_end - self.scene.frame_start + 1)

                self.log("\n" + "=" * 70)
                self.log("✅ RENDER COMPLETE!")
                self.log("=" * 70)
                self.log(f"   Total time: {minutes:.1f} minutes")
                self.log(f"   Avg per frame: {avg_time:.2f} seconds")
                self.log(f"   Output: {self.output_dir}")

        @bpy.app.handlers.persistent
        def on_render_cancel(dummy):
            self.log(f"\n❌ RENDER CANCELLED at frame {self.scene.frame_current}")

        # Clear and set handlers
        bpy.app.handlers.render_pre.clear()
        bpy.app.handlers.render_post.clear()
        bpy.app.handlers.render_complete.clear()
        bpy.app.handlers.render_cancel.clear()

        bpy.app.handlers.render_pre.append(on_render_init)
        bpy.app.handlers.render_post.append(on_frame_post)
        bpy.app.handlers.render_complete.append(on_render_complete)
        bpy.app.handlers.render_cancel.append(on_render_cancel)

    def print_summary(self):
        """Print render configuration summary"""
        self.log("\n" + "=" * 70)
        self.log("RENDER CONFIGURATION SUMMARY")
        self.log("=" * 70)
        self.log(f"Engine:    {self.args.engine}")
        self.log(
            f"Quality:   {self.args.quality} ({QUALITY_PRESETS[self.args.quality]['description']})")
        self.log(
            f"Materials: {self.args.materials} ({MATERIAL_STYLES[self.args.materials]})")
        self.log(f"Frames:    {self.args.start}-{self.args.end}")
        self.log(f"GPU:       {'Enabled' if self.args.gpu else 'Disabled'}")
        self.log(f"Output:    {self.output_dir}")
        self.log(f"Log:       {self.log_file}")

    def encode_video(self):
        """Encode rendered frames to video using FFmpeg"""
        self.log("\n" + "=" * 70)
        self.log("🎬 ENCODING VIDEO")
        self.log("=" * 70)

        # Build output video filename: {project}_{engine}_{quality}_{timestamp}.mp4
        video_name = f"{self.project_name}_{self.args.engine}_{self.args.quality}_{self.timestamp}.mp4"
        video_path = self.exports_dir / video_name

        # FFmpeg command
        frame_pattern = str(self.output_dir / "frame_%04d.png")

        import subprocess

        ffmpeg_cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-framerate', '24',
            '-i', frame_pattern,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '18',  # High quality (lower = better, 18 = visually lossless)
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',  # Enable streaming
            str(video_path)
        ]

        self.log(f"   Input:  {frame_pattern}")
        self.log(f"   Output: {video_path}")
        self.log(f"   Codec:  H.264 (CRF 18, high quality)")
        self.log(f"\n   Running FFmpeg...")

        try:
            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Get video file size
            video_size_mb = video_path.stat().st_size / (1024 * 1024)

            self.log("\n✅ VIDEO ENCODED SUCCESSFULLY!")
            self.log(f"   File: {video_path}")
            self.log(f"   Size: {video_size_mb:.1f} MB")

            return video_path

        except subprocess.CalledProcessError as e:
            self.log(f"\n❌ FFmpeg encoding failed!")
            self.log(f"   Error: {e.stderr}")
            self.log(f"\n⚠️  Frames are still available at: {self.output_dir}")
            self.log(f"   You can manually encode with:")
            self.log(
                f"   ffmpeg -framerate 24 -i {frame_pattern} -c:v libx264 -crf 18 {video_path}")
            return None
        except FileNotFoundError:
            self.log(f"\n❌ FFmpeg not found!")
            self.log(f"   Please install FFmpeg: brew install ffmpeg")
            self.log(f"\n⚠️  Frames are still available at: {self.output_dir}")
            return None

    def render(self):
        """Execute the render"""
        try:
            self.print_summary()
            self.setup_render_engine()
            self.apply_materials()
            self.setup_output()
            self.setup_handlers()

            self.log("\n" + "=" * 70)
            self.log("▶️  STARTING RENDER")
            self.log("=" * 70)

            bpy.ops.render.render('EXEC_DEFAULT', animation=True, write_still=True)

            self.log("\n🎉 Render service execution complete!")

            # Automatically encode to video
            self.encode_video()

        except Exception as e:
            self.log(f"\n❌ RENDER ERROR: {e}")
            import traceback
            self.log(traceback.format_exc())
            sys.exit(1)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    args = parse_args()
    service = RenderService(args)
    service.render()
