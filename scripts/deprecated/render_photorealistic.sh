#!/bin/bash
set -e

# ============================================================================
# Dadosfera Photorealistic Render Script
# ============================================================================
# This script:
# 1. Checks if Blender is installed
# 2. Loads the dadosfera scene
# 3. Applies photorealistic materials
# 4. Renders with CYCLES engine in background mode
# ============================================================================

PROJECT_ROOT="/Users/luismartins/local_repos/3d-ddf"
SCENE_FILE="$PROJECT_ROOT/projects/dadosfera/blender_files/dadosfera_animation_v1.blend"
BLENDER_APP="/Applications/Blender.app/Contents/MacOS/Blender"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/apply_photorealistic_and_render.py"
OUTPUT_DIR="$PROJECT_ROOT/projects/dadosfera/renders/frames_cycles_photorealistic"
LOG_FILE="$PROJECT_ROOT/render_logs/render_$(date +%Y%m%d_%H%M%S).log"

# Engine: CYCLES or EEVEE
ENGINE="${1:-CYCLES}"

echo "============================================================================"
echo "DADOSFERA PHOTOREALISTIC RENDER"
echo "============================================================================"
echo ""
echo "📁 Project root: $PROJECT_ROOT"
echo "🎬 Scene file: $SCENE_FILE"
echo "🎨 Engine: $ENGINE"
echo "📂 Output: $OUTPUT_DIR"
echo "📝 Log: $LOG_FILE"
echo ""

# ============================================================================
# VALIDATION
# ============================================================================

if [ ! -f "$BLENDER_APP" ]; then
    echo "❌ ERROR: Blender not found at $BLENDER_APP"
    echo "   Please install Blender from https://www.blender.org/download/"
    exit 1
fi

if [ ! -f "$SCENE_FILE" ]; then
    echo "❌ ERROR: Scene file not found: $SCENE_FILE"
    exit 1
fi

# ============================================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================================

mkdir -p "$OUTPUT_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# ============================================================================
# START RENDER
# ============================================================================

echo "🚀 Starting Blender in background mode..."
echo ""

"$BLENDER_APP" \
    --background \
    "$SCENE_FILE" \
    --python "$PYTHON_SCRIPT" \
    -- "$ENGINE" \
    2>&1 | tee "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "============================================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ RENDER COMPLETE!"
    echo "============================================================================"
    echo ""
    echo "📂 Frames: $OUTPUT_DIR"
    echo "📝 Log: $LOG_FILE"
    echo ""
    echo "🎬 Next step: Encode to video"
    echo "   Run: bash scripts/encode_frames_to_video.sh cycles_photorealistic"
    echo ""
else
    echo "❌ RENDER FAILED (exit code: $EXIT_CODE)"
    echo "============================================================================"
    echo ""
    echo "📝 Check log: $LOG_FILE"
    echo ""
    exit $EXIT_CODE
fi

