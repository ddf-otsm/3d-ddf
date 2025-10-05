# Jenkins Local Automation Plan (Active)

## Status
- **Lifecycle**: ACTIVE
- **Owner**: DevOps & Platform Engineering
- **Stakeholders**: CI/CD, QA, 3D-DDF Engineering
- **Created**: 2025-10-05

## Objectives
1. Convert the existing Jenkins job to a Pipeline job that uses the repository `Jenkinsfile`.
2. Provide a programmatic trigger script (REST API with crumb + cookie) for local-only builds.
3. Ensure Python is available inside the Jenkins controller so real validator scripts can run within Jenkins.

---

## Work Item 1: Convert to Pipeline Job (uses repo Jenkinsfile)

### Approach
- Use Jenkins REST API to create/replace a Pipeline job that points to the Git repo and `Jenkinsfile`.
- Keep it local-only; no external webhooks.

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
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
```

### Commands (local-only)
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

### Acceptance Criteria
- Jenkins API lists `3d-ddf-validation` as a WorkflowJob.
- A build of `3d-ddf-validation` fetches the repo and follows the `Jenkinsfile`.

---

## Work Item 2: Programmatic Trigger Script (REST API, crumb + cookie)

### Script: `scripts/ci/jenkins_local_trigger.sh`
- Triggers local Jenkins jobs without UI.
- Uses cookie jar + crumb to satisfy CSRF.
- Downloads console output for the last build.

### Example
```bash
#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL=${JENKINS_URL:-http://localhost:8080}
JENKINS_USER=${JENKINS_USER:-admin}
JENKINS_PASS=${JENKINS_PASS:?set JENKINS_PASS}
JOB=${1:-3d-ddf-validation}

# Get crumb and save cookies
curl -s -c cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/crumbIssuer/api/json" > crumb.json
CRUMB=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["crumb"])' < crumb.json)
HEADER=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["crumbRequestField"])' < crumb.json)

# Trigger build
curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" -H "$HEADER: $CRUMB" -X POST \
  "$JENKINS_URL/job/$JOB/build" -o /dev/null

echo "Triggered job: $JOB"
```

### Optional: Fetch build console
```bash
# After trigger, poll for the lastBuild URL and fetch console output
curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/job/$JOB/lastBuild/consoleText" -o lastBuild.log
```

### Acceptance Criteria
- Running the script triggers a build.
- Console logs are retrievable programmatically.

---

## Work Item 3: Install Python in Jenkins Controller Image

### Option A (Recommended): Custom image
Create `docker/jenkins-controller.Dockerfile`:
```dockerfile
FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
USER jenkins
```
Update `docker/docker-compose.jenkins.yml` to use the custom image:
```yaml
services:
  deployer-jenkins-cicd:
    build:
      context: ..
      dockerfile: docker/jenkins-controller.Dockerfile
    ports:
      - "${JENKINS_PORT:-8080}:8080"
      - "${JENKINS_AGENT_PORT:-50000}:50000"
    volumes:
      - jenkins-cicd-data:/var/jenkins_home
```

### Option B: In-place (non-persistent across image changes)
```bash
# Not recommended for reproducibility; good for quick tests only
docker exec -u root deployer-jenkins-cicd bash -lc "apt-get update && apt-get install -y python3 python3-pip"
```

### Acceptance Criteria
- `python3 --version` succeeds inside the controller container.
- Jenkins can execute `python3 scripts/validate_*.py` steps during a build.

---

## Milestones
1. Pipeline job created and verified with a manual trigger.
2. Trigger script works end-to-end (build starts, console logs downloadable).
3. Jenkins controller image includes Python; validation steps run in Jenkins.

## Risks / Mitigations
- CSRF/crumb mismatch: Always fetch crumb with cookies; reuse both for subsequent POST.
- Image drift: Prefer custom image to guarantee Python presence.
- Network egress (Git clone): Ensure controller can reach GitHub.

## Success Criteria
- Local-only automation: No external webhooks/Actions used.
- End-to-end builds run from `Jenkinsfile` and produce artifacts in `reports/`.
- Programmatic automation (script) reproducibly triggers and fetches logs.
