# Explosion Development Roadmap — Tier‑1 Execution Pack (Enhanced)

**Pack Version**: 2.0 (Sonnet 4.5 Enhanced)  
**Source Plan**: `docs/plans/active/explosion-development-roadmap.md`  
**Owners**: VFX Team  
**Status**: Active (High Priority)  
**Last Updated (Source)**: 2025-10-04  
**Pack Created**: 2025-10-07  

---

## 🎯 Mission & Context

### Primary Goal
Deliver a production-ready, realistic explosion system using hybrid particle + volume approach that:
- Produces visually compelling results (75-85% realism target)
- Executes deterministically without manual intervention
- Maintains performance targets (<15s/frame @ 1080p)
- Integrates seamlessly with Dadosfera project pipeline

### Current State Assessment
- **Completed**: Hybrid explosion implementation, production scripts, test suite (18/18 passing)
- **In Progress**: Scene baseline creation, integration with main project
- **Pending**: Final render validation, performance optimization, documentation updates

### Strategic Context
This plan consolidates work from:
- `explosion-realism-improvements.md` (archived 2025-10-03)
- `explosion-content-consolidation.md` (archived 2025-10-03)
- Current active roadmap with fresh start approach

---

## 📋 Scope & Boundaries

### In Scope
1. **Path Safety & Portability**
   - Eliminate all hardcoded user paths (`/Users/<name>`, `/home/<name>`)
   - Replace with environment variables (`${HOME}`, `${PROJECT_ROOT}`)
   - Validate portability across macOS/Linux environments

2. **Script Validation & Testing**
   - Verify importability of core explosion scripts
   - Run existing test suite (239 tests available)
   - Ensure render_production.py works with both projects

3. **Baseline Scene Creation**
   - Create clean `dadosfera_v2_clean.blend` with professional materials
   - Create `particle_explosion_v1.blend` with Quick Smoke setup
   - Integrate and render validation keyframes

4. **Documentation & Artifacts**
   - Update project READMEs with current state
   - Archive analysis results under `projects/*/analysis/`
   - Maintain render batch tracking

### Out of Scope
- Advanced animation features (deferred to Phase 2)
- Cloud deployment (local execution only)
- Real-time preview systems
- External API integrations

---

## 🔗 Dependencies & Prerequisites

### Required Files & Directories
- `scripts/render_production.py` — Multi-project render orchestration
- `scripts/explosions/` — Explosion creation modules (if present)
- `projects/dadosfera/` — Main project structure
- `projects/explosion-test/` — Validation project structure
- `tests/explosions/` — Test suite (18 tests)

### External Dependencies
- **Blender 4.2+**: Headless execution capability
- **Python 3.11+**: Script runtime
- **GNU timeout** (`gtimeout` on macOS): Process timeout enforcement
- **FFmpeg**: Video encoding (optional, for final outputs)

### Environment Variables
```bash
export PROJECT_ROOT="${HOME}/local_repos/3d-ddf"
export BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"
```

---

## ✅ Success Criteria

### Technical Metrics
- [ ] **Zero hardcoded paths**: `validate_paths.py` reports 0 findings
- [ ] **All tests passing**: 239/239 tests green (or documented skips)
- [ ] **Script importability**: All explosion scripts import without errors
- [ ] **Render validation**: Keyframes (1, 24, 48, 72, 96, 120) generated successfully

### Quality Metrics
- [ ] **Visual realism**: 75-85% target (subjective assessment)
- [ ] **Performance**: <15s/frame average @ 1080p preview quality
- [ ] **Memory usage**: <4GB VRAM during render
- [ ] **File sizes**: Render outputs <10MB per frame PNG

### Process Metrics
- [ ] **Test-gated commits**: All commits pass pre-commit hooks
- [ ] **Documentation current**: READMEs reflect actual file locations
- [ ] **Artifact tracking**: All renders logged in batch tracking docs

---

## 🚨 Risk Assessment & Mitigation

### High Risk: Blender Environment Availability
- **Impact**: Cannot execute render tasks without Blender
- **Mitigation**: Early verification step; clear error messages; fallback to mock validation
- **Escalation**: Document Blender installation requirements; provide setup guide

### Medium Risk: Test Flakiness
- **Impact**: False negatives block commits
- **Mitigation**: Retry logic (2 attempts); timeout enforcement; mock Blender in CI
- **Escalation**: Mark flaky tests with `@pytest.mark.flaky`; investigate root cause

### Low Risk: Path Replacement Breaking Functionality
- **Impact**: Scripts fail after path substitution
- **Mitigation**: Comprehensive verification step; run smoke tests post-replacement
- **Escalation**: Rollback capability via git; manual review of sed replacements

---

## 📊 Execution Metrics

### Estimated Effort
- **AI Hours**: 2-3 hours (script execution, verification, documentation)
- **Human Hours**: 1-2 hours (review, approval, manual validation)
- **Total Duration**: 1 day (with review cycles)

### Task Breakdown
- Path safety: 30 min
- Script validation: 45 min
- Test execution: 60 min
- Baseline creation: 90 min (if Blender available)
- Documentation: 30 min

---

## 🔄 Integration Points

### Upstream Dependencies
- `docs/plans/active/QUALITY_AND_VALIDATION_CONSOLIDATED.md` — Path validation standards
- `mini_prompt/lv2/test_driven_commit_mini_prompt.md` — Commit gating process

### Downstream Consumers
- `docs/projects/dadosfera/prioritized/TASKS.md` — Integration into main project
- `docs/plans/active/logo-to-3d-service.md` — Receives explosions in name pipeline

### Related Artifacts
- `projects/dadosfera/analysis/render_comparison_20251004/` — Visual quality baseline
- `projects/explosion-test/RENDER_BATCHES.md` — Historical render tracking

---

## 📚 Reference Documentation

### Internal Docs
- Source plan: `docs/plans/active/explosion-development-roadmap.md`
- Test guide: `projects/explosion-test/HOW_TO_RUN_VALIDATION.md`
- Render guide: `docs/guides/rendering-guide.md`

### External Resources
- Blender Python API: https://docs.blender.org/api/current/
- Cycles Rendering: https://docs.blender.org/manual/en/latest/render/cycles/

---

## 🎬 Next Actions (Post-Execution)

1. **Immediate**: Verify all postconditions met; review logs
2. **Short-term**: Create baseline scenes if Blender available
3. **Medium-term**: Integrate explosions into dadosfera_v2_clean.blend
4. **Long-term**: Performance optimization; advanced material system

---

**Approval Status**: ⏳ Pending Execution  
**Review Required**: Yes (post-execution)  
**Escalation Contact**: VFX Team Lead