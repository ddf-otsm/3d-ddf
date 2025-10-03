#!/usr/bin/env python3
"""
Phase 1 Setup Script
Sets up the Phase 1 integration environment
"""

import os
import sys
import json
from pathlib import Path

def setup_directories():
    """Create all required directories"""
    print("🔧 Setting up Phase 1 directories...")
    
    # Get the integration directory
    integration_dir = Path(__file__).parent.parent
    assets_dir = integration_dir / "assets"
    
    # Create asset directories
    directories = [
        assets_dir,
        assets_dir / "opengameart",
        assets_dir / "free3d", 
        assets_dir / "imported",
        assets_dir / "exports",
        integration_dir / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    return assets_dir

def setup_configuration():
    """Set up configuration files"""
    print("\n⚙️  Setting up configuration...")
    
    integration_dir = Path(__file__).parent.parent
    config_dir = integration_dir / "config"
    
    # Check if settings.py exists
    settings_file = config_dir / "settings.py"
    if settings_file.exists():
        print(f"  ✅ {settings_file}")
    else:
        print(f"  ❌ {settings_file} - Please create this file")
    
    # Check if platforms.json exists
    platforms_file = config_dir / "platforms.json"
    if platforms_file.exists():
        print(f"  ✅ {platforms_file}")
    else:
        print(f"  ❌ {platforms_file} - Please create this file")
    
    return config_dir

def test_imports():
    """Test that all imports work correctly"""
    print("\n🧪 Testing imports...")
    
    # Add src to path
    integration_dir = Path(__file__).parent.parent
    src_dir = integration_dir / "src"
    sys.path.insert(0, str(src_dir))
    
    try:
        from phase1_asset_importer import Phase1AssetImporter
        print("  ✅ Phase1AssetImporter imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import Phase1AssetImporter: {e}")
        return False
    
    try:
        from blender_mcp_phase1 import Phase1BlenderIntegration
        print("  ✅ Phase1BlenderIntegration imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import Phase1BlenderIntegration: {e}")
        return False
    
    return True

def create_sample_assets():
    """Create sample assets for testing"""
    print("\n📦 Creating sample assets...")
    
    integration_dir = Path(__file__).parent.parent
    assets_dir = integration_dir / "assets"
    
    # Create sample asset files
    sample_assets = [
        ("opengameart", "sample_character.blend"),
        ("opengameart", "sample_weapon.fbx"),
        ("free3d", "sample_environment.obj"),
        ("free3d", "sample_vehicle.3ds")
    ]
    
    for platform, filename in sample_assets:
        asset_file = assets_dir / platform / filename
        with open(asset_file, 'w') as f:
            f.write(f"# Sample {platform} asset: {filename}\n")
            f.write(f"# Created by Phase 1 setup\n")
            f.write(f"# Platform: {platform}\n")
            f.write(f"# Format: {Path(filename).suffix}\n")
        print(f"  ✅ {asset_file}")

def generate_setup_report():
    """Generate a setup report"""
    print("\n📊 Generating setup report...")
    
    integration_dir = Path(__file__).parent.parent
    assets_dir = integration_dir / "assets"
    
    # Count assets
    asset_counts = {}
    for platform_dir in ["opengameart", "free3d", "imported", "exports"]:
        platform_path = assets_dir / platform_dir
        if platform_path.exists():
            asset_counts[platform_dir] = len(list(platform_path.glob("*")))
        else:
            asset_counts[platform_dir] = 0
    
    # Create report
    report = {
        "setup_completed": True,
        "directories_created": len(list(assets_dir.rglob("*"))),
        "asset_counts": asset_counts,
        "integration_path": str(integration_dir),
        "assets_path": str(assets_dir)
    }
    
    # Save report
    report_file = assets_dir / "setup_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"  ✅ Setup report saved to: {report_file}")
    return report

def main():
    """Main setup function"""
    print("🚀 Phase 1 Setup")
    print("=" * 40)
    
    try:
        # Setup directories
        assets_dir = setup_directories()
        
        # Setup configuration
        config_dir = setup_configuration()
        
        # Test imports
        if not test_imports():
            print("\n❌ Import tests failed. Please check the source files.")
            return False
        
        # Create sample assets
        create_sample_assets()
        
        # Generate report
        report = generate_setup_report()
        
        print("\n🎉 Phase 1 setup complete!")
        print("=" * 40)
        print(f"📁 Assets directory: {assets_dir}")
        print(f"⚙️  Config directory: {config_dir}")
        print(f"📊 Total directories: {report['directories_created']}")
        print(f"📦 Sample assets created: {sum(report['asset_counts'].values())}")
        
        print("\n🚀 Next steps:")
        print("  1. Run tests: python tests/test_phase1.py")
        print("  2. Run workflow: python scripts/run_phase1_workflow.py")
        print("  3. Check documentation: docs/phase1-quickstart.md")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

