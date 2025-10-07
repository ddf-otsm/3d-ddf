# Archived Geometry Test Files

**Archived on**: 2025-10-06 19:04  
**Reason**: These files used simple geometry, not real particle systems

## Files Archived

All these files attempted to create explosions using geometry with emission shaders:
- `ultra_realistic_explosion_refined.blend` - Most developed version
- `hybrid_quick_test.blend` - Minimal test setup
- `explosion_test_scene.blend` - Early test
- `realistic_explosion_test.blend` - Iteration
- `ultra_realistic_explosion*.blend` - Various attempts

## Why This Approach Failed

❌ Geometry-based explosions don't look realistic  
❌ No volumetric fire/smoke simulation  
❌ No proper physics or turbulence  
❌ Static appearance, not dynamic  

## New Approach

See `../active/particle_explosion_v1.blend` for the fresh start with:
- Quick Smoke particle emitter
- Fire + Smoke domain with proper settings
- Volumetric rendering
- Realistic physics simulation
- Optimized for production rendering
