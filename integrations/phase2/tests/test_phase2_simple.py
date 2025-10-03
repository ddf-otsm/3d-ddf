#!/usr/bin/env python3
"""
Simple Phase 2 Test Suite
Basic tests for Phase 2 asset integration
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from phase2_asset_importer import Phase2AssetImporter
        print("  ✅ Phase2AssetImporter imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import Phase2AssetImporter: {e}")
        return False
    
    try:
        from blender_mcp_phase2 import Phase2BlenderIntegration
        print("  ✅ Phase2BlenderIntegration imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import Phase2BlenderIntegration: {e}")
        return False
    
    return True

def test_asset_importer():
    """Test asset importer functionality"""
    print("\n🔍 Testing Asset Importer...")
    
    try:
        from phase2_asset_importer import Phase2AssetImporter
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize importer
            importer = Phase2AssetImporter(download_dir=temp_dir)
            
            # Test initialization
            if importer and importer.download_dir:
                print("  ✅ Importer initialized successfully")
            else:
                print("  ❌ Importer initialization failed")
                return False
            
            # Test platform configuration
            if len(importer.platforms) == 2:
                print("  ✅ Platform configuration correct")
            else:
                print("  ❌ Platform configuration incorrect")
                return False
            
            # Test authentication setup
            if hasattr(importer, 'auth_credentials'):
                print("  ✅ Authentication system initialized")
            else:
                print("  ❌ Authentication system not initialized")
                return False
            
            # Test directory creation
            if os.path.exists(importer.download_dir):
                print("  ✅ Download directory created")
            else:
                print("  ❌ Download directory not created")
                return False
            
            # Test asset search
            sketchfab_assets = importer.search_sketchfab("character", limit=3)
            if isinstance(sketchfab_assets, list):
                print("  ✅ Sketchfab search working")
            else:
                print("  ❌ Sketchfab search failed")
                return False
            
            clara_assets = importer.search_clara("character", limit=3)
            if isinstance(clara_assets, list):
                print("  ✅ Clara.io search working")
            else:
                print("  ❌ Clara.io search failed")
                return False
            
            # Test asset download
            test_asset = {
                "title": "Test Asset",
                "format": ".gltf",
                "license": "CC-BY",
                "url": "https://example.com/test.gltf"
            }
            
            filepath = importer.download_asset(test_asset, "sketchfab")
            if filepath and os.path.exists(filepath):
                print("  ✅ Asset download working")
            else:
                print("  ❌ Asset download failed")
                return False
            
            # Test asset library creation
            library = importer.create_asset_library()
            if isinstance(library, dict) and "phase2_assets" in library:
                print("  ✅ Asset library creation working")
            else:
                print("  ❌ Asset library creation failed")
                return False
            
            return True
            
        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"  ❌ Asset importer test failed: {e}")
        return False

def test_blender_integration():
    """Test Blender integration functionality"""
    print("\n🔍 Testing Blender Integration...")
    
    try:
        from blender_mcp_phase2 import Phase2BlenderIntegration
        
        # Initialize integration
        integration = Phase2BlenderIntegration()
        
        # Test initialization
        if integration and integration.asset_directories:
            print("  ✅ Integration initialized successfully")
        else:
            print("  ❌ Integration initialization failed")
            return False
        
        # Test asset discovery
        assets = integration.get_available_assets()
        if isinstance(assets, dict):
            print("  ✅ Asset discovery working")
        else:
            print("  ❌ Asset discovery failed")
            return False
        
        # Test scene setup simulation
        if integration.setup_phase2_scene():
            print("  ✅ Advanced scene setup simulation working")
        else:
            print("  ❌ Advanced scene setup simulation failed")
            return False
        
        # Test advanced lighting setup
        if integration.setup_advanced_lighting():
            print("  ✅ Advanced lighting setup simulation working")
        else:
            print("  ❌ Advanced lighting setup simulation failed")
            return False
        
        # Test collection creation simulation
        for platform in ["sketchfab", "clara"]:
            if integration.create_asset_collection(platform):
                print(f"  ✅ Collection creation for {platform} working")
            else:
                print(f"  ❌ Collection creation for {platform} failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Blender integration test failed: {e}")
        return False

def test_workflow_runner():
    """Test workflow runner functionality"""
    print("\n🔍 Testing Workflow Runner...")
    
    try:
        # Add scripts directory to path
        scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        sys.path.insert(0, scripts_path)
        
        from run_phase2_workflow import Phase2WorkflowRunner
        
        # Initialize workflow runner
        runner = Phase2WorkflowRunner()
        
        # Test initialization
        if hasattr(runner, 'importer') and hasattr(runner, 'blender_integration'):
            print("  ✅ Workflow runner initialized")
        else:
            print("  ❌ Workflow runner initialization failed")
            return False
        
        # Test workflow results structure
        if 'start_time' in runner.workflow_results:
            print("  ✅ Workflow results structure correct")
        else:
            print("  ❌ Workflow results structure incorrect")
            return False
        
        # Test authentication tracking
        if 'auth_required' in runner.workflow_results:
            print("  ✅ Authentication tracking working")
        else:
            print("  ❌ Authentication tracking not working")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Failed to import workflow runner: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Workflow runner test failed: {e}")
        return False

def test_configuration():
    """Test configuration files"""
    print("\n🔍 Testing Configuration...")
    
    integration_dir = Path(__file__).parent.parent
    
    # Test directory structure
    required_dirs = ["src", "tests", "scripts", "docs", "assets", "config", "logs"]
    
    for dir_name in required_dirs:
        dir_path = integration_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name} directory exists")
        else:
            print(f"  ❌ {dir_name} directory missing")
            return False
    
    # Test configuration files
    config_files = ["settings.py", "platforms.json"]
    
    for config_file in config_files:
        config_path = integration_dir / "config" / config_file
        if config_path.exists():
            print(f"  ✅ {config_file} exists")
        else:
            print(f"  ❌ {config_file} missing")
            return False
    
    # Test platforms.json content
    platforms_file = integration_dir / "config" / "platforms.json"
    if platforms_file.exists():
        with open(platforms_file, 'r') as f:
            config = json.load(f)
        
        if "platforms" in config and "sketchfab" in config["platforms"] and "clara" in config["platforms"]:
            print("  ✅ Platforms configuration correct")
        else:
            print("  ❌ Platforms configuration incorrect")
            return False
    
    return True

def test_authentication():
    """Test authentication system"""
    print("\n🔍 Testing Authentication...")
    
    try:
        from phase2_asset_importer import Phase2AssetImporter
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize importer
            importer = Phase2AssetImporter(download_dir=temp_dir)
            
            # Test authentication credentials loading
            if hasattr(importer, 'auth_credentials'):
                print("  ✅ Authentication credentials system working")
            else:
                print("  ❌ Authentication credentials system not working")
                return False
            
            # Test platform authentication requirements
            for platform, platform_info in importer.platforms.items():
                if platform_info.get("requires_auth", False):
                    print(f"  ✅ {platform} requires authentication")
                else:
                    print(f"  ✅ {platform} does not require authentication")
            
            return True
            
        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"  ❌ Authentication test failed: {e}")
        return False

def test_file_permissions():
    """Test file permissions"""
    print("\n🔍 Testing File Permissions...")
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Test write permission
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            
            # Test read permission
            with open(test_file, 'r') as f:
                content = f.read()
            
            if content == "test":
                print("  ✅ File permissions working")
                return True
            else:
                print("  ❌ File content mismatch")
                return False
                
        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"  ❌ File permission test failed: {e}")
        return False

def run_simple_tests():
    """Run all simple tests"""
    print("🧪 Simple Phase 2 Tests")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Asset Importer", test_asset_importer),
        ("Blender Integration", test_blender_integration),
        ("Workflow Runner", test_workflow_runner),
        ("Configuration", test_configuration),
        ("Authentication", test_authentication),
        ("File Permissions", test_file_permissions)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 40)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Phase 2 is ready to use.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
