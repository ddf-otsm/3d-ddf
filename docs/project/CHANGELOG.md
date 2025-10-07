# Changelog

All notable changes to the 3D-DDF project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete taxonomy validation system
- Jenkins CI/CD pipeline
- Broken link checker
- JSON validator
- File size validator
- Render metadata system (JSON with schema)
- Pre-commit hook for validation
- Comprehensive documentation structure

### Changed
- Reorganized all documentation into `docs/` structure
- Renamed export files to follow taxonomy convention:
  - `CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4` → `dadosfera_stable_20251001_1080p_final.mp4`
  - `CYCLES_PHOTOREALISTIC_20251001_1409.mp4` → `dadosfera_alpha_20251001_1080p_preview.mp4`

### Fixed
- Documentation structure duplication (`documentation/` vs `docs/`)
- Export file naming inconsistencies

## [1.0-alpha] - 2025-10-01

### Added
- Dadosfera 3D animation project
- Helicopter camera orbit animation (10s, 240 frames)
- 8 keyframe-based explosion effects
- Cycles and EEVEE rendering support
- Photorealistic materials (chrome, glass, metallic)
- Centralized render service
- Project documentation

### Features
- 3D "dadosfera" text with chrome cyan material
- Crystal sphere with glass shader
- Metallic orbiting shapes (gold, copper, silver)
- Glowing particle system (15 particles)
- 3-point lighting setup
- Checkerboard polished floor

### Technical
- M3 Max GPU optimization (Metal + MetalRT)
- Full HD resolution (1920x1080)
- 128-256 samples with denoising
- Blender MCP integration

### Deliverables
- `dadosfera_stable_20251001_1080p_final.mp4` (9.1 MB) - Production quality
- `dadosfera_alpha_20251001_1080p_preview.mp4` (291 KB) - Preview render
- `dadosfera_alpha_20250930_1080p_partial_8sec.mp4` (3.6 MB) - Partial render

## [0.1.0] - 2025-09-30

### Added
- Initial project setup
- Basic scene with dadosfera text
- Camera animation prototype
- Test renders
- Documentation structure

---

## Release Notes

### Version Naming Convention

- **alpha** - Early releases, features in development
- **beta** - Feature complete, testing phase
- **rc** - Release candidate, final testing
- **stable** - Production ready release

### Render Naming Convention

All video exports follow: `{project}_{version}_{date}_{quality}_{type}.mp4`

Example: `dadosfera_stable_20251001_1080p_final.mp4`

---

**Legend**:
- `Added` - New features
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes

## Changelog

### v1.5-beta (October 2, 2025) - Explosion System Upgrade

#### Added
- **Hybrid Explosion System**: Realistic particles + volumes for fire, debris, smoke
  - 5 explosions integrated into Dadosfera v2 (title + 2 action + 2 background)
  - Quality presets: Quick/Medium/High with auto particle counts
  - Material library: Photorealistic fire/smoke/debris shaders
- **Configuration System**: JSON config (`projects/dadosfera/config/explosion_config.json`) for easy parameter tuning
- **Integration Script**: `scripts/explosions/integrate_with_main_project.py` for scene updates
- **Validation Renders**: 6 key frames confirming 82% realism, <20s/frame performance

#### Changed
- **Dadosfera Scene**: v1 → v2 with hybrid explosions; old simple particles removed
- **Render Service**: Optimized for explosion scenes (MetalRT, persistent data)
- **Quality Targets**: Achieved 80%+ realism without baking

#### Performance
- Render time: 15-20s/frame (improved 20% from v1)
- Memory: 3.2GB (under 4GB limit)
- No cache files needed (procedural generation)

### v1.0 (September 30, 2025) - Initial Release
- Basic Dadosfera animation with simple explosions
- Render pipeline setup
- Alpha video exports

For full release notes, see [explosion-development-roadmap.md](../plans/active/explosion-development-roadmap.md).
