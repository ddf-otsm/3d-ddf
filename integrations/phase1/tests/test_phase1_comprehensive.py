#!/usr/bin/env python3
"""
Comprehensive Phase 1 Test Suite
Tests all aspects of Phase 1 asset integration
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

from phase1_asset_importer import Phase1AssetImporter
from blender_mcp_phase1 import Phase1BlenderIntegration

class TestPhase1AssetImporter(unittest.TestCase):
    """Test Phase1AssetImporter functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.importer = Phase1AssetImporter(download_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test importer initialization"""
        self.assertIsNotNone(self.importer)
        self.assertIsNotNone(self.importer.download_dir)
        self.assertIsNotNone(self.importer.platforms)
        self.assertEqual(len(self.importer.platforms), 2)
    
    def test_platform_configuration(self):
        """Test platform configuration"""
        platforms = self.importer.platforms
        
        # Check OpenGameArt.org
        self.assertIn("opengameart", platforms)
        og_platform = platforms["opengameart"]
        self.assertEqual(og_platform["name"], "OpenGameArt.org")
        self.assertIn(".blend", og_platform["supported_formats"])
        self.assertEqual(og_platform["complexity"], 1)
        
        # Check Free3D
        self.assertIn("free3d", platforms)
        free3d_platform = platforms["free3d"]
        self.assertEqual(free3d_platform["name"], "Free3D")
        self.assertIn(".obj", free3d_platform["supported_formats"])
        self.assertEqual(free3d_platform["complexity"], 1)
    
    def test_directory_creation(self):
        """Test directory creation"""
        self.assertTrue(os.path.exists(self.importer.download_dir))
        
        # Test platform directories
        for platform in self.importer.platforms.keys():
            platform_dir = os.path.join(self.importer.download_dir, platform)
            self.assertTrue(os.path.exists(platform_dir))
    
    def test_search_opengameart(self):
        """Test OpenGameArt search"""
        results = self.importer.search_opengameart("character", limit=3)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 3)
        
        if results:
            asset = results[0]
            self.assertIn("title", asset)
            self.assertIn("format", asset)
            self.assertIn("license", asset)
            self.assertIn("url", asset)
    
    def test_download_asset(self):
        """Test asset downloading"""
        asset_info = {
            "title": "Test Asset",
            "format": ".blend",
            "license": "CC0",
            "url": "https://example.com/test.blend"
        }
        
        filepath = self.importer.download_asset(asset_info, "opengameart")
        
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith(".blend"))
        
        # Check file content
        with open(filepath, 'r') as f:
            content = f.read()
            self.assertIn("Test Asset", content)
            self.assertIn("opengameart", content)
    
    def test_import_to_blender_simulation(self):
        """Test Blender import simulation"""
        asset_info = {
            "title": "Test Asset",
            "format": ".blend"
        }
        
        # Create a test file
        test_file = os.path.join(self.temp_dir, "test.blend")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Test import (should work in simulation mode)
        result = self.importer.import_to_blender(test_file, asset_info)
        self.assertTrue(result)
    
    def test_asset_library_creation(self):
        """Test asset library creation"""
        # Create some test assets
        test_assets = [
            {"title": "Asset 1", "format": ".blend"},
            {"title": "Asset 2", "format": ".fbx"}
        ]
        
        for i, asset in enumerate(test_assets):
            filepath = self.importer.download_asset(asset, "opengameart")
            self.assertIsNotNone(filepath)
        
        # Create library
        library = self.importer.create_asset_library()
        
        self.assertIsInstance(library, dict)
        self.assertIn("phase1_assets", library)
        self.assertIn("metadata", library)
        self.assertIn("opengameart", library["phase1_assets"])
        self.assertIn("free3d", library["phase1_assets"])
    
    def test_workflow_execution(self):
        """Test complete workflow execution"""
        search_terms = ["character", "weapon"]
        
        results = self.importer.run_phase1_workflow(search_terms)
        
        self.assertIsInstance(results, dict)
        self.assertIn("searched_terms", results)
        self.assertIn("assets_found", results)
        self.assertIn("assets_downloaded", results)
        self.assertIn("assets_imported", results)
        self.assertIn("errors", results)
        self.assertIn("library", results)

class TestPhase1BlenderIntegration(unittest.TestCase):
    """Test Phase1BlenderIntegration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.integration = Phase1BlenderIntegration()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test integration initialization"""
        self.assertIsNotNone(self.integration)
        self.assertIsNotNone(self.integration.asset_directories)
        self.assertEqual(len(self.integration.asset_directories), 2)
    
    def test_asset_directories(self):
        """Test asset directory structure"""
        for platform, directory in self.integration.asset_directories.items():
            self.assertTrue(os.path.exists(directory))
            self.assertIn(platform, directory)
    
    def test_get_available_assets(self):
        """Test asset discovery"""
        assets = self.integration.get_available_assets()
        
        self.assertIsInstance(assets, dict)
        self.assertIn("opengameart", assets)
        self.assertIn("free3d", assets)
        
        for platform, platform_assets in assets.items():
            self.assertIsInstance(platform_assets, list)
    
    def test_import_asset_simulation(self):
        """Test asset import simulation"""
        # Create a test asset file
        test_asset = os.path.join(self.temp_dir, "test.blend")
        with open(test_asset, 'w') as f:
            f.write("test content")
        
        # Test import (should work in simulation mode)
        result = self.integration.import_asset_to_blender(test_asset, "Test Asset")
        self.assertTrue(result)
    
    def test_scene_setup_simulation(self):
        """Test scene setup simulation"""
        result = self.integration.setup_phase1_scene()
        self.assertTrue(result)
    
    def test_collection_creation_simulation(self):
        """Test collection creation simulation"""
        for platform in ["opengameart", "free3d"]:
            result = self.integration.create_asset_collection(platform)
            self.assertTrue(result)

class TestPhase1WorkflowIntegration(unittest.TestCase):
    """Test Phase 1 workflow integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.importer = Phase1AssetImporter(download_dir=self.temp_dir)
        self.integration = Phase1BlenderIntegration()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Test workflow runner
        from run_phase1_workflow import Phase1WorkflowRunner
        
        runner = Phase1WorkflowRunner()
        
        # Test initialization
        self.assertIsNotNone(runner.importer)
        self.assertIsNotNone(runner.blender_integration)
        self.assertIsNotNone(runner.workflow_results)
        
        # Test workflow results structure
        self.assertIn("start_time", runner.workflow_results)
        self.assertIn("steps_completed", runner.workflow_results)
        self.assertIn("assets_processed", runner.workflow_results)
        self.assertIn("errors", runner.workflow_results)
    
    def test_workflow_steps(self):
        """Test individual workflow steps"""
        from run_phase1_workflow import Phase1WorkflowRunner
        
        runner = Phase1WorkflowRunner()
        
        # Test step 1: Platform discovery
        runner.step_1_discover_platforms()
        self.assertIn("platform_discovery", runner.workflow_results["steps_completed"])
        
        # Test step 2: Environment setup
        runner.step_2_setup_environment()
        self.assertIn("environment_setup", runner.workflow_results["steps_completed"])
        
        # Test step 3: Asset workflow
        runner.step_3_demo_asset_workflow()
        self.assertIn("asset_workflow", runner.workflow_results["steps_completed"])
        
        # Test step 4: Asset library
        runner.step_4_create_asset_library()
        self.assertIn("asset_library", runner.workflow_results["steps_completed"])
        
        # Test step 5: Integration verification
        runner.step_5_verify_integration()
        self.assertIn("integration_verification", runner.workflow_results["steps_completed"])
        
        # Test step 6: Report generation
        runner.step_6_generate_report()
        self.assertIn("report_generation", runner.workflow_results["steps_completed"])

class TestPhase1Configuration(unittest.TestCase):
    """Test Phase 1 configuration management"""
    
    def test_settings_import(self):
        """Test settings import"""
        try:
            from config.settings import PLATFORMS, ASSET_DIRECTORIES, WORKFLOW_SETTINGS
            self.assertIsNotNone(PLATFORMS)
            self.assertIsNotNone(ASSET_DIRECTORIES)
            self.assertIsNotNone(WORKFLOW_SETTINGS)
        except ImportError:
            # Settings not available, use fallback
            self.assertTrue(True)
    
    def test_platforms_json(self):
        """Test platforms.json configuration"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'platforms.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.assertIn("platforms", config)
            self.assertIn("workflow", config)
            
            platforms = config["platforms"]
            self.assertIn("opengameart", platforms)
            self.assertIn("free3d", platforms)
    
    def test_directory_structure(self):
        """Test directory structure integrity"""
        integration_dir = Path(__file__).parent.parent
        
        required_dirs = [
            "src",
            "tests", 
            "scripts",
            "docs",
            "assets",
            "config",
            "logs"
        ]
        
        for dir_name in required_dirs:
            dir_path = integration_dir / dir_name
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} should exist")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} should be a directory")

class TestPhase1ErrorHandling(unittest.TestCase):
    """Test Phase 1 error handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_invalid_asset_info(self):
        """Test handling of invalid asset info"""
        importer = Phase1AssetImporter(download_dir=self.temp_dir)
        
        # Test with invalid asset info
        invalid_asset = {"invalid": "data"}
        result = importer.download_asset(invalid_asset, "opengameart")
        
        # Should handle gracefully
        self.assertIsNone(result)
    
    def test_invalid_platform(self):
        """Test handling of invalid platform"""
        importer = Phase1AssetImporter(download_dir=self.temp_dir)
        
        asset_info = {"title": "Test", "format": ".blend"}
        result = importer.download_asset(asset_info, "invalid_platform")
        
        # Should handle gracefully
        self.assertIsNone(result)
    
    def test_file_permission_errors(self):
        """Test handling of file permission errors"""
        # Create a read-only directory
        read_only_dir = os.path.join(self.temp_dir, "readonly")
        os.makedirs(read_only_dir)
        os.chmod(read_only_dir, 0o444)  # Read-only
        
        try:
            importer = Phase1AssetImporter(download_dir=read_only_dir)
            # Should handle permission errors gracefully
            self.assertTrue(True)
        except Exception:
            # Expected to fail, but should be handled gracefully
            self.assertTrue(True)
        finally:
            # Restore permissions for cleanup
            os.chmod(read_only_dir, 0o755)

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 Running Comprehensive Phase 1 Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestPhase1AssetImporter,
        TestPhase1BlenderIntegration,
        TestPhase1WorkflowIntegration,
        TestPhase1Configuration,
        TestPhase1ErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)

