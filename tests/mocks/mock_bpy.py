"""Mock Blender Python API (bpy) for testing without Blender."""
from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock


class MockVector:
    """Mock for mathutils.Vector."""
    def __init__(self, coords=(0, 0, 0)):
        self.x, self.y, self.z = coords[:3] if len(coords) >= 3 else (*coords, *[0]*(3-len(coords)))

    def __add__(self, other):
        if isinstance(other, MockVector):
            return MockVector((self.x + other.x, self.y + other.y, self.z + other.z))
        return MockVector((self.x + other[0] if len(other) > 0 else 0,
                           self.y + other[1] if len(other) > 1 else 0,
                           self.z + other[2] if len(other) > 2 else 0))

    def __repr__(self):
        return f"Vector(({self.x}, {self.y}, {self.z}))"


class MockColor:
    """Mock for mathutils.Color."""
    def __init__(self, rgb=(1, 1, 1)):
        self.r, self.g, self.b = rgb[:3] if len(rgb) >= 3 else (*rgb, *[1]*(3-len(rgb)))
    
    def __repr__(self):
        return f"Color(({self.r}, {self.g}, {self.b}))"


class MockColorRampElement:
    """Mock for color ramp element."""
    def __init__(self):
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.position = 0.0


class MockColorRamp:
    """Mock for color ramp."""
    def __init__(self):
        self.elements = [MockColorRampElement(), MockColorRampElement()]
        
    def new(self, position):
        elem = MockColorRampElement()
        elem.position = position
        self.elements.append(elem)
        return elem


class MockNodeInputs:
    """Mock for node inputs that supports subscriptable access."""
    def __init__(self):
        self._inputs = {}

    def __getitem__(self, key):
        if key not in self._inputs:
            self._inputs[key] = MagicMock()
            self._inputs[key].default_value = 1.0
        return self._inputs[key]

    def __setitem__(self, key, value):
        self._inputs[key] = value


class MockNode:
    """Mock for shader node."""
    def __init__(self, node_type=""):
        self.type = node_type
        self.name = node_type
        self.location = (0, 0)
        self.inputs = MockNodeInputs()
        self.outputs = MagicMock()
        # For color ramp nodes
        self.color_ramp = MockColorRamp()
        # For emission nodes
        self.strength = 1.0
        # For mapping nodes
        self.vector_type = 'POINT'
        # For texture coordinate nodes
        self.object = MagicMock()

    def __repr__(self):
        return f"<MockNode '{self.type}'>"


class MockNodeTree:
    """Mock for node tree."""
    def __init__(self):
        self.nodes = MockNodeCollection()
        self.links = MockLinkCollection()


class MockNodeCollection:
    """Mock for node collection."""
    def __init__(self):
        self._nodes = []
        
    def new(self, node_type):
        node = MockNode(node_type)
        self._nodes.append(node)
        return node
    
    def clear(self):
        self._nodes.clear()
    
    def __iter__(self):
        return iter(self._nodes)
    
    def __len__(self):
        return len(self._nodes)


class MockLinkCollection:
    """Mock for node link collection."""
    def __init__(self):
        self._links = []
    
    def new(self, from_socket, to_socket):
        link = MagicMock()
        link.from_socket = from_socket
        link.to_socket = to_socket
        self._links.append(link)
        return link
    
    def __iter__(self):
        return iter(self._links)


class MockParticleSystem:
    """Mock for particle system."""
    def __init__(self):
        self.settings = MagicMock()
        self.settings.count = 100
        self.settings.lifetime = 50
        self.settings.physics_type = 'NEWTON'
        self.settings.normal_factor = 1.0
        self.settings.tangent_factor = 0.0


class MockParticleSystems:
    """Mock for particle systems collection."""
    def __init__(self):
        self._systems = []

    def new(self, name="ParticleSystem"):
        system = MockParticleSystem()
        self._systems.append(system)
        return system

    def __getitem__(self, index):
        if isinstance(index, int):
            if 0 <= index < len(self._systems):
                return self._systems[index]
            elif index == 0 and len(self._systems) == 0:
                # Return a default particle system if none exist
                ps = MockParticleSystem()
                self._systems.append(ps)
                return ps
        raise IndexError("Particle system index out of range")


class MockObject:
    """Mock for bpy.types.Object."""
    def __init__(self, name="Object"):
        self.name = name
        self.type = "MESH"
        self.location = MockVector()
        self.rotation_euler = MockVector()
        self.scale = MockVector((1, 1, 1))
        self.data = MagicMock()
        self.modifiers = []
        self.material_slots = []
        self.animation_data = None
        self.particle_systems = MockParticleSystems()
        self.constraints = MockCollection()
        # For lights
        self.data.energy = 10.0
        self.data.color = (1.0, 1.0, 1.0)

    def select_set(self, state):
        """Mock select_set method."""
        pass

    def __getattr__(self, name):
        """Return a mock attribute for any unknown object attributes."""
        return MagicMock()

    def __repr__(self):
        return f"<bpy.types.Object '{self.name}'>"


class MockMesh:
    """Mock for bpy.types.Mesh."""
    def __init__(self, name="Mesh"):
        self.name = name
        self.materials = MockCollection()
        self.materials._object_type = 'MATERIAL'

    def __repr__(self):
        return f"<bpy.types.Mesh '{self.name}'>"


class MockMaterial:
    """Mock for bpy.types.Material."""
    def __init__(self, name="Material"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

    def __repr__(self):
        return f"<bpy.types.Material '{self.name}'>"


class MockCollection:
    """Mock for bpy.types.Collection."""
    def __init__(self):
        self._objects = []

    def __iter__(self):
        return iter(self._objects)

    def __len__(self):
        return len(self._objects)

    def get(self, name, default=None):
        for obj in self._objects:
            if obj.name == name:
                return obj
        return default

    def new(self, name, object_data=None):
        if hasattr(self, '_object_type') and self._object_type == 'MATERIAL':
            # For materials
            obj = MockMaterial(name)
        elif hasattr(self, '_object_type') and self._object_type == 'MESH':
            # For meshes
            obj = MockMesh(name)
        else:
            obj = MockObject(name)
        self._objects.append(obj)
        return obj

    def remove(self, obj, do_unlink=False):
        """Remove object with optional do_unlink parameter."""
        if obj in self._objects:
            self._objects.remove(obj)

    def __getitem__(self, index):
        """Support indexing for particle systems, etc."""
        if isinstance(index, int) and 0 <= index < len(self._objects):
            return self._objects[index]
        elif isinstance(index, str):
            # Support string keys by name lookup
            for obj in self._objects:
                if hasattr(obj, 'name') and obj.name == index:
                    return obj
            # If not found, create a mock constraint
            mock_constraint = MagicMock()
            mock_constraint.name = index
            return mock_constraint
        raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        """Support item assignment."""
        if isinstance(index, int) and 0 <= index < len(self._objects):
            self._objects[index] = value
        else:
            raise IndexError("Index out of range")


class MockWorld:
    def __init__(self, name="World"):
        self.name = name
        self.use_nodes = True
        self.node_tree = MockNodeTree()

class MockData:
    """Mock for bpy.data."""
    def __init__(self):
        self.objects = MockCollection()
        self.materials = MockCollection()
        self.materials._object_type = 'MATERIAL'
        self.meshes = MockCollection()
        self.meshes._object_type = 'MESH'
        # Ensure meshes.new exists like Blender
        def meshes_new(name):
            mock_mesh = Mock()
            mock_mesh.name = name
            mock_mesh.type = 'MESH'
            return mock_mesh
        self.meshes.new = meshes_new
        self.scenes = MockCollection()
        self.cameras = MockCollection()
        self.lights = MockCollection()
        self.images = MockCollection()
        self.textures = MockCollection()
        self.node_groups = MockCollection()
        # Worlds collection
        self.worlds = MockCollection()
        default_world = MockWorld("World")
        self.worlds._objects.append(default_world)


class MockContext:
    """Mock for bpy.context."""
    def __init__(self):
        self.scene = MagicMock()
        self.scene.frame_start = 1
        self.scene.frame_end = 250
        self.scene.frame_current = 1
        self.scene.render = MagicMock()
        self.scene.render.fps = 24
        self.scene.render.resolution_x = 1920
        self.scene.render.resolution_y = 1080
        self.scene.objects = MockCollection()
        self.scene.camera = MockObject("Camera")
        self.object = None
        # Don't set active_object here so __getattr__ will handle it
        self.selected_objects = []
        self.view_layer = MagicMock()
        # For linking objects - collection should have objects attribute
        self.collection = MagicMock()
        self.collection.objects = MagicMock()
        self.collection.objects.link = MagicMock()

    def __getattr__(self, name):
        """Return a mock attribute for any unknown context attributes."""
        if name == 'active_object':
            # Return a mock object that was presumably just created
            mock_obj = MockObject("Mock_Active_Object")
            return mock_obj
        return MagicMock()


class MockObjectOps:
    """Mock for bpy.ops.object."""
    def __init__(self):
        self.camera_add = MagicMock()
        self.select_all = MagicMock(return_value={'FINISHED'})
        self.delete = MagicMock(return_value={'FINISHED'})
        self.light_add = MagicMock()
        # Particle system add with side effect
        def particle_system_add_side_effect(**kwargs):
            # Add a particle system to the active object
            if self.context.active_object and hasattr(self.context.active_object, 'particle_systems'):
                ps = MockParticleSystem()
                self.context.active_object.particle_systems._systems.append(ps)
            return {'FINISHED'}
        self.particle_system_add = MagicMock(side_effect=particle_system_add_side_effect)
        self.empty_add = MagicMock(return_value={'FINISHED'})
        self.transform_apply = MagicMock(return_value={'FINISHED'})
        self.constraint_add = MagicMock(return_value={'FINISHED'})
        # Additional ops used in tests
        self.mode_set = MagicMock(return_value={'FINISHED'})
        self.origin_set = MagicMock(return_value={'FINISHED'})
        self.shade_smooth = MagicMock(return_value={'FINISHED'})
        self.modifier_add = MagicMock(return_value={'FINISHED'})

    def __getattr__(self, name):
        """Return a mock method for any unknown ops.object methods."""
        return MagicMock(return_value={'FINISHED'})


class MockOps:
    """Mock for bpy.ops."""
    def __init__(self):
        self.mesh = MagicMock()
        self.object = MockObjectOps()
        # Enhanced render ops
        self.render = MagicMock()
        self.render.render = MagicMock(return_value={'FINISHED'})
        self.scene = MagicMock()
        self.node = MagicMock()
        self.material = MagicMock()
        self.transform = MagicMock()

    def camera_add(self, location=(0, 0, 0), **kwargs):
        """Mock camera_add that sets active_object."""
        camera = MockObject("Camera")
        camera.type = "CAMERA"
        camera.location = MockVector(location)
        # Set the active object
        mock_bpy.context.active_object = camera
        return {'FINISHED'}

    def light_add(self, location=(0, 0, 0), **kwargs):
        """Mock light_add that sets active_object."""
        light = MockObject("Light")
        light.type = "LIGHT"
        light.location = MockVector(location)
        # Set the active object
        mock_bpy.context.active_object = light
        return {'FINISHED'}


# Create the mock bpy module
class MockBpy:
    """Mock Blender Python API."""
    def __init__(self):
        self.data = MockData()
        self.context = MockContext()
        self.ops = MockOps()
        self.types = MagicMock()
        self.utils = MagicMock()
        self.props = MagicMock()
        self.app = MagicMock()
        self.app.version = (4, 0, 0)
        self.app.version_string = "4.0.0"

        # Set up ops methods with proper side effects
        def camera_add_side_effect(location=(0, 0, 0), **kwargs):
            camera = MockObject("Camera")
            camera.type = "CAMERA"
            camera.location = MockVector(location)
            self.context.active_object = camera
            # Also add to scene objects
            self.data.objects._objects.append(camera)
            return {'FINISHED'}

        def light_add_side_effect(location=(0, 0, 0), type='POINT', **kwargs):
            light = MockObject("Light")
            light.type = type
            light.location = MockVector(location)
            self.context.active_object = light
            # Also add to scene objects
            self.data.objects._objects.append(light)
            return {'FINISHED'}

        def empty_add_side_effect(location=(0, 0, 0), **kwargs):
            empty = MockObject("Empty")
            empty.type = "EMPTY"
            empty.location = MockVector(location)
            self.context.active_object = empty
            # Also add to scene objects
            self.data.objects._objects.append(empty)
            return {'FINISHED'}

        self.ops.object.camera_add.side_effect = camera_add_side_effect
        self.ops.object.light_add.side_effect = light_add_side_effect
        self.ops.object.empty_add.side_effect = empty_add_side_effect


# Create mock mathutils module
class MockMathutils:
    """Mock for mathutils module."""
    Vector = MockVector
    Color = MockColor
    Matrix = MagicMock
    Euler = MagicMock
    Quaternion = MagicMock


# Singleton instances
mock_bpy = MockBpy()
mock_mathutils = MockMathutils()


def install_mocks():
    """Install mock modules into sys.modules."""
    import sys
    sys.modules['bpy'] = mock_bpy
    sys.modules['mathutils'] = mock_mathutils
    return mock_bpy, mock_mathutils


def uninstall_mocks():
    """Remove mock modules from sys.modules."""
    import sys
    if 'bpy' in sys.modules:
        del sys.modules['bpy']
    if 'mathutils' in sys.modules:
        del sys.modules['mathutils']

