#!/bin/bash
# Setup Jenkins Pipeline for 3d-ddf via CLI/API (no UI needed)
set -euo pipefail

# Source shared Jenkins config
source ~/vars/jenkins_config.sh

JENKINS_CLI_JAR="${JENKINS_CLI_JAR:-/opt/homebrew/opt/jenkins-lts/libexec/jenkins-cli.jar}"
JENKINS_USER="${JENKINS_USER:-admin}"
# Try multiple password sources
if [ -n "${JENKINS_PASSWORD:-}" ]; then
    : # Use existing env var
elif [ -f ~/vars/jenkins_admin_password_port17843.txt ]; then
    JENKINS_PASSWORD=$(cat ~/vars/jenkins_admin_password_port17843.txt)
elif [ -f /opt/homebrew/var/jenkins_home/secrets/initialAdminPassword ]; then
    JENKINS_PASSWORD=$(cat /opt/homebrew/var/jenkins_home/secrets/initialAdminPassword)
else
    JENKINS_PASSWORD=""
fi
PIPELINE_NAME="3d-ddf-local"
REPO_PATH="/Users/luismartins/local_repos/3d-ddf"

echo "🔧 Setting up Jenkins pipeline: $PIPELINE_NAME"
echo "   Jenkins URL: $JENKINS_URL"

# Create pipeline config XML
cat > /tmp/3d-ddf-pipeline-config.xml <<'EOF'
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.40">
  <description>3D-DDF validation pipeline (automated setup)</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <org.jenkinsci.plugins.workflow.job.properties.DisableConcurrentBuildsJobProperty/>
    <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
      <triggers/>
    </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.90">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.10.0">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>file:///Users/luismartins/local_repos/3d-ddf</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
EOF

# Check if Jenkins is running
if ! curl -s -o /dev/null -w "%{http_code}" "$JENKINS_URL" | grep -qE '^(200|403)$'; then
    echo "❌ Jenkins is not running at $JENKINS_URL"
    echo "   Start it with: ~/vars/jenkins_config.sh (see handoff doc)"
    exit 1
fi

echo "✅ Jenkins is running"

# Method 1: Jenkins CLI (preferred)
if [ -f "$JENKINS_CLI_JAR" ] && [ -n "$JENKINS_PASSWORD" ]; then
    echo "🔧 Using Jenkins CLI to create pipeline..."
    
    # Check if job exists
    if java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_PASSWORD" get-job "$PIPELINE_NAME" &>/dev/null; then
        echo "⚠️  Pipeline '$PIPELINE_NAME' already exists. Updating..."
        java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_PASSWORD" \
            update-job "$PIPELINE_NAME" < /tmp/3d-ddf-pipeline-config.xml
    else
        echo "📦 Creating pipeline '$PIPELINE_NAME'..."
        java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_PASSWORD" \
            create-job "$PIPELINE_NAME" < /tmp/3d-ddf-pipeline-config.xml
    fi
    
    echo "✅ Pipeline created/updated successfully (CLI)"
    
# Method 2: REST API fallback
elif [ -n "$JENKINS_PASSWORD" ]; then
    echo "🔧 Using REST API to create pipeline..."
    
    # Get CSRF crumb for API calls
    echo "   Fetching CSRF crumb..."
    CRUMB_JSON=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" "$JENKINS_URL/crumbIssuer/api/json" 2>/dev/null || echo '{}')
    CRUMB_FIELD=$(echo "$CRUMB_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('crumbRequestField',''))" 2>/dev/null || echo "")
    CRUMB_VALUE=$(echo "$CRUMB_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('crumb',''))" 2>/dev/null || echo "")
    
    if [ -z "$CRUMB_FIELD" ] || [ -z "$CRUMB_VALUE" ]; then
        echo "⚠️  Warning: Could not fetch CSRF crumb (may fail)"
        CRUMB_ARGS=""
    else
        CRUMB_ARGS="-H \"$CRUMB_FIELD: $CRUMB_VALUE\""
        echo "   Using crumb: $CRUMB_FIELD"
    fi
    
    # Check if job exists
    if curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" "$JENKINS_URL/job/$PIPELINE_NAME/config.xml" -o /dev/null -w "%{http_code}" 2>/dev/null | grep -q 200; then
        echo "⚠️  Pipeline '$PIPELINE_NAME' already exists. Updating..."
        eval curl -s -X POST -u "$JENKINS_USER:$JENKINS_PASSWORD" \
            $CRUMB_ARGS \
            "$JENKINS_URL/job/$PIPELINE_NAME/config.xml" \
            --data-binary "@/tmp/3d-ddf-pipeline-config.xml" \
            -H "Content-Type: application/xml"
    else
        echo "📦 Creating pipeline '$PIPELINE_NAME'..."
        RESPONSE=$(eval curl -s -w "\\n%{http_code}" -X POST -u "$JENKINS_USER:$JENKINS_PASSWORD" \
            $CRUMB_ARGS \
            "$JENKINS_URL/createItem?name=$PIPELINE_NAME" \
            --data-binary "@/tmp/3d-ddf-pipeline-config.xml" \
            -H "Content-Type: application/xml")
        
        HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
        if [ "$HTTP_CODE" = "200" ]; then
            echo "✅ Pipeline created successfully"
        else
            echo "❌ Failed to create pipeline (HTTP $HTTP_CODE)"
            echo "$RESPONSE" | head -n -1 || true
            exit 1
        fi
    fi
    
    echo "✅ Pipeline created/updated successfully (REST API)"
else
    echo "❌ Missing Jenkins credentials"
    echo "   Set JENKINS_PASSWORD or save it to ~/vars/jenkins_admin_password_port17843.txt"
    exit 1
fi

# Clean up temp file
rm -f /tmp/3d-ddf-pipeline-config.xml

echo ""
echo "📊 Pipeline Details:"
echo "   Name: $PIPELINE_NAME"
echo "   URL: $JENKINS_URL/job/$PIPELINE_NAME"
echo "   Repo: $REPO_PATH"
echo "   Jenkinsfile: Jenkinsfile"
echo ""
echo "🚀 To trigger a build (without UI):"
echo "   bash scripts/trigger_jenkins_build.sh"
echo "   or:"
echo "   curl -X POST -u $JENKINS_USER:PASSWORD $JENKINS_URL/job/$PIPELINE_NAME/build"

