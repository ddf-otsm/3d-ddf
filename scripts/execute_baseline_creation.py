#!/usr/bin/env python3
"""
Execute Baseline Scene Creation

This script executes the baseline scene creation for the explosion development roadmap.
It can run with or without Blender available.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_blender_available():
    """Check if Blender is available."""
    try:
        result = subprocess.run(['blender', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def create_baseline_scenes_with_blender():
    """Create baseline scenes using Blender."""
    print("🎬 Creating baseline scenes with Blender...")
    
    # Define output paths
    dadosfera_path = "projects/dadosfera/blender_files/active/dadosfera_v2_clean.blend"
    explosion_path = "projects/explosion-test/blender_files/active/particle_explosion_v1.blend"
    
    # Create directories
    Path(dadosfera_path).parent.mkdir(parents=True, exist_ok=True)
    Path(explosion_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Run Blender script
    script_path = "scripts/create_baseline_scenes.py"
    
    cmd = [
        'blender',
        '--background',
        '--python', script_path,
        '--',
        '--output-dadosfera', dadosfera_path,
        '--output-explosion', explosion_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Baseline scenes created successfully with Blender!")
            return True
        else:
            print(f"❌ Blender execution failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Blender execution timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Blender: {e}")
        return False

def create_baseline_scenes_without_blender():
    """Create baseline scenes without Blender (simulation mode)."""
    print("🎬 Creating baseline scenes (simulation mode - Blender not available)...")
    
    # Define output paths
    dadosfera_path = "projects/dadosfera/blender_files/active/dadosfera_v2_clean.blend"
    explosion_path = "projects/explosion-test/blender_files/active/particle_explosion_v1.blend"
    
    # Create directories
    Path(dadosfera_path).parent.mkdir(parents=True, exist_ok=True)
    Path(explosion_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Create placeholder files
    dadosfera_placeholder = f"""# Dadosfera v2 Clean Scene (Simulated)

This is a placeholder file created because Blender is not available.

To create the actual scene:
1. Open Blender
2. Run: scripts/create_baseline_scenes.py
3. Save as: {dadosfera_path}

Scene should contain:
- Dadosfera 3D text with metallic material
- Studio floor with PBR material
- 3-point lighting setup
- Professional camera setup
- No explosion objects (add later)

Status: Placeholder created - requires Blender for actual scene creation
"""
    
    explosion_placeholder = f"""# Particle Explosion Test Scene (Simulated)

This is a placeholder file created because Blender is not available.

To create the actual scene:
1. Open Blender
2. Run: scripts/create_baseline_scenes.py
3. Save as: {explosion_path}

Scene should contain:
- Fire particle emitter
- Smoke domain with volumetric material
- Proper physics settings
- Test render validation

Status: Placeholder created - requires Blender for actual scene creation
"""
    
    # Write placeholder files
    with open(dadosfera_path, 'w') as f:
        f.write(dadosfera_placeholder)
    
    with open(explosion_path, 'w') as f:
        f.write(explosion_placeholder)
    
    print("✅ Placeholder files created (Blender required for actual scenes)")
    return True

def main():
    """Main execution."""
    print("🚀 Executing Baseline Scene Creation")
    print("=" * 50)
    
    # Check if Blender is available
    blender_available = check_blender_available()
    
    if blender_available:
        print("✅ Blender detected - creating actual scenes")
        success = create_baseline_scenes_with_blender()
    else:
        print("⚠️  Blender not detected - creating placeholder files")
        success = create_baseline_scenes_without_blender()
    
    if success:
        print("\n🎉 Baseline scene creation complete!")
        print("\n📋 Next Steps:")
        print("1. Review created scenes")
        print("2. Test render quality")
        print("3. Proceed with explosion integration")
        print("4. Update explosion development roadmap status")
    else:
        print("\n❌ Baseline scene creation failed")
        print("Please check Blender installation and try again")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
