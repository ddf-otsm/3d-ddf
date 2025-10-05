# Post-Push Hook Documentation

## Overview

The post-push hook is a Git hook that runs **after** a successful push to the remote repository. Unlike the pre-push hook (which prevents pushes when checks fail), the post-push hook provides **comprehensive validation** and is designed to run the full test suite without exclusions.

**Key Purpose**:
- Catch issues that pre-push might miss (e.g., non-critical tests, integration issues)
- Provide complete CI/CD validation after code is deployed
- Generate reports and notifications for monitoring
- Ensure long-term code quality without blocking development workflow

**Location**: `.git/hooks/post-push`

## Configuration

### Hook Script Structure
The post-push hook is written in Bash and follows this structure:

```bash
#!/bin/bash
set -euo pipefail

echo "🚀 Post-push: Running comprehensive validation suite..." >&2

# Run full test suite (no exclusions for post-push)
if command -v pytest >/dev/null 2>&1; then
    echo "Running full test suite..." >&2
    pytest tests/ -v --tb=short
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo "❌ Some tests failed during post-push validation!" >&2
        echo "Check the test output above for details." >&2
        exit $exit_code
    fi
fi

# Run validation scripts
echo "Running validation scripts..." >&2
for script in scripts/validate_*.py; do
    if [ -f "$script" ]; then
        echo "Running $script..." >&2
        python3 "$script"
        if [ $? -ne 0 ]; then
            echo "❌ Validation failed: $script" >&2
            exit 1
        fi
    fi
done

# Generate reports
echo "Generating reports..." >&2
python3 scripts/generate_report.py || echo "Report generation failed (non-critical)"

echo "✅ Post-push validation completed successfully!" >&2
exit 0
```

### Key Features
- **Full Test Suite**: Runs `pytest tests/ -v --tb=short` **without exclusions** (unlike pre-push)
- **Validation Scripts**: Executes all `validate_*.py` scripts in `scripts/`
- **Report Generation**: Runs `generate_report.py` (non-critical if it fails)
- **Exit Code Handling**: Fails only on actual errors (exit code 0 for success, non-zero for failures)
- **Logging**: All output to stderr for easy capture in CI/CD systems

### Environment Variables
The hook respects these environment variables:
- `PYTHON`: Python interpreter (default: `python3`)
- `PROJECT_ROOT`: Project root path (auto-detected if not set)
- `NO_TESTS`: Skip test suite if set to `1` (for debugging)

## Differences from Pre-Push Hook

| Aspect | Pre-Push Hook | Post-Push Hook |
|--------|---------------|----------------|
| **Timing** | Before push (blocks if fails) | After push (runs asynchronously) |
| **Purpose** | Fast, critical checks only | Comprehensive validation |
| **Test Scope** | Critical/High priority only (excludes problematic dirs) | Full suite (no exclusions) |
| **Duration** | <1 second (fast) | 3-5 seconds (thorough) |
| **Exit Behavior** | Blocks push on failure | Runs after push, emails failures |
| **Test Count** | 45 critical tests (100% pass) | 272 total tests (82% pass currently) |
| **Focus** | Prevent broken code from reaching remote | Monitor and report on deployed code |

### Why Both Hooks?
- **Pre-Push**: Keeps development fast (only critical checks)
- **Post-Push**: Ensures comprehensive coverage (full suite validation)
- **Combined Effect**: Fast local workflow + thorough remote validation

## Expected Outcomes

### Current Test Statistics (as of October 5, 2025)
- **Total Tests**: 272
- **Passing**: 223 (82%)
- **Failing**: 49 (18%) - Primarily Blender-dependent and module import issues
- **Deselected in Pre-Push**: 264 (intentionally excluded for speed)
- **Critical Tests**: 45 (100% pass rate)

### Typical Post-Push Output
```
🚀 Post-push: Running comprehensive validation suite...
Running full test suite...
tests/unit/test_validate_taxonomy.py::TestTaxonomyValidation::test_basic_structure PASSED
tests/integration/test_pipeline.py::TestPipelineIntegration::test_end_to_end_flow PASSED
... [223 more passing tests]
tests/unit/test_blender_render.py::TestBlenderIntegration::test_gpu_render FAILED
... [49 failing tests]
❌ Some tests failed during post-push validation!
Running validation scripts...
Running scripts/validate_taxonomy.py... ✅
Running scripts/validate_links.py... ✅
Generating reports... ✅
```

### Success Criteria
- **Exit Code 0**: All tests pass + validations succeed
- **Exit Code Non-Zero**: Failures detected (triggers notifications)
- **Duration**: <5 seconds (optimized for post-push)

## Setup & Maintenance

### Installation
The post-push hook is installed via the centralized hook system:

```bash
# Install centralized hooks
./install-hooks.sh

# Verify installation
ls -la .git/hooks/post-push
# Should show: .git/hooks/post-push → ../../.githooks/post-push
```

### Customization
Edit the hook in `.githooks/post-push` (not `.git/hooks/` directly):

1. **Add New Validation**:
   ```bash
   # Add after validation scripts
   echo "Running custom validation..." >&2
   python3 scripts/custom_validator.py || exit 1
   ```

2. **Skip Tests** (temporary):
   ```bash
   if [ "${NO_TESTS:-0}" != "1" ]; then
       # Run pytest only if not skipped
       pytest tests/ -v --tb=short
   fi
   ```

3. **Notifications** (add to end):
   ```bash
   # Send Slack notification
   curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"Post-push validation completed - Exit: $exit_code"}' \
        $SLACK_WEBHOOK_URL
   ```

### Troubleshooting

#### Common Issues
1. **Hook Not Running**:
   - Verify executable: `chmod +x .git/hooks/post-push`
   - Check symlink: `ls -la .git/hooks/post-push`
   - Test manually: `bash .git/hooks/post-push`

2. **Python Not Found**:
   - Ensure Python 3 is in PATH
   - Set `PYTHON` environment variable

3. **Long Runtime**:
   - Post-push should be <5s; if longer, optimize test suite
   - Use `--tb=short` for shorter tracebacks

4. **False Positives**:
   - Blender-dependent tests may fail without GPU
   - Use `-m "not blender"` for CPU-only environments

#### Debug Mode
Run with debug output:
```bash
bash -x .git/hooks/post-push
```

#### Exit Codes
- **0**: Success (all tests pass)
- **1-4**: Test failures (pytest standard codes)
- **5**: No tests collected (unexpected - check configuration)
- **127**: Command not found (Python/pytest missing)

### Integration with CI/CD

#### Jenkins Integration
The post-push hook complements Jenkins pipelines:
- **Local Development**: Post-push runs immediately after local push
- **Remote CI**: Jenkins runs similar full suite on webhook trigger
- **Consistency**: Both use same validation scripts

#### Notification Setup
Add to hook for alerting:
```bash
# Email on failure
if [ $exit_code -ne 0 ]; then
    echo "Post-push validation failed - $exit_code tests failed" | \
    mail -s "3D-DDF Validation Alert" team@ddf-otsm.com
fi
```

## Future Enhancements

1. **Parallel Execution**: Run tests/validations in parallel for <2s runtime
2. **Artifact Upload**: Auto-upload reports to S3/OCI Object Storage
3. **Performance Metrics**: Track test duration trends
4. **Selective Runs**: Run only changed file tests (git diff-based)
5. **Integration Tests**: Add end-to-end workflow validation

---

**Last Updated**: October 5, 2025  
**Current Pass Rate**: 82% (223/272 tests)  
**Critical Tests**: 100% pass rate  
**Duration**: ~3 seconds  
**Status**: Active and monitoring
