# 3D-DDF Test Suite: Achieve 100% Pass Rate Plan

## Executive Summary

**Current Status** (as of October 5, 2025):
- **Total Tests**: 272
- **Passing**: 223 (82%)
- **Failing**: 49 (18%)
- **Deselected in Pre-Push**: 264 (intentionally excluded for speed; these include most failures)
- **Critical/High Priority**: 45/45 (100% pass rate - production-ready)

**Goal**: Achieve **100% pass rate** for the full test suite by addressing all 49 failures. This will enable:
- Reliable post-push validation
- Comprehensive CI/CD coverage
- Reduced false negatives in monitoring

**Estimated Timeline**: 2 weeks (Phase 1: 1 week, Phase 2: 1 week)
**Priority**: High (blocks full CI/CD confidence)
**Owner**: Development Team
**Dependencies**: Blender installation, missing Python modules (freetype, torch), import path fixes

## Problem Analysis

### Test Failure Categories
The 49 failures are categorized as follows:

1. **Blender-Dependent Tests** (23 failures, 47%):
   - Missing `bpy` module (Blender Python API)
   - GPU rendering tests requiring CUDA
   - Examples: `test_blender_render.py`, `test_gpu_integration.py`
   - Impact: Blocks 3D rendering validation

2. **Logo-to-3D Service Tests** (16 failures, 33%):
   - Missing `src` module (import path issues)
   - Missing `freetype` dependency for font processing
   - Examples: `test_text_to_3d_pipeline.py`, `test_font_manager.py`
   - Impact: Breaks text-to-3D pipeline validation

3. **Validation Script Tests** (10 failures, 20%):
   - Import path issues for `scripts/` modules
   - Syntax errors in validation logic
   - Examples: `test_validate_json.py`, `test_utility_scripts.py`
   - Impact: Affects documentation and metadata validation

### Deselected Tests Context
- **264 deselected tests** are intentionally excluded in pre-push for speed (0.2s runtime)
- These include the 49 failures + 215 non-critical tests
- Post-push runs the **full suite** (no exclusions) to catch all issues
- **Critical tests** (45) pass 100%, ensuring core functionality is protected

## Fix Strategy

### Phase 1: Critical Fixes (Week 1 - Target: 95% Pass Rate)
Focus on high-impact failures that block core workflows.

#### 1.1 Fix Blender-Dependent Tests (23 failures)
**Steps**:
1. Install Blender locally for testing:
   ```bash
   # macOS
   brew install --cask blender
   
   # Add to PATH
   echo 'export PATH="/Applications/Blender.app/Contents/Resources/2.93/python/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
2. Mock Blender API for non-GPU environments:
   - Create `tests/mocks/mock_bpy.py` with minimal `bpy` stubs
   - Use `@patch('bpy')` in tests for simulation
3. Run Blender-specific tests:
   ```bash
   # Run only Blender tests
   pytest tests/ -v -m "blender"
   
   # Expected: 23/23 pass after fixes
   ```
4. Fix GPU rendering tests:
   - Install CUDA toolkit if needed
   - Use environment variables for mock GPU: `CUDA_VISIBLE_DEVICES="" pytest -m "gpu"`

**Timeline**: Days 1-3
**Success Metric**: 23/23 Blender tests pass

#### 1.2 Fix Logo-to-3D Service Tests (16 failures)
**Steps**:
1. Install missing dependencies:
   ```bash
   cd services/logo-to-3d
   pip install freetype-py torch pillow
   ```
2. Fix import paths:
   - Add `services/logo-to-3d` to PYTHONPATH in tests
   - Update imports from `src.` to relative paths
3. Run service tests:
   ```bash
   cd services/logo-to-3d
   PYTHONPATH=. pytest tests/ -v
   
   # Expected: 16/16 pass
   ```
4. Mock external dependencies (e.g., font files) using pytest fixtures

**Timeline**: Days 4-5
**Success Metric**: 16/16 service tests pass

#### 1.3 Quick Wins: Validation Script Tests (10 failures)
**Steps**:
1. Fix import paths in `tests/unit/`:
   - Update relative imports for `scripts/` modules
   - Add `sys.path.insert(0, str(project_root))` in test setup
2. Run validation tests:
   ```bash
   pytest tests/unit/ -v -k "validate"
   
   # Expected: 10/10 pass
   ```
3. Handle edge cases in validation logic (e.g., missing files)

**Timeline**: Days 6-7
**Success Metric**: 10/10 validation tests pass
**Phase 1 Total**: 239/272 pass (88%)

### Phase 2: Full Suite Optimization (Week 2 - Target: 100% Pass Rate)
Polish and optimize the remaining tests.

#### 2.1 Integration & Edge Case Tests
**Steps**:
1. Run full suite locally:
   ```bash
   # Run all tests (no exclusions)
   pytest tests/ -v --tb=short
   
   # Focus on remaining failures
   pytest tests/ -v --tb=short -k "FAILED"
   ```
2. Add comprehensive fixtures:
   - Mock external services (Blender, fonts, ML models)
   - Use `conftest.py` for shared setup
3. Parallel execution for speed:
   ```bash
   pytest tests/ -v -n auto  # Run in parallel
   ```

#### 2.2 Test Coverage & Refactoring
**Steps**:
1. Generate coverage report:
   ```bash
   pip install pytest-cov
   pytest tests/ --cov=scripts --cov-report=html
   ```
2. Refactor failing tests:
   - Replace hard dependencies with mocks
   - Add `@pytest.mark.skipif` for environment-specific tests
3. Verify 100% coverage for critical paths

**Timeline**: Days 8-10
**Success Metric**: 100% pass rate (272/272)

#### 2.3 Documentation & Maintenance
**Steps**:
1. Update test documentation in `docs/testing/full-suite-guide.md`
2. Add CI/CD configuration for full suite runs
3. Create maintenance checklist for test health

**Timeline**: Days 11-14
**Success Metric**: Documented process for ongoing 100% maintenance

## Local Run Commands for Deselected/Failing Tests

### Run All Deselected Tests (Full Suite)
```bash
# Run everything (no exclusions) - catches all 49 failures
pytest tests/ -v --tb=short

# Run with verbose output for failures only
pytest tests/ -v --tb=short -rf  # Show failures with full traceback
```

### Run Specific Failure Categories
1. **Blender Tests Only**:
   ```bash
   pytest tests/ -v -m "blender"
   ```

2. **Logo-to-3D Tests Only**:
   ```bash
   cd services/logo-to-3d
   PYTHONPATH=. pytest tests/ -v
   ```

3. **Validation Tests Only**:
   ```bash
   pytest tests/unit/ -v -k "validate"
   ```

### Run Failing Tests Only
```bash
# List all failing tests
pytest tests/ --collect-only | grep -E "FAILED|ERROR"

# Run just the failing ones
pytest tests/ -v -k "FAILED or ERROR"
```

### Environment Setup for Testing
```bash
# Install all dependencies
pip install -r requirements.txt
pip install -r services/logo-to-3d/requirements.txt

# Install Blender (macOS)
brew install --cask blender
echo 'export PATH="/Applications/Blender.app/Contents/Resources/4.2/python/bin:$PATH"' >> ~/.zshrc

# Install freetype for logo-to-3d
pip install freetype-py

# Verify setup
python -c "import bpy, freetype; print('All modules available')"
```

## Dependencies & Prerequisites

### Required Installations
1. **Python Packages**:
   ```bash
   pip install pytest pytest-cov freetype-py torch pillow
   ```

2. **Blender**:
   - Version: 4.2+ LTS
   - GPU Support: CUDA 11.8+ (for rendering tests)

3. **System Dependencies**:
   ```bash
   # macOS
   brew install nvidia-cuda-toolkit
   
   # Ubuntu
   sudo apt install libfreetype6-dev
   ```

### Test Environment Variables
Add to `.env` or export:
```bash
export BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
export PYTHONPATH="${PYTHONPATH}:services/logo-to-3d"
export CUDA_VISIBLE_DEVICES="0"
```

## Verification & Success Metrics

### Phase 1 Verification (88% Pass Rate)
```bash
# Run full suite
pytest tests/ -v --tb=no  # Should show 239/272 PASSED

# Check critical tests
pytest tests/ -v -k "critical or high"  # 45/45 PASSED

# Coverage report
pytest --cov=scripts --cov-report=term-missing
```

### Phase 2 Verification (100% Pass Rate)
```bash
# Full suite validation
pytest tests/ -v  # 272/272 PASSED

# No failures
pytest tests/ -v -rf  # No output (no failures)

# Post-push simulation
bash .git/hooks/post-push  # Should end with "✅ Post-push validation completed successfully!"
```

### Success Metrics
- **Phase 1**: 239/272 tests pass (88%) + 100% critical tests
- **Phase 2**: 272/272 tests pass (100%)
- **Performance**: Full suite <5s runtime
- **Coverage**: >90% line coverage for core modules
- **Maintenance**: Zero failures in post-push for 30 days

## Risks & Mitigations

### Risk 1: Blender Installation Issues
- **Mitigation**: Use mock Blender API for CI environments
- **Fallback**: Mark Blender tests as `@pytest.mark.skipif` if not available

### Risk 2: External Dependencies (freetype, torch)
- **Mitigation**: Pin versions in requirements.txt
- **Fallback**: Use Docker for reproducible environments

### Risk 3: Import Path Conflicts
- **Mitigation**: Standardize path resolution in conftest.py
- **Fallback**: Relative imports for module-specific tests

## Timeline & Milestones

| Week | Phase | Milestone | Target Pass Rate |
|------|-------|-----------|------------------|
| Week 1 | Phase 1: Critical Fixes | Blender + Service tests fixed | 88% (239/272) |
| Week 1 | Phase 1: Validation | Validation scripts fixed | 88% complete |
| Week 2 | Phase 2: Optimization | Full suite refactoring | 95% (258/272) |
| Week 2 | Phase 2: Verification | 100% pass rate achieved | 100% (272/272) |

**Total Duration**: 2 weeks
**Weekly Check-ins**: Run full suite every Friday

## Next Actions
1. **Immediate**: Install Blender and freetype dependencies
2. **Day 1**: Run `pytest tests/ -v -k "blender"` and fix top 5 failures
3. **Ongoing**: Track progress in this plan (update pass rate weekly)
4. **Completion**: Merge fixes and update post-push hook documentation

---

**Status**: Active  
**Priority**: High  
**Owner**: Development Team  
**Last Updated**: October 5, 2025  
**Current Pass Rate**: 82% → Target: 100%
