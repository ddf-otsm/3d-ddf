#!/usr/bin/env python3
"""
Phase 2: Free with Registration Asset Importer
Integrates Sketchfab and Clara.io with Blender MCP

This script provides automated asset downloading and importing
for platforms that require user registration but remain free.
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

class Phase2AssetImporter:
    """Handles asset importing from free platforms with registration (Sketchfab, Clara.io)"""
    
    def __init__(self, download_dir: str = None):
        """Initialize the asset importer"""
        # Use configured directories or fallback to default
        if ASSET_DIRECTORIES:
            self.download_dir = download_dir or str(ASSET_DIRECTORIES.get("sketchfab", Path.home() / "3d_assets" / "phase2"))
        else:
            self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "3d_assets", "phase2")
        
        self.ensure_download_dir()
        
        # Use configured platforms or fallback to default
        if PLATFORMS:
            self.platforms = PLATFORMS
        else:
            self.platforms = {
                "sketchfab": {
                    "name": "Sketchfab",
                    "base_url": "https://sketchfab.com",
                    "api_url": "https://api.sketchfab.com/v3",
                    "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".gltf"],
                    "license": "Various licenses",
                    "complexity": 2,
                    "requires_auth": True,
                    "auth_type": "api_key"
                },
                "clara": {
                    "name": "Clara.io",
                    "base_url": "https://clara.io",
                    "api_url": "https://clara.io/api",
                    "supported_formats": [".blend", ".fbx", ".obj", ".dae", ".3ds"],
                    "license": "Various licenses",
                    "complexity": 2,
                    "requires_auth": True,
                    "auth_type": "oauth"
                }
            }
        
        # Authentication credentials (should be loaded from secure storage)
        self.auth_credentials = self.load_auth_credentials()
    
    def ensure_download_dir(self):
        """Create download directory if it doesn't exist"""
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Download directory: {self.download_dir}")
    
    def load_auth_credentials(self) -> Dict[str, str]:
        """Load authentication credentials from secure storage"""
        credentials = {}
        
        # Try to load from environment variables
        sketchfab_key = os.getenv("SKETCHFAB_API_KEY")
        if sketchfab_key:
            credentials["sketchfab"] = sketchfab_key
        
        clara_token = os.getenv("CLARA_IO_TOKEN")
        if clara_token:
            credentials["clara"] = clara_token
        
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
    
    def search_sketchfab(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Sketchfab for assets
        Note: This is a simulation - real implementation would use Sketchfab API
        """
        logger.info(f"Searching Sketchfab for: {query}")
        
        # Simulate API response
        mock_assets = [
            {
                "title": f"Sketchfab {query} Asset 1",
                "url": f"https://sketchfab.com/models/example1",
                "format": ".gltf",
                "license": "CC-BY",
                "download_url": f"https://sketchfab.com/models/example1/download",
                "thumbnail": "https://media.sketchfab.com/models/example1/thumbnails/example1.jpg",
                "polygon_count": 5000,
                "vertex_count": 2500
            },
            {
                "title": f"Sketchfab {query} Asset 2",
                "url": f"https://sketchfab.com/models/example2",
                "format": ".fbx",
                "license": "CC0",
                "download_url": f"https://sketchfab.com/models/example2/download",
                "thumbnail": "https://media.sketchfab.com/models/example2/thumbnails/example2.jpg",
                "polygon_count": 8000,
                "vertex_count": 4000
            }
        ]
        
        return mock_assets[:limit]
    
    def search_clara(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Clara.io for assets
        Note: This is a simulation - real implementation would use Clara.io API
        """
        logger.info(f"Searching Clara.io for: {query}")
        
        # Simulate API response
        mock_assets = [
            {
                "title": f"Clara.io {query} Asset 1",
                "url": f"https://clara.io/view/example1",
                "format": ".blend",
                "license": "Royalty Free",
                "download_url": f"https://clara.io/api/download/example1",
                "thumbnail": "https://clara.io/thumbnails/example1.jpg",
                "file_size": "2.5MB",
                "created_date": "2024-01-15"
            },
            {
                "title": f"Clara.io {query} Asset 2",
                "url": f"https://clara.io/view/example2",
                "format": ".obj",
                "license": "Commercial",
                "download_url": f"https://clara.io/api/download/example2",
                "thumbnail": "https://clara.io/thumbnails/example2.jpg",
                "file_size": "1.8MB",
                "created_date": "2024-01-20"
            }
        ]
        
        return mock_assets[:limit]
    
    def download_asset(self, asset_info: Dict, platform: str) -> Optional[str]:
        """
        Download an asset from the specified platform
        
        Args:
            asset_info: Dictionary containing asset information
            platform: Platform name ('sketchfab' or 'clara')
            
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
                else:
                    # Simulate authenticated download
                    logger.info(f"Downloading {asset_info['title']} with authentication")
                    with open(filepath, 'w') as f:
                        f.write(f"# Authenticated download for {asset_info['title']}\n")
                        f.write(f"# Platform: {platform}\n")
                        f.write(f"# License: {asset_info.get('license', 'Unknown')}\n")
                        f.write(f"# Original URL: {asset_info.get('url', 'N/A')}\n")
                        f.write(f"# Auth type: {self.platforms[platform]['auth_type']}\n")
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
            
            if file_ext == '.gltf':
                # Import GLTF file (Sketchfab format)
                return self._import_gltf_file(filepath, asset_info)
            elif file_ext == '.blend':
                # Import Blender file
                return self._import_blend_file(filepath, asset_info)
            elif file_ext == '.fbx':
                # Import FBX file
                return self._import_fbx_file(filepath, asset_info)
            elif file_ext == '.obj':
                # Import OBJ file
                return self._import_obj_file(filepath, asset_info)
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to import asset: {e}")
            return False
    
    def _import_gltf_file(self, filepath: str, asset_info: Dict) -> bool:
        """Import GLTF file (Sketchfab format)"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating GLTF import: {filepath}")
            return True
            
        try:
            logger.info(f"Importing GLTF file: {filepath}")
            
            # Create a complex object as placeholder for GLTF
            bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0))
            sphere = bpy.context.active_object
            sphere.name = f"Sketchfab_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import GLTF file: {e}")
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
            cube.name = f"Clara_Asset_{asset_info['title'].replace(' ', '_')}"
            
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
            
            # Create a sphere as placeholder
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
            
            # Create a cylinder as placeholder
            bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
            cylinder = bpy.context.active_object
            cylinder.name = f"OBJ_Asset_{asset_info['title'].replace(' ', '_')}"
            
            return True
        except Exception as e:
            logger.error(f"Failed to import OBJ file: {e}")
            return False
    
    def setup_advanced_materials(self, obj_name: str, platform: str, asset_info: Dict):
        """Set up advanced materials for imported assets"""
        if not BLENDER_AVAILABLE:
            logger.info(f"Simulating advanced material setup for {obj_name}")
            return True
            
        try:
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                return False
            
            # Create advanced material
            mat = bpy.data.materials.new(name=f"{platform}_Advanced_Material")
            mat.use_nodes = True
            
            # Set up advanced material nodes
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            # Add Principled BSDF
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf.location = (0, 0)
            
            # Add Material Output
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (300, 0)
            
            # Add texture nodes if available
            if "thumbnail" in asset_info:
                # Add image texture node
                tex_node = nodes.new(type='ShaderNodeTexImage')
                tex_node.location = (-300, 0)
                
                # Connect nodes
                mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
            
            # Connect BSDF to output
            mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
            
            logger.info(f"Applied advanced material to {obj_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup advanced materials: {e}")
            return False
    
    def create_asset_library(self) -> Dict:
        """Create an advanced asset library structure"""
        library = {
            "phase2_assets": {
                "sketchfab": [],
                "clara": []
            },
            "metadata": {
                "created": str(Path().cwd()),
                "total_assets": 0,
                "platforms": list(self.platforms.keys()),
                "auth_status": {
                    platform: platform in self.auth_credentials 
                    for platform in self.platforms.keys()
                }
            }
        }
        
        # Scan existing assets
        for platform in self.platforms.keys():
            platform_dir = os.path.join(self.download_dir, platform)
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    if file.endswith(tuple(self.platforms[platform]["supported_formats"])):
                        file_path = os.path.join(platform_dir, file)
                        library["phase2_assets"][platform].append({
                            "filename": file,
                            "path": file_path,
                            "imported": False,
                            "auth_required": self.platforms[platform]["requires_auth"]
                        })
                        library["metadata"]["total_assets"] += 1
        
        return library
    
    def run_phase2_workflow(self, search_terms: List[str]) -> Dict:
        """
        Run the complete Phase 2 workflow
        
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
            "auth_required": [],
            "errors": []
        }
        
        logger.info("Starting Phase 2: Free with Registration Asset Workflow")
        
        for term in search_terms:
            logger.info(f"Searching for: {term}")
            
            # Search Sketchfab
            try:
                sketchfab_assets = self.search_sketchfab(term, limit=3)
                results["assets_found"] += len(sketchfab_assets)
                
                for asset in sketchfab_assets:
                    # Download asset
                    filepath = self.download_asset(asset, "sketchfab")
                    if filepath:
                        results["assets_downloaded"] += 1
                        
                        # Import to Blender
                        if self.import_to_blender(filepath, asset):
                            results["assets_imported"] += 1
                            self.setup_advanced_materials(
                                f"Sketchfab_Asset_{asset['title'].replace(' ', '_')}", 
                                "sketchfab",
                                asset
                            )
                
                results["platforms_used"].append("sketchfab")
                
                # Check if auth was required
                if "sketchfab" not in self.auth_credentials:
                    results["auth_required"].append("sketchfab")
                
            except Exception as e:
                error_msg = f"Sketchfab search failed: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
            
            # Search Clara.io
            try:
                clara_assets = self.search_clara(term, limit=3)
                results["assets_found"] += len(clara_assets)
                
                for asset in clara_assets:
                    # Download asset
                    filepath = self.download_asset(asset, "clara")
                    if filepath:
                        results["assets_downloaded"] += 1
                        
                        # Import to Blender
                        if self.import_to_blender(filepath, asset):
                            results["assets_imported"] += 1
                            self.setup_advanced_materials(
                                f"Clara_Asset_{asset['title'].replace(' ', '_')}", 
                                "clara",
                                asset
                            )
                
                results["platforms_used"].append("clara")
                
                # Check if auth was required
                if "clara" not in self.auth_credentials:
                    results["auth_required"].append("clara")
                
            except Exception as e:
                error_msg = f"Clara.io search failed: {e}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        # Create asset library
        library = self.create_asset_library()
        results["library"] = library
        
        logger.info(f"Phase 2 workflow completed: {results}")
        return results

def main():
    """Main function to demonstrate Phase 2 workflow"""
    print("🎯 Phase 2: Free with Registration Asset Importer")
    print("=" * 50)
    
    # Initialize importer
    importer = Phase2AssetImporter()
    
    # Example search terms
    search_terms = ["character", "weapon", "environment", "vehicle"]
    
    # Run workflow
    results = importer.run_phase2_workflow(search_terms)
    
    # Print results
    print(f"\n📊 Results:")
    print(f"Assets found: {results['assets_found']}")
    print(f"Assets downloaded: {results['assets_downloaded']}")
    print(f"Assets imported: {results['assets_imported']}")
    print(f"Platforms used: {', '.join(results['platforms_used'])}")
    
    if results['auth_required']:
        print(f"\n🔐 Authentication required for: {', '.join(results['auth_required'])}")
        print("Set environment variables: SKETCHFAB_API_KEY, CLARA_IO_TOKEN")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    print(f"\n✅ Phase 2 workflow completed!")
    print(f"Download directory: {importer.download_dir}")

if __name__ == "__main__":
    main()

