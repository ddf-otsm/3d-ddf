# Local Jenkins Controller Reference - Shared Instance Priority

## 🚨 IMPORTANT: Use Shared Local Jenkins Instance

**Recommendation**: For local development across all repositories (including 3d-ddf), use the centralized shared Jenkins LTS instance instead of the Docker-based setup below. This provides unified CI/CD with lower overhead.

### Shared Instance Details (Preferred)
- **URL**: http://localhost:17843
- **Admin Password**: See `~/vars/jenkins_admin_password_port17843.txt` (initial: `d1ec460e7187404daaa37de5f9547bce`)
- **Configuration**: Centralized in `~/vars/JENKINS_LOCAL_HANDOFF.md` and `~/vars/jenkins_config.sh`
- **Supported Projects**: budget-ddf, planner-ddf-floor-2, deployer-ddf-mod-open-llms, 3d-ddf
- **Pipeline Name for 3d-ddf**: `3d-ddf-local`
- **Setup**: Follow quick start in `~/vars/JENKINS_LOCAL_HANDOFF.md` > Quick Start for New Projects
- **Benefits**: Single maintenance, shared resources (~800MB RAM), no Docker overhead

**When to Use Docker Setup Below**:
- Testing Docker-specific pipelines
- Isolated environments for advanced debugging
- Legacy compatibility (not recommended for daily use)

---

## Overview (Docker-Based - Deprecated for Local Dev)
- **Purpose**: Development and testing environment for 3D-DDF CI/CD pipelines (use shared instance instead)
- **Architecture**: Local Docker-based Jenkins with optional webhook integration (deprecated)
- **Install Method**: Docker Compose (only for specific testing)
- **Primary Use Cases**:
  - Pipeline development and testing (Jenkinsfile validation) - prefer shared instance
  - Webhook integration testing (GitHub triggers) - update webhook to point to localhost:17843
  - Cost-effective development environment ($0/month)
  - Advanced architecture testing before production deployment

## Infrastructure (Updated for Compatibility)
| Component | Details |
|-----------|---------|
| **Container** | `deployer-jenkins-cicd` (Jenkins LTS) - **Deprecated: Use shared instance** |
| **Webhook** | `deployer-jenkins-webhook` (Python Flask) - Update to trigger shared instance |
| **Ports** | 8080 (Jenkins UI - deprecated), 50000 (agents), 9000 (webhook) - **Use 17843 for shared** |
| **Network** | `jenkins-cicd-network` (isolated) |
| **Storage** | Docker volume `jenkins-cicd-data` |
| **Access** | http://localhost:17843 (shared instance recommended) |

## Architecture Options (Updated)

### Option 1: Shared Local Instance (Recommended)
See `~/vars/JENKINS_LOCAL_HANDOFF.md` for setup. No Docker needed.

### Option 2: Local Docker (Development - Deprecated)
```bash
# Start complete Jenkins environment (only if needed for isolation)
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Services started:
# - deployer-jenkins-cicd (Jenkins controller) - **Point to shared instead**
# - deployer-jenkins-webhook (Webhook receiver) - Update env to JENKINS_URL=http://localhost:17843
# - jenkins-cicd-network (isolated network)
```

### Option 3: Production Two-Instance (Recommended)
- **Controller**: OCI bastion instance (always-on, ~$10-15/month)
- **GPU Agent**: OCI GPU instance (on-demand, ~$5-10/month)
- **Migration Path**: Shared Local → Production (documented in deployment strategy)

## Local Development Setup (Updated)

### Quick Start Commands (Shared Instance Priority)

**Preferred: Use Shared Instance**
```bash
# Source shared config
source ~/vars/jenkins_config.sh

# Verify Jenkins is running
curl -s -o /dev/null -w "HTTP %{http_code}\n" $JENKINS_URL

# Access UI
open $JENKINS_URL

# For 3d-ddf pipeline: Create '3d-ddf-local' as per handoff doc
```

**Docker Fallback (If Needed)**:
```bash
# 1. Start Docker Desktop (if not running)
open -a Docker  # macOS

# 2. Launch Jenkins locally (deprecated)
docker-compose -f docker/docker-compose.jenkins.yml up -d

# 3. Wait for Jenkins to initialize
echo "⏳ Waiting for Jenkins to start..."
sleep 60

# 4. Get initial admin password (for Docker only)
docker exec deployer-jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword

# 5. Access Jenkins UI (use shared instead)
open http://localhost:8080  # Deprecated - use http://localhost:17843
```

### Initial Configuration (Shared Instance)
1. **Enter admin password** from `~/vars/jenkins_admin_password_port17843.txt`
2. **Install suggested plugins** (Pipeline, Git, Credentials Binding, etc.)
3. **Create admin user** with secure credentials
4. **Skip instance configuration** (use default localhost:17843)

### Webhook Integration (Updated for Shared)
```bash
# Test webhook endpoint (update script to use port 17843)
curl http://localhost:9000/health  # If using Docker webhook, update env

# Trigger pipeline via webhook (point to shared Jenkins)
curl http://localhost:9000/webhook \
  -H "Content-Type: application/json" \
  -d '{"repository": {"name": "3d-ddf"}, "ref": "refs/heads/main"}'
```

## Jenkins Configuration

### Essential Plugins for Local Development
- **Pipeline** - Core pipeline functionality
- **Git** - Repository integration
- **Credentials Binding** - Secure credential management
- **Blue Ocean** - Enhanced UI (optional but recommended)
- **Workspace Cleanup** - Automated cleanup
- **Docker Pipeline** - Docker integration (if needed)

### Local Configuration Notes
- **Admin Access**: Use initial password from container, then create admin user
- **Users**: Local accounts for development (LDAP/SSO for production)
- **Security**: Development mode - no HTTPS required for local access
- **Logs**: Available via `docker logs deployer-jenkins-cicd`

### Production Configuration (Two-Instance)
- **Admin Access**: Secure credential vault integration
- **Users**: LDAP/SSO integration recommended
- **Security**:
  - HTTPS via reverse proxy (nginx)
  - Root access restricted to DevOps team
  - Audit logs forwarded to centralized logging
- **Plugins**: All development plugins + production-specific ones

## Pipelines & Jobs

### Pipeline Development Workflow

#### Local Development Testing
```bash
# 1. Create test pipeline in Jenkins UI
# 2. Configure Git repository integration
# 3. Set Script Path to: config/jenkins/Jenkinsfile.terraform
# 4. Test with different branches and triggers
```

#### Pipeline Stages (Local vs Production)

**Lightweight Stages** (Run on local Jenkins):
1. **Checkout** - Repository code checkout
2. **Validate Taxonomy** - Documentation and export validation
3. **Check Broken Links** - Internal link validation
4. **Validate JSON** - Schema and syntax validation
5. **Check File Sizes** - Large file detection
6. **Generate Reports** - HTML/PDF report generation

**GPU Stages** (Production only):
7. **GPU Tests** - Blender rendering, ML inference, CUDA validation
8. **Advanced Rendering** - Complex 3D model processing

### Webhook Integration Testing

#### Local Webhook Testing
```bash
# Test webhook receiver health
curl http://localhost:9000/health

# Simulate GitHub webhook payload
curl http://localhost:9000/webhook \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d @test-webhook-payload.json
```

#### Webhook Job Mapping (Local)
- `main`/`master` → `ai-ml-pipeline-production`
- `develop`/`staging` → `ai-ml-pipeline-staging`
- `feature/*` → `ai-ml-pipeline-feature`

### Production Pipeline Integration

#### Two-Instance Architecture (Production)
- **Controller**: Lightweight tests, orchestration
- **GPU Agent**: On-demand GPU processing
- **Auto-scaling**: GPU agent starts/stops automatically
- **Cost Optimization**: 95% reduction vs always-on GPU

#### Migration Strategy
1. **Develop locally** with Docker Compose
2. **Test webhooks** and pipeline triggers
3. **Deploy to OCI** using Terraform or existing instance
4. **Migrate configurations** from local to production
5. **Enable GPU agent** for production workloads

## Integrations & Dependencies

### Local Development Dependencies
- **GitHub**: Personal Access Token for repository access
- **Docker**: For containerized pipeline testing
- **Python**: For validation script execution
- **Node.js/npm**: For any JavaScript-based tooling

### Production Dependencies (Two-Instance)
- **OCI CLI**: For GPU agent lifecycle management
- **SSH Keys**: For secure agent communication
- **Terraform**: For Infrastructure-as-Code deployment
- **Monitoring**: Prometheus/Grafana integration
- **Logging**: ELK stack or similar centralized logging

## Maintenance

### Local Development Maintenance
```bash
# Update Jenkins container
docker-compose -f docker/docker-compose.jenkins.yml pull
docker-compose -f docker/docker-compose.jenkins.yml down
docker-compose -f docker/docker-compose.jenkins.yml up -d

# View logs
docker logs -f deployer-jenkins-cicd

# Clean up Docker resources
docker system prune -f
```

### Production Maintenance (Two-Instance)
- **Controller Updates**: Monthly Jenkins LTS and plugin updates
- **GPU Agent Updates**: Update when agent is running (auto-update on start)
- **Monitoring**: Prometheus Node Exporter + Grafana dashboards
- **Logging**: Forward logs to centralized ELK or Loki stack
- **Cost Monitoring**: Track GPU agent usage and costs

## Runbook (Quick Actions)

### Local Development Commands
| Task | Command |
|------|---------|
| **Start Jenkins** | `docker-compose -f docker/docker-compose.jenkins.yml up -d` |
| **Stop Jenkins** | `docker-compose -f docker/docker-compose.jenkins.yml down` |
| **View logs** | `docker logs -f deployer-jenkins-cicd` |
| **Get admin password** | `docker exec deployer-jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword` |
| **Test webhook** | `curl http://localhost:9000/health` |
| **Clean restart** | `docker-compose down && docker-compose up -d` |

### Production Commands (Two-Instance)
| Task | Command |
|------|---------|
| **Check GPU agent status** | `/opt/manage-gpu-agent.sh status` |
| **Start GPU agent** | `/opt/manage-gpu-agent.sh start` |
| **Stop GPU agent** | `/opt/manage-gpu-agent.sh stop` |
| **Get GPU agent IP** | `/opt/manage-gpu-agent.sh ip` |
| **Check GPU costs** | `/opt/gpu-agent-cost-tracker.sh report` |
| **Restart controller** | `sudo systemctl restart jenkins` |

## Migration Guide: Local → Production

### Phase 1: Local Development (Current)
1. ✅ Docker Compose setup
2. ✅ Webhook integration testing
3. ✅ Pipeline configuration validation
4. ✅ Multi-branch pipeline testing

### Phase 2: Production Deployment (Next)
1. **Choose deployment strategy**:
   - **Option A**: Use existing OCI instance (140.238.181.119)
   - **Option B**: Deploy with Terraform (recommended)
   - **Option C**: Manual OCI instance setup

2. **Deploy Jenkins controller** on OCI bastion
3. **Configure GPU agent** for on-demand processing
4. **Migrate credentials** and configurations
5. **Set up monitoring** and alerting
6. **Enable webhook integration** for production

### Benefits of Two-Instance Architecture

| Aspect | Local Docker | Two-Instance Production |
|--------|-------------|------------------------|
| **Cost** | $0/month | $15-25/month |
| **GPU Support** | Limited | Full GPU agent support |
| **Scalability** | Single instance | Auto-scaling GPU agent |
| **Webhook Integration** | ✅ | ✅ |
| **Production Ready** | Testing only | ✅ |

## Related Documentation

### Local Development
- [Jenkins Setup Guide (Main)](jenkins.md) - Comprehensive setup guide
- [Docker Compose Configuration](../../docker/docker-compose.jenkins.yml) - Local setup file
- [Deployment Strategy](jenkins.md) - Migration guide

### Production Deployment
- [Two-Instance Architecture](local-jenkins.md) - Cost-optimized architecture
- Terraform GPU Production: refer to your cloud provider’s Terraform registry and internal infra docs - Infrastructure-as-Code
- [Jenkins Setup Guide (OCI)](jenkins.md) - OCI-specific setup

### Advanced Features
- [Jenkins Deployment Strategy](jenkins.md) - Complete deployment guide
- [Two-Instance Deployment Plan](jenkins.md) - Step-by-step plan
- [Local Jenkins Overview](local-jenkins.md) - Architecture overview

---

**Last Reviewed**: October 5, 2025
**Architecture**: Local Docker (Development) → Two-Instance Production (Recommended)
**Cost Optimization**: 95% reduction enabled in production
**Status**: Ready for production deployment
**Next Step**: Execute production deployment following [Jenkins Deployment Strategy](jenkins.md)
