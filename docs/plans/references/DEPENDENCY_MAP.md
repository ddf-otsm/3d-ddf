# Dependency & Bi-directional Map

**Last Updated**: 2025-10-03  
**Purpose**: Track dependencies between active plans, projects, and technical components

## Conventions
- Use exact file paths for accuracy
- Maintain "Depends on" and "Required by" symmetry
- Update when plans are archived or consolidated
- Add "Task moved to" / "Task received from" annotations for consolidations

---

## 🟢 Active Plans

### `docs/plans/active/logo-to-3d-service.md`
**Status**: 🔄 Planning (High Priority)  
**Depends on**:
  - `services/logo-to-3d/` (implementation code)
  - `services/logo-to-3d/src/core/blender_server.py` (Blender integration)
  - `docs/plans/active/MODERNIZATION_REPORT.md` (FastAPI/Pydantic versions)
  - `.env.example` (environment configuration)

**Required by**:
  - `docs/projects/dadosfera/prioritized/TASKS.md` (project-level execution)
  - `docs/plans/active/explosion-development-roadmap.md` (integration target)

**Related**:
  - `docs/setup/installation.md` (setup instructions)
  - `requirements.txt` (Python dependencies)

---

### `docs/plans/active/explosion-development-roadmap.md`
**Status**: 🔄 Active (High Priority - v1.5-beta complete)  
**Depends on**:
  - `scripts/explosions/` (explosion implementation scripts)
  - `projects/explosion-test/` (test project and validation)
  - `projects/explosion-test/VALIDATION_CHECKLIST.md` (validation framework)

**Required by**:
  - `docs/projects/dadosfera/prioritized/TASKS.md` (integration into main project)
  - `docs/plans/active/logo-to-3d-service.md` (receives explosions in name pipeline)

**Consolidates** (archived on 2025-10-03):
  - `docs/plans/active/explosion-realism-improvements.md` → See consolidation section
  - `docs/plans/active/explosion-content-consolidation.md` → See consolidation section

**Related**:
  - `projects/explosion-test/RENDER_BATCHES.md` (render tracking)
  - `projects/explosion-test/README.md` (project overview)

---

## 📦 Archived/Redirect Plans

### `docs/plans/active/phase1-basic-integration.md`
**Status**: ✅ Complete  
**Note**: Minimal dependency tracking needed (complete and stable)

### `docs/plans/active/phase2-registration-integration.md`
**Status**: 📦 Archived → `docs/plans/finished/phase2-registration-integration.md`  
**Date**: 2025-10-03

### `docs/plans/active/phase3-game-development.md`
**Status**: 📦 Archived → `docs/plans/finished/phase3-game-development.md`  
**Date**: 2025-10-03

### `docs/plans/active/phase4-professional-marketplaces.md`
**Status**: 📦 Archived → `docs/plans/finished/phase4-professional-marketplaces.md`  
**Date**: 2025-10-03

### `docs/plans/active/advanced-features.md`
**Status**: 📦 Archived → `docs/plans/finished/advanced-features.md`  
**Date**: 2025-10-03

### `docs/plans/active/explosion-realism-improvements.md`
**Status**: 📦 Consolidated → `explosion-development-roadmap.md` (section: Realism Improvements)  
**Date**: 2025-10-03

### `docs/plans/active/explosion-content-consolidation.md`
**Status**: 📦 Consolidated → `explosion-development-roadmap.md` (section: Content Consolidation)  
**Date**: 2025-10-03

---

## 📚 Supporting Documentation

### `docs/plans/active/README.md`
**Purpose**: Active plans index and status summary  
**Depends on**:
  - All active plan files (for status aggregation)

**Required by**:
  - Developers navigating plan structure
  - `docs/plans/active/EXECUTION_SUMMARY_2025-10-03.md` (references structure)

---

### `docs/plans/active/MODERNIZATION_REPORT.md`
**Purpose**: Security, CVE tracking, and version management  
**Depends on**:
  - `services/logo-to-3d/pyproject.toml` (current versions)
  - `requirements.txt` (project dependencies)
  - `.env.example` (environment configuration)

**Required by**:
  - `docs/plans/active/logo-to-3d-service.md` (FastAPI/Uvicorn/Pydantic versions)
  - Security/upgrade planning decisions

**Related**:
  - `docs/plans/active/PATH_MIGRATION_PLAN.md` (portability and environment)

---

### `docs/plans/active/PATH_MIGRATION_PLAN.md`
**Purpose**: Path portability and environment variable strategy  
**Depends on**:
  - `.env.example` (canonical path definitions)
  - `docs/plans/active/MODERNIZATION_REPORT.md` (cross-platform considerations)

**Required by**:
  - All setup guides that reference paths
  - Scripts that use `PROJECT_ROOT` or `BLENDER`

**Related**:
  - `docs/setup/` (all setup guides updated for portability)

---

### `docs/plans/active/DEPENDENCY_MAP.md` (this file)
**Purpose**: Centralized dependency tracking  
**Depends on**:
  - All active plan files (reads dependencies)

**Required by**:
  - Developers planning task execution order
  - Navigation and impact analysis

---

### `docs/plans/active/CONVERSATION_ACTIONS_2025-10-03.md`
**Purpose**: Daily action tracking log  
**Depends on**:
  - Active conversation context

**Required by**:
  - `docs/plans/active/PROGRESS_AND_RESOURCING.md` (progress rollup)

---

### `docs/plans/active/EXECUTION_SUMMARY_2025-10-03.md`
**Purpose**: Execution results documentation  
**Depends on**:
  - Completed tasks from priority list (items 1-5)

**Required by**:
  - Historical record and audit trail
  - Future sprint planning reference

---

### `docs/plans/active/PROGRESS_AND_RESOURCING.md`
**Purpose**: Resource allocation and progress tracking  
**Depends on**:
  - `docs/plans/active/CONVERSATION_ACTIONS_2025-10-03.md`
  - All active plan progress

**Required by**:
  - Resource planning decisions

---

## 🎯 Project-Level Dependencies

### `docs/projects/dadosfera/prioritized/TASKS.md`
**Purpose**: Dadosfera project task prioritization  
**Depends on**:
  - `docs/plans/active/logo-to-3d-service.md` (name-to-video pipeline)
  - `docs/plans/active/explosion-development-roadmap.md` (explosion effects)

**Required by**:
  - Dadosfera project execution

---

### `projects/explosion-test/`
**Purpose**: Explosion system validation and testing  
**Contains**:
  - `VALIDATION_CHECKLIST.md` (validation framework)
  - `RENDER_BATCHES.md` (render tracking)
  - `README.md` (project overview)
  - `scripts/` (test scripts)
  - `tests/` (automated tests)

**Required by**:
  - `docs/plans/active/explosion-development-roadmap.md`

---

## 🔧 Technical Component Dependencies

### `services/logo-to-3d/`
**Purpose**: Logo/text to 3D API service  
**Key Files**:
  - `pyproject.toml` (dependencies)
  - `src/core/blender_server.py` (Blender integration)
  - `src/api/main.py` (FastAPI app)

**Required by**:
  - `docs/plans/active/logo-to-3d-service.md`

---

### `scripts/explosions/`
**Purpose**: Explosion generation and rendering scripts  
**Key Files**:
  - `create_production_explosion.py`
  - `render_explosions.py`
  - `integrate_with_main_project.py`

**Required by**:
  - `docs/plans/active/explosion-development-roadmap.md`
  - `projects/explosion-test/`

---

### `.env.example`
**Purpose**: Environment configuration template  
**Required by**:
  - All setup guides (`docs/setup/`)
  - All scripts using `PROJECT_ROOT` or `BLENDER`
  - `docs/plans/active/PATH_MIGRATION_PLAN.md`

---

## 🔄 Consolidation Tracking

### Explosion Plans Consolidation (2025-10-03)

**Before**:
- `docs/plans/active/explosion-development-roadmap.md` (primary)
- `docs/plans/active/explosion-realism-improvements.md` (separate)
- `docs/plans/active/explosion-content-consolidation.md` (separate)

**After**:
- `docs/plans/active/explosion-development-roadmap.md` (consolidated)
  - Section: "📦 Consolidated Tasks from Related Plans"
  - Subsection: "Realism Improvements" (from explosion-realism-improvements.md)
  - Subsection: "Content Consolidation" (from explosion-content-consolidation.md)

**Redirect Stubs Created**:
- `explosion-realism-improvements.md` → points to roadmap
- `explosion-content-consolidation.md` → points to roadmap

---

## 📝 Maintenance Notes

### When Adding New Plans
1. Add entry to this file with "Depends on" and "Required by"
2. Add reciprocal entries in dependent files
3. Update `docs/plans/active/README.md` status table
4. Ensure symmetry of dependencies

### When Archiving Plans
1. Move file to `docs/plans/finished/`
2. Create redirect stub in `docs/plans/active/`
3. Update this file to show archived status
4. Remove from `docs/plans/active/README.md` active list
5. Update dependent plans to remove references

### When Consolidating Plans
1. Merge content into target plan
2. Add "Task received from" section in target
3. Create redirect stubs for source plans
4. Update this file to show consolidation
5. Update dependency links to point to consolidated plan

---

## 🎯 Quick Reference: Current Active Dependencies

```
logo-to-3d-service.md
  ├─ depends on: services/logo-to-3d/, MODERNIZATION_REPORT.md, .env.example
  └─ required by: dadosfera/TASKS.md, explosion-development-roadmap.md

explosion-development-roadmap.md
  ├─ depends on: scripts/explosions/, explosion-test/, VALIDATION_CHECKLIST.md
  ├─ consolidates: explosion-realism-improvements.md, explosion-content-consolidation.md
  └─ required by: dadosfera/TASKS.md, logo-to-3d-service.md
```

---

**Last Review**: 2025-10-03  
**Next Review**: When plans change status or new plans added  
**Maintained By**: Development team / AI agents
