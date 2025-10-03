# Git Hooks for Documentation Validation

This directory contains git hooks to enforce documentation structure standards.

## Installation

### Automatic Installation (Recommended)

Run from the repository root:

```bash
./scripts/hooks/install.sh
```

### Manual Installation

```bash
# From repository root
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Available Hooks

### pre-commit

**Purpose**: Validates documentation structure before each commit

**Checks**:
- ✅ No unauthorized `.md` files in root directory
- ✅ No `documentation/` folder (use `docs/` instead)
- ✅ Proper `docs/` subdirectory structure exists
- ✅ No orphaned markdown files in unexpected locations

**Bypass** (not recommended):
```bash
git commit --no-verify
```

## Validation Rules

### Allowed Root-Level Markdown Files
- `README.md` - Project overview
- `QUICKSTART.md` - Quick setup guide
- `LICENSE.md` - License information
- `CONTRIBUTING.md` - Contribution guidelines

### Required Directory Structure
```
docs/
├── project/     # Roadmap, backlog, releases
├── guides/      # User guides
└── setup/       # Installation & troubleshooting
```

### Disallowed Patterns
- ❌ `documentation/` folder (duplication)
- ❌ `doc/` folder (inconsistent naming)
- ❌ `.md` files scattered in root
- ❌ Documentation in non-standard locations

## Manual Validation

Run validation anytime without committing:

```bash
python3 scripts/validate_docs.py
```

## Troubleshooting

### Hook not running?

```bash
# Check if hook is executable
ls -la .git/hooks/pre-commit

# If not executable, fix it:
chmod +x .git/hooks/pre-commit
```

### Skip validation for emergency commits

```bash
git commit --no-verify -m "Emergency fix"
```

**Note**: Only use `--no-verify` when absolutely necessary!

## Customization

Edit `scripts/validate_docs.py` to modify validation rules.
