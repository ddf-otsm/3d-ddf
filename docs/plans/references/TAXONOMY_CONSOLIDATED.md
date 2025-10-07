# Taxonomy and Optimization — Consolidated

> Consolidates the following documents into one source of truth (2025-10-07):
> - docs/plans/active/TAXONOMY_AND_OPTIMIZATION_IMPROVEMENTS.md
> - docs/plans/active/TAXONOMY_MIGRATION_COMPLETE.md
> - docs/plans/active/COMPLETE_TAXONOMY_STANDARDIZATION.md
>
> Status: ✅ Complete | Owner: Documentation & Tooling

---

## Executive Summary
All timestamped artifacts now follow the `YYYYMMDD_HHMM_description` convention. Validation and migration tooling exist and are enforced via pre-commit and CI.

- Render folders migrated: 22
- Export files migrated: 14
- Reports/logs/backups/folders: 26+
- Validation scripts updated and integrated into CI

---

## Standards
- Naming: `YYYYMMDD_HHMM_description`
- Applies to: render folders, export videos, reports, logs, backups, and future artifacts

---

## Tooling
- Migration Scripts:
  - `scripts/migrate_render_folder_names.py`
  - `scripts/migrate_export_file_names.py`
  - `scripts/migrate_all_timestamps.py`
- Validators:
  - `scripts/validate_taxonomy.py` (render folders + export files)
  - Pre-commit hook + CI integration

---

## Results and Verification
- 100% compliance across verified categories
- Chronological sorting, automation-friendly filenames
- Metal GPU optimization confirmed for render pipeline (context from optimization doc)

---

## Operational Guidance
- Always generate timestamp-first names in scripts
- Use `${PROJECT_ROOT}` and `${BLENDER}` env vars in docs/scripts
- Run validators locally before commits

### Commands
```bash
python3 scripts/validate_taxonomy.py
python3 scripts/migrate_render_folder_names.py --path . --execute
python3 scripts/migrate_export_file_names.py --path . --execute
```

---

## Acceptance Criteria (Met)
- All render folders and export files compliant
- Validator enforces rules in CI and hooks
- Documentation updated; examples reflect standard

---

## References
- `docs/guides/rendering-guide.md` (path portability examples)
- `projects/explosion-test/VALIDATION_CHECKLIST.md`
- `docs/plans/active/README.md` (plan management)
