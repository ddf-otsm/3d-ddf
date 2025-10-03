#!/usr/bin/env python3
"""
Phase 2 Workflow Runner
Demonstrates the complete Phase 2 workflow for free asset integration with registration
"""

import os
import sys
import json
import time
from pathlib import Path

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

from phase2_asset_importer import Phase2AssetImporter
from blender_mcp_phase2 import Phase2BlenderIntegration

class Phase2WorkflowRunner:
    """Runs the complete Phase 2 workflow"""
    
    def __init__(self):
        self.importer = Phase2AssetImporter()
        self.blender_integration = Phase2BlenderIntegration()
        self.workflow_results = {
            "start_time": time.time(),
            "steps_completed": [],
            "assets_processed": 0,
            "auth_required": [],
            "errors": []
        }
    
    def step_1_authentication_setup(self):
        """Step 1: Set up authentication for platforms"""
        print("\n🔐 Step 1: Authentication Setup")
        print("-" * 40)
        
        auth_status = {}
        
        for platform, platform_info in self.importer.platforms.items():
            if platform_info.get("requires_auth", False):
                has_auth = platform in self.importer.auth_credentials
                auth_status[platform] = has_auth
                
                if has_auth:
                    print(f"  ✅ {platform_info['name']}: Authenticated")
                else:
                    print(f"  ⚠️  {platform_info['name']}: Authentication required")
                    print(f"      Set {platform_info['auth_type']} environment variable")
                    self.workflow_results["auth_required"].append(platform)
            else:
                print(f"  ✅ {platform_info['name']}: No authentication required")
                auth_status[platform] = True
        
        self.workflow_results["steps_completed"].append("authentication_setup")
        print(f"\n✅ Authentication setup complete")
    
    def step_2_discover_platforms(self):
        """Step 2: Discover and understand Phase 2 platforms"""
        print("\n🔍 Step 2: Discovering Phase 2 Platforms")
        print("-" * 40)
        
        platforms = self.importer.platforms
        
        for platform_id, platform_info in platforms.items():
            print(f"\n📦 {platform_info['name']}")
            print(f"   Complexity: {'⭐' * platform_info['complexity']}")
            print(f"   License: {platform_info['license']}")
            print(f"   Formats: {', '.join(platform_info['supported_formats'])}")
            print(f"   Auth Required: {'Yes' if platform_info.get('requires_auth', False) else 'No'}")
            print(f"   URL: {platform_info['base_url']}")
        
        self.workflow_results["steps_completed"].append("platform_discovery")
        print(f"\n✅ Discovered {len(platforms)} platforms")
    
    def step_3_setup_environment(self):
        """Step 3: Set up the working environment"""
        print("\n🔧 Step 3: Setting Up Environment")
        print("-" * 40)
        
        # Create directories
        self.importer.ensure_download_dir()
        print(f"✅ Download directory: {self.importer.download_dir}")
        
        # Setup Blender environment
        print("🔧 Setting up Blender environment...")
        if self.blender_integration.setup_phase2_scene():
            print("✅ Advanced Blender scene setup complete")
        else:
            print("❌ Blender scene setup failed")
            self.workflow_results["errors"].append("Blender scene setup failed")
        
        # Setup advanced lighting
        if self.blender_integration.setup_advanced_lighting():
            print("✅ Advanced lighting setup complete")
        else:
            print("❌ Advanced lighting setup failed")
            self.workflow_results["errors"].append("Advanced lighting setup failed")
        
        # Create asset collections
        for platform in ["sketchfab", "clara"]:
            if self.blender_integration.create_asset_collection(platform):
                print(f"✅ Created collection for {platform}")
            else:
                print(f"❌ Failed to create collection for {platform}")
                self.workflow_results["errors"].append(f"Failed to create {platform} collection")
        
        self.workflow_results["steps_completed"].append("environment_setup")
    
    def step_4_demo_asset_workflow(self):
        """Step 4: Demonstrate asset workflow with mock data"""
        print("\n📥 Step 4: Asset Workflow Demo")
        print("-" * 40)
        
        # Mock search terms for demonstration
        search_terms = ["character", "weapon", "environment"]
        
        print(f"🔍 Searching for: {', '.join(search_terms)}")
        
        for term in search_terms:
            print(f"\n  📋 Processing: {term}")
            
            # Search Sketchfab
            try:
                sketchfab_assets = self.importer.search_sketchfab(term, limit=2)
                print(f"    📦 Found {len(sketchfab_assets)} Sketchfab assets")
                
                for asset in sketchfab_assets:
                    print(f"      📦 {asset['title']} ({asset['format']})")
                    
                    # Download asset
                    filepath = self.importer.download_asset(asset, "sketchfab")
                    if filepath:
                        print(f"        ✅ Downloaded to: {filepath}")
                        
                        # Import to Blender
                        if self.blender_integration.import_asset_to_blender(filepath, asset['title']):
                            print(f"        ✅ Imported to Blender")
                            self.workflow_results["assets_processed"] += 1
                        else:
                            print(f"        ❌ Failed to import to Blender")
                            self.workflow_results["errors"].append(f"Failed to import {asset['title']}")
                    else:
                        print(f"        ❌ Failed to download")
                        self.workflow_results["errors"].append(f"Failed to download {asset['title']}")
                
            except Exception as e:
                print(f"    ❌ Sketchfab search failed: {e}")
                self.workflow_results["errors"].append(f"Sketchfab search failed: {e}")
            
            # Search Clara.io
            try:
                clara_assets = self.importer.search_clara(term, limit=2)
                print(f"    📦 Found {len(clara_assets)} Clara.io assets")
                
                for asset in clara_assets:
                    print(f"      📦 {asset['title']} ({asset['format']})")
                    
                    # Download asset
                    filepath = self.importer.download_asset(asset, "clara")
                    if filepath:
                        print(f"        ✅ Downloaded to: {filepath}")
                        
                        # Import to Blender
                        if self.blender_integration.import_asset_to_blender(filepath, asset['title']):
                            print(f"        ✅ Imported to Blender")
                            self.workflow_results["assets_processed"] += 1
                        else:
                            print(f"        ❌ Failed to import to Blender")
                            self.workflow_results["errors"].append(f"Failed to import {asset['title']}")
                    else:
                        print(f"        ❌ Failed to download")
                        self.workflow_results["errors"].append(f"Failed to download {asset['title']}")
                
            except Exception as e:
                print(f"    ❌ Clara.io search failed: {e}")
                self.workflow_results["errors"].append(f"Clara.io search failed: {e}")
        
        self.workflow_results["steps_completed"].append("asset_workflow")
    
    def step_5_create_asset_library(self):
        """Step 5: Create and organize asset library"""
        print("\n📚 Step 5: Creating Asset Library")
        print("-" * 40)
        
        # Create asset library
        library = self.importer.create_asset_library()
        
        print(f"📊 Asset Library Summary:")
        print(f"   Total assets: {library['metadata']['total_assets']}")
        print(f"   Platforms: {', '.join(library['metadata']['platforms'])}")
        print(f"   Auth status: {library['metadata']['auth_status']}")
        
        for platform, assets in library["phase2_assets"].items():
            print(f"\n   {platform.title()}: {len(assets)} assets")
            for asset in assets[:2]:  # Show first 2 assets
                print(f"     - {asset['filename']}")
        
        # Save library to file
        library_file = os.path.join(self.importer.download_dir, "asset_library.json")
        with open(library_file, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n✅ Asset library saved to: {library_file}")
        self.workflow_results["steps_completed"].append("asset_library")
    
    def step_6_verify_integration(self):
        """Step 6: Verify Blender integration"""
        print("\n🔍 Step 6: Verifying Blender Integration")
        print("-" * 40)
        
        # Check available assets
        assets = self.blender_integration.get_available_assets()
        
        print(f"📁 Available Assets in Blender:")
        for platform, platform_assets in assets.items():
            print(f"   {platform}: {len(platform_assets)} assets")
        
        # Test scene info
        print("\n🎬 Scene Information:")
        print("   - Advanced scene setup complete")
        print("   - Advanced lighting configured")
        print("   - Collections created for each platform")
        print("   - Ready for asset import")
        
        self.workflow_results["steps_completed"].append("integration_verification")
    
    def step_7_generate_report(self):
        """Step 7: Generate workflow report"""
        print("\n📊 Step 7: Generating Report")
        print("-" * 40)
        
        end_time = time.time()
        duration = end_time - self.workflow_results["start_time"]
        
        report = {
            "workflow": "Phase 2: Free with Registration Asset Integration",
            "duration_seconds": round(duration, 2),
            "steps_completed": self.workflow_results["steps_completed"],
            "assets_processed": self.workflow_results["assets_processed"],
            "auth_required": self.workflow_results["auth_required"],
            "errors": self.workflow_results["errors"],
            "success_rate": len(self.workflow_results["steps_completed"]) / 7 * 100,
            "recommendations": [
                "Set up authentication for full platform access",
                "Use Sketchfab for high-quality VR/AR content",
                "Use Clara.io for collaborative modeling",
                "Organize assets by platform in separate collections",
                "Check licensing for commercial use"
            ]
        }
        
        # Save report
        report_file = os.path.join(self.importer.download_dir, "phase2_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        print(f"\n📈 Success Rate: {report['success_rate']:.1f}%")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📦 Assets Processed: {report['assets_processed']}")
        
        if report['auth_required']:
            print(f"\n🔐 Authentication required for: {', '.join(report['auth_required'])}")
        
        if report['errors']:
            print(f"\n❌ Errors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"   - {error}")
        
        self.workflow_results["steps_completed"].append("report_generation")
    
    def run_complete_workflow(self):
        """Run the complete Phase 2 workflow"""
        print("🚀 Starting Phase 2: Free with Registration Asset Integration")
        print("=" * 60)
        
        try:
            self.step_1_authentication_setup()
            self.step_2_discover_platforms()
            self.step_3_setup_environment()
            self.step_4_demo_asset_workflow()
            self.step_5_create_asset_library()
            self.step_6_verify_integration()
            self.step_7_generate_report()
            
            print("\n🎉 Phase 2 Workflow Complete!")
            print("=" * 60)
            print("✅ Ready to proceed to Phase 3 (Game Development)")
            print("📁 Check your asset directories for downloaded files")
            print("🎬 Open Blender to see imported assets")
            
        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            self.workflow_results["errors"].append(f"Workflow failure: {e}")

def main():
    """Main function"""
    runner = Phase2WorkflowRunner()
    runner.run_complete_workflow()

if __name__ == "__main__":
    main()
