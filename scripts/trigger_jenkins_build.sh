#!/bin/bash
# Trigger Jenkins build via CLI/API (no UI needed)
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
PIPELINE_NAME="${1:-3d-ddf-local}"
WAIT_FOR_BUILD="${WAIT_FOR_BUILD:-false}"

echo "🚀 Triggering Jenkins build: $PIPELINE_NAME"

# Check if Jenkins is running
if ! curl -s -o /dev/null -w "%{http_code}" "$JENKINS_URL" | grep -qE '^(200|403)$'; then
    echo "❌ Jenkins is not running at $JENKINS_URL"
    exit 1
fi

# Method 1: Jenkins CLI (preferred)
if [ -f "$JENKINS_CLI_JAR" ] && [ -n "$JENKINS_PASSWORD" ]; then
    echo "🔧 Triggering via Jenkins CLI..."
    
    if [ "$WAIT_FOR_BUILD" = "true" ]; then
        java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_PASSWORD" \
            build "$PIPELINE_NAME" -s -v
    else
        java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_PASSWORD" \
            build "$PIPELINE_NAME"
    fi
    
# Method 2: REST API fallback
elif [ -n "$JENKINS_PASSWORD" ]; then
    echo "🔧 Triggering via REST API..."
    
    # Get CSRF crumb
    CRUMB_JSON=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" "$JENKINS_URL/crumbIssuer/api/json" 2>/dev/null || echo '{}')
    CRUMB_FIELD=$(echo "$CRUMB_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('crumbRequestField',''))" 2>/dev/null || echo "")
    CRUMB_VALUE=$(echo "$CRUMB_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('crumb',''))" 2>/dev/null || echo "")
    
    if [ -z "$CRUMB_FIELD" ] || [ -z "$CRUMB_VALUE" ]; then
        CRUMB_ARGS=""
    else
        CRUMB_ARGS="-H \"$CRUMB_FIELD: $CRUMB_VALUE\""
    fi
    
    RESPONSE=$(eval curl -s -w "\\n%{http_code}" -X POST -u "$JENKINS_USER:$JENKINS_PASSWORD" \
        $CRUMB_ARGS \
        "$JENKINS_URL/job/$PIPELINE_NAME/build")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    
    if [ "$HTTP_CODE" = "201" ]; then
        echo "✅ Build triggered successfully"
        
        if [ "$WAIT_FOR_BUILD" = "true" ]; then
            echo "⏳ Waiting for build to complete..."
            sleep 5
            
            # Get last build number
            BUILD_NUM=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" \
                "$JENKINS_URL/job/$PIPELINE_NAME/lastBuild/buildNumber")
            
            # Poll build status
            while true; do
                BUILD_STATUS=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" \
                    "$JENKINS_URL/job/$PIPELINE_NAME/$BUILD_NUM/api/json" | \
                    python3 -c "import sys, json; print(json.load(sys.stdin).get('result', 'BUILDING'))")
                
                if [ "$BUILD_STATUS" != "BUILDING" ]; then
                    echo "📊 Build #$BUILD_NUM completed: $BUILD_STATUS"
                    
                    # Show console output
                    echo ""
                    echo "📋 Console Output:"
                    curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" \
                        "$JENKINS_URL/job/$PIPELINE_NAME/$BUILD_NUM/consoleText" | tail -n 50
                    
                    [ "$BUILD_STATUS" = "SUCCESS" ] && exit 0 || exit 1
                fi
                
                echo "   Build #$BUILD_NUM still running..."
                sleep 10
            done
        fi
    else
        echo "❌ Failed to trigger build (HTTP $HTTP_CODE)"
        exit 1
    fi
else
    echo "❌ Missing Jenkins credentials"
    echo "   Set JENKINS_PASSWORD or save it to ~/vars/jenkins_admin_password_port17843.txt"
    exit 1
fi

echo ""
echo "📊 View build at: $JENKINS_URL/job/$PIPELINE_NAME"
echo "📋 Console output: $JENKINS_URL/job/$PIPELINE_NAME/lastBuild/console"

