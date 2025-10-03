#!/usr/bin/env python3
"""
Test suite for Blender MCP cube creation
Tests the ability to create objects and verify them with Blender data feedback

⚠️  REQUIRES: Live Blender instance with MCP server running
Run this test only when Blender is open with MCP addon connected.
"""

import pytest
import json
import socket
import time
from typing import Dict, Any, Optional

pytestmark = pytest.mark.blender  # Mark all tests in this module as requiring Blender


class BlenderMCPTester:
    """Test client for Blender MCP operations"""
    
    def __init__(self, host: str = "localhost", port: int = 9876):
        self.host = host
        self.port = port
        self.sock: Optional[socket.socket] = None
    
    def connect(self) -> bool:
        """Connect to Blender MCP server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"✅ Connected to Blender at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def send_command(self, command_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a command to Blender and get response"""
        if self.sock is None:
            raise ConnectionError("Not connected to Blender")

        if params is None:
            params = {}

        command = {
            "type": command_type,
            "params": params
        }

        command_json = json.dumps(command) + "\n"
        self.sock.sendall(command_json.encode())

        response = self.sock.recv(65536).decode()
        return json.loads(response)
    
    def disconnect(self):
        """Disconnect from Blender"""
        if self.sock:
            self.sock.close()
            print("Disconnected from Blender")
    
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """Get detailed information about an object"""
        return self.send_command("get_object_info", {"name": object_name})
    
    def execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in Blender"""
        return self.send_command("execute_code", {"code": code})
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get scene information"""
        return self.send_command("get_scene_info", {})


def test_create_cube():
    """Test creating a cube and verify with Blender data feedback"""
    
    print("\n" + "="*60)
    print("TEST: Create Cube and Verify with Blender Data")
    print("="*60 + "\n")
    
    tester = BlenderMCPTester()
    
    # Step 1: Connect to Blender
    if not tester.connect():
        return False
    
    # Step 2: Get initial scene info
    print("📊 Getting initial scene info...")
    scene_before = tester.get_scene_info()
    if scene_before.get("status") == "success":
        initial_count = scene_before["result"]["object_count"]
        print(f"   Initial object count: {initial_count}")
    else:
        print(f"❌ Failed to get scene info: {scene_before}")
        tester.disconnect()
        return False
    
    # Step 3: Create a test cube
    print("\n🔨 Creating test cube...")
    cube_code = """
import bpy

# Create a cube at specific location
bpy.ops.mesh.primitive_cube_add(location=(5, 3, 1))
cube = bpy.context.active_object
cube.name = "MCP_Test_Cube"

# Add a green material
mat = bpy.data.materials.new(name="Test_Green_Material")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0, 1, 0, 1)  # Green
cube.data.materials.append(mat)

# Scale it to 1.5x
cube.scale = (1.5, 1.5, 1.5)

print(f"Created {cube.name} at location {cube.location}")
"""
    
    result = tester.execute_python(cube_code)
    if result.get("status") == "success":
        print(f"✅ Cube created successfully")
        print(f"   Output: {result.get('result', 'N/A')}")
    else:
        print(f"❌ Failed to create cube: {result}")
        tester.disconnect()
        return False
    
    # Step 4: Verify cube exists with get_object_info
    print("\n🔍 Verifying cube with Blender data feedback...")
    time.sleep(0.1)  # Small delay to ensure Blender has updated
    
    obj_info = tester.get_object_info("MCP_Test_Cube")
    if obj_info.get("status") == "success":
        cube_data = obj_info["result"]
        print("✅ Cube verified! Details:")
        print(f"   Name: {cube_data['name']}")
        print(f"   Type: {cube_data['type']}")
        print(f"   Location: {cube_data['location']}")
        print(f"   Rotation: {cube_data['rotation']}")
        print(f"   Scale: {cube_data['scale']}")
        print(f"   Materials: {cube_data['materials']}")
        print(f"   Mesh data:")
        print(f"     - Vertices: {cube_data['mesh']['vertices']}")
        print(f"     - Edges: {cube_data['mesh']['edges']}")
        print(f"     - Polygons: {cube_data['mesh']['polygons']}")
        
        # Validate cube properties
        validations = {
            "Location X": cube_data['location'][0] == 5.0,
            "Location Y": cube_data['location'][1] == 3.0,
            "Location Z": cube_data['location'][2] == 1.0,
            "Scale X": cube_data['scale'][0] == 1.5,
            "Scale Y": cube_data['scale'][1] == 1.5,
            "Scale Z": cube_data['scale'][2] == 1.5,
            "Type is MESH": cube_data['type'] == "MESH",
            "Has vertices": cube_data['mesh']['vertices'] == 8,
            "Has edges": cube_data['mesh']['edges'] == 12,
            "Has polygons": cube_data['mesh']['polygons'] == 6,
            "Has material": len(cube_data['materials']) > 0,
        }
        
        print("\n✓ Validation Results:")
        all_passed = True
        for check, passed in validations.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}: {passed}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 ALL VALIDATIONS PASSED!")
        else:
            print("\n⚠️  Some validations failed")
            tester.disconnect()
            return False
    else:
        print(f"❌ Failed to get object info: {obj_info}")
        tester.disconnect()
        return False
    
    # Step 5: Verify scene object count increased
    print("\n📊 Getting final scene info...")
    scene_after = tester.get_scene_info()
    if scene_after.get("status") == "success":
        final_count = scene_after["result"]["object_count"]
        print(f"   Final object count: {final_count}")
        count_increased = final_count == initial_count + 1
        if count_increased:
            print(f"✅ Object count increased by 1 (as expected)")
        else:
            print(f"❌ Object count mismatch. Expected {initial_count + 1}, got {final_count}")
            tester.disconnect()
            return False
    else:
        print(f"❌ Failed to get final scene info: {scene_after}")
        tester.disconnect()
        return False
    
    # Step 6: Cleanup - Delete test cube
    print("\n🧹 Cleaning up test cube...")
    cleanup_code = """
import bpy
if "MCP_Test_Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["MCP_Test_Cube"])
    print("Test cube removed")
"""
    cleanup_result = tester.execute_python(cleanup_code)
    if cleanup_result.get("status") == "success":
        print("✅ Cleanup successful")
    
    tester.disconnect()
    
    print("\n" + "="*60)
    print("TEST PASSED: Cube creation and verification successful! 🎉")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = test_create_cube()
    exit(0 if success else 1)
