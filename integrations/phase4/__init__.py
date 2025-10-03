"""
Phase 4: Professional Marketplace Integration
CGTrader, TurboSquid, and Unreal Marketplace integration with Blender MCP
"""

__version__ = "1.0.0"
__author__ = "3D-DDF Team"
__description__ = "Professional marketplace asset integration for CGTrader, TurboSquid, and Unreal Marketplace"

from .src.phase4_asset_importer import Phase4AssetImporter
from .src.blender_mcp_phase4 import Phase4BlenderIntegration

__all__ = [
    "Phase4AssetImporter",
    "Phase4BlenderIntegration"
]
