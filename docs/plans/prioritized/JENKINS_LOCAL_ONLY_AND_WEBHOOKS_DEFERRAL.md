# PRIORITY: Jenkins Local-Only Operations and Webhooks Deferral

## Status
- **Lifecycle**: PRIORITIZED (execute now)
- **Owner**: DevOps & Platform Engineering
- **Stakeholders**: CI/CD, QA, 3D-DDF Engineering
- **Decision Date**: 2025-10-05

## Decision
- ✅ Immediate: Operate exclusively with the local Jenkins instance
- 🚫 Prohibited: GitHub Actions (no usage permitted)
- ⏸ Deferred: External GitHub webhooks calling Jenkins until a 24x7 bastion-jenkins on OCI is provisioned

## Rationale
- Ensure deterministic, fully local CI without cloud dependencies
- Avoid exposing local developer machines to external inbound traffic
- Align with policy: “No GitHub Actions” while keeping a path for webhook triggers in the future

## Scope
- **In-scope** (NOW):
  - Local Jenkins job execution (manual or local webhook invocation)
  - Artifact/report generation under `reports/`
  - Documentation and runbooks targeting local-only flows
- **Out-of-scope** (UNTIL BASTION EXISTS):
  - Any public or external webhook exposure
  - GitHub Actions, GitHub-hosted runners
  - Always-on cloud agents

## Execution Plan (Now)
1) Lock Process to Local Jenkins
- Use `docker/docker-compose.jenkins.yml` to run Jenkins/webhook locally
- Trigger builds manually or via localhost webhook only
- Archive artifacts via Jenkins as configured

2) Disable External Exposure
- Do not publish ports beyond localhost
- Do not configure public DNS, reverse proxies, or tunnels for local services

3) Documentation Updates
- Update references to clarify: “Local Jenkins only; GitHub Actions prohibited; external webhooks deferred”
- Point contributors to local testing commands and Jenkins usage

## Future Plan (Prereq: Bastion Jenkins on OCI - 100% Available)
To enable GitHub → Jenkins webhooks safely, provision a dedicated controller with public availability.

### Prerequisites
- OCI instance `bastion-jenkins` (always-on)
- Static public IP, firewall open for 443/8080 as needed
- TLS termination via reverse proxy (nginx) or OCI LB
- Jenkins hardened (RBAC, CSRF, credentials management)

### High-Level Steps
- Provision OCI instance (Terraform preferred)
- Install Jenkins LTS + required plugins
- Configure webhook endpoint `/github-webhook/` with secret
- Restrict inbound by IP and secret validation
- Migrate pipelines or set up multi-controller federation if needed

### Risk Controls
- CSRF enabled, crumb issuer enforced
- Webhook secret (HMAC) required
- Minimal surface exposure (only required endpoints)
- Audit logging and alerting configured

## Acceptance Criteria
- Local Jenkins: Jobs can be run and artifacts archived without any external dependency
- No external webhooks configured
- Clear, documented path to enable external webhooks once bastion is ready

## Deliverables
- This plan file (`docs/plans/prioritized/JENKINS_LOCAL_ONLY_AND_WEBHOOKS_DEFERRAL.md`)
- Updated Jenkins docs reflecting local-only mode and webhook deferral

## Notes
- If occasional remote triggers are needed pre-bastion, use secure operator-initiated methods (e.g., SSH to developer machine + local curl) rather than exposing endpoints.
