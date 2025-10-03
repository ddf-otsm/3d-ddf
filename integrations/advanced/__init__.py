"""
Advanced Integration Features
AI recommendations, batch processing, and custom platform integration
"""

__version__ = "1.0.0"
__author__ = "3D-DDF Team"
__description__ = "Advanced integration features for 3D asset management"

from .src.ai_asset_recommender import AIAssetRecommender
from .src.batch_processor import BatchProcessor
from .src.custom_platform_integration import CustomPlatformManager, PlatformInterface

__all__ = [
    "AIAssetRecommender",
    "BatchProcessor", 
    "CustomPlatformManager",
    "PlatformInterface"
]
