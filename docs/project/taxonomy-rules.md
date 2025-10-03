# Project Taxonomy Rules

This document defines the complete taxonomy rules for the 3D-DDF project, including documentation structure and file naming conventions.

## 📚 Documentation Taxonomy

### Allowed Root-Level Files

Only these markdown files are permitted in the repository root:

- ✅ `README.md` - Project overview
- ✅ `QUICKSTART.md` - Quick setup guide
- ✅ `LICENSE.md` - License information
- ✅ `CONTRIBUTING.md` - Contribution guidelines

### Required Directory Structure

```
docs/
├── project/     # Project planning, roadmaps, history, releases
├── guides/      # User guides and tutorials
└── setup/       # Installation and troubleshooting
```

### Allowed Documentation Locations

- ✅ `docs/project/*.md` - Project planning and history
- ✅ `docs/guides/*.md` - User guides
- ✅ `docs/setup/*.md` - Installation guides
- ✅ `projects/{name}/*.md` - Project-specific documentation
- ✅ `scripts/*/README.md` - Component documentation
- ✅ `tests/README.md` - Test documentation

### Disallowed Patterns

- ❌ `documentation/` folder (use `docs/` instead)
- ❌ `doc/` folder (inconsistent naming)
- ❌ Root-level `.md` files (except allowed list)
- ❌ Orphaned markdown files in unexpected locations

## 🎬 Export File Naming Convention

All video exports must follow this standardized format:

```
{project}_{version}_{date}_{quality}_{type}.mp4
```

### Component Definitions

#### 1. `{project}`
- **Format**: Lowercase, single word
- **Example**: `dadosfera`
- **Rule**: Must match the parent directory name under `projects/`

#### 2. `{version}`
- **Format**: Lowercase, single word
- **Valid values**:
  - `alpha` - Alpha release
  - `beta` - Beta release
  - `rc` - Release candidate
  - `stable` - Stable release
  - `deprecated` - Deprecated/old versions
- **Example**: `alpha`

#### 3. `{date}`
- **Format**: `YYYYMMDD` (8 digits)
- **Example**: `20251002`
- **Rule**: Must be a valid date

#### 4. `{quality}`
- **Format**: Resolution with 'p' suffix
- **Valid values**:
  - `270p` - 480×270 (ultra-low, testing)
  - `360p` - 640×360 (low, previews)
  - `480p` - 854×480 (SD)
  - `720p` - 1280×720 (HD)
  - `1080p` - 1920×1080 (Full HD)
  - `1440p` - 2560×1440 (2K)
  - `4k` - 3840×2160 (4K UHD)
- **Example**: `1080p`

#### 5. `{type}`
- **Format**: Lowercase, alphanumeric with underscores
- **Common values**:
  - `final` - Final production render
  - `partial` - Incomplete render
  - `test` - Test render
  - `preview` - Preview quality
  - `viewport` - Viewport capture
- **Example**: `final`

### Complete Examples

✅ **Good**:
```
dadosfera_alpha_20251002_1080p_final.mp4
dadosfera_beta_20251015_720p_preview.mp4
dadosfera_stable_20251101_4k_final.mp4
dadosfera_deprecated_20250930_360p_test.mp4
```

❌ **Bad**:
```
dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4
  - Missing: date, quality
  - Invalid: uppercase components

dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4
  - Invalid: 'CYCLES' not a valid version
  - Invalid: '1409' not a valid quality
  - Format: timestamp should be date only (YYYYMMDD)
```

### Migration Guide

To fix non-compliant filenames:

1. Identify the render properties:
   - What version is this? (alpha, beta, stable)
   - What date was it created?
   - What resolution?
   - What type/purpose?

2. Rename following the pattern:

```bash
# Example fix for CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL
# This is a stable, photorealistic, 1080p final render from Oct 1

mv dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4 \
   dadosfera_stable_20251001_1080p_photorealistic.mp4

# Example fix for CYCLES_PHOTOREALISTIC with timestamp
mv dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4 \
   dadosfera_stable_20251001_1080p_cycles.mp4
```

3. Update references in documentation

## 🔍 Validation

### Automatic Validation

The pre-commit hook automatically validates all taxonomy rules:

```bash
# Runs automatically on: git commit
🔍 Validating project taxonomy (docs + exports)...
```

### Manual Validation

Run anytime without committing:

```bash
python3 scripts/validate_taxonomy.py
```

**Output Example**:
```
======================================================================
📋 Project Taxonomy Validation
======================================================================

✅ Found 14 documentation files in docs/

🎬 Export Naming Issues:
----------------------------------------------------------------------
❌ projects/dadosfera/exports/file.mp4
   Export file does not follow naming convention
   💡 Fix: Rename to: dadosfera_<version>_<YYYYMMDD>_<quality>_<type>.mp4

======================================================================
```

### Bypass Validation

Only for emergency commits:

```bash
git commit --no-verify -m "Emergency fix"
```

**⚠️ Warning**: Bypassing validation can introduce taxonomy violations!

## 📊 Benefits of Taxonomy Rules

1. **Consistency** - All files follow predictable patterns
2. **Discoverability** - Easy to find and understand files
3. **Automation** - Scripts can parse filenames reliably
4. **Documentation** - Self-documenting file structure
5. **Version Control** - Clear history through naming
6. **Quality Control** - Automated validation prevents errors

## 🔄 Updating Rules

To modify taxonomy rules:

1. Edit validation script: `scripts/validate_taxonomy.py`
2. Update this documentation: `docs/project/taxonomy-rules.md`
3. Announce changes to team
4. Run validation: `python3 scripts/validate_taxonomy.py`
5. Fix any newly detected violations

## 📝 Exceptions

### Documentation Exceptions
- `README.md` files are allowed in any directory (component docs)
- Files in `blender-mcp/` (submodule) are excluded from validation

### Export Exceptions
- `README.md` - Documentation about exports
- `.rename_mapping.txt` - Rename history tracking

To add new exceptions, edit the relevant section in:
- `scripts/validate_taxonomy.py`

---

**Last Updated**: October 2, 2025  
**Validation Script**: `scripts/validate_taxonomy.py`  
**Pre-commit Hook**: `scripts/hooks/pre-commit`
