# 3D-DDF Documentation

Complete documentation for the 3D-DDF Blender MCP project.

## 📚 Documentation Structure

```
docs/
├── project/          # Project planning and releases
│   ├── roadmap.md   # Version timeline & features
│   ├── backlog.md   # Feature tracking (91 items)
│   ├── release.md   # Current release info
│   └── overview.md  # Complete project summary
├── guides/           # User guides
│   ├── blender-mcp-usage.md
│   └── rendering-guide.md
└── setup/            # Installation & troubleshooting
    ├── installation.md
    └── troubleshooting.md
```

## 🎯 Quick Navigation

### Project Planning
- **[Product Roadmap](project/roadmap.md)** - Version timeline from v1.0-alpha through v2.5-enhanced
- **[Feature Backlog](project/backlog.md)** - 91 tracked features with priorities and effort estimates
- **[Current Release](project/release.md)** - v1.0-alpha status and specifications
- **[Project Overview](project/overview.md)** - Complete technical summary

### Project History & Standards
- **[Taxonomy Rules](project/taxonomy-rules.md)** - ⭐ Complete naming conventions and structure rules
- **[Documentation Reorganization](project/docs-reorganization.md)** - How we organized all docs (Oct 2, 2025)
- **[Reorganization Summary](project/reorganization-summary.md)** - Project restructuring
- **[Photorealistic Fix](project/photorealistic-fix.md)** - Cycles rendering improvements
- **[Render Service Consolidation](project/render-service-consolidation.md)** - Render pipeline unification

### Getting Started
- **[Installation Guide](setup/installation.md)** - Step-by-step setup instructions
- **[Troubleshooting](setup/troubleshooting.md)** - Common issues and solutions

### User Guides
- **[MCP Usage Guide](guides/blender-mcp-usage.md)** - How to use Blender MCP
- **[Rendering Guide](guides/rendering-guide.md)** - Rendering workflow and best practices

## 📋 Documentation Standards

### File Organization Rules

**✅ Correct Locations:**
- Project planning docs → `docs/project/`
- User guides → `docs/guides/`
- Setup instructions → `docs/setup/`
- Project-specific docs → `projects/{name}/`

**❌ Avoid:**
- Root-level `.md` files (except `README.md`, `QUICKSTART.md`, `LICENSE.md`)
- Duplicate `documentation/` folders
- Scattered documentation across multiple locations

### Naming Conventions
- Use lowercase with hyphens: `feature-name.md`
- Be descriptive: `installation.md` not `setup.md`
- Group related docs in subdirectories

### Validation
Run `scripts/validate_taxonomy.py` to check complete taxonomy compliance:
- ✅ Documentation structure (docs/ organization)
- ✅ Export file naming conventions
- ✅ Project structure consistency

The pre-commit hook automatically validates before each commit.

---

**Last Updated**: October 2, 2025
