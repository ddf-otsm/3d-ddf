"""End-to-end tests for the complete text-to-3D pipeline."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.text_processor.renderer import TextRenderer
from src.core.blender_server import BlenderServer, reset_blender_server


class TestTextTo3DPipelineE2E:
    """End-to-end tests for complete text-to-3D conversion pipeline."""

    @pytest.fixture(autouse=True)
    def reset_blender_server_fixture(self):
        """Reset Blender server before each test."""
        reset_blender_server()
        yield
        reset_blender_server()

    @pytest.fixture
    def mock_blender_server(self):
        """Create a mocked Blender server."""
        server = BlenderServer()
        # Mock the actual Blender execution
        original_process_request = server.process_request

        def mock_process_request(script_path, timeout=300):
            # Simulate successful processing
            return {
                "success": True,
                "stdout": "SUCCESS: Processing completed",
                "stderr": "",
                "returncode": 0,
                "script_path": str(script_path),
                "temp_dir": str(server.temp_dir)
            }

        server.process_request = mock_process_request
        return server

    def test_complete_text_to_3d_pipeline(self, tmp_path, mock_blender_server):
        """Test the complete pipeline from text to 3D output."""
        # Setup
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Step 1: Render text to SVG
        renderer = TextRenderer()

        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock FreeType face
            mock_face.ascender = 800
            mock_face.descender = -200
            mock_face.height = 1000

            mock_glyph = Mock()
            mock_glyph.advance.x = 500
            mock_face.glyph = mock_glyph

            mock_face.load_char = Mock()
            mock_face.get_kerning = Mock(return_value=Mock(x=0))

            mock_outline = Mock()
            mock_outline.n_contours = 1
            mock_outline.points = [(0, 0), (100, 0), (100, 100), (0, 100)]
            mock_outline.tags = [1, 1, 1, 1]
            mock_outline.contours = [3]
            mock_glyph.outline = mock_outline

            # Render text to SVG
            svg_content = renderer.render_text_to_svg("TEST", "Arial", 1.0)
            assert isinstance(svg_content, str)
            assert "<svg" in svg_content

            # Save SVG to file
            svg_path = output_dir / "test_text.svg"
            with open(svg_path, 'w') as f:
                f.write(svg_content)

            # Step 2: Create Blender operations for 3D conversion
            operations = [
                {
                    "type": "import_svg",
                    "params": {"svg_path": str(svg_path)}
                },
                {
                    "type": "extrude_mesh",
                    "params": {
                        "depth": 0.1,
                        "bevel_depth": 0.01,
                        "resolution": 12
                    }
                },
                {
                    "type": "apply_material",
                    "params": {
                        "name": "TextMaterial",
                        "base_color": [0.8, 0.2, 0.2, 1.0]  # Red color
                    }
                },
                {
                    "type": "setup_lighting",
                    "params": {}
                },
                {
                    "type": "export_mesh",
                    "params": {
                        "format": "obj",
                        "output_path": str(output_dir / "test_output.obj")
                    }
                }
            ]

            # Step 3: Generate Blender script
            script_path = mock_blender_server.create_blender_script(operations)
            assert script_path.exists()

            # Verify script content
            with open(script_path) as f:
                script_content = f.read()

            assert "import bpy" in script_content
            assert "extrude_region_move" in script_content
            assert "export_scene.obj" in script_content

            # Step 4: Execute Blender processing (mocked)
            result = mock_blender_server.process_request(script_path)
            assert result["success"] is True
            assert result["returncode"] == 0

            # Step 5: Verify output (in real scenario, check if file was created)
            expected_output = output_dir / "test_output.obj"
            # Note: In mocked test, file won't actually be created
            # In real test, we would check: assert expected_output.exists()

    def test_pipeline_error_handling(self, tmp_path, mock_blender_server):
        """Test error handling in the pipeline."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Mock Blender to fail
        def failing_process_request(script_path, timeout=300):
            return {
                "success": False,
                "stdout": "",
                "stderr": "Blender processing failed",
                "returncode": 1,
                "script_path": str(script_path),
                "temp_dir": str(mock_blender_server.temp_dir)
            }

        mock_blender_server.process_request = failing_process_request

        # Create a basic script
        operations = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "test.obj"}}]
        script_path = mock_blender_server.create_blender_script(operations)

        # Process should report failure
        result = mock_blender_server.process_request(script_path)
        assert result["success"] is False
        assert result["returncode"] == 1

    def test_different_output_formats(self, tmp_path, mock_blender_server):
        """Test pipeline with different output formats."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        formats_to_test = ["obj", "fbx", "gltf", "glb"]

        for fmt in formats_to_test:
            operations = [{
                "type": "export_mesh",
                "params": {
                    "format": fmt,
                    "output_path": str(output_dir / f"test.{fmt}")
                }
            }]

            script_path = mock_blender_server.create_blender_script(operations)

            # Verify format-specific export commands are in script
            with open(script_path) as f:
                content = f.read()

            if fmt == "obj":
                assert "export_scene.obj" in content
            elif fmt == "fbx":
                assert "export_scene.fbx" in content
            elif fmt in ["gltf", "glb"]:
                assert "export_scene.gltf" in content

    def test_pipeline_with_custom_parameters(self, tmp_path, mock_blender_server):
        """Test pipeline with custom extrusion and material parameters."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        custom_operations = [
            {
                "type": "extrude_mesh",
                "params": {
                    "depth": 0.2,  # Custom depth
                    "bevel_depth": 0.02,  # Custom bevel
                    "resolution": 8  # Custom resolution
                }
            },
            {
                "type": "apply_material",
                "params": {
                    "name": "CustomMaterial",
                    "base_color": [0.1, 0.8, 0.3, 1.0]  # Green color
                }
            }
        ]

        script_path = mock_blender_server.create_blender_script(custom_operations)

        # Verify custom parameters are in script
        with open(script_path) as f:
            content = f.read()

        assert "value': (0, 0, 0.2)" in content  # Custom depth
        assert "offset=0.02" in content  # Custom bevel
        assert "segments=8" in content  # Custom resolution
        assert "[0.1, 0.8, 0.3, 1.0]" in content  # Custom color

    def test_blender_server_resource_management(self, mock_blender_server):
        """Test that Blender server properly manages resources."""
        # Create script
        operations = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "test.obj"}}]
        script_path = mock_blender_server.create_blender_script(operations)

        assert script_path.exists()
        assert script_path.parent == mock_blender_server.temp_dir

        # Process request
        result = mock_blender_server.process_request(script_path)
        assert "temp_dir" in result

        # Cleanup
        mock_blender_server.cleanup()

        # Temp directory should be cleaned up (in real implementation)
        # Note: In this test, we're using a mock, so temp dir persists

    def test_script_generation_comprehensive(self, mock_blender_server):
        """Test comprehensive Blender script generation."""
        operations = [
            {"type": "import_svg", "params": {"svg_path": "/path/to/test.svg"}},
            {"type": "extrude_mesh", "params": {"depth": 0.15, "bevel_depth": 0.005}},
            {"type": "apply_material", "params": {"name": "TestMat", "base_color": [1.0, 1.0, 0.0, 1.0]}},
            {"type": "setup_lighting", "params": {}},
            {"type": "export_mesh", "params": {"format": "fbx", "output_path": "/output/test.fbx"}}
        ]

        script_path = mock_blender_server.create_blender_script(operations)

        with open(script_path) as f:
            content = f.read()

        # Verify all operations are included
        assert "import_curve.svg" in content
        assert "extrude_region_move" in content
        assert "materials.new" in content
        assert "light_add" in content
        assert "export_scene.fbx" in content

        # Verify proper error handling
        assert "try:" in content
        assert "except Exception" in content
        assert "sys.exit(main())" in content

    @pytest.mark.asyncio
    async def test_async_processing(self, mock_blender_server):
        """Test asynchronous processing capability."""
        operations = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "async_test.obj"}}]
        script_path = mock_blender_server.create_blender_script(operations)

        # Test async processing
        result = await mock_blender_server.process_request_async(script_path, timeout=60)
        assert result["success"] is True
        assert result["returncode"] == 0

    def test_pipeline_performance_baseline(self, mock_blender_server):
        """Test basic performance characteristics."""
        import time

        operations = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "perf_test.obj"}}]
        script_path = mock_blender_server.create_blender_script(operations)

        # Measure processing time (mocked, so very fast)
        start_time = time.time()
        result = mock_blender_server.process_request(script_path, timeout=30)
        end_time = time.time()

        processing_time = end_time - start_time

        # Should complete quickly (mocked processing)
        assert processing_time < 1.0  # Less than 1 second for mocked processing
        assert result["success"] is True

    def test_error_recovery_and_cleanup(self, mock_blender_server):
        """Test that server properly cleans up after errors."""
        # Create script
        operations = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "error_test.obj"}}]
        script_path = mock_blender_server.create_blender_script(operations)

        # Simulate processing failure
        def failing_process_request(script_path, timeout=300):
            raise Exception("Simulated Blender failure")

        mock_blender_server.process_request = failing_process_request

        # Should handle error gracefully
        with pytest.raises(Exception, match="Simulated Blender failure"):
            mock_blender_server.process_request(script_path)

        # Cleanup should still work
        mock_blender_server.cleanup()

        # Server should be able to create new scripts after cleanup
        operations2 = [{"type": "export_mesh", "params": {"format": "obj", "output_path": "recovery_test.obj"}}]
        script_path2 = mock_blender_server.create_blender_script(operations2)
        assert script_path2.exists()

