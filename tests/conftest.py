"""Pytest configuration and fixtures for 3D-DDF tests."""
import sys
from pathlib import Path
import pytest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "services" / "logo-to-3d"))

# Install Blender mocks before any tests run
# This allows tests to import bpy without having Blender installed
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    # Install mocks
    from tests.mocks.mock_bpy import install_mocks
    install_mocks()
    # Also mock bmesh
    from unittest.mock import MagicMock
    sys.modules['bmesh'] = MagicMock()


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def blender_available():
    """Check if Blender is available."""
    return BLENDER_AVAILABLE


@pytest.fixture
def mock_bpy():
    """Provide mock bpy module for tests."""
    if BLENDER_AVAILABLE:
        import bpy
        return bpy
    else:
        from tests.mocks.mock_bpy import mock_bpy
        return mock_bpy


@pytest.fixture
def temp_blend_file(tmp_path):
    """Create a temporary .blend file path for testing."""
    return tmp_path / "test_scene.blend"


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "blender: mark test as requiring Blender"
    )
    config.addinivalue_line(
        "markers", "gpu: mark test as requiring GPU"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
