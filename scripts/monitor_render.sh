#!/bin/bash
# Monitor the current render progress in real-time

LOG_FILE=$(ls -t /Users/luismartins/local_repos/3d-ddf/render_logs/dadosfera_FINAL_*.log 2>/dev/null | head -1)

if [ -z "$LOG_FILE" ]; then
    echo "❌ No render log found"
    exit 1
fi

echo "📊 Monitoring render: $(basename $LOG_FILE)"
echo "Press Ctrl+C to stop monitoring"
echo ""

tail -f "$LOG_FILE"
