# Blender MCP Test Suite

This directory contains automated tests for the Blender MCP integration.

## Tests

### `test_blender_mcp_cube.py`

Tests the ability to create a cube in Blender and verify it with comprehensive Blender data feedback.

**What it tests:**
- Connection to Blender MCP server
- Execution of Python code in Blender
- Object creation (cube with green material)
- Object property verification (location, scale, rotation)
- Mesh data validation (vertices, edges, polygons)
- Material application
- Scene object count updates
- Cleanup operations

**Test output includes:**
- ✅ Detailed cube properties (name, type, location, rotation, scale)
- ✅ Mesh statistics (8 vertices, 12 edges, 6 polygons for a cube)
- ✅ Material verification
- ✅ 11 validation checks with pass/fail status

## Running Tests

### Prerequisites

1. **Blender must be running** with the MCP addon installed and enabled
2. **Blender MCP server must be connected** (click "Connect to Claude" in Blender)
3. Server must be running on default port `9876`

### Run a Test

```bash
# From project root
python3 tests/integration/test_blender_mcp_cube.py
```

### Expected Output

```
============================================================
TEST: Create Cube and Verify with Blender Data
============================================================

✅ Connected to Blender at localhost:9876
📊 Getting initial scene info...
   Initial object count: 4

🔨 Creating test cube...
✅ Cube created successfully

🔍 Verifying cube with Blender data feedback...
✅ Cube verified! Details:
   Name: MCP_Test_Cube
   Type: MESH
   Location: [5.0, 3.0, 1.0]
   Scale: [1.5, 1.5, 1.5]
   ...

✓ Validation Results:
   ✅ Location X: True
   ✅ Location Y: True
   ✅ Scale X: True
   ... (all validations pass)

🎉 ALL VALIDATIONS PASSED!
============================================================
```

## Test Details

### Cube Properties Tested

| Property | Expected Value | Description |
|----------|---------------|-------------|
| Location X | 5.0 | X coordinate in 3D space |
| Location Y | 3.0 | Y coordinate in 3D space |
| Location Z | 1.0 | Z coordinate in 3D space |
| Scale X/Y/Z | 1.5 | Uniform scale factor |
| Type | MESH | Object type |
| Vertices | 8 | Number of vertices (cube has 8) |
| Edges | 12 | Number of edges (cube has 12) |
| Polygons | 6 | Number of faces (cube has 6) |
| Materials | 1+ | Has at least one material |

### Blender Data Feedback

The test demonstrates getting comprehensive feedback from Blender:

```python
# Example response from get_object_info
{
  "name": "MCP_Test_Cube",
  "type": "MESH",
  "location": [5.0, 3.0, 1.0],
  "rotation": [0.0, 0.0, 0.0],
  "scale": [1.5, 1.5, 1.5],
  "visible": true,
  "materials": ["Test_Green_Material"],
  "world_bounding_box": [...],
  "mesh": {
    "vertices": 8,
    "edges": 12,
    "polygons": 6
  }
}
```

## Troubleshooting

**Test fails with "Connection refused":**
- Make sure Blender is running
- Make sure the MCP addon is installed and enabled
- Click "Connect to Claude" in the BlenderMCP panel in Blender

**Test fails with "Object not found":**
- The test may have failed mid-execution
- Manually delete any `MCP_Test_Cube` objects in Blender
- Run the test again

**Test fails with "Unknown command type":**
- Make sure the addon is up to date
- Check that the Blender MCP server is version 1.2 or higher

## Test Structure

- `integration/` - Integration tests with Blender MCP
- `results/` - Test results and reports
- `fixtures/test_scenes/` - Test data and Blender scenes

## Adding New Tests

To add a new test:

1. Create a new file: `tests/integration/test_<feature_name>.py`
2. Use the `BlenderMCPTester` class from `test_blender_mcp_cube.py`
3. Follow the pattern:
   - Connect
   - Get initial state
   - Execute operation
   - Verify with Blender data feedback
   - Cleanup
4. Add documentation to this README
