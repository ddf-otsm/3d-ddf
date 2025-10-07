from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Any

try:
    import bpy  # type: ignore
except Exception:  # pragma: no cover - in test env this is mocked
    bpy = None  # type: ignore


def _detect_project_root() -> Path:
    start = Path(__file__).resolve()
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT: Path = Path(os.environ.get("PROJECT_ROOT", str(_detect_project_root())))


def analyze_current_explosions() -> Dict[str, List[str]]:
    """Analyze current explosion-related objects and materials in the scene.

    Returns a dictionary with lists of issues and recommendations.
    The function is intentionally conservative to work with mocked bpy in tests.
    """
    issues: List[str] = []
    recommendations: List[str] = []

    if bpy is None or not hasattr(bpy, "data"):
        issues.append("Blender API (bpy) not available")
        recommendations.append("Run inside Blender's Python or provide a mock bpy module")
        return {"issues": issues, "recommendations": recommendations}

    # Basic scene scan
    scene_objects = getattr(getattr(bpy, "data", object()), "objects", [])
    for obj in list(scene_objects) if hasattr(scene_objects, "__iter__") else []:
        name = getattr(obj, "name", "")
        if "Explosion" in name or name.startswith("Explosion_"):
            # Check for common realism pitfalls
            if not getattr(obj, "particle_systems", []):
                issues.append(f"{name}: missing particle system")
                recommendations.append("Add particle system with NEWTON physics and increased count")

    # Material checks (very shallow, designed to work with mocks)
    materials = getattr(getattr(bpy, "data", object()), "materials", [])
    for mat in list(materials) if hasattr(materials, "__iter__") else []:
        mat_name = getattr(mat, "name", "")
        if any(keyword in mat_name for keyword in ("Fire", "Smoke", "Debris")):
            if not getattr(mat, "use_nodes", False):
                issues.append(f"{mat_name}: nodes disabled")
                recommendations.append("Enable use_nodes and add emission/volume shaders as needed")

    return {"issues": issues, "recommendations": recommendations}


def _print_report(report: Dict[str, List[str]]) -> None:
    width = 80
    print("=" * width)
    print("Explosion Realism Analysis Report".center(width))
    print("=" * width)
    print("Issues:")
    for item in report.get("issues", []):
        print(f" - {item}")
    print("\nRecommendations:")
    for item in report.get("recommendations", []):
        print(f" - {item}")


if __name__ == "__main__":
    result = analyze_current_explosions()
    _print_report(result)
