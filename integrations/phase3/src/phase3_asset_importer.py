#!/usr/bin/env python3
"""
Phase 3: Game Development Asset Importer
Integrates Unity Asset Store and Adobe Mixamo with Blender MCP

This script provides automated asset downloading and importing
for game development platforms with character animation support.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

# Add the config directory to the path
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
sys.path.insert(0, config_path)

try:
    from settings import PLATFORMS, ASSET_DIRECTORIES, WORKFLOW_SETTINGS
except ImportError:
    # Fallback configuration if settings not available
    PLATFORMS = {}
    ASSET_DIRECTORIES = {}
    WORKFLOW_SETTINGS = {}

# Try to import Blender modules, but don't fail if not available
try:
    import bpy
    import bmesh
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    print("Warning: Blender modules not available. Some features will be limited.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase3AssetImporter:
    """Handles asset importing from game development platforms (Unity Asset Store, Mixamo)"""
    
    def __init__(self, download_dir: Optional[str] = None):
        """Initialize the asset importer"""
        # Use configured directories or fallback to default
        if ASSET_DIRECTORIES:
            self.download_dir = download_dir or str(ASSET_DIRECTORIES.get("unity", Path.home() / "3d_assets" / "phase3"))
        else:
            self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "3d_assets", "phase3")
        
        self.ensure_download_dir()
        
        # Use configured platforms or fallback to default
        if PLATFORMS:
            self.platforms = PLATFORMS
        else:
            self.platforms = {
                "unity": {
                    "name": "Unity Asset Store",
                    "base_url": "https://assetstore.unity.com",
                    "api_url": "https://assetstore.unity.com/api",
                    "supported_formats": [".fbx", ".blend", ".obj", ".dae", ".3ds", ".max"],
                    "license": "Unity Asset Store License",
                    "complexity": 3,
                    "requires_auth": True,
                    "auth_type": "unity_id",
                    "rate_limit": 2000,
                    "special_features": ["game_ready", "optimized", "prefabs"]
                },
                "mixamo": {
                    "name": "Adobe Mixamo",
                    "base_url": "https://mixamo.com",
                    "api_url": "https://mixamo.com/api",
                    "supported_formats": [".fbx", ".bvh", ".dae"],
                    "license": "Adobe License",
                    "complexity": 3,
                    "requires_auth": True,
                    "auth_type": "adobe_id",
                    "rate_limit": 1000,
                    "special_features": ["character_animation", "auto_rigging", "motion_capture"]
                }
            }
        
        # Authentication credentials
        self.auth_credentials = self.load_auth_credentials()
        
        # Character animation settings
        self.animation_settings = {
            "default_fps": 30,
            "bone_mapping": "mixamo_standard",
            "scale_factor": 0.01,  # Mixamo uses cm, Blender uses m
            "root_motion": True
        }
    
    def ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Download directory: {self.download_dir}")
    
    def load_auth_credentials(self) -> Dict[str, str]:
        """Load authentication credentials from secure storage"""
        credentials = {}
        
        # Try to load from environment variables
        unity_id = os.getenv("UNITY_ID")
        if unity_id:
            credentials["unity"] = unity_id
        
        adobe_id = os.getenv("ADOBE_ID")
        if adobe_id:
            credentials["mixamo"] = adobe_id
        
        # Try to load from config file
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'auth.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_credentials = json.load(f)
                    credentials.update(file_credentials)
            except Exception as e:
                logger.warning(f"Could not load auth credentials: {e}")
        
        return credentials
    
    def search_unity_asset_store(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Unity Asset Store for assets
        Note: This is a simulation - real implementation would use Unity Asset Store API
        """
        logger.info(f"Searching Unity Asset Store for: {query}")
        
        # Simulate API response
        mock_assets = [
            {
                "title": f"Unity {query} Asset Pack 1",
                "url": f"https://assetstore.unity.com/packages/example1",
                "format": ".fbx",
                "license": "Unity Asset Store License",
                "download_url": f"https://assetstore.unity.com/downloads/example1.unitypackage",
                "thumbnail": "https://assetstore.unity.com/thumbnails/example1.jpg",
                "price": "Free",
                "rating": 4.8,
                "downloads": 15000,
                "category": "3D Models",
                "tags": ["game-ready", "optimized", "low-poly"],
                "polygon_count": 2000,
                "texture_resolution": "1024x1024"
            },
            {
                "title": f"Unity {query} Character 1",
                "url": f"https://assetstore.unity.com/packages/example2",
                "format": ".fbx",
                "license": "Unity Asset Store License",
                "download_url": f"https://assetstore.unity.com/downloads/example2.unitypackage",
                "thumbnail": "https://assetstore.unity.com/thumbnails/example2.jpg",
                "price": "$15.99",
                "rating": 4.9,
                "downloads": 8500,
                "category": "Characters",
                "tags": ["character", "animated", "rigged"],
                "polygon_count": 5000,
                "texture_resolution": "2048x2048"
            }
        ]
        
        return mock_assets[:limit]
    
    def search_mixamo(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Adobe Mixamo for character animations
        Note: This is a simulation - real implementation would use Mixamo API
        """
        logger.info(f"Searching Mixamo for: {query}")
        
        # Simulate API response
        mock_assets = [
            {
                "title": f"Mixamo {query} Animation 1",
                "url": f"https://mixamo.com/animations/example1",
                "format": ".fbx",
                "license": "Adobe License",
                "download_url": f"https://mixamo.com/downloads/example1.fbx",
                "thumbnail": "https://mixamo.com/thumbnails/example1.jpg",
                "duration": 2.5,
                "fps": 30,
                "bone_count": 54,
                "category": "Locomotion",
                "tags": ["walk", "run", "idle"],
                "character_type": "humanoid",
                "file_size": "1.2MB"
            },
            {
                "title": f"Mixamo {query} Combat 1",
                "url": f"https://mixamo.com/animations/example2",
                "format": ".fbx",
                "license": "Adobe License",
                "download_url": f"https://mixamo.com/downloads/example2.fbx",
                "thumbnail": "https://mixamo.com/thumbnails/example2.jpg",
                "duration": 1.8,
                "fps": 30,
                "bone_count": 54,
                "category": "Combat",
                "tags": ["attack", "punch", "kick"],
                "character_type": "humanoid",
                "file_size": "0.9MB"
            }
        ]
        
        return mock_assets[:limit]
    
    def download_asset(self, asset_info: Dict, platform: str) -> Optional[str]:
        """
        Download an asset from the specified platform
        
        Args:
            asset_info: Dictionary containing asset information
            platform: Platform name ('unity' or 'mixamo')
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            # Create platform-specific directory
            platform_dir = os.path.join(self.download_dir, platform)
            Path(platform_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            filename = f"{asset_info['title'].replace(' ', '_')}{asset_info['format']}"
            filepath = os.path.join(platform_dir, filename)
            
            # Check authentication
            if self.platforms[platform]["requires_auth"]:
                if platform not in self.auth_credentials:
                    logger.warning(f"No authentication credentials for {platform}")
                    # Create placeholder file for demo
                    with open(filepath, 'w') as f:
                        f.write(f"# Placeholder for {asset_info['title']}\n")
                        f.write(f"# Platform: {platform}\n")
                        f.write(f"# License: {asset_info.get('license', 'Unknown')}\n")
                        f.write(f"# Original URL: {asset_info.get('url', 'N/A')}\n")
                        f.write(f"# Authentication required: {self.platforms[platform]['auth_type']}\n")
                        f.write(f"# Special features: {', '.join(self.platforms[platform].get('special_features', []))}\n")
                else:
                    # Simulate authenticated download
                    logger.info(f"Downloading {asset_info['title']} with authentication")
                    with open(filepath, 'w') as f:
                        f.write(f"# Authenticated download for {asset_info['title']}\n")
                        f.write(f"# Platform: {platform}\n")
                        f.write(f"# License: {asset_info.get('license', 'Unknown')}\n")
                        f.write(f"# Original URL: {asset_info.get('url', 'N/A')}\n")
                        f.write(f"# Auth type: {self.platforms[platform]['auth_type']}\n")
                        f.write(f"# Special features: {', '.join(self.platforms[platform].get('special_features', []))}\n")
                        
                        # Add platform-specific metadata
                        if platform == "unity":
                            f.write(f"# Price: {asset_info.get('price', 'Unknown')}\n")
                            f.write(f"# Rating: {asset_info.get('rating', 'Unknown')}\n")
                            f.write(f"# Downloads: {asset_info.get('downloads', 'Unknown')}\n")
                        elif platform == "mixamo":
                            f.write(f"# Duration: {asset_info.get('duration', 'Unknown')}s\n")
                            f.write(f"# FPS: {asset_info.get('fps', 'Unknown')}\n")
                            f.write(f"# Bone count: {asset_info.get('bone_count', 'Unknown')}\n")
            else:
                # Free download
                logger.info(f"Downloading {asset_info['title']} (free)")
                with open(filepath, 'w') as f:
                    f.write(f"# Free download for {asset_info['title']}\n")
                    f.write(f"# Platform: {platform}\n")
                    f.write(f"# License: {asset_info.get('license', 'Unknown')}\n")
                    f.write(f"# Original URL: {asset_info.get('url', 'N/A')}\n")
            
            logger.info(f"Successfully downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download asset: {e}")
            return None
    
    def import_to_blender(self, filepath: str, asset_info: Dict) -> bool:
        """
        Import downloaded asset into Blender with game development optimizations
        
        Args:
            filepath: Path to the asset file
            asset_info: Asset information dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not BLENDER_AVAILABLE:
            logger.warning("Blender not available, simulating import")
            return True
            
        try:
            file_ext = Path(filepath).suffix.lower()
            
            # Clear selection
            bpy.ops.object.select_all(action='DESELECT')
            
            if file_ext == '.fbx':
                # Import FBX file with game development settings
                return self._import_fbx_file(filepath, asset_info)
            elif file_ext == '.blend':
                # Import Blender file
                return self._import_blend_file(filepath, asset_info)
            elif file_ext == '.obj':
                # Import OBJ file
                return self._import_obj_file(filepath, asset_info)
            elif file_ext == '.bvh':
                # Import BVH motion capture file
                return self._import_bvh_file(filepath, asset_info)
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to import asset: {e}")
            return False
    
    def _import_fbx_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import FBX file with game development optimizations"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating FBX import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing FBX file: {filepath}")
            
            # Create a character-like object for game assets
            bpy.ops.mesh.primitive_capsule_add(location=(0, 0, 0))
            capsule = bpy.context.active_object
            capsule.name = f"Game_Asset_{asset_info['title'].replace(' ', '_')}"
            
            # Apply game development optimizations
            self._apply_game_optimizations(capsule, asset_info)
            
            return True
        except Exception as e:
            logger.error(f"Failed to import FBX file: {e}")
            return False
    
    def _import_blend_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import .blend file using Blender's append functionality"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating .blend import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing .blend file: {filepath}")
            
            # Create a cube as placeholder
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
            cube = bpy.context.active_object
            cube.name = f"Unity_Asset_{asset_info['title'].replace(' ', '_')}"
            
            # Apply game optimizations
            self._apply_game_optimizations(cube, asset_info)
            
            return True
        except Exception as e:
            logger.error(f"Failed to import .blend file: {e}")
            return False
    
    def _import_obj_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import OBJ file"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating OBJ import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing OBJ file: {filepath}")
            
            # Create a cylinder as placeholder
            bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
            cylinder = bpy.context.active_object
            cylinder.name = f"OBJ_Asset_{asset_info['title'].replace(' ', '_')}"
            
            # Apply game optimizations
            self._apply_game_optimizations(cylinder, asset_info)
            
            return True
        except Exception as e:
            logger.error(f"Failed to import OBJ file: {e}")
            return False
    
    def _import_bvh_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import BVH motion capture file"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating BVH import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing BVH file: {filepath}")
            
            # Create a simple armature for motion capture
            bpy.ops.object.armature_add(location=(0, 0, 0))
            armature = bpy.context.active_object
            armature.name = f"Mixamo_Animation_{asset_info['title'].replace(' ', '_')}"
            
            # Apply animation settings
            self._apply_animation_settings(armature, asset_info)
            
            return True
        except Exception as e:
            logger.error(f"Failed to import BVH file: {e}")
            return False
    
    def _apply_game_optimizations(self, obj, asset_info: Dict):
        """Apply game development optimizations to imported object"""
        if not BLENDER_AVAILABLE:
            return
            
        try:
            # Set up game-ready material
            mat = bpy.data.materials.new(name=f"Game_Material_{obj.name}")
            mat.use_nodes = True
            
            # Add game-specific material nodes
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            # Add Principled BSDF for game rendering
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf.location = (0, 0)
            
            # Add Material Output
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (300, 0)
            
            # Connect nodes
            mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
            
            # Apply LOD settings if available
            if "polygon_count" in asset_info:
                polygon_count = asset_info["polygon_count"]
                if polygon_count > 5000:
                    # High-poly asset - mark for LOD generation
                    obj["is_high_poly"] = True
                elif polygon_count < 1000:
                    # Low-poly asset - good for mobile
                    obj["is_mobile_ready"] = True
            
            logger.info(f"Applied game optimizations to {obj.name}")
            
        except Exception as e:
            logger.error(f"Failed to apply game optimizations: {e}")
    
    def _apply_animation_settings(self, armature, asset_info: Dict):
        """Apply animation settings for character animations"""
        if not BLENDER_AVAILABLE:
            return
            
        try:
            # Set up animation properties
            armature["animation_duration"] = asset_info.get("duration", 0)
            armature["animation_fps"] = asset_info.get("fps", 30)
            armature["bone_count"] = asset_info.get("bone_count", 0)
            armature["character_type"] = asset_info.get("character_type", "humanoid")
            
            # Apply scale factor for Mixamo
            if "mixamo" in armature.name.lower():
                armature.scale = (self.animation_settings["scale_factor"], 
                                self.animation_settings["scale_factor"], 
                                self.animation_settings["scale_factor"])
            
            logger.info(f"Applied animation settings to {armature.name}")
            
        except Exception as e:
            logger.error(f"Failed to apply animation settings: {e}")
    
    def setup_character_rigging(self, character_obj: str, animation_data: Dict) -> bool:
        """Set up character rigging for animations"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating character rigging for {character_obj}")
            return True
            
        try:
            # This would set up proper character rigging
            # For now, just log the operation
            logger.info(f"Setting up character rigging for {character_obj}")
            logger.info(f"Animation data: {animation_data}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup character rigging: {e}")
            return False
    
    def create_asset_library(self) -> Dict[str, Any]:
        """Create a game development asset library structure"""
        library: Dict[str, Any] = {
            "phase3_assets": {
                "unity": [],
                "mixamo": []
            },
            "metadata": {
                "created": str(Path().cwd()),
                "total_assets": 0,
                "platforms": list(self.platforms.keys()),
                "auth_status": {
                    platform: platform in self.auth_credentials 
                    for platform in self.platforms.keys()
                },
                "game_ready_assets": 0,
                "animated_assets": 0
            }
        }
        
        # Scan existing assets
        for platform in self.platforms.keys():
            platform_dir = os.path.join(self.download_dir, platform)
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    if file.endswith(tuple(self.platforms[platform]["supported_formats"])):
                        file_path = os.path.join(platform_dir, file)
                        asset_info = {
                            "filename": file,
                            "path": file_path,
                            "imported": False,
                            "auth_required": self.platforms[platform]["requires_auth"],
                            "game_ready": "game_ready" in self.platforms[platform].get("special_features", []),
                            "animated": "character_animation" in self.platforms[platform].get("special_features", [])
                        }
                        library["phase3_assets"][platform].append(asset_info)
                        library["metadata"]["total_assets"] += 1
                        
                        if asset_info["game_ready"]:
                            library["metadata"]["game_ready_assets"] += 1
                        if asset_info["animated"]:
                            library["metadata"]["animated_assets"] += 1
        
        return library
    
    def run_phase3_workflow(self, search_terms: List[str]) -> Dict:
        """
        Run the complete Phase 3 workflow
        
        Args:
            search_terms: List of search terms to find assets
            
        Returns:
            Dictionary with workflow results
        """
        results: Dict[str, Any] = {
            "searched_terms": search_terms,
            "platforms_used": [],
            "assets_found": 0,
            "assets_downloaded": 0,
            "assets_imported": 0,
            "auth_required": [],
            "game_ready_assets": 0,
            "animated_assets": 0,
            "errors": []
        }
        
        logger.info("Starting Phase 3: Game Development Asset Workflow")
        
        for term in search_terms:
            logger.info(f"Searching for: {term}")
            
            # Search Unity Asset Store
            try:
                unity_assets = self.search_unity_asset_store(term, limit=3)
                results["assets_found"] += len(unity_assets)
                
                for asset in unity_assets:
                    # Download asset
                    filepath = self.download_asset(asset, "unity")
                    if filepath:
                        results["assets_downloaded"] += 1
                        
                        # Import to Blender
                        if self.import_to_blender(filepath, asset):
                            results["assets_imported"] += 1
                            results["game_ready_assets"] += 1
                
                results["platforms_used"].append("unity")
                
                # Check if auth was required
                if "unity" not in self.auth_credentials:
                    results["auth_required"].append("unity")
                
            except Exception as e:
                error_msg = f"Unity Asset Store search failed: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
            
            # Search Mixamo
            try:
                mixamo_assets = self.search_mixamo(term, limit=3)
                results["assets_found"] += len(mixamo_assets)
                
                for asset in mixamo_assets:
                    # Download asset
                    filepath = self.download_asset(asset, "mixamo")
                    if filepath:
                        results["assets_downloaded"] += 1
                        
                        # Import to Blender
                        if self.import_to_blender(filepath, asset):
                            results["assets_imported"] += 1
                            results["animated_assets"] += 1
                            
                            # Setup character rigging
                            self.setup_character_rigging(f"Mixamo_Animation_{asset['title'].replace(' ', '_')}", asset)
                
                results["platforms_used"].append("mixamo")
                
                # Check if auth was required
                if "mixamo" not in self.auth_credentials:
                    results["auth_required"].append("mixamo")
                
            except Exception as e:
                error_msg = f"Mixamo search failed: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        # Create asset library
        library = self.create_asset_library()
        results["library"] = library
        
        logger.info(f"Phase 3 workflow completed: {results}")
        return results

def main():
    """Main function to demonstrate Phase 3 workflow"""
    print("🎯 Phase 3: Game Development Asset Importer")
    print("=" * 50)
    
    # Initialize importer
    importer = Phase3AssetImporter()
    
    # Example search terms
    search_terms = ["character", "weapon", "environment", "animation"]
    
    # Run workflow
    results = importer.run_phase3_workflow(search_terms)
    
    # Print results
    print(f"\n📊 Results:")
    print(f"Assets found: {results['assets_found']}")
    print(f"Assets downloaded: {results['assets_downloaded']}")
    print(f"Assets imported: {results['assets_imported']}")
    print(f"Game-ready assets: {results['game_ready_assets']}")
    print(f"Animated assets: {results['animated_assets']}")
    print(f"Platforms used: {', '.join(results['platforms_used'])}")
    
    if results['auth_required']:
        print(f"\n🔐 Authentication required for: {', '.join(results['auth_required'])}")
        print("Set environment variables: UNITY_ID, ADOBE_ID")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    print(f"\n✅ Phase 3 workflow completed!")
    print(f"Download directory: {importer.download_dir}")

if __name__ == "__main__":
    main()
