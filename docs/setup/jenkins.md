# Jenkins CI/CD Setup - Advanced Multi-Architecture

This document explains how to setup Jenkins for automated 3D-DDF project validation using modern, cost-optimized architectures.

## 🚀 Quick Start Options

### Option 1: Local Docker (Development/Testing)
```bash
# Start Jenkins locally for testing
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Access at: http://localhost:8080
# Get password: docker exec deployer-jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword
```

### Option 2: Two-Instance Architecture (Production)
- **Controller**: Lightweight bastion instance (always-on, ~$10-15/month)
- **GPU Agent**: On-demand GPU instance (~$5-10/month, 2-4 hours/week)
- **Cost Savings**: 95% reduction vs always-on GPU Jenkins

### Option 3: Existing OCI Instance
- Check existing Jenkins at: http://140.238.181.119:8080
- Admin password: `e3e1a3cdf81e441b83ad45f5eba07667`

## Prerequisites

### For Local Docker Setup
- Docker Desktop/Engine 24.x
- Git repository access
- 8GB+ RAM recommended

### For Production Deployment
- OCI account with compute instances
- SSH key pair for agent management
- Terraform (for Infrastructure-as-Code deployment)

## Architecture Overview

### Two-Instance Architecture (Recommended)

**Primary Jenkins Controller** (Bastion - Non-GPU)
- **Instance**: CPU-only bastion instance
- **Role**: Main Jenkins controller, lightweight tests
- **Always Running**: Yes (low cost: ~$10-15/month)
- **Runs**: Jest, Pytest (unit), BATS, Playwright, linting

**GPU Agent** (Mid-GPU - GPU-Capable)
- **Instance**: `VM.GPU.A10.1` or similar
- **Role**: GPU-heavy tests only (ML inference, CUDA tests)
- **Always Running**: No (on-demand, auto-start/stop)
- **Cost**: ~$5-10/month (only when running)

### Cost Comparison

| Architecture | Monthly Cost | Details |
|-------------|-------------|---------|
| **Always-On GPU Jenkins** | $450/month | VM.GPU.A10.1 24/7 |
| **Two-Instance (Recommended)** | $15-25/month | 95% cost reduction |
| **Local Docker** | $0/month | Development/testing only |

## Quick Setup

### 1. Create Jenkins Pipeline Job

1. Log into Jenkins
2. Click "New Item"
3. Enter name: `3d-ddf-validation`
4. Select "Pipeline"
5. Click OK

### 2. Configure Pipeline

**Pipeline Configuration:**
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: Your git repository URL
- **Branch**: `*/main` (or your main branch)
- **Script Path**: `Jenkinsfile`

### 3. Configure Build Triggers

Choose one or more:

**Option A: Webhook (Recommended)**
- Check "GitHub hook trigger for GITScm polling"
- Or configure webhook in your Git server
- Webhook service available at: `http://localhost:9000/webhook` (local) or OCI equivalent

**Option B: Poll SCM**
```
H/15 * * * *  # Poll every 15 minutes
```

**Option C: Manual**
- Trigger builds manually as needed

**Option D: Scheduled (Nightly GPU Tests)**
```
H 2 * * *  # Daily at 2 AM for GPU tests
```

### 4. Save and Test

1. Click "Save"
2. Click "Build Now"
3. Check console output

## Pipeline Stages

The Jenkins pipeline supports both lightweight (controller) and GPU-intensive (agent) stages:

### Lightweight Stages (Run on Controller)
These stages run on the main Jenkins controller (bastion instance):

### 1. Checkout
Checks out the repository code.

### 2. Validate Taxonomy
Runs `scripts/validate_taxonomy.py`:
- ✅ Documentation structure
- ✅ Export file naming
- ✅ Project consistency

### 3. Check Broken Links
Runs `scripts/validate_links.py`:
- ✅ Internal markdown links
- ✅ File references
- ✅ Orphaned files

### 4. Validate JSON
Runs `scripts/validate_json.py`:
- ✅ JSON syntax
- ✅ Schema validation
- ✅ Metadata consistency

### 5. Check File Sizes
Runs `scripts/validate_file_sizes.py`:
- ✅ Large file detection (>50MB warning)
- ✅ Empty file detection
- ✅ Size trend analysis

### GPU Stages (Run on GPU Agent - On-Demand)
These stages automatically start the GPU agent when needed:

### 6. GPU Tests (Optional)
Runs GPU-intensive tests:
- ✅ Blender rendering validation
- ✅ CUDA/ML inference tests
- ✅ GPU memory validation
- ✅ 3D model processing

### 7. Generate Reports
Creates validation reports in `reports/` directory.

## Advanced Jenkinsfile Configuration

### Two-Instance Pipeline Example

```groovy
pipeline {
    agent none  // Don't use default agent

    environment {
        PROJECT_NAME = '3d-ddf'
        PYTHON = 'python3'
        CUDA_VISIBLE_DEVICES = '0'
    }

    stages {
        stage('Lightweight Tests') {
            agent { label 'built-in' }  // Run on controller
            steps {
                parallel {
                    stage('Taxonomy') {
                        sh 'python3 scripts/validate_taxonomy.py'
                    }
                    stage('Links') {
                        sh 'python3 scripts/validate_links.py'
                    }
                    stage('JSON') {
                        sh 'python3 scripts/validate_json.py'
                    }
                }
            }
        }

        stage('GPU Tests') {
            when {
                anyOf {
                    branch 'main'
                    triggeredBy 'TimerTrigger'  // Nightly builds
                    expression { params.RUN_GPU_TESTS == true }
                }
            }
            agent {
                label 'gpu'  // Run on GPU agent
            }
            steps {
                echo '🚀 Starting GPU agent (if not already running)...'
                sh '''
                    # GPU-specific tests
                    nvidia-smi
                    python3 scripts/validate_blender_renders.py
                    python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
                '''
            }
            post {
                always {
                    echo '✅ GPU tests complete. Agent will shutdown after idle period.'
                }
            }
        }
    }

    post {
        always {
            node('built-in') {
                // Publish reports from controller
                publishHTML([
                    reportDir: 'reports/',
                    reportFiles: '*.html',
                    reportName: 'Validation Reports'
                ])
            }
        }
        success {
            emailext subject: "✅ Build SUCCESS",
                     body: "All validations passed.",
                     to: "team@example.com"
        }
        failure {
            emailext subject: "❌ Build FAILED",
                     body: "Check console output.",
                     to: "team@example.com"
        }
    }
}
```

### Environment Variables

```groovy
environment {
    PROJECT_NAME = '3d-ddf'
    PYTHON = 'python3'
    CUDA_VISIBLE_DEVICES = '0'
    NVIDIA_VISIBLE_DEVICES = 'all'
}
```

### GPU Agent Management

For automatic GPU agent lifecycle:

```groovy
// Shared library function for GPU agent management
def startGPUAgent() {
    sh '''
        cd /opt/deployer-ddf-mod-open-llms
        timeout 300 bash scripts/jenkins/manage-gpu-agent.sh start
    '''

    // Get IP and wait for agent to connect
    def gpuIP = sh(
        script: "timeout 30 bash scripts/jenkins/manage-gpu-agent.sh ip",
        returnStdout: true
    ).trim()

    timeout(time: 5, unit: 'MINUTES') {
        waitUntil {
            def node = Jenkins.instance.getNode('gpu-agent-mid-gpu')
            return node != null && node.toComputer().isOnline()
        }
    }
}
```

### Timeout Configuration

```groovy
timeout(time: 15, unit: 'MINUTES')  // Increased for GPU tests

// Stage-specific timeouts
stage('GPU Tests') {
    timeout(time: 30, unit: 'MINUTES')
    // ... GPU test steps
}
```

### Notifications (Enhanced)

```groovy
post {
    success {
        emailext subject: "✅ Build SUCCESS - 3D-DDF Validation",
                 body: "All validations passed.\nBuild: ${BUILD_NUMBER}\nDuration: ${currentBuild.durationString}",
                 to: "team@example.com"
    }
    failure {
        emailext subject: "❌ Build FAILED - 3D-DDF Validation",
                 body: "Check console output for details.\nBuild: ${BUILD_NUMBER}\nFailed Stage: ${failedStage}",
                 to: "team@example.com"
    }
    unstable {
        emailext subject: "⚠️ Build UNSTABLE - 3D-DDF Validation",
                 body: "Some tests failed but build continued.\nBuild: ${BUILD_NUMBER}",
                 to: "team@example.com"
    }
}
```

## Advanced Configuration

### Multi-branch Pipeline

For feature branch validation:

1. Create "Multibranch Pipeline" instead
2. Configure branch sources
3. Jenkins will auto-discover branches with `Jenkinsfile`

### GPU Agent Setup (Two-Instance Architecture)

#### 1. Configure GPU Agent Node

**Via Jenkins UI**:
1. Go to: Manage Jenkins → Manage Nodes and Clouds
2. Click: New Node
3. Configure:
   - **Name**: `gpu-agent-mid-gpu`
   - **Type**: Permanent Agent
   - **Remote root directory**: `/home/ubuntu/jenkins-agent`
   - **Labels**: `gpu gpu-a10 ml-inference cuda nvidia`
   - **Usage**: "Only build jobs with label expressions matching this node"
   - **Launch method**: "Launch agents via SSH"
     - **Host**: Dynamic IP from `manage-gpu-agent.sh ip`
     - **Credentials**: Add SSH key (`gpu-agent-key`)
     - **Host Key Verification**: Manually trusted
   - **Availability**: "Take this agent online when in demand, and offline when idle"
     - **In demand delay**: 1 minute
     - **Idle delay**: 10 minutes

#### 2. GPU Agent Management Script

```bash
#!/bin/bash
# Manage GPU Agent Instance Lifecycle
# Place at: /opt/manage-gpu-agent.sh

set -euo pipefail

OCI_PROFILE="${OCI_CLI_PROFILE:-sandbox}"
GPU_INSTANCE_NAME="deployer-ddf-production-mid-gpu"
COMPARTMENT_ID="${OCI_COMPARTMENT_ID:-ocid1.compartment.oc1..aaaaaaaa4ufqcvxjdlhagkcwwrh5w7ur4amsyzeg2i4gztco5ejitlzsnnbq}"

# Function to get instance OCID
get_instance_ocid() {
    timeout 30 oci --profile "$OCI_PROFILE" compute instance list \
        --compartment-id "$COMPARTMENT_ID" \
        --display-name "$GPU_INSTANCE_NAME" \
        --query 'data[0].id' \
        --raw-output
}

# Function to start instance
start_instance() {
    local instance_ocid="$1"

    echo "🚀 Starting GPU instance: $GPU_INSTANCE_NAME"
    timeout 60 oci --profile "$OCI_PROFILE" compute instance action \
        --instance-id "$instance_ocid" \
        --action START \
        --wait-for-state RUNNING

    # Wait for SSH to be ready
    local ip
    ip=$(get_instance_ip "$instance_ocid")

    echo "⏳ Waiting for SSH to be ready at $ip..."
    for i in {1..30}; do
        if timeout 5 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            ubuntu@"$ip" "echo 'SSH ready'" >/dev/null 2>&1; then
            echo "✅ SSH ready"
            return 0
        fi
        sleep 10
    done

    echo "⚠️  SSH not ready after 5 minutes"
    return 1
}

# Main command dispatcher
case "${1:-status}" in
    start)
        instance_ocid=$(get_instance_ocid)
        start_instance "$instance_ocid"
        get_instance_ip "$instance_ocid"
        ;;
    stop)
        instance_ocid=$(get_instance_ocid)
        echo "🛑 Stopping GPU instance: $GPU_INSTANCE_NAME"
        timeout 60 oci --profile "$OCI_PROFILE" compute instance action \
            --instance-id "$instance_ocid" \
            --action STOP \
            --wait-for-state STOPPED
        ;;
    status)
        instance_ocid=$(get_instance_ocid)
        state=$(get_instance_state "$instance_ocid")
        echo "Instance: $GPU_INSTANCE_NAME"
        echo "State: $state"
        ;;
    ip)
        instance_ocid=$(get_instance_ocid)
        get_instance_ip "$instance_ocid"
        ;;
esac
```

#### 3. Cost Tracking Script

```bash
#!/bin/bash
# GPU Agent Cost Tracker
# Place at: /opt/gpu-agent-cost-tracker.sh

LOG_FILE="/var/log/jenkins/gpu-agent-usage.log"
HOURLY_RATE=0.60

case "$1" in
    start)
        echo "$(date +%Y-%m-%d\ %H:%M:%S),START" >> "$LOG_FILE"
        ;;
    stop)
        echo "$(date +%Y-%m-%d\ %H:%M:%S),STOP" >> "$LOG_FILE"
        ;;
    report)
        MONTH=$(date +%Y-%m)
        HOURS=$(awk -F, -v month="$MONTH" 'BEGIN { total=0 } $1 ~ month { total += 1 } END { print total }' "$LOG_FILE")
        COST=$(echo "$HOURS * $HOURLY_RATE" | bc)
        echo "GPU Agent Usage - $MONTH"
        echo "Hours: $HOURS"
        echo "Cost: \$$COST"
        ;;
esac
```

### Deployment Options

#### Option 1: Local Docker (Development)

```bash
# Start for testing
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Access: http://localhost:8080
# Webhook: http://localhost:9000/webhook
```

#### Option 2: Check Existing OCI Instance

```bash
# Check if existing Jenkins is running
curl -I http://140.238.181.119:8080

# If accessible, login with existing credentials
```

#### Option 3: Deploy with Terraform (Recommended)

```bash
cd terraform/oci/gpu-production
terraform apply \
  -var="enable_sandbox_bastion=true" \
  -var="enable_sandbox_jenkins=true" \
  -var="sandbox_jenkins_port=8080"

# Get Jenkins URL
terraform output sandbox_jenkins_url
```

### Parallel Execution

Speed up validation with parallel stages:

```groovy
stage('Parallel Validations') {
    parallel {
        stage('Taxonomy') {
            steps {
                sh 'python3 scripts/validate_taxonomy.py'
            }
        }
        stage('Links') {
            steps {
                sh 'python3 scripts/validate_links.py'
            }
        }
        stage('JSON') {
            steps {
                sh 'python3 scripts/validate_json.py'
            }
        }
    }
}
```

### Agent Labels

Run on specific Jenkins agents:

```groovy
// Run on controller (lightweight tests)
agent { label 'built-in' }

// Run on GPU agent (GPU tests)
agent { label 'gpu' }

// Run on any agent with python3
agent { label 'python3' }
```

## Troubleshooting

### Python Not Found

**Error**: `python3: command not found`

**Solution**: Install Python 3 on Jenkins agent or specify full path:
```groovy
environment {
    PYTHON = '/usr/local/bin/python3'
}
```

### GPU Agent Connection Issues

**Error**: `GPU agent won't connect`

**Solutions**:
```bash
# Check GPU instance is running
/opt/manage-gpu-agent.sh status

# Check SSH connectivity from controller
sudo -u jenkins ssh -i ~/.ssh/gpu-agent-key ubuntu@<GPU_IP> "hostname"

# Check Jenkins agent logs on GPU instance
tail -f /home/ubuntu/jenkins-agent/remoting/logs/remoting.log
```

**Error**: `Agent doesn't stop after idle`

**Solutions**:
- Verify "Availability" is set to "Take offline when idle" in node config
- Check idle timeout setting (default: 10 minutes)
- Manual stop: `/opt/manage-gpu-agent.sh stop`

### Permission Denied

**Error**: `Permission denied: scripts/validate_taxonomy.py`

**Solution**: Ensure scripts are executable:
```bash
chmod +x scripts/*.py
```

### Validation Fails

**Check**:
1. Console output for specific error
2. Run validation locally: `python3 scripts/validate_taxonomy.py`
3. Check pre-commit hook works: `.git/hooks/pre-commit`

### High GPU Costs

**Check**:
```bash
# Check usage report
/opt/gpu-agent-cost-tracker.sh report

# Review Jenkins job configuration
# Ensure GPU label is only used for GPU-required tests
# Consider increasing idle timeout if jobs are frequent
```

### Slow Builds

**Solutions**:
- Use parallel stages for lightweight tests
- Increase timeout for GPU tests
- Cache dependencies
- Run only changed file validation

## Local Testing

Test the pipeline locally before pushing:

### Lightweight Tests (Controller)
```bash
# Run all validators
python3 scripts/validate_taxonomy.py
python3 scripts/validate_links.py
python3 scripts/validate_json.py
python3 scripts/validate_file_sizes.py

# Or use pre-commit hook
.git/hooks/pre-commit
```

### GPU Tests (Local Development)
```bash
# Test GPU functionality locally
nvidia-smi
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python3 scripts/validate_blender_renders.py
```

### Local Jenkins Testing
```bash
# Start local Jenkins for pipeline testing
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Access at: http://localhost:8080
# Test webhook: curl http://localhost:9000/webhook
```

## Integration with Git

### Pre-commit Hook

The pre-commit hook provides first-line defense:
```bash
# Runs on: git commit
🔍 Validating project taxonomy (docs + exports)...
```

### Jenkins Pipeline

Jenkins provides second-line defense:
- Validates on push/merge
- Runs full validation suite (lightweight + GPU tests)
- Generates reports
- Sends notifications
- Auto-manages GPU agent lifecycle

### Workflow

```
Developer → git commit → pre-commit hook → git push → Jenkins pipeline
              ↓              ↓                  ↓           ↓
           Local check   Fast check        Remote      Full suite + GPU
```

### Webhook Integration

**Local Development**:
```bash
# Webhook service for triggering builds
curl http://localhost:9000/webhook \
  -H "Content-Type: application/json" \
  -d '{"repository": {"name": "3d-ddf"}, "ref": "refs/heads/main"}'
```

**Production**:
- Configure GitHub webhook to point to Jenkins webhook service
- Supports automatic job mapping (main → production, develop → staging)

## Monitoring

### Build Status

- Green ✅ - All validations passed
- Red ❌ - Validation failed
- Yellow ⚠️ - Unstable (warnings)

### Metrics to Track

1. **Build success rate**
2. **Average build duration** (lightweight vs GPU stages)
3. **GPU agent utilization and costs**
4. **Validation failure types**
5. **Trend over time**

### Jenkins Dashboard

Add widgets:
- Build status
- Last success/failure
- Trend graph
- Test results
- GPU agent status
- Cost tracking

### Cost Monitoring

```bash
# Monthly GPU cost report
/opt/gpu-agent-cost-tracker.sh report

# Real-time agent status
/opt/manage-gpu-agent.sh status
```

## Security

### Credentials

Never hardcode credentials in `Jenkinsfile`. Use Jenkins credentials:

```groovy
environment {
    API_KEY = credentials('render-api-key')
    OCI_CLI_PROFILE = credentials('oci-cli-profile')
}
```

### SSH Key Management

For GPU agent access:
```bash
# Generate SSH key for GPU agent
ssh-keygen -t rsa -b 4096 -f ~/.ssh/gpu-agent-key -N ""

# Store private key in Jenkins credentials
# Copy public key to GPU agent authorized_keys
```

### Workspace Cleanup

Clean workspace after builds:

```groovy
post {
    always {
        cleanWs()
        // Stop GPU agent if it was started
        script {
            try {
                sh '/opt/manage-gpu-agent.sh stop'
            } catch (Exception e) {
                echo "No GPU agent to stop or already stopped"
            }
        }
    }
}
```

## Deployment Strategies

### Local Docker (Development/Testing)

**Best for**: Pipeline development, testing, CI/CD learning

```bash
# Quick start
docker-compose -f docker/docker-compose.jenkins.yml up -d

# Access: http://localhost:8080
# Webhook: http://localhost:9000/webhook
# Stop: docker-compose down
```

**Features**:
- Complete Jenkins environment in Docker
- Webhook receiver for testing triggers
- Persistent data storage
- Network isolation

### Two-Instance Architecture (Production)

**Best for**: Cost-optimized production workloads

**Architecture**:
- **Controller**: CPU-only bastion (~$10-15/month)
- **GPU Agent**: On-demand GPU instance (~$5-10/month)

**Benefits**:
- ✅ 95% cost reduction vs always-on GPU
- ✅ Lightweight tests run immediately
- ✅ GPU tests start automatically when needed
- ✅ Auto-shutdown after idle period

**Setup**: See [Two-Instance Architecture](#gpu-agent-setup-two-instance-architecture)

### Existing OCI Instance (Quick Start)

**Best for**: If existing Jenkins instance is available

```bash
# Check existing instance
curl -I http://140.238.181.119:8080

# Access with existing credentials
# Migrate pipelines to new Jenkinsfile format
```

## Best Practices

### Updated Best Practices for Advanced Setup

1. ✅ Keep Jenkinsfile in repository root
2. ✅ Version control all scripts and configurations
3. ✅ Use descriptive stage names with clear separation (lightweight vs GPU)
4. ✅ Add timeout limits (15min total, 30min for GPU stages)
5. ✅ Archive important artifacts and reports
6. ✅ Send notifications on failure with detailed context
7. ✅ Clean workspace after build and stop GPU agents
8. ✅ Use parallel stages for lightweight validations
9. ✅ Document environment requirements (controller vs GPU agent)
10. ✅ Test locally before pushing (both lightweight and GPU tests)
11. ✅ Implement cost tracking for GPU agent usage
12. ✅ Use Infrastructure-as-Code for production deployments
13. ✅ Configure proper SSH key management for agent access
14. ✅ Set up monitoring for both controller and GPU agent health
15. ✅ Use webhook integration for automated triggering

### Environment Variables for Jenkins

#### Controller (Bastion) Requirements
```groovy
environment {
    PROJECT_ROOT = "${WORKSPACE}"
    BLENDER = "/usr/bin/blender"  // For lightweight tests
    PYTHON = "python3"
}
```

#### GPU Agent Requirements
```groovy
environment {
    CUDA_VISIBLE_DEVICES = "0"
    NVIDIA_VISIBLE_DEVICES = "all"
    BLENDER = "/usr/bin/blender"  // GPU-enabled version
    TORCH_HOME = "/tmp/torch-cache"  // For ML models
}
```

#### Global Properties (Jenkins UI)
1. Go to Jenkins → Manage Jenkins → Configure System
2. Scroll to "Global properties"
3. Check "Environment variables"
4. Add key-value pairs:
   - `PROJECT_ROOT`: `/var/lib/jenkins/workspace/3d-ddf-validation`
   - `BLENDER`: `/usr/bin/blender`
   - `OCI_CLI_PROFILE`: `sandbox`
   - `CUDA_VISIBLE_DEVICES`: `0`

## Migration Guide

### From Basic to Advanced Jenkins

1. **Update Jenkinsfile** to use `agent none` pattern
2. **Add GPU stages** with `agent { label 'gpu' }`
3. **Configure GPU agent** in Jenkins UI
4. **Set up SSH keys** for GPU agent access
5. **Deploy management scripts** (`manage-gpu-agent.sh`)
6. **Configure webhooks** for automated triggering
7. **Set up cost tracking** for GPU agent monitoring
8. **Update notifications** to include GPU agent status

### From Local to Production

1. **Test locally** with Docker Compose
2. **Choose deployment option** (existing, Terraform, or manual)
3. **Deploy Jenkins** on OCI infrastructure
4. **Migrate pipelines** from local to production
5. **Configure production credentials** and SSH keys
6. **Set up monitoring** and alerting
7. **Deploy GPU agent** infrastructure
8. **Test end-to-end** pipeline execution

---

## Support

- **Jenkinsfile**: `/Jenkinsfile`
- **Validators**: `/scripts/validate_*.py`
- **Pre-commit**: `/scripts/hooks/pre-commit`
- **Documentation**: `/docs/setup/jenkins.md`
- **Environment**: `/.env.example`
- **Docker Compose**: `docker/docker-compose.jenkins.yml`
- **GPU Agent Management**: `/opt/manage-gpu-agent.sh`
- **Cost Tracking**: `/opt/gpu-agent-cost-tracker.sh`

### Related Documentation

- [Two-Instance Architecture Guide](../infrastructure/jenkins-two-instance-architecture.md)
- [Jenkins Deployment Strategy](../deployment/JENKINS_DEPLOYMENT_STRATEGY.md)
- [Local Jenkins Overview](../infrastructure/local-jenkins-overview.md)
- [Terraform GPU Production Module](../../../terraform/oci/gpu-production)

---

**Last Updated**: October 5, 2025
**Architecture**: Two-Instance (Controller + GPU Agent)
**Cost Optimization**: 95% reduction enabled
**Jenkins Version**: 2.x compatible
**Python Version**: 3.10+
**Recommended Deployment**: Terraform + OCI
