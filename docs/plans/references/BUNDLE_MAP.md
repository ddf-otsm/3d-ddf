# Consolidated Plan Bundles (Bundle Map)

> Purpose: Show which original plans were clustered into each consolidated plan, with owners and cross-bundle dependencies. This map is read-only metadata for navigation and audits.

## Bundle: execution_and_operations
- consolidated_doc: `docs/plans/active/EXECUTION_AND_OPERATIONS_CONSOLIDATED.md`
- includes:
  - `docs/plans/references/CONVERSATION_ACTIONS_2025-10-03.md`
  - `docs/plans/references/EXECUTION_SUMMARY_2025-10-03.md`
  - `docs/plans/references/RENDER_STATUS.md`
  - `docs/plans/references/PROGRESS_AND_RESOURCING.md`
  - `docs/plans/references/PATH_MIGRATION_PLAN.md`
- owners: Core Maintainers
- cross-bundle deps:
  - `quality_and_validation` (testing/validation gates)
  - `explosion_development` (feature execution status)

## Bundle: quality_and_validation
- consolidated_doc: `docs/plans/active/QUALITY_AND_VALIDATION_CONSOLIDATED.md`
- includes:
  - `fix-failing-tests-100-percent-plan.md` (consolidated)
  - `VALIDATION_REMEDIATION_PLAN.completed` (consolidated)
  - `pending-tasks-consolidation-plan.md` (consolidated)
- owners: Core Maintainers
- cross-bundle deps:
  - `execution_and_operations` (status rollups)
  - `explosion_development` (validation work)

## Bundle: explosion_development
- consolidated_doc: `docs/plans/active/explosion-development-roadmap.md`
- includes:
  - `explosion-realism-improvements.md` (consolidated)
  - `explosion-content-consolidation.md` (consolidated)
- owners: VFX Team
- cross-bundle deps:
  - `quality_and_validation` (validation harness)
  - `execution_and_operations` (render queue/status)

## Bundle: logo_to_3d_service
- consolidated_doc: `docs/plans/active/logo-to-3d-service.md`
- includes: (single-source plan)
- owners: 3D Service Team
- cross-bundle deps:
  - `quality_and_validation` (tests)
  - `execution_and_operations` (API execution status)

## Bundle: jenkins_automation (reference)
- consolidated_doc: `docs/plans/references/JENKINS_AUTOMATION_CONSOLIDATED.md`
- includes:
  - `JENKINS_LOCAL_AUTOMATION_PLAN.md` (consolidated)
  - `JENKINS_DOCKER_COMPOSE_SETUP.md` (consolidated)
- owners: DevOps
- cross-bundle deps: none (reference)

## Bundle: taxonomy (reference)
- consolidated_doc: `docs/plans/references/TAXONOMY_CONSOLIDATED.md`
- includes:
  - `COMPLETE_TAXONOMY_STANDARDIZATION.md` (consolidated)
  - `TAXONOMY_MIGRATION_COMPLETE.md` (consolidated)
  - `TAXONOMY_AND_OPTIMIZATION_IMPROVEMENTS.md` (consolidated)
- owners: Documentation & Tooling
- cross-bundle deps: none (reference)

## Bundle: modernization (reference)
- consolidated_doc: `docs/plans/references/MODERNIZATION_REPORT.md`
- includes: (single-source reference)
- owners: Platform/Backend
- cross-bundle deps: none (reference)

## Bundle: dependency_map (reference)
- consolidated_doc: `docs/plans/references/DEPENDENCY_MAP.md`
- includes: (single-source reference)
- owners: Core Maintainers
- cross-bundle deps: all (navigational)
