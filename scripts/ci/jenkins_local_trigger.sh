#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL=${JENKINS_URL:-http://localhost:8080}
JENKINS_USER=${JENKINS_USER:-admin}
JENKINS_PASS=${JENKINS_PASS:?set JENKINS_PASS}
JOB=${1:-3d-ddf-validation}

echo "🚀 Triggering Jenkins job: $JOB"
echo "📍 Jenkins URL: $JENKINS_URL"
echo "👤 User: $JENKINS_USER"

# Get crumb and save cookies
echo "�� Getting authentication crumb..."
CRUMB=$(curl -s -c cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/crumbIssuer/api/json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["crumb"])')
HEADER=$(curl -s -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/crumbIssuer/api/json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["crumbRequestField"])')

echo "🍪 Got crumb and cookies"

# Trigger build
echo "▶️  Triggering build..."
curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" -H "$HEADER: $CRUMB" -X POST \
  "$JENKINS_URL/job/$JOB/build" -o /dev/null

echo "✅ Build triggered successfully"

# Optional: Wait and fetch build status
if [[ "${2:-}" == "--wait" ]]; then
    echo "⏳ Waiting for build to start..."
    sleep 5
    
    # Get last build number
    BUILD_NUMBER=$(curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/job/$JOB/lastBuild/api/json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["number"])')
    
    if [[ -n "$BUILD_NUMBER" ]]; then
        echo "📊 Build #$BUILD_NUMBER started"
        
        # Fetch console output
        echo "📄 Fetching console output..."
        curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/job/$JOB/$BUILD_NUMBER/consoleText" -o "jenkins_build_${BUILD_NUMBER}.log"
        echo "💾 Console output saved to: jenkins_build_${BUILD_NUMBER}.log"
    fi
fi

# Clean up cookies
rm -f cookies.txt

echo "🧹 Cleanup completed"
echo "🎉 Jenkins job trigger completed successfully"
