#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL=${JENKINS_URL:-http://localhost:8080}
JENKINS_USER=${JENKINS_USER:-admin}
JENKINS_PASS=${JENKINS_PASS:?set JENKINS_PASS}
JOB_NAME="3d-ddf-validation"
CONFIG_FILE="docker/jenkins-pipeline-config.xml"

echo "🔧 Setting up Jenkins Pipeline job: $JOB_NAME"
echo "📍 Jenkins URL: $JENKINS_URL"
echo "📄 Config file: $CONFIG_FILE"

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Get crumb and save cookies
echo "�� Getting authentication crumb..."
CRUMB=$(curl -s -c cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/crumbIssuer/api/json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["crumb"])')
HEADER=$(curl -s -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/crumbIssuer/api/json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["crumbRequestField"])')

echo "🍪 Got crumb and cookies"

# Create/replace the Pipeline job
echo "📝 Creating/replacing Pipeline job..."
RESPONSE=$(curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" \
  -H "$HEADER: $CRUMB" \
  -H "Content-Type: application/xml" \
  --data-binary @"$CONFIG_FILE" \
  "$JENKINS_URL/createItem?name=$JOB_NAME&mode=org.jenkinsci.plugins.workflow.job.WorkflowJob")

if [[ -z "$RESPONSE" ]]; then
    echo "✅ Pipeline job created/replaced successfully"
else
    echo "⚠️  Response received: $RESPONSE"
fi

# Verify job was created
echo "🔍 Verifying job creation..."
JOB_INFO=$(curl -s -b cookies.txt -u "$JENKINS_USER:$JENKINS_PASS" "$JENKINS_URL/job/$JOB_NAME/api/json")

if echo "$JOB_INFO" | python3 -c 'import json,sys; data=json.load(sys.stdin); print(f"Job: {data.get(\"name\")}, Class: {data.get(\"_class\")}")' 2>/dev/null; then
    echo "✅ Job verified: Pipeline job created successfully"
else
    echo "❌ Job verification failed"
    echo "Response: $JOB_INFO"
    exit 1
fi

# Clean up cookies
rm -f cookies.txt

echo "🧹 Cleanup completed"
echo "🎉 Jenkins Pipeline job setup completed successfully"
echo ""
echo "📋 Next steps:"
echo "1. Open Jenkins at: $JENKINS_URL"
echo "2. Job should be available as: $JOB_NAME"
echo "3. Trigger a build to test the pipeline"
