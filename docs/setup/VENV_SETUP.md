# Virtual Environment Setup

This guide explains how to set up and use the Python virtual environment for the 3D-DDF project.

## Quick Setup (Automated)

```bash
# Run the setup script
./setup_venv.sh
```

This will:
- Create a `venv` directory
- Install all dependencies from `requirements.txt`
- Set up pre-commit hooks
- Prepare your environment for development

## Manual Setup

If you prefer to set up manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install pre-commit hooks
pre-commit install
```

## Using the Virtual Environment

### Activate
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

You'll see `(venv)` in your prompt when activated.

### Deactivate
```bash
deactivate
```

### Run Tests
```bash
# With venv activated
pytest tests/

# Or without activating
./venv/bin/pytest tests/
```

## Dependencies

The project includes:

- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality
- **numpy/pandas**: Data processing (for integrations)
- **requests/beautifulsoup4**: Web scraping (for asset integrations)

See `requirements.txt` for full list.

## Blender Scripts

**Important**: Scripts that use `bpy` (Blender Python) cannot use this venv. They must be run with Blender's Python:

```bash
# Run Blender scripts
blender --background --python scripts/render_service.py

# Or from within Blender's script editor
```

## Troubleshooting

### "python3: command not found"
- Install Python 3.8+ from [python.org](https://python.org)
- macOS: `brew install python3`

### Permission denied on setup_venv.sh
```bash
chmod +x setup_venv.sh
```

### Pre-commit hook failures
```bash
# Update hooks
pre-commit autoupdate

# Run manually
pre-commit run --all-files
```

### Virtual environment not activating
- Check you're in the project root directory
- Try recreating: `rm -rf venv && ./setup_venv.sh`

## Adding New Dependencies

1. Activate venv
2. Install package: `pip install package-name`
3. Update requirements: `pip freeze > requirements.txt`
4. Or manually add to `requirements.txt` with version

## Environment Variables

Configure project paths and Blender executable using environment variables:

```bash
# Copy the example file
cp .env.example .env

# Edit with your paths
# PROJECT_ROOT=/your/path/to/3d-ddf
# BLENDER=/path/to/blender
```

See [`.env.example`](../../.env.example) for all available variables.

## Git Integration

The `venv/` directory is already in `.gitignore` - it won't be committed.

Each developer should create their own venv using `./setup_venv.sh`.
