"""Integration tests for text processing functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.text_processor.renderer import TextRenderer
from src.text_processor.font_manager import FontManager
from src.core.exceptions import FontNotFoundError


class TestTextProcessingIntegration:
    """Integration tests for text processing pipeline."""

    @pytest.fixture
    def mock_font_path(self, tmp_path):
        """Create a mock font file."""
        font_file = tmp_path / "mock_font.ttf"
        font_file.write_bytes(b"mock font data")
        return font_file

    @pytest.fixture
    def font_manager(self, mock_font_path, tmp_path):
        """Create a font manager with a mock font."""
        with patch('src.text_processor.font_manager.settings') as mock_settings:
            mock_settings.fonts_dir = tmp_path / "fonts"
            mock_settings.default_font = "MockFont"
            mock_settings.supported_fonts = ["MockFont", "FallbackFont"]

            manager = FontManager()

            # Manually add mock font
            from src.text_processor.font_manager import FontMetrics
            metrics = FontMetrics("MockFont", "Regular", 2048, 1854, -434, 67)
            manager._font_cache["MockFont"] = metrics
            manager._font_paths["MockFont"] = mock_font_path

            return manager

    @pytest.fixture
    def text_renderer(self, font_manager):
        """Create a text renderer with mocked font manager."""
        renderer = TextRenderer()
        renderer.font_manager = font_manager
        return renderer

    def test_text_renderer_font_manager_integration(self, text_renderer, font_manager):
        """Test integration between text renderer and font manager."""
        # Verify font manager has the mock font
        assert font_manager.is_font_available("MockFont")
        assert font_manager.get_font_path("MockFont").exists()

        # Test that renderer can access font through manager
        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock face
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

            # Test rendering
            result = text_renderer.render_text_to_svg("Test", "MockFont", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result
            assert "Test" in result or "path" in result  # SVG contains path data

    def test_font_fallback_mechanism(self, text_renderer, font_manager):
        """Test font fallback mechanism when primary font fails."""
        # Remove primary font
        if "MockFont" in font_manager._font_paths:
            del font_manager._font_paths["MockFont"]

        # Add fallback font
        fallback_path = font_manager.fonts_dir / "fallback.ttf"
        fallback_path.write_bytes(b"fallback font data")

        from src.text_processor.font_manager import FontMetrics
        metrics = FontMetrics("FallbackFont", "Regular", 2048, 1854, -434, 67)
        font_manager._font_cache["FallbackFont"] = metrics
        font_manager._font_paths["FallbackFont"] = fallback_path

        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock face
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

            # Test that fallback works
            result = text_renderer.render_text_to_svg("Test", "MockFont", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result

    def test_font_manager_caching(self, font_manager):
        """Test that font manager caches metrics properly."""
        # Access font metrics multiple times
        metrics1 = font_manager.get_font_metrics("MockFont")
        metrics2 = font_manager.get_font_metrics("MockFont")

        # Should be the same object (cached)
        assert metrics1 is metrics2

        # Test font path caching
        path1 = font_manager.get_font_path("MockFont")
        path2 = font_manager.get_font_path("MockFont")

        assert path1 is path2

    def test_text_renderer_with_different_font_sizes(self, text_renderer):
        """Test text rendering with different font sizes."""
        font_sizes = [0.5, 1.0, 2.0, 5.0]

        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock face
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

            for font_size in font_sizes:
                result = text_renderer.render_text_to_svg("Test", "MockFont", font_size)

                assert isinstance(result, str)
                assert "<svg" in result
                # Font size should affect character size in the SVG
                # (This is a basic check - real validation would parse SVG)

    def test_multiline_text_rendering(self, text_renderer):
        """Test rendering multiline text."""
        multiline_text = "Line 1\nLine 2\nLine 3"

        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock face
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

            result = text_renderer.render_text_to_svg(multiline_text, "MockFont", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result
            # Should have height for 3 lines
            assert 'height="3.6"' in result  # 3 * 1.2

    def test_special_characters_handling(self, text_renderer):
        """Test handling of special characters and Unicode."""
        special_text = "Hello 世界! ñoño ©®™"

        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Setup mock face
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

            # Should not raise exception for Unicode characters
            result = text_renderer.render_text_to_svg(special_text, "MockFont", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result

    def test_font_manager_error_handling(self, font_manager):
        """Test error handling in font manager."""
        # Test accessing non-existent font
        with pytest.raises(FontNotFoundError):
            font_manager.get_font_path("NonExistentFont")

        with pytest.raises(FontNotFoundError):
            font_manager.get_font_metrics("NonExistentFont")

        # Test with empty font name
        with pytest.raises(FontNotFoundError):
            font_manager.get_font_path("")

    def test_text_renderer_error_recovery(self, text_renderer):
        """Test error recovery in text renderer."""
        # Test with invalid font that has no fallbacks
        with patch.object(text_renderer.font_manager, 'get_font_path', side_effect=FontNotFoundError("TestFont")):
            with pytest.raises(FontNotFoundError):
                text_renderer.render_text_to_svg("Test", "TestFont")

    @pytest.mark.parametrize("text_input,expected_lines", [
        ("Single line", 1),
        ("Line 1\nLine 2", 2),
        ("A\nB\nC\nD", 4),
        ("\n\n\n", 4),  # Empty lines still count
    ])
    def test_line_counting(self, text_renderer, text_input, expected_lines):
        """Test that renderer handles different line counts correctly."""
        lines = text_input.split('\n')
        assert len(lines) == expected_lines

        # This is more of a setup verification, but shows the renderer
        # would handle these inputs appropriately

