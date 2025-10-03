# Workflows Directory

This directory contains automation scripts for common 3D-DDF operations.

## `run.sh` - Main Workflow Runner

The `run.sh` script implements all operations defined in the root `Makefile`. It provides detailed implementations for:

- **Setup & Validation**: Environment checks, taxonomy validation, documentation checks
- **Testing**: Unit, integration, explosion, and Blender tests
- **Rendering**: Automated rendering for dadosfera and explosion projects
- **Explosion System**: Explosion creation, analysis, and video generation
- **Video Encoding**: FFmpeg-based video encoding from rendered frames
- **Monitoring**: Render progress monitoring and log viewing
- **Integrations**: 3D asset platform integrations (Phase 1-4)
- **Cleanup**: Cache, logs, and render cleanup utilities
- **Development**: Linting, formatting, git hooks, and MCP updates
- **Project Info**: Status, version, and detailed project information

## Usage

The script is designed to be called via the Makefile:

```bash
# Via Makefile (recommended)
make help                    # Show all available commands
make test                    # Run tests
make render-dadosfera        # Render dadosfera project
make status                  # Show project status

# Direct invocation (advanced)
./workflows/run.sh test
./workflows/run.sh render-dadosfera preview
```

## Script Features

### Color-Coded Output
- 🔵 **Blue** - Information messages
- 🟢 **Green** - Success messages
- 🟡 **Yellow** - Warning messages
- 🔴 **Red** - Error messages

### Error Handling
- Exits on first error (`set -e`)
- Validates file existence before operations
- Checks for required tools (Blender, Python, etc.)

### Background Processing
- Supports background renders with `nohup`
- Provides PID tracking for monitoring
- Logs output to `/tmp` for easy access

### Safety Features
- Confirmation prompts for destructive operations
- Age-based cleanup (7 days for logs, 30 days for renders)
- Preserves recent files automatically

## Configuration

Edit these variables in `run.sh` to customize paths:

```bash
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
PYTHON="python3"
PROJECT_ROOT="..."  # Auto-detected
```

## Examples

### Render Operations
```bash
make render-dadosfera-draft         # Fast draft render
make render-dadosfera-preview       # Preview quality (default)
make render-dadosfera-production    # High quality
make render-dadosfera-final         # Maximum quality
make render-all-preview             # Render both projects
```

### Testing
```bash
make test                  # All tests (excluding Blender)
make test-unit            # Unit tests only
make test-explosion       # Explosion system tests
make test-coverage        # With coverage report
```

### Monitoring
```bash
make status               # Show render status
make logs                 # Show recent logs
make logs-tail            # Tail logs in real-time
make monitor-render       # Monitor render progress
```

### Maintenance
```bash
make clean                # Clean temp files
make clean-logs           # Clean old logs (7+ days)
make clean-cache          # Clean Python cache
make validate             # Run all validations
```

## Integration with CI/CD

The Makefile and workflow scripts are designed for easy CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: make test

- name: Validate project
  run: make validate

- name: Render preview
  run: make render-dadosfera-draft
```

## Troubleshooting

### "Blender not found"
```bash
make check                # Detect Blender installation
python scripts/detect_blender.py
```

### "Permission denied"
```bash
chmod +x workflows/run.sh
```

### Render not starting
1. Check Blender is installed: `make check`
2. Verify blend files exist
3. Check logs: `make logs`

## Development

To add new commands:

1. Add target to `Makefile`
2. Implement function in `run.sh` (e.g., `cmd_new_feature()`)
3. Add case in `main()` function
4. Update this README

## Dependencies

### Required
- **Blender 3.0+** - 3D rendering
- **Python 3.10+** - Scripts and testing
- **FFmpeg** - Video encoding

### Optional
- **pytest** - Testing framework
- **black** - Code formatting
- **ruff/flake8** - Linting
- **pytest-watch** - Watch mode for tests

Install Python dependencies:
```bash
pip install pytest pytest-cov black ruff pytest-watch
```

## License

Part of the 3D-DDF project. See root LICENSE file for details.


