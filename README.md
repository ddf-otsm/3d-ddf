# 3D-DDF with Blender MCP Integration

This repository integrates Blender with Cursor AI using the Model Context Protocol (MCP), allowing you to control Blender directly from Cursor. Create stunning 3D animations, renders, and scenes using natural language!

## 🚀 Quick Start

See **[QUICKSTART.md](QUICKSTART.md)** for a 3-step setup guide.

## 📁 Repository Structure

```
3d-ddf/
├── docs/                    # Documentation and guides
│   ├── project/            # Project planning, roadmaps, releases
│   ├── guides/             # User guides and tutorials
│   └── setup/              # Installation and troubleshooting
├── projects/               # Production projects
│   ├── dadosfera/          # Complete dadosfera 3D branding project
│   │   ├── blender_files/  # Blender scene files
│   │   ├── config/         # Project configuration
│   │   ├── exports/        # Final video exports (taxonomy compliant)
│   │   ├── renders/        # Rendered outputs and test batches
│   │   └── PROJECT_STRUCTURE.md
│   └── explosion-test/     # Explosion system development and testing
│       ├── blender_files/  # Test scene files
│       ├── exports/        # Explosion showcase exports
│       ├── renders/        # Test render batches
│       └── README.md
├── tests/                  # Test suite for MCP integration
│   ├── unit/              # Unit tests (33/33 passing)
│   ├── integration/       # Integration tests
│   ├── explosions/        # Explosion system tests
│   └── README.md
├── scripts/               # Utility scripts and tools
│   ├── explosions/        # Explosion system components
│   │   ├── config.py      # Configuration dataclasses
│   │   ├── materials.py   # Material creation utilities
│   │   ├── create_production_explosion.py  # Main explosion logic
│   │   └── README.md      # Component documentation
│   ├── detect_blender.py  # Blender installation detection
│   ├── create_explosion_video.py  # Video creation pipeline
│   └── validate_taxonomy.py  # Project structure validation
├── logs/                  # Render logs and system logs
└── blender-mcp/           # MCP server (submodule)
```

## 📖 Documentation

### Getting Started
- **Setup**: [Virtual Environment](docs/setup/VENV_SETUP.md) | [Installation Guide](docs/setup/installation.md) | [Troubleshooting](docs/setup/troubleshooting.md)
- **Guides**: [MCP Usage](docs/guides/blender-mcp-usage.md) | [Rendering](docs/guides/rendering-guide.md)
- **Tests**: [Test Suite](tests/README.md)

### Planning & Releases
- **Product Roadmap**: [docs/project/roadmap.md](docs/project/roadmap.md) - Version timeline and feature planning
- **Feature Backlog**: [docs/project/backlog.md](docs/project/backlog.md) - Detailed feature tracking and priorities
- **Current Release**: [docs/project/release.md](docs/project/release.md) - v1.0-alpha status and specs
- **Project Overview**: [docs/project/overview.md](docs/project/overview.md) - Complete technical summary

**📚 [View all documentation →](docs/README.md)**

## 🎯 Example Commands

Try asking Cursor:

### 🎬 **3D Scene Creation**
- "Create a helicopter-style camera orbit around the scene"
- "Add a metallic sphere with cyan emission glow"
- "Make the lighting cinematic with three-point setup"

### 💥 **Explosion System**
- "Create 8 red explosion spheres that appear throughout the animation"
- "Add a massive explosion at the center of the scene"
- "Create multiple explosions with different quality levels"
- "Render an explosion showcase video"

### 📹 **Rendering & Export**
- "Render frames 1, 60, 120, 180, and 240 from the animation"
- "Export the current scene as a 1080p video following the project taxonomy"
- "Create a preview render of the explosion sequence"

See [MCP Usage Guide](docs/guides/blender-mcp-usage.md) and [Explosion Creation Guide](docs/guides/explosion-creation.md) for comprehensive examples.

## 🛠️ Development Setup

### Quick Start
```bash
# Clone and setup
git clone <repo-url> 3d-ddf
cd 3d-ddf

# Create virtual environment and install dependencies
./setup_venv.sh

# Activate virtual environment
source venv/bin/activate

# Run tests
pytest tests/
```

See [Virtual Environment Setup Guide](docs/setup/VENV_SETUP.md) for detailed instructions.

## ⚙️ Prerequisites

- **Blender 3.0+** installed ([Installation guide](docs/setup/blender-installation.md))
- **Python 3.10+**
- **uv package manager**
- **Cursor** IDE

### 🔍 Check Blender Installation

```bash
# Quick check
python scripts/detect_blender.py

# Manual check
which blender  # macOS/Linux
blender --version
```

See [Blender Installation Guide](docs/setup/blender-installation.md) for detailed setup.

## 💥 Explosion System (v1.0-alpha)

The 3D-DDF project features a **production-ready explosion system** with hybrid particle + volume rendering for realistic effects.

### 🎬 Latest Demo
- **Showcase Video**: `projects/explosion-test/exports/explosion_test_alpha_20251002_1080p_showcase.mp4`
- **Duration**: 3.1 seconds | **Resolution**: 1920×1080 | **Size**: 249KB
- **Features**: 4 explosions, cinematic camera, professional lighting

### 🚀 Quick Demo
```bash
# Create explosion showcase (requires Blender)
python scripts/create_explosion_video.py --quality production

# Run explosion tests (no Blender required)
pytest tests/explosions/ -v  # 100% pass rate
```

### 📚 Documentation
- [💥 Explosion System Guide](scripts/explosions/README.md) - Complete technical overview
- [🎯 Active Development Plans](docs/plans/active/explosion-development-roadmap.md)
- [🧪 Test Results](docs/project/test_pass_summary_20251002.md)

**Status**: ✅ Production Ready | **Test Coverage**: 100% | **Integration**: Complete

## ⚠️ Important Notes

- **Security Warning**: The MCP allows running arbitrary Python code in Blender. ALWAYS save your work before using it.
- **Single Instance**: Only run one instance of the MCP server at a time.

## 🔧 Development

- **Tests**: Run all tests with `pytest tests/ -v -m "not blender"` (33/33 passing)
- **Blender Tests**: `pytest tests/ -v -m "blender"` (requires live Blender + MCP server)
- **Taxonomy Validation**: `python scripts/validate_taxonomy.py`
- **Submodule**: Update MCP server with `git submodule update --remote blender-mcp`

## 📝 Credits

**BlenderMCP** is created by [Siddharth Ahuja](https://x.com/sidahuj) and is a third-party integration not made by Blender Foundation.

Repository: https://github.com/ahujasid/blender-mcp

**3D-DDF Projects** created with Cursor AI + Blender MCP on Apple M3 Max (30 GPU cores)

## 🎯 Project Status

### ✅ **Current Release: v1.0-alpha**
- **MCP Integration**: ✅ Complete (Blender ↔ Cursor communication)
- **Dadosfera Project**: ✅ Active (3D branding animations)
- **Explosion System**: ✅ Production Ready (v1.0-alpha)
- **Test Coverage**: ✅ 100% (33/33 non-Blender tests)
- **Documentation**: ✅ Complete with taxonomy compliance

### 🚀 **Ready for Production**
- **Explosion Showcase**: Available at `projects/explosion-test/exports/explosion_test_alpha_20251002_1080p_showcase.mp4`
- **Integration Ready**: Seamless integration with Dadosfera and other projects
- **Quality Assured**: Comprehensive test suite and validation

### 📈 **Next Milestones**
- **v1.0-beta**: Performance optimizations and user feedback integration
- **v1.0-stable**: Full production deployment with advanced features
- **v2.0**: Multi-project orchestration and advanced asset management

**For full changelog, see [docs/project/CHANGELOG.md](docs/project/CHANGELOG.md).**
