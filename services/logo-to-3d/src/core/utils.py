"""Utility functions for the Logo to 3D service."""

import hashlib
import secrets
import string
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from PIL import Image


def generate_job_id() -> str:
    """Generate a unique job ID."""
    return secrets.token_urlsafe(16)


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    return file_path.stat().st_size / (1024 * 1024)


def validate_image_file(file_path: Path) -> Dict[str, Any]:
    """Validate and get information about an image file."""
    try:
        with Image.open(file_path) as img:
            return {
                "valid": True,
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
                "width": img.width,
                "height": img.height,
            }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


def ensure_directory_exists(directory: Path) -> None:
    """Ensure a directory exists, creating it if necessary."""
    directory.mkdir(parents=True, exist_ok=True)


def cleanup_temp_files(temp_dir: Path, max_age_hours: int = 24) -> None:
    """Clean up temporary files older than specified hours."""
    import time
    from datetime import datetime, timedelta

    cutoff_time = time.time() - (max_age_hours * 3600)

    for file_path in temp_dir.rglob("*"):
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
            except OSError:
                pass  # Ignore deletion errors


def calculate_delta_e(color1: Union[List[float], np.ndarray],
                     color2: Union[List[float], np.ndarray]) -> float:
    """Calculate Delta E (CIE76) color difference."""
    color1 = np.array(color1)
    color2 = np.array(color2)

    # Convert RGB to LAB (simplified conversion)
    # This is a basic approximation - for production, use a proper color library
    def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
        rgb = rgb / 255.0
        rgb = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
        rgb = rgb * 100

        x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
        y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505

        x = x / 95.047
        y = y / 100.000
        z = z / 108.883

        x = np.where(x > 0.008856, x ** (1/3), (7.787 * x) + (16/116))
        y = np.where(y > 0.008856, y ** (1/3), (7.787 * y) + (16/116))
        z = np.where(z > 0.008856, z ** (1/3), (7.787 * z) + (16/116))

        return np.array([
            (116 * y) - 16,  # L
            500 * (x - y),   # A
            200 * (y - z)    # B
        ])

    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)

    return np.sqrt(np.sum((lab1 - lab2) ** 2))


def get_image_dominant_colors(image_path: Path, num_colors: int = 5) -> List[List[int]]:
    """Extract dominant colors from an image."""
    with Image.open(image_path) as img:
        # Resize for faster processing
        img = img.resize((150, 150))

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Get colors
        colors = img.getcolors(150 * 150)
        if not colors:
            return []

        # Sort by frequency and return top colors
        colors.sort(key=lambda x: x[0], reverse=True)
        return [list(color) for count, color in colors[:num_colors]]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and invalid characters."""
    # Remove path separators
    filename = filename.replace("/", "").replace("\\", "")

    # Keep only alphanumeric characters, dots, hyphens, and underscores
    allowed_chars = string.ascii_letters + string.digits + ".-_"
    filename = "".join(c for c in filename if c in allowed_chars)

    # Ensure it's not empty and doesn't start with a dot
    if not filename or filename.startswith("."):
        filename = "file_" + filename

    return filename[:255]  # Limit length


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return ".1f"
        size_bytes /= 1024.0
    return ".1f"


def create_archive(files: List[Path], archive_path: Path) -> None:
    """Create a ZIP archive from a list of files."""
    import zipfile

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            if file_path.exists():
                zipf.write(file_path, file_path.name)


def validate_export_format(format_name: str) -> bool:
    """Validate if export format is supported."""
    supported_formats = ['obj', 'fbx', 'gltf', 'glb', 'stl', 'ply', 'x3d', 'usd']
    return format_name.lower() in supported_formats


def get_mime_type_for_format(format_name: str) -> str:
    """Get MIME type for export format."""
    mime_types = {
        'obj': 'application/octet-stream',
        'fbx': 'application/octet-stream',
        'gltf': 'model/gltf+json',
        'glb': 'model/gltf-binary',
        'stl': 'application/sla',
        'ply': 'application/octet-stream',
        'x3d': 'model/x3d+xml',
        'usd': 'application/octet-stream'
    }
    return mime_types.get(format_name.lower(), 'application/octet-stream')

