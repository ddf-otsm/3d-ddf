# Active Plans - Agent Guide

## Content Summary
- Execution summaries for active plans
- Progress and status reports for specific dates (e.g., `OCT_7_2025`)

## File Naming Convention
- Allowed (per date):
  - `ACTIVE_PLANS_EXECUTION_SUMMARY_<DATE>.md`
  - `ACTIVE_PLANS_EXECUTION_SUMMARY_<DATE>_FINAL.md`
- Not allowed:
  - Any filename with repeated `_FINAL` segments (e.g., `_FINAL_FINAL`, `_FINAL_FINAL_FINAL`, ...)
  - More than one base or more than one single-final variant for the same `<DATE>`

## Purpose
Keep only one canonical summary per date (base) and optionally a single `FINAL` version. Prevent filename inflation and duplication.

## Common Operations
```bash
# List active execution summaries
ls -1 ACTIVE_PLANS_EXECUTION_SUMMARY_*.md | sort

# Show duplicates by base key
ls -1 ACTIVE_PLANS_EXECUTION_SUMMARY_*.md | \
  sed -E 's/_FINAL(\.md)$/.md/' | sort | uniq -c | sort -nr

# Validate (CI/local)
python3 scripts/validate_active_summaries.py

# Cleanup (dry-run)
python3 scripts/cleanup_active_summaries.py

# Cleanup (apply fixes)
python3 scripts/cleanup_active_summaries.py --fix
```

## Dependencies
- `scripts/validate_active_summaries.py` (validation)
- `scripts/cleanup_active_summaries.py` (canonicalization)
- Pre-push hook (`.githooks/pre-push`) runs validation automatically after `./install-hooks.sh`


