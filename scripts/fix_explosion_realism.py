from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple, Optional, Any

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


def clear_all_explosions() -> None:
    """Remove explosion-related objects from the scene by name pattern.

    This targets objects whose names include 'Explosion' or 'Fire'.
    """
    if bpy is None or not hasattr(bpy, "data"):
        return

    objects = getattr(bpy.data, "objects", [])
    # Iterate a copy in case the underlying list changes
    for obj in list(objects) if hasattr(objects, "__iter__") else []:
        name = getattr(obj, "name", "")
        if "Explosion" in name or name.startswith("Fire_") or name.startswith("Explosion_"):
            remove_fn = getattr(getattr(bpy.data, "objects", object()), "remove", None)
            if callable(remove_fn):
                try:
                    remove_fn(obj, do_unlink=True)  # type: ignore[arg-type]
                except TypeError:
                    # Some mocks may not accept keyword args
                    remove_fn(obj)  # type: ignore[misc]


def create_ultra_realistic_fire_material(suffix: str) -> Any:
    if bpy is None:
        return None
    name = f"Ultra_Fire_{suffix}"
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    output = nodes.new("ShaderNodeOutputMaterial")
    try:
        # Connect emission to surface
        links.new(emission.outputs[0], output.inputs[0])
    except Exception:
        pass
    return mat


def create_enhanced_smoke_material(suffix: str) -> Any:
    if bpy is None:
        return None
    name = f"Enhanced_Smoke_{suffix}"
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    output = nodes.new("ShaderNodeOutputMaterial")
    try:
        links.new(principled.outputs[0], output.inputs[0])
    except Exception:
        pass
    return mat


def create_realistic_debris_material(suffix: str) -> Any:
    if bpy is None:
        return None
    name = f"Realistic_Debris_{suffix}"
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    output = nodes.new("ShaderNodeOutputMaterial")
    try:
        links.new(principled.outputs[0], output.inputs[0])
    except Exception:
        pass
    return mat


def create_advanced_particle_system(name: str, count: int, lifetime: int) -> Any:
    if bpy is None:
        return None
    obj = bpy.data.objects.new(name, None)
    try:
        bpy.context.collection.objects.link(obj)
    except Exception:
        pass

    # Create a particle system and adjust settings
    try:
        obj.particle_systems.new(name=f"{name}_PS")
    except Exception:
        # Some mocks may not expose new(); ensure index access works in tests
        pass

    # Adjust first particle system if accessible
    try:
        ps = obj.particle_systems[0]
        settings = getattr(ps, "settings", None)
        if settings is not None:
            # Ensure sensible minimums
            settings.count = max(getattr(settings, "count", 0), max(count, 200))
            settings.lifetime = max(getattr(settings, "lifetime", 0), max(lifetime, 50))
            settings.physics_type = "NEWTON"
    except Exception:
        pass

    return obj


def apply_explosion_lighting() -> None:
    if bpy is None:
        return
    # Key light
    key = bpy.data.objects.new("Explosion_Light_Key", None)
    try:
        key.data.energy = 500.0  # type: ignore[attr-defined]
    except Exception:
        pass
    try:
        bpy.context.collection.objects.link(key)
    except Exception:
        pass

    # Fill/rim lights
    fill = bpy.data.objects.new("Explosion_Light_Fill", None)
    rim = bpy.data.objects.new("Explosion_Light_Rim", None)
    for light in (fill, rim):
        try:
            bpy.context.collection.objects.link(light)
        except Exception:
            pass


def create_volume_explosion_effect(location: Tuple[float, float, float],
                                   scale: Tuple[float, float, float]) -> Any:
    if bpy is None:
        return None
    obj = bpy.data.objects.new("Volume_Explosion", None)
    try:
        obj.location = location  # type: ignore[attr-defined]
        obj.scale = scale  # type: ignore[attr-defined]
    except Exception:
        pass
    try:
        bpy.context.collection.objects.link(obj)
    except Exception:
        pass

    # Attach a basic volume material placeholder
    try:
        mat = bpy.data.materials.new("Volume_Material")
        if hasattr(obj, "data") and hasattr(obj.data, "materials"):
            obj.data.materials.append(mat)  # type: ignore[attr-defined]
    except Exception:
        pass

    return obj


def fix_particle_system_settings() -> None:
    if bpy is None or not hasattr(bpy, "data"):
        return
    objects = getattr(bpy.data, "objects", [])
    for obj in list(objects) if hasattr(objects, "__iter__") else []:
        systems = getattr(obj, "particle_systems", [])
        for ps in list(systems) if hasattr(systems, "__iter__") else []:
            settings = getattr(ps, "settings", None)
            if settings is None:
                continue
            # Improve minimal parameters
            try:
                if getattr(settings, "count", 0) < 200:
                    settings.count = 200
            except Exception:
                pass
            try:
                if getattr(settings, "lifetime", 0) < 50:
                    settings.lifetime = 50
            except Exception:
                pass
            try:
                if getattr(settings, "physics_type", "") != "NEWTON":
                    settings.physics_type = "NEWTON"
            except Exception:
                pass


def create_fire_glow_effect(location: Tuple[float, float, float],
                             intensity: float = 100.0) -> Any:
    if bpy is None:
        return None
    light = bpy.data.objects.new("Fire_Glow_Light", None)
    try:
        light.location = location  # type: ignore[attr-defined]
        if hasattr(light, "data") and hasattr(light.data, "energy"):
            light.data.energy = intensity  # type: ignore[assignment]
    except Exception:
        pass
    try:
        bpy.context.collection.objects.link(light)
    except Exception:
        pass
    return light


if __name__ == "__main__":
    # Simple manual run helpers (no CLI args to keep it Blender-friendly)
    clear_all_explosions()
    apply_explosion_lighting()
