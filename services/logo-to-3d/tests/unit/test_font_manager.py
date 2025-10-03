"""Unit tests for font manager functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.text_processor.font_manager import FontManager, FontMetrics, get_font_manager
from src.core.exceptions import FontNotFoundError


class TestFontMetrics:
    """Test cases for FontMetrics class."""

    def test_init(self):
        """Test FontMetrics initialization."""
        metrics = FontMetrics(
            family_name="Arial",
            style_name="Regular",
            units_per_em=2048,
            ascender=1854,
            descender=-434,
            line_gap=67
        )

        assert metrics.family_name == "Arial"
        assert metrics.style_name == "Regular"
        assert metrics.units_per_em == 2048
        assert metrics.ascender == 1854
        assert metrics.descender == -434
        assert metrics.line_gap == 67

    def test_height_property(self):
        """Test height property calculation."""
        metrics = FontMetrics(
            family_name="Arial",
            style_name="Regular",
            units_per_em=2048,
            ascender=1854,
            descender=-434,
            line_gap=67
        )

        expected_height = (1854 - (-434) + 67) / 2048
        assert metrics.height == pytest.approx(expected_height, rel=1e-6)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        metrics = FontMetrics(
            family_name="Arial",
            style_name="Regular",
            units_per_em=2048,
            ascender=1854,
            descender=-434,
            line_gap=67
        )

        result = metrics.to_dict()

        assert result["family_name"] == "Arial"
        assert result["style_name"] == "Regular"
        assert result["units_per_em"] == 2048
        assert result["ascender"] == 1854
        assert result["descender"] == -434
        assert result["line_gap"] == 67
        assert "height" in result


class TestFontManager:
    """Test cases for FontManager class."""

    @pytest.fixture
    def temp_fonts_dir(self, tmp_path):
        """Create a temporary fonts directory."""
        fonts_dir = tmp_path / "fonts"
        fonts_dir.mkdir()
        return fonts_dir

    @pytest.fixture
    def font_manager(self, temp_fonts_dir):
        """Create a font manager instance with mocked settings."""
        with patch('src.text_processor.font_manager.settings') as mock_settings:
            mock_settings.fonts_dir = temp_fonts_dir
            mock_settings.supported_fonts = ["Arial", "Verdana", "Times New Roman"]
            manager = FontManager()
            return manager

    def test_init(self, font_manager):
        """Test FontManager initialization."""
        assert font_manager.fonts_dir.exists()
        assert isinstance(font_manager._font_cache, dict)
        assert isinstance(font_manager._font_paths, dict)

    def test_get_font_manager_singleton(self):
        """Test get_font_manager returns singleton instance."""
        manager1 = get_font_manager()
        manager2 = get_font_manager()
        assert manager1 is manager2

    @patch('src.text_processor.font_manager.TTFont')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.rglob')
    def test_load_font_metrics_fonttools(self, mock_rglob, mock_exists, mock_ttfont, font_manager, temp_fonts_dir):
        """Test loading font metrics using fonttools."""
        # Setup mocks
        mock_exists.return_value = True

        # Create a mock font file
        font_file = temp_fonts_dir / "test.ttf"
        font_file.touch()

        # Mock the rglob to return our font file
        mock_rglob.return_value = [font_file]

        # Mock TTFont
        mock_font = Mock()
        mock_font.__getitem__.return_value = Mock(unitsPerEm=2048)

        # Mock name table
        mock_name_table = Mock()
        mock_name_record = Mock()
        mock_name_record.toUnicode.return_value = "Arial"
        mock_name_table.names = [mock_name_record]
        mock_font.__getitem__.side_effect = lambda key: {
            'name': mock_name_table,
            'hhea': Mock(ascent=1854, descent=-434, lineGap=67),
            'OS/2': Mock(),
            'head': Mock(unitsPerEm=2048)
        }[key]

        mock_ttfont.return_value = mock_font

        # Reload fonts
        font_manager._load_fonts()

        # Check that font was loaded
        assert "Arial" in font_manager._font_cache
        metrics = font_manager._font_cache["Arial"]
        assert metrics.family_name == "Arial"

    @patch('src.text_processor.font_manager.freetype')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.rglob')
    def test_load_font_metrics_freetype_fallback(self, mock_rglob, mock_exists, mock_freetype, font_manager, temp_fonts_dir):
        """Test loading font metrics using freetype as fallback."""
        # Setup mocks
        mock_exists.return_value = True

        font_file = temp_fonts_dir / "test.ttf"
        font_file.touch()
        mock_rglob.return_value = [font_file]

        # Mock fonttools to fail
        with patch('src.text_processor.font_manager.TTFont', side_effect=Exception("FontTools failed")):
            # Mock freetype
            mock_face = Mock()
            mock_face.family_name = b"Arial"
            mock_face.style_name = b"Regular"
            mock_face.units_per_EM = 2048
            mock_face.ascender = 1854
            mock_face.descender = -434
            mock_face.height = 1000

            mock_freetype.Face.return_value = mock_face

            # Reload fonts
            font_manager._load_fonts()

            # Check that font was loaded via freetype
            assert "Arial" in font_manager._font_cache

    def test_get_font_path_success(self, font_manager):
        """Test getting font path for existing font."""
        # Manually add a font to the cache
        test_path = Path("/path/to/font.ttf")
        font_manager._font_paths["TestFont"] = test_path

        result = font_manager.get_font_path("TestFont")
        assert result == test_path

    def test_get_font_path_not_found(self, font_manager):
        """Test getting font path for non-existing font."""
        with pytest.raises(FontNotFoundError):
            font_manager.get_font_path("NonExistentFont")

    def test_get_font_metrics_success(self, font_manager):
        """Test getting font metrics for existing font."""
        metrics = FontMetrics("Test", "Regular", 2048, 1854, -434, 67)
        font_manager._font_cache["TestFont"] = metrics

        result = font_manager.get_font_metrics("TestFont")
        assert result == metrics

    def test_get_font_metrics_not_found(self, font_manager):
        """Test getting font metrics for non-existing font."""
        with pytest.raises(FontNotFoundError):
            font_manager.get_font_metrics("NonExistentFont")

    def test_list_fonts(self, font_manager):
        """Test listing all available fonts."""
        font_manager._font_cache = {
            "Arial": Mock(),
            "Verdana": Mock(),
            "Times": Mock()
        }

        result = font_manager.list_fonts()
        assert set(result) == {"Arial", "Verdana", "Times"}

    def test_is_font_available(self, font_manager):
        """Test checking if font is available."""
        font_manager._font_cache["Arial"] = Mock()

        assert font_manager.is_font_available("Arial") is True
        assert font_manager.is_font_available("NonExistent") is False

    def test_find_similar_fonts(self, font_manager):
        """Test finding similar fonts."""
        font_manager._font_cache = {
            "Arial": Mock(),
            "Arial Black": Mock(),
            "Arial Narrow": Mock(),
            "Verdana": Mock()
        }

        result = font_manager.find_similar_fonts("Arial", limit=2)
        assert len(result) <= 2
        assert all("Arial" in font for font in result)

    def test_get_font_info(self, font_manager):
        """Test getting detailed font information."""
        metrics = FontMetrics("Arial", "Regular", 2048, 1854, -434, 67)
        font_path = Path("/path/to/arial.ttf")

        font_manager._font_cache["Arial"] = metrics
        font_manager._font_paths["Arial"] = font_path

        # Mock stat to return file size
        with patch.object(font_path, 'stat') as mock_stat:
            mock_stat.return_value = Mock(st_size=123456)

            result = font_manager.get_font_info("Arial")

            assert result["name"] == "Arial"
            assert result["path"] == str(font_path)
            assert result["metrics"]["family_name"] == "Arial"
            assert result["file_size"] == 123456

    def test_normalize_font_name(self, font_manager):
        """Test font name normalization."""
        # Test removing suffixes
        assert font_manager._normalize_font_name("Arial Bold") == "Arial"
        assert font_manager._normalize_font_name("Arial Italic") == "Arial"
        assert font_manager._normalize_font_name("Arial Regular") == "Arial"

        # Test no change needed
        assert font_manager._normalize_font_name("Arial") == "Arial"

    @patch('src.text_processor.font_manager.ensure_directory_exists')
    def test_load_fonts_creates_directory(self, mock_ensure_dir, font_manager):
        """Test that fonts directory is created during loading."""
        font_manager._load_fonts()
        mock_ensure_dir.assert_called_once_with(font_manager.fonts_dir)

    def test_ensure_fallback_fonts(self, font_manager):
        """Test ensuring fallback fonts are available."""
        # Set up scenario where some fallback fonts are missing
        font_manager._font_cache = {"Arial": Mock()}
        font_manager._font_paths = {"Arial": Path("/path/to/arial.ttf")}

        # Mock supported fonts to include missing fallbacks
        with patch('src.text_processor.font_manager.settings') as mock_settings:
            mock_settings.supported_fonts = ["Arial", "Liberation Sans", "DejaVu Sans"]

            font_manager._ensure_fallback_fonts()

            # Arial should still be available
            assert "Arial" in font_manager._font_cache

    @pytest.mark.parametrize("font_name,expected_normalized", [
        ("Arial Bold", "Arial"),
        ("Times New Roman Italic", "Times New Roman"),
        ("Verdana Regular", "Verdana"),
        ("Helvetica Light", "Helvetica"),
        ("Courier New Medium", "Courier New"),
        ("Arial", "Arial"),  # No change needed
    ])
    def test_normalize_font_name_comprehensive(self, font_manager, font_name, expected_normalized):
        """Test comprehensive font name normalization."""
        result = font_manager._normalize_font_name(font_name)
        assert result == expected_normalized

