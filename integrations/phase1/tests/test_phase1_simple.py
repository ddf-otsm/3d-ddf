#!/usr/bin/env python3
"""
Simple Phase 1 Test Suite
Basic tests for Phase 1 asset integration
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

def test_asset_importer():
    """Test asset importer functionality"""
    print("\n🔍 Testing Asset Importer...")
    
    try:
        from phase1_asset_importer import Phase1AssetImporter
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize importer
            importer = Phase1AssetImporter(download_dir=temp_dir)
            
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
            
            # Test directory creation
            if os.path.exists(importer.download_dir):
                print("  ✅ Download directory created")
            else:
                print("  ❌ Download directory not created")
                return False
            
            # Test asset search
            assets = importer.search_opengameart("character", limit=3)
            if isinstance(assets, list):
                print("  ✅ Asset search working")
            else:
                print("  ❌ Asset search failed")
                return False
            
            # Test asset download
            test_asset = {
                "title": "Test Asset",
                "format": ".blend",
                "license": "CC0",
                "url": "https://example.com/test.blend"
            }
            
            filepath = importer.download_asset(test_asset, "opengameart")
            if filepath and os.path.exists(filepath):
                print("  ✅ Asset download working")
            else:
                print("  ❌ Asset download failed")
                return False
            
            # Test asset library creation
            library = importer.create_asset_library()
            if isinstance(library, dict) and "phase1_assets" in library:
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
        from blender_mcp_phase1 import Phase1BlenderIntegration
        
        # Initialize integration
        integration = Phase1BlenderIntegration()
        
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
        if integration.setup_phase1_scene():
            print("  ✅ Scene setup simulation working")
        else:
            print("  ❌ Scene setup simulation failed")
            return False
        
        # Test collection creation simulation
        for platform in ["opengameart", "free3d"]:
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
        
        from run_phase1_workflow import Phase1WorkflowRunner
        
        # Initialize workflow runner
        runner = Phase1WorkflowRunner()
        
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
    
    return True

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
    print("🧪 Simple Phase 1 Tests")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Asset Importer", test_asset_importer),
        ("Blender Integration", test_blender_integration),
        ("Workflow Runner", test_workflow_runner),
        ("Configuration", test_configuration),
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
        print("\n🎉 All tests passed! Phase 1 is ready to use.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
