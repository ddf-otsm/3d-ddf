"""
Phase 2: Free with Registration Asset Integration

This package provides integration with free 3D asset platforms that require registration:
- Sketchfab
- Clara.io

Features:
- Authentication management
- Advanced asset downloading
- Blender MCP integration
- Asset library management
- Workflow automation
"""

__version__ = "1.0.0"
__author__ = "3D-DDF Team"

from .src.phase2_asset_importer import Phase2AssetImporter
from .src.blender_mcp_phase2 import Phase2BlenderIntegration

__all__ = [
    "Phase2AssetImporter",
    "Phase2BlenderIntegration"
]
