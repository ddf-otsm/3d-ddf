#!/bin/bash
#
# Fix export file naming violations
#
# This script renames files to follow the taxonomy convention:
# {project}_{version}_{date}_{quality}_{type}.mp4
#

set -e

EXPORTS_DIR="projects/dadosfera/exports"

echo "🔧 Fixing export file names..."
echo ""

cd "$EXPORTS_DIR"

# Check if files exist
if [ ! -f "dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4" ]; then
    echo "⚠️  File 1 already renamed or not found"
else
    echo "Renaming: CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4"
    mv "dadosfera_CYCLES_PRODUCTION_PHOTOREALISTIC_FINAL.mp4" \
       "dadosfera_stable_20251001_1080p_final.mp4"
    echo "   → dadosfera_stable_20251001_1080p_final.mp4"
    echo ""
fi

if [ ! -f "dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4" ]; then
    echo "⚠️  File 2 already renamed or not found"
else
    echo "Renaming: CYCLES_PHOTOREALISTIC_20251001_1409.mp4"
    mv "dadosfera_CYCLES_PHOTOREALISTIC_20251001_1409.mp4" \
       "dadosfera_alpha_20251001_1080p_preview.mp4"
    echo "   → dadosfera_alpha_20251001_1080p_preview.mp4"
    echo ""
fi

echo "✅ Done!"
echo ""
echo "Validating taxonomy..."
cd ../../..
python3 scripts/validate_taxonomy.py
