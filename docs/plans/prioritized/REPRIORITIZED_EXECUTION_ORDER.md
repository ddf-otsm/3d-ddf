# Reprioritized Execution Order (IUC + Dual Effort)

## Objective
Minimal front-end to trigger Blender render of Dadosfera with realistic explosions, via FastAPI service, and path portability.

## Scoring Key
- importance: 1-5 (5 highest)
- urgency: 1-5 (5 highest)
- complexity: 1-5 (5 hardest)
- effort.ai_hours, effort.human_hours: decimal hours

## Active Plans (Execute Immediately)
- QW_2h_HIGH_fix_path_hardcoding
  - importance: 5, urgency: 5, complexity: 1
  - effort.ai_hours: 0.8, effort.human_hours: 1.0
  - Scope: replace `/Users/luismartins` hardcodes; use `${PROJECT_ROOT}` detection and env overrides
  - Status: done for core scripts (`render_service.py`, `monitor_render.sh`, `encode_frames_to_video.sh`, `integrate_with_main_project.py`, `workflows/run.sh`)

- DEP_2h_HIGH_move_non_plans_to_references
  - importance: 5, urgency: 5, complexity: 1
  - effort.ai_hours: 0.5, effort.human_hours: 1.5
  - Move reference docs out of `docs/plans/active/` to `docs/plans/references/` and update links
  - Status: complete

- CB_4h_CRITICAL_frontend_trigger_route
  - importance: 5, urgency: 5, complexity: 2
  - effort.ai_hours: 1.0, effort.human_hours: 2.0
  - Add minimal HTML at `/` and `/api/v1/text-to-3d` PoC route to run Blender server pipeline
  - Status: initial PoC implemented

- SEC_1h_HIGH_portability_env
  - importance: 4, urgency: 4, complexity: 1
  - effort.ai_hours: 0.5, effort.human_hours: 0.5
  - Document env vars: `PROJECT_ROOT`, `BLENDER`, `BLENDER_EXECUTABLE`
  - Status: pending doc

## High Priority (Next Sprint)
- HI_8h_HIGH_text_to_3d_extrusion_pipeline
  - importance: 5, urgency: 4, complexity: 3
  - effort.ai_hours: 3.0, effort.human_hours: 5.0
  - Implement Blender ops to create text curve → mesh extrusion, material, camera, output frames/video; wire to route
  - Depends on: `services/logo-to-3d/src/core/blender_server.py`

- TD_6h_MED_render_service_api_bridge
  - importance: 4, urgency: 3, complexity: 2
  - effort.ai_hours: 2.5, effort.human_hours: 3.5
  - Bridge API route to call `scripts/render_service.py` with proper scene and arguments
  - Required by: Dadosfera video generation from name flow

- DEP_3h_HIGH_explosion_preset_integration
  - importance: 4, urgency: 4, complexity: 2
  - effort.ai_hours: 1.5, effort.human_hours: 1.5
  - Integrate `scripts/explosions/create_production_explosion.py` presets into text pipeline for realistic effects

## Standard Priority (Backlog)
- MED_2d_MED_job_queue_and_status
  - importance: 3, urgency: 3, complexity: 3
  - effort.ai_hours: 6.0, effort.human_hours: 8.0
  - Implement Redis/Celery job queue with job status endpoints and websockets

- LOW_4h_LOW_docs_cleanup_and_links
  - importance: 2, urgency: 2, complexity: 1
  - effort.ai_hours: 1.0, effort.human_hours: 3.0
  - Ensure bi-directional links and project folder parity across docs

- EXP_1d_LOW_webgl_preview
  - importance: 2, urgency: 2, complexity: 3
  - effort.ai_hours: 4.0, effort.human_hours: 4.0
  - Three.js preview for quick QA

## Interdependencies
- Depends on: `docs/plans/active/logo-to-3d-service.md`
- Required by: `projects/dadosfera/active/` (to be mirrored when project folders are updated)

## Ordered Execution List
1. QW_2h_HIGH_fix_path_hardcoding (done)
2. DEP_2h_HIGH_move_non_plans_to_references (done)
3. CB_4h_CRITICAL_frontend_trigger_route (PoC in place)
4. SEC_1h_HIGH_portability_env
5. HI_8h_HIGH_text_to_3d_extrusion_pipeline
6. TD_6h_MED_render_service_api_bridge
7. DEP_3h_HIGH_explosion_preset_integration
8. MED_2d_MED_job_queue_and_status
9. LOW_4h_LOW_docs_cleanup_and_links
10. EXP_1d_LOW_webgl_preview
