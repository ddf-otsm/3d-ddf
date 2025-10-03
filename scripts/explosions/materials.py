"""
Material creation utilities for explosions.
"""

try:
    import bpy
    # Check if it's real Blender, not a mock
    BLENDER_AVAILABLE = (hasattr(bpy, 'data')
                         and hasattr(bpy.data, 'materials')
                         and not isinstance(bpy.data, type(None)))
    # Additional check: real Blender has app module
    if BLENDER_AVAILABLE and hasattr(bpy, 'app'):
        BLENDER_AVAILABLE = True
    elif BLENDER_AVAILABLE:
        # Has data.materials but no app - likely a partial mock, treat as unavailable
        BLENDER_AVAILABLE = hasattr(bpy, 'app')
except ImportError:
    BLENDER_AVAILABLE = False
    # Create a mock bpy module for type checking

    class MockBpy:
        class types:
            class Material:
                pass

        class data:
            class materials:
                @staticmethod
                def new(name):
                    return MockBpy.types.Material()
    bpy = MockBpy()

from typing import Dict, Optional


class ExplosionMaterials:
    """Manager for explosion-related materials."""

    def __init__(self):
        self.materials: Dict[str, bpy.types.Material] = {}

    def create_fire_material(
            self,
            name: str,
            temperature: float = 1.0) -> 'bpy.types.Material':
        """Create a fire material with realistic color gradient."""
        if not BLENDER_AVAILABLE:
            # Return a mock material for testing
            from unittest.mock import Mock
            mock_mat = Mock()
            mock_mat.name = f"Explosion_Fire_{name}"
            mock_mat.use_nodes = True
            self.materials[f"fire_{name}"] = mock_mat
            return mock_mat

        mat = bpy.data.materials.new(name=f"Explosion_Fire_{name}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Output
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (1000, 0)

        # Emission
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (800, 0)
        emission.inputs['Strength'].default_value = 25.0

        # Color ramp with realistic fire colors
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (600, 0)

        # Realistic fire color gradient based on temperature
        if temperature < 0.3:  # Cool fire
            color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
            color_ramp.color_ramp.elements[1].color = (1.0, 0.3, 0.0, 1.0)  # Red-orange
        elif temperature < 0.7:  # Medium fire
            color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
            color_ramp.color_ramp.elements[1].color = (1.0, 0.5, 0.0, 1.0)  # Orange
        else:  # Hot fire
            color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.0, 1.0)  # Red
            color_ramp.color_ramp.elements[1].color = (1.0, 0.8, 0.2, 1.0)  # Yellow

        # Noise for texture
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (400, 0)
        noise.inputs['Scale'].default_value = 15.0

        # Connect nodes
        links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        self.materials[f"fire_{name}"] = mat
        return mat

    def create_smoke_material(
            self,
            name: str,
            density: float = 0.8) -> 'bpy.types.Material':
        """Create a smoke material with volume rendering."""
        if not BLENDER_AVAILABLE:
            # Return a mock material for testing
            from unittest.mock import Mock
            mock_mat = Mock()
            mock_mat.name = f"Explosion_Smoke_{name}"
            mock_mat.use_nodes = True
            self.materials[f"smoke_{name}"] = mock_mat
            return mock_mat

        mat = bpy.data.materials.new(name=f"Explosion_Smoke_{name}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Output
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)

        # Volume principled
        volume = nodes.new('ShaderNodeVolumePrincipled')
        volume.location = (400, 0)
        volume.inputs['Density'].default_value = density
        volume.inputs['Color'].default_value = (0.2, 0.2, 0.2, 1.0)

        # Noise for texture variation
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (200, 0)
        noise.inputs['Scale'].default_value = 8.0

        # Connect nodes
        links.new(noise.outputs['Fac'], volume.inputs['Density'])
        links.new(volume.outputs['Volume'], output.inputs['Volume'])

        self.materials[f"smoke_{name}"] = mat
        return mat

    def create_debris_material(self, name: str) -> 'bpy.types.Material':
        """Create a debris material for explosion fragments."""
        if not BLENDER_AVAILABLE:
            # Return a mock material for testing
            from unittest.mock import Mock
            mock_mat = Mock()
            mock_mat.name = f"Explosion_Debris_{name}"
            mock_mat.use_nodes = True
            self.materials[f"debris_{name}"] = mock_mat
            return mock_mat

        mat = bpy.data.materials.new(name=f"Explosion_Debris_{name}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Output
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)

        # Principled BSDF
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.location = (400, 0)
        principled.inputs['Base Color'].default_value = (
            0.3, 0.25, 0.2, 1.0)  # Brownish
        principled.inputs['Roughness'].default_value = 0.8
        principled.inputs['Metallic'].default_value = 0.1

        # Noise for surface variation
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (200, 0)
        noise.inputs['Scale'].default_value = 5.0

        # Connect nodes
        links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        self.materials[f"debris_{name}"] = mat
        return mat

    def get_material(
            self,
            material_type: str,
            name: str) -> Optional['bpy.types.Material']:
        """Get a cached material or create a new one."""
        key = f"{material_type}_{name}"
        if key in self.materials:
            return self.materials[key]

        # Create new material based on type
        if material_type == "fire":
            return self.create_fire_material(name)
        elif material_type == "smoke":
            return self.create_smoke_material(name)
        elif material_type == "debris":
            return self.create_debris_material(name)

        return None

    def cleanup_unused_materials(self):
        """Remove materials that aren't linked to any objects."""
        if not BLENDER_AVAILABLE:
            # Can't cleanup without Blender
            return

        used_materials = set()
        for obj in bpy.data.objects:
            if obj.material_slots:
                for slot in obj.material_slots:
                    if slot.material:
                        used_materials.add(slot.material.name)

        # Remove unused explosion materials
        for mat_name in list(self.materials.keys()):
            if mat_name not in used_materials:
                bpy.data.materials.remove(self.materials[mat_name])
                del self.materials[mat_name]
