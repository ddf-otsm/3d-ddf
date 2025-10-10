# Jenkins Automation - No UI Required

## Overview
Complete Jenkins automation for 3d-ddf using the shared local Jenkins instance (`http://localhost:17843`). All operations can be performed via CLI/API without opening the browser.

## Setup Status

### ✅ Completed
- **Shared Jenkins Integration**: 3d-ddf added to `~/vars/jenkins_config.sh`
- **Documentation Updated**: Local Jenkins refs point to shared instance (port 17843)
- **Automation Scripts**: Three scripts created for full automation
- **CSRF Protection**: Proper crumb handling for API calls
- **Multi-Source Auth**: Fallback password detection from multiple locations

### ⏳ Requires One-Time Manual Setup
Jenkins needs initial configuration via UI (one time only):
1. Visit: `http://localhost:17843`
2. Enter password: Check `~/vars/jenkins_admin_password_port17843.txt`
3. Install suggested plugins
4. Create admin user (or use 'admin' + initial password)
5. After setup, all automation scripts work without UI

## Automation Scripts

### 1. Check Status
**Script**: `scripts/check_jenkins_status.sh`

```bash
bash scripts/check_jenkins_status.sh
```

**Output**:
- Jenkins running status (HTTP code, PID)
- Version information
- Configured jobs list
- Build queue status
- Helpful tips

**No Authentication Required**: Basic status check works without credentials

---

### 2. Setup Pipeline
**Script**: `scripts/setup_jenkins_pipeline.sh`

```bash
# Create/update pipeline
bash scripts/setup_jenkins_pipeline.sh
```

**What it does**:
- Creates `3d-ddf-local` pipeline job
- Configures Git SCM: `file:///Users/luismartins/local_repos/3d-ddf`
- Sets branch: `*/main`
- Links to `Jenkinsfile` in repo root
- Uses CLI (preferred) or REST API (fallback)

**Requirements**: Jenkins credentials (auto-detected from multiple sources)

**Output**:
```
🔧 Setting up Jenkins pipeline: 3d-ddf-local
   Jenkins URL: http://localhost:17843
✅ Jenkins is running
🔧 Using REST API to create pipeline...
   Fetching CSRF crumb...
   Using crumb: Jenkins-Crumb
📦 Creating pipeline '3d-ddf-local'...
✅ Pipeline created/updated successfully (REST API)
```

---

### 3. Trigger Build
**Script**: `scripts/trigger_jenkins_build.sh`

```bash
# Quick trigger (async)
bash scripts/trigger_jenkins_build.sh

# Wait for completion and show console output
WAIT_FOR_BUILD=true bash scripts/trigger_jenkins_build.sh

# Trigger different pipeline
bash scripts/trigger_jenkins_build.sh my-other-pipeline
```

**Features**:
- Triggers builds via CLI or REST API
- Optional: Wait for build completion
- Stream console output when waiting
- Exit code reflects build result (0=success, 1=failure)

**Requirements**: Jenkins credentials + pipeline must exist

---

## Complete Workflow (No UI)

### Initial Setup (One-time)
```bash
# 1. Source shared config
source ~/vars/jenkins_config.sh

# 2. Verify Jenkins is running
bash scripts/check_jenkins_status.sh

# 3. Complete Jenkins initial setup (UI - one time only)
open http://localhost:17843
# - Enter password from ~/vars/jenkins_admin_password_port17843.txt
# - Install suggested plugins
# - Create admin user

# 4. Create pipeline (automated)
bash scripts/setup_jenkins_pipeline.sh
```

### Daily Use (Fully Automated)
```bash
# Trigger builds anytime
bash scripts/trigger_jenkins_build.sh

# Or wait for results
WAIT_FOR_BUILD=true bash scripts/trigger_jenkins_build.sh

# Check status
bash scripts/check_jenkins_status.sh

# View logs
tail -f ~/vars/jenkins.log
```

---

## Integration Examples

### Makefile
```makefile
.PHONY: jenkins-status jenkins-setup jenkins-build

jenkins-status:
\t@bash scripts/check_jenkins_status.sh

jenkins-setup:
\t@bash scripts/setup_jenkins_pipeline.sh

jenkins-build:
\t@WAIT_FOR_BUILD=true bash scripts/trigger_jenkins_build.sh
```

Usage:
```bash
make jenkins-status
make jenkins-setup
make jenkins-build
```

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run validations locally first
python3 scripts/validate_taxonomy.py || exit 1
python3 scripts/validate_links.py || exit 1

# Trigger Jenkins build (optional)
if [ "$JENKINS_AUTO_BUILD" = "true" ]; then
    bash scripts/trigger_jenkins_build.sh
fi
```

### CI/CD Wrapper
```bash
#!/bin/bash
# scripts/ci_cd_validate.sh

set -e

echo "🔍 Running local validations..."
python3 scripts/validate_taxonomy.py
python3 scripts/validate_links.py
python3 scripts/validate_json.py

echo "🚀 Triggering Jenkins pipeline..."
WAIT_FOR_BUILD=true bash scripts/trigger_jenkins_build.sh

echo "✅ All validations passed!"
```

---

## Technical Details

### Authentication
Scripts auto-detect credentials from multiple sources (in order):
1. `$JENKINS_PASSWORD` environment variable
2. `~/vars/jenkins_admin_password_port17843.txt`
3. `/opt/homebrew/var/jenkins_home/secrets/initialAdminPassword`

### CSRF Protection
- Fetches crumb from `/crumbIssuer/api/json`
- Includes `Jenkins-Crumb` header in all POST requests
- Handles crumb failures gracefully

### Methods
- **Preferred**: Jenkins CLI jar (`/opt/homebrew/opt/jenkins-lts/libexec/jenkins-cli.jar`)
- **Fallback**: REST API with CSRF crumbs
- Both support same operations (create, update, trigger builds)

### Error Handling
- Exit codes: `0` (success), `1` (failure)
- Helpful error messages with troubleshooting tips
- Graceful degradation (works with partial setup)

---

## Troubleshooting

### "Jenkins is not running"
```bash
# Start Jenkins
/opt/homebrew/opt/openjdk@21/bin/java \
  -Dmail.smtp.starttls.enable=true \
  -jar /opt/homebrew/opt/jenkins-lts/libexec/jenkins.war \
  --httpListenAddress=127.0.0.1 \
  --httpPort=17843 \
  > ~/vars/jenkins.log 2>&1 &
echo $! > ~/vars/jenkins.pid
```

### "Missing Jenkins credentials"
```bash
# Check password files
ls -l ~/vars/jenkins_admin_password_port17843.txt
ls -l /opt/homebrew/var/jenkins_home/secrets/initialAdminPassword

# Set manually
export JENKINS_PASSWORD="your-password-here"
```

### "No valid crumb" (403 Error)
- Jenkins initial setup incomplete
- Complete setup via UI: `open http://localhost:17843`
- After setup, rerun scripts

### "Pipeline not found"
```bash
# Create pipeline first
bash scripts/setup_jenkins_pipeline.sh

# Then trigger
bash scripts/trigger_jenkins_build.sh
```

### "Version: N/A" or empty job list
- Authentication issue or Jenkins not fully initialized
- Complete initial setup via UI
- Verify credentials work: `cat ~/vars/jenkins_admin_password_port17843.txt`

---

## Comparison: UI vs Automation

| Task | UI Method | Automation Method |
|------|-----------|-------------------|
| **Check Status** | Open browser, login | `bash scripts/check_jenkins_status.sh` |
| **Create Pipeline** | Click through 7+ screens | `bash scripts/setup_jenkins_pipeline.sh` |
| **Trigger Build** | Navigate, click "Build Now" | `bash scripts/trigger_jenkins_build.sh` |
| **View Results** | Open browser, find build | `WAIT_FOR_BUILD=true bash scripts/trigger_jenkins_build.sh` |
| **Integration** | Manual steps | Single command in CI/CD |

---

## Benefits

✅ **Speed**: Instant execution vs clicking through UI  
✅ **Reproducibility**: Same command, same result every time  
✅ **Automation**: Integrate with scripts, Makefiles, CI/CD  
✅ **No Context Switch**: Stay in terminal, no browser needed  
✅ **Scriptable**: Batch operations, conditional logic  
✅ **Documentation**: Commands are self-documenting

---

## Related Documentation

- **Shared Instance Setup**: `~/vars/JENKINS_LOCAL_HANDOFF.md`
- **Configuration**: `~/vars/jenkins_config.sh`
- **Docker Setup (Deprecated)**: `docs/setup/local-jenkins.md`
- **Main Jenkins Guide**: `docs/setup/jenkins.md`
- **Webhook Integration**: `scripts/webhook-receiver.py`

---

**Last Updated**: October 10, 2025  
**Status**: ✅ Ready for use (after initial Jenkins setup)  
**Scripts Location**: `scripts/check_jenkins_status.sh`, `scripts/setup_jenkins_pipeline.sh`, `scripts/trigger_jenkins_build.sh`

