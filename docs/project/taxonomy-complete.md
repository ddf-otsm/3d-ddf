# Complete Taxonomy Validation System ✅

## Summary

Successfully created a comprehensive taxonomy validation system that enforces:
1. ✅ **Documentation structure** (docs/ organization)
2. ✅ **Export file naming conventions** (standardized format)
3. ✅ **Project structure consistency**

## What the Hook Catches

### ✅ Documentation Violations

**Example violations blocked**:
- Root-level `.md` files (except README.md, QUICKSTART.md, LICENSE.md, CONTRIBUTING.md)
- `documentation/` folder (duplicating `docs/`)
- Orphaned markdown files in wrong locations

### ✅ Export Naming Violations (NEW!)

**Currently detected violations**:

1. ❌ `dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4`
   - Missing: date, quality
   - Invalid format
   
2. ❌ `dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4`
   - Invalid version: `CYCLES`
   - Invalid quality: `1409`

## Validation Status

```bash
$ python3 scripts/validate_taxonomy.py

======================================================================
📋 Project Taxonomy Validation
======================================================================

✅ Found 15 documentation files in docs/

🎬 Export Naming Issues:
----------------------------------------------------------------------
❌ 2 export files violate naming convention

======================================================================
❌ Validation FAILED (export naming issues)
======================================================================
```

## Required Export Format

```
{project}_{version}_{date}_{quality}_{type}.mp4
```

**Example**: `dadosfera_stable_20251001_1080p_photorealistic.mp4`

### Valid Components

- **version**: `alpha`, `beta`, `rc`, `stable`, `deprecated`
- **date**: `YYYYMMDD` (e.g., `20251002`)
- **quality**: `270p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `4k`
- **type**: `final`, `preview`, `test`, `photorealistic`, `cycles`, etc.

## Fixing the Violations

### Option 1: Rename Files Manually

See detailed guide: `projects/dadosfera/exports/RENAME_GUIDE.md`

**Quick fix**:
```bash
cd projects/dadosfera/exports

# File 1
mv dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4 \
   dadosfera_stable_20251001_1080p_photorealistic.mp4

# File 2  
mv dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4 \
   dadosfera_alpha_20251001_1080p_cycles.mp4
```

### Option 2: Keep Current Names (Not Recommended)

Add to exceptions in `scripts/validate_taxonomy.py`:

```python
EXPORT_EXCEPTIONS = {
    "README.md",
    ".rename_mapping.txt",
    "dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4",  # Add here
}
```

⚠️ **Not recommended** - breaks taxonomy consistency!

## How the System Works

### 1. Validation Script

**Location**: `scripts/validate_taxonomy.py`

**Checks**:
- Documentation structure in `docs/`
- Export file naming in `projects/*/exports/`
- Project structure consistency

**Usage**:
```bash
python3 scripts/validate_taxonomy.py
```

### 2. Pre-commit Hook

**Location**: `.git/hooks/pre-commit` (installed)

**Behavior**:
- Runs automatically before each commit
- Blocks commit if violations found
- Provides clear error messages with fix suggestions

**Bypass** (emergency only):
```bash
git commit --no-verify
```

### 3. Installation

Already installed! To reinstall or install on other machines:

```bash
./scripts/hooks/install.sh
```

## Documentation

Complete documentation available:

1. **[Taxonomy Rules](taxonomy-rules.md)** - Complete reference
2. **[Rename Guide](../../projects/dadosfera/exports/RENAME_GUIDE.md)** - Fix export files
3. **[Hook README](../../scripts/hooks/README.md)** - Hook installation & usage
4. **[Docs Index](../README.md)** - Documentation navigation

## Benefits

### Before
- ❌ Documentation scattered across `docs/` and `documentation/`
- ❌ Export files with inconsistent naming
- ❌ No automated validation
- ❌ Manual checking required

### After
- ✅ Single source of truth: `docs/`
- ✅ Standardized export naming
- ✅ Automated pre-commit validation
- ✅ Clear error messages with fix suggestions
- ✅ Self-documenting file structure

## Testing the Hook

### Test 1: Try to commit with violations

The hook will block the commit and show:

```
🔍 Validating project taxonomy (docs + exports)...

❌ projects/dadosfera/exports/badname.mp4
   Export file does not follow naming convention
   
⚠️  Commit blocked: Project taxonomy validation failed
```

### Test 2: After fixing violations

```bash
# Fix the violations
mv badname.mp4 goodname_alpha_20251002_1080p_final.mp4

# Commit will succeed
git commit -m "fix: rename export files"

🔍 Validating project taxonomy (docs + exports)...
✅ Validation PASSED - All taxonomy rules followed!
```

## Next Steps

1. **Review violations**: Check `projects/dadosfera/exports/RENAME_GUIDE.md`

2. **Rename files**:
   ```bash
   cd projects/dadosfera/exports
   # Follow RENAME_GUIDE.md instructions
   ```

3. **Validate**:
   ```bash
   python3 scripts/validate_taxonomy.py
   ```

4. **Commit** (when validation passes):
   ```bash
   git add -A
   git commit -m "fix: rename export files to follow taxonomy convention"
   ```

## Files Created/Modified

### New Files
- ✅ `scripts/validate_taxonomy.py` - Comprehensive validator
- ✅ `docs/project/taxonomy-rules.md` - Complete rules documentation
- ✅ `projects/dadosfera/exports/RENAME_GUIDE.md` - Specific rename instructions
- ✅ `docs/project/summary.md` - Reorganization summary

### Modified Files
- ✅ `scripts/hooks/pre-commit` - Updated to use comprehensive validator
- ✅ `docs/README.md` - Added taxonomy rules link
- ✅ `.git/hooks/pre-commit` - Re-installed with new validator

### Files Moved
- ✅ 7 root-level docs → `docs/project/`
- ✅ `documentation/PROJECT_SUMMARY.md` → `docs/project/overview.md`

## Validation Commands

```bash
# Full taxonomy validation (docs + exports)
python3 scripts/validate_taxonomy.py

# Documentation only (legacy)
python3 scripts/validate_docs.py

# Manual pre-commit test
.git/hooks/pre-commit
```

## Support

- **Rules**: See `docs/project/taxonomy-rules.md`
- **Rename Help**: See `projects/dadosfera/exports/RENAME_GUIDE.md`
- **Hook Help**: See `scripts/hooks/README.md`
- **Questions**: Contact project maintainer

---

**Completed**: October 2, 2025  
**Status**: ✅ Hook installed and active  
**Violations Found**: 2 export files (fixable)  
**Action Required**: Rename export files or add exceptions
