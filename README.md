# 3D-DDF with Blender MCP Integration

This repository integrates Blender with Cursor AI using the Model Context Protocol (MCP), allowing you to control Blender directly from Cursor. Create stunning 3D animations, renders, and scenes using natural language!

## 🚀 Quick Start

See **[QUICKSTART.md](QUICKSTART.md)** for a 3-step setup guide.

## 📁 Repository Structure

```
3d-ddf/
├── docs/              # Documentation and guides
├── projects/          
│   └── dadosfera/    # Complete dadosfera 3D branding project
│       ├── blender/           # Blender project files
│       ├── renders/           # Rendered outputs
│       │   ├── frames/        # Animation frames
│       │   └── stills/        # Single renders
│       └── exports/           # Final video exports
├── tests/             # Test suite for MCP integration
├── scripts/           # Utility scripts (planned)
└── blender-mcp/       # MCP server (submodule)
```

## 📖 Documentation

- **Setup**: [Installation Guide](docs/setup/installation.md) | [Troubleshooting](docs/setup/troubleshooting.md)
- **Guides**: [MCP Usage](docs/guides/blender-mcp-usage.md) | [Rendering](docs/guides/rendering-guide.md)
- **Tests**: [Test Suite](tests/README.md)

## 🎨 Project: Dadosfera 3D Branding

A comprehensive 3D animated branding project featuring the **"dadosfera"** logo with multiple rendering techniques. [See project →](projects/dadosfera/)

**Includes:**
- 🎬 10-second helicopter-style camera orbit animation
- 💎 Photorealistic crystal scene with metallic materials
- 💥 8 animated red explosion effects
- ✨ 15 glowing particle effects
- 🎨 Dual rendering: Cycles (ray-traced) & EEVEE (real-time)
- 📹 5 video exports + 13 rendered frames

## ⚡ Features

- **Object manipulation**: Create, modify, and delete 3D objects
- **Material control**: Apply realistic materials (glass, metal, emission)
- **Scene inspection**: Get detailed scene information
- **Animation**: Create camera paths and object animations
- **Rendering**: Both real-time (EEVEE) and ray-traced (Cycles)
- **Poly Haven integration**: Download models, textures, and HDRIs
- **Hyper3D AI models**: Generate 3D models using AI

## 🎯 Example Commands

Try asking Cursor:

- "Create a helicopter-style camera orbit around the scene"
- "Add a metallic sphere with cyan emission glow"
- "Render frames 1, 60, 120, 180, and 240 from the animation"
- "Make the lighting cinematic with three-point setup"
- "Create 8 red explosion spheres that appear throughout the animation"

See [MCP Usage Guide](docs/guides/blender-mcp-usage.md) for more examples.

## ⚙️ Prerequisites

- **Blender 3.0+** installed on macOS
- **Python 3.10+**
- **uv package manager**
- **Cursor** IDE

## ⚠️ Important Notes

- **Security Warning**: The MCP allows running arbitrary Python code in Blender. ALWAYS save your work before using it.
- **Single Instance**: Only run one instance of the MCP server at a time.

## 🔧 Development

- **Tests**: Run integration tests with `python3 tests/integration/test_blender_mcp_cube.py`
- **Submodule**: Update MCP server with `git submodule update --remote blender-mcp`

## 📝 Credits

**BlenderMCP** is created by [Siddharth Ahuja](https://x.com/sidahuj) and is a third-party integration not made by Blender Foundation.

Repository: https://github.com/ahujasid/blender-mcp

**3D-DDF Projects** created with Cursor AI + Blender MCP on Apple M3 Max (30 GPU cores)
