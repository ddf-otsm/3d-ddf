"""Blender server for processing 3D operations."""

import asyncio
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, Optional

from .config import settings
from .exceptions import BlenderError, ProcessingTimeoutError
from .logging import get_logger
from .utils import ensure_directory_exists

logger = get_logger(__name__)


class BlenderServer:
    """Manages Blender subprocess for 3D operations."""

    def __init__(self, blender_executable: Optional[str] = None):
        self.blender_executable = blender_executable or settings.blender_executable or "blender"
        self.temp_dir = Path(tempfile.mkdtemp(prefix="logo3d_blender_"))
        self.process: Optional[subprocess.Popen] = None
        self._cleanup_temp_dirs()

        ensure_directory_exists(self.temp_dir)
        logger.info(f"Initialized Blender server with temp dir: {self.temp_dir}")

    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except (subprocess.TimeoutExpired, OSError):
                try:
                    self.process.kill()
                except OSError:
                    pass
            self.process = None

        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp dir {self.temp_dir}: {e}")

    def _cleanup_temp_dirs(self):
        """Clean up old temporary directories."""
        import glob
        temp_base = Path(tempfile.gettempdir())
        pattern = str(temp_base / "logo3d_blender_*")

        for temp_dir_path in glob.glob(pattern):
            temp_dir = Path(temp_dir_path)
            try:
                # Only cleanup directories older than 1 hour
                if temp_dir.exists() and temp_dir.is_dir():
                    stat = temp_dir.stat()
                    age_hours = (time.time() - stat.st_mtime) / 3600
                    if age_hours > 1:
                        import shutil
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        logger.debug(f"Cleaned up old temp dir: {temp_dir}")
            except Exception as e:
                logger.debug(f"Failed to cleanup {temp_dir}: {e}")

    async def process_request_async(self, script_path: Path, timeout: int = 300) -> Dict[str, any]:
        """
        Process a Blender script asynchronously.

        Args:
            script_path: Path to the Python script to execute in Blender
            timeout: Maximum processing time in seconds

        Returns:
            Dict containing processing results

        Raises:
            ProcessingTimeoutError: If processing takes too long
            BlenderError: If Blender execution fails
        """
        return await asyncio.get_event_loop().run_in_executor(
            None, self.process_request, script_path, timeout
        )

    def process_request(self, script_path: Path, timeout: int = 300) -> Dict[str, any]:
        """
        Process a Blender script synchronously.

        Args:
            script_path: Path to the Python script to execute in Blender
            timeout: Maximum processing time in seconds

        Returns:
            Dict containing processing results

        Raises:
            ProcessingTimeoutError: If processing takes too long
            BlenderError: If Blender execution fails
        """
        if not script_path.exists():
            raise BlenderError(f"Script file not found: {script_path}")

        # Prepare command
        cmd = [
            self.blender_executable,
            "--background",  # Run without UI
            "--python", str(script_path)  # Execute script
        ]

        logger.info(f"Starting Blender process: {' '.join(cmd)}")

        try:
            # Start Blender process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.temp_dir,
                text=True  # Use text mode for easier string handling
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = self.process.communicate(timeout=timeout)
                returncode = self.process.returncode

            except subprocess.TimeoutExpired:
                logger.error(f"Blender process timed out after {timeout} seconds")
                self.process.kill()
                try:
                    stdout, stderr = self.process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    self.process.terminate()
                    raise ProcessingTimeoutError(timeout)

                raise ProcessingTimeoutError(timeout)

            # Check return code
            if returncode != 0:
                error_msg = f"Blender process failed with return code {returncode}"
                if stderr:
                    error_msg += f"\nStderr: {stderr}"
                logger.error(error_msg)
                raise BlenderError(error_msg, blender_output=stderr)

            logger.info("Blender process completed successfully")
            return {
                "success": True,
                "stdout": stdout,
                "stderr": stderr,
                "returncode": returncode,
                "script_path": str(script_path),
                "temp_dir": str(self.temp_dir)
            }

        except FileNotFoundError:
            error_msg = f"Blender executable not found: {self.blender_executable}"
            logger.error(error_msg)
            raise BlenderError(error_msg)

        except Exception as e:
            error_msg = f"Unexpected error running Blender: {e}"
            logger.error(error_msg)
            raise BlenderError(error_msg)

    def create_blender_script(self, operations: list) -> Path:
        """
        Create a Blender Python script from a list of operations.

        Args:
            operations: List of operation dictionaries

        Returns:
            Path to the created script file
        """
        script_content = self._generate_script_content(operations)
        script_path = self.temp_dir / f"blender_script_{int(time.time())}.py"

        with open(script_path, 'w') as f:
            f.write(script_content)

        logger.debug(f"Created Blender script: {script_path}")
        return script_path

    def _generate_script_content(self, operations: list) -> str:
        """Generate Python script content for Blender operations."""
        script_lines = [
            "#!/usr/bin/env python3",
            '"""Auto-generated Blender script for Logo to 3D processing."""',
            "",
            "import bpy",
            "import sys",
            "import traceback",
            "",
            "def main():",
            '    """Main processing function."""',
            "    try:",
            "        # Clear scene",
            "        bpy.ops.wm.read_homefile(use_empty=True)",
            "",
        ]

        # Add operations
        for operation in operations:
            op_type = operation.get("type", "")
            params = operation.get("params", {})

            if op_type == "import_svg":
                script_lines.extend(self._generate_svg_import(params))
            elif op_type == "extrude_mesh":
                script_lines.extend(self._generate_extrusion(params))
            elif op_type == "apply_material":
                script_lines.extend(self._generate_material(params))
            elif op_type == "setup_lighting":
                script_lines.extend(self._generate_lighting(params))
            elif op_type == "export_mesh":
                script_lines.extend(self._generate_export(params))
            else:
                logger.warning(f"Unknown operation type: {op_type}")

        # Add error handling and cleanup
        script_lines.extend([
            "",
            '        print("SUCCESS: Processing completed")',
            "        return 0",
            "",
            "    except Exception as e:",
            '        print(f"ERROR: {e}", file=sys.stderr)',
            '        traceback.print_exc(file=sys.stderr)',
            "        return 1",
            "",
            "if __name__ == '__main__':",
            "    sys.exit(main())"
        ])

        return "\n".join(script_lines)

    def _generate_svg_import(self, params: dict) -> list:
        """Generate SVG import code."""
        svg_path = params.get("svg_path", "")
        return [
            f"        # Import SVG",
            f"        bpy.ops.import_curve.svg(filepath='{svg_path}')",
            "",
        ]

    def _generate_extrusion(self, params: dict) -> list:
        """Generate mesh extrusion code."""
        depth = params.get("depth", 0.1)
        bevel_depth = params.get("bevel_depth", 0.01)
        resolution = params.get("resolution", 12)

        return [
            f"        # Convert curves to mesh and extrude",
            f"        bpy.ops.object.select_all(action='SELECT')",
            f"        bpy.ops.object.convert(target='MESH')",
            f"",
            f"        # Enter edit mode for extrusion",
            f"        bpy.ops.object.mode_set(mode='EDIT')",
            f"        bpy.ops.mesh.select_all(action='SELECT')",
            f"        bpy.ops.mesh.extrude_region_move(",
            f"            TRANSFORM_OT_translate={{'value': (0, 0, {depth})}}",
            f"        )",
            f"",
            f"        # Add bevel",
            f"        bpy.ops.mesh.bevel(",
            f"            offset={bevel_depth},",
            f"            offset_type='OFFSET',",
            f"            segments={resolution}",
            f"        )",
            f"",
            f"        # Exit edit mode",
            f"        bpy.ops.object.mode_set(mode='OBJECT')",
            f"",
        ]

    def _generate_material(self, params: dict) -> list:
        """Generate material application code."""
        material_name = params.get("name", "LogoMaterial")
        base_color = params.get("base_color", [0.8, 0.8, 0.8, 1.0])

        return [
            f"        # Create and apply material",
            f"        mat = bpy.data.materials.new(name='{material_name}')",
            f"        mat.use_nodes = True",
            f"        nodes = mat.node_tree.nodes",
            f"        principled = nodes.get('Principled BSDF')",
            f"        if principled:",
            f"            principled.inputs['Base Color'].default_value = {base_color}",
            f"",
            f"        # Apply to selected objects",
            f"        for obj in bpy.context.selected_objects:",
            f"            if obj.type == 'MESH':",
            f"                obj.data.materials.append(mat)",
            f"",
        ]

    def _generate_lighting(self, params: dict) -> list:
        """Generate lighting setup code."""
        return [
            f"        # Setup basic lighting",
            f"        # Add a sun light",
            f"        bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))",
            f"        sun = bpy.context.active_object",
            f"        sun.data.energy = 5.0",
            f"",
            f"        # Add environment lighting",
            f"        world = bpy.context.scene.world",
            f"        world.use_nodes = True",
            f"        bg = world.node_tree.nodes.get('Background')",
            f"        if bg:",
            f"            bg.inputs['Strength'].default_value = 0.5",
            f"",
        ]

    def _generate_export(self, params: dict) -> list:
        """Generate export code."""
        format_type = params.get("format", "obj")
        output_path = params.get("output_path", "output.obj")

        if format_type.lower() == "obj":
            export_cmd = f"        bpy.ops.export_scene.obj(filepath='{output_path}', use_selection=True)"
        elif format_type.lower() == "fbx":
            export_cmd = f"        bpy.ops.export_scene.fbx(filepath='{output_path}', use_selection=True)"
        elif format_type.lower() in ["gltf", "glb"]:
            export_cmd = f"        bpy.ops.export_scene.gltf(filepath='{output_path}', use_selection=True, export_format='GLB')"
        else:
            export_cmd = f"        # Unsupported format: {format_type}"

        return [
            f"        # Export result",
            f"        {export_cmd}",
            f"",
        ]

    def is_blender_available(self) -> bool:
        """Check if Blender executable is available."""
        try:
            result = subprocess.run(
                [self.blender_executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def get_blender_version(self) -> Optional[str]:
        """Get Blender version string."""
        try:
            result = subprocess.run(
                [self.blender_executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Extract version from first line
                first_line = result.stdout.strip().split('\n')[0]
                return first_line
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        return None


# Global Blender server instance
_blender_server: Optional[BlenderServer] = None


def get_blender_server() -> BlenderServer:
    """Get the global Blender server instance."""
    global _blender_server
    if _blender_server is None:
        _blender_server = BlenderServer()
    return _blender_server


def reset_blender_server():
    """Reset the global Blender server (for testing)."""
    global _blender_server
    if _blender_server:
        _blender_server.cleanup()
    _blender_server = None

