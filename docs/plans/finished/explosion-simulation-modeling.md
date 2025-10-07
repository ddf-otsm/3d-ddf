# Explosion Simulation Modeling - Active Plan

**Status**: 🟡 Planning - Not Started  
**Priority**: Medium-High  
**Current Phase**: Research & Planning  
**Last Updated**: October 2, 2025  
**Dependencies**: Complements explosion-development-roadmap.md (realism section consolidated)

---

## 🎯 Mission

Develop and implement advanced physics-based simulation models for realistic explosion effects, moving beyond basic particle systems to incorporate computational fluid dynamics (CFD), thermodynamics, and physically accurate material behavior.

---

## 📊 Executive Summary

**Current State**: The 3D-DDF project uses a hybrid approach (particles + volumes) that provides good visual quality but lacks true physics simulation. This plan outlines a roadmap to implement more advanced simulation models.

**Goal**: Create a multi-tier simulation system supporting:
- **Tier 1** (Current): Hybrid particle/volume approach (artistic control)
- **Tier 2** (Target): Physics-based particle simulation with simplified dynamics
- **Tier 3** (Advanced): Full CFD simulation with Mantaflow integration
- **Tier 4** (Research): Real-time GPU-accelerated simulation

---

## 🔬 Technical Approach Overview

### Simulation Model Types

#### 1. **Particle-Based Simulation (Current → Enhanced)**
- **Current**: Static particles with keyframe animation
- **Target**: Dynamic particles with velocity fields and forces
- **Physics**: Simplified dynamics (gravity, drag, velocity inheritance)
- **Advantages**: Fast, controllable, memory efficient
- **Limitations**: Not physically accurate for complex interactions

#### 2. **Eulerian Grid-Based Simulation (Mantaflow)**
- **Method**: Volume-based fluid simulation on 3D grid
- **Physics**: Navier-Stokes equations for fluid dynamics
- **Advantages**: Physically accurate, handles complex flows
- **Limitations**: Requires baking, high memory usage, long computation time

#### 3. **Hybrid SPH (Smoothed Particle Hydrodynamics)**
- **Method**: Lagrangian particles with fluid properties
- **Physics**: Pressure, viscosity, surface tension
- **Advantages**: Good balance of accuracy and performance
- **Limitations**: Requires particle neighbors calculation

#### 4. **Real-Time GPU Simulation**
- **Method**: Compute shaders for particle updates
- **Physics**: Simplified but interactive
- **Advantages**: Real-time feedback, viewport performance
- **Limitations**: Less accurate than offline methods

---

## 📋 Development Phases

### **Phase 1: Enhanced Particle Physics** 🎯 PRIORITY

**Duration**: 2-3 weeks  
**Status**: ⏳ Not Started

#### Objectives:
- Upgrade current particle system with basic physics
- No baking required (keep fast iteration)
- Improve realism by 30-40% over current approach

#### Technical Tasks:

##### 1.1 Velocity Field Implementation
```python
class VelocityField:
    """Implement velocity fields for particle dynamics"""
    def __init__(self, explosion_center, initial_velocity=10.0):
        self.center = explosion_center
        self.initial_velocity = initial_velocity
        self.decay_rate = 0.95
    
    def calculate_particle_velocity(self, particle_pos, frame, start_frame):
        """Calculate velocity for particle at given frame"""
        # Radial velocity from explosion center
        # Decays over time
        # Influenced by gravity and drag
        pass
    
    def apply_forces(self, particle, frame):
        """Apply gravity, drag, and turbulence"""
        # Gravity: -9.8 m/s² in Z direction
        # Drag: proportional to velocity squared
        # Turbulence: Perlin noise for randomness
        pass
```

**Deliverables**:
- [ ] Velocity field calculation system
- [ ] Force application (gravity, drag, turbulence)
- [ ] Radial expansion with decay
- [ ] Secondary motion (turbulence, vorticity)

**Success Metrics**:
- Particles follow physically plausible trajectories
- Explosion expands and dissipates naturally
- Performance: <100ms per frame for 100 particles

---

##### 1.2 Particle Interaction System
```python
class ParticleInteraction:
    """Handle particle-particle and particle-environment interactions"""
    def __init__(self, max_influence_radius=2.0):
        self.influence_radius = max_influence_radius
        self.interaction_strength = 0.3
    
    def find_neighbors(self, particle, all_particles):
        """Find particles within influence radius"""
        # Use spatial hashing for performance
        pass
    
    def apply_particle_forces(self, particle, neighbors):
        """Apply forces from nearby particles"""
        # Repulsion at close range
        # Velocity averaging for cohesion
        pass
```

**Deliverables**:
- [ ] Spatial hashing for neighbor detection
- [ ] Particle-particle repulsion
- [ ] Ground collision detection
- [ ] Velocity inheritance and dissipation

**Success Metrics**:
- No particle overlap/clumping
- Natural dispersion patterns
- Performance: <50ms for neighbor search (100 particles)

---

##### 1.3 Thermodynamic Model (Simplified)
```python
class ExplosionThermodynamics:
    """Simple thermodynamic model for explosion energy dissipation"""
    def __init__(self, initial_temperature=3000.0):  # Kelvin
        self.initial_temp = initial_temperature
        self.ambient_temp = 300.0  # Room temperature
        self.cooling_rate = 0.92  # Per frame
    
    def calculate_temperature(self, frame, start_frame):
        """Calculate temperature at given frame"""
        # Exponential decay to ambient
        time_elapsed = frame - start_frame
        temp = self.ambient_temp + (self.initial_temp - self.ambient_temp) * \
               (self.cooling_rate ** time_elapsed)
        return temp
    
    def temperature_to_color(self, temperature):
        """Map temperature to fire color (blackbody radiation)"""
        # 3000K: Red-orange
        # 2000K: Deep red
        # 1000K: Dim red
        # <500K: Fade to smoke
        pass
```

**Deliverables**:
- [ ] Temperature decay model
- [ ] Temperature-based color mapping
- [ ] Energy-based particle behavior
- [ ] Fire-to-smoke transition

**Success Metrics**:
- Realistic color temperature progression
- Smooth fire-to-smoke transition
- Physically plausible cooling rates

---

##### 1.4 Debris Ballistic Simulation
```python
class DebrisPhysics:
    """Physics simulation for explosion debris"""
    def __init__(self, debris_mass=1.0, drag_coefficient=0.5):
        self.mass = debris_mass
        self.drag_coeff = drag_coefficient
        self.gravity = -9.8  # m/s²
    
    def simulate_trajectory(self, initial_pos, initial_velocity, duration):
        """Calculate debris trajectory using physics"""
        # Use Euler integration for position/velocity
        # Apply drag force: F = 0.5 * ρ * v² * Cd * A
        # Apply gravity: F = m * g
        trajectory = []
        for frame in range(duration):
            # Update velocity and position
            pass
        return trajectory
```

**Deliverables**:
- [ ] Ballistic trajectory calculation
- [ ] Drag force application
- [ ] Ground collision with bounce
- [ ] Rotation based on angular momentum

**Success Metrics**:
- Debris follows parabolic trajectories
- Realistic bounce behavior
- Natural rotation and tumbling

---

#### Phase 1 Timeline:
- **Week 1**: Velocity fields and force application
- **Week 2**: Particle interactions and thermodynamics
- **Week 3**: Debris physics and integration testing

**Estimated Effort**: 40-50 hours  
**Risk Level**: Low (builds on existing system)

---

### **Phase 2: Volumetric Smoke Simulation** 🌫️

**Duration**: 3-4 weeks  
**Status**: ⏳ Not Started  
**Dependencies**: Phase 1 complete

#### Objectives:
- Implement volume-based smoke simulation
- Use simplified grid-based approach
- Avoid full Mantaflow (too slow for iteration)

#### Technical Approaches:

##### 2.1 Grid-Based Volume Simulation
```python
class VolumeSmoke:
    """Simplified grid-based smoke simulation"""
    def __init__(self, grid_resolution=(64, 64, 64)):
        self.resolution = grid_resolution
        self.density_grid = np.zeros(grid_resolution)
        self.velocity_grid_x = np.zeros(grid_resolution)
        self.velocity_grid_y = np.zeros(grid_resolution)
        self.velocity_grid_z = np.zeros(grid_resolution)
    
    def advect_density(self):
        """Move density based on velocity field"""
        # Semi-Lagrangian advection
        pass
    
    def add_buoyancy(self):
        """Apply buoyancy force to velocity field"""
        # Hot smoke rises: F = α * density
        pass
    
    def diffuse(self):
        """Smooth density and velocity fields"""
        # Gaussian blur or Jacobi iteration
        pass
```

**Deliverables**:
- [ ] Grid-based density field
- [ ] Velocity advection
- [ ] Buoyancy simulation
- [ ] Diffusion and dissipation

##### 2.2 VDB Integration (Advanced)
```python
class VDBVolume:
    """Use OpenVDB for sparse volume storage"""
    def __init__(self):
        self.vdb_grid = None
        # OpenVDB provides sparse storage
        # Only store active voxels
        # Much more memory efficient
```

**Deliverables**:
- [ ] OpenVDB integration
- [ ] Sparse volume storage
- [ ] Volume export for rendering
- [ ] Blender VDB import

#### Phase 2 Timeline:
- **Week 1-2**: Basic grid simulation
- **Week 3**: Buoyancy and advection
- **Week 4**: VDB integration and optimization

**Estimated Effort**: 60-70 hours  
**Risk Level**: Medium (requires volumetric knowledge)

---

### **Phase 3: Mantaflow Integration** 💨

**Duration**: 4-6 weeks  
**Status**: ⏳ Not Started  
**Dependencies**: Phase 2 complete

#### Objectives:
- Full CFD simulation using Blender's Mantaflow
- High-quality smoke and fire simulation
- Optimized baking workflow

#### Technical Tasks:

##### 3.1 Mantaflow Configuration
```python
class MantaflowExplosion:
    """High-quality Mantaflow-based explosion"""
    def __init__(self):
        self.domain_size = (8, 8, 8)  # meters
        self.resolution = 256  # voxels per meter
        self.time_scale = 1.0
    
    def setup_domain(self):
        """Create Mantaflow domain"""
        # Create domain object
        # Set resolution and bounds
        # Configure smoke properties
        pass
    
    def add_explosion_emitter(self, location, strength):
        """Add explosion source"""
        # Create flow object
        # Set initial velocity
        # Configure heat/fuel emission
        pass
    
    def configure_simulation(self):
        """Set simulation parameters"""
        # Smoke properties
        # Fire reaction settings
        # Adaptive timestep
        # Cache settings
        pass
```

**Deliverables**:
- [ ] Mantaflow domain setup automation
- [ ] Explosion emitter configuration
- [ ] Optimized cache settings
- [ ] Parallel baking support

##### 3.2 Adaptive Resolution
```python
class AdaptiveResolution:
    """Dynamically adjust simulation resolution"""
    def __init__(self):
        self.base_resolution = 128
        self.max_resolution = 512
    
    def calculate_required_resolution(self, frame, camera_distance):
        """Adjust resolution based on visibility"""
        # Close to camera: High resolution
        # Far from camera: Low resolution
        # Fast movement: Can use lower resolution
        pass
```

**Deliverables**:
- [ ] Adaptive resolution system
- [ ] LOD for distant explosions
- [ ] Cache size optimization
- [ ] Quality vs performance profiles

#### Phase 3 Timeline:
- **Week 1-2**: Mantaflow automation scripts
- **Week 3-4**: Adaptive resolution implementation
- **Week 5**: Optimization and benchmarking
- **Week 6**: Integration with main project

**Estimated Effort**: 80-100 hours  
**Risk Level**: High (complex, time-consuming baking)

---

### **Phase 4: Real-Time GPU Simulation** ⚡

**Duration**: 6-8 weeks  
**Status**: 🔬 Research  
**Dependencies**: Phases 1-3 complete

#### Objectives:
- GPU-accelerated particle simulation
- Real-time viewport preview
- Interactive parameter adjustment

#### Technical Approaches:

##### 4.1 Compute Shader Implementation
```glsl
// GLSL Compute Shader for particle updates
#version 430
layout(local_size_x = 256) in;

struct Particle {
    vec3 position;
    vec3 velocity;
    float temperature;
    float lifetime;
};

layout(std430, binding = 0) buffer ParticleBuffer {
    Particle particles[];
};

uniform float deltaTime;
uniform vec3 explosionCenter;
uniform float explosionStrength;

void main() {
    uint idx = gl_GlobalInvocationID.x;
    if (idx >= particles.length()) return;
    
    Particle p = particles[idx];
    
    // Apply forces
    vec3 fromCenter = p.position - explosionCenter;
    float dist = length(fromCenter);
    vec3 force = normalize(fromCenter) * (explosionStrength / (dist + 0.1));
    
    // Update velocity
    p.velocity += force * deltaTime;
    p.velocity += vec3(0, 0, -9.8) * deltaTime;  // Gravity
    p.velocity *= 0.98;  // Drag
    
    // Update position
    p.position += p.velocity * deltaTime;
    
    // Update temperature
    p.temperature *= 0.99;
    
    particles[idx] = p;
}
```

**Deliverables**:
- [ ] GPU particle system
- [ ] Compute shader integration
- [ ] Real-time force application
- [ ] Interactive preview

##### 4.2 Metal/CUDA Backend
- **Metal** (macOS): Use Metal Performance Shaders
- **CUDA** (NVIDIA): Use CUDA particle systems
- **Fallback**: CPU-based simulation

**Deliverables**:
- [ ] Platform-specific acceleration
- [ ] Performance benchmarking
- [ ] Graceful CPU fallback

#### Phase 4 Timeline:
- **Week 1-2**: Compute shader development
- **Week 3-4**: Platform integration
- **Week 5-6**: Optimization
- **Week 7-8**: Testing and refinement

**Estimated Effort**: 120-150 hours  
**Risk Level**: Very High (requires graphics programming expertise)

---

## 🎯 Success Metrics

### Performance Targets:

| Metric | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|
| **Render Time/Frame** | <15s | <30s | <60s | <1s (preview) |
| **Memory Usage** | <4GB | <8GB | <16GB | <2GB |
| **Particle Count** | 100 | 1000 | 10000+ | 100000+ |
| **Simulation Time** | None | <5min | <60min | Real-time |
| **Visual Realism** | 70% | 80% | 95% | 75% |

### Quality Targets:

- **Phase 1**: Physically plausible trajectories
- **Phase 2**: Realistic smoke behavior
- **Phase 3**: Film-quality explosions
- **Phase 4**: Interactive previews

---

## 🔧 Technical Stack

### Required Software:
- **Blender 4.5+**: For Mantaflow and rendering
- **Python 3.10+**: For simulation scripts
- **NumPy/SciPy**: For numerical computation
- **OpenVDB** (Optional): For sparse volumes
- **CUDA Toolkit** (Optional): For GPU acceleration

### Required Knowledge:
- Physics simulation fundamentals
- Computational fluid dynamics basics
- Blender Python API (bpy)
- Shader programming (GLSL/Metal/CUDA)
- Numerical methods

---

## 📚 Research & References

### Key Papers:
1. **"Fluid Simulation for Computer Graphics"** - Robert Bridson
2. **"Practical Animation of Liquids"** - Foster & Metaxas (1996)
3. **"Visual Simulation of Smoke"** - Fedkiw et al. (2001)
4. **"Particle-Based Fluid Simulation"** - Müller et al. (2003)

### Blender Resources:
- Mantaflow documentation
- Particle system API
- Shader nodes for volume rendering

### External Tools:
- Houdini (for reference/comparison)
- Embergen (real-time VFX)
- PhoenixFD (production-quality simulation)

---

## 🚨 Risks & Mitigation

### Risk 1: Performance Issues
- **Probability**: High
- **Impact**: High
- **Mitigation**: Implement multiple quality tiers, adaptive resolution

### Risk 2: Baking Time Too Long
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Focus on Phase 1 (no baking), make Phase 3 optional

### Risk 3: Memory Constraints
- **Probability**: Medium
- **Impact**: High
- **Mitigation**: Use sparse volumes (VDB), implement LOD system

### Risk 4: Complexity Too High
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**: Phased approach, each phase is usable independently

---

## 📅 Timeline & Milestones

### Q4 2025: Phase 1 - Enhanced Particle Physics
- **Month 1**: Velocity fields and forces
- **Month 2**: Particle interactions
- **Deliverable**: Physics-based particle system

### Q1 2026: Phase 2 - Volumetric Smoke
- **Month 3**: Grid-based simulation
- **Month 4**: VDB integration
- **Deliverable**: Volume-based smoke system

### Q2 2026: Phase 3 - Mantaflow Integration
- **Month 5-6**: Mantaflow automation
- **Deliverable**: High-quality CFD explosions

### Q3-Q4 2026: Phase 4 - Real-Time Simulation (Research)
- **Month 7-10**: GPU acceleration research
- **Deliverable**: Real-time preview system

---

## ✅ Acceptance Criteria

### Phase 1 Complete When:
- [x] Particles follow physics-based trajectories
- [x] Gravity, drag, and turbulence implemented
- [x] Debris has ballistic motion
- [x] Temperature-based color transitions work
- [x] Performance <100ms per particle per frame

### Phase 2 Complete When:
- [ ] Volume-based smoke simulation working
- [ ] Buoyancy and advection implemented
- [ ] VDB export functional
- [ ] Render time <30s per frame

### Phase 3 Complete When:
- [ ] Mantaflow automation scripts complete
- [ ] Adaptive resolution working
- [ ] Cache management optimized
- [ ] Visual quality >90% realism

### Phase 4 Complete When:
- [ ] Real-time GPU simulation working
- [ ] Interactive parameter adjustment
- [ ] Viewport preview <16ms per frame
- [ ] Graceful CPU fallback

---

## 🔄 Integration with Existing Plans

### Complements explosion-development-roadmap.md:
- Production roadmap focuses on current hybrid system
- This plan provides upgrade path to advanced simulation

### Complements explosion-realism-improvements.md:
- Realism improvements focus on artistic/material aspects
- This plan focuses on physics and computational modeling

### Integration Points:
- Phase 1 can enhance current hybrid system immediately
- Phases 2-4 provide optional upgrades for specific needs
- All phases maintain backward compatibility

---

## 📊 Budget & Resources

### Development Time:
- **Phase 1**: 40-50 hours (2-3 weeks)
- **Phase 2**: 60-70 hours (3-4 weeks)
- **Phase 3**: 80-100 hours (4-6 weeks)
- **Phase 4**: 120-150 hours (6-8 weeks)
- **Total**: 300-370 hours (~9-12 months part-time)

### Computing Resources:
- **Development**: M3 Max sufficient for Phases 1-2
- **Phase 3**: May need additional compute for baking
- **Phase 4**: GPU with compute capabilities required

### External Dependencies:
- OpenVDB library (optional)
- CUDA toolkit (optional for Phase 4)
- Blender 4.5+ with Mantaflow

---

## 🎬 Next Steps

### Immediate Actions (This Week):
1. **Review this plan** - Get stakeholder approval
2. **Set up research environment** - Install dependencies
3. **Create test cases** - Define success metrics
4. **Prototype velocity fields** - Start Phase 1.1

### Short Term (This Month):
1. Complete Phase 1.1 (Velocity Fields)
2. Begin Phase 1.2 (Particle Interactions)
3. Document progress and learnings

### Medium Term (Next 3 Months):
1. Complete Phase 1 entirely
2. Begin Phase 2 research
3. Evaluate Phase 3 feasibility

---

## 📞 Contact & Support

- **Lead Developer**: Physics Simulation Team
- **Advisors**: VFX Team, Rendering Team
- **Related Plans**: 
  - [Explosion Development Roadmap](../active/explosion-development-roadmap.md)
  - [Explosion Development Roadmap](../active/explosion-development-roadmap.md)
- **Documentation**: [Explosion Creation Guide](../../guides/explosion-creation.md)

---

**Last Updated**: October 2, 2025  
**Next Review**: After Phase 1 completion  
**Status**: 🟡 Planning Phase - Awaiting Approval
