# Local Jenkins Controller Reference

## Overview
- **Purpose**: Primary on-premises Jenkins controller for 3d-ddf CI/CD
- **Location**: Managed locally within Dadosfera studio network
- **Install Method**: Docker Compose (preferred) or systemd-managed Jenkins service
- **Primary Use Cases**:
  - Taxonomy validation pipeline (Jenkinsfile in repo root)
  - Render workflow automation (Blender scripts, Moon orchestration)
  - Regression test orchestration via Moon CLI

## Infrastructure
| Component | Details |
|-----------|---------|
| Hostname  | `jenkins.local.ddf` (example; update with actual) |
| OS        | Ubuntu Server 22.04 LTS |
| Compute   | 8 vCPU / 16 GB RAM |
| Storage   | 250 GB SSD (Jenkins home on `/var/jenkins_home`) |
| Docker    | Docker Engine 24.x (if running in containers) |
| Access    | VPN or internal LAN only |

### Service Management
- **Docker Compose** (`/opt/jenkins/docker-compose.yml`):
  ```yaml
  version: '3.8'
  services:
    jenkins:
      image: jenkins/jenkins:lts-jdk17
      ports:
        - "8080:8080"
        - "50000:50000"
      volumes:
        - jenkins_home:/var/jenkins_home
      environment:
        - JAVA_OPTS=-Xms1g -Xmx4g
  volumes:
    jenkins_home:
  ```
- **systemd** (if not containerized):
  ```ini
  [Unit]
  Description=Jenkins Continuous Integration Server
  After=network.target

  [Service]
  Type=simple
  User=jenkins
  Group=jenkins
  ExecStart=/usr/bin/java -jar /opt/jenkins/jenkins.war
  Restart=on-failure

  [Install]
  WantedBy=multi-user.target
  ```

## Jenkins Configuration
- **Admin Access**: Stored in secure password vault (`credentials/local-jenkins-admin`)
- **Users**: LDAP/SSO integration optional; otherwise local accounts
- **Plugins**:
  - Pipeline
  - Git
  - Credentials Binding
  - Blue Ocean (optional)
  - Workspace Cleanup
  - Docker Pipeline
  - Matrix Authorization (if RBAC enabled)
  - Configuration as Code (optional)
- **Security**:
  - HTTPS termination via reverse proxy (nginx) recommended
  - Root access restricted to DevOps/Platform engineering group
  - Audit logs rotated weekly (`/var/log/jenkins/jenkins.log`)

## Pipelines & Jobs
### Core Pipeline: 3d-ddf Validation
- **Source**: Repository root `Jenkinsfile`
- **Stages**:
  1. Checkout
  2. Validate Taxonomy
  3. Check Broken Links
  4. Validate JSON
  5. Check File Sizes
  6. Check Hardcoded Paths
  7. Generate Reports
- **Triggers**: Manual and GitHub webhook (branch `main`)
- **Artifacts**: Reports archived to `reports/*.txt`

### Moon-Orchestrated Tests
- **Integration**: Moon CLI installed on controller
- **Usage**: Post-push hook triggers Moon jobs for full test suites
- **Configs**:
  - `tests/moon/suite.yaml`
  - `.moon/tasks.yml`
  - Ensure Moon API endpoint accessible from controller

### GPU/ML Pipelines (Optional)
- **Scenario**: When GPU tests are needed without OCI Jenkins
- **Setup**:
  - GPU agent configured locally (NVIDIA drivers, CUDA)
  - Jenkins node label: `gpu-local`
  - Pipelines referencing Blender/render scripts run on this node
- **Note**: For cost-efficient GPU workloads, prefer Dadosfera OCI GPU agents via deployer stack

## Integrations & Dependencies
- **GitHub**: Personal Access Token stored as Jenkins credential `github-ddf-ci`
- **Slack**: Optional notifications via `slack-webhook` credential
- **Artifacts**: Local NFS share or S3-compatible storage
- **Backups**:
  - Jenkins home snapshot nightly using `restic` (script in `/opt/jenkins/scripts/backup.sh`)
  - Configuration as Code export stored in `backups/jenkins/`

## Maintenance
- **Updates**: Check monthly for Jenkins LTS and plugin updates
- **Monitoring**: Integrate with Prometheus Node Exporter + Grafana dashboard
- **Logs**: Forward `/var/log/jenkins/jenkins.log` to centralized logging (ELK or Loki)
- **Disaster Recovery**:
  - Restore from latest `restic` snapshot
  - Rehydrate Docker volume or `/var/jenkins_home`

## Runbook (Quick Actions)
| Task | Command |
|------|---------|
| Restart Jenkins (Docker) | `docker compose restart jenkins` |
| View logs | `docker logs -f jenkins` or `journalctl -u jenkins -f` |
| List jobs | `java -jar jenkins-cli.jar -s http://jenkins.local:8080/ list-jobs` |
| Trigger build | `java -jar jenkins-cli.jar -s http://jenkins.local:8080/ build 3d-ddf-validation -f` |
| Export config | `java -jar jenkins-cli.jar -s http://jenkins.local:8080/ get-job 3d-ddf-validation > job.xml` |

## Future Enhancements
- Align configuration with deployer OCI architecture for hybrid workloads
- Automate plugin/update checks via Jenkins Configuration as Code
- Integrate Moon job status reporting directly into Jenkins build steps

---
**Last Reviewed**: 2025-10-05 (local controller active)
