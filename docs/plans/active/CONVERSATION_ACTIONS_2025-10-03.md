# Active Plan - Conversation Actions (2025-10-03)

## Context
- Repo: `3d-ddf`
- Branch: `master`
- State: Working tree clean; pre-commit taxonomy validation passing; remote in sync

## Completed
- Virtual environment tooling
  - Added `requirements.txt`, `setup_venv.sh`, and `docs/setup/VENV_SETUP.md`
  - Updated `README.md` and `QUICKSTART.md` with venv workflow
- Composer/IDE hygiene
  - Created `.cursorignore` to exclude binary assets from AI context
- Taxonomy validation
  - Enhanced `scripts/validate_taxonomy.py` to ignore venv paths and allow `AGENTS.md`
  - Added exceptions and fixed export naming issues; added `.pre-commit-config.yaml`
- Submodule conversion and update workflow
  - Converted `blender-mcp` from submodule to a tracked directory
  - Removed `.gitmodules` and nested `.git`; cleaned caches and environment artifacts
  - Documented manual upstream comparison in `docs/setup/BLENDER_MCP_UPDATE.md`
- Render workflow improvements
  - `scripts/render_service.py`: prefixed frame directories with `frames_`; dynamic export dir (dadosfera vs explosion-test); included project name in video filenames
  - Portability: removed hardcoded `/Users/luismartins` path by resolving `PROJECT_ROOT` dynamically (env var or script-relative)
  - `workflows/run.sh`: status shows recent renders and exported videos for dadosfera and explosion-test
  - Portability: `BLENDER` path can be overridden via env; defaults to macOS install path
  - `scripts/monitor_render.sh` and `scripts/encode_frames_to_video.sh`: replaced hardcoded paths with dynamic project root
  - Added `docs/project/enhancement-results.md`
- Repository housekeeping
  - Resolved export naming warnings; taxonomy validation now passes
  - Cleaned unintended/untracked files and directories; working tree restored to a clean state
  - Commits pushed to remote (`6094290`, `74f166b`, and cleanup revert `6d78963`)

## Pending
- Execution of `render_service.py` outside Blender fails (expected): `ModuleNotFoundError: No module named 'bpy'`
  - This is by design; `bpy` is only available inside Blender's Python runtime

## Next Tasks
- Run Blender-based validations
  - Use Blender CLI to execute scripts:
    ```bash
    ${BLENDER}/Contents/MacOS/Blender \
      --background \
      --python scripts/render_service.py -- \
      --engine cycles --quality preview --materials standard \
      --camera main \
      --scene projects/dadosfera/blender_files/dadosfera_animation_v1.blend \
      --frame-start 1 --frame-end 10 \
      --output-name test_render
    ```
  - Note the `--` separator before script args; required by Blender
- (Optional) CI enhancement
  - Add a Blender job (self-hosted or local) to run non-interactive smoke tests for `render_service.py`
- (Optional) Git LFS
  - Consider Git LFS for large `.blend`/`.mp4` assets if they need to live in the repo

## Verification Checklist
- Pre-commit hook runs `scripts/validate_taxonomy.py` and passes
- `docs/setup/VENV_SETUP.md` steps succeed on a fresh clone
- `docs/setup/BLENDER_MCP_UPDATE.md` process validated with a dry-run diff
- Render artifacts land in:
  - `projects/dadosfera/renders/frames_*` and exports in `projects/dadosfera/exports`
  - For explosion previews, exports route to `projects/explosion-test/exports`

## Notes & Risks
- IDE warnings (TrustedTypes, extension API proposals) are environment-specific and not part of repo code
- `bpy` availability requires executing via Blender; do not expect local Python to import it

## Dependencies
- Depends on: `docs/plans/ACTIVE_PLANS_SUMMARY.md`
- Required by: `docs/plans/active/PROGRESS_AND_RESOURCING.md`
