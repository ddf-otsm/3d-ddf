#!/bin/bash
# ============================================================================
# Unified Dadosfera Render Service Wrapper
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SCENE_FILE="$PROJECT_ROOT/projects/dadosfera/blender_files/dadosfera_animation_v1.blend"
BLENDER_APP="/Applications/Blender.app/Contents/MacOS/Blender"
RENDER_SCRIPT="$SCRIPT_DIR/render_service.py"

# ============================================================================
# HELP
# ============================================================================

show_help() {
    cat << EOF
Dadosfera Unified Render Service

Usage: $0 [ENGINE] [QUALITY] [MATERIALS] [OPTIONS]

Quick Presets:
  $0 quick       # EEVEE draft (fastest)
  $0 preview     # CYCLES preview 
  $0 production  # CYCLES production (recommended)
  $0 final       # CYCLES final (highest quality)

Manual Configuration:
  ENGINE:     CYCLES | EEVEE (default: CYCLES)
  QUALITY:    draft | preview | production | final (default: production)
  MATERIALS:  default | photorealistic | clay (default: photorealistic)

Options:
  --start N        Start frame (default: 1)
  --end N          End frame (default: 240)
  --output-name    Custom output directory name
  --no-gpu         Disable GPU rendering

Examples:
  # Quick draft with EEVEE
  $0 EEVEE draft

  # Production render with photorealistic materials
  $0 CYCLES production photorealistic

  # Custom frame range
  $0 CYCLES preview --start 60 --end 120

  # Quick presets
  $0 quick       # Same as: EEVEE draft
  $0 preview     # Same as: CYCLES preview photorealistic
  $0 production  # Same as: CYCLES production photorealistic
  $0 final       # Same as: CYCLES final photorealistic

Quality Presets:
  draft      - 32 samples, 50% resolution (fastest)
  preview    - 64 samples, 75% resolution
  production - 128 samples, 100% resolution (recommended)
  final      - 256 samples, 100% resolution (highest quality)

Material Styles:
  default        - Use existing scene materials
  photorealistic - Chrome text, polished floor, glowing explosions
  clay           - Simple matte materials for lighting tests

EOF
    exit 0
}

# ============================================================================
# QUICK PRESETS
# ============================================================================

case "$1" in
    quick)
        ENGINE="EEVEE"
        QUALITY="draft"
        MATERIALS="default"
        shift
        ;;
    preview)
        ENGINE="CYCLES"
        QUALITY="preview"
        MATERIALS="photorealistic"
        shift
        ;;
    production)
        ENGINE="CYCLES"
        QUALITY="production"
        MATERIALS="photorealistic"
        shift
        ;;
    final)
        ENGINE="CYCLES"
        QUALITY="final"
        MATERIALS="photorealistic"
        shift
        ;;
    -h|--help|help)
        show_help
        ;;
    *)
        # Manual configuration
        ENGINE="${1:-CYCLES}"
        QUALITY="${2:-production}"
        MATERIALS="${3:-photorealistic}"
        shift 3 2>/dev/null || true
        ;;
esac

# ============================================================================
# VALIDATION
# ============================================================================

if [ ! -f "$BLENDER_APP" ]; then
    echo "❌ ERROR: Blender not found at $BLENDER_APP"
    exit 1
fi

if [ ! -f "$SCENE_FILE" ]; then
    echo "❌ ERROR: Scene file not found: $SCENE_FILE"
    exit 1
fi

# ============================================================================
# START RENDER
# ============================================================================

echo "============================================================================"
echo "DADOSFERA RENDER SERVICE"
echo "============================================================================"
echo ""
echo "📁 Scene:     $SCENE_FILE"
echo "🎨 Engine:    $ENGINE"
echo "⚙️  Quality:   $QUALITY"
echo "🎭 Materials: $MATERIALS"
echo "📌 Options:   $@"
echo ""
echo "🚀 Starting Blender..."
echo ""

"$BLENDER_APP" \
    --background \
    "$SCENE_FILE" \
    --python "$RENDER_SCRIPT" \
    -- \
    --engine "$ENGINE" \
    --quality "$QUALITY" \
    --materials "$MATERIALS" \
    "$@"

EXIT_CODE=$?

echo ""
echo "============================================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ RENDER COMPLETE!"
    echo ""
    echo "📂 Check: projects/dadosfera/renders/"
    echo "📝 Log:   logs/"
    echo ""
    echo "🎬 Next step: Encode to video"
    echo "   cd projects/dadosfera/renders/[output_dir]"
    echo "   ffmpeg -framerate 24 -i frame_%04d.png output.mp4"
    echo ""
else
    echo "❌ RENDER FAILED (exit code: $EXIT_CODE)"
    echo ""
    exit $EXIT_CODE
fi

