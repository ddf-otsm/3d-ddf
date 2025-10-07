# Project Taxonomy

This document outlines the naming conventions, file organization, and structural patterns used throughout the 3D-DDF project.

## File Organization

See [Taxonomy Complete](taxonomy-complete.md) for detailed file organization rules.

## Naming Conventions

- Timestamps: `YYYYMMDD_HHMM_` prefix for all output files
- Projects: `dadosfera`, `explosion-test`
- Versions: `alpha`, `beta`, `rc`, `stable`, `deprecated`
- Quality: `270p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `4k`

## Directory Structure

```
docs/
├── guides/          # User-facing guides
├── plans/           # Development plans and roadmaps
├── project/         # Project documentation
├── setup/           # Installation and setup guides
└── testing/         # Testing documentation

integrations/        # Integration code by phase
├── phase1/         # Basic integration
├── phase2/         # Registration integration
├── phase3/         # Game development
├── phase4/         # Professional marketplaces
└── advanced/       # Advanced features

projects/           # Project-specific content
├── dadosfera/      # Dadosfera project
└── explosion-test/ # Explosion testing project

scripts/            # Utility and automation scripts
services/           # Service implementations
tests/              # Test suites
```
