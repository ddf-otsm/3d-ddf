"""
Phase 3: Game Development Integration
Unity Asset Store and Adobe Mixamo integration with Blender MCP
"""

__version__ = "1.0.0"
__author__ = "3D-DDF Team"
__description__ = "Game development asset integration for Unity Asset Store and Adobe Mixamo"

from .src.phase3_asset_importer import Phase3AssetImporter
from .src.blender_mcp_phase3 import Phase3BlenderIntegration

__all__ = [
    "Phase3AssetImporter",
    "Phase3BlenderIntegration"
]
