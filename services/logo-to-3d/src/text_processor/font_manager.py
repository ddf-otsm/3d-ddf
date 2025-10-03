"""Font management for text processing."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import freetype
from fonttools.ttLib import TTFont

from ..core.config import settings
from ..core.exceptions import FontNotFoundError
from ..core.logging import get_logger
from ..core.utils import ensure_directory_exists

logger = get_logger(__name__)


class FontMetrics:
    """Font metrics information."""

    def __init__(self, family_name: str, style_name: str, units_per_em: int,
                 ascender: int, descender: int, line_gap: int):
        self.family_name = family_name
        self.style_name = style_name
        self.units_per_em = units_per_em
        self.ascender = ascender
        self.descender = descender
        self.line_gap = line_gap

    @property
    def height(self) -> float:
        """Get font height in em units."""
        return (self.ascender - self.descender + self.line_gap) / self.units_per_em

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "family_name": self.family_name,
            "style_name": self.style_name,
            "units_per_em": self.units_per_em,
            "ascender": self.ascender,
            "descender": self.descender,
            "line_gap": self.line_gap,
            "height": self.height
        }


class FontManager:
    """Manages font collection and provides font information."""

    def __init__(self):
        self.fonts_dir = settings.fonts_dir
        self._font_cache: Dict[str, FontMetrics] = {}
        self._font_paths: Dict[str, Path] = {}
        self._load_fonts()

    def _load_fonts(self) -> None:
        """Load available fonts from the fonts directory."""
        ensure_directory_exists(self.fonts_dir)

        # System font directories (common locations)
        system_font_dirs = [
            Path("/System/Library/Fonts"),  # macOS
            Path("/Library/Fonts"),         # macOS
            Path("/usr/share/fonts"),       # Linux
            Path("/usr/local/share/fonts"), # Linux
            Path("C:/Windows/Fonts"),       # Windows
        ]

        # Add custom font directory
        font_dirs = system_font_dirs + [self.fonts_dir]

        supported_extensions = {'.ttf', '.otf', '.woff', '.woff2'}

        for font_dir in font_dirs:
            if not font_dir.exists():
                continue

            for font_file in font_dir.rglob("*"):
                if font_file.suffix.lower() in supported_extensions:
                    try:
                        metrics = self._load_font_metrics(font_file)
                        if metrics:
                            font_name = self._normalize_font_name(metrics.family_name)
                            self._font_cache[font_name] = metrics
                            self._font_paths[font_name] = font_file
                            logger.debug(f"Loaded font: {font_name} from {font_file}")
                    except Exception as e:
                        logger.warning(f"Failed to load font {font_file}: {e}")

        # Add fallback fonts if not found
        self._ensure_fallback_fonts()

        logger.info(f"Loaded {len(self._font_cache)} fonts")

    def _load_font_metrics(self, font_path: Path) -> Optional[FontMetrics]:
        """Load font metrics from a font file."""
        try:
            # Try with fonttools first (better for OpenType)
            font = TTFont(str(font_path), recalcBBoxes=False)

            name_table = font['name']
            family_name = self._get_name_record(name_table, 1)  # Font Family
            style_name = self._get_name_record(name_table, 2)   # Font Subfamily

            if not family_name:
                return None

            # Get metrics from hhea table
            hhea = font['hhea']
            os2 = font['OS/2']

            return FontMetrics(
                family_name=family_name,
                style_name=style_name or "Regular",
                units_per_em=font['head'].unitsPerEm,
                ascender=hhea.ascent,
                descender=hhea.descent,
                line_gap=hhea.lineGap
            )

        except Exception:
            # Fallback to freetype
            try:
                face = freetype.Face(str(font_path))
                face.set_char_size(48 * 64)  # 48pt

                family_name = face.family_name.decode('utf-8')
                style_name = face.style_name.decode('utf-8')

                return FontMetrics(
                    family_name=family_name,
                    style_name=style_name,
                    units_per_em=face.units_per_EM,
                    ascender=face.ascender,
                    descender=face.descender,
                    line_gap=face.height - (face.ascender - face.descender)
                )
            except Exception as e:
                logger.debug(f"Failed to load font metrics for {font_path}: {e}")
                return None

    def _get_name_record(self, name_table, name_id: int) -> Optional[str]:
        """Get name record from font name table."""
        for record in name_table.names:
            if record.nameID == name_id and record.platformID == 3:  # Windows
                try:
                    return record.toUnicode()
                except UnicodeDecodeError:
                    continue
        return None

    def _normalize_font_name(self, name: str) -> str:
        """Normalize font name for consistent lookup."""
        # Handle common font name variations
        name = name.strip()

        # Remove common suffixes
        suffixes = [" Regular", " Bold", " Italic", " Light", " Medium", " Heavy"]
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]

        return name

    def _ensure_fallback_fonts(self) -> None:
        """Ensure fallback fonts are available."""
        fallback_fonts = ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"]

        for font_name in fallback_fonts:
            if font_name not in self._font_cache:
                # Try to find similar fonts
                for available_font in self._font_cache.keys():
                    if font_name.lower() in available_font.lower():
                        self._font_cache[font_name] = self._font_cache[available_font]
                        self._font_paths[font_name] = self._font_paths[available_font]
                        break

    def get_font_path(self, font_name: str) -> Path:
        """Get the file path for a font."""
        if font_name not in self._font_paths:
            raise FontNotFoundError(font_name)
        return self._font_paths[font_name]

    def get_font_metrics(self, font_name: str) -> FontMetrics:
        """Get metrics for a font."""
        if font_name not in self._font_cache:
            raise FontNotFoundError(font_name)
        return self._font_cache[font_name]

    def list_fonts(self) -> List[str]:
        """List all available fonts."""
        return sorted(self._font_cache.keys())

    def is_font_available(self, font_name: str) -> bool:
        """Check if a font is available."""
        return font_name in self._font_cache

    def find_similar_fonts(self, query: str, limit: int = 5) -> List[str]:
        """Find fonts similar to the query."""
        query = query.lower()
        matches = []

        for font_name in self._font_cache.keys():
            if query in font_name.lower():
                matches.append(font_name)

        return matches[:limit]

    def get_font_info(self, font_name: str) -> Dict:
        """Get detailed information about a font."""
        metrics = self.get_font_metrics(font_name)
        font_path = self.get_font_path(font_name)

        return {
            "name": font_name,
            "path": str(font_path),
            "metrics": metrics.to_dict(),
            "file_size": font_path.stat().st_size if font_path.exists() else 0
        }


# Global font manager instance
font_manager = FontManager()


def get_font_manager() -> FontManager:
    """Get the global font manager instance."""
    return font_manager

