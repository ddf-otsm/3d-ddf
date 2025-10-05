#!/bin/bash
set -euo pipefail

echo "🚀 Installing centralized git hooks..."

# Create .githooks directory if it doesn't exist
mkdir -p .githooks

# Remove existing hooks
rm -f .git/hooks/pre-push

# Create symlink for pre-push hook
ln -sf ../../.githooks/pre-push .git/hooks/pre-push

# Make sure the hook is executable
chmod +x .git/hooks/pre-push

echo "✅ Git hooks installed successfully!"
echo "   Pre-push hook: .git/hooks/pre-push → .githooks/pre-push"

echo ""
echo "To install hooks on other clones:"
echo "   git clone <repo>"
echo "   cd <repo>"
echo "   ./install-hooks.sh"
echo ""
echo "To update hooks:"
echo "   git pull"
echo "   ./install-hooks.sh"
