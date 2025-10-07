# Local Jenkins Controller Reference - Advanced Multi-Architecture

## Overview
- **Purpose**: Development and testing environment for 3D-DDF CI/CD pipelines
- **Architecture**: Local Docker-based Jenkins with optional webhook integration
- **Install Method**: Docker Compose (recommended) for easy testing and development
- **Primary Use Cases**:
  - Pipeline development and testing (Jenkinsfile validation)
  - Webhook integration testing (GitHub triggers)
  - Cost-effective development environment ($0/month)
  - Advanced architecture testing before production deployment

## Infrastructure
| Component | Details |
|-----------|---------|
| **Container** | `deployer-jenkins-cicd` (Jenkins LTS) |
| **Webhook** | `deployer-jenkins-webhook` (Python Flask) |
| **Ports** | 8080 (Jenkins UI), 50000 (agents), 9000 (webhook) |
| **Network** | `jenkins-cicd-network` (isolated) |
| **Storage** | Docker volume `jenkins-cicd-data` |
| **Access** | http://localhost:8080 (local only) |

## Architecture Options

### Option 1: Local Docker (Development)
```bash
# Start complete Jenkins environment
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Services started:
# - deployer-jenkins-cicd (Jenkins controller)
# - deployer-jenkins-webhook (Webhook receiver)
# - jenkins-cicd-network (isolated network)
```

### Option 2: Production Two-Instance (Recommended)
- **Controller**: OCI bastion instance (always-on, ~$10-15/month)
- **GPU Agent**: OCI GPU instance (on-demand, ~$5-10/month)
- **Migration Path**: Local → Production (documented in deployment strategy)

## Local Development Setup

### Quick Start Commands

```bash
# 1. Start Docker Desktop (if not running)
open -a Docker  # macOS

# 2. Launch Jenkins locally
docker-compose -f docker/docker-compose.jenkins.yml up -d

# 3. Wait for Jenkins to initialize
echo "⏳ Waiting for Jenkins to start..."
sleep 60

# 4. Get initial admin password
docker exec deployer-jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword

# 5. Access Jenkins UI
open http://localhost:8080
```

### Initial Configuration

1. **Enter admin password** from step 4 above
2. **Install suggested plugins** (Pipeline, Git, Credentials Binding, etc.)
3. **Create admin user** with secure credentials
4. **Skip instance configuration** (use default localhost:8080)

### Webhook Integration (Optional)

```bash
# Test webhook endpoint locally
curl http://localhost:9000/health

# Trigger pipeline via webhook
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
- [Docker Compose Configuration](See docker-compose.jenkins.yml in project root) - Local setup file
- [Deployment Strategy](See Jenkins deployment documentation) - Migration guide

### Production Deployment
- [Two-Instance Architecture](See Jenkins infrastructure documentation) - Cost-optimized architecture
- [Terraform GPU Production](See terraform documentation for OCI GPU production setup) - Infrastructure-as-Code
- [Jenkins Setup Guide (OCI)](See Jenkins setup guide documentation) - OCI-specific setup

### Advanced Features
- [Jenkins Deployment Strategy](See Jenkins deployment documentation) - Complete deployment guide
- [Two-Instance Deployment Plan](See Jenkins deployment plan in active plans) - Step-by-step plan
- [Local Jenkins Overview](See local Jenkins overview documentation) - Architecture overview

---

**Last Reviewed**: October 5, 2025
**Architecture**: Local Docker (Development) → Two-Instance Production (Recommended)
**Cost Optimization**: 95% reduction enabled in production
**Status**: Ready for production deployment
**Next Step**: Execute production deployment following [Jenkins Deployment Strategy](See Jenkins deployment documentation)
