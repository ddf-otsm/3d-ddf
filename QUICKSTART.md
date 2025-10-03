# Quick Start Guide - Blender MCP with Cursor

## 🛠️ Initial Setup (One-time)

### Step 0: Setup Development Environment
```bash
# Create virtual environment and install dependencies
./setup_venv.sh

# Activate it
source venv/bin/activate  # macOS/Linux
```

See [Virtual Environment Setup](docs/setup/VENV_SETUP.md) for details.

## 🚀 Getting Started in 3 Steps

### Step 1: Install Blender Addon (One-time setup)
1. Open **Blender**
2. `Edit > Preferences > Add-ons`
3. Click **Install** → Select: `/Users/luismartins/local_repos/3d-ddf/blender-mcp/addon.py`
4. ✅ Enable **"Interface: Blender MCP"**

### Step 2: Start Blender MCP Server
1. In Blender, press `N` to show sidebar
2. Click **"BlenderMCP"** tab
3. Click **"Connect to Claude"** button
4. ✅ Server should show as connected

### Step 3: Restart Cursor
1. Quit and restart Cursor
2. ✅ Look for the hammer icon 🔨 in Cursor (indicates MCP is active)

## 🎯 Test It

Try asking me:
- "Create a red sphere in Blender"
- "Add a blue cube next to it"
- "Make the scene lighting cinematic"

## 🔍 Check Blender Installation (Before Setup)

```bash
# Detect Blender on your system
python scripts/detect_blender.py

# Or manually check
which blender        # macOS/Linux
blender --version    # All platforms
```

**Don't have Blender?** See [Installation Guide](docs/setup/blender-installation.md)

## ❗ Troubleshooting

**MCP showing red or "no tools"?**
- ✓ Is Blender open?
- ✓ Is the addon enabled?
- ✓ Did you click "Connect to Claude" in Blender?
- ✓ Did you restart Cursor after connecting?

**"blender: command not found"?**
- Run `python scripts/detect_blender.py` to find Blender
- See [Blender Installation Guide](docs/setup/blender-installation.md)

**Still not working?**
1. Check Blender BlenderMCP panel shows "Connected"
2. Restart Cursor
3. See [Troubleshooting Guide](docs/setup/troubleshooting.md)

## 📝 Notes

- The MCP server runs from the local `blender-mcp/` submodule
- Blender must be running with the addon connected for the MCP to work
- Only run one instance at a time (don't use both Cursor and Claude Desktop)
