#!/usr/bin/env python3
"""
Phase 3: Game Development Integration Main Entry Point
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from phase3_asset_importer import Phase3AssetImporter
from blender_mcp_phase3 import Phase3BlenderIntegration

def main():
    """Main entry point for Phase 3 operations"""
    if len(sys.argv) < 2:
        print("Phase 3: Game Development Integration")
        print("=" * 50)
        print("Usage: python main.py <command> [options]")
        print("\nCommands:")
        print("  setup     - Set up Phase 3 environment")
        print("  test      - Run Phase 3 tests")
        print("  workflow  - Run Phase 3 workflow")
        print("  status    - Check Phase 3 status")
        print("\nExamples:")
        print("  python main.py setup")
        print("  python main.py test")
        print("  python main.py workflow character weapon environment")
        print("  python main.py status")
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_phase3()
    elif command == "test":
        test_phase3()
    elif command == "workflow":
        search_terms = sys.argv[2:] if len(sys.argv) > 2 else ["character", "weapon", "environment"]
        run_workflow(search_terms)
    elif command == "status":
        check_status()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py' to see available commands")

def setup_phase3():
    """Set up Phase 3 environment"""
    print("🎯 Setting up Phase 3: Game Development Integration")
    print("=" * 60)
    
    # Initialize importer
    importer = Phase3AssetImporter()
    print(f"✅ Asset importer initialized")
    print(f"   Download directory: {importer.download_dir}")
    
    # Initialize Blender integration
    integration = Phase3BlenderIntegration()
    print(f"✅ Blender integration initialized")
    
    # Check authentication
    print(f"\n🔐 Authentication Status:")
    for platform in ["unity", "mixamo"]:
        if platform in integration.auth_credentials:
            print(f"   {platform}: ✅ Authenticated")
        else:
            print(f"   {platform}: ❌ Not authenticated")
            print(f"      Set environment variable: {platform.upper()}_ID")
    
    print(f"\n✅ Phase 3 setup complete!")

def test_phase3():
    """Run Phase 3 tests"""
    print("🧪 Running Phase 3 Tests")
    print("=" * 40)
    
    # Initialize components
    importer = Phase3AssetImporter()
    integration = Phase3BlenderIntegration()
    
    # Test asset importer
    print("Testing asset importer...")
    try:
        # Test search functionality
        unity_assets = importer.search_unity_asset_store("test", limit=2)
        print(f"   Unity search: ✅ Found {len(unity_assets)} assets")
        
        mixamo_assets = importer.search_mixamo("test", limit=2)
        print(f"   Mixamo search: ✅ Found {len(mixamo_assets)} assets")
        
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
        if integration.setup_game_scene():
            print(f"   Game scene setup: ✅ Success")
        else:
            print(f"   Game scene setup: ❌ Failed")
        
    except Exception as e:
        print(f"   Blender integration: ❌ Error - {e}")
    
    print(f"\n✅ Phase 3 tests completed!")

def run_workflow(search_terms):
    """Run Phase 3 workflow with search terms"""
    print(f"🚀 Running Phase 3 Workflow")
    print(f"Search terms: {', '.join(search_terms)}")
    print("=" * 50)
    
    # Initialize importer
    importer = Phase3AssetImporter()
    
    # Run workflow
    results = importer.run_phase3_workflow(search_terms)
    
    # Print results
    print(f"\n📊 Workflow Results:")
    print(f"   Assets found: {results['assets_found']}")
    print(f"   Assets downloaded: {results['assets_downloaded']}")
    print(f"   Assets imported: {results['assets_imported']}")
    print(f"   Game-ready assets: {results['game_ready_assets']}")
    print(f"   Animated assets: {results['animated_assets']}")
    print(f"   Platforms used: {', '.join(results['platforms_used'])}")
    
    if results['auth_required']:
        print(f"\n🔐 Authentication required for: {', '.join(results['auth_required'])}")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    print(f"\n✅ Phase 3 workflow completed!")

def check_status():
    """Check Phase 3 status"""
    print("📊 Phase 3 Status")
    print("=" * 30)
    
    # Initialize components
    importer = Phase3AssetImporter()
    integration = Phase3BlenderIntegration()
    
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
    for platform in ["unity", "mixamo"]:
        if platform in integration.auth_credentials:
            print(f"   {platform}: ✅ Authenticated")
        else:
            print(f"   {platform}: ❌ Not authenticated")
    
    # Check asset library
    print(f"\n📚 Asset Library:")
    library = importer.create_asset_library()
    print(f"   Total assets: {library['metadata']['total_assets']}")
    print(f"   Game-ready assets: {library['metadata']['game_ready_assets']}")
    print(f"   Animated assets: {library['metadata']['animated_assets']}")
    
    print(f"\n✅ Phase 3 status check complete!")

if __name__ == "__main__":
    main()
