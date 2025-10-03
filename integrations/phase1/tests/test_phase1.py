#!/usr/bin/env python3
"""
Phase 1 Test Script
Tests the Phase 1 asset integration setup
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to the path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

def test_directory_structure():
    """Test that required directories are created"""
    print("🔍 Testing Directory Structure...")
    
    # Create directories first
    from phase1_asset_importer import Phase1AssetImporter
    from blender_mcp_phase1 import Phase1BlenderIntegration
    
    # Initialize both classes to create directories
    importer = Phase1AssetImporter()
    integration = Phase1BlenderIntegration()
    
    # Get the integration directory
    integration_dir = Path(__file__).parent.parent
    base_dir = integration_dir / "assets"
    
    required_dirs = [
        str(base_dir),
        str(base_dir / "opengameart"),
        str(base_dir / "free3d")
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory}")
            all_exist = False
    
    return all_exist

def test_asset_importer():
    """Test the asset importer functionality"""
    print("\n🔍 Testing Asset Importer...")
    
    try:
        from phase1_asset_importer import Phase1AssetImporter
        
        importer = Phase1AssetImporter()
        
        # Test platform configurations
        platforms = importer.platforms
        print(f"  ✅ Found {len(platforms)} platforms")
        
        for platform_id, platform_info in platforms.items():
            print(f"    - {platform_info['name']}: {len(platform_info['supported_formats'])} formats")
        
        # Test directory creation
        if os.path.exists(importer.download_dir):
            print(f"  ✅ Download directory exists: {importer.download_dir}")
        else:
            print(f"  ❌ Download directory missing: {importer.download_dir}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Failed to import Phase1AssetImporter: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing asset importer: {e}")
        return False

def test_blender_integration():
    """Test the Blender integration"""
    print("\n🔍 Testing Blender Integration...")
    
    try:
        from blender_mcp_phase1 import Phase1BlenderIntegration
        
        integration = Phase1BlenderIntegration()
        
        # Test directory structure
        for platform, directory in integration.asset_directories.items():
            if os.path.exists(directory):
                print(f"  ✅ {platform} directory: {directory}")
            else:
                print(f"  ❌ {platform} directory missing: {directory}")
                return False
        
        # Test asset discovery
        assets = integration.get_available_assets()
        print(f"  ✅ Asset discovery working: {len(assets)} platform(s)")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Failed to import Phase1BlenderIntegration: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing Blender integration: {e}")
        return False

def test_workflow_runner():
    """Test the workflow runner"""
    print("\n🔍 Testing Workflow Runner...")
    
    try:
        # Add scripts directory to path
        scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        sys.path.insert(0, scripts_path)
        
        from run_phase1_workflow import Phase1WorkflowRunner
        
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
        print(f"  ❌ Failed to import Phase1WorkflowRunner: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing workflow runner: {e}")
        return False

def test_file_permissions():
    """Test file permissions for asset directories"""
    print("\n🔍 Testing File Permissions...")
    
    home_dir = os.path.expanduser("~")
    test_dir = os.path.join(home_dir, "3d_assets", "phase1", "test")
    
    try:
        # Create test directory
        Path(test_dir).mkdir(parents=True, exist_ok=True)
        
        # Test write permission
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        # Test read permission
        with open(test_file, 'r') as f:
            content = f.read()
        
        if content == "test":
            print("  ✅ File permissions working")
            
            # Cleanup
            os.remove(test_file)
            os.rmdir(test_dir)
            
            return True
        else:
            print("  ❌ File content mismatch")
            return False
            
    except Exception as e:
        print(f"  ❌ File permission test failed: {e}")
        return False

def run_all_tests():
    """Run all Phase 1 tests"""
    print("🧪 Phase 1 Integration Tests")
    print("=" * 40)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Asset Importer", test_asset_importer),
        ("Blender Integration", test_blender_integration),
        ("Workflow Runner", test_workflow_runner),
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
        print("🚀 You can now run: python scripts/run_phase1_workflow.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("🔧 Fix the issues before proceeding to Phase 2.")
    
    return passed == total

def main():
    """Main test function"""
    success = run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
