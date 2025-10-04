#!/bin/bash
# Monitor the current render progress in real-time

# Resolve project root dynamically
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

LOG_FILE=$(ls -t "$PROJECT_ROOT"/logs/dadosfera_FINAL_*.log 2>/dev/null | head -1)

if [ -z "$LOG_FILE" ]; then
    echo "❌ No render log found"
    exit 1
fi

echo "📊 Monitoring render: $(basename $LOG_FILE)"
echo "Press Ctrl+C to stop monitoring"
echo ""

tail -f "$LOG_FILE"

