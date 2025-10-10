#!/bin/bash
# Check Jenkins status without UI
set -euo pipefail

# Source shared Jenkins config
source ~/vars/jenkins_config.sh

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

echo "🔍 Checking Jenkins Status"
echo "   URL: $JENKINS_URL"
echo ""

# Check if Jenkins is responding
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$JENKINS_URL" || echo "000")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "403" ]; then
    echo "✅ Jenkins is running (HTTP $HTTP_CODE)"
else
    echo "❌ Jenkins is not responding (HTTP $HTTP_CODE)"
    echo ""
    echo "To start Jenkins:"
    echo "  /opt/homebrew/opt/openjdk@21/bin/java \\"
    echo "    -Dmail.smtp.starttls.enable=true \\"
    echo "    -jar /opt/homebrew/opt/jenkins-lts/libexec/jenkins.war \\"
    echo "    --httpListenAddress=127.0.0.1 \\"
    echo "    --httpPort=17843 \\"
    echo "    > ~/vars/jenkins.log 2>&1 &"
    echo "  echo \$! > ~/vars/jenkins.pid"
    exit 1
fi

# Check process
if [ -f ~/vars/jenkins.pid ]; then
    PID=$(cat ~/vars/jenkins.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Jenkins process running (PID: $PID)"
    else
        echo "⚠️  PID file exists but process not running"
    fi
fi

# Get Jenkins version and system info (if credentials available)
if [ -n "$JENKINS_PASSWORD" ]; then
    echo ""
    echo "📊 Jenkins Information (authenticated as: $JENKINS_USER):"
    
    # Get version
    API_RESPONSE=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" "$JENKINS_URL/api/json" 2>/dev/null || echo '{}')
    VERSION=$(echo "$API_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Version: {data.get('version', 'N/A')}\")" 2>/dev/null || echo "Version: N/A")
    echo "   $VERSION"
    
    # List jobs
    echo ""
    echo "📋 Configured Jobs:"
    JOBS=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" \
        "$JENKINS_URL/api/json?tree=jobs[name,color,url]" | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
jobs = data.get('jobs', [])
if jobs:
    for job in jobs:
        status = '✅' if 'blue' in job.get('color', '') else '❌' if 'red' in job.get('color', '') else '⚪'
        print(f\"   {status} {job['name']}\")
        print(f\"      URL: {job['url']}\")
else:
    print('   No jobs configured')
" 2>/dev/null || echo "   Unable to fetch jobs")
    
    # Queue status
    echo ""
    echo "🔄 Build Queue:"
    QUEUE=$(curl -s -u "$JENKINS_USER:$JENKINS_PASSWORD" \
        "$JENKINS_URL/queue/api/json" | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"   {len(data.get('items', []))} items in queue\")" 2>/dev/null || echo "   Unable to fetch queue")
    echo "$QUEUE"
else
    echo ""
    echo "⚠️  No Jenkins credentials found. Limited information available."
    echo "   Set JENKINS_PASSWORD or ensure password file exists:"
    echo "   - ~/vars/jenkins_admin_password_port17843.txt"
    echo "   - /opt/homebrew/var/jenkins_home/secrets/initialAdminPassword"
fi

echo ""
echo "📁 Jenkins Home: $JENKINS_HOME"
echo "📝 Logs: tail -f ~/vars/jenkins.log"
echo ""
echo "💡 Tips:"
echo "   - Setup pipeline: bash scripts/setup_jenkins_pipeline.sh"
echo "   - Trigger build: bash scripts/trigger_jenkins_build.sh"
echo "   - View UI: open $JENKINS_URL"

