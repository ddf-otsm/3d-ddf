"""Text rendering engine for converting text to vector paths."""

import math
from pathlib import Path
from typing import List, Optional, Tuple

import freetype
import numpy as np
import svgwrite
from fonttools.ttLib import TTFont

from ..core.config import settings
from ..core.exceptions import FontNotFoundError
from ..core.logging import get_logger
from .font_manager import get_font_manager

logger = get_logger(__name__)


class TextRenderer:
    """Renders text to vector paths using FreeType."""

    def __init__(self):
        self.font_manager = get_font_manager()

    def render_text_to_svg(self,
                          text: str,
                          font_name: str = None,
                          font_size: float = 1.0,
                          line_spacing: float = 1.2) -> str:
        """
        Render text to SVG format.

        Args:
            text: Text to render
            font_name: Font family name
            font_size: Font size in scene units
            line_spacing: Line spacing multiplier

        Returns:
            SVG string containing the text paths
        """
        if not font_name:
            font_name = settings.default_font

        # Get font path
        try:
            font_path = self.font_manager.get_font_path(font_name)
        except FontNotFoundError:
            # Try fallback fonts
            for fallback in ["Liberation Sans", "DejaVu Sans", "Arial"]:
                try:
                    font_path = self.font_manager.get_font_path(fallback)
                    logger.warning(f"Using fallback font {fallback} instead of {font_name}")
                    break
                except FontNotFoundError:
                    continue
            else:
                raise FontNotFoundError(f"No suitable font found for {font_name}")

        # Split text into lines
        lines = text.split('\n')
        if not lines:
            return self._create_empty_svg()

        # Load font and get metrics
        face = freetype.Face(str(font_path))
        face.set_char_size(int(font_size * 64))  # FreeType uses 26.6 fixed point

        metrics = self.font_manager.get_font_metrics(font_name)
        line_height = metrics.height * font_size * line_spacing

        # Calculate total dimensions
        total_width = 0
        total_height = len(lines) * line_height

        for line in lines:
            if line:
                line_width = self._calculate_line_width(face, line, font_size)
                total_width = max(total_width, line_width)

        # Create SVG
        dwg = svgwrite.Drawing(size=(total_width, total_height))

        # Render each line
        y_offset = line_height * 0.8  # Baseline offset

        for line_num, line in enumerate(lines):
            if line:
                self._render_line_to_svg(dwg, face, line, 0, y_offset, font_size)
            y_offset += line_height

        return dwg.tostring()

    def _calculate_line_width(self, face: freetype.Face, text: str, font_size: float) -> float:
        """Calculate the width of a text line."""
        width = 0
        prev_char = None

        for char in text:
            # Load glyph
            face.load_char(char, freetype.FT_LOAD_DEFAULT)

            # Add kerning if available
            if prev_char and hasattr(face, 'get_kerning'):
                try:
                    kerning = face.get_kerning(prev_char, char)
                    width += kerning.x / 64.0 * font_size
                except:
                    pass

            # Add glyph advance
            width += face.glyph.advance.x / 64.0 * font_size
            prev_char = char

        return width

    def _render_line_to_svg(self, dwg: svgwrite.Drawing, face: freetype.Face,
                           text: str, x_offset: float, y_offset: float, font_size: float) -> None:
        """Render a single line of text to SVG."""
        current_x = x_offset
        prev_char = None

        for char in text:
            # Load glyph
            face.load_char(char, freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_SCALE)

            # Add kerning
            if prev_char and hasattr(face, 'get_kerning'):
                try:
                    kerning = face.get_kerning(prev_char, char)
                    current_x += kerning.x / 64.0 * font_size
                except:
                    pass

            # Get glyph outline
            glyph = face.glyph
            outline = glyph.outline

            if outline.n_contours > 0:
                # Convert outline to SVG path
                path_data = self._outline_to_svg_path(outline, current_x, y_offset, font_size)
                if path_data:
                    dwg.add(dwg.path(d=path_data, fill="black", stroke="none"))

            # Move to next character position
            current_x += glyph.advance.x / 64.0 * font_size
            prev_char = char

    def _outline_to_svg_path(self, outline: freetype.Outline,
                           x_offset: float, y_offset: float, font_size: float) -> Optional[str]:
        """Convert FreeType outline to SVG path data."""
        points = outline.points
        tags = outline.tags
        contours = outline.contours

        if not points:
            return None

        path_commands = []
        start_x, start_y = None, None
        current_x, current_y = x_offset, y_offset

        contour_start = 0

        for contour_end in contours:
            # Process each contour
            path_commands.extend(self._process_contour(
                points[contour_start:contour_end + 1],
                tags[contour_start:contour_end + 1],
                current_x, current_y, font_size
            ))
            contour_start = contour_end + 1

        if path_commands:
            return " ".join(path_commands)
        return None

    def _process_contour(self, contour_points: List[Tuple[int, int]],
                        contour_tags: List[int], x_offset: float, y_offset: float,
                        font_size: float) -> List[str]:
        """Process a single contour to SVG path commands."""
        if not contour_points:
            return []

        commands = []
        i = 0

        while i < len(contour_points):
            point = contour_points[i]
            tag = contour_tags[i]

            # Convert coordinates
            x = (point[0] / 64.0 * font_size) + x_offset
            y = (point[1] / -64.0 * font_size) + y_offset  # Flip Y for SVG

            if tag & 1:  # On-curve point
                if not commands:
                    commands.append(f"M {x:.3f} {y:.3f}")
                else:
                    commands.append(f"L {x:.3f} {y:.3f}")
                i += 1
            else:  # Off-curve point (control point for quadratic Bezier)
                # Find the next on-curve point
                next_i = (i + 1) % len(contour_points)
                while not (contour_tags[next_i] & 1) and next_i != i:
                    next_i = (next_i + 1) % len(contour_points)

                if next_i != i:
                    next_point = contour_points[next_i]
                    next_x = (next_point[0] / 64.0 * font_size) + x_offset
                    next_y = (next_point[1] / -64.0 * font_size) + y_offset

                    # Quadratic Bezier curve
                    commands.append(f"Q {x:.3f} {y:.3f} {next_x:.3f} {next_y:.3f}")
                    i = next_i
                else:
                    i += 1

        commands.append("Z")  # Close path
        return commands

    def _create_empty_svg(self) -> str:
        """Create an empty SVG document."""
        dwg = svgwrite.Drawing(size=(1, 1))
        return dwg.tostring()


# Global text renderer instance
text_renderer = TextRenderer()


def get_text_renderer() -> TextRenderer:
    """Get the global text renderer instance."""
    return text_renderer

