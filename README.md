# 3D-DDF with Blender MCP Integration

This repository integrates Blender with Cursor AI using the Model Context Protocol (MCP), allowing you to control Blender directly from Cursor.

## Prerequisites

- **Blender 3.0 or newer** installed on macOS
- **Python 3.10 or newer**
- **uv package manager** (already installed ✓)
- **Cursor** IDE

## Setup Instructions

### 1. Install Blender Addon

1. Open **Blender**
2. Go to `Edit > Preferences > Add-ons`
3. Click **"Install..."** button
4. Navigate to and select: `/Users/luismartins/local_repos/3d-ddf/blender-mcp/addon.py`
5. Enable the addon by checking the box next to **"Interface: Blender MCP"**

### 2. MCP Server Configuration

The MCP server is already configured in `.cursor/mcp.json` for this project.

### 3. Start Using Blender with Cursor

#### In Blender:
1. Press `N` in the 3D View to open the sidebar (if not visible)
2. Find the **"BlenderMCP"** tab
3. (Optional) Turn on the **Poly Haven** checkbox if you want to use assets from their API
4. Click **"Connect to Claude"** button

#### In Cursor:
1. Restart Cursor to load the MCP server configuration
2. Look for the hammer icon 🔨 which indicates the Blender MCP tools are available
3. Start asking Cursor to create 3D scenes and objects!

## Features

- **Object manipulation**: Create, modify, and delete 3D objects in Blender
- **Material control**: Apply and modify materials and colors
- **Scene inspection**: Get detailed information about the current Blender scene
- **Code execution**: Run Python code in Blender from Cursor
- **Poly Haven integration**: Download models, textures, and HDRIs
- **Hyper3D AI models**: Generate 3D models using AI
- **Viewport screenshots**: View Blender viewport to understand the scene

## Example Commands

Try asking Cursor things like:

- "Create a low poly scene in a dungeon, with a dragon guarding a pot of gold"
- "Create a beach vibe using HDRIs, textures, and models from Poly Haven"
- "Make this car red and metallic"
- "Create a sphere and place it above the cube"
- "Make the lighting like a studio"
- "Point the camera at the scene, and make it isometric"
- "Generate a 3D model of a garden gnome through Hyper3D"

## Environment Variables (Optional)

You can configure the Blender connection with these environment variables:

- `BLENDER_HOST`: Host address for Blender socket server (default: "localhost")
- `BLENDER_PORT`: Port number for Blender socket server (default: 9876)

## Troubleshooting

- **Connection issues**: Make sure the Blender addon server is running (click "Connect to Claude" in Blender)
- **MCP not showing**: Restart Cursor after adding the MCP configuration
- **Timeout errors**: Try simplifying your requests or breaking them into smaller steps
- **Still having issues?**: Try restarting both Cursor and the Blender server

## Important Notes

⚠️ **Security Warning**: The MCP allows running arbitrary Python code in Blender. ALWAYS save your work before using it.

⚠️ **Single Instance**: Only run one instance of the MCP server at a time (don't run it in both Cursor and Claude Desktop simultaneously).

## Submodule Information

This repository includes the `blender-mcp` server as a git submodule. To update it:

```bash
git submodule update --remote blender-mcp
```

## Credits

BlenderMCP is created by [Siddharth Ahuja](https://x.com/sidahuj) and is a third-party integration not made by Blender Foundation.

Repository: https://github.com/ahujasid/blender-mcp
