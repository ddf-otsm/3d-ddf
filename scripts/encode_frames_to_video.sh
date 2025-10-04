#!/bin/bash
# Encode rendered PNG frames to final video

# Resolve project root dynamically
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

FRAMES_DIR="$PROJECT_ROOT/projects/dadosfera/renders/frames_alpha"
OUTPUT="$PROJECT_ROOT/projects/dadosfera/exports/dadosfera_ALPHA_RELEASE.mp4"

echo "🎬 Checking frame render progress..."

# Count frames
FRAME_COUNT=$(ls -1 "$FRAMES_DIR"/frame_*.png 2>/dev/null | wc -l | tr -d ' ')
EXPECTED=240

echo "   Frames rendered: $FRAME_COUNT / $EXPECTED"

if [ "$FRAME_COUNT" -lt "$EXPECTED" ]; then
    PERCENT=$(echo "scale=1; $FRAME_COUNT * 100 / $EXPECTED" | bc)
    echo "   Progress: ${PERCENT}%"
    echo "   ⏳ Still rendering... ($((EXPECTED - FRAME_COUNT)) frames remaining)"
    exit 0
fi

echo "   ✅ All $EXPECTED frames complete!"
echo ""
echo "🎥 Encoding frames to video..."
echo "   Output: $OUTPUT"

# Use FFmpeg to encode frames to high-quality MP4
ffmpeg -y \
    -framerate 24 \
    -i "$FRAMES_DIR/frame_%04d.png" \
    -c:v libx264 \
    -preset slow \
    -crf 18 \
    -pix_fmt yuv420p \
    -movflags +faststart \
    "$OUTPUT" \
    -hide_banner \
    -loglevel warning

if [ $? -eq 0 ]; then
    SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
    echo ""
    echo "✅ Video encode complete!"
    echo "   File: dadosfera_ALPHA_RELEASE.mp4"
    echo "   Size: $SIZE"
    echo "   Location: $OUTPUT"
    echo ""
    echo "🚀 ALPHA RELEASE READY!"
    echo "   Deploy to: 3d-ddf.alpha.dadosfera.info"
else
    echo "❌ Encoding failed!"
    exit 1
fi

