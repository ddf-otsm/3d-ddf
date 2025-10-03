# Logo to 3D Service

Convert company logos and text into professional 3D models using Blender and Python.

## Features

- **Text to 3D**: Generate 3D text using copyleft fonts (Verdana, Arial, Helvetica, etc.)
- **Image to Vector**: Convert logo images to scalable SVG vectors
- **Vector to 3D**: Extrude 2D vectors into 3D models with customizable parameters
- **Advanced Features**: Edge rounding, material assignment, lighting optimization
- **Multiple Formats**: Export to OBJ, STL, FBX, glTF, and more

## Quick Start

### Prerequisites

- Python 3.11+
- Blender 4.2+
- uv package manager

### Installation

```bash
# Clone or navigate to the service directory
cd services/logo-to-3d

# Install dependencies
uv venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Run Proof of Concept

```bash
# Test basic text-to-3D conversion
blender --background --python scripts/poc_text_to_3d.py
```

### Start API Server

```bash
# Start the FastAPI server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Convert Text to 3D

```bash
curl -X POST "http://localhost:8000/api/v1/text-to-3d" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ACME Corp",
    "font": "Liberation Sans",
    "extrude_depth": 0.1,
    "material_preset": "plastic"
  }'
```

### Convert Image to 3D

```bash
curl -X POST "http://localhost:8000/api/v1/image-to-3d" \
  -F "file=@logo.png" \
  -F "extrude_depth=0.1" \
  -F "material_preset=metal"
```

## Supported Fonts

- Liberation Sans/Serif/Mono (GPL)
- DejaVu Sans/Serif/Mono (copyleft)
- Arial, Helvetica, Verdana, Tahoma (system fonts)

## Supported Formats

- **OBJ**: Wavefront OBJ (universal compatibility)
- **STL**: STL (3D printing)
- **FBX**: Autodesk FBX (gaming engines)
- **glTF/GLB**: Khronos glTF (web and modern engines)
- **USD**: Universal Scene Description

## Configuration

Edit `src/core/config.py` or set environment variables:

```bash
export BLENDER_EXECUTABLE="/Applications/Blender.app/Contents/MacOS/Blender"
export REDIS_URL="redis://localhost:6379"
export DATABASE_URL="postgresql://user:pass@localhost/logo3d"
```

## Project Structure

```
services/logo-to-3d/
├── src/
│   ├── core/              # Core utilities and configuration
│   ├── text_processor/    # Text-to-vector conversion
│   ├── image_processor/   # Image-to-vector conversion
│   ├── blender_engine/    # 3D processing with Blender
│   ├── api/               # REST API endpoints
│   └── db/                # Database models
├── fonts/                 # Copyleft font collection
├── presets/              # Material and lighting presets
├── tests/                # Test suite
├── scripts/              # Utility scripts
├── data/                 # Test data and temporary files
├── pyproject.toml        # Project configuration
└── requirements.txt      # Python dependencies
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed and will run on each commit:

- Code formatting (black)
- Linting (ruff)
- Type checking (mypy)
- Trailing whitespace removal

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Deployment

### Docker

```bash
# Build image
docker build -t logo-to-3d .

# Run container
docker run -p 8000:8000 logo-to-3d
```

### Docker Compose

```bash
# Start all services (API, Redis, PostgreSQL)
docker-compose up -d
```

## License

This project uses copyleft fonts and libraries. See individual font licenses in the `fonts/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Full Documentation](../../docs/)
- **Internal Wiki**: Company internal documentation

---

**Version**: 0.1.0
**Status**: Planning → Development
**Next Milestone**: Week 2 - Core Implementation

