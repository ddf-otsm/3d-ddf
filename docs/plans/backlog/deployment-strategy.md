# Logo to 3D Service - Deployment Strategy (Backlog)

## 📦 **Future Deployment Strategy**

This deployment strategy has been moved to backlog as the initial implementation will use a local Blender server approach. The following deployment options will be considered for future scaling and production deployment.

### **Development Environment**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src  # Live reload
    environment:
      - ENV=development
      - DEBUG=true
    depends_on:
      - redis
      - postgres

  worker:
    build: .
    command: celery -A src.core.celery worker
    volumes:
      - ./src:/app/src
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: logo3d
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### **Production Deployment Options**

#### **Option 1: Docker Compose (Small Scale)**
- Single server deployment
- Suitable for < 100 requests/hour
- Easy to manage and update
- Cost-effective

#### **Option 2: Kubernetes (Large Scale)**
- Multi-node cluster
- Auto-scaling based on load
- High availability
- Suitable for production with high traffic

```yaml
# k8s deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logo-to-3d-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: logo-to-3d:latest
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### **CI/CD Pipeline**

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -r requirements.txt
          uv pip install -r requirements-dev.txt
      - name: Run linters
        run: |
          ruff check src/
          black --check src/
          mypy src/
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t logo-to-3d:${{ github.sha }} .
      - name: Push to registry
        run: |
          docker tag logo-to-3d:${{ github.sha }} registry.example.com/logo-to-3d:latest
          docker push registry.example.com/logo-to-3d:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - name: Deploy to production
        run: |
          # Trigger deployment (k8s, docker-compose, etc.)
          kubectl set image deployment/logo-to-3d-api api=registry.example.com/logo-to-3d:latest
```

## 🎯 **Current Approach: Local Blender Server**

### **Initial Implementation Strategy**
- **Local Blender Installation**: Use system-installed Blender for development and testing
- **Direct Process Management**: Launch Blender as subprocess with proper isolation
- **File-based Communication**: Use temporary files for input/output between API and Blender
- **Resource Limits**: Implement CPU/memory limits and timeout handling
- **Error Recovery**: Automatic cleanup and process restart on failures

### **Benefits of Local Approach**
- **Faster Development**: No container overhead during development
- **Easier Debugging**: Direct access to Blender process and logs
- **Simpler Deployment**: Single process deployment for initial rollout
- **Resource Efficiency**: Better resource utilization for small-scale usage

### **Migration Path to Containerized Deployment**
1. **Phase 1 (Current)**: Local Blender server with API wrapper
2. **Phase 2**: Docker containerization with volume mounting
3. **Phase 3**: Kubernetes deployment with auto-scaling
4. **Phase 4**: Multi-region deployment with CDN integration

### **Local Blender Server Implementation**

#### **Process Management**
```python
import subprocess
import tempfile
import time
from pathlib import Path

class BlenderServer:
    def __init__(self, blender_executable: str = "blender"):
        self.blender_executable = blender_executable
        self.temp_dir = Path(tempfile.mkdtemp())
        self.process = None

    def process_request(self, script_path: Path, timeout: int = 300) -> dict:
        """Process a Blender script with timeout."""
        try:
            cmd = [
                self.blender_executable,
                "--background",
                "--python", str(script_path)
            ]

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.temp_dir
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = self.process.communicate(timeout=timeout)
                return {
                    "success": self.process.returncode == 0,
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode(),
                    "returncode": self.process.returncode
                }
            except subprocess.TimeoutExpired:
                self.process.kill()
                return {
                    "success": False,
                    "error": "Processing timeout",
                    "timeout": timeout
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            if self.process:
                try:
                    self.process.kill()
                except:
                    pass
```

#### **Script Template System**
```python
# template_processor.py
def generate_blender_script(task_type: str, parameters: dict) -> str:
    """Generate Blender Python script for specific task."""

    if task_type == "text_to_3d":
        return f"""
import bpy
import sys

# Clear scene
bpy.ops.wm.read_homefile(use_empty=True)

# Create text object
bpy.ops.object.text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object

# Set text properties
text_obj.data.body = "{parameters['text']}"
text_obj.data.size = {parameters.get('font_size', 1.0)}

# Convert to mesh and extrude
bpy.ops.object.convert(target='MESH')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={{"value": (0, 0, {parameters.get('depth', 0.1)})}}
)
bpy.ops.object.mode_set(mode='OBJECT')

# Export to requested format
output_path = "{parameters['output_path']}"
format_type = "{parameters.get('format', 'obj')}"

if format_type == "obj":
    bpy.ops.export_scene.obj(
        filepath=output_path,
        use_selection=True,
        use_materials=False
    )
elif format_type == "fbx":
    bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)

print("Script completed successfully")
"""

    # Add more task types as needed
    return ""
```

### **Resource Management**
- **Process Isolation**: Each request runs in separate Blender instance
- **Temporary Files**: Automatic cleanup of intermediate files
- **Memory Limits**: System-level memory constraints
- **CPU Affinity**: Optional CPU core assignment for performance
- **Health Monitoring**: Process health checks and automatic restart

### **Error Handling**
- **Timeout Protection**: Automatic termination of hanging processes
- **Resource Limits**: CPU and memory usage monitoring
- **Cleanup Procedures**: Ensure no orphaned processes or files
- **Logging**: Comprehensive logging for debugging failed requests

### **Future Migration Considerations**
- **API Compatibility**: Design API to work with both local and containerized Blender
- **Configuration**: Environment-based switching between deployment modes
- **Testing**: Ensure same functionality across deployment methods
- **Monitoring**: Unified monitoring regardless of deployment approach

---

**Status**: Backlog - To be implemented after initial local Blender server proof of concept
**Priority**: Medium (Post-MVP)
**Estimated Effort**: 2-3 weeks for basic containerization, 4-6 weeks for full production deployment

