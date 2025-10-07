# Jenkins Automation — Consolidated

> Consolidates the following documents into one source of truth (2025-10-07):
> - docs/plans/active/JENKINS_LOCAL_AUTOMATION_PLAN.md
> - docs/plans/active/JENKINS_LOCAL_AUTOMATION_PLAN.completed
> - docs/plans/active/JENKINS_DOCKER_COMPOSE_SETUP.md
>
> Status: ✅ Completed | Owner: DevOps & Platform Engineering

---

## Overview

- Local-only Jenkins automation and Docker Compose environment are fully implemented and verified.
- This document provides setup, usage, and verification steps, replacing the separate plan files.

---

## Part A: Local Automation Plan (Pipeline + Trigger)

### Status
- Lifecycle: ✅ Completed (2025-10-05)
- Deliverables: Pipeline job, local trigger script, Python in controller

### Objectives
1. Convert Jenkins job to Pipeline using repo `Jenkinsfile`.
2. Programmatic trigger script (crumb + cookie) for local-only builds.
3. Ensure Python is available in the controller image.

### Pipeline Job Config (config.xml)
```xml
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <actions/>
  <description>3D-DDF Validation Pipeline (uses Jenkinsfile in repo)</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
    <scm class="hudson.plugins.git.GitSCM" plugin="git">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>https://github.com/ddf-otsm/3d-ddf.git</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="empty-list"/>
      <extensions/>
      </extensions>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
```

### Commands (Local Only)
```bash
# 1) Get crumb and store cookies
curl -s -c cookies.txt -u admin:${JENKINS_PASS} http://localhost:8080/crumbIssuer/api/json > crumb.json
CRUMB=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["crumb"])' < crumb.json)
HEADER=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["crumbRequestField"])' < crumb.json)

# 2) Create/replace job (Pipeline)
curl -s -b cookies.txt -u admin:${JENKINS_PASS} \
  -H "${HEADER}: ${CRUMB}" \
  -H "Content-Type: application/xml" \
  --data-binary @config.xml \
  "http://localhost:8080/createItem?name=3d-ddf-validation&mode=org.jenkinsci.plugins.workflow.job.WorkflowJob"
```

### Local Trigger Script
- Script: `scripts/ci/jenkins_local_trigger.sh`
- Features: CSRF crumb + cookie, optional console log download

```bash
./scripts/ci/jenkins_local_trigger.sh  # triggers default job
./scripts/ci/jenkins_local_trigger.sh --wait  # triggers and waits for completion
```

### Python in Controller Image
- Dockerfile: `docker/jenkins-controller.Dockerfile`
```dockerfile
FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
USER jenkins
```
- Compose service: `docker/docker-compose.jenkins.yml` uses the custom image

### Acceptance Criteria
- Pipeline job builds from `Jenkinsfile`.
- Trigger script builds and retrieves logs.
- `python3 --version` works in controller container.

---

## Part B: Docker Compose Setup (Controller + Webhook)

### Status
- ✅ 100% Complete (2025-10-05)

### Services Summary
- Jenkins Controller (LTS 2.516.1) on 8080/50000
- Webhook Receiver (Flask) on 9000
- Network: `jenkins-cicd-network`; Volume: `jenkins-cicd-data`

### Compose File
- File: `docker/docker-compose.jenkins.yml`
- Key points:
```yaml
services:
  deployer-jenkins-cicd:
    # Jenkins LTS (jdk17)
    ports:
      - "${JENKINS_PORT:-8080}:8080"
      - "${JENKINS_AGENT_PORT:-50000}:50000"
    volumes:
      - jenkins-cicd-data:/var/jenkins_home

  deployer-jenkins-webhook:
    # Python Flask receiver on port 9000
    # Health checks + GitHub branch routing
```

### Verification
- Jenkins UI: `http://localhost:8080` → Healthy
- Webhook health: `http://localhost:9000/health` → `{status: healthy}`
- Compose startup, networking, volumes: ✅ Verified

### Operational Commands
```bash
# Start
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Stop
docker-compose -f docker/docker-compose.jenkins.yml down

# Logs
docker-compose -f docker/docker-compose.jenkins.yml logs -f
```

### Production Migration (Next)
- Choose deployment strategy (OCI instance vs Terraform)
- GPU agent integration, monitoring, HTTPS, secrets management

---

## Files and References
- Jenkinsfile (pipeline definition)
- `docker/jenkins-pipeline-config.xml` (job config example)
- `scripts/ci/jenkins_setup_pipeline.sh` (job setup helper)
- `scripts/ci/jenkins_local_trigger.sh` (local trigger)
- `docker/docker-compose.jenkins.yml` (environment)
- `docker/jenkins-controller.Dockerfile` (Python-enabled controller)

## Success Criteria (Met)
- Local-only automation without external webhooks
- Builds use repo `Jenkinsfile` and produce artifacts in `reports/`
- Trigger script works and fetches logs
- Python available in controller

