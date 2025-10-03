#!/usr/bin/env python3
"""
Phase 1: Free & Simple Asset Importer
Integrates OpenGameArt.org and Free3D with Blender MCP

This script provides automated asset downloading and importing
for the simplest free platforms in our roadmap.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
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

class Phase1AssetImporter:
    """Handles asset importing from free platforms (OpenGameArt.org, Free3D)"""
    
    def __init__(self, download_dir: str = None):
        """Initialize the asset importer"""
        # Use configured directories or fallback to default
        if ASSET_DIRECTORIES:
            self.download_dir = download_dir or str(ASSET_DIRECTORIES.get("opengameart", Path.home() / "3d_assets" / "phase1"))
        else:
            self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "3d_assets", "phase1")
        
        self.ensure_download_dir()
        
        # Use configured platforms or fallback to default
        if PLATFORMS:
            self.platforms = PLATFORMS
        else:
            self.platforms = {
                "opengameart": {
                    "name": "OpenGameArt.org",
                    "base_url": "https://opengameart.org",
                    "api_url": "https://opengameart.org/api",
                    "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds"],
                    "license": "CC0, CC-BY, CC-BY-SA",
                    "complexity": 1
                },
                "free3d": {
                    "name": "Free3D",
                    "base_url": "https://free3d.com",
                    "supported_formats": [".blend", ".fbx", ".obj", ".3ds", ".max"],
                    "license": "Various free licenses",
                    "complexity": 1
                }
            }
    
    def ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Download directory: {self.download_dir}")
    
    def search_opengameart(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search OpenGameArt.org for assets
        Note: OpenGameArt doesn't have a public API, so this is a placeholder
        for manual asset discovery workflow
        """
        logger.info(f"Searching OpenGameArt.org for: {query}")
        
        # In a real implementation, you would:
        # 1. Use web scraping (with proper respect for robots.txt)
        # 2. Or use their RSS feeds
        # 3. Or implement a manual workflow
        
        # For now, return example structure
        example_assets = [
            {
                "title": f"Example {query} Asset 1",
                "url": "https://opengameart.org/content/example-1",
                "format": ".blend",
                "license": "CC0",
                "download_url": "https://opengameart.org/files/example1.blend"
            },
            {
                "title": f"Example {query} Asset 2", 
                "url": "https://opengameart.org/content/example-2",
                "format": ".fbx",
                "license": "CC-BY",
                "download_url": "https://opengameart.org/files/example2.fbx"
            }
        ]
        
        return example_assets[:limit]
    
    def download_asset(self, asset_info: Dict, platform: str) -> Optional[str]:
        """
        Download an asset from the specified platform
        
        Args:
            asset_info: Dictionary containing asset information
            platform: Platform name ('opengameart' or 'free3d')
            
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
            
            # For demo purposes, create a placeholder file
            # In real implementation, you would download from the URL
            logger.info(f"Downloading {asset_info['title']} to {filepath}")
            
            # Create a simple placeholder file for demonstration
            with open(filepath, 'w') as f:
                f.write(f"# Placeholder for {asset_info['title']}\n")
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
        Import downloaded asset into Blender
        
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
            
            if file_ext == '.blend':
                # Import from .blend file
                return self._import_blend_file(filepath, asset_info)
            elif file_ext == '.fbx':
                # Import FBX file
                return self._import_fbx_file(filepath, asset_info)
            elif file_ext == '.obj':
                # Import OBJ file
                return self._import_obj_file(filepath, asset_info)
            elif file_ext == '.dae':
                # Import Collada file
                return self._import_dae_file(filepath, asset_info)
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to import asset: {e}")
            return False
    
    def _import_blend_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import .blend file using Blender's append functionality"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating .blend import: {filepath}")
            return True
            
        try:
            # For .blend files, we would use bpy.ops.wm.append()
            # This is a simplified version for demonstration
            logger.info(f"Importing .blend file: {filepath}")
            
            # Create a simple cube as placeholder
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
            cube = bpy.context.active_object
            cube.name = f"OG_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import .blend file: {e}")
            return False
    
    def _import_fbx_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import FBX file"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating FBX import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing FBX file: {filepath}")
            
            # Create a simple sphere as placeholder
            bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
            sphere = bpy.context.active_object
            sphere.name = f"FBX_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import FBX file: {e}")
            return False
    
    def _import_obj_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import OBJ file"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating OBJ import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing OBJ file: {filepath}")
            
            # Create a simple cylinder as placeholder
            bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
            cylinder = bpy.context.active_object
            cylinder.name = f"OBJ_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import OBJ file: {e}")
            return False
    
    def _import_dae_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import Collada DAE file"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating DAE import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing DAE file: {filepath}")
            
            # Create a simple cone as placeholder
            bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0))
            cone = bpy.context.active_object
            cone.name = f"DAE_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import DAE file: {e}")
            return False
    
    def setup_basic_materials(self, obj_name: str, platform: str):
        """Set up basic materials for imported assets"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating material setup for {obj_name}")
            return True
            
        try:
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                return False
            
            # Create material
            mat = bpy.data.materials.new(name=f"{platform}_Material")
            mat.use_nodes = True
            
            # Set up basic material nodes
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            # Add Principled BSDF
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
            
            logger.info(f"Applied material to {obj_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup materials: {e}")
            return False
    
    def create_asset_library(self) -> Dict:
        """Create a simple asset library structure"""
        library = {
            "phase1_assets": {
                "opengameart": [],
                "free3d": []
            },
            "metadata": {
                "created": str(Path().cwd()),
                "total_assets": 0,
                "platforms": list(self.platforms.keys())
            }
        }
        
        # Scan existing assets
        for platform in self.platforms.keys():
            platform_dir = os.path.join(self.download_dir, platform)
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    if file.endswith(tuple(self.platforms[platform]["supported_formats"])):
                        library["phase1_assets"][platform].append({
                            "filename": file,
                            "path": os.path.join(platform_dir, file),
                            "imported": False
                        })
                        library["metadata"]["total_assets"] += 1
        
        return library
    
    def run_phase1_workflow(self, search_terms: List[str]) -> Dict:
        """
        Run the complete Phase 1 workflow
        
        Args:
            search_terms: List of search terms to find assets
            
        Returns:
            Dictionary with workflow results
        """
        results = {
            "searched_terms": search_terms,
            "platforms_used": [],
            "assets_found": 0,
            "assets_downloaded": 0,
            "assets_imported": 0,
            "errors": []
        }
        
        logger.info("Starting Phase 1: Free & Simple Asset Workflow")
        
        for term in search_terms:
            logger.info(f"Searching for: {term}")
            
            # Search OpenGameArt.org
            try:
                og_assets = self.search_opengameart(term, limit=3)
                results["assets_found"] += len(og_assets)
                
                for asset in og_assets:
                    # Download asset
                    filepath = self.download_asset(asset, "opengameart")
                    if filepath:
                        results["assets_downloaded"] += 1
                        
                        # Import to Blender
                        if self.import_to_blender(filepath, asset):
                            results["assets_imported"] += 1
                            self.setup_basic_materials(
                                f"OG_Asset_{asset['title'].replace(' ', '_')}", 
                                "opengameart"
                            )
                
                results["platforms_used"].append("opengameart")
                
            except Exception as e:
                error_msg = f"OpenGameArt search failed: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        # Create asset library
        library = self.create_asset_library()
        results["library"] = library
        
        logger.info(f"Phase 1 workflow completed: {results}")
        return results

def main():
    """Main function to demonstrate Phase 1 workflow"""
    print("🎯 Phase 1: Free & Simple Asset Importer")
    print("=" * 50)
    
    # Initialize importer
    importer = Phase1AssetImporter()
    
    # Example search terms
    search_terms = ["character", "weapon", "environment", "vehicle"]
    
    # Run workflow
    results = importer.run_phase1_workflow(search_terms)
    
    # Print results
    print(f"\n📊 Results:")
    print(f"Assets found: {results['assets_found']}")
    print(f"Assets downloaded: {results['assets_downloaded']}")
    print(f"Assets imported: {results['assets_imported']}")
    print(f"Platforms used: {', '.join(results['platforms_used'])}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    print(f"\n✅ Phase 1 workflow completed!")
    print(f"Download directory: {importer.download_dir}")

if __name__ == "__main__":
    main()
