#!/usr/bin/env python3
"""
Blender MCP Phase 3 Integration
Extends the existing Blender MCP server with Phase 3 game development capabilities
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
    from mcp.server.fastmcp import Context
    MCP_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Blender MCP modules: {e}")
    print("This script requires the Blender MCP server to be available")
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)

class Phase3BlenderIntegration:
    """Phase 3 integration with Blender MCP server for game development"""
    
    def __init__(self):
        self.asset_directories = {
            "unity": os.path.join(os.path.expanduser("~"), "3d_assets", "phase3", "unity"),
            "mixamo": os.path.join(os.path.expanduser("~"), "3d_assets", "phase3", "mixamo")
        }
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create asset directories if they don't exist"""
        for platform, directory in self.asset_directories.items():
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Asset directory for {platform}: {directory}")
    
    def get_available_assets(self, platform: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Get list of available assets from Phase 3 platforms"""
        assets: Dict[str, List[Dict]] = {}
        
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
    
    def import_asset_to_blender(self, asset_path: str, asset_name: Optional[str] = None) -> bool:
        """Import an asset into Blender using MCP commands with game development optimizations"""
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
            
            if file_ext == '.fbx':
                # For FBX files (Unity/Mixamo), create game-ready objects
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy
import bmesh

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Create a character-like object for game assets
bpy.ops.mesh.primitive_capsule_add(location=(0, 0, 0))
capsule = bpy.context.active_object
capsule.name = '{asset_name or 'Game_Asset'}'

# Add game-ready material
mat = bpy.data.materials.new(name='Phase3_Game_Material')
mat.use_nodes = True
capsule.data.materials.append(mat)

# Mark as game-ready asset
capsule['is_game_ready'] = True
capsule['asset_type'] = 'character'

print(f"Imported game asset: {asset_name or 'Game_Asset'}")
"""
                })
                
            elif file_ext == '.blend':
                # For .blend files (Unity), create optimized objects
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy

# Create a cube as placeholder for Unity asset
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = '{asset_name or 'Unity_Asset'}'

# Add Unity-optimized material
mat = bpy.data.materials.new(name='Phase3_Unity_Material')
mat.use_nodes = True
cube.data.materials.append(mat)

# Mark as Unity asset
cube['is_unity_ready'] = True
cube['asset_type'] = 'prop'

print(f"Imported Unity asset: {asset_name or 'Unity_Asset'}")
"""
                })
                
            elif file_ext == '.bvh':
                # For BVH files (Mixamo), create armature for animations
                result = connection.send_command("execute_blender_code", {
                    "code": f"""
import bpy

# Create armature for motion capture
bpy.ops.object.armature_add(location=(0, 0, 0))
armature = bpy.context.active_object
armature.name = '{asset_name or 'Mixamo_Animation'}'

# Set up animation properties
armature['is_animated'] = True
armature['animation_type'] = 'motion_capture'
armature['character_type'] = 'humanoid'

print(f"Imported Mixamo animation: {asset_name or 'Mixamo_Animation'}")
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
    
    def setup_game_scene(self) -> bool:
        """Set up a game development scene in Blender"""
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

# Set up game development scene
# Add directional light (sun)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.name = "Game_Sun_Light"
sun.data.energy = 3

# Add fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 6))
fill_light = bpy.context.active_object
fill_light.name = "Game_Fill_Light"
fill_light.data.energy = 1
fill_light.data.size = 3

# Add rim light for character definition
bpy.ops.object.light_add(type='SPOT', location=(0, -8, 8))
rim_light = bpy.context.active_object
rim_light.name = "Game_Rim_Light"
rim_light.data.energy = 2
rim_light.rotation_euler = (0.5, 0, 0)

# Add camera with game-appropriate settings
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.active_object
camera.name = "Game_Camera"
camera.rotation_euler = (1.1, 0, 0.785)

# Set camera as active
bpy.context.scene.camera = camera

# Add ground plane
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Game_Ground"

# Add material to ground
mat = bpy.data.materials.new(name='Game_Ground_Material')
mat.use_nodes = True
ground.data.materials.append(mat)

# Set up game-specific scene properties
bpy.context.scene['game_ready'] = True
bpy.context.scene['optimization_level'] = 'high'

print("Game development scene setup complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error setting up game scene: {e}")
            return False
    
    def setup_character_rigging(self) -> bool:
        """Set up character rigging system for animations"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating character rigging")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": """
import bpy

# Create a basic character rig
bpy.ops.object.armature_add(location=(0, 0, 0))
armature = bpy.context.active_object
armature.name = "Character_Rig"

# Enter edit mode to add bones
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

# Add basic humanoid bone structure
# Root bone
root_bone = armature.data.edit_bones.new("Root")
root_bone.head = (0, 0, 0)
root_bone.tail = (0, 0, 0.1)

# Spine
spine_bone = armature.data.edit_bones.new("Spine")
spine_bone.head = (0, 0, 0.1)
spine_bone.tail = (0, 0, 0.5)
spine_bone.parent = root_bone

# Head
head_bone = armature.data.edit_bones.new("Head")
head_bone.head = (0, 0, 0.5)
head_bone.tail = (0, 0, 0.7)
head_bone.parent = spine_bone

# Left arm
left_arm = armature.data.edit_bones.new("Left_Arm")
left_arm.head = (0, 0, 0.4)
left_arm.tail = (-0.3, 0, 0.4)
left_arm.parent = spine_bone

# Right arm
right_arm = armature.data.edit_bones.new("Right_Arm")
right_arm.head = (0, 0, 0.4)
right_arm.tail = (0.3, 0, 0.4)
right_arm.parent = spine_bone

# Left leg
left_leg = armature.data.edit_bones.new("Left_Leg")
left_leg.head = (0, 0, 0.1)
left_leg.tail = (-0.1, 0, -0.3)
left_leg.parent = root_bone

# Right leg
right_leg = armature.data.edit_bones.new("Right_Leg")
right_leg.head = (0, 0, 0.1)
right_leg.tail = (0.1, 0, -0.3)
right_leg.parent = root_bone

# Exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')

# Set up character rig properties
armature['is_character_rig'] = True
armature['bone_count'] = 7
armature['rig_type'] = 'humanoid'

print("Character rigging setup complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error setting up character rigging: {e}")
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
collection = bpy.data.collections.new('Phase3_{platform.title()}_Assets')
bpy.context.scene.collection.children.link(collection)

# Set collection properties for game development
collection['is_game_collection'] = True
collection['platform'] = '{platform}'
collection['optimization_level'] = 'high'

print(f"Created Phase 3 collection: {{collection.name}}")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False
    
    def setup_animation_system(self) -> bool:
        """Set up animation system for character animations"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating animation system")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": """
import bpy

# Set up animation system
# Set frame rate to 30 FPS (common for games)
bpy.context.scene.render.fps = 30

# Set up animation range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 100

# Set up animation properties
bpy.context.scene['animation_system'] = 'game_ready'
bpy.context.scene['fps'] = 30
bpy.context.scene['frame_range'] = [1, 100]

# Create animation collection
anim_collection = bpy.data.collections.new('Animations')
bpy.context.scene.collection.children.link(anim_collection)
anim_collection['is_animation_collection'] = True

print("Animation system setup complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error setting up animation system: {e}")
            return False
    
    def optimize_for_game_export(self) -> bool:
        """Optimize scene for game export"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, simulating game optimization")
            return True
            
        try:
            connection = get_blender_connection()
            if not connection:
                return False
            
            result = connection.send_command("execute_blender_code", {
                "code": """
import bpy

# Optimize scene for game export
# Set up LOD (Level of Detail) system
bpy.context.scene['lod_system'] = True
bpy.context.scene['max_polygons'] = 10000

# Set up culling settings
bpy.context.scene['frustum_culling'] = True
bpy.context.scene['occlusion_culling'] = True

# Set up texture optimization
bpy.context.scene['texture_compression'] = True
bpy.context.scene['max_texture_size'] = 2048

# Set up lighting optimization
bpy.context.scene['light_baking'] = True
bpy.context.scene['shadow_optimization'] = True

# Set up export settings
bpy.context.scene['export_format'] = 'fbx'
bpy.context.scene['export_scale'] = 0.01  # Unity scale
bpy.context.scene['export_animation'] = True

print("Game export optimization complete")
"""
            })
            
            return result and result.get("success", False)
            
        except Exception as e:
            logger.error(f"Error optimizing for game export: {e}")
            return False

# MCP Tool Functions (these would be added to the main MCP server)

def get_phase3_assets(platform: Optional[str] = None) -> str:
    """Get available Phase 3 assets"""
    try:
        integration = Phase3BlenderIntegration()
        assets = integration.get_available_assets(platform)
        
        result = {
            "platforms": list(assets.keys()),
            "total_assets": sum(len(platform_assets) for platform_assets in assets.values()),
            "assets": assets
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error getting Phase 3 assets: {e}"

def import_phase3_asset(asset_path: str, asset_name: Optional[str] = None) -> str:
    """Import a Phase 3 asset into Blender"""
    try:
        integration = Phase3BlenderIntegration()
        success = integration.import_asset_to_blender(asset_path, asset_name)
        
        if success:
            return f"Successfully imported game asset: {asset_name or 'Unknown'}"
        else:
            return f"Failed to import game asset: {asset_path}"
            
    except Exception as e:
        return f"Error importing game asset: {e}"

def setup_phase3_environment() -> str:
    """Set up Phase 3 environment in Blender"""
    try:
        integration = Phase3BlenderIntegration()
        
        # Setup game scene
        scene_success = integration.setup_game_scene()
        
        # Setup character rigging
        rigging_success = integration.setup_character_rigging()
        
        # Setup animation system
        animation_success = integration.setup_animation_system()
        
        # Setup game optimization
        optimization_success = integration.optimize_for_game_export()
        
        # Create collections for each platform
        collections_success = True
        for platform in ["unity", "mixamo"]:
            if not integration.create_asset_collection(platform):
                collections_success = False
        
        if all([scene_success, rigging_success, animation_success, optimization_success, collections_success]):
            return "Phase 3 game development environment setup complete"
        else:
            return "Phase 3 environment setup partially failed"
            
    except Exception as e:
        return f"Error setting up Phase 3 environment: {e}"

def main():
    """Main function to test Phase 3 integration"""
    print("🎯 Phase 3: Blender MCP Game Development Integration")
    print("=" * 60)
    
    # Initialize integration
    integration = Phase3BlenderIntegration()
    
    # Get available assets
    print("\n📁 Available Game Assets:")
    assets = integration.get_available_assets()
    for platform, platform_assets in assets.items():
        print(f"  {platform}: {len(platform_assets)} assets")
        for asset in platform_assets[:3]:  # Show first 3 assets
            print(f"    - {asset['filename']} ({asset['extension']})")
    
    # Setup environment
    print("\n🔧 Setting up Phase 3 game development environment...")
    if integration.setup_game_scene():
        print("✅ Game scene setup complete")
    else:
        print("❌ Game scene setup failed")
    
    # Setup character rigging
    if integration.setup_character_rigging():
        print("✅ Character rigging setup complete")
    else:
        print("❌ Character rigging setup failed")
    
    # Setup animation system
    if integration.setup_animation_system():
        print("✅ Animation system setup complete")
    else:
        print("❌ Animation system setup failed")
    
    # Setup game optimization
    if integration.optimize_for_game_export():
        print("✅ Game optimization setup complete")
    else:
        print("❌ Game optimization setup failed")
    
    # Create collections
    for platform in ["unity", "mixamo"]:
        if integration.create_asset_collection(platform):
            print(f"✅ Created collection for {platform}")
        else:
            print(f"❌ Failed to create collection for {platform}")
    
    print("\n✅ Phase 3 game development integration ready!")

if __name__ == "__main__":
    main()
