# Jenkins CI/CD Setup

This document explains how to setup Jenkins for automated taxonomy validation.

## Prerequisites

- Jenkins server (on-premise installation)
- Python 3.10+ installed on Jenkins agent
- Git plugin for Jenkins
- Workspace cleanup plugin (optional)

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
- **Branch**: `*/master` (or your main branch)
- **Script Path**: `Jenkinsfile`

### 3. Configure Build Triggers

Choose one or more:

**Option A: Webhook (Recommended)**
- Check "GitHub hook trigger for GITScm polling"
- Or configure webhook in your Git server

**Option B: Poll SCM**
```
H/15 * * * *  # Poll every 15 minutes
```

**Option C: Manual**
- Trigger builds manually as needed

### 4. Save and Test

1. Click "Save"
2. Click "Build Now"
3. Check console output

## Pipeline Stages

The Jenkins pipeline runs these validation stages:

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

### 6. Generate Reports
Creates validation reports in `reports/` directory.

## Jenkinsfile Configuration

The `Jenkinsfile` at the repository root defines the pipeline.

### Environment Variables

```groovy
environment {
    PROJECT_NAME = '3d-ddf'
    PYTHON = 'python3'
}
```

Customize as needed for your Jenkins environment.

### Timeout

Default: 10 minutes. Adjust if needed:
```groovy
timeout(time: 10, unit: 'MINUTES')
```

### Notifications (Optional)

Uncomment email notifications in the `post` section:

```groovy
post {
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
```

## Advanced Configuration

### Multi-branch Pipeline

For feature branch validation:

1. Create "Multibranch Pipeline" instead
2. Configure branch sources
3. Jenkins will auto-discover branches with `Jenkinsfile`

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
agent {
    label 'python3'  // Only agents with 'python3' label
}
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

### Slow Builds

**Solutions**:
- Use parallel stages
- Increase timeout
- Cache dependencies
- Run only changed file validation

## Local Testing

Test the pipeline locally before pushing:

```bash
# Run all validators
python3 scripts/validate_taxonomy.py
python3 scripts/validate_links.py
python3 scripts/validate_json.py
python3 scripts/validate_file_sizes.py

# Or use pre-commit hook
.git/hooks/pre-commit
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
- Runs full validation suite
- Generates reports
- Sends notifications

### Workflow

```
Developer → git commit → pre-commit hook → git push → Jenkins pipeline
              ↓              ↓                  ↓           ↓
           Local check   Fast check        Remote      Full suite
```

## Monitoring

### Build Status

- Green ✅ - All validations passed
- Red ❌ - Validation failed
- Yellow ⚠️ - Unstable (warnings)

### Metrics to Track

1. **Build success rate**
2. **Average build duration**
3. **Validation failure types**
4. **Trend over time**

### Jenkins Dashboard

Add widgets:
- Build status
- Last success/failure
- Trend graph
- Test results

## Security

### Credentials

Never hardcode credentials in `Jenkinsfile`. Use Jenkins credentials:

```groovy
environment {
    API_KEY = credentials('render-api-key')
}
```

### Workspace Cleanup

Clean workspace after builds:

```groovy
post {
    always {
        cleanWs()
    }
}
```

## Best Practices

1. ✅ Keep Jenkinsfile in repository root
2. ✅ Version control all scripts
3. ✅ Use descriptive stage names
4. ✅ Add timeout limits
5. ✅ Archive important artifacts
6. ✅ Send notifications on failure
7. ✅ Clean workspace after build
8. ✅ Use parallel stages when possible
9. ✅ Document environment requirements
10. ✅ Test locally before pushing

## Support

- **Jenkinsfile**: `/Jenkinsfile`
- **Validators**: `/scripts/validate_*.py`
- **Pre-commit**: `/scripts/hooks/pre-commit`
- **Documentation**: `/docs/setup/jenkins.md`

---

**Last Updated**: October 2, 2025  
**Jenkins Version**: 2.x compatible  
**Python Version**: 3.10+
