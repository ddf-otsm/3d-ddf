"""Unit tests for text renderer functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.text_processor.renderer import TextRenderer, get_text_renderer
from src.core.exceptions import FontNotFoundError


class TestTextRenderer:
    """Test cases for TextRenderer class."""

    @pytest.fixture
    def renderer(self):
        """Create a text renderer instance."""
        return TextRenderer()

    @pytest.fixture
    def mock_font_manager(self):
        """Mock font manager."""
        with patch('src.text_processor.renderer.get_font_manager') as mock_get:
            mock_manager = Mock()
            mock_manager.get_font_path.return_value = Path("/path/to/font.ttf")
            mock_manager.get_font_metrics.return_value = Mock(height=1.2)
            mock_get.return_value = mock_manager
            yield mock_manager

    def test_init(self, renderer):
        """Test TextRenderer initialization."""
        assert renderer.font_manager is not None

    def test_get_text_renderer_singleton(self):
        """Test get_text_renderer returns singleton instance."""
        renderer1 = get_text_renderer()
        renderer2 = get_text_renderer()
        assert renderer1 is renderer2

    def test_render_text_to_svg_simple(self, renderer, mock_font_manager):
        """Test rendering simple text to SVG."""
        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Mock the face methods
            mock_face.ascender = 800
            mock_face.descender = -200
            mock_face.height = 1000

            # Mock glyph
            mock_glyph = Mock()
            mock_glyph.advance.x = 500
            mock_face.glyph = mock_glyph

            mock_face.load_char = Mock()
            mock_face.get_kerning = Mock(return_value=Mock(x=0))

            # Mock outline
            mock_outline = Mock()
            mock_outline.n_contours = 1
            mock_outline.points = [(0, 0), (100, 0), (100, 100), (0, 100)]
            mock_outline.tags = [1, 1, 1, 1]
            mock_outline.contours = [3]
            mock_glyph.outline = mock_outline

            result = renderer.render_text_to_svg("Test", "Arial", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result
            assert 'width="1.5625"' in result  # 500/64 * 2 characters

    def test_render_text_to_svg_multiline(self, renderer, mock_font_manager):
        """Test rendering multi-line text to SVG."""
        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            # Mock the face methods
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

            result = renderer.render_text_to_svg("Line 1\nLine 2", "Arial", 1.0)

            assert isinstance(result, str)
            assert "<svg" in result
            # Should have height for 2 lines
            assert 'height="2.4"' in result  # 2 * 1.2

    def test_render_text_to_svg_empty_text(self, renderer, mock_font_manager):
        """Test rendering empty text."""
        result = renderer.render_text_to_svg("", "Arial", 1.0)
        assert isinstance(result, str)
        assert "<svg" in result

    def test_render_text_to_svg_font_not_found(self, renderer):
        """Test handling of font not found."""
        with patch.object(renderer.font_manager, 'get_font_path', side_effect=FontNotFoundError("Arial")):
            with patch.object(renderer.font_manager, 'get_font_path') as mock_get_path:
                mock_get_path.side_effect = [FontNotFoundError("Liberation Sans"),
                                           FontNotFoundError("DejaVu Sans"),
                                           Path("/path/to/arial.ttf")]

                result = renderer.render_text_to_svg("Test", "Arial", 1.0)
                assert isinstance(result, str)

    def test_render_text_to_svg_all_fonts_fail(self, renderer):
        """Test handling when all fonts fail to load."""
        with patch.object(renderer.font_manager, 'get_font_path', side_effect=FontNotFoundError("Arial")):
            with pytest.raises(FontNotFoundError):
                renderer.render_text_to_svg("Test", "Arial", 1.0)

    def test_calculate_line_width(self, renderer):
        """Test line width calculation."""
        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

            mock_glyph = Mock()
            mock_glyph.advance.x = 500
            mock_face.glyph = mock_glyph

            mock_face.load_char = Mock()
            mock_face.get_kerning = Mock(return_value=Mock(x=50))

            width = renderer._calculate_line_width(mock_face, "AB", 1.0)

            # 500 + 500 + 50 (kerning) = 1050, divided by 64 = 16.40625
            assert width == 16.40625

    def test_create_empty_svg(self, renderer):
        """Test creating empty SVG."""
        result = renderer._create_empty_svg()
        assert isinstance(result, str)
        assert "<svg" in result
        assert 'width="1"' in result
        assert 'height="1"' in result

    @pytest.mark.parametrize("text,font_name,font_size,expected_contains", [
        ("Hello", "Arial", 1.0, "Hello"),
        ("Test", "Verdana", 2.0, "Test"),
        ("World", "Times", 0.5, "World"),
    ])
    def test_render_text_various_inputs(self, renderer, mock_font_manager, text, font_name, font_size, expected_contains):
        """Test rendering with various input parameters."""
        with patch('freetype.Face') as mock_face_class:
            mock_face = Mock()
            mock_face_class.return_value = mock_face

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

            result = renderer.render_text_to_svg(text, font_name, font_size)
            assert isinstance(result, str)
            assert "<svg" in result

