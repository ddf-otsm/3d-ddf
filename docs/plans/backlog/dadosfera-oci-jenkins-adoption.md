# Dadosfera OCI Jenkins Adoption Plan (Backlog)

## Status
- **Lifecycle**: Backlog / exploratory
- **Owner**: DevOps & Automation Guild
- **Stakeholders**: Platform Engineering, Render Pipeline Team, QA Automation
- **Target Window**: Evaluate once current local Jenkins upgrades are stable (ETA Q1 2026)

## Context
We currently run all CI/CD jobs on the on-prem (or local) Jenkins controller. During the branch migration audit we confirmed there are **no existing references to the Dadosfera OCI Jenkins instance**. As the organization expands, we may need a cloud-managed Jenkins (Dadosfera OCI) for elasticity, managed upgrades, and closer alignment with the broader Dadosfera tooling ecosystem.

This backlog item captures the evaluation and migration plan should we decide to adopt the Dadosfera OCI-hosted Jenkins instance in the future. No immediate action is required, but documenting the path keeps the option visible and ensures prerequisites are tracked.

## High-Level Objectives
1. **Feasibility**: Determine functional parity between local Jenkins and OCI Jenkins for Blender render jobs, Moon orchestration, and custom scripts.
2. **Security & Compliance**: Validate access controls, secrets management, network egress rules, and artifact retention policies in OCI Jenkins.
3. **Operational Efficiency**: Assess whether OCI-managed Jenkins reduces maintenance overhead compared to self-managed infrastructure.
4. **Cost & Performance**: Model projected OCI spend vs. hardware depreciation and evaluate build performance with cloud executors.
5. **Migration Safety**: Outline a zero-downtime migration approach with rollbacks and dual-running strategies if needed.

## Proposed Phases
### Phase 0 – Discovery & Requirements
- Inventory existing local Jenkins jobs, pipelines, credentials, and dependencies.
- Confirm Moon OSS integration expectations (pre- and post-push hooks) with OCI Jenkins agents.
- Document compliance and audit requirements for running in Dadosfera OCI.

### Phase 1 – Proof of Concept (PoC)
- Provision sandbox namespace on Dadosfera OCI Jenkins.
- Mirror a subset of non-critical pipelines (e.g., nightly regression renders) using shared library stubs.
- Validate runner compatibility (Dockerized, GPU/CPU requirements) and Moon CLI availability.

### Phase 2 – Integration Architecture
- Decide on credential management approach (HashiCorp Vault, OCI Secrets, etc.).
- Define network routing for Blender asset storage, artifact uploads, and metrics.
- Update shared pipeline libraries to support dual-target controllers (local vs. OCI).

### Phase 3 – Migration Plan
- Create migration runbook including:
  - Cutover criteria & maintenance windows.
  - Rollback protocol back to local Jenkins.
  - Smoke test coverage post migration.
- Update documentation, onboarding materials, and CI alarms.

### Phase 4 – Full Adoption (Conditional)
- Execute phased migration of critical pipelines.
- Enable monitoring, logging, and alerting on OCI Jenkins.
- Decommission or repurpose local Jenkins after stability window (if approved).

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| OCI Jenkins lacks required plugins or GPU agents | High | Validate in PoC; coordinate with Dadosfera infra team for plugin installation or alternative runner strategy |
| Cost overrun from OCI compute | Medium | Set cost thresholds and alerts; analyze usage patterns in PoC |
| Secrets exposure during migration | High | Require secrets rotation and adopt centralized secrets management |
| Team unfamiliarity with OCI Jenkins | Medium | Provide training sessions and update CI playbooks |

## Dependencies
- DevOps capacity to provision OCI resources.
- Dadosfera platform team approval for namespace/project.
- Updated Moon suite definitions compatible with OCI runner environment.
- Render pipeline validation datasets for soak tests.

## Decision Criteria to Exit Backlog
- Clear ROI (operational savings, scalability, or compliance) is demonstrated in discovery/PoC.
- Approved budget and security sign-off for OCI workloads.
- Stakeholder agreement on migration timeline.

## Next Actions (when prioritized)
1. Assign DevOps lead and schedule discovery workshop.
2. Request OCI Jenkins sandbox credentials from Dadosfera platform team.
3. Draft requirements checklist (plugins, runner types, networking, Moon integration).

Until these actions are triggered, this document serves as the canonical reference confirming the absence of current OCI Jenkins usage and outlining the path forward if/when adoption is prioritized.
