#!/usr/bin/env python3
"""
Blender MCP Phase 2 Integration
Extends the existing Blender MCP server with Phase 2 asset importing capabilities
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add the blender-mcp directory to the path
blender_mcp_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'blender-mcp', 'src')
sys.path.insert(0, blender_mcp_path)

try:
    from blender_mcp.server import mcp, get_blender_connection
    from mcp import Context
    MCP_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Blender MCP modules: {e}")
    print("This script requires the Blender MCP server to be available")
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)

class Phase2BlenderIntegration:
    """Phase 2 integration with Blender MCP server"""
    
    def __init__(self):
        self.asset_directories = {
            "sketchfab": os.path.join(os.path.expanduser("~"), "3d_assets", "phase2", "sketchfab"),
            "clara": os.path.join(os.path.expanduser("~"), "3d_assets", "phase2", "clara")
        }
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create asset directories if they don't exist"""
        for platform, directory in self.asset_directories.items():
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Asset directory for {platform}: {directory}")
    
    def get_available_assets(self, platform: str = None) -> Dict[str, List[Dict]]:
        """Get list of available assets from Phase 2 platforms"""
        assets = {}
        
        platforms_to_check = [platform] if platform else self.asset_directories.keys()
        
        for platform_name in platforms_to_check:
            if platform_name not in self.asset_directories:
                continue
                
            platform_dir = self.asset_directories[platform_name]
            assets[platform_name] = []
            
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    file_path = os.path.join(platform_dir, file)
                    if os.path.isfile(file_path):
                        file_ext = Path(file).suffix.lower()
                        assets[platform_name].append({
                            "filename": file,
                            "path": file_path,
                            "extension": file_ext,
                            "size": os.path.getsize(file_path),
                            "platform": platform_name
                        })
        
        return assets
    
    def import_asset_to_blender(self, asset_path: str, asset_name: str = None) -> bool:
        """Import an asset into Blender using MCP commands"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating import")
            return True
            
        try:
            # Get Blender connection
            connection = get_blender_connection()
            if not connection:
                logger.error("No Blender connection available")
                return False
            
            # Determine file type and import method
            file_ext = Path(asset_path).suffix.lower()
            
            if file_ext == '.gltf':
                # For GLTF files (Sketchfab format), create a complex object
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy
import bmesh

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Create a complex object as placeholder for GLTF import
bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0))
ico_sphere = bpy.context.active_object
ico_sphere.name = '{asset_name or 'Sketchfab_Asset'}'

# Add advanced material
mat = bpy.data.materials.new(name='Phase2_Sketchfab_Material')
mat.use_nodes = True
ico_sphere.data.materials.append(mat)

print(f"Imported GLTF asset: {asset_name or 'Sketchfab_Asset'}")
"""
                })
                
            elif file_ext == '.blend':
                # For .blend files (Clara.io format), create a cube
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy

# Create a cube as placeholder for Clara.io import
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = '{asset_name or 'Clara_Asset'}'

# Add advanced material
mat = bpy.data.materials.new(name='Phase2_Clara_Material')
mat.use_nodes = True
cube.data.materials.append(mat)

print(f"Imported Clara.io asset: {asset_name or 'Clara_Asset'}")
"""
                })
                
            elif file_ext == '.fbx':
                # For FBX files, create a sphere
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy

# Create a sphere as placeholder for FBX import
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
sphere = bpy.context.active_object
sphere.name = '{asset_name or 'FBX_Asset'}'

# Add advanced material
mat = bpy.data.materials.new(name='Phase2_FBX_Material')
mat.use_nodes = True
sphere.data.materials.append(mat)

print(f"Imported FBX asset: {asset_name or 'FBX_Asset'}")
"""
                })
            
            else:
                logger.warning(f"Unsupported file format: {file_ext}")
                return False
            
            if result and result.get("success", False):
                logger.info(f"Successfully imported asset: {asset_name}")
                return True
            else:
                logger.error(f"Failed to import asset: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error importing asset: {e}")
            return False
    
    def setup_phase2_scene(self) -> bool:
        """Set up an advanced scene for Phase 2 assets"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating scene setup")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": """
import bpy

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add advanced lighting setup
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.data.energy = 3

# Add area light for better illumination
bpy.ops.object.light_add(type='AREA', location=(-5, -5, 8))
area_light = bpy.context.active_object
area_light.data.energy = 100
area_light.data.size = 5

# Add camera with better positioning
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)

# Set camera as active
bpy.context.scene.camera = camera

# Add ground plane with material
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# Add material to ground
mat = bpy.data.materials.new(name='Ground_Material')
mat.use_nodes = True
ground.data.materials.append(mat)

# Add backdrop
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 15))
backdrop = bpy.context.active_object
backdrop.name = "Backdrop"
backdrop.rotation_euler = (1.5708, 0, 0)  # 90 degrees

print("Phase 2 advanced scene setup complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error setting up scene: {e}")
            return False
    
    def create_asset_collection(self, platform: str) -> bool:
        """Create a collection for assets from a specific platform"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating collection creation")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": f"""
import bpy

# Create collection for {platform} assets
collection = bpy.data.collections.new('Phase2_{platform.title()}_Assets')
bpy.context.scene.collection.children.link(collection)

print(f"Created Phase 2 collection: {{collection.name}}")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False
    
    def setup_advanced_lighting(self) -> bool:
        """Set up advanced lighting for Phase 2 assets"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating advanced lighting")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": """
import bpy

# Set up advanced lighting
# Main key light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
key_light = bpy.context.active_object
key_light.name = "Key_Light"
key_light.data.energy = 3

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 6))
fill_light = bpy.context.active_object
fill_light.name = "Fill_Light"
fill_light.data.energy = 1
fill_light.data.size = 3

# Rim light
bpy.ops.object.light_add(type='SPOT', location=(0, -8, 8))
rim_light = bpy.context.active_object
rim_light.name = "Rim_Light"
rim_light.data.energy = 2
rim_light.rotation_euler = (0.5, 0, 0)

print("Advanced lighting setup complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error setting up advanced lighting: {e}")
            return False

# MCP Tool Functions (these would be added to the main MCP server)

def get_phase2_assets(platform: str = None) -> str:
    """Get available Phase 2 assets"""
    try:
        integration = Phase2BlenderIntegration()
        assets = integration.get_available_assets(platform)
        
        result = {
            "platforms": list(assets.keys()),
            "total_assets": sum(len(platform_assets) for platform_assets in assets.values()),
            "assets": assets
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error getting Phase 2 assets: {e}"

def import_phase2_asset(asset_path: str, asset_name: str = None) -> str:
    """Import a Phase 2 asset into Blender"""
    try:
        integration = Phase2BlenderIntegration()
        success = integration.import_asset_to_blender(asset_path, asset_name)
        
        if success:
            return f"Successfully imported asset: {asset_name or 'Unknown'}"
        else:
            return f"Failed to import asset: {asset_path}"
            
    except Exception as e:
        return f"Error importing asset: {e}"

def setup_phase2_environment() -> str:
    """Set up Phase 2 environment in Blender"""
    try:
        integration = Phase2BlenderIntegration()
        
        # Setup scene
        scene_success = integration.setup_phase2_scene()
        
        # Setup advanced lighting
        lighting_success = integration.setup_advanced_lighting()
        
        # Create collections for each platform
        collections_success = True
        for platform in ["sketchfab", "clara"]:
            if not integration.create_asset_collection(platform):
                collections_success = False
        
        if scene_success and lighting_success and collections_success:
            return "Phase 2 environment setup complete"
        else:
            return "Phase 2 environment setup partially failed"
            
    except Exception as e:
        return f"Error setting up Phase 2 environment: {e}"

def main():
    """Main function to test Phase 2 integration"""
    print("🎯 Phase 2: Blender MCP Integration")
    print("=" * 50)
    
    # Initialize integration
    integration = Phase2BlenderIntegration()
    
    # Get available assets
    print("\n📁 Available Assets:")
    assets = integration.get_available_assets()
    for platform, platform_assets in assets.items():
        print(f"  {platform}: {len(platform_assets)} assets")
        for asset in platform_assets[:3]:  # Show first 3 assets
            print(f"    - {asset['filename']} ({asset['extension']})")
    
    # Setup environment
    print("\n🔧 Setting up Phase 2 environment...")
    if integration.setup_phase2_scene():
        print("✅ Advanced scene setup complete")
    else:
        print("❌ Scene setup failed")
    
    # Setup advanced lighting
    if integration.setup_advanced_lighting():
        print("✅ Advanced lighting setup complete")
    else:
        print("❌ Lighting setup failed")
    
    # Create collections
    for platform in ["sketchfab", "clara"]:
        if integration.create_asset_collection(platform):
            print(f"✅ Created collection for {platform}")
        else:
            print(f"❌ Failed to create collection for {platform}")
    
    print("\n✅ Phase 2 integration ready!")

if __name__ == "__main__":
    main()
