"""
Phase 1: Free & Simple Asset Integration

This package provides integration with free 3D asset platforms:
- OpenGameArt.org
- Free3D

Features:
- Automated asset downloading
- Blender MCP integration
- Asset library management
- Workflow automation
"""

__version__ = "1.0.0"
__author__ = "3D-DDF Team"

from .src.phase1_asset_importer import Phase1AssetImporter
from .src.blender_mcp_phase1 import Phase1BlenderIntegration

__all__ = [
    "Phase1AssetImporter",
    "Phase1BlenderIntegration"
]

