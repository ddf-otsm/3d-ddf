# Validation Remediation Plan (Active)

## Status
- **Lifecycle**: ACTIVE
- **Owner**: DevOps & Documentation Engineering
- **Stakeholders**: CI/CD, QA, 3D-DDF Engineering
- **Created**: 2025-10-05

## Context (from latest local validations)
- **Broken links**: 94
- **JSON reference issues**: 1
- **Hardcoded paths**: 32 files
- Source of results: local runs of `scripts/validate_links.py`, `scripts/validate_json.py`, `scripts/validate_paths.py` on 2025-10-05.

## Objectives
1. Reduce broken links to 0 and keep them at 0 via CI validation.
2. Resolve the single JSON reference issue by updating the reference or restoring the missing asset as appropriate.
3. Eliminate hardcoded paths by replacing with portable variables, documented examples, or neutral placeholders.

---

## Work Item A: Fix 94 Broken Links

### Approach
- Triage link failures into categories:
  - Wrong relative paths (e.g., missing `docs/` or incorrect depth).
  - References to non-existent files/sections (remove or replace).
  - Links to directories lacking `README.md` (add minimal README.md or link to a specific file).
  - Cross-repo or external paths that should be documented rather than linked.

### Steps
1. Generate a fresh link report:
   ```bash
   python3 scripts/validate_links.py | tee logs/link_validation_latest.txt
   ```
2. Batch-fix common patterns:
   - Prefix missing `docs/` where appropriate.
   - Update outdated doc paths (e.g., moved guides or plans).
   - Add `README.md` to linked directories that represent topics.
3. Manually address remaining edge cases (deleted/moved content, re-organize or remove links).
4. Re-run validation until 0 errors.

### Acceptance Criteria
- `scripts/validate_links.py` exits successfully with 0 broken links on CI and locally.

---

## Work Item B: Fix 1 JSON Reference Issue

### Observed
- File: `projects/dadosfera/exports/metadata.json`
- Issue: References a non-existent asset: `dadosfera_stable_20251001_1080p_final.mp4`

### Resolution Options (choose one)
1. Update JSON to reference the correct, existing filename if a rename occurred.
2. Restore the missing media asset if it should exist (preferred if it is a canonical artifact).
3. If deprecated, remove the stale entry or mark it with a valid placeholder and rationale.

### Steps
1. Confirm intended asset mapping with stakeholders.
2. Apply the selected update in JSON.
3. Re-run JSON validation:
   ```bash
   python3 scripts/validate_json.py
   ```

### Acceptance Criteria
- `scripts/validate_json.py` reports 0 issues.

---

## Work Item C: Remove Hardcoded Paths (32 files)

### Patterns to Eliminate
- Absolute user paths: `/Users/<name>/...`, `/home/<name>/...`
- Application paths: `/Applications/Blender.app/...`
- Windows drive paths: `C:\\Program Files\\...`
- Repo-specific absolute roots: `/local_repos/` or similar

### Replacement Strategy
- Use environment variables and document them:
  - `PROJECT_ROOT` for repository root.
  - `BLENDER` for Blender executable path.
- In code/scripts, read from `os.environ` (Python) or `$VAR` (shell).
- In docs, present paths as examples with variables instead of machine-specific values.

### Steps
1. Create a changeset that replaces hardcoded paths with variables/placeholders.
2. Update `docs/setup/` to clearly document required env vars and example resolutions per OS.
3. Re-run path validation:
   ```bash
   python3 scripts/validate_paths.py | tee logs/path_validation_latest.txt
   ```

### Acceptance Criteria
- `scripts/validate_paths.py` reports 0 hardcoded path findings.

---

## Execution Plan
1. Create a working branch: `chore/validation-remediation-oct-2025`.
2. Execute Work Item B (JSON) first — quick win and unblocks downstream checks.
3. Execute Work Item A (links): batch fixes + targeted manual edits.
4. Execute Work Item C (paths): variable substitution and documentation updates.
5. Re-run full validation suite:
   ```bash
   python3 scripts/validate_taxonomy.py && \
   python3 scripts/validate_links.py && \
   python3 scripts/validate_json.py && \
   python3 scripts/validate_file_sizes.py && \
   python3 scripts/validate_paths.py
   ```
6. Commit with high-signal messages and open PR; run local Jenkins pipeline.

## Milestones
- M1: JSON reference fixed and passing.
- M2: Broken links reduced to < 10.
- M3: Broken links at 0.
- M4: Hardcoded paths at 0.
- M5: All validators pass in local Jenkins.

## Risks & Mitigations
- Large number of link fixes may miss context: review diffs by section owners.
- Directory links: adding `README.md` stubs may need follow-up content.
- Path substitutions could confuse users: ensure clear env var docs and examples.

## Success Criteria
- All five validators pass locally and in Jenkins.
- No regressions introduced in documentation navigation.
- Path guidance is portable across macOS, Linux, and Windows.
