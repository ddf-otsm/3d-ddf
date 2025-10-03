#!/bin/bash
#
# Install git hooks for documentation validation
#

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SCRIPT_DIR="$REPO_ROOT/scripts/hooks"

echo "📦 Installing documentation validation hooks..."
echo ""

# Check if .git directory exists
if [ ! -d "$HOOKS_DIR" ]; then
    echo "❌ Error: Not a git repository or .git/hooks directory not found"
    exit 1
fi

# Install pre-commit hook
echo "Installing pre-commit hook..."
cp "$SCRIPT_DIR/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"
echo "✅ pre-commit hook installed"

echo ""
echo "✅ Installation complete!"
echo ""
echo "The pre-commit hook will now validate documentation structure before each commit."
echo ""
echo "To test the hook, run:"
echo "  python3 scripts/validate_docs.py"
echo ""
echo "To bypass the hook (not recommended):"
echo "  git commit --no-verify"
echo ""
