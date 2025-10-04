# Installation Guide

## Prerequisites

- **Blender 3.0 or newer** installed ([Installation guide](./blender-installation.md))
- **Python 3.10 or newer**
- **uv package manager** (already installed ✓)
- **Cursor** IDE

### 🔍 Check Blender Installation

Before proceeding, verify Blender is installed:

```bash
# Automated detection (recommended)
python scripts/detect_blender.py

# Manual check
which blender        # macOS/Linux
blender --version    # All platforms
```

**Expected Output:**
```
✅ Found 1 Blender installation(s):
[1] Blender 4.0.2
    Path:       /Applications/Blender.app
    Executable: /Applications/Blender.app/Contents/MacOS/Blender
```

**If Blender is not found**, follow the **[Blender Installation Guide](./blender-installation.md)** first.

## Setup Steps

### 1. Install Blender Addon

1. Open **Blender**
2. Go to `Edit > Preferences > Add-ons`
3. Click **"Install..."** button
4. Navigate to and select: `${PROJECT_ROOT}/blender-mcp/addon.py`
5. Enable the addon by checking the box next to **"Interface: Blender MCP"**

### 2. MCP Server Configuration

The MCP server is already configured in `.cursor/mcp.json` for this project. It runs the local blender-mcp from the submodule, so no PyPI installation is needed.

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

## Environment Variables (Optional)

You can configure the Blender connection and project paths with environment variables. 

**Recommended**: Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
# Edit .env with your paths
```

Available variables:
- `PROJECT_ROOT`: Absolute path to the project root (defaults to repository root)
- `BLENDER` / `BLENDER_EXECUTABLE`: Path to Blender executable (platform-specific)
- `BLENDER_HOST`: Host address for Blender socket server (default: "localhost")
- `BLENDER_PORT`: Port number for Blender socket server (default: 9876)

See [`.env.example`](../../.env.example) for full documentation and platform-specific examples.

## Submodule Information

This repository includes the `blender-mcp` server as a git submodule. To update it:

```bash
git submodule update --remote blender-mcp
```

## Credits

BlenderMCP is created by [Siddharth Ahuja](https://x.com/sidahuj) and is a third-party integration not made by Blender Foundation.

Repository: https://github.com/ahujasid/blender-mcp
