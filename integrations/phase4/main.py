#!/usr/bin/env python3
"""
Phase 4: Professional Marketplace Integration Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from phase4_asset_importer import Phase4AssetImporter
from blender_mcp_phase4 import Phase4BlenderIntegration

def main():
    """Main entry point for Phase 4 operations"""
    if len(sys.argv) < 2:
        print("Phase 4: Professional Marketplace Integration")
        print("=" * 60)
        print("Usage: python main.py <command> [options]")
        print("\nCommands:")
        print("  setup     - Set up Phase 4 environment")
        print("  test      - Run Phase 4 tests")
        print("  workflow  - Run Phase 4 workflow")
        print("  status    - Check Phase 4 status")
        print("\nExamples:")
        print("  python main.py setup")
        print("  python main.py test")
        print("  python main.py workflow architecture character vehicle")
        print("  python main.py status")
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_phase4()
    elif command == "test":
        test_phase4()
    elif command == "workflow":
        search_terms = sys.argv[2:] if len(sys.argv) > 2 else ["architecture", "character", "vehicle"]
        run_workflow(search_terms)
    elif command == "status":
        check_status()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py' to see available commands")

def setup_phase4():
    """Set up Phase 4 environment"""
    print("🎯 Setting up Phase 4: Professional Marketplace Integration")
    print("=" * 70)
    
    # Initialize importer
    importer = Phase4AssetImporter()
    print(f"✅ Asset importer initialized")
    print(f"   Download directory: {importer.download_dir}")
    
    # Initialize Blender integration
    integration = Phase4BlenderIntegration()
    print(f"✅ Blender integration initialized")
    
    # Check authentication
    print(f"\n🔐 Authentication Status:")
    for platform in ["cgtrader", "turbosquid", "unreal"]:
        if platform in integration.auth_credentials:
            print(f"   {platform}: ✅ Authenticated")
        else:
            print(f"   {platform}: ❌ Not authenticated")
            print(f"      Set environment variable: {platform.upper()}_API_KEY")
    
    print(f"\n✅ Phase 4 setup complete!")

def test_phase4():
    """Run Phase 4 tests"""
    print("🧪 Running Phase 4 Tests")
    print("=" * 40)
    
    # Initialize components
    importer = Phase4AssetImporter()
    integration = Phase4BlenderIntegration()
    
    # Test asset importer
    print("Testing asset importer...")
    try:
        # Test search functionality
        cgtrader_assets = importer.search_cgtrader("test", limit=2)
        print(f"   CGTrader search: ✅ Found {len(cgtrader_assets)} assets")
        
        turbosquid_assets = importer.search_turbosquid("test", limit=2)
        print(f"   TurboSquid search: ✅ Found {len(turbosquid_assets)} assets")
        
        unreal_assets = importer.search_unreal_marketplace("test", limit=2)
        print(f"   Unreal Marketplace search: ✅ Found {len(unreal_assets)} assets")
        
        # Test library creation
        library = importer.create_asset_library()
        print(f"   Asset library: ✅ Created with {library['metadata']['total_assets']} assets")
        
    except Exception as e:
        print(f"   Asset importer: ❌ Error - {e}")
    
    # Test Blender integration
    print("Testing Blender integration...")
    try:
        # Test asset listing
        assets = integration.get_available_assets()
        total_assets = sum(len(platform_assets) for platform_assets in assets.values())
        print(f"   Available assets: ✅ Found {total_assets} assets")
        
        # Test environment setup
        if integration.setup_professional_scene():
            print(f"   Professional scene setup: ✅ Success")
        else:
            print(f"   Professional scene setup: ❌ Failed")
        
    except Exception as e:
        print(f"   Blender integration: ❌ Error - {e}")
    
    print(f"\n✅ Phase 4 tests completed!")

def run_workflow(search_terms):
    """Run Phase 4 workflow with search terms"""
    print(f"🚀 Running Phase 4 Workflow")
    print(f"Search terms: {', '.join(search_terms)}")
    print("=" * 50)
    
    # Initialize importer
    importer = Phase4AssetImporter()
    
    # Run workflow
    results = importer.run_phase4_workflow(search_terms)
    
    # Print results
    print(f"\n📊 Workflow Results:")
    print(f"   Assets found: {results['assets_found']}")
    print(f"   Assets downloaded: {results['assets_downloaded']}")
    print(f"   Assets imported: {results['assets_imported']}")
    print(f"   Commercial assets: {results['commercial_assets']}")
    print(f"   Total value: ${results['total_value']:.2f}")
    print(f"   Platforms used: {', '.join(results['platforms_used'])}")
    
    if results['auth_required']:
        print(f"\n🔐 Authentication required for: {', '.join(results['auth_required'])}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    print(f"\n✅ Phase 4 workflow completed!")

def check_status():
    """Check Phase 4 status"""
    print("📊 Phase 4 Status")
    print("=" * 30)
    
    # Initialize components
    importer = Phase4AssetImporter()
    integration = Phase4BlenderIntegration()
    
    # Check directories
    print("📁 Directories:")
    for platform, directory in integration.asset_directories.items():
        if os.path.exists(directory):
            file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
            print(f"   {platform}: ✅ {directory} ({file_count} files)")
        else:
            print(f"   {platform}: ❌ {directory} (not found)")
    
    # Check authentication
    print(f"\n🔐 Authentication:")
    for platform in ["cgtrader", "turbosquid", "unreal"]:
        if platform in integration.auth_credentials:
            print(f"   {platform}: ✅ Authenticated")
        else:
            print(f"   {platform}: ❌ Not authenticated")
    
    # Check asset library
    print(f"\n📚 Asset Library:")
    library = importer.create_asset_library()
    print(f"   Total assets: {library['metadata']['total_assets']}")
    print(f"   Commercial assets: {library['metadata']['commercial_assets']}")
    print(f"   High-poly assets: {library['metadata']['high_poly_assets']}")
    print(f"   Total value: ${library['metadata']['total_value']:.2f}")
    
    print(f"\n✅ Phase 4 status check complete!")

if __name__ == "__main__":
    main()
