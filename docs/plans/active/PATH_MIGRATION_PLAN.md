# Path Migration Plan

## Hardcoded Path Issues Found
1. `/Users/luismartins/local_repos/3d-ddf` → `${PROJECT_ROOT}` or script-relative root
2. `/Applications/Blender.app/Contents/MacOS/Blender` → `${BLENDER}` env with sensible default
3. Scripts saving into absolute project paths → use `PROJECT_ROOT` + relative subpaths

## Migration Strategy
- Phase 1: Environment variable implementation (completed in core scripts)
- Phase 2: Documentation for env vars and usage in workflows
- Phase 3: Cross-platform testing (macOS/Linux; Windows via WSL)
- Phase 4: Remove remaining hardcoded examples in docs; use dynamic snippets

## Implementation Details
- `scripts/render_service.py`: derives project root from `PROJECT_ROOT` or script location
- `workflows/run.sh`: `BLENDER` can be overridden via env; default macOS path remains
- `scripts/monitor_render.sh`, `scripts/encode_frames_to_video.sh`: use `${PROJECT_ROOT}` resolution
- `scripts/explosions/integrate_with_main_project.py`: saves `.blend` using dynamic root

## Cross-Platform Notes
- Use `${HOME}`, `${USER}`, `${PWD}` where applicable
- Avoid spaces in paths for Blender command line invocations
- Prefer forward slashes and quote paths in shell scripts

## Next Steps
- Audit remaining docs with hardcoded paths and update examples
- Add `.env.example` illustrating `PROJECT_ROOT`, `BLENDER`, `BLENDER_EXECUTABLE`
- Add CI check to flag hardcoded `/Users/` paths in PRs

## Dependencies
- Depends on: `docs/plans/active/MODERNIZATION_REPORT.md`
- Required by: `docs/plans/active/README.md`
