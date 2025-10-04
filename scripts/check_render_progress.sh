#!/bin/bash
# Check render progress for dadosfera alpha release

# Resolve project root dynamically
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

RENDER_FILE="$PROJECT_ROOT/projects/dadosfera-explosions/exports/dadosfera_rendered_alpha.mp4"

echo "🎬 Checking render progress..."
echo ""

if [ -f "$RENDER_FILE" ]; then
    SIZE=$(ls -lh "$RENDER_FILE" | awk '{print $5}')
    echo "✅ Render file exists!"
    echo "   File: dadosfera_rendered_alpha.mp4"
    echo "   Size: $SIZE"
    echo ""
    echo "📊 File info:"
    ffprobe -v quiet -print_format json -show_format -show_streams "$RENDER_FILE" 2>/dev/null | grep -E "duration|width|height|bit_rate" | head -5
    echo ""
    echo "✅ Render complete! Ready for alpha release."
else
    echo "⏳ Render still in progress..."
    echo "   Expected completion: 15-20 minutes from start"
    echo "   Target: 1920x1080, 240 frames, EEVEE with materials"
    echo ""
    echo "💡 This is a PROPER render (not viewport capture)"
    echo "   Materials, lighting, and effects will be fully visible"
fi
