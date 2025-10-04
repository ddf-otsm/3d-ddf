# Export Files Rename Guide

## Current Violations

The following files need to be renamed to follow the taxonomy convention:

```
{project}_{version}_{date}_{quality}_{type}.mp4
```

## Files to Rename

### 1. dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4

**Current**: `dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4`

**Issues**:
- Missing date (YYYYMMDD)
- Missing quality (resolution)
- Invalid format (all caps, no standard components)

**Suggested rename** (based on Oct 1, 2025 creation, 1080p):
```bash
mv dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4 \
   dadosfera_stable_20251001_1080p_photorealistic.mp4
```

**Reasoning**:
- `stable` - This is the production-ready version
- `20251001` - Created October 1, 2025
- `1080p` - Full HD 1920×1080 resolution
- `photorealistic` - Cycles render with photorealistic quality

---

### 2. dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4

**Current**: `dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4`

**Issues**:
- Invalid version component (`CYCLES` not in allowed list)
- Invalid quality component (`1409` looks like a time, not resolution)
- Inconsistent format (mixed uppercase)

**Suggested rename** (assuming 1080p, alpha version):
```bash
mv dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4 \
   dadosfera_alpha_20251001_1080p_cycles.mp4
```

**Alternative** (if this is a stable version):
```bash
mv dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4 \
   dadosfera_stable_20251001_1080p_cycles.mp4
```

**Reasoning**:
- `alpha` or `stable` - Determine based on release status
- `20251001` - Date from original filename
- `1080p` - Typical Full HD resolution (verify in file metadata)
- `cycles` - Indicates Cycles render engine

---

## Rename Script

Run all renames at once:

```bash
#!/bin/bash
cd ${PROJECT_ROOT}/projects/dadosfera/exports  # e.g., ~/local_repos/3d-ddf/projects/dadosfera/exports

# Rename file 1
mv "dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4" \
   "dadosfera_stable_20251001_1080p_photorealistic.mp4"

# Rename file 2
mv "dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4" \
   "dadosfera_alpha_20251001_1080p_cycles.mp4"

echo "✅ Files renamed successfully!"
```

## After Renaming

1. **Update documentation references**:
   - Check `README.md` in this directory
   - Update any references in `docs/`
   - Update project documentation

2. **Validate taxonomy**:
   ```bash
   python3 scripts/validate_taxonomy.py
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "fix: rename export files to follow taxonomy convention"
   ```

## Naming Convention Reference

### Format
```
{project}_{version}_{date}_{quality}_{type}.mp4
```

### Valid Components

**Version**:
- `alpha` - Alpha release
- `beta` - Beta release  
- `rc` - Release candidate
- `stable` - Stable/production release
- `deprecated` - Old versions

**Quality**:
- `270p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `4k`

**Type** (examples):
- `final` - Final production render
- `preview` - Preview quality
- `test` - Test render
- `photorealistic` - Photorealistic render
- `cycles` - Cycles engine render
- `eevee` - EEVEE engine render

### Examples of Good Names

```
dadosfera_alpha_20251002_1080p_final.mp4
dadosfera_beta_20251015_720p_preview.mp4
dadosfera_stable_20251101_4k_photorealistic.mp4
dadosfera_rc_20251020_1080p_cycles.mp4
```

## Questions?

- See: `docs/project/taxonomy-rules.md` for complete rules
- Run: `python3 scripts/validate_taxonomy.py` to check compliance
- Contact: Project maintainer for clarifications

---

**Created**: October 2, 2025  
**Status**: Pending rename
